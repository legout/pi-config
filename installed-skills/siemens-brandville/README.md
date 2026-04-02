# Siemens Brandville Skill

A comprehensive skill for creating world-class Siemens-branded presentations using the Brandville methodology and O365 template system.

## Overview

This skill guides agents in creating Siemens presentations that embody the brand principles:
- **Make change with clarity** — Bold, clear palette
- **Make change with purpose** — Technology-inspired feel
- **Make change with impact** — Bold, powerful colors

## Contents

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill instructions for agents |
| `references/full-style-guide.md` | Complete style guide with all specifications |
| `references/quick-start.md` | Quick reference for common tasks |
| `scripts/siemens_utils.py` | Python utilities for footer generation, color validation, etc. |
| `evals/evals.json` | Test cases for skill validation |

## Key Features

### Color System
- **Primary:** Siemens Petrol (#009999), Bold Green (#00ffb9), Bold Blue (#00e6dc), Deep Blue (#000028)
- **Background:** Deep Blue (default for digital), Light Sand (for print/accessibility)
- **Secondary:** Full chart/data visualization palette

### Typography
- **Fonts:** Siemens Sans (primary), Arial (fallback)
- **Title sizing:** 80pt (≤15 chars), 60pt (≤35 chars), 40pt (36+ chars)
- **Type scale:** From 9pt footnotes to 80pt titles

### Layout System
- **80+ layouts** across 9 categories
- **Strategic layouts:** Key Takeaways, Way Forward, Go/No-Go, Topic Overview
- **Content layouts:** One Object, Two/Three Columns, Four Objects, Table, Process Flow
- **Story layouts:** Title, Chapter Divider, Quote, Statement, Contact

### Content Strategy
- **SCQA Framework:** Situation, Complication, Question, Answer
- **McKinsey Pyramid Principle:** Lead with conclusions, support with 3 arguments
- **Mandatory slides:** Key Takeaways, Quote, Contact

### Helper Script Functions

```python
from scripts.siemens_utils import (
    get_title_size,           # Get appropriate title font size
    get_text_colors,          # Get text colors for background
    generate_footer,          # Create properly formatted footer
    generate_contact_block,   # Create contact slide content
    scqa_to_slides,           # Convert SCQA to slide recommendations
    validate_color_usage,     # Validate color usage
    get_secondary_colors      # Get chart/data colors
)
```

## When to Use This Skill

Use whenever creating or editing:
- Siemens-branded presentations
- Executive decks for Siemens leadership
- Brandville template-based slides
- Presentations requiring Siemens corporate identity
- Slides needing Siemens-specific layouts or color schemes

## References

- Full style guide: `references/full-style-guide.md`
- Quick start: `references/quick-start.md`
- Brandville: https://brandville.siemens.com
