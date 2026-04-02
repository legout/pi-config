#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

SENSITIVE_KEY_RE = re.compile(r"(api[_-]?key|token|secret|password)", re.IGNORECASE)
ENV_SENSITIVE_KEY_RE = re.compile(r"(key|token|secret|password)", re.IGNORECASE)


def sanitize_models(node):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k == "apiKey" and isinstance(v, str) and v.lower() != "none":
                out[k] = "__REQUIRED__"
            else:
                out[k] = sanitize_models(v)
        return out
    if isinstance(node, list):
        return [sanitize_models(v) for v in node]
    return node


def sanitize_web_search(node):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if isinstance(v, str) and SENSITIVE_KEY_RE.search(k):
                out[k] = "__REQUIRED__"
            else:
                out[k] = sanitize_web_search(v)
        return out
    if isinstance(node, list):
        return [sanitize_web_search(v) for v in node]
    return node


def sanitize_mcp(node, parent=None):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if parent == "headers" and k.lower() == "authorization" and isinstance(v, str):
                if v.lower().startswith("bearer "):
                    out[k] = "Bearer __REQUIRED__"
                else:
                    out[k] = "__REQUIRED__"
            elif parent == "env" and isinstance(v, str) and ENV_SENSITIVE_KEY_RE.search(k):
                out[k] = "__REQUIRED__"
            else:
                out[k] = sanitize_mcp(v, k)
        return out
    if isinstance(node, list):
        return [sanitize_mcp(v, parent) for v in node]
    return node


SANITIZERS = {
    "models": sanitize_models,
    "mcp": sanitize_mcp,
    "web-search": sanitize_web_search,
}


def main() -> int:
    if len(sys.argv) != 4 or sys.argv[1] not in SANITIZERS:
        print("usage: sanitize_configs.py {models|mcp|web-search} <src> <dst>", file=sys.stderr)
        return 2

    kind, src, dst = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    data = json.loads(src.read_text())
    sanitized = SANITIZERS[kind](data)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(sanitized, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
