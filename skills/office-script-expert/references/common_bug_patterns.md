# Common Bug Patterns in Office Scripts Development

This document catalogs 13 real-world bugs discovered during the development of
CalculateRequirements.ts and ImportCsvData.ts for the Round1 Food Hall project.

---

## Part A: Bugs Discovered and Fixed During Development (6 items)

### Bug D1: CSV Single-Cell Assumption

**Severity**: High
**Script**: ImportCsvData.ts
**Symptom**: CSV import fails or reads only one row when data is pasted across cells.
**Root Cause**: Original code assumed CSV text always lands in cell A1 as a single string.
When Excel auto-splits pasted CSV across cells, A1 contains only the first field.
**Fix**: Implement dual-mode detection:
```typescript
if (a1Value.includes(",") && a1Value.includes("\n")) {
  rows = parseCsvText(a1Value);  // Single-cell mode
} else {
  rows = readCellGrid(csvSheet);  // Cell-grid mode
}
```
**Lesson**: Always test both paste modes. Users may paste CSV differently depending on their Excel version and settings.

---

### Bug D2: Sheet Protection Write Failure

**Severity**: High
**Script**: CalculateRequirements.ts, ImportCsvData.ts
**Symptom**: Runtime error "The object is protected" when writing results.
**Root Cause**: Output sheets (Prep List, Ingredient List, Dashboard) have sheet protection
enabled for end-user safety. Write operations fail without unprotecting first.
**Fix**: Wrap every write function with unprotect/protect:
```typescript
const protection = sheet.getProtection();
if (protection.getProtected()) protection.unprotect();
// ... write ...
protection.protect();
```
**Lesson**: Check **every** sheet that receives writes. Don't assume only "output" sheets are protected; Dashboard KPI cells are also protected.

---

### Bug D3: Section Header Destruction on Clear

**Severity**: High
**Script**: ImportCsvData.ts
**Symptom**: After inventory import, section headers ("--- Prep Item Inventory ---") disappear.
Subsequent imports fail because section positions cannot be found.
**Root Cause**: `sheet.getUsedRange().clear()` deletes everything including section markers
and column headers. Only data rows should be cleared.
**Fix**: Calculate exact data row ranges and clear only those:
```typescript
// Clear only data rows between section header+column header and next section
const prepRowCount = ingDataStartRow - 2 - prepDataStartRow;
sheet.getRangeByIndexes(prepDataStartRow, 0, prepRowCount, totalCols)
  .clear(ExcelScript.ClearApplyTo.contents);
```
**Lesson**: Never use blanket `getUsedRange().clear()` on section-based sheets. Always preserve structural elements (section headers, column headers).

---

### Bug D4: Section Position Search After Clear

**Severity**: High
**Script**: ImportCsvData.ts
**Symptom**: Section positions return wrong row numbers or default fallback values.
**Root Cause**: Code searched for section headers AFTER clearing the sheet, but clear
had already removed the section header text.
**Fix**: Pre-locate section positions BEFORE any clearing:
```typescript
// Step 1: Read positions
const invValues = sheet.getUsedRange()?.getValues() ?? [];
let prepDataStartRow = 2; // fallback
for (let i = 0; i < invValues.length; i++) { /* find positions */ }

// Step 2: Clear (positions already saved)
clearInventoryData(sheet, prepDataStartRow, ingDataStartRow);
```
**Lesson**: Ordering matters. Any "find then act" pattern must complete the find phase before the destructive act phase.

---

### Bug D5: Unquoted Sheet Names in Formulas

**Severity**: Medium
**Script**: CalculateRequirements.ts
**Symptom**: Formula errors (`#REF!`) when referencing sheets with spaces.
**Root Cause**: Sheet names like "Busy Index" or "Forecast Input" must be quoted
in Excel formula syntax: `'Busy Index'!A1`, not `Busy Index!A1`.
**Fix**: Always wrap sheet names in single quotes for formula references.
**Lesson**: Even if you're not writing formulas, be aware that cross-sheet references in
comments or documentation should use the quoted form.

---

### Bug D6: Rounding Method Mismatch

**Severity**: Medium
**Script**: CalculateRequirements.ts
**Symptom**: Calculated values differ slightly from Python web app results.
**Root Cause**: Using `Math.round()` (half-up) instead of banker's rounding (half-even)
for Step 1 calculations. Python's `round()` uses half-even.
**Fix**: Implement `roundHalfEven2()` to match Python behavior:
```typescript
function roundHalfEven2(value: number): number {
  const shifted = value * 100;
  const floored = Math.floor(shifted);
  if (shifted === floored + 0.5) {
    return (floored % 2 === 0 ? floored : floored + 1) / 100;
  }
  return Math.round(shifted) / 100;
}
```
**Lesson**: When porting calculations between languages, verify rounding semantics.
JavaScript `Math.round()` != Python `round()` at the 0.5 boundary.

---

## Part B: Bugs Found During Code Review (7 items, potentially unresolved)

### Bug R1: Recipe Import Diff-Only Without Data Update

**Severity**: High
**Script**: ImportCsvData.ts (recipe mode)
**Symptom**: Recipe import shows diff summary ("+3 ~1 -0") on Dashboard but the M_Recipe
sheet data remains unchanged. Users think the import succeeded.
**Root Cause**: The recipe import code computes `detectRecipeDiff()` and writes summary
to Dashboard, but never actually writes the new recipe data to the M_Recipe sheet.
Only the diff display logic was implemented.
**Fix Required**: After computing diffs, apply the changes to M_Recipe sheet:
- Added rows: Insert new recipe rows in the appropriate section
- Modified rows: Update qty_per_serving for changed recipes
- Removed rows: Clear or mark removed recipe rows
**Lesson**: Always verify that an "import" function actually imports data, not just displays what would change. End-to-end testing would catch this.

---

### Bug R2: item_type Absence Causes Over-Skipping in ING21

**Severity**: High
**Script**: ImportCsvData.ts (inventory mode)
**Symptom**: When CSV lacks the `item_type` column, rows with valid ING/PREP-prefixed
item codes are skipped if their Eatec Number is not in the master mapping.
**Root Cause**: The fallback logic chain is:
1. Check `item_type` column (if exists) -> set type
2. If no type AND isIng21 -> lookup Eatec Number -> skip if not found
3. Infer from item_code prefix (ING*/PREP*)

Step 2 short-circuits: if `isIng21` is true (detected by header heuristic), items
without Eatec Number mapping are skipped **before reaching** the prefix-based fallback.
**Fix Required**: Allow prefix-based fallback even for ING21 format:
```typescript
if (!itemType && isIng21 && eatecNumberMap.size > 0) {
  const mapping = eatecNumberMap.get(rawItemCode);
  if (mapping) {
    itemType = mapping.itemType;
    itemCode = mapping.itemCode;
  }
  // DON'T skip here - fall through to prefix-based detection
}
if (!itemType) {
  // Prefix-based fallback for all formats
  if (itemCode.startsWith("ING")) itemType = "ingredient";
  else if (itemCode.startsWith("PREP")) itemType = "prep";
  else { warnings.push(...); continue; }
}
```
**Lesson**: Verify all code paths in fallback chains. Short-circuit `continue` can bypass valid downstream logic.

---

### Bug R3: prepPrepRecipes Always Empty

**Severity**: High
**Script**: CalculateRequirements.ts
**Symptom**: PREP->PREP hierarchical recipes (e.g., a prep item made from another prep item)
are never expanded. Ingredient calculations are underestimated.
**Root Cause**: `loadRecipes()` parses MENU_PREP, MENU_INGREDIENT, and PREP_INGREDIENT
sections, but has **no parsing logic for PREP_PREP** section. The `prepPrepRecipes` Map
is initialized empty and never populated.
**Fix Required**: Add PREP_PREP section detection and parsing in `loadRecipes()`:
```typescript
} else if (firstCell.startsWith("--- PREP_PREP")) {
  currentSection = "PREP_PREP";
  currentHeaders = [];
  continue;
}

// In data processing:
if (currentSection === "PREP_PREP") {
  const parentCode = String(row[srcIdx]).trim();
  const recipe: PrepPrepRecipe = {
    prepItemCode: parentCode,
    childPrepItemCode: String(row[tgtIdx]).trim(),
    qtyPerUnit: Number(row[qtyIdx]),
    isActive: toBool(row[activeIdx]),
  };
  if (!prepPrepRecipes.has(parentCode)) {
    prepPrepRecipes.set(parentCode, []);
  }
  prepPrepRecipes.get(parentCode)!.push(recipe);
}
```
**Lesson**: When a function returns multiple data structures, verify each one is actually populated. `expandPrepHierarchy` supports PREP->PREP, but the data loader doesn't feed it.

---

### Bug R4: safety_stock_qty Not Applied to Order Calculation

**Severity**: High
**Script**: CalculateRequirements.ts
**Symptom**: Order lots cover only the shortage quantity. If the ingredient has a safety stock
requirement, the order may be insufficient.
**Root Cause**: `IngredientMaster.safetyStockQty` is loaded from the sheet but never used
in `calculateIngredientRequirements()` or `calculateOrderLots()`.
**Fix Required**: Add safety stock to shortage calculation:
```typescript
const effectiveShortage = shortageLb + (ingredient.safetyStockQty ?? 0);
const orderLots = effectiveShortage > 0
  ? calculateOrderLots(effectiveShortage, ingredient.lbPerLot, ingredient.minOrderLot)
  : 0;
```
**Lesson**: When porting business logic, audit all master data fields. If a field is loaded but never referenced in calculations, it's likely a missed requirement.

---

### Bug R5: Recipe Header Assumption Mismatch

**Severity**: Medium
**Script**: ImportCsvData.ts / CalculateRequirements.ts
**Symptom**: Recipe import and recipe reading may fail if workbook headers don't match expected names.
**Root Cause**: The workbook M_Recipe sheet uses `source_code`, `source_name`, `target_code`
as column headers. But the CSV import uses `menu_code`, `component_code`, `component_type`.
The `readCurrentRecipes()` function expects workbook headers, while `parseRecipeRows()`
expects CSV headers. If either format changes, the wrong parser may be applied.
**Fix Required**: Document and enforce a single canonical column naming for each format.
Add validation that detects and reports header mismatches:
```typescript
const requiredWorkbookHeaders = ["recipe_type", "source_code", "target_code", "qty_per_serving"];
const missingHeaders = requiredWorkbookHeaders.filter(h => !currentHeaders.includes(h));
if (missingHeaders.length > 0) {
  throw new Error(`M_Recipe header mismatch: missing ${missingHeaders.join(", ")}`);
}
```
**Lesson**: When two systems exchange data with different column naming conventions, explicitly document the mapping and validate on read.

---

### Bug R6: CSVImport Clear Scope Insufficient

**Severity**: Medium
**Script**: ImportCsvData.ts
**Symptom**: After import, stale data from a previous (larger) CSV may remain in CSVImport sheet.
The next import may pick up leftover rows.
**Root Cause**: The CSV import clears with `csvSheet.getUsedRange().clear(...)`.
If `getUsedRange()` returns `undefined` (edge case), no clearing occurs. Also, if the
user pastes data beyond the used range (e.g., formatting exists), leftover data may persist.
**Fix Required**: Clear a generous fixed range or track previous import bounds:
```typescript
// Safe: clear the entire used range, plus a buffer
const csvUsedRange = csvSheet.getUsedRange();
if (csvUsedRange) {
  csvUsedRange.clear(ExcelScript.ClearApplyTo.contents);
}
// Additional safety: clear a fixed range (e.g., A1:Z1000)
```
**Lesson**: When a sheet is used as a data staging area, ensure complete cleanup. Residual data is a silent bug.

---

### Bug R7: Negative on_hand_qty Silently Zeroed

**Severity**: Low
**Script**: ImportCsvData.ts
**Symptom**: Negative inventory quantities (e.g., -5 from Eatec data errors) are silently
converted to 0 with only a warning. Downstream calculations produce incorrect results
because the negative quantity (indicating a data issue) is hidden.
**Root Cause**: `sanitizeQuantity()` clamps negative values to 0 and logs a warning,
but warnings are only written to Dashboard summary (count), not the actual warning text.
Users cannot see which items had data issues.
**Fix Required**:
1. Write individual warnings to a "Import Log" section or separate sheet
2. Consider preserving negative values with a flag, allowing users to investigate
3. At minimum, include the warning details in Dashboard output (not just count)
**Lesson**: Silent data correction is dangerous. Make data quality issues visible to users,
especially when the correction affects downstream calculations.
