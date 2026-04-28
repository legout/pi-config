# Secrets Handling

This file is for internal reference. For user-facing documentation, see [README.md](../README.md#required-api-keys).

## Files with `__REQUIRED__` placeholders

| Tracked file | Placeholders |
|---|---|
| `config/models.json` | `providers.openrouter.apiKey`, `providers.nvidia-nim.apiKey`, `providers.siemens.apiKey` |
| `config/mcp.json` | `mcpServers.zai-web-reader.headers.Authorization`, `mcpServers.zai-vision.env.Z_AI_API_KEY` |
| `config/web-search.json` | `geminiApiKey` |

## Local-only secret copies

When you run `./sync.sh export` on a configured machine, real secret-bearing copies are written to:

- `private/models.json`
- `private/mcp.json`
- `private/web-search.json`

`private/` is gitignored and **must never** be committed.

## Bootstrap helper

```bash
./bootstrap-secrets.sh status    # Check state
./bootstrap-secrets.sh capture   # Copy live → private/
./bootstrap-secrets.sh install   # Copy private/ → live
```

## Restore behavior

`restore.sh` prefers local `private/*.json` files when present.

If `private/` is missing, restore uses the sanitized tracked config and prints warnings. In that case you must re-add secrets locally (see README: [Setup on a Brand-New Machine](../README.md#setup-on-a-brand-new-machine)).

## Auth

`auth.json` is not exported or restored by this project.
