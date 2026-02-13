---
name: fujisoft-presentation-creator
description: This skill should be used when creating professional presentation materials, slide decks, or proposal documents following FUJISOFT America's corporate template standards. Triggers include requests like "create a presentation", "make slides", "prepare proposal materials", "FUJISOFT template", or when MARP-format Markdown presentations are needed with consistent corporate branding. The skill provides a complete MARP template with CSS styling, visual design components, and quality assurance workflows.
---

# FUJISOFT America Presentation Creator

## Overview

This skill enables creation of professional, high-quality presentation materials using FUJISOFT America's corporate slide template. The template is built on MARP (Markdown Presentation Ecosystem), enabling efficient slide creation through Markdown while maintaining consistent corporate branding and design standards.

## When to Use This Skill

- Creating client proposals and technical presentations
- Preparing project progress reports
- Building sales presentations
- Developing seminar or workshop materials
- Any external-facing presentation requiring FUJISOFT America branding

## Workflow

### Step 1: Understand Requirements

Before creating slides, gather the following information:

1. **Purpose**: Information sharing, decision-making, or action promotion
2. **Audience**: Executives, technical staff, sales prospects, etc.
3. **Key Messages**: Main points to convey (limit to 3-5)
4. **Time Constraint**: Presentation duration including Q&A
5. **Output Format**: PDF, HTML, or editable PPTX

### Step 2: Create Presentation Structure

Follow the Guy Kawasaki 10-20-30 Rule as a guideline:
- **10 slides** maximum for optimal engagement
- **20 minutes** presentation time
- **30pt** minimum font size

Typical presentation structure:
1. Cover Page (title, subtitle, company info)
2. Executive Summary / Agenda
3. Current Situation / Problem Statement
4. Proposed Solution
5. Technical Architecture / Approach
6. Implementation Timeline
7. Budget / ROI Analysis
8. Risk Management
9. Summary / Call to Action
10. Thank You Page (contact information)

### Step 3: Write MARP Markdown

Use the template in `assets/FUJISOFT_America_Slide_Template.md` as the foundation.

#### Page Classes

**Cover Page** (`cover`):
```markdown
<!-- _class: cover -->
# <span style="color: rgba(255,255,255,0.9);">PROJECT TITLE</span>
## Subtitle Description

<div class="company-info">FUJISOFT America, Inc.</div>
<div class="confidential">CONFIDENTIAL</div>
```

**Content Page** (`content`):
```markdown
<!-- _class: content -->
## Page Title

### Section Heading
- Bullet point 1
- Bullet point 2

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">Page Number</div>
<div class="footer-right">CONFIDENTIAL</div>
```

**Thank You Page** (`thankyou content`):
```markdown
<!-- _class: thankyou content -->
# Thank You

<div class="blue-line"></div>
<div class="company-logo">FUJISOFT America, Inc.</div>
<div class="address">
1825 South Grant Street<br>
Ste. 200<br>
San Mateo, CA 94402
</div>

<div class="contact-info">
  <div class="contact-item">
    <span class="icon">phone</span>
    650-235-9422
  </div>
  <div class="contact-item">
    <span class="icon">email</span>
    inquiry@fsi-america.com
  </div>
</div>

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">Page Number</div>
<div class="footer-right">CONFIDENTIAL</div>
```

**Two-Column Layout**:
```markdown
<div class="two-column">
<div class="column">
### Left Column
Content here...
</div>
<div class="column">
### Right Column
Content here...
</div>
</div>
```

### Step 4: Apply Visual Design Elements

Use these CSS classes to enhance visual appeal and information clarity:

#### Information Boxes (for categorizing information)

```html
<div class="info-box">
<strong>Information Title (Blue)</strong><br>
Important information or explanations
</div>

<div class="success-box">
<strong>Success/Completion (Green)</strong><br>
Achievements, positive outcomes
</div>

<div class="warning-box">
<strong>Warning/Caution (Orange)</strong><br>
Risks, important warnings
</div>

<div class="error-box">
<strong>Error/Critical (Red)</strong><br>
Critical issues, blockers
</div>
```

#### Metric Display (for KPIs and numbers)

```html
<div class="metric-grid">
<div class="metric-box metric-green">
<div class="metric-icon" style="color: #4caf50;">checkmark</div>
<div class="metric-label">Metric Label</div>
<div class="metric-number">99%</div>
<div class="metric-description">Description text</div>
</div>
<!-- metric-blue, metric-orange, metric-red also available -->
</div>
```

#### Step Process Cards

```html
<div class="grid-3">
<div class="step-card">
<div class="step-number">STEP 1</div>
<div class="step-content">
<div class="step-icon">icon</div>
Step description
</div>
</div>
<!-- Repeat for STEP 2, STEP 3 -->
</div>
```

#### Timeline Display

```html
<div class="timeline-item">
<div class="timeline-badge">Month 1</div>
<div>
<strong>Phase Name</strong><br>
Phase description
</div>
</div>
```

#### Badges and Highlights

```html
<div class="success-badge">Completed</div>
<div class="badge">In Progress</div>
<div class="warning-badge">Attention</div>

<span class="highlight">Important keyword</span>
```

#### Grid Layouts

```html
<div class="grid-2">...</div>  <!-- 2-column -->
<div class="grid-3">...</div>  <!-- 3-column -->
<div class="grid-4">...</div>  <!-- 4-column -->
```

### Step 5: Quality Assurance

#### Content Guidelines

1. **One Slide One Message**: Each slide focuses on exactly one key point
2. **3-5 Bullet Maximum**: Limit bullet points per slide
3. **10-Second Scan Rule**: Key information understandable in 10 seconds
4. **Footer Clearance**: Leave at least 100px from last content to footer
5. **Table Limits**: Maximum 5 rows per table (excluding header)
6. **Content Density**: Maximum 8 bullet items per slide

#### Title Length Optimization (Cover Page)

- **Short (1-15 chars)**: Default template font sizes
- **Medium (16-30 chars)**: Apply `font-size: 1.8rem` for h1
- **Long (31+ chars)**: Apply `font-size: 1.6rem` for h1, consider `<br>` for line breaks

#### Self-Review Checklist

Before finalizing, review against `references/presentation_best_practices_checklist.md`:

- [ ] Purpose and audience clearly defined
- [ ] Logical flow (Introduction → Problem → Solution → Effect → Action)
- [ ] Font sizes readable (headings 36-60pt, body 24-30pt)
- [ ] Color palette consistent (primary: #1a237e, secondary: #3949ab)
- [ ] High contrast ratio (4.5:1 minimum)
- [ ] Footer on every content page
- [ ] No content overlapping footer area

### Step 6: Automated Visual Review

After creating the presentation, run the automated visual review:

```bash
# 1. Convert to HTML
marp presentation.md -o presentation.html

# 2. Setup review tools (first time only)
cd scripts && ./setup-review-tools.sh

# 3. Run visual review
node visual-review.js ../presentation.html

# 4. Check results
open review-output/review-report.html
```

The visual review detects:
- **Footer Overlap** (High severity): Content extending into bottom 100px
- **Content Overflow** (Medium severity): Elements exceeding slide boundaries
- **Layout Issues** (Low severity): Minor alignment problems

Quality scoring:
- 100 points = perfect
- -20 points per footer overlap
- -10 points per content overflow
- Target: 80+ points per slide

### Step 7: Export

**Using Cursor/VS Code with Marp Extension**:
- Cmd+Shift+P → "Marp: Export Slide Deck"
- Choose format: PDF (recommended), HTML, or PPTX

**Using Command Line**:
```bash
# PDF (most common)
marp --pdf presentation.md -o presentation.pdf

# HTML
marp --html presentation.md -o presentation.html

# Editable PPTX (requires LibreOffice)
npx @marp-team/marp-cli@latest presentation.md --pptx-editable -o presentation.pptx
```

## Brand Guidelines

### Color Palette

| Purpose | Color | Hex Code |
|---------|-------|----------|
| Primary | Dark Blue | #1a237e |
| Secondary | Blue | #3949ab |
| Accent | Light Blue | #5c6bc0 |
| Success | Green | #4caf50 |
| Warning | Orange | #ff9800 |
| Info | Blue | #2196f3 |
| Error | Red | #f44336 |
| Text | Dark Gray | #212121 |

### Cover Gradient

```css
linear-gradient(135deg, #4a90a4 0%, #2b5797 25%, #1e3a8a 75%, #1a237e 100%)
```

### Fonts

- **Title Font**: Bahnschrift, Arial Black, sans-serif
- **Body Font**: Lato, Segoe UI, Tahoma, Geneva, Verdana, sans-serif
- **Light Font**: Lato Light, Segoe UI Light, sans-serif

### Typography Guidelines

| Element | Size | Weight |
|---------|------|--------|
| Cover Title (h1) | 1.7rem | 300 |
| Cover Subtitle (h2) | 1.1rem | 300 |
| Content Title (h1) | 2.1rem | 600 |
| Section Heading (h2) | 1.6rem | 500 |
| Subsection (h3) | 1.3rem | 500 |
| Body Text | 19px | 400 |

## Resources

### scripts/

- `visual-review.js`: Automated visual quality check using Puppeteer
- `setup-review-tools.sh`: One-time setup script for review dependencies
- `package.json`: Node.js dependencies

### references/

- `presentation_best_practices_checklist.md`: Comprehensive quality checklist covering preparation, design, content, delivery, and accessibility

### assets/

- `FUJISOFT_America_Slide_Template.md`: Complete MARP template with all CSS styles and example slides

## Common Issues and Solutions

### Footer Overlap

**Problem**: Content extends into footer area

**Solution**:
- Split tables across multiple slides (max 5 rows per slide)
- Reduce bullet points (max 6-8 items)
- Add `margin-bottom: 120px` to last content element

### Long Title on Cover Page

**Problem**: Title wraps awkwardly or is too small

**Solution**:
```markdown
<!-- _class: cover -->
# <span style="font-size: 1.5rem; color: rgba(255,255,255,0.9);">LONG PROJECT<br>TITLE HERE</span>
```

### Content Density Too High

**Problem**: Slide feels cluttered

**Solution**:
- Apply "One Slide One Message" principle
- Split content across multiple slides
- Use visual hierarchy (info boxes, grids) to organize
- Prioritize by importance, move details to appendix

### Gray Rectangles Behind Cards in PDF

**Problem**: When exporting to PDF via `marp --pdf`, cards (`.step-card`, `.metric-card`, `.tier-card`, etc.) show gray rectangles behind them. This is caused by CSS `box-shadow` — Marp's Chromium-based PDF renderer draws `box-shadow` as visible gray boxes instead of subtle shadows.

**Solution**:
- **Never use `box-shadow`** in any CSS when the output will be PDF
- Use `border` instead for visual separation:
  ```css
  /* BAD — causes gray rectangles in PDF */
  .step-card { box-shadow: 0 2px 6px rgba(0,0,0,0.1); }

  /* GOOD — clean in both HTML and PDF */
  .step-card { border: 1px solid #e0e0e0; }
  ```
- For elements that already have `border-left` (`.info-box`, `.success-box`, etc.) or `border` (`.metric-box`), simply remove `box-shadow` — no replacement needed
- The template (`assets/FUJISOFT_America_Slide_Template.md`) has already been updated to exclude all `box-shadow` properties
- The only acceptable use of `box-shadow` is `box-shadow: none;` (to explicitly disable shadows on elements like tables)
