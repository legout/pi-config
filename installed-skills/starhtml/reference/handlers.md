# StarHTML Plugins — Reference

## Contents
- [Overview](#overview)
- [persist — localStorage sync](#persist)
- [scroll — scroll tracking](#scroll)
- [resize — resize events](#resize)
- [drag — drag and drop](#drag)
- [canvas — canvas drawing](#canvas)
- [position — element positioning](#position)
- [motion — CSS/SVG animations](#motion)
- [Performance notes](#performance-notes)

---

## Overview

Plugins extend StarHTML with additional functionality. Each plugin must be:
1. Imported from `starhtml.plugins`
2. Registered with the app using `app.register(plugin)`

```python
from starhtml import *
from starhtml.plugins import persist, scroll, resize, drag, canvas, position, motion

app, rt = star_app()
app.register(persist)
app.register(motion)
# ... register other plugins as needed
```

Plugins provide `data_*` attributes that work with signals to enable advanced behaviors.

---

## persist

Syncs signal values to `localStorage` or `sessionStorage`. Values are restored on page load.

```python
from starhtml.plugins import persist

app.register(persist)

# Basic usage — persists to localStorage
(theme := Signal("theme", "light"))
Div(data_persist=theme)  # key defaults to signal name

# Explicit key
Div(data_persist=(theme, {"key": "app_theme"}))

# Session-only (clears when tab closes)
Div(data_persist=(theme, {"session": True}))

# Multiple signals with shared key
Div(data_persist=([theme, font_size], {"key": "app_settings"}))
```

**Features:**
- Automatic save/restore on page reload
- Debounced writes (500ms) to prevent excessive storage calls
- JSON serialization for complex data types

📄 See: `https://raw.githubusercontent.com/banditburai/starHTML/main/web/demos/09_persist_plugin.py`

---

## scroll

Tracks scroll position and provides scroll-based reactive triggers.

```python
from starhtml.plugins import scroll

app.register(scroll)

# Basic usage — update signal on scroll
(scroll_y := Signal("scroll_y", 0))
Div(
    data_scroll=(scroll_y.set, {"throttle": 100}),
    style="overflow-y: auto; height: 400px"
)

# Use scroll variables directly
data_show=scroll.is_top       # show when at top
data_show=scroll.is_bottom    # show when at bottom
data_text=scroll.page_progress  # scroll percentage (0-100)
```

**Available scroll signals:**
- `scroll.x` / `scroll.y` — scroll position
- `scroll.direction` — "up", "down", or "none"
- `scroll.page_progress` — page scroll percentage
- `scroll.is_top` / `scroll.is_bottom` — boundary detection
- `scroll.visible_percent` — element visibility percentage

**Config options:**
- `throttle` — milliseconds between updates (default 100ms)
- `smooth` — enables interpolation for smoother animations

📄 See: `https://raw.githubusercontent.com/banditburai/starHTML/main/web/demos/10_scroll_plugin.py`

---

## resize

Updates signals when window or element is resized.

```python
from starhtml.plugins import resize

app.register(resize)

(win_width := Signal("win_width", 0))
(win_height := Signal("win_height", 0))

# Window resize
Div(data_resize=(win_width.set, {"throttle": 100}))

# Use dimensions in UI
Span(data_text="Width: " + win_width)
Div(data_show=win_width > 768, style="display:none", cls="desktop-only")
```

📄 See: `https://raw.githubusercontent.com/banditburai/starHTML/main/web/demos/11_resize_plugin.py`

---

## drag

Enables drag and drop functionality with sortable lists and drop zones.

```python
from starhtml.plugins import drag

app.register(drag)

# Create drag handler instance
todos_drag = drag(name="todos", mode="sortable")
app.register(todos_drag)

# Make elements draggable
Div("Item 1", data_drag=True, id="item-1")
Div("Item 2", data_drag=True, id="item-2")

# Define drop zones
Div(data_drop_zone="inbox", cls="drop-zone")
```

**Features:**
- Sortable lists with `mode="sortable"`
- Cross-container drag with `mode="free"`
- Accessibility: keyboard navigation, screen reader announcements
- Built-in visual feedback (cursor, hover states)

📄 See complete examples:
- `https://raw.githubusercontent.com/banditburai/starHTML/main/web/demos/12_drag_plugin.py`
- `https://raw.githubusercontent.com/banditburai/starHTML/main/web/demos/16_freeform_drag.py`

---

## canvas

Provides canvas drawing capabilities with reactive signal binding.

```python
from starhtml.plugins import canvas

app.register(canvas)

# Enable canvas on element
Canvas(
    data_canvas=True,
    width="800",
    height="600",
    id="my-canvas"
)
```

**Features:**
- Brush tools with configurable color/size
- Drawing modes (freehand, shapes, etc.)
- Signal-based state management
- Undo/redo support

📄 See complete examples:
- `https://raw.githubusercontent.com/banditburai/starHTML/main/web/demos/17_canvas_plugin.py`
- `https://raw.githubusercontent.com/banditburai/starHTML/main/web/demos/18_canvas_fullpage.py`
- `https://raw.githubusercontent.com/banditburai/starHTML/main/web/demos/29_drawing_canvas.py`

---

## position

Tracks and controls element position with reactive signals.

```python
from starhtml.plugins import position

app.register(position)

(pos_x := Signal("pos_x", 0))
(pos_y := Signal("pos_y", 0))

# Track position
Div(
    data_position=(pos_x.set, pos_y.set),
    id="target",
    style="position: absolute"
)

# Control position
Div(
    data_style_left=pos_x + "px",
    data_style_top=pos_y + "px",
    id="draggable"
)
```

📄 See: `https://raw.githubusercontent.com/banditburai/starHTML/main/web/demos/20_position_plugin.py`

---

## motion

CSS and SVG animations with declarative and imperative APIs.

```python
from starhtml.plugins import motion

app.register(motion)
```

### Declarative Animations

```python
# Enter animations (on mount)
Div("Content", data_motion=enter(preset="fade", duration=300))
Div("Content", data_motion=enter(x=50, opacity=0, duration=400))

# Exit animations (on unmount)
Div("Content", data_motion_exit=exit_(opacity=0, x=50, duration=300))

# Hover gestures
Div("Content", data_motion=hover(scale=1.1))

# Press gestures
Button("Press Me", data_motion=press(scale=0.95))

# In-view (scroll-triggered, run once)
Div("Content", data_motion=in_view(preset="fade", once=True))

# Scroll-linked parallax
Div("Content", data_motion=scroll_link(y=(0, -50)))

# Visibility helper (signal-based show/hide with animation)
Div("Content",
    data_motion=visibility(
        signal=show_details,
        enter=enter(y=-20, opacity=0, duration=400),
        exit_=exit_(y=-10, opacity=0, duration=250),
    )
)
```

### Imperative Actions

```python
# Animate an element
Button("Slide Right", 
    data_on_click=motion.animate("#target", x=100, duration=300)
)

# Set properties instantly
Button("Reset", 
    data_on_click=motion.set("#target", x=0, scale=1)
)

# Remove element with exit animation
Button("Remove", 
    data_on_click=motion.remove("#notif-1")
)

# Replace element with exit animation (SSE-friendly)
yield motion_replace("#target", Div("New content"))

# Animation sequences
Button("Run", data_on_click=motion.sequence([
    ("#title", {"opacity": 1, "duration": 300}),
    ("#subtitle", {"y": 0, "opacity": 1}, {"at": "+0.15"}),
]))

# Playback controls
motion.play("demo-anim")
motion.pause("demo-anim")
motion.cancel("demo-anim")
```

### Event Handling

```python
Div("Content",
    data_on_motion_start=event_log.set("Started!"),
    data_on_motion_complete=event_log.set("Complete!"),
    data_on_motion_cancel=event_log.set("Cancelled!"),
)
```

📄 See complete examples:
- `https://raw.githubusercontent.com/banditburai/starHTML/main/web/demos/23_motion_plugin.py`
- `https://raw.githubusercontent.com/banditburai/starHTML/main/web/demos/24_motion_svg_plugin.py`

---

## Performance notes

High-frequency plugins must use throttle/debounce to avoid performance issues:

```python
# scroll — throttle to max 60fps
data_scroll=(handler.set, {"throttle": 16})  # 16ms = 60fps

# resize — debounce (fires after user stops resizing)
data_resize=(handler.set, {"debounce": 100})  # wait 100ms

# Always register plugins before using their data-* attributes
app.register(scroll)
app.register(resize)
```
