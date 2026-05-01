# MARP Layout Patterns and Anti-Patterns

This reference documents common MARP layout patterns, their proper implementation, and anti-patterns to avoid.

## Slide Structure Fundamentals

### Basic Slide Anatomy

```markdown
---
marp: true
theme: default
paginate: true
---

# Slide Title

Content goes here

---

# Next Slide
```

**Key Rules:**
- Three dashes `---` separate slides
- Frontmatter must be at the very top
- One blank line after the slide separator before content

## Spacing Patterns

### Correct Spacing

```markdown
---

# Title

First paragraph with content.

Second paragraph after one blank line.

- Bullet item 1
- Bullet item 2

---
```

### Anti-Pattern: Excessive Blank Lines

```markdown
---


# Title


First paragraph with content.



Second paragraph after THREE blank lines.  <-- Creates large gap
```

**Fix:** Use exactly one blank line between elements.

### Anti-Pattern: Missing Spacing

```markdown
---
# Title
First paragraph immediately after title.
- Bullet with no space before list
```

**Fix:** Add blank lines between major elements.

## Flexbox Layout Patterns

### Two-Column Layout (Correct)

```markdown
<div class="columns">
<div class="column">

### Left Column
Content here

</div>
<div class="column">

### Right Column
Content here

</div>
</div>
```

CSS:
```css
.columns {
  display: flex;
  gap: 2rem;
}
.column {
  flex: 1;
}
```

### Anti-Pattern: Nested Flex Without Gap

```css
/* BAD */
.columns {
  display: flex;
}
.column {
  flex: 1;
  margin-right: 20px; /* Creates uneven spacing */
}
```

**Fix:** Use `gap` property instead of margins for flex children.

### Anti-Pattern: Fixed Width in Flex Container

```css
/* BAD */
.column {
  flex: 1;
  width: 400px; /* Conflicts with flex */
}
```

**Fix:** Use `flex-basis` instead of `width` or remove fixed width.

## Bullet List Patterns

### Correct List Formatting

```markdown
- Item one
- Item two
  - Nested item (2 spaces indent)
  - Another nested item
- Back to top level
```

### Anti-Pattern: Mixed Markers

```markdown
- Item with dash
* Item with asterisk  <-- Inconsistent
- Back to dash
```

**Fix:** Use consistent markers (prefer `-` for MARP).

### Anti-Pattern: Wrong Nesting Indentation

```markdown
- Item one
   - Nested with 3 spaces  <-- Should be 2 spaces
    - Nested with 4 spaces  <-- Inconsistent
```

**Fix:** Use exactly 2 spaces for each nesting level.

### Anti-Pattern: No Space After Marker

```markdown
-Item without space  <-- Won't render as list
-Another item
```

**Fix:** Add space after the dash marker.

## Image Layout Patterns

### Centered Image

```markdown
![center](image.png)
```

Or with HTML:
```html
<div style="text-align: center;">

![](image.png)

</div>
```

### Sized Image (Correct)

```markdown
![w:500](image.png)
![h:300](image.png)
![w:500 h:300](image.png)
```

### Anti-Pattern: Oversized Image

```markdown
![](huge-image.png)  <-- No size constraint, may overflow
```

**Fix:** Always specify dimensions for images.

### Anti-Pattern: Percentage Width Without Container

```markdown
<img src="image.png" style="width: 150%;">  <-- Overflows slide
```

**Fix:** Keep images within 100% of container width.

## Code Block Patterns

### Correct Code Block

```markdown
```python
def short_function():
    return "fits on slide"
```
```

### Anti-Pattern: Long Lines

```markdown
```python
def very_long_function_name_that_keeps_going_and_going_and_going_until_it_overflows():
    return "this line is way too long for a presentation slide"
```
```

**Fix:** Break long lines or use smaller font size:
```css
pre {
  font-size: 0.7em;
}
```

### Anti-Pattern: Too Many Lines

```markdown
```python
# 50+ lines of code that requires scrolling
```
```

**Fix:** Show only essential code; use `<!-- fit -->` directive or split across slides.

## Table Patterns

### Responsive Table

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Short    | Data     | Here     |
```

### Anti-Pattern: Wide Table

```markdown
| Very Long Header 1 | Very Long Header 2 | Very Long Header 3 | Very Long Header 4 | Very Long Header 5 |
|--------------------|--------------------|--------------------|--------------------|--------------------|
| Data               | More Data          | Even More          | Still Going        | Overflow           |
```

**Fix:**
- Reduce columns
- Use abbreviations
- Apply smaller font via CSS
- Split into multiple slides

## CSS Specificity Patterns

### Correct: Low Specificity

```css
/* Theme-level styles */
section {
  background: white;
}

/* Slide-specific override */
section.dark {
  background: #333;
}
```

### Anti-Pattern: Specificity War

```css
/* BAD */
section.custom-slide h1.title span.text {
  color: blue !important;
}
```

**Fix:** Keep selectors simple; avoid `!important` unless absolutely necessary.

### Anti-Pattern: Redundant Rules

```css
/* BAD */
h1 {
  font-size: 2em;
  color: blue;
}

section h1 {
  font-size: 2em;  /* Redundant - same as above */
  color: red;
}
```

**Fix:** Remove redundant declarations.

## Responsive Design Patterns

### Container Query for Content

```css
section {
  container-type: inline-size;
}

@container (max-width: 800px) {
  .columns {
    flex-direction: column;
  }
}
```

### Anti-Pattern: Fixed Dimensions

```css
/* BAD */
.box {
  width: 800px;  /* Won't adapt to different viewport */
  height: 400px;
}
```

**Fix:** Use relative units (`%`, `vw`, `vh`, `em`, `rem`).

## Common MARP Directives

### Fit Text to Slide

```markdown
<!-- fit -->
# This Title Will Auto-Size
```

### Background Image

```markdown
![bg](background.jpg)
![bg left:40%](side-image.jpg)
```

### Scoped Style

```markdown
<!-- _class: custom -->

<style scoped>
h1 { color: navy; }
</style>
```

## Diagnostic Checklist

When debugging MARP layouts:

1. **Whitespace Audit**
   - [ ] Single blank lines between elements
   - [ ] No trailing whitespace
   - [ ] Consistent indentation (2 spaces)

2. **Structure Check**
   - [ ] Valid slide separators (`---`)
   - [ ] Proper frontmatter format
   - [ ] Balanced HTML tags

3. **CSS Review**
   - [ ] No `!important` overuse
   - [ ] Reasonable specificity
   - [ ] No conflicting rules

4. **Content Fit**
   - [ ] Images sized appropriately
   - [ ] Code blocks fit horizontally
   - [ ] Tables don't overflow

5. **Responsiveness**
   - [ ] Relative units where appropriate
   - [ ] Flexbox using `gap` not margins
   - [ ] No fixed pixel dimensions on containers
