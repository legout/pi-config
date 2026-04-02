# StarHTML Demos — Reference Index

All demo files are in the official StarHTML framework repository.
Base URL: `https://raw.githubusercontent.com/banditburai/starHTML/main/web/demos/`

To fetch any demo: `curl <base_url><filename>`
Example: `curl https://raw.githubusercontent.com/banditburai/starHTML/main/web/demos/01_basic_signals.py`

## Contents
- [Basic patterns (01–08)](#basic-patterns)
- [Plugins (09–24)](#plugins)
- [Advanced patterns (25–30)](#advanced-patterns)

---

## Basic patterns

| File | Demonstrates | Fetch when you need |
|------|-------------|---------------------|
| `01_basic_signals.py` | Signal definition with walrus `:=`, `data_text`, `data_bind`, `data_on_click`, `data_show` with flash prevention | Basic reactivity from scratch |
| `02_sse_elements.py` | `@sse` decorator, `yield signals()`, `yield elements()`, append vs replace/morph mode | SSE patterns, streaming updates |
| `03_forms_binding.py` | `data_bind` for inputs, validation with `switch()`, form submit with `prevent`, `is_valid` guard | Form handling |
| `04_live_updates.py` | Real-time data updates via SSE, polling patterns | Live dashboards, feeds |
| `05_background_tasks.py` | Long-running server tasks, SSE progress reporting, cancellation | Progress bars, async jobs |
| `06_control_attributes.py` | Event modifiers (`debounce`, `throttle`, `prevent`, `stop`, `once`), conditional attributes | Event handling nuances |
| `07_todo_list.py` | Complete CRUD app: signals, SSE, routing, `data_bind`, `data_show`, list rendering | Real-world app reference |
| `08_routing_patterns.py` | `@rt` routing, partial HTML responses, hypermedia morph, `id` preservation rule | Server-side routing |

---

## Plugins

Each demo is a complete, runnable example showing how to import, configure, and use the plugin.

| File | Plugin | Demonstrates |
|------|--------|-------------|
| `09_persist_plugin.py` | persist | Sync signal values to `localStorage`, restore on page load |
| `10_scroll_plugin.py` | scroll | Track scroll position as signals, react to scroll events |
| `11_resize_plugin.py` | resize | Window and element resize events as signals |
| `12_drag_plugin.py` | drag | Drag and drop basics, draggable elements, drop zones |
| `13_markdown_plugin.py` | markdown | Render markdown content reactively |
| `14_katex_plugin.py` | katex | Render math / LaTeX expressions |
| `15_mermaid_plugin.py` | mermaid | Render diagrams from text definitions |
| `16_freeform_drag.py` | drag | Freeform drag positioning, absolute coordinates |
| `17_canvas_plugin.py` | canvas | Canvas drawing basics, brush tools |
| `18_canvas_fullpage.py` | canvas | Full-page canvas application |
| `19_nodegraph_demo.py` | nodegraph | Node graph UI, connecting nodes |
| `20_position_plugin.py` | position | Track and control element position |
| `21_split_responsive.py` | split | Responsive resizable split panes |
| `22_split_universal.py` | split | Universal split panes (horizontal + vertical) |
| `23_motion_plugin.py` | motion | CSS animations triggered by signals |
| `24_motion_svg_plugin.py` | motion-svg | SVG path animations |

---

## Advanced patterns

| File | Demonstrates | Fetch when you need |
|------|-------------|---------------------|
| `25_advanced_toggle_patterns.py` | Complex toggle logic, multiple conditions, state machines | Non-trivial show/hide logic |
| `26_complex_modifiers.py` | Advanced event modifier combinations, custom event handling | Fine-grained event control |
| `27_nested_property_chaining.py` | Computed signals, method chaining, derived state from multiple signals | Complex derived state |
| `28_datastar_helpers_showcase.py` | Complete showcase of `if_()`, `match()`, `switch()`, `collect()`, `f()`, `all()`, `any()` | All conditional helpers in one place |
| `29_drawing_canvas.py` | Interactive drawing application with tools, colors, undo | Complex canvas app |
| `30_debugger_demo.py` | StarHTML debugger tool, inspecting signals and events at runtime | Debugging StarHTML apps |
