# Siemens Ultimate Presentation Style Guide

> A comprehensive, standalone style guide for creating world-class Siemens-branded presentations. Combines the technical precision of the O365 template system with the strategic storytelling methodology of Brandville.

---

## Table of Contents

1. [Brand Principles](#brand-principles)
2. [Color Palette](#color-palette)
3. [Typography](#typography)
4. [Slide Dimensions](#slide-dimensions)
5. [Layout System](#layout-system)
6. [Layout Reference](#layout-reference)
7. [Content Strategy](#content-strategy)
8. [Slide Types & When to Use Them](#slide-types--when-to-use-them)
9. [Footer & Metadata](#footer--metadata)
10. [Best Practices](#best-practices)
11. [Quick Reference](#quick-reference)

---

## Brand Principles

All Siemens presentations should embody these three principles:

| Principle | Meaning |
|-----------|---------|
| **Make change with clarity** | The bold, clear palette differentiates Siemens externally and provides orientation internally |
| **Make change with purpose** | Colors create a technology-inspired feel — especially on Deep Blue backgrounds, which make Bold Green and Bold Blue pop on screen |
| **Make change with impact** | Individual colors are bold and powerful — built to stand out in a cluttered digital age |

---

## Color Palette

### Primary Colors

**Use these first.** The core Siemens brand colors.

| Color Name | HEX | RGB | CMYK | Pantone | Usage |
|------------|-----|-----|------|---------|-------|
| **Siemens Petrol** ⭐ | `#009999` | 0 153 153 | 100 0 40 0 | 321 C | Signature color, logos, accents |
| Light Petrol | `#00c1b6` | 0 193 182 | 70 0 37 0 | 2398 C | Accent elements |
| **Bold Green** | `#00ffb9` | 0 255 185 | — | 3385 C | Headlines on dark backgrounds |
| Soft Green | `#00d7a0` | 0 215 160 | 60 0 50 0 | 2412 C | Light background alternative |
| **Bold Blue** | `#00e6dc` | 0 230 220 | — | 3115 C | Accent elements on dark |
| Soft Blue | `#00bedc` | 0 190 220 | 70 0 10 0 | 3545 C | Light background alternative |
| **Deep Blue** 🔲 | `#000028` | 0 0 40 | 100 90 30 75 | 5255 C | **Primary background** |
| Light Sand | `#f3f3f0` | 243 243 240 | 0 0 3 8 | 9043 C | Light background, body text |

> ⭐ **Siemens Petrol** is the signature color.
> 🔲 **Deep Blue** is the primary background color.

### Secondary Colors

Use primarily in information graphics, illustrations, and tables.

#### Sand Tones
| Color Name | HEX | Usage |
|------------|-----|-------|
| Dark Sand | `#aaaa96` | Borders, dividers |
| Soft Sand | `#c5c5b8` | Subtle backgrounds |
| Bright Sand | `#dfdfd9` | Layered depth |

#### Accent Colors (Charts & Data)
| Color Name | HEX | Usage |
|------------|-----|-------|
| Yellow | `#ffd732` | Chart category |
| Dark Yellow | `#f7c600` | Chart category |
| Green | `#00af8e` | Chart category |
| Blue | `#0087be` | Chart category |
| Dark Blue | `#00557c` | Chart category |
| Purple | `#805cff` | Chart category |
| Dark Purple | `#553ba3` | Chart category |
| Red | `#ef0137` | Warning, critical |
| Orange | `#ff9000` | Highlight, attention |
| Dark Orange | `#ec6602` | Warning accent |

### Deep Blue Tints (Grays)

For fine-grained layering and depth in complex layouts.

| Tint | HEX | Usage |
|------|-----|-------|
| Deep Blue 95% | `#0d0d33` | Deepest layer |
| Deep Blue 90% | `#19193d` | Dark layering |
| Deep Blue 80% | `#333353` | Dark containers |
| Deep Blue 60% | `#66667e` | Medium containers |
| Deep Blue 40% | `#9999a9` | Light containers |
| Deep Blue 20% | `#ccccd4` | Subtle backgrounds |
| Deep Blue 10% | `#e5e5e9` | Very subtle layering |

### Corporate Gradients

> ⚠️ Use **only** for organic shapes, CTA elements, and UI linear gradients — **not for general backgrounds**.

| Gradient | Stop A | Stop B |
|----------|--------|--------|
| Bold Dynamic Petrol | `#00ffb9` | `#00e6dc` |
| Soft Dynamic Petrol | `#00d7a0` | `#00bedc` |
| Deep Blue–Petrol | `#009999` | `#000028` |

### Color Decision Logic

```
Is it a BACKGROUND?
├─ Digital/Screen → Deep Blue (#000028) ✅ PRIMARY CHOICE
├─ Light context (print, accessibility) → Light Sand (#f3f3f0) or White
└─ Layered depth → Deep Blue tints

Is it a HEADLINE or PRIMARY ELEMENT?
├─ On Deep Blue → Bold Green (#00ffb9) or Bold Blue (#00e6dc)
├─ Signature/logo context → Siemens Petrol (#009999)
└─ Softer feel → Soft Green (#00d7a0) or Soft Blue (#00bedc)

Is it a CHART, TABLE, or ILLUSTRATION?
└─ Use secondary colors (Yellows, Greens, Blues, Purples, Accents)
```

---

## Typography

### Font Family

| Context | Font | Notes |
|---------|------|-------|
| **Primary** | Siemens Sans | Brand font (when available) |
| **Fallback** | Arial | Standard across all systems |
| **Bold** | Arial Bold | Headlines, emphasis |
| **Regular** | Arial Regular | Body text |
| **Light** | Arial Light | Subtle elements |

### Font Sizes by Element

| Element | Size | Style | Use Case |
|---------|------|-------|----------|
| **Title (80pt)** | 80 pt | Bold | ≤ 15 characters |
| **Title (60pt)** | 60 pt | Bold | ≤ 35 characters (default) |
| **Title (40pt)** | 40 pt | Bold | 36+ characters, 4+ lines |
| **Title picture (48pt)** | 48 pt | Bold | Title slides with images |
| **Title picture (40pt)** | 40 pt | Bold | Title slides with images |
| **Title picture (36pt)** | 36 pt | Bold | Title slides with images |
| **Subtitle (32pt)** | 32 pt | Regular | Secondary headlines |
| **Subtitle (24pt)** | 24 pt | Regular | Secondary headlines |
| **Subtitle (18pt)** | 18 pt | Regular | Secondary headlines |
| **Subtitle (16pt)** | 16 pt | Regular | Secondary headlines |
| **Subtitle (14pt)** | 14 pt | Regular | Secondary headlines |
| **Headline** | 20 pt | Bold | Section headers |
| **Body text** | 14–18 pt | Regular | Main content |
| **Footnote** | 9 pt | Regular | Citations, sources |
| **Footer** | 10–12 pt | Regular | Slide metadata |

### Title Size Selection Guide

| Title Length | Recommended Size | Rationale |
|--------------|------------------|-----------|
| Short (≤15 chars) | 80 pt | Maximum impact for brief titles |
| Medium (≤35 chars, 2-3 lines) | 60 pt | Default for most presentations |
| Long (36+ chars, 4+ lines) | 40 pt | Readability for complex titles |

### Text Colors by Background

| Background | Headline | Body Text | Accent |
|------------|----------|-----------|--------|
| Deep Blue | Bold Green `#00ffb9` or White | Light Sand `#f3f3f0` | Bold Blue `#00e6dc` |
| Light Sand | Deep Blue `#000028` | Deep Blue `#000028` | Siemens Petrol `#009999` |

### Writing Guidelines

- **One core message per slide** — not a topic dump
- **Lead with the answer** — state conclusions first (Pyramid Principle)
- **3 supporting arguments** — ideal number for persuasion
- **Headline-style titles** — express findings, not topics

| ❌ Topic Title | ✅ Finding Title |
|----------------|------------------|
| "Current Situation" | "IT costs grew 23% while headcount stayed flat" |
| "Options Analysis" | "Only Option B meets the Q3 deadline" |
| "Key Takeaways" | "Three actions needed to hit the 2026 target" |

---

## Slide Dimensions

| Property | Inches | Centimeters | Pixels (96 DPI) |
|----------|--------|-------------|-----------------|
| Width | 13.33" | 33.87 cm | 1280 px |
| Height | 7.50" | 19.05 cm | 720 px |
| Aspect Ratio | 16:9 | 16:9 | 16:9 |

---

## Layout System

### Layout Categories

| Category | Purpose | Typical Count |
|----------|---------|---------------|
| **Title Slides** | Cover/presentation opening | 30 variations |
| **Title with Picture** | Visual cover slides | 9 variations |
| **Chapter Dividers** | Section transitions | 9 variations |
| **Agenda / Index** | Table of contents | 2 variations |
| **Full Bleed / Free Content** | Minimal custom layouts | 4 variations |
| **Image Slides** | Photo-centric layouts | 4 variations |
| **Standard Content** | One object, columns, tables | 20+ variations |
| **Strategic Layouts** | Key takeaways, decisions | 12+ variations |
| **Special Purpose** | Quotes, statements, contact | 6 variations |

### Theme Variants

Most layouts come in multiple theme variants:

| Theme | Background | When to Use |
|-------|------------|-------------|
| **Deep Blue** (Dark) | `#000028` | Default, formal, executive, screen presentations |
| **Light Sand** (Light) | `#f3f3f0` | Print, accessibility, light preference |
| **Petrol Accent** | `#009999` highlights | Brand emphasis, signatures |
| **Gradient** | Dynamic blends | Modern, dynamic contexts |

### Background Motifs (Title Slides)

| Motif | Description | Use Case |
|-------|-------------|----------|
| **Deep Blue Solid** | Solid dark blue | Default formal presentations |
| **Transformation** | Mask & blur with transformation imagery | Digital transformation topics |
| **Siemens Xcelerator** | Mask & blur with Xcelerator branding | Xcelerator product presentations |
| **Sustainability** | Mask & blur with sustainability theme | ESG, sustainability reports |

---

## Layout Reference

### Placeholder System

| Code | Type | Description |
|------|------|-------------|
| `ph0` | TITLE | Main title/headline |
| `ph1` | SUBTITLE / OBJECT | Subtitle or primary content object |
| `ph2` | BODY / COLUMN | Body text or secondary column |
| `ph3–ph9` | CONTENT | Extended content placeholders |
| `ph10` | FOOTER | Footer text area |
| `ph11` | SLIDE_NUMBER | Slide number indicator |
| `ph12` | BODY / PICTURE / LEFT | Multi-use: body, image, left column |
| `ph13` | BODY / RIGHT | Right column or secondary body |
| `ph14–ph18` | EXTENDED | Additional content areas for complex layouts |

### Title Slides (Cover)

**Purpose:** First impression, presentation opening

| Variant | Title Sizes | Background Options |
|---------|-------------|-------------------|
| Deep Blue Solid | 80pt, 60pt, 40pt | Solid `#000028` |
| Transformation Motif | 80pt, 60pt, 40pt | Mask & blur (3 variations) |
| Xcelerator Motif | 80pt, 60pt, 40pt | Mask & blur (3 variations) |
| Sustainability Motif | 80pt, 60pt, 40pt | Mask & blur (3 variations) |

**Placeholders:** `ph0` (Title), `ph1` (Subtitle), `ph12` (Footer)

### Title with Picture

**Purpose:** Visual impact covers with integrated imagery

| Theme | Title Sizes |
|-------|-------------|
| Dark | 48pt, 40pt, 36pt |
| Gradient | 48pt, 40pt, 36pt |
| Light | 48pt, 40pt, 36pt |

**Placeholders:** `ph0` (Title), `ph1` (Subtitle), `ph11` (Picture), `ph13` (Footer)

### Chapter Dividers

**Purpose:** Major section transitions

| Theme | Title Sizes | Accent |
|-------|-------------|--------|
| Dark | 80pt, 60pt, 40pt | Deep Blue |
| Petrol Color | 80pt, 60pt, 40pt | Siemens Petrol `#009999` |
| Light | 80pt, 60pt, 40pt | Light Sand |

**Placeholders:** `ph0` (Title), `ph1` (Subtitle), `ph10` (Footer), `ph11` (Slide Number)

### Agenda / Index

**Purpose:** Table of contents, meeting agenda

| Theme | Layout | Columns |
|-------|--------|---------|
| Dark | Two-column | Left items + Right items |
| Light | Single-column | Stacked items |

**Pro tip:** Use tab-separated text for page numbers: `"Chapter 1\t3"`

### Standard Content Layouts

| Type | Purpose | Placeholders |
|------|---------|--------------|
| **One Object (small)** | Limited content, text focus | `ph0`=Title, `ph1`=Content |
| **One Object (large)** | Full-page text or graphics | `ph0`=Title, `ph1`=Content |
| **Two Columns** | Comparison, before/after | `ph0`=Title, `ph1`=Left, `ph2`=Right |
| **Three Columns** | Three pillars, principles | `ph0`=Title, `ph1`=Col1, `ph2`=Col2, `ph12`=Col3 |
| **Four Objects (2×2)** | Matrix, grid scenarios | `ph0`=Title, `ph1`=TL, `ph12`=TR, `ph2`=BL, `ph13`=BR |
| **Two Columns Spotlight** | Image + text focus | `ph0`=Title, `ph12`=Picture, `ph2`=Text |
| **Table** | Data presentation | `ph0`=Title, `ph12`=Table |
| **Process Flow** | Step-by-step (3 steps) | `ph0`=Title, `ph1`=Step1, `ph13`=Step2, `ph12`=Step3 |
| **Quote** | Inspirational quotes | `ph0`=Hidden, `ph12`=Quote text |
| **Statement** | Bold single message | `ph0`=Statement only |

### Strategic Layouts (Brandville)

#### Key Takeaways
**Purpose:** Summary with decision context and balanced pros/cons

| Placeholder | Content |
|-------------|---------|
| `ph12`, `ph13`, `ph14` | 3 key point boxes (2–3 bullets each) |
| `ph15` | Decision facts / context |
| `ph16` | Pros (2–3 bullets) |
| `ph17` | Cons (2–3 bullets) |

> **Always include** in every presentation. Three crisp insights, honest framing with pros/cons builds credibility.

#### Way Forward
**Purpose:** Present multiple scenarios/options

| Placeholder | Scenario |
|-------------|----------|
| `ph12` | Scenario A — Do nothing / status quo |
| `ph13` | Scenario B — Selective / partial approach |
| `ph14` | Scenario C — Full deployment |

> Use whenever there are genuine choices to present.

#### Go / No-Go
**Purpose:** Decision framework with resource details

| Row | Rollout | Budget | Resources |
|-----|---------|--------|-----------|
| No-Go | `ph18` | `ph19` | `ph20` |
| Go | `ph21` | `ph22` | `ph23` |

> Use when: Budget approval pending, resource reallocation required, timing risks exist.

#### Topic Overview
**Purpose:** Six subtopics surrounding a central theme

| Placeholder | Content |
|-------------|---------|
| `ph12`–`ph17` | Subtopics 1–6 |
| `ph18` | Core topic (center) |

### Contact Slide

**Purpose:** Final slide with speaker information

**Placeholders:** `ph0` (Title), `ph1` (Details), `ph10` (Footer), `ph11` (Slide Number)

**Standard Format:**
```
Publisher: [Company]
[Name]
[Position]
[Division]
[Address]
[Phone] | [Email]
```

---

## Content Strategy

### SCQA Framework

Use SCQA to structure your opening narrative:

| Element | Purpose | Slide Type |
|---------|---------|------------|
| **Situation** | What's the stable context the audience knows | Content or Statement |
| **Complication** | What changed / what creates tension | Content or Two Columns |
| **Question** | What key question does this create? | Statement or Chapter |
| **Answer** | Your core recommendation | Key Takeaways or Content |

### McKinsey Pyramid Principle

Structure arguments top-down:

1. **Lead with the answer** — state the conclusion first
2. **Group supporting arguments** — 3 is ideal, 2–5 acceptable
3. **Support with evidence** — data, examples, precedents

```
Slide title  = conclusion / recommendation
Slide body   = 3 supporting reasons (bullets or 3-column layout)
Speaker note = evidence, sources, data citations
```

### Recommended Presentation Structure

```
1.  Title slide           — Branded cover (motif appropriate to topic)
2.  Agenda                — Map the journey
3.  Chapter: Context      — Setting the stage
4.  Situation slide       — What's true today
5.  Complication slide    — What's changed / the problem
6.  Chapter: Analysis     — Diving deeper
7.  Data / findings       — Evidence (one message per slide)
8.  Framework slide       — Three-column or four-object
9.  Chapter: Recommendation
10. Topic overview        — The full picture at a glance
11. Way Forward           — 3 scenarios
12. Go / No-Go            — If applicable
13. Key Takeaways         — Always include
14. Quote                 — Close with inspiration
15. Contact slide
```

---

## Slide Types & When to Use Them

| Situation | Best Slide Type | Layout Theme |
|-----------|-----------------|--------------|
| Cover / first impression | Title slide (with motif) | Match topic to motif |
| New chapter / major topic shift | Chapter divider | Dark (default) or Petrol |
| Meeting agenda | Agenda | Dark (2-col) or Light (1-col) |
| Single key message with detail | One Object (large) | Match overall theme |
| Comparing two options | Two Columns | Match overall theme |
| Three pillars / principles | Three Columns | Match overall theme |
| 2×2 matrix / four scenarios | Four Objects | Match overall theme |
| Phased rollout / milestones | Process Flow | Match overall theme |
| Inspiring start or emotional close | Quote | Match overall theme |
| Bold mission / vision | Statement | Match overall theme |
| End-of-presentation summary | Key Takeaways | Match overall theme |
| Multiple paths forward | Way Forward | Match overall theme |
| Decision with budget/resource detail | Go / No-Go | Match overall theme |
| Complex topic with 6 sub-dimensions | Topic Overview | Match overall theme |
| Final speaker contact | Contact | Dark or Light |

---

## Footer & Metadata

### Footer Format

```
[Confidentiality] | © Siemens YYYY | Author Name | Department | DD.MM.YYYY
```

### Confidentiality Labels

| English | German | Usage |
|---------|--------|-------|
| Public | Öffentlich | External distribution approved |
| Internal | Intern | Siemens internal use only |
| Confidential | Vertraulich | Restricted circulation |

### Example Footers

```
Intern | © Siemens 2026 | Max Mustermann | IT DA DO | 10.03.2026
Public | © Siemens 2026 | Anna Schmidt | Digitalization | 10.03.2026
```

### Metadata Checklist

| Field | Source | Used In |
|-------|--------|---------|
| Author name | User input | Footer + Contact slide |
| Department | User input | Footer + Contact slide |
| Date (DD.MM.YYYY) | Auto/user | Footer |
| Confidentiality level | User selection | Footer prefix |
| Year | Auto | Copyright notice |
| Presentation title | User input | Cover slide |
| Target audience | User context | Storyline calibration |
| Key decision / outcome | User input | Core message focus |

---

## Best Practices

### Always Include

1. **Key Takeaways slide** — Every presentation ends with one
   - 3 crisp key findings (real insights, not titles)
   - Decision context / recommendation
   - At least 2 pros and 2 cons (honest framing builds credibility)

2. **Quote slide** — Find a relevant, real quote
   - Include source URL in speaker notes
   - Format: `"The quote text exactly as said."\n— First Name Last Name, context/year`

3. **Way Forward slide** — Whenever there are choices
   - Scenario A: Do nothing (status quo implications)
   - Scenario B: Selective / phased approach
   - Scenario C: Full / accelerated deployment

4. **Go / No-Go slide** — When:
   - Budget approval is pending
   - Resource reallocation is required
   - Rollout dependencies have timing risk

### Speaker Notes

Every slide should have speaker notes:

| Component | Content |
|-----------|---------|
| **Opening sentence** | The single message this slide conveys |
| **Supporting context** | Data, rationale, examples |
| **Source citations** | Include URL or document reference for KPIs |
| **Transition line** | How this slide connects to the next |

> For AI audio dubbing compatibility: write speaker notes as complete, flowing sentences — not bullet fragments.

### KPI and Data Handling

1. Include source reference on the slide (small text or footnote)
2. Include full source URL in speaker notes
3. Round figures to meaningful precision (23% not 23.4177%)
4. Label forward-looking figures as "estimate" or "forecast"

### Design Rules

| Rule | Reason |
|------|--------|
| Deep Blue is always the first choice for background | Brand standard |
| Never use Bold Green or Bold Blue as backgrounds | They are foreground/accent colors |
| Never apply gradients to general backgrounds | Gradients are for CTAs and organic shapes only |
| One core message per slide | Clarity and impact |
| 3 supporting arguments ideal | Persuasion sweet spot |
| Cite sources in speaker notes | Credibility and traceability |
| Choose title size by character count | Readability optimization |
| Match motif to topic | Transformation, Xcelerator, or Sustainability |

### Theme Selection Guide

| Context | Recommended Theme |
|---------|-------------------|
| Standard presentations | Dark (Deep Blue) |
| Print / handouts | Light (Light Sand) |
| Accessibility requirements | Light |
| Executive / formal settings | Dark |
| Sustainability topics | Sustainability motif |
| Digital transformation | Transformation motif |
| Xcelerator products | Siemens Xcelerator motif |

---

## Quick Reference

### Theme Defaults

| Element | Dark Theme | Light Theme |
|---------|------------|-------------|
| Background | Deep Blue `#000028` | Light Sand `#f3f3f0` |
| Headlines | Bold Green `#00ffb9` or White | Deep Blue `#000028` |
| Body text | Light Sand `#f3f3f0` | Deep Blue `#000028` |
| Accent | Bold Blue `#00e6dc` | Siemens Petrol `#009999` |

### Essential Layouts Quick Pick

| Purpose | Dark Layout | Light Layout |
|---------|-------------|--------------|
| Title (default: ≤35 chars) | Title 60pt | Title 60pt |
| Title (short: ≤15 chars) | Title 80pt | Title 80pt |
| Title (long: 36+ chars) | Title 40pt | Title 40pt |
| Chapter divider | Dark or Petrol | Light |
| Agenda | Dark (2-col) | Light (1-col) |
| Content (large object) | One Object Large | One Object Large |
| Content (small object) | One Object Small | One Object Small |
| Two columns | Two Columns | Two Columns |
| Three columns | Three Columns | Three Columns |
| Four objects (2×2) | Four Objects | Four Objects |
| Image with text | Spotlight Dark | Spotlight Light |
| Table | Table Dark | Table Light |
| Process flow | Process Flow Dark | Process Flow Light |
| Quote | Quote Dark | Quote Light |
| Statement | Statement Dark | Statement Light |
| Key Takeaways | Key Takeaways Dark | Key Takeaways Light |
| Way Forward | Way Forward Dark | Way Forward Light |
| Go / No-Go | Go/No-Go Dark | Go/No-Go Light |
| Contact | Contact Dark | Contact Light |

### Title Size Quick Reference

```
Title length ≤ 15 characters → 80pt
Title length ≤ 35 characters → 60pt (default)
Title length > 35 characters → 40pt
```

### Quote Slide Format

```
Title (ph0): Hidden or "Quote"
Body (ph12): "The quote text in quotation marks."
             "— First Name Last Name, Role/Context, Year"
```

### Process Flow Format

```
Step 1 (ph1): Left position
Step 2 (ph13): Center position
Step 3 (ph12): Right position (highlighted)
```

### Contact Slide Format

```
Title (ph0): "Contact" or "Kontakt"
Details (ph1): Publisher: Siemens [Company]
               [Full Name]
               [Position]
               [Division/Department]
               [Street Address]
               [Postal Code] [City]
               [Phone] | [Email]
```

---

## File Information

| Property | Value |
|----------|-------|
| Guide Version | 1.0 (Ultimate) |
| Based On | O365 Template v3.4.5 + Brandville Template |
| Aspect Ratio | 16:9 Widescreen |
| Primary Background | Deep Blue `#000028` |
| Signature Color | Siemens Petrol `#009999` |
| Primary Font | Siemens Sans / Arial |
| Total Layouts | 80–104 (template dependent) |

---

*This style guide combines the technical precision of the Siemens O365 Template with the strategic storytelling methodology of Brandville. For the most current brand assets, visit: https://brandville.siemens.com*
