# Office Script Implementation Checklist

Use this checklist before deploying any new or modified Office Script.

---

## 1. Architecture

- [ ] Pure logic functions are in `lib/*.ts` with `export` keyword
- [ ] Main script has corresponding `// INLINED: lib/*.ts` markers for each inlined function
- [ ] Inlined functions match their `lib/*.ts` canonical versions (no `export` keyword)
- [ ] No `import` / `export` / `require` in main script files
- [ ] No external library dependencies (lodash, date-fns, etc.)

## 2. Map/Set Iteration Safety

- [ ] No `for (const [k, v] of map)` patterns in main scripts
- [ ] All Map/Set iterations use `Array.from(map.entries())` + indexed loop or `.forEach()`
- [ ] Loop index variables use unique names to avoid collision (`_i`, `_ri`, `_ci`, etc.)

## 3. Sheet Protection

- [ ] Every function that writes to a sheet calls `getProtection()` first
- [ ] `unprotect()` is called before any write operation
- [ ] `protect()` is called after write operations complete
- [ ] Protection is re-applied even when there's no data to write (early returns)
- [ ] All sheets that receive writes are checked (including Dashboard for KPI updates)

## 4. Data Reading

- [ ] CSV import handles dual-mode input (single-cell text AND cell grid)
- [ ] Header normalization handles inconsistent casing and spacing
- [ ] Dynamic header lookup used (not hardcoded column indices)
- [ ] `getUsedRange()` null-checked with `?? []` fallback
- [ ] Excel date serial numbers converted via `excelDateToJsDate()`

## 5. Section-Based Sheets

- [ ] Section positions are located BEFORE any data clearing
- [ ] Only data rows are cleared (section headers and column headers preserved)
- [ ] Section state machine resets `currentHeaders = []` on section change
- [ ] Empty rows and unrecognized sections are skipped gracefully

## 6. Calculation Logic

- [ ] Step 1 uses `roundHalfEven2()` (not `Math.round()`)
- [ ] Step 2 uses `roundUp2()` (ceiling to 2 decimal places)
- [ ] Steps 3-5 use `roundUp4()` (ceiling to 4 decimal places)
- [ ] Step 4 CK transfer uses `roundDown4()` (floor to prevent over-allocation)
- [ ] `safety_stock_qty` is included in order lot calculation (if applicable)
- [ ] `min_order_lot` is applied as minimum for `calculateOrderLots()`
- [ ] Yield rate and loss rate are applied: `effective_yield = yield_rate * (1 - loss_rate)`
- [ ] PREP->PREP hierarchy is expanded (not just PREP->INGREDIENT)

## 7. Header Consistency

- [ ] Workbook M_Recipe uses: `recipe_type`, `source_code`, `source_name`, `target_code`, `qty_per_serving`, `unit`, `location_applicable`, `is_active`
- [ ] CSV recipe import uses: `menu_code`, `menu_name`, `brand_name`, `component_type`, `component_code`, `component_name`, `qty_per_serving`, `input_uom`
- [ ] CSV inventory import uses: `location_code`, `item_code`, `item_name`, `on_hand_qty`, `uom` (+ optional: `item_type`, `lot_no`, `expiration_date`)
- [ ] Header aliases are maintained in `HEADER_ALIASES` for Eatec ING21 compatibility

## 8. Clear Operations

- [ ] CSVImport sheet is cleared after import (entire used range, contents only)
- [ ] Inventory Input sheet clears only data rows (preserving section structure)
- [ ] Clear uses `ExcelScript.ClearApplyTo.contents` (not `all`, which removes formatting)

## 9. Testing

- [ ] `npm test` (vitest run) passes with 0 failures
- [ ] Boundary value tests exist for all rounding functions
- [ ] Business scenario tests verify realistic data combinations
- [ ] Python consistency tests verify TypeScript results match Python engine
- [ ] New pure logic functions have corresponding `lib/*.ts` exports and `__tests__/*.test.ts`

## 10. Design Document Synchronization

- [ ] `excel/docs/` design documents updated to match implementation
- [ ] Workbook sheet structure matches design doc specifications
- [ ] Column names and data types match between design doc and script
- [ ] README or change log updated with new features or bug fixes

## 11. Performance

- [ ] All sheet writes use batch `setValues()` (not cell-by-cell)
- [ ] Each sheet is read once (data cached in memory for processing)
- [ ] No redundant `getUsedRange().getValues()` calls on the same sheet
- [ ] Estimated execution time is within 120-second timeout for expected data volumes

## 12. Data Quality

- [ ] Negative quantities are handled with visible warnings (not silent zeroing)
- [ ] Unknown Eatec Numbers generate warnings (not silent skips)
- [ ] Import warnings are written to Dashboard with detail (not just count)
- [ ] Empty/null values in optional fields use explicit defaults (`?? 0`, `?? ""`, `?? null`)
