# StarHTML Icons — Reference

## Contents
- [Basic usage](#basic-usage)
- [Sizing](#sizing)
- [Color and styling](#color-and-styling)
- [CDN mode vs inline mode](#cdn-mode-vs-inline-mode)
- [Production workflow](#production-workflow)
- [Custom icons](#custom-icons)
- [CLS prevention](#cls-prevention)

---

## Basic usage

    from starhtml import *

    # Format: "prefix:icon-name" — uses any Iconify-compatible icon set
    Icon("lucide:home")         # Lucide icons
    Icon("mdi:account")         # Material Design Icons
    Icon("ph:star")             # Phosphor Icons
    Icon("tabler:settings")     # Tabler Icons
    Icon("heroicons:user")      # Heroicons

Browse all available icons at: https://icon-sets.iconify.design/

---

## Sizing

    # Explicit numeric size (applied to both width and height)
    Icon("lucide:home", size=24)          # 24px
    Icon("lucide:home", size=16)          # 16px

    # Explicit string size
    Icon("lucide:home", size="1.5rem")    # 1.5rem
    Icon("lucide:home", size="2em")       # 2em

    # Separate width and height
    Icon("lucide:home", width=32, height=24)

    # Tailwind size classes (extracted and applied automatically)
    Icon("lucide:home", cls="size-6")     # 1.5rem (Tailwind size scale)
    Icon("lucide:home", cls="w-8 h-8")   # 2rem

    # No size specified → defaults to 1em (inherits from parent font-size)
    Icon("lucide:home")

---

## Color and styling

    # Icons use currentColor — control color via Tailwind text-* classes
    Icon("lucide:heart", cls="text-red-500 size-6")
    Icon("lucide:star",  cls="text-amber-400 size-5")
    Icon("lucide:check", cls="text-green-600 size-4")

    # Spacing on the wrapper span
    Icon("lucide:home", cls="mr-2")

    # In a button with text
    Button(
        Icon("lucide:download", cls="size-4 mr-2"),
        "Download",
        cls="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded",
    )

---

## CDN mode vs inline mode

| Mode | How | When |
|------|-----|------|
| **CDN** (default) | `<iconify-icon>` web component, client-side fetch from Iconify CDN | Development |
| **Inline** | `<svg>` server-rendered, zero JavaScript, zero layout shift, works offline | Production |

    # Enable inline mode in code
    app, rt = star_app(inline_icons=True)

    # Or via environment variable (overrides code setting)
    # STARHTML_INLINE_ICONS=1   (accepts: 1, true, yes — case-insensitive)

---

## Production workflow

    # Step 1: Pre-cache all icons used in your source files
    # Run from project root before deploy
    starhtml icons scan web/ src/

    # Step 2: Commit the cache or bake into Docker image
    git add .starhtml/icons/

    # Step 3: At runtime, inline_icons=True loads from disk cache
    # Zero API calls, zero external dependencies in production

    # Re-scan to add newly used icons
    starhtml icons scan web/ src/

    # Exclude specific directories
    starhtml icons scan --exclude "*/tests/*.py" web/ src/

    # Disable default excludes (tests/, .venv/, __pycache__/, etc.)
    starhtml icons scan --no-default-excludes web/ src/

**Note:** Dynamically constructed icon names like `Icon(f"{prefix}:home")` or `Icon(variable)` are not detected by scan. Register these manually:

    from starhtml.icons import resolver, IconData
    resolver.register("custom", "logo", IconData(body='<path d="M..."/>', width=24, height=24))

---

## Custom icons

    from starhtml.icons import resolver, IconData

    # Register a custom SVG icon
    resolver.register(
        "custom",           # prefix
        "logo",             # icon name
        IconData(
            body='<path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>',
            width=24,
            height=24
        )
    )

    # Use like any other icon
    Icon("custom:logo", size=32)

---

## CLS prevention

The `Icon()` wrapper `<span>` automatically reserves space to prevent Cumulative Layout Shift (CLS):
- `display: inline-block`
- `flex-shrink: 0`
- `vertical-align: middle`
- `line-height: 0`
- Explicit width and height

    # Default: stable=True — wrapper span with reserved space (recommended)
    Icon("lucide:home")

    # stable=False — bare element without wrapper span (advanced use only)
    Icon("lucide:home", stable=False)
