# StarHTML JavaScript Integration — Reference

## Contents
- [When to use each approach](#when-to-use-each-approach)
- [f() — reactive string templates](#f---reactive-string-templates)
- [js() — raw JavaScript expressions](#js---raw-javascript-expressions)
- [value() — force literal values](#value---force-literal-values)
- [regex() — JavaScript regular expressions](#regex---javascript-regular-expressions)
- [Global JavaScript objects](#global-javascript-objects)

---

## When to use each approach

| Situation | Solution |
|-----------|---------|
| 1–2 signals in a string | `"Label: " + signal` (+ operator) |
| 3+ signals in a string | `f("Label: {a} {b}", a=sig1, b=sig2)` |
| f-string in reactive attr | **Never** — becomes static, won't update |
| Raw JS expression needed | `js("expression")` |
| Force a Python literal | `value(literal)` (rarely needed) |
| Regex pattern | `regex(r"pattern")` |

---

## f() — reactive string templates

For reactive string templates with 3 or more signals. Requires explicit import.

    # REQUIRED import — f() is NOT included in `from starhtml import *`
    from starhtml.datastar import f

    # Basic usage
    data_text=f("Hello {name}, you have {count} items", name=username, count=counter)
    # Compiles to: `Hello ${$username}, you have ${$counter} items`
    # Updates reactively when username or counter changes

    # Comparison of approaches:
    # 1 signal  → + operator
    data_text="Count: " + counter

    # 2 signals → + operator
    data_text=first + " " + last

    # 3+ signals → f() helper
    data_text=f("{greeting}, {first} {last}!", greeting=g, first=fn, last=ln)

    # WRONG — f-string is Python-evaluated once, becomes a static string:
    data_text=f"Count: {counter}"    # → "Count: $counter" (literal string, never updates)

---

## js() — raw JavaScript expressions

Escape hatch for when the Python API is insufficient.

    # Signal initial value from JavaScript expression
    (timestamp := Signal("timestamp", js("Date.now()")))
    (random    := Signal("random",    js("Math.random()")))

    # Complex expressions in event handlers
    data_on_click=js("confirm('Are you sure?') && deleteItem()")

    # Browser APIs
    data_effect=js("navigator.clipboard.writeText($message)")
    data_on_click=js("document.querySelector('#modal').showModal()")

    # Filtering/transforming signal values
    (completed := Signal("completed", js("$todos.filter(t => t.completed)")))

**Security warning:** Never interpolate user-controlled values directly into `js()` expressions.
Use signal references (which are sandboxed) instead of string concatenation.

    # WRONG — potential injection if item_name contains JS:
    js(f"doSomething('{item_name}')")

    # RIGHT — pass as signal reference:
    (item := Signal("item", item_name))
    js("doSomething($item)")

---

## value() — force literal values

Explicitly marks a value as a JavaScript literal (not a signal reference). Rarely needed — StarHTML usually infers this correctly.

    # Usually not needed — these are equivalent:
    (pi     := Signal("pi",     3.14159))
    (pi     := Signal("pi",     value(3.14159)))

    # Useful when StarHTML might misinterpret a value:
    (config := Signal("config", value({"theme": "dark", "lang": "en"})))
    (items  := Signal("items",  value([1, 2, 3, 4])))

---

## regex() — JavaScript regular expressions

Creates a JavaScript regex literal for use in signal expressions.

    # Basic patterns
    regex(r"^\d{3}-\d{4}$")     # → /^\d{3}-\d{4}$/
    regex("^todo_")              # → /^todo_/
    regex(r"[A-Z]{2,}")         # → /[A-Z]{2,}/

    # Use in reactive expressions
    data_show=email.match(regex(r"^[^ @]+@[^ @]+\.[^ @]+$"))
    data_class_error=~phone.match(regex(r"^\d{10}$"))
    data_show=text.match(regex(r"\bimportant\b"))

---

## Global JavaScript objects

These are pre-defined in StarHTML and can be used directly in expressions:

    # Console
    console.log("Debug value:", signal_name)
    console.error("Error:", error_msg)

    # Math
    Math.round(value)
    Math.floor(value)
    Math.ceil(value)
    Math.random()
    Math.max(a, b)
    Math.min(a, b)
    Math.abs(value)

    # JSON
    JSON.stringify(data)
    JSON.parse(raw_string)

    # Date
    Date.now()

    # Object
    Object.keys(obj)
    Object.values(obj)
    Object.entries(obj)

    # Array
    Array.isArray(value)
    Array.from(iterable)
