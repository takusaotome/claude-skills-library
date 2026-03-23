# Consistency Rule Catalog

## Purpose

This catalog provides a comprehensive list of consistency rule categories that should be checked when a change propagates across multiple modules. Each category includes a definition, common failure patterns, and example rules to adapt to your specific change.

## Category 1: Aggregation Totals

### Definition
Rules that ensure sums, counts, and computed totals remain consistent across all levels of aggregation and all views of the same data.

### Common Failure Patterns
- Report total does not match the sum of line items because a new line type was added but not included in the aggregation query
- Subtotal at module A includes a category that subtotal at module B excludes
- Aggregation uses different rounding at the line level vs the total level, causing penny discrepancies
- Batch aggregation job uses a stale snapshot while real-time API uses live data

### Example Rules
- `SUM(line_amounts) == reported_total` for every report that shows a total
- All aggregation queries include the same WHERE clause filters for the affected data type
- Rounding is applied after summation, not before (or vice versa, but consistently)
- Excluded items are explicitly documented and consistent across all aggregation points

## Category 2: Status Transitions

### Definition
Rules that ensure state machine behavior is identical at every entry point and enforcement boundary.

### Common Failure Patterns
- A new status is added to the enum but not to the guard conditions at all entry points
- One API endpoint allows a transition (e.g., PENDING to CANCELLED) that another endpoint rejects
- UI allows a button click that the backend would reject, or backend allows a transition the UI does not surface
- Batch job does not check status guards before making transitions

### Example Rules
- The set of allowed status transitions is defined in exactly one place and referenced by all entry points
- Every entry point (UI, API, batch, event handler) validates transitions against the same rule set
- Invalid transition attempts produce consistent error codes and messages across all entry points
- Status transition audit logs are written by all entry points using the same format

## Category 3: Sign Inversion

### Definition
Rules that ensure forward operations and their reverse counterparts produce mathematically symmetric results.

### Common Failure Patterns
- Refund calculates tax on the refunded amount differently than the original sale calculated tax
- Void entry does not reverse all components (e.g., reverses the base amount but not the surcharge)
- Correction entry uses subtraction instead of creating a negative-amount line, causing aggregation to miss it
- Rounding adjustment on the forward path has no corresponding reverse rounding adjustment

### Example Rules
- `forward_amount + reverse_amount == 0` for every reversible component
- Reverse operations create distinct line items with negative amounts (not modify existing lines)
- Tax calculation on refund uses the same rate and method as the original transaction
- All adjustment/correction lines are included in aggregation with correct sign

## Category 4: Tax and Rounding

### Definition
Rules that ensure tax calculations and rounding behavior are identical across all calculation paths.

### Common Failure Patterns
- One flow rounds to 2 decimal places while another rounds to the nearest 0.05
- Tax-inclusive vs tax-exclusive calculation is inconsistent between the order entry screen and the invoice generation module
- Rounding is applied at the line-item level in one module and at the total level in another
- Currency-specific rounding rules are hard-coded in one module but read from configuration in another

### Example Rules
- All modules reference the same tax rate source (configuration table, tax service API)
- Rounding mode (HALF_UP, HALF_EVEN, FLOOR, CEILING) is defined once and used everywhere
- Rounding precision is defined per currency and applied consistently
- Tax calculation order (tax on rounded amount vs round on taxed amount) is documented and consistent
- Tax-inclusive and tax-exclusive displays are clearly labeled and computed from the same base values

## Category 5: Visibility and Permission

### Definition
Rules that ensure the same data is visible or hidden to the same roles and contexts across all access paths.

### Common Failure Patterns
- A report shows data that the corresponding API endpoint filters out for the same role
- A new field is added to the database but not masked in the export for roles that should not see it
- UI hides a column for non-admin users but the CSV export includes it
- Tenant isolation is enforced in the API layer but not in the batch report generation

### Example Rules
- Field-level visibility rules are defined once and applied at the data access layer (not duplicated in each consumer)
- Every data access path (API, report, export, batch) applies the same permission filter
- New fields default to restricted visibility and are explicitly opened for each role
- Tenant isolation is enforced at the query level, not just the presentation level

## Category 6: Naming and Constants

### Definition
Rules that ensure enum values, status codes, error codes, and other constants are consistent across all modules that reference them.

### Common Failure Patterns
- A new status value is added to the backend enum but the frontend uses a hard-coded list that does not include it
- Error codes are defined as string literals in multiple modules with slight variations (e.g., "NOT_FOUND" vs "not_found" vs "NotFound")
- API response uses a different field name than the database column for the same concept
- Configuration key names are inconsistent between environments or modules

### Example Rules
- Enum values are defined in a single shared definition (proto file, constants file, database table) and generated or imported by all consumers
- Error codes follow a documented naming convention and are defined in one location
- API field names follow a consistent convention (camelCase, snake_case) across all endpoints
- Configuration keys follow a namespace convention (e.g., `module.feature.setting`) and are documented

## Category 7: Report vs Drill-Down

### Definition
Rules that ensure summary-level numbers in reports match the sum of the detail-level numbers when the user drills down.

### Common Failure Patterns
- Summary report uses a materialized view that is refreshed hourly while drill-down queries live data
- Summary report includes archived records but drill-down only shows active records
- Summary report rounds each category total independently while drill-down sums unrounded values
- Filter criteria differ between the summary query and the drill-down query (different date ranges, different status filters)

### Example Rules
- Summary total for any category equals `SUM(drill-down rows for that category)` at any point in time
- Both summary and drill-down use the same data source (or the materialized view refresh is triggered before report generation)
- Both summary and drill-down apply identical filter criteria (date range, status, entity type)
- Rounding in summary is applied after summing the same values that appear in drill-down

## Cross-Category Patterns

### The "New Line Type" Pattern
When a new line type is introduced (e.g., rounding adjustment, discount line, surcharge):
- Check Category 1: Is it included in all aggregation totals?
- Check Category 3: Does the reverse flow handle it?
- Check Category 4: Is tax calculated on it?
- Check Category 7: Does it appear in both summary and drill-down?

### The "New Status" Pattern
When a new status is introduced:
- Check Category 2: Are all transition rules updated at all entry points?
- Check Category 5: Are visibility rules defined for the new status?
- Check Category 6: Is the constant defined in the shared enum?
- Check Category 1: Are aggregation queries updated to include or exclude the new status?

### The "New Field" Pattern
When a new field is added:
- Check Category 5: Are visibility and permission rules defined?
- Check Category 6: Is the naming consistent with conventions?
- Check Category 7: Does it appear correctly in reports and drill-downs?
- Check Category 1: If it is a numeric field, is it included in relevant aggregations?

## Using This Catalog

1. For each change kernel, scan all 7 categories and identify which are applicable
2. For each applicable category, write specific rules tailored to the change
3. For each rule, identify all modules/flows/reports where it must be verified
4. Populate the consistency matrix with one row per module and one column per rule
5. Mark each cell as PASS / FAIL / NOT TESTED / NOT APPLICABLE
6. Every FAIL cell must produce an action item with an owner and deadline
