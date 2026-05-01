# CSS Fix Catalog

Catalog of automated CSS fixes for common MARP layout issues.

## Whitespace Fixes

### WS001: Double Blank Lines

**Detection Pattern:**
```regex
\n{3,}
```

**Auto-Fix:**
Replace with exactly two newlines (`\n\n`).

**Example:**
```diff
- Content before
-
-
-
- Content after
+ Content before
+
+ Content after
```

---

### WS002: Trailing Whitespace

**Detection Pattern:**
```regex
[ \t]+$
```

**Auto-Fix:**
Remove all trailing spaces and tabs from line ends.

**Example:**
```diff
- # Title with trailing spaces
+ # Title with trailing spaces
```

---

### WS003: Tabs Mixed with Spaces

**Detection Pattern:**
```regex
^( *\t|\t+ )
```

**Auto-Fix:**
Convert tabs to 2 spaces.

**Example:**
```diff
- 	- Indented with tab
+   - Indented with spaces
```

---

### WS004: Missing Blank Line Before Header

**Detection Pattern:**
```regex
[^\n]\n#
```

**Auto-Fix:**
Insert blank line before header.

**Example:**
```diff
- Previous paragraph content.
- # Next Section
+ Previous paragraph content.
+
+ # Next Section
```

## Alignment Fixes

### AL001: Margin Instead of Gap in Flexbox

**Detection Pattern:**
```css
.flex-container .child {
  margin-right: *;
}
```

**Auto-Fix:**
Add `gap` to parent, remove child margins.

**Before:**
```css
.columns {
  display: flex;
}
.column {
  flex: 1;
  margin-right: 20px;
}
.column:last-child {
  margin-right: 0;
}
```

**After:**
```css
.columns {
  display: flex;
  gap: 20px;
}
.column {
  flex: 1;
}
```

---

### AL002: Width in Flex Child

**Detection Pattern:**
```css
.flex-child {
  flex: 1;
  width: *px;
}
```

**Auto-Fix:**
Convert `width` to `flex-basis`.

**Before:**
```css
.column {
  flex: 1;
  width: 300px;
}
```

**After:**
```css
.column {
  flex: 1 0 300px;
}
```

---

### AL003: Centering Without Flexbox

**Detection Pattern:**
```css
.center {
  margin-left: auto;
  margin-right: auto;
  text-align: center;
}
```

**Auto-Fix (optional upgrade):**
Use flexbox for more robust centering.

**After:**
```css
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

## Bullet Fixes

### BL001: Mixed List Markers

**Detection Pattern:**
```regex
^(\s*)-.*\n\s*\*
```

**Auto-Fix:**
Normalize all markers to `-`.

**Before:**
```markdown
- First item
* Second item
- Third item
```

**After:**
```markdown
- First item
- Second item
- Third item
```

---

### BL002: 4-Space Nesting

**Detection Pattern:**
```regex
^    -
```

**Auto-Fix:**
Convert 4-space indent to 2-space.

**Before:**
```markdown
- Parent
    - Child with 4 spaces
```

**After:**
```markdown
- Parent
  - Child with 2 spaces
```

---

### BL003: Missing Space After Marker

**Detection Pattern:**
```regex
^(\s*)-[^\s]
```

**Auto-Fix:**
Insert space after marker.

**Before:**
```markdown
-Item without space
```

**After:**
```markdown
- Item with space
```

## Overflow Fixes

### OF001: Long Code Line

**Detection Pattern:**
- Code block with line > 80 characters

**Auto-Fix:**
Add CSS to reduce font size or suggest line breaks.

**CSS Fix:**
```css
pre code {
  font-size: 0.65em;
  white-space: pre-wrap;
  word-break: break-all;
}
```

**Manual Alternative:**
Break long lines with backslash continuation.

---

### OF002: Unsized Image

**Detection Pattern:**
```regex
!\[(?!.*[wh]:).*\]\(
```

**Auto-Fix:**
Add default width constraint.

**Before:**
```markdown
![alt text](large-image.png)
```

**After:**
```markdown
![w:800 alt text](large-image.png)
```

---

### OF003: Table Too Wide

**Detection Pattern:**
- Table with > 5 columns
- Table with any cell > 30 characters

**Auto-Fix:**
Add CSS for table responsiveness.

**CSS Fix:**
```css
table {
  font-size: 0.75em;
  width: 100%;
  table-layout: fixed;
}
td, th {
  word-wrap: break-word;
}
```

## CSS Rule Fixes

### CS001: Redundant Declarations

**Detection Pattern:**
Same property-value pair in both general and specific selector.

**Auto-Fix:**
Remove redundant declaration from more specific selector.

**Before:**
```css
h1 {
  font-size: 2em;
  color: blue;
}
section h1 {
  font-size: 2em;  /* redundant */
  color: red;
}
```

**After:**
```css
h1 {
  font-size: 2em;
  color: blue;
}
section h1 {
  color: red;
}
```

---

### CS002: !important Removal

**Detection Pattern:**
```css
property: value !important;
```

**Auto-Fix:**
- Check if can be removed
- Increase specificity instead if needed

**Before:**
```css
h1 {
  color: blue !important;
}
```

**After:**
```css
section h1 {
  color: blue;
}
```

---

### CS003: Shorthand Optimization

**Detection Pattern:**
Multiple longhand properties that can be combined.

**Auto-Fix:**
Combine into shorthand.

**Before:**
```css
.box {
  margin-top: 10px;
  margin-right: 20px;
  margin-bottom: 10px;
  margin-left: 20px;
}
```

**After:**
```css
.box {
  margin: 10px 20px;
}
```

---

### CS004: Zero Unit Removal

**Detection Pattern:**
```regex
: 0(px|em|rem|%);
```

**Auto-Fix:**
Remove unit from zero values.

**Before:**
```css
.element {
  margin: 0px;
  padding: 0em;
}
```

**After:**
```css
.element {
  margin: 0;
  padding: 0;
}
```

## Fix Priority Matrix

| Issue ID | Severity | Auto-Fix Safe | Risk Level |
|----------|----------|---------------|------------|
| WS001    | Low      | Yes           | None       |
| WS002    | Low      | Yes           | None       |
| WS003    | Medium   | Yes           | Low        |
| WS004    | Low      | Yes           | Low        |
| AL001    | Medium   | Partial       | Medium     |
| AL002    | Medium   | Partial       | Medium     |
| AL003    | Low      | No            | Medium     |
| BL001    | Low      | Yes           | None       |
| BL002    | Medium   | Yes           | Low        |
| BL003    | High     | Yes           | None       |
| OF001    | High     | Partial       | Low        |
| OF002    | Medium   | Yes           | Low        |
| OF003    | Medium   | Partial       | Medium     |
| CS001    | Low      | Yes           | None       |
| CS002    | Medium   | Partial       | Medium     |
| CS003    | Low      | Yes           | None       |
| CS004    | Low      | Yes           | None       |

## Application Order

Apply fixes in this order to avoid conflicts:

1. **Whitespace fixes** (WS*) - Structural changes first
2. **Bullet fixes** (BL*) - Content normalization
3. **Overflow fixes** (OF*) - Size constraints
4. **Alignment fixes** (AL*) - Layout adjustments
5. **CSS fixes** (CS*) - Style optimization

## Rollback Guidelines

All auto-fixes should be reversible. The fix tool:
1. Creates backup of original file
2. Logs all changes made
3. Provides diff output
4. Supports `--dry-run` mode
