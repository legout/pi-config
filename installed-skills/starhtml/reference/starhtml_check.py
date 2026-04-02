#!/usr/bin/env python3
"""
starhtml-check — Static analyzer for StarHTML code.
Designed for LLM tool-call loops: minimal tokens, maximum signal.

Usage:
    python starhtml_check.py <file.py>
    python starhtml_check.py --code "..."
    python starhtml_check.py --fix <file.py>
    python starhtml_check.py --summary <file.py>
    python starhtml_check.py --help-llm
"""

import ast
import re
import sys
import argparse
import textwrap
from dataclasses import dataclass, field
from typing import Literal, Optional

HELP_LLM = textwrap.dedent("""
    # StarHTML Checker — LLM Integration Guide

    ## SEVERITY LEVELS (production-ready mindset)

    ### 🔴 ERROR (BLOCKER — do not ship)
    - **Broken code**: SyntaxError, NameError, reactivity broken
    - **Bugs**: UX issues, security risks, performance problems
    - **Action**: Fix ALL before deploying — production must be reliable

    ### 🟡 WARNING (REVIEW — may be intentional)
    - **Code quality**: Style, conventions, naming
    - **Potential issues**: Review to ensure it's intentional
    - **Action**: Review each case, document if keeping intentionally

    ## COMMANDS

        python starhtml_check.py <file.py>      # full analysis
        python starhtml_check.py --summary f.py # compact output (fewer tokens)
        python starhtml_check.py --fix f.py     # auto-fix safe issues
        python starhtml_check.py --code "..."   # analyze inline snippet
        python starhtml_check.py --help-llm     # this guide

    ## LLM WORKFLOW

    1. **Write** — Generate StarHTML component
    2. **Check** — Run: `python starhtml_check.py file.py`
    3. **Fix ERRORs** — Address all ERROR-level issues first
    4. **Re-run** — Repeat until no errors, then fix WARNINGs

    ## OUTPUT FORMAT

    - **ERRORS** — must fix, will break runtime or reactivity
    - **WARNINGS** — should fix, may cause subtle bugs or UX issues
    - **SUMMARY** — signal inventory + total counts

    ## ERROR CODES (must fix)

    - **E001** — positional arg after keyword → caught by Python parser
      GOT:  Div(cls="container", "Hello")
      FIX:  Div("Hello", cls="container")
      Note: This is a Python SyntaxError — your editor/IDE should catch it

    - **E002** — f-string in reactive attribute → static, won't update in browser
      GOT:  data_text=f"Count: {counter}"
      FIX:  data_text="Count: " + counter
            data_text=f("Count: {c}", c=counter)  # for 3+ signals

    - **E003** — f-string URL in HTTP action → Python-static, signal value not reactive
      GOT:  data_on_click=get(f"/api/{item_id}")
      FIX:  data_on_click=get("/api/item", id=item_id_sig)

    - **E004** — special chars (`:` `/` `[` `]`) in `data_class_*` keyword name → Python parse error
      GOT:  data_class_hover:bg-blue=sig
      FIX:  data_attr_class=sig.if_("hover:bg-blue-500", "")

    - **E005** — camelCase Signal name → must be snake_case
      GOT:  Signal("myCounter", 0)
      FIX:  Signal("my_counter", 0)

    - **E006** — `f()` helper used without import → NameError at runtime
      GOT:  (uses f() but no import)
      FIX:  from starhtml.datastar import f

    - **E007** — `data_attr_class` and `data_attr_cls` on same element → different behaviors
      GOT:  Div(data_attr_class=..., data_attr_cls=...)
      FIX:  Use only one (data_attr_class replaces, data_attr_cls adds)

    - **E008** — walrus `:=` Signal without outer parentheses → won't register as positional arg, breaks reactivity
      GOT:  name := Signal("name", "")
      FIX:  (name := Signal("name", ""))
      NOTE: Without parens, Signal is not passed to parent element!

    ## WARNING CODES (review — may be intentional)

    - **W003** — 3+ signals with `&` operator — prefer `all()` for readability
      GOT:  a & b & c  # 3 signals chained
      FIX:  all(a, b, c)

    - **W008** — Signal name too short → prefer descriptive snake_case names
      GOT:  Signal("x", 0)
      FIX:  Signal("counter", 0)

    - **W012** — Signal with empty name → use descriptive snake_case names
      GOT:  Signal("", 0)
      FIX:  Signal("counter", 0)

    - **W015** — `delete()` HTTP action without confirmation → accidental data loss risk
      GOT:  data_on_click=delete("/api/item", id=123)
      FIX:  Add confirmation: data_on_click=confirm("Delete?").then(delete(...))

    - **W016** — Signal used but not defined → will cause runtime error
      GOT:  data_text=count  # count was never defined
      FIX:  Define signal: (count := Signal("count", 0))

    - **W017** — Computed Signal detected (expression as initial value, auto-updates)
      GOT:  (doubled := Signal("doubled", count * 2))

    - **W018** — `_ref_only=True` Signal — correctly excluded from `data-signals`

    - **W019** — f-string in `elements()` selector — verify selector is static
      GOT:  elements(content, f"#todo-{id}")

    - **W020** — `elements()` replace-mode without explicit `id` — element may not be targetable later
      GOT:  elements(Div(cls="content"), "#target")
      FIX:  elements(Div(id="target", cls="content"), "#target")
      NOTE: No warning if element has `id=`, uses variable/function return, or uses append/prepend mode

    - **W021** — `switch()` used for CSS classes — use `collect()` to combine multiple classes
      GOT:  data_attr_class=switch([(is_active, "active")], default="")
      FIX:  data_attr_class=collect([(is_active, "active")])

    - **W022** — `collect()` used for exclusive logic — use `switch()` or `if_()` for single result
      GOT:  data_text=collect([(is_valid, "OK", "Error")])
      FIX:  data_text=status.if_("Active", "Inactive")

    - **W023** — `.then()` without conditional signal — verify a boolean signal is used
      GOT:  data_on_click=then(post("/api/save"))
      FIX:  data_on_click=is_valid.then(post("/api/save"))

    - **W024** — `data_effect` without `.set()` — use `signal.set(expression)` for side effects
      GOT:  data_effect=price * quantity
      FIX:  data_effect=total.set(price * quantity)

    - **W025** — Component function without `**kwargs` — limits pass-through attributes
      GOT:  def Modal(body_content):
      FIX:  def Modal(body_content, **kwargs):

    - **W026** — `f()` helper with < 3 signals — prefer `+` operator for 1-2 signals
      GOT:  f("Hello {name}", name=username)  # only 1 signal
      FIX:  "Hello " + username  (saves tokens)

    ## ERROR CODES (BUGS — broken code, do not ship)

    - **E001** — positional arg after keyword → caught by Python parser
      GOT:  Div(cls="container", "Hello")
      FIX:  Div("Hello", cls="container")

    - **E002** — f-string in reactive attribute → static, won't update in browser
      GOT:  data_text=f"Count: {counter}"
      FIX:  data_text="Count: " + counter

    - **E003** — f-string URL in HTTP action → Python-static, signal value not reactive
      GOT:  data_on_click=get(f"/api/{item_id}")
      FIX:  data_on_click=get("/api/item", id=item_id_sig)

    - **E004** — special chars in `data_class_*` keyword → Python parse error
      GOT:  data_class_hover:bg-blue=sig
      FIX:  data_attr_class=sig.if_("hover:bg-blue-500", "")

    - **E005** — camelCase Signal name → must be snake_case
      GOT:  Signal("myCounter", 0)
      FIX:  Signal("my_counter", 0)

    - **E006** — `f()` helper used without import → NameError at runtime
      GOT:  (uses f() but no import)
      FIX:  from starhtml.datastar import f

    - **E007** — `data_attr_class` and `data_attr_cls` on same element → different behaviors
      GOT:  Div(data_attr_class=..., data_attr_cls=...)
      FIX:  Use only one

    - **E008** — walrus `:=` Signal without outer parens → breaks reactivity
      GOT:  count := Signal("count", 0)
      FIX:  (count := Signal("count", 0))

    - **E009** — `data_show` without flash prevention → element flashes before JS loads
      GOT:  Div("content", data_show=is_open)
      FIX:  Div("content", style="display:none", data_show=is_open)

    - **E010** — form submit without `is_valid` guard → submits invalid data
      GOT:  data_on_submit=(post("/api/save"), {"prevent": True})
      FIX:  data_on_submit=(is_valid.then(post("/api/save")), {"prevent": True})

    - **E011** — `data_on_scroll`/`data_on_input` without throttle/debounce → performance bug
      GOT:  data_on_scroll=handler
      FIX:  data_on_scroll=(handler, {"throttle": 16})

    - **E012** — `@sse` endpoint without `yield signals()` reset → client state not cleaned up
      GOT:  @sse def fn(): yield elements(...)
      FIX:  @sse def fn(): yield elements(...); yield signals(...)

    - **E013** — `Icon()` without explicit size → inherits 1em from font-size
      GOT:  Icon("lucide:home")
      FIX:  Icon("lucide:home", size=24)

    - **E014** — `js()` raw JavaScript → potential security risk
      GOT:  js("doSomething(" + user_input + ")")
      FIX:  (item := Signal("item", user_input)); js("doSomething($item)")

    - **E015** — Plugin data attribute used without plugin registration
      GOT:  Div(data_persist=theme)  # but no plugin imported
      FIX:  from starhtml.plugins import persist; app.register(persist)

    - **E016** — `data_on_submit` with `post()` without `{"prevent": True}` — form reloads page
      GOT:  data_on_submit=(post("/api/save"), {"prevent": False})
      FIX:  data_on_submit=(post("/api/save"), {"prevent": True})

    ## WARNING CODES (review — may be intentional)

    - **W021** — `switch()` used for CSS classes — use `collect()` to combine multiple classes
      GOT:  data_attr_class=switch([(is_active, "active")], default="")
      FIX:  data_attr_class=collect([(is_active, "active")])

    - **W022** — `collect()` used for exclusive logic — use `switch()` or `if_()` for single result
      GOT:  data_text=collect([(is_valid, "OK", "Error")])
      FIX:  data_text=status.if_("Active", "Inactive")

    - **W023** — `.then()` without conditional signal — verify a boolean signal is used
      GOT:  data_on_click=then(post("/api/save"))
      FIX:  data_on_click=is_valid.then(post("/api/save"))

    - **W024** — `data_effect` without `.set()` — use `signal.set(expression)` for side effects
      GOT:  data_effect=price * quantity
      FIX:  data_effect=total.set(price * quantity)

    - **W025** — Component function without `**kwargs` — limits pass-through attributes
      GOT:  def Modal(body_content):
      FIX:  def Modal(body_content, **kwargs):

    - **W026** — `f()` helper with < 3 signals — prefer `+` operator for 1-2 signals
      GOT:  f("Hello {name}", name=username)  # only 1 signal
      FIX:  "Hello " + username  (saves tokens)

    - **W027** — File > 400 lines — consider splitting into smaller modules
      GOT:  File has 450 lines
      FIX:  Split into components.py, routes.py, handlers.py

    - **W028** — Deep nesting (>3 levels) — extract to sub-component for better LoB
      GOT:  Div(Div(Div(Div(...))))  # 4 levels
      FIX:  Extract inner Divs to separate component function

    - **W029** — Signal not used in backend without `_` prefix — indicate frontend-only
      GOT:  (counter := Signal("counter", 0))  # never sent to backend
      FIX:  (_counter := Signal("_counter", 0))

    - **W030** — js() that StarHTML can handle — LoB violation
      GOT:  js("element.classList.add('active')")
      FIX:  data_attr_class=is_active.if_("active", "")

    - **W003** — 3+ signals with `&` operator — prefer `all()` for readability
      GOT:  a & b & c  # 3 signals chained
      FIX:  all(a, b, c)
""")


@dataclass
class Issue:
    level: Literal["ERROR", "WARNING"]
    line: int
    code: str
    message: str
    original: str = ""
    fix: str = ""

    def __str__(self):
        lines = [f"  L{self.line} [{self.code}] {self.message}"]
        if self.original:
            lines.append(f"    GOT:  {self.original.strip()}")
        if self.fix:
            fix_lines = self.fix.strip().split("\n")
            for i, fl in enumerate(fix_lines):
                prefix = "    FIX:  " if i == 0 else "          "
                lines.append(prefix + fl)
        return "\n".join(lines)


REACTIVE_FSTRING_ATTRS = {
    "data_text", "data_html", "data_value", "data_href", "data_src",
    "data_style_left", "data_style_top", "data_style_width", "data_style_height",
    "data_style_opacity", "data_style_transform", "data_style_background",
}

REACTIVE_PREFIXES = ("data_on_", "data_class_", "data_style_", "data_attr_", "data_bind")

HTTP_ACTIONS = {"get", "post", "put", "patch", "delete"}

# Plugin-specific data attributes
PLUGIN_DATA_ATTRS = {
    "persist": {"data_persist"},
    "scroll": {"data_scroll", "data_scroll_into_view"},
    "resize": {"data_resize"},
    "drag": {"data_drag", "data_drop_zone"},
    "canvas": {"data_canvas"},
    "position": {"data_position"},
    "motion": {"data_motion", "data_motion_enter", "data_motion_exit", "data_motion_hover", 
               "data_motion_press", "data_motion_in_view", "data_motion_scroll_link", 
               "data_on_motion_start", "data_on_motion_complete", "data_on_motion_cancel"},
    "markdown": {"data_markdown"},
    "katex": {"data_katex"},
    "mermaid": {"data_mermaid"},
    "split": {"data_split"},
}

TAILWIND_SIZE_PATTERN = re.compile(r"(size-|w-|h-)(\d+|\d+/\d+|full|screen|min|max|px|auto|fit)")


class StarHTMLAnalyzer(ast.NodeVisitor):
    def __init__(self, source: str):
        self.lines = source.splitlines()
        self.issues: list[Issue] = []
        self.signals: list[str] = []
        self.events: list[str] = []
        self.reactive_attrs: list[str] = []
        self._seen_signals: set[str] = set()
        self._defined_signals: set[str] = set()  # Signals definidos
        self._used_signals: dict[int, tuple[str, str]] = {}  # lineno -> (signal_name, attr)
        self._has_f_import = False
        self._uses_f_helper: list[int] = []
        self._sse_functions: list[str] = []
        self._sse_has_yield_signals: set[str] = set()
        self._current_func: str = ""
        # Plugin tracking
        self._registered_plugins: set[str] = set()
        self._used_plugin_attrs: dict[int, tuple[str, str]] = {}  # lineno -> (attr, plugin_name)
        # Track f() usage with signal count for I003
        self._f_helper_usage: list[tuple[int, int]] = []  # (lineno, signal_count)
        # Track .then() calls for W023
        self._then_calls: list[int] = []  # lineno
        # Track data_effect for W024
        self._data_effect_usage: list[int] = []  # lineno
        # Track switch/collect usage for W021/W022
        self._switch_usage: list[int] = []  # lineno
        self._collect_usage: list[int] = []  # lineno
        # Track signal operators for I004
        self._and_chains: list[int] = []  # lineno
        # Track component functions for W025
        self._component_functions: list[tuple[str, int, bool]] = []  # (name, lineno, has_kwargs)
        # Track js() usage for W030 (LoB violations)
        self._js_calls: list[tuple[int, str]] = []  # (lineno, js_code)
        # Track deep nesting in components
        self._max_nesting_depth: int = 0
        self._deep_nesting_locations: list[tuple[int, int]] = []  # (lineno, depth)
        # Track signals used in backend (HTTP actions) for W029
        self._backend_signals: set[str] = set()
        self._all_signal_definitions: dict[str, int] = {}  # signal_name -> lineno

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module == "starhtml.datastar":
            for alias in node.names:
                if alias.name == "f":
                    self._has_f_import = True
        # Track plugin imports: from starhtml.plugins import persist, scroll, etc.
        if node.module == "starhtml.plugins":
            for alias in node.names:
                self._registered_plugins.add(alias.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._current_func = node.name
        # Check if function has **kwargs (for W025 - component functions)
        has_kwargs = any(isinstance(arg, ast.kwarg) for arg in node.args.kwonlyargs) or \
                     (node.args.kwarg is not None)
        # Check if function returns HTML elements (simple heuristic: has Div, Span, etc. in body)
        returns_html = False
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name) and child.func.id in {"Div", "Span", "Button", "Input", "Form", "Label", "Select", "Textarea", "Ul", "Ol", "Li", "Table", "Tr", "Td", "Th", "H1", "H2", "H3", "H4", "H5", "H6", "P", "A", "Img", "Canvas", "Svg", "Nav", "Header", "Footer", "Main", "Section", "Article", "Aside"}:
                    returns_html = True
                    break
        # Only track as component if it returns HTML and is not an SSE handler or utility function
        # SSE handlers typically have @sse decorator or yield statements
        is_sse_handler = any(name == node.name for name, _ in self._sse_functions)
        has_yield = any(isinstance(child, ast.Yield) for child in ast.walk(node))
        is_utility = node.name.startswith("_") or "todo" in node.name.lower() and "render" in node.name.lower()
        
        if returns_html and not is_sse_handler and not has_yield and not is_utility:
            self._component_functions.append((node.name, node.lineno, has_kwargs))
            # Calculate nesting depth for this component
            self._calculate_nesting_depth(node)
        
        for decorator in node.decorator_list:
            is_sse = False
            # Handle @sse, @app.sse, and aliased imports
            if isinstance(decorator, ast.Name) and decorator.id == "sse":
                is_sse = True
            elif isinstance(decorator, ast.Attribute) and decorator.attr == "sse":
                is_sse = True  # Handles @app.sse, @starhtml.sse, etc.
            if is_sse:
                self._sse_functions.append((node.name, node.lineno))
        self.generic_visit(node)
        self._current_func = ""

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef(node)

    def visit_Call(self, node: ast.Call):
        func_name = ""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        # E001: positional arg after keyword — SyntaxError
        # Note: Python's parser catches this, but we document it for completeness
        # The AST won't even be generated if this error exists in the source

        # E002: f-string in reactive attribute
        for kw in node.keywords:
            if kw.arg:
                arg_name = kw.arg
                is_reactive = (arg_name in REACTIVE_FSTRING_ATTRS or
                               any(arg_name.startswith(p) for p in REACTIVE_PREFIXES))
                if is_reactive and isinstance(kw.value, ast.JoinedStr):
                    self.issues.append(Issue(
                        level="ERROR",
                        line=kw.lineno,
                        code="E002",
                        message="f-string in reactive attribute — static, won't update in browser",
                        original=self._get_line(kw.lineno),
                        fix='Use + operator: "Label: " + signal\n'
                            'Or f() helper: f("Label: {s}", s=signal) for 3+ signals'
                    ))

        # E003: f-string URL in HTTP action
        if func_name in HTTP_ACTIONS:
            if node.args and isinstance(node.args[0], ast.JoinedStr):
                self.issues.append(Issue(
                    level="ERROR",
                    line=node.lineno,
                    code="E003",
                    message="f-string URL in HTTP action — Python-static, signal value not reactive",
                    original=self._get_line(node.lineno),
                    fix='Pass signal as parameter: get("/api/item", id=item_id_sig)'
                ))

        # E004: special chars in data_class_* keyword name
        for kw in node.keywords:
            if kw.arg and kw.arg.startswith("data_class_"):
                suffix = kw.arg[len("data_class_"):]
                if any(c in suffix for c in ":/[\\]"):
                    self.issues.append(Issue(
                        level="ERROR",
                        line=kw.lineno,
                        code="E004",
                        message=f"special chars in `data_class_*` keyword name — Python parse error",
                        original=self._get_line(kw.lineno),
                        fix='Use data_attr_class: data_attr_class=sig.if_("hover:bg-blue-500", "")'
                    ))

        # E007: data_attr_class and data_attr_cls on same element
        kw_args = {kw.arg for kw in node.keywords if kw.arg}
        if "data_attr_class" in kw_args and "data_attr_cls" in kw_args:
            self.issues.append(Issue(
                level="ERROR",
                line=node.lineno,
                code="E007",
                message="`data_attr_class` and `data_attr_cls` on same element — different behaviors",
                original=self._get_line(node.lineno),
                fix="Use only one: data_attr_class replaces, data_attr_cls adds to base cls="
            ))

        # E009: data_show without flash prevention (UX bug)
        has_data_show = any(kw.arg == "data_show" for kw in node.keywords)
        if has_data_show:
            has_flash_prevention = False
            for kw in node.keywords:
                if kw.arg == "style" and isinstance(kw.value, ast.Constant):
                    if "display" in str(kw.value.value).lower():
                        has_flash_prevention = True
                if kw.arg == "data_style_display" and isinstance(kw.value, ast.Constant):
                    if str(kw.value.value).lower() == "none":
                        has_flash_prevention = True
                if kw.arg == "cls" and isinstance(kw.value, ast.Constant):
                    if "hidden" in str(kw.value.value).lower():
                        has_flash_prevention = True
                if kw.arg == "data_class_hidden":
                    has_flash_prevention = True
                if kw.arg == "data_style_opacity":
                    has_flash_prevention = True
            if not has_flash_prevention:
                # Check if it's an input-like element
                is_input_like = func_name in {"Input", "Form", "Select", "Textarea", "Script"}
                if not is_input_like:
                    self.issues.append(Issue(
                        level="ERROR",
                        line=node.lineno,
                        code="E009",
                        message="`data_show` without flash prevention — element flashes visible before JS loads",
                        original=self._get_line(node.lineno),
                        fix='Add style="display:none": Div("content", style="display:none", data_show=is_open)'
                    ))

        # E011: data_on_scroll without throttle or data_on_input without debounce (performance bug)
        for kw in node.keywords:
            if kw.arg == "data_on_scroll":
                has_throttle = self._has_modifier(kw.value, "throttle")
                if not has_throttle:
                    self.issues.append(Issue(
                        level="ERROR",
                        line=kw.lineno,
                        code="E011",
                        message="`data_on_scroll` without throttle — performance bug",
                        original=self._get_line(kw.lineno),
                        fix='Add throttle: data_on_scroll=(handler, {"throttle": 16})'
                    ))
            if kw.arg == "data_on_input":
                has_debounce = self._has_modifier(kw.value, "debounce")
                if not has_debounce:
                    self.issues.append(Issue(
                        level="ERROR",
                        line=kw.lineno,
                        code="E011",
                        message="`data_on_input` without debounce — performance bug",
                        original=self._get_line(kw.lineno),
                        fix='Add debounce: data_on_input=(handler, {"debounce": 300})'
                    ))

        # E013: Icon() without explicit size (layout bug)
        if func_name == "Icon":
            has_size = False
            for kw in node.keywords:
                if kw.arg in ("size", "width", "height"):
                    has_size = True
                if kw.arg == "cls" and isinstance(kw.value, ast.Constant):
                    cls_val = str(kw.value.value)
                    if TAILWIND_SIZE_PATTERN.search(cls_val):
                        has_size = True
            if not has_size:
                self.issues.append(Issue(
                    level="ERROR",
                    line=node.lineno,
                    code="E013",
                    message="`Icon()` without explicit size — inherits 1em from font-size (layout issue)",
                    original=self._get_line(node.lineno),
                    fix='Add size: Icon("lucide:home", size=24)'
                ))

        # E014: js() raw JavaScript (security risk)
        if func_name == "js":
            self.issues.append(Issue(
                level="ERROR",
                line=node.lineno,
                code="E014",
                message="`js()` raw JavaScript — potential security risk with user input",
                original=self._get_line(node.lineno),
                fix="Use signal references: (item := Signal('item', val)); js('doSomething($item)')"
            ))
            # Track js() calls for W030 (LoB violations)
            js_code = self._get_line(node.lineno)
            self._js_calls.append((node.lineno, js_code))

        # Track signals used in HTTP actions (for W029 - frontend-only signals)
        if func_name in HTTP_ACTIONS:
            for kw in node.keywords:
                if kw.arg and isinstance(kw.value, ast.Name):
                    self._backend_signals.add(kw.value.id)

        # I001: Computed Signal
        if func_name == "Signal":
            if len(node.args) >= 2:
                second_arg = node.args[1]
                is_literal = isinstance(second_arg, (ast.Constant, ast.List, ast.Dict, ast.Set, ast.Tuple))
                if not is_literal:
                    self.issues.append(Issue(
                        level="WARNING",
                        line=node.lineno,
                        code="W017",
                        message="Computed Signal detected (expression as initial value, auto-updates)",
                        original=self._get_line(node.lineno)
                    ))
            # I004: _ref_only=True
            for kw in node.keywords:
                if kw.arg == "_ref_only" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    self.issues.append(Issue(
                        level="WARNING",
                        line=node.lineno,
                        code="W018",
                        message="`_ref_only=True` Signal — correctly excluded from `data-signals` HTML output",
                        original=self._get_line(node.lineno)
                    ))

        # W015: delete() HTTP action without confirmation (UX risk)
        if func_name == "delete":
            self.issues.append(Issue(
                level="WARNING",
                line=node.lineno,
                code="W015",
                message="`delete()` HTTP action — ensure user confirmation UX exists",
                original=self._get_line(node.lineno)
            ))

        # W009: f-string in elements() selector
        if func_name == "elements":
            if len(node.args) >= 2 and isinstance(node.args[1], ast.JoinedStr):
                self.issues.append(Issue(
                    level="WARNING",
                    line=node.lineno,
                    code="W019",
                    message="f-string in elements() selector — verify selector is static or use signal concatenation",
                    original=self._get_line(node.lineno),
                    fix='If dynamic: elements(content, "#target-" + id_sig)\nIf static: elements(content, "#todo-123")  # OK'
                ))

        # Track plugin data attributes usage
        for kw in node.keywords:
            if kw.arg:
                # Check each plugin's attributes
                for plugin_name, attrs in PLUGIN_DATA_ATTRS.items():
                    if kw.arg in attrs:
                        self._used_plugin_attrs[kw.lineno] = (kw.arg, plugin_name)
                        break

        # Track f() usage with signal count for I003
        if func_name == "f":
            self._uses_f_helper.append(node.lineno)
            # Count keyword arguments as signal count
            signal_count = len(node.keywords)
            self._f_helper_usage.append((node.lineno, signal_count))

        # Track switch() and collect() usage for W021/W022
        if func_name == "switch":
            self._switch_usage.append(node.lineno)
        if func_name == "collect":
            self._collect_usage.append(node.lineno)

        # Track .then() calls for W023
        if isinstance(node.func, ast.Attribute) and node.func.attr == "then":
            self._then_calls.append(node.lineno)

        # Track data_effect for W024
        for kw in node.keywords:
            if kw.arg == "data_effect":
                self._data_effect_usage.append(node.lineno)

        # Track SSE yield signals
        if func_name == "signals" and self._current_func:
            # Check if current function is an SSE function
            for sse_name, _ in self._sse_functions:
                if sse_name == self._current_func:
                    self._sse_has_yield_signals.add(self._current_func)
                    break

        # Track signals used in reactive attributes (W016: undefined signals)
        for kw in node.keywords:
            if kw.arg and kw.arg.startswith("data_"):
                # Check if value is a signal reference (simple Name node)
                if isinstance(kw.value, ast.Name):
                    self._used_signals[kw.lineno] = (kw.value.id, kw.arg)
                # Check for signal.method() calls like count.add(1)
                elif isinstance(kw.value, ast.Attribute) and isinstance(kw.value.value, ast.Name):
                    self._used_signals[kw.lineno] = (kw.value.value.id, kw.arg)
                # Check for binary operations like count > 10
                elif isinstance(kw.value, ast.Compare):
                    if isinstance(kw.value.left, ast.Name):
                        self._used_signals[kw.lineno] = (kw.value.left.id, kw.arg)
                # Check for unary operations like ~is_running
                elif isinstance(kw.value, ast.UnaryOp):
                    if isinstance(kw.value.operand, ast.Name):
                        self._used_signals[kw.lineno] = (kw.value.operand.id, kw.arg)

        # Collect events and reactive attrs
        for kw in node.keywords:
            if kw.arg:
                if kw.arg.startswith("data_on_"):
                    self.events.append(f"{kw.arg}(L{kw.lineno})")
                elif kw.arg.startswith("data_"):
                    self.reactive_attrs.append(kw.arg)

        self.generic_visit(node)

    def visit_NamedExpr(self, node: ast.NamedExpr):
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name) and node.value.func.id == "Signal":
                if isinstance(node.target, ast.Name):
                    sig_name = node.target.id
                    if sig_name not in self._seen_signals:
                        self.signals.append(sig_name)
                        self._seen_signals.add(sig_name)
                        self._defined_signals.add(sig_name)
                        self._all_signal_definitions[sig_name] = node.lineno
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name) and node.value.func.id == "Signal":
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        sig_name = target.id
                        if sig_name not in self._seen_signals:
                            self.signals.append(sig_name)
                            self._seen_signals.add(sig_name)
                            self._defined_signals.add(sig_name)
                            self._all_signal_definitions[sig_name] = node.lineno
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp):
        # Track & (BitAnd) operator chains for W003
        if isinstance(node.op, ast.BitAnd):
            self._and_chains.append(node.lineno)
        self.generic_visit(node)

    def _calculate_nesting_depth(self, node: ast.AST, current_depth: int = 0, max_depth: int = 10) -> int:
        """Calculate maximum nesting depth of HTML elements in a node."""
        if current_depth > max_depth:
            return current_depth
        
        html_elements = {"Div", "Span", "Button", "Input", "Form", "Label", "Select", 
                        "Textarea", "Ul", "Ol", "Li", "Table", "Tr", "Td", "Th", 
                        "H1", "H2", "H3", "H4", "H5", "H6", "P", "A", "Img", 
                        "Canvas", "Svg", "Nav", "Header", "Footer", "Main", 
                        "Section", "Article", "Aside", "Card", "Modal"}
        
        max_child_depth = current_depth
        
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in html_elements:
                current_depth += 1
                if current_depth > 5:  # Threshold for warning (was 3)
                    self._deep_nesting_locations.append((node.lineno, current_depth))
        
        for child in ast.iter_child_nodes(node):
            child_depth = self._calculate_nesting_depth(child, current_depth, max_depth)
            max_child_depth = max(max_child_depth, child_depth)
        
        return max_child_depth

    def _get_line(self, lineno: int) -> str:
        if 1 <= lineno <= len(self.lines):
            return self.lines[lineno - 1]
        return ""

    def _has_modifier(self, value: ast.AST, modifier: str) -> bool:
        """Check if a value has a modifier (throttle/debounce)."""
        if isinstance(value, ast.Tuple) and len(value.elts) >= 2:
            second = value.elts[1]
            if isinstance(second, ast.Dict):
                for key in second.keys:
                    if isinstance(key, ast.Constant) and key.value == modifier:
                        return True
            if isinstance(second, ast.Call):
                if isinstance(second.func, ast.Name) and second.func.id == "dict":
                    for kw in second.keywords:
                        if kw.arg == modifier:
                            return True
        return False


def check_regex(source: str, issues: list[Issue], lines: list[str]) -> None:
    """Regex-based checks that complement AST analysis."""

    # E005: camelCase Signal name (includes PascalCase and camelCase)
    signal_name_pattern = re.compile(r'Signal\s*\(\s*["\']([a-zA-Z_][a-zA-Z0-9_]*)["\']')
    for i, line in enumerate(lines, 1):
        match = signal_name_pattern.search(line)
        if match:
            name = match.group(1)
            # Detect camelCase (lowerUpper) or PascalCase (UpperUpper like XMLParser)
            # but allow snake_case (lower_lower) and _underscore_prefix
            has_camel = bool(re.search(r"[a-z][A-Z]", name))  # lowerUpper
            is_pascal_case = bool(re.match(r"^[A-Z][a-zA-Z0-9]*$", name))  # PascalCase puro
            is_snake_case = "_" in name and name.islower()  # snake_case
            is_underscore_prefix = name.startswith("_") and (name[1:].islower() or "_" in name[1:])
            
            if (has_camel or is_pascal_case) and not is_snake_case and not is_underscore_prefix:
                snake_case = re.sub(r"([a-z])([A-Z])", r"\1_\2", name).lower()
                issues.append(Issue(
                    level="ERROR",
                    line=i,
                    code="E005",
                    message="camelCase Signal name — must be snake_case",
                    original=line.strip(),
                    fix=f'Rename to snake_case: Signal("{snake_case}", ...)'
                ))

    # W012: Empty Signal name
    empty_signal_pattern = re.compile(r'Signal\s*\(\s*["\']["\']')
    for i, line in enumerate(lines, 1):
        if empty_signal_pattern.search(line):
            issues.append(Issue(
                level="WARNING",
                line=i,
                code="W012",
                message="Signal with empty name — use descriptive snake_case names",
                original=line.strip(),
                fix='Signal("counter", 0) instead of Signal("", 0)'
            ))

    # E008: walrus := without outer parens (BREAKS reactivity - Signal not passed)
    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if ":= Signal(" in line and not stripped.startswith("("):
            issues.append(Issue(
                level="ERROR",
                line=i,
                code="E008",
                message="walrus `:=` Signal without outer parentheses — won't register as positional arg, breaks reactivity",
                original=line.strip(),
                fix="Wrap in parens: (name := Signal(\"name\", \"\"))"
            ))

    # E010: form submit without is_valid guard (functional bug)
    for i, line in enumerate(lines, 1):
        if "data_on_submit" in line and "post(" in line:
            has_guard = any(x in line for x in ["is_valid", ".then(", "if_("])
            if not has_guard:
                issues.append(Issue(
                    level="ERROR",
                    line=i,
                    code="E010",
                    message="form submit fires `post()` without `is_valid` guard — submits invalid data",
                    original=line.strip(),
                    fix="Add guard: is_valid.then(post(\"/api/save\"))"
                ))

    # W008: Signal name too short
    short_signal_pattern = re.compile(r'Signal\s*\(\s*["\']([a-z_]{1,2})["\']')
    for i, line in enumerate(lines, 1):
        match = short_signal_pattern.search(line)
        if match:
            name = match.group(1)
            # Count non-underscore chars
            useful_chars = len([c for c in name if c != "_"])
            if useful_chars <= 1:
                issues.append(Issue(
                    level="WARNING",
                    line=i,
                    code="W008",
                    message="Signal name too short — prefer descriptive snake_case names",
                    original=line.strip(),
                    fix='Use descriptive name: Signal("counter", 0) instead of Signal("x", 0)'
                ))

    # W020: elements() replace-mode — check if element has id matching selector
    # Only warn if element does NOT have explicit id or selector doesn't match
    for i, line in enumerate(lines, 1):
        # Skip docstrings and comment lines
        stripped = line.strip()
        if stripped.startswith('"""') or stripped.startswith("'''") or stripped.startswith("#"):
            continue
            
        if "elements(" in line:
            # Check if this line or next few lines have append/prepend
            context_lines = "\n".join(lines[i-1:min(i+3, len(lines))])
            has_append_prepend = any(x in context_lines for x in ["\"append\"", "\"prepend\"", "'append'", "'prepend'"])
            if has_append_prepend:
                continue  # append/prepend mode doesn't need id matching

            # Check if element has explicit id attribute
            # Pattern 1: Div(id="...", ...) or similar with literal id
            has_explicit_id = bool(re.search(r'elements\s*\(\s*\w+\s*\([^)]*id\s*=\s*["\'][^"\']+["\']', line))
            # Pattern 2: id=f"..." with f-string (dynamic but valid)
            has_explicit_id = has_explicit_id or bool(re.search(r'elements\s*\(\s*\w+\s*\([^)]*id\s*=\s*f["\'][^"\']*["\']', line))
            # Pattern 3: id=... with string concatenation (e.g., "#todo-" + str(id))
            has_explicit_id = has_explicit_id or bool(re.search(r'elements\s*\(\s*\w+\s*\([^)]*id\s*=\s*[^,)]*\+', line))
            # Pattern 4: element is a variable (function return or variable reference)
            # e.g., elements(todo_element, "...") or elements(render_todo(todo), "...")
            # In this case, assume developer knows what they're doing
            has_variable_element = bool(re.search(r'elements\s*\(\s*[a-z_][a-z0-9_]*\s*\(', line, re.IGNORECASE))
            has_variable_element = has_variable_element or bool(re.search(r'elements\s*\(\s*[a-z_][a-z0-9_]*\s*,', line, re.IGNORECASE))

            if not has_explicit_id and not has_variable_element:
                issues.append(Issue(
                    level="WARNING",
                    line=i,
                    code="W020",
                    message="`elements()` replace-mode — ensure returned element preserves `id` for future targeting",
                    original=line.strip(),
                    fix="Add id to element: elements(Div(id=\"target\", ...), \"#target\")"
                ))


def check_post(analyzer: StarHTMLAnalyzer, issues: list[Issue]) -> None:
    """Post-AST checks that require full context."""

    # E006: f() used without import
    if analyzer._uses_f_helper and not analyzer._has_f_import:
        for lineno in analyzer._uses_f_helper:
            issues.append(Issue(
                level="ERROR",
                line=lineno,
                code="E006",
                message="`f()` helper used without import — NameError at runtime",
                original=analyzer._get_line(lineno),
                fix="Add import: from starhtml.datastar import f"
            ))

    # E012: @sse function without yield signals (state cleanup bug)
    for func_name, lineno in analyzer._sse_functions:
        if func_name not in analyzer._sse_has_yield_signals:
            issues.append(Issue(
                level="ERROR",
                line=lineno,
                code="E012",
                message=f"`@sse` function `{func_name}` missing `yield signals()` reset — client state not cleaned up",
                original=f"def {func_name}(): ...",
                fix="Add at end: yield signals(is_sending=False, message=\"\")"
            ))

    # W016: Signal used but not defined (runtime error)
    for lineno, (sig_name, attr) in analyzer._used_signals.items():
        if sig_name not in analyzer._defined_signals:
            # Skip Python builtins and common names
            if sig_name in {"True", "False", "None", "print", "len", "str", "int", "float", "list", "dict"}:
                continue
            issues.append(Issue(
                level="WARNING",
                line=lineno,
                code="W016",
                message=f"Signal `{sig_name}` used in `{attr}` but never defined — will cause runtime error",
                original=analyzer._get_line(lineno),
                fix=f'Define signal: ({sig_name} := Signal("{sig_name}", 0))'
            ))

    # E015: Plugin data attribute used without plugin import/registration
    for lineno, (attr, plugin_name) in analyzer._used_plugin_attrs.items():
        if plugin_name not in analyzer._registered_plugins:
            issues.append(Issue(
                level="ERROR",
                line=lineno,
                code="E015",
                message=f"`{attr}` requires plugin `{plugin_name}` — import and register it",
                original=analyzer._get_line(lineno),
                fix=f'Add: from starhtml.plugins import {plugin_name}\n'
                    f'Then: app.register({plugin_name})'
            ))

    # E016: data_on_submit with post() but without {"prevent": True}
    for lineno, line in enumerate(analyzer.lines, 1):
        if "data_on_submit" in line and "post(" in line:
            if '{"prevent": True}' not in line and "{'prevent': True}" not in line:
                issues.append(Issue(
                    level="ERROR",
                    line=lineno,
                    code="E016",
                    message="`data_on_submit` with `post()` without `{{\"prevent\": True}}` — form reloads page",
                    original=line.strip(),
                    fix='Add prevent modifier: data_on_submit=(post("/api/save"), {"prevent": True})'
                ))

    # W021: switch() used for CSS classes (should use collect())
    for lineno in analyzer._switch_usage:
        line = analyzer._get_line(lineno)
        # Check if switch is used in data_attr_class or data_class_* context
        if "data_attr_class" in line or "data_class_" in line:
            issues.append(Issue(
                level="WARNING",
                line=lineno,
                code="W021",
                    message="`switch()` used for CSS classes — use `collect()` to combine multiple classes",
                original=line.strip(),
                fix="Use collect() for CSS classes: data_attr_class=collect([(cond1, 'class1'), (cond2, 'class2')])"
            ))

    # W022: collect() used for exclusive logic (should use switch() or if_())
    for lineno in analyzer._collect_usage:
        line = analyzer._get_line(lineno)
        # Check if collect is used in non-CSS context (data_text, data_html, etc.)
        if "data_text" in line or "data_html" in line or "data_value" in line:
            issues.append(Issue(
                level="WARNING",
                line=lineno,
                code="W022",
                message="`collect()` used for exclusive logic — use `switch()` or `if_()` for single result",
                original=line.strip(),
                fix="Use switch() or if_() for exclusive logic: data_text=status.if_('Active', 'Inactive')"
            ))

    # W026: f() helper with < 3 signals (prefer + operator)
    for lineno, signal_count in analyzer._f_helper_usage:
        if signal_count < 3:
            line = analyzer._get_line(lineno)
            issues.append(Issue(
                level="WARNING",
                line=lineno,
                code="W026",
                message=f"`f()` helper with {signal_count} signal(s) — prefer `+` operator for 1-2 signals",
                original=line.strip(),
                fix='Use + operator: "Label: " + signal  (saves tokens, simpler code)'
            ))

    # W023: .then() without conditional signal
    for lineno in analyzer._then_calls:
        line = analyzer._get_line(lineno)
        # Check if .then() is called on a signal (has signal name before .then)
        # Simple heuristic: check if there's a signal-like pattern before .then
        has_conditional = bool(re.search(r'[a-z_][a-z0-9_]*\.then\(', line))
        if not has_conditional:
            issues.append(Issue(
                level="WARNING",
                line=lineno,
                code="W023",
                message="`.then()` without conditional signal — verify a boolean signal is used",
                original=line.strip(),
                fix="Use boolean signal: is_valid.then(post('/api/save'))"
            ))

    # W003: 3+ signals with & operator (prefer all())
    # Count & operators on same line
    for lineno in analyzer._and_chains:
        line = analyzer._get_line(lineno)
        and_count = line.count(" & ")
        if and_count >= 2:  # 2 & means 3+ signals
            issues.append(Issue(
                level="WARNING",
                line=lineno,
                code="W003",
                message=f"3+ signals with `&` operator — prefer `all(a, b, c)` for readability",
                original=line.strip(),
                fix="Use all(): all(sig1, sig2, sig3) instead of sig1 & sig2 & sig3"
            ))

    # W024: data_effect without .set() assignment
    for lineno in analyzer._data_effect_usage:
        line = analyzer._get_line(lineno)
        # Check if data_effect value has .set() call
        if ".set(" not in line:
            issues.append(Issue(
                level="WARNING",
                line=lineno,
                code="W024",
                message="`data_effect` without `.set()` — use `signal.set(expression)` for side effects",
                original=line.strip(),
                fix="Use .set(): data_effect=total.set(price * quantity)"
            ))

    # W025: Component function without **kwargs
    for func_name, func_lineno, has_kwargs in analyzer._component_functions:
        if not has_kwargs:
            issues.append(Issue(
                level="WARNING",
                line=func_lineno,
                code="W025",
                message=f"Component `{func_name}` without `**kwargs` — limits pass-through attributes",
                original=f"def {func_name}(...):",
                fix=f"def {func_name}(..., **kwargs):  # then pass **kwargs to root element"
            ))

    # W027: File > 400 lines (suggest split)
    if len(analyzer.lines) > 400:
        issues.append(Issue(
            level="WARNING",
            line=1,
            code="W027",
            message=f"File has {len(analyzer.lines)} lines — consider splitting into smaller modules (max 400 lines)",
            original=f"File: {analyzer.lines[0] if analyzer.lines else ''}",
            fix="Split into multiple files: components.py, routes.py, handlers.py, etc."
        ))

    # W028: Deep nesting (>3 levels) in components
    for lineno, depth in analyzer._deep_nesting_locations:
        issues.append(Issue(
            level="WARNING",
            line=lineno,
            code="W028",
            message=f"Deep nesting ({depth} levels) — extract to sub-component for better LoB",
            original=analyzer._get_line(lineno),
            fix="Extract nested elements to a separate component function"
        ))

    # W029: Signal used only frontend without _ prefix
    for sig_name, lineno in analyzer._all_signal_definitions.items():
        if sig_name not in analyzer._backend_signals and not sig_name.startswith("_"):
            # Skip common names and signals that might be used indirectly
            if sig_name in {"index", "id", "type", "name", "value", "cls", "todo", "item", "data", "content", "text", "title", "message"}:
                continue
            # Skip computed signals (they're usually frontend-only by design)
            if "getter=" in analyzer._get_line(lineno):
                continue
            issues.append(Issue(
                level="WARNING",
                line=lineno,
                code="W029",
                message=f"Signal `{sig_name}` not used in backend — consider `_` prefix for frontend-only signals",
                original=analyzer._get_line(lineno),
                fix=f"Rename to _{sig_name} to indicate frontend-only usage"
            ))

    # W030: js() that could be StarHTML (LoB violation)
    for lineno, js_code in analyzer._js_calls:
        # Check if js() is used for something that StarHTML could handle
        # Patterns that StarHTML handles well: show/hide, class toggle, simple value updates
        lob_violations = [
            ("showModal()", "data_show with <dialog> element"),
            ("close()", "data_show to hide <dialog>"),
            (".classList.add", "data_class_* or data_attr_class"),
            (".classList.remove", "data_class_* or data_attr_class"),
            (".style.display", "data_show or data_style_display"),
            (".style.opacity", "data_style_opacity"),
            (".value =", "data_bind for two-way binding"),
            (".textContent", "data_text"),
            (".innerHTML", "data_html"),
            ("alert(", "custom modal with data_show"),
            ("confirm(", "custom confirmation modal"),
        ]
        for pattern, suggestion in lob_violations:
            if pattern in js_code:
                issues.append(Issue(
                    level="WARNING",
                    line=lineno,
                    code="W030",
                    message=f"js() using `{pattern}` — StarHTML can handle this with {suggestion} (LoB)",
                    original=js_code.strip(),
                    fix=f"Use StarHTML attribute: {suggestion}"
                ))
                break


def auto_fix(source: str) -> str:
    """Apply safe automatic fixes."""
    lines = source.splitlines()
    fixed_lines = []

    for line in lines:
        stripped = line.lstrip()
        # W003: wrap walrus := in parens
        if re.match(r"^\w+\s*:=\s*Signal\s*\(", stripped) and not stripped.startswith("("):
            indent = line[:len(line) - len(stripped)]
            fixed_lines.append(indent + "(" + stripped + ")")
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines)


def format_report(issues: list[Issue], analyzer: StarHTMLAnalyzer, filename: str, summary_only: bool = False) -> str:
    """Format the analysis report."""
    errors = [i for i in issues if i.level == "ERROR"]
    warnings = [i for i in issues if i.level == "WARNING"]

    lines = [f"── starhtml-check: {filename} ──"]

    if not summary_only:
        if errors:
            lines.append(f"\nERRORS ({len(errors)}):")
            for issue in errors:
                lines.append(str(issue))

        if warnings:
            lines.append(f"\nWARNINGS ({len(warnings)}):")
            for issue in warnings:
                lines.append(str(issue))

    # Summary
    lines.append("\nSUMMARY:")
    signals_str = ", ".join(analyzer.signals[:10])
    if len(analyzer.signals) > 10:
        signals_str += f" ... (+{len(analyzer.signals) - 10})"
    lines.append(f"  SIGNALS  : {signals_str if analyzer.signals else '(none)'}")

    events_str = ", ".join(analyzer.events[:5])
    if len(analyzer.events) > 5:
        events_str += f" ... (+{len(analyzer.events) - 5})"
    lines.append(f"  EVENTS   : {events_str if analyzer.events else '(none)'}")

    reactive_str = ", ".join(list(set(analyzer.reactive_attrs))[:10])
    lines.append(f"  REACTIVE : {reactive_str if analyzer.reactive_attrs else '(none)'}")

    error_word = "error" if len(errors) == 1 else "errors"
    warning_word = "warning" if len(warnings) == 1 else "warnings"
    lines.append(f"  ISSUES   : {len(errors)} {error_word}, {len(warnings)} {warning_word}")

    if not errors and not warnings:
        lines.append("\n  ✓ No issues found")
    elif summary_only:
        lines.append(f"\n  ✗ Fix {len(errors)} {error_word} before proceeding")

    return "\n".join(lines)


def analyze(source: str, filename: str = "<stdin>", summary_only: bool = False) -> str:
    """Run full analysis on source code."""
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return f"── starhtml-check: {filename} ──\n\nSYNTAX ERROR at line {e.lineno}:\n  {e.text.strip() if e.text else ''}\n  {' ' * (e.offset or 0)}^\n  {e.msg}"

    analyzer = StarHTMLAnalyzer(source)
    analyzer.visit(tree)

    issues = analyzer.issues
    lines = source.splitlines()
    check_regex(source, issues, lines)
    check_post(analyzer, issues)

    # Deduplicate by (line, code, message[:40])
    seen = set()
    unique_issues = []
    for issue in issues:
        key = (issue.line, issue.code, issue.message[:40])
        if key not in seen:
            seen.add(key)
            unique_issues.append(issue)

    # Sort by line number
    unique_issues.sort(key=lambda i: (i.line != 0, i.line))

    return format_report(unique_issues, analyzer, filename, summary_only)


def main():
    parser = argparse.ArgumentParser(
        description="starhtml-check — Static analyzer for StarHTML code"
    )
    parser.add_argument("file", nargs="?", help="File to analyze")
    parser.add_argument("--code", help="Analyze inline code snippet")
    parser.add_argument("--fix", metavar="FILE", help="Auto-fix safe issues and print result")
    parser.add_argument("--summary", metavar="FILE", help="Compact output (fewer tokens)")
    parser.add_argument("--help-llm", action="store_true", help="Print LLM integration guide")

    args = parser.parse_args()

    if args.help_llm:
        print(HELP_LLM)
        sys.exit(0)

    if args.fix:
        with open(args.fix, "r") as f:
            source = f.read()
        fixed = auto_fix(source)
        print(fixed)
        # Also run analysis on fixed code
        report = analyze(fixed, args.fix, summary_only=True)
        print("\n" + report, file=sys.stderr)
        sys.exit(0)

    if args.summary:
        with open(args.summary, "r") as f:
            source = f.read()
        report = analyze(source, args.summary, summary_only=True)
        print(report)
        sys.exit(0)

    if args.code:
        report = analyze(args.code, "<code>")
        print(report)
        sys.exit(0)

    if args.file:
        with open(args.file, "r") as f:
            source = f.read()
        report = analyze(source, args.file)
        print(report)
        sys.exit(0)

    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
