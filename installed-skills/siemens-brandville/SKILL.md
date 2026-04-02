---
name: siemens-brandville
description: Guide for creating world-class Siemens-branded presentations using the Brandville methodology and O365 template system. Use this skill whenever the user is creating Siemens presentations, working with Brandville templates, designing slides with Siemens corporate identity, building executive presentations for Siemens, or needs help with Siemens-specific slide layouts, content structure, typography sizing, or presentation workflows. This skill covers layout selection, content strategy (SCQA framework, McKinsey Pyramid Principle), mandatory slide types (Key Takeaways, Way Forward), and presentation structure. For detailed color specifications (CMYK, Pantone, RAL, skin tones, etc.), use the siemens-color-guidance skill.
---

# Siemens Brandville Presentation Guide

Create Siemens-branded presentations that embody the brand principles: **Make change with clarity, purpose, and impact**.

## Related Skills

- **siemens-color-guidance**: Use for detailed color specifications including CMYK, Pantone, HKS, NCS, RAL values, skin tones, hair tones, extended Deep Blue tints, and multi-context color decisions (UI, print, illustrations).
- **siemens-brandville** (this skill): Use for presentation structure, slide layouts, content strategy, typography, and mandatory slide types.

## Core Principles

| Principle | Application |
|-----------|-------------|
| **Clarity** | Bold, clear palette that differentiates Siemens |
| **Purpose** | Technology-inspired feel with purposeful color use |
| **Impact** | Individual bold colors that stand out |

## Presentation Colors (Quick Reference)

For detailed color specifications (all color systems, tints, tones), see **siemens-color-guidance** skill.

### Primary Colors for Presentations

| Color | HEX | Role |
|-------|-----|------|
| **Deep Blue** | `#000028` | **Primary background** |
| **Bold Green** | `#00ffb9` | Headlines on dark backgrounds |
| **Bold Blue** | `#00e6dc` | Accent elements |
| **Siemens Petrol** | `#009999` | Signature color, logos |
| **Light Sand** | `#f3f3f0` | Light backgrounds, body text on dark |

### Text Colors by Background

| Background | Headlines | Body Text |
|------------|-----------|-----------|
| Deep Blue | Bold Green `#00ffb9` or White | Light Sand `#f3f3f0` |
| Light Sand | Deep Blue `#000028` | Deep Blue `#000028` |

### Color Usage Rules

```
BACKGROUND → Deep Blue (#000028) for digital/screen [DEFAULT]
           → Light Sand (#f3f3f0) for print/accessibility

HEADLINES on Deep Blue → Bold Green (#00ffb9)

CHARTS/DATA → Use secondary colors (see siemens-color-guidance)

GRADIENTS → Only for CTAs and shapes, never general backgrounds
```

### Secondary Colors (Charts/Data Only)

| Use | Color | HEX |
|-----|-------|-----|
| Category 1 | Yellow | `#ffd732` |
| Category 2 | Blue | `#0087be` |
| Category 3 | Purple | `#805cff` |
| Category 4 | Green | `#00af8e` |
| Warning | Red | `#ef0137` |
| Highlight | Orange | `#ff9000` |

For complete secondary palette with all color systems → **siemens-color-guidance**

## Typography

### Font Stack
- **Primary:** Siemens Sans (when available)
- **Fallback:** Arial / Arial Bold / Arial Light

### Title Sizing Guide

| Title Length | Size | Use Case |
|--------------|------|----------|
| ≤ 15 characters | **80 pt** | Maximum impact |
| ≤ 35 characters (2-3 lines) | **60 pt** | Default for most slides |
| 36+ characters (4+ lines) | **40 pt** | Long, complex titles |

### Type Scale

| Element | Size | Style |
|---------|------|-------|
| Title (long) | 40 pt | Bold |
| Title (default) | 60 pt | Bold |
| Title (short) | 80 pt | Bold |
| Title with picture | 36-48 pt | Bold |
| Subtitle | 14-32 pt | Regular |
| Headline | 20 pt | Bold |
| Body text | 14-18 pt | Regular |
| Footer | 10-12 pt | Regular |
| Footnote | 9 pt | Regular |

## Layout Selection

### Slide Type Decision Tree

```
PURPOSE?
├─ Cover / First impression → Title slide (with motif matching topic)
├─ New chapter / Major shift → Chapter divider
├─ Meeting agenda → Agenda (2-col dark or 1-col light)
├─ Single key message → One Object (large)
├─ Compare two options → Two Columns
├─ Three pillars/principles → Three Columns
├─ 2×2 matrix/scenarios → Four Objects
├─ Phased rollout → Process Flow
├─ Emotional close → Quote
├─ Bold mission/vision → Statement
├─ Summary/recommendation → Key Takeaways
├─ Multiple paths → Way Forward
├─ Decision with resources → Go/No-Go
└─ Speaker contact → Contact
```

### Layout Reference by Code

| Layout | Placeholders | Use For |
|--------|--------------|---------|
| **Title slides** | `ph0` (Title), `ph1` (Subtitle), `ph12` (Footer) | Cover slides |
| **Title with Picture** | `ph0`, `ph1`, `ph11` (Picture), `ph13` (Footer) | Visual covers |
| **Chapter Divider** | `ph0`, `ph1`, `ph10` (Footer), `ph11` (Slide #) | Section breaks |
| **Agenda** | Multi-column | Table of contents |
| **One Object** | `ph0`=Title, `ph1`=Content | Single message |
| **Two Columns** | `ph0`=Title, `ph1`=Left, `ph2`=Right | Comparisons |
| **Three Columns** | `ph0`=Title, `ph1`=Col1, `ph2`=Col2, `ph12`=Col3 | Three pillars |
| **Four Objects** | `ph0`=Title, `ph1`=TL, `ph12`=TR, `ph2`=BL, `ph13`=BR | 2×2 matrix |
| **Key Takeaways** | `ph12-14` (3 points), `ph15` (context), `ph16` (pros), `ph17` (cons) | Summary slides |
| **Way Forward** | `ph12` (Scenario A), `ph13` (B), `ph14` (C) | Options/scenarios |
| **Go/No-Go** | `ph18-23` (decision matrix) | Budget/resource decisions |
| **Topic Overview** | `ph12-17` (subtopics), `ph18` (center) | Six-dimension topics |
| **Contact** | `ph0`, `ph1`, `ph10`, `ph11` | Final slide |

## Content Strategy

### Writing Guidelines

**Lead with the answer** — State conclusions first (Pyramid Principle).

| ❌ Topic Title | ✅ Finding Title |
|---------------|------------------|
| "Current Situation" | "IT costs grew 23% while headcount stayed flat" |
| "Options Analysis" | "Only Option B meets the Q3 deadline" |
| "Key Takeaways" | "Three actions needed to hit the 2026 target" |

### SCQA Framework

Structure your opening narrative:

| Element | Purpose | Slide Type |
|---------|---------|------------|
| **Situation** | Stable context audience knows | Content/Statement |
| **Complication** | What changed / tension | Content/Two Columns |
| **Question** | Key question created | Statement/Chapter |
| **Answer** | Core recommendation | Key Takeaways/Content |

### The 3-Argument Rule
- One core message per slide
- Three supporting arguments (ideal number for persuasion)
- Lead with conclusion, support with evidence

## Mandatory Slides

Every Siemens presentation must include:

### 1. Key Takeaways (Always Include)
- **3 crisp key findings** (real insights, not titles)
- **Decision context** or recommendation
- **Pros and cons** (at least 2 each — honest framing builds credibility)

### 2. Quote Slide (Always Include)
- Relevant, attributed quote
- Include source URL in speaker notes
- Format: `"Quote text."\n— Name, context/year`

### 3. Way Forward (When Choices Exist)
- **Scenario A:** Do nothing / status quo implications
- **Scenario B:** Selective / phased approach  
- **Scenario C:** Full / accelerated deployment

### 4. Go/No-Go (When Applicable)
Use when budget approval pending, resource reallocation required, or timing risks exist.

## Footer & Metadata

### Standard Footer Format
```
[Confidentiality] | © Siemens YYYY | Author Name | Department | DD.MM.YYYY
```

### Confidentiality Labels
- **Public / Öffentlich** — External distribution approved
- **Internal / Intern** — Siemens internal use only
- **Confidential / Vertraulich** — Restricted circulation

### Contact Slide Format
```
Publisher: Siemens [Company]
[Full Name]
[Position]
[Division/Department]
[Street Address]
[Postal Code] [City]
[Phone] | [Email]
```

## Speaker Notes

Every slide needs speaker notes with:

| Component | Content |
|-----------|---------|
| Opening sentence | Single message this slide conveys |
| Supporting context | Data, rationale, examples |
| Source citations | URL or document reference |
| Transition line | How this connects to next slide |

> Write as complete sentences for AI audio dubbing compatibility.

## Recommended Presentation Structure

```
 1. Title slide (motif matching topic)
 2. Agenda
 3. Chapter: Context
 4. Situation slide
 5. Complication slide
 6. Chapter: Analysis
 7. Data/findings slides
 8. Framework slide
 9. Chapter: Recommendation
10. Topic overview
11. Way Forward
12. Go/No-Go (if applicable)
13. Key Takeaways [REQUIRED]
14. Quote [REQUIRED]
15. Contact slide
```

## Quick Reference

### Slide Dimensions
- **Aspect Ratio:** 16:9
- **Pixels:** 1280 × 720 (96 DPI)

### Theme Selection

| Context | Theme |
|---------|-------|
| Standard presentations | Dark (Deep Blue) |
| Print/handouts | Light (Light Sand) |
| Accessibility needs | Light |
| Executive/formal | Dark |
| Sustainability topics | Sustainability motif |
| Digital transformation | Transformation motif |
| Xcelerator products | Siemens Xcelerator motif |

## Design Rules

| Rule | Rationale |
|------|-----------|
| Deep Blue is default background | Brand standard |
| Never use Bold Green/Blue as backgrounds | They're foreground colors |
| Never apply gradients to general backgrounds | Gradients only for CTAs/shapes |
| One core message per slide | Clarity and impact |
| 3 supporting arguments ideal | Persuasion sweet spot |
| Cite sources in speaker notes | Credibility and traceability |
| Match motif to topic | Transformation, Xcelerator, or Sustainability |

---

*Reference: Brandville.siemens.com | O365 Template v3.4.5*
