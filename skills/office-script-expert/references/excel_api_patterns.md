# ExcelScript API Patterns

## #1: Reading Sheet Data (Header-Based Column Lookup)

Always use dynamic header lookup instead of hardcoded column indices:

```typescript
function loadStores(workbook: ExcelScript.Workbook): Map<string, StoreMaster> {
  const sheet = workbook.getWorksheet("M_Store");
  if (!sheet) throw new Error("M_Store sheet not found");

  const data = sheet.getUsedRange()?.getValues() ?? [];
  // Dynamic header detection
  const headers = (data[0] as (string | number)[]).map((h) =>
    String(h).trim().toLowerCase()
  );
  const stores = new Map<string, StoreMaster>();

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const code = String(row[headers.indexOf("store_code")]).trim();
    if (!code) continue;
    stores.set(code, {
      storeCode: code,
      storeName: String(row[headers.indexOf("store_name")]).trim(),
      // ...
    });
  }
  return stores;
}
```

**Key points**:
- `getUsedRange()?.getValues()` returns a 2D array of `(string | number | boolean)[][]`
- Always null-check `getUsedRange()` (empty sheets return `undefined`)
- Use `headers.indexOf("column_name")` for column positions
- Normalize headers: `.trim().toLowerCase()` (and optionally `.replace(/\s+/g, "_")`)

## #2: Writing Data to Sheets (Batch setValues)

Always write entire ranges at once for performance:

```typescript
function writePrepList(workbook: ExcelScript.Workbook, results: PrepRequirement[]): void {
  const sheet = workbook.getWorksheet("Prep List");
  if (!sheet) throw new Error("Prep List sheet not found");

  // Build 2D array
  const values = results.map((r) => [
    r.prepItemName,
    r.prepCategory,
    r.storeCode,
    r.requiredQty,
    r.unit,
    r.stockQty,
    r.shortageQty,
  ]);

  // Write entire range at once
  const range = sheet.getRangeByIndexes(2, 0, values.length, 7);
  range.setValues(values);
}
```

**Key points**:
- `getRangeByIndexes(startRow, startCol, rowCount, colCount)` - all 0-indexed
- Column count in `setValues` must match the inner array length exactly
- Use empty string `""` for blank cells (not `null` or `undefined`)

## #3: Sheet Protection: Unprotect -> Write -> Protect

Sheets with protection will throw runtime errors on write operations.
**Always wrap write operations with unprotect/protect**:

```typescript
function writeResults(sheet: ExcelScript.Worksheet, data: any[][]): void {
  // 1. Unprotect
  const protection = sheet.getProtection();
  if (protection.getProtected()) {
    protection.unprotect();  // No password for data sheets
  }

  // 2. Write
  // ... clear old data, write new data ...

  // 3. Re-protect
  protection.protect();
}
```

**Common mistake**: Forgetting to re-protect in error paths. Consider try/finally:

```typescript
const protection = sheet.getProtection();
const wasProtected = protection.getProtected();
if (wasProtected) protection.unprotect();

try {
  // ... write operations ...
} finally {
  if (wasProtected) protection.protect();
}
```

## #4: Excel Date Serial Number Conversion

Excel stores dates as serial numbers (days since 1899-12-30).
Convert to JavaScript Date:

```typescript
function excelDateToJsDate(serial: number): Date {
  const epoch = new Date(1899, 11, 30);  // Dec 30, 1899
  return new Date(epoch.getTime() + serial * 86400000);
}
```

**When to use**: Reading date cells where `getValue()` returns a number.

```typescript
const val = dashboard.getRange("C3").getValue();
if (typeof val === "number" && val > 0) {
  const date = excelDateToJsDate(val);
}
```

## #5: Sheet Names with Spaces in Formulas

When referencing sheets with spaces in formulas or named references,
**always quote the sheet name**:

```typescript
// WRONG - will cause formula error:
const formula = `=Busy Index!A1`;

// CORRECT - quoted sheet name:
const formula = `='Busy Index'!A1`;
```

This applies to:
- `setFormula()` / `setFormulaR1C1()`
- Any dynamic formula construction
- Named range references

## #6: Section-Based Sheet Parsing (State Machine)

For sheets with multiple data sections (e.g., M_Recipe with MENU_PREP, MENU_INGREDIENT, PREP_INGREDIENT sections), use a section-tracking state machine:

```typescript
let currentSection = "";
let currentHeaders: string[] = [];

for (const row of allValues) {
  const firstCell = String(row[0]).trim();

  // Detect section separators
  if (firstCell.startsWith("--- MENU_PREP")) {
    currentSection = "MENU_PREP";
    currentHeaders = [];  // Reset headers for new section
    continue;
  } else if (firstCell.startsWith("--- MENU_INGREDIENT")) {
    currentSection = "MENU_INGREDIENT";
    currentHeaders = [];
    continue;
  }

  // Detect column header rows
  const lower = firstCell.toLowerCase();
  if (lower === "recipe_type") {
    currentHeaders = row.map((h) => String(h).trim().toLowerCase());
    continue;
  }

  if (!firstCell || currentHeaders.length === 0) continue;

  // Process data rows based on currentSection
  if (currentSection === "MENU_PREP") {
    // ... parse MENU_PREP row using currentHeaders indices
  }
}
```

**Key points**:
- Reset `currentHeaders = []` on section change (sections may have different column layouts)
- Skip rows until both `currentSection` and `currentHeaders` are set
- Stop processing at empty rows or next section header

## #7: CSV Dual-Mode Reading (Single Cell vs Cell Grid)

When users paste CSV data, it may land in Excel as:
- **Single cell**: All CSV text in A1 (one long string with newlines)
- **Cell grid**: Data spread across cells (Excel auto-parsed on paste)

**Always handle both modes**:

```typescript
const a1Value = String(csvSheet.getRange("A1").getValue()).trim();
let rows: string[][];

if (a1Value.includes(",") && a1Value.includes("\n")) {
  // Mode A: Raw CSV text in single cell
  rows = parseCsvText(a1Value);
} else {
  // Mode B: Cell grid — read used range
  const usedRange = csvSheet.getUsedRange();
  if (!usedRange) throw new Error("No data found");
  const allValues = usedRange.getValues();

  // Find header row (first row with 3+ non-empty cells)
  let headerRowIdx = -1;
  for (let r = 0; r < allValues.length; r++) {
    let nonEmpty = 0;
    for (let c = 0; c < allValues[r].length; c++) {
      if (allValues[r][c] !== null && allValues[r][c] !== "") nonEmpty++;
    }
    if (nonEmpty >= 3) { headerRowIdx = r; break; }
  }

  rows = [];
  for (let r = headerRowIdx; r < allValues.length; r++) {
    const row = allValues[r].map((v) => v === null ? "" : String(v));
    if (row.some((cell) => cell !== "")) rows.push(row);
  }
}
```

## #8: Data Clear with Section Position Pre-Location

**Critical pattern**: When clearing data in a section-based sheet, locate section positions **before** clearing. Otherwise the section markers get destroyed and can't be found.

```typescript
// CORRECT: Pre-locate BEFORE clearing
const invValues = sheet.getUsedRange()?.getValues() ?? [];
let prepDataStartRow = 2;
let ingDataStartRow = 20;

for (let i = 0; i < invValues.length; i++) {
  const cell = String(invValues[i][0]).trim().toLowerCase();
  if (cell.includes("prep item inventory")) {
    prepDataStartRow = i + 2;  // section header + column header + data
  }
  if (cell.includes("ingredient inventory")) {
    ingDataStartRow = i + 2;
  }
}

// NOW clear data (only data rows, preserving section headers and column headers)
clearInventoryData(sheet, prepDataStartRow, ingDataStartRow);
```

**Anti-pattern**: Clear first, then search for section positions -> positions are gone!

## #9: Rounding Precision (Python Compatibility)

The system uses 4 rounding functions matching Python behavior per requirement 6.9.1:

| Step | Function | Python Equivalent | Purpose |
|------|----------|-------------------|---------|
| Step 1 | `roundHalfEven2(value)` | `round(value, 2)` | Adjusted sales = forecast * busy_index |
| Step 2 | `roundUp2(value)` | `math.ceil(v*100)/100` | Prep quantity = adjusted_sales * recipe_qty |
| Steps 3-5 | `roundUp4(value)` | `math.ceil(v*10000)/10000` | Ingredient qty in lb |
| Step 4 | `roundDown4(value)` | `math.floor(v*10000)/10000` | CK transfer (prevent over-allocation) |

**Important**: Excel's built-in `ROUND()` uses half-up rounding, which differs from Python's `round()` (half-even / banker's rounding). The custom `roundHalfEven2` function ensures consistency with the Python calculation engine.

### Known Edge Case

```typescript
// 0.005: TypeScript roundHalfEven2(0.005) = 0.00
//        Python     round(0.005, 2)       = 0.01
// Difference due to IEEE 754 representation.
// Acceptable: only affects values near 0, not business calculations.
```
