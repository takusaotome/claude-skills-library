# Aggregation Reconciliation Guide

## Purpose

This reference provides detailed guidance for verifying that aggregation totals, subtotals, and drill-down details remain consistent across all views, reports, and data access paths. Aggregation inconsistency is one of the most common and most impactful cross-module defects, particularly when new line types, new statuses, or new flows are introduced.

## Total vs Subtotal vs Drill-Down Hierarchy

### Definitions

- **Grand Total**: The highest-level aggregation, typically shown on summary dashboards or executive reports. Example: "Total Revenue: $1,234,567"
- **Subtotal**: A mid-level aggregation grouped by a dimension (department, product category, region, time period). Example: "Revenue by Region: East $500K, West $400K, Central $334K"
- **Drill-Down Detail**: The lowest-level individual records that, when summed, should produce the subtotal or grand total. Example: individual transaction records

### The Reconciliation Invariant

```
Grand Total == SUM(Subtotals) == SUM(Drill-Down Details)
```

This invariant must hold at all times, across all access paths, and for all filter combinations.

### Common Violations

1. **Missing category in subtotal grouping**: A new category is added but the GROUP BY query does not include it, so its records appear in drill-down but not in any subtotal.

2. **Double-counting in subtotal**: A record belongs to multiple groups (e.g., a transaction tagged with two departments) and is counted in each subtotal but only once in the grand total.

3. **Filter mismatch**: The subtotal query uses `status IN ('completed', 'refunded')` but the drill-down query uses `status = 'completed'`, excluding refunded records from drill-down.

4. **Timing mismatch**: The grand total is computed from a materialized view refreshed hourly, while subtotals are computed from live data, causing temporary discrepancies.

5. **Rounding accumulation**: Each subtotal is rounded independently, and the sum of rounded subtotals does not equal the independently rounded grand total.

## Included/Excluded Item Catalog

When a new item type is introduced, it must be explicitly classified as included or excluded for every aggregation point. Use this catalog to track the decisions.

### Classification Framework

For each new item type (line type, status, transaction type, entity category), document:

| Item | Aggregation Point | Included? | Rationale | Verified By |
|------|-------------------|-----------|-----------|-------------|
| Rounding adjustment | Daily cash summary | Yes | Affects cash in drawer | [Reviewer] |
| Rounding adjustment | Tax report | No | Not a taxable event | [Reviewer] |
| Rounding adjustment | Revenue report | Yes | Affects net revenue | [Reviewer] |
| Rounding adjustment | Receipt total | Yes | Customer-facing amount | [Reviewer] |

### Items That Commonly Need Classification

- **Adjustment lines**: Rounding adjustments, price corrections, manual overrides
- **Discount lines**: Coupon discounts, volume discounts, promotional discounts
- **Fee lines**: Surcharges, convenience fees, processing fees
- **Tax lines**: Sales tax, VAT, withholding tax
- **Void/cancelled records**: Voided transactions, cancelled orders
- **Refund/return records**: Full refunds, partial refunds, exchanges
- **Internal transfers**: Inter-department transfers, inter-company transactions
- **Pending/draft records**: Records not yet finalized
- **Archived records**: Historical records moved to archive storage

### The "Should This Be Included?" Decision Tree

```
1. Is this item part of the business metric being aggregated?
   - YES -> Include (unless explicitly excluded by business rule)
   - NO -> Exclude
   - UNCLEAR -> Escalate to business stakeholder for decision

2. If included, does it need special handling?
   - Sign: Should it be positive or negative?
   - Timing: Should it be included at creation time or completion time?
   - Grouping: Which dimension(s) should it be grouped under?

3. Document the decision in the included/excluded item catalog
```

## Report Alignment

### Cross-Report Consistency

When the same data appears in multiple reports, they must agree. Common report pairs that must reconcile:

| Report A | Report B | Reconciliation Rule |
|----------|----------|---------------------|
| Daily summary | Monthly summary | Monthly total = SUM(daily totals for the month) |
| POS report | HQ report | HQ total = SUM(POS totals for all locations) |
| Revenue report | Tax report | Tax base amount in tax report = taxable revenue in revenue report |
| Cash report | Bank reconciliation | Cash report total = bank deposit amount + float |
| UI dashboard | Exported CSV | Every number visible on dashboard appears identically in CSV |
| API response | Database query | API total = database query total (no middleware transformation loss) |

### Report Alignment Verification Procedure

1. **Identify all reports that display the affected data**
2. **For each pair of reports, define the reconciliation formula**
3. **Execute both reports with identical parameters** (date range, filters, entity scope)
4. **Compare results numerically**, not just visually
5. **Investigate any discrepancy**, even if it appears minor (penny differences often indicate systemic issues)
6. **Document the reconciliation result** in the consistency matrix

## Refund/Void Reversal Rules

### The Reversal Invariant

For any reversible operation, the following must hold:

```
original_entry + reversal_entry == expected_net_result
```

Where `expected_net_result` is:
- **Full reversal**: 0 (complete cancellation)
- **Partial reversal**: original - reversed portion
- **Exchange**: original - returned item + new item

### Component-Level Reversal

Every component of the original entry must be reversed:

| Component | Original | Reversal | Net |
|-----------|----------|----------|-----|
| Base amount | +100.00 | -100.00 | 0.00 |
| Tax | +8.00 | -8.00 | 0.00 |
| Discount | -5.00 | +5.00 | 0.00 |
| Rounding adj | +0.02 | -0.02 | 0.00 |
| **Total** | **+103.02** | **-103.02** | **0.00** |

### Common Reversal Failures

1. **Missing component reversal**: The base amount is reversed but the rounding adjustment is not, leaving a penny discrepancy.

2. **Tax recalculation on reversal**: Instead of reversing the original tax amount, the system recalculates tax on the refund amount using a potentially different rate, creating a difference.

3. **Sign error in reversal**: The reversal uses a positive amount instead of negative (or stores the absolute value with a separate "reversal" flag that aggregation queries ignore).

4. **Aggregation exclusion**: Reversal entries exist in the database but are excluded from the aggregation query because they have a different transaction type or status that is not in the WHERE clause.

5. **Timing asymmetry**: The original entry is dated at transaction time but the reversal is dated at processing time, causing them to appear in different reporting periods.

### Reversal Verification Checklist

- [ ] Every component of the original entry has a corresponding reversal component
- [ ] Reversal amounts are the exact negative of original amounts (not recalculated)
- [ ] Reversal entries use the same tax rate as the original (not the current rate)
- [ ] Reversal entries are included in all aggregation queries that include the original
- [ ] Net result of original + reversal equals the expected value (0 for full reversal)
- [ ] Both original and reversal appear in the same reporting period (or the cross-period behavior is documented)
- [ ] Reversal entries are visible in drill-down views
- [ ] Reversal entries have audit trail linking them to the original

## Reconciliation Testing Strategy

### Automated Reconciliation Tests

Create automated tests that verify the reconciliation invariant:

```
Test: Grand total reconciliation
  Given: A set of transactions with known amounts
  When: Grand total is computed
  Then: Grand total == SUM(all transaction amounts including adjustments, refunds, and voids)

Test: Subtotal reconciliation
  Given: A set of transactions across multiple categories
  When: Subtotals are computed per category
  Then: SUM(subtotals) == Grand total
  And: Each subtotal == SUM(transactions in that category)

Test: Report cross-reconciliation
  Given: A set of transactions
  When: Report A and Report B are generated with identical parameters
  Then: Reconciliation formula produces zero difference
```

### Boundary Conditions for Reconciliation Tests

- Zero-amount transactions (should be included in count but not affect totals)
- Maximum-value transactions (verify no overflow in aggregation)
- Negative-amount transactions (verify correct sign handling in SUM)
- Transactions at period boundaries (last second of day, first second of day)
- Mixed-currency transactions (verify aggregation respects currency isolation)
- Empty result sets (verify reports show zero, not null or error)

### Reconciliation Monitoring in Production

For critical aggregation points, implement ongoing reconciliation monitoring:

1. **Scheduled reconciliation job**: Runs daily/hourly, compares grand total to SUM(subtotals) to SUM(details)
2. **Alerting threshold**: Any discrepancy greater than the defined tolerance triggers an alert
3. **Tolerance definition**: Some systems accept rounding tolerance (e.g., within $0.01 per 1000 records); document the tolerance and its rationale
4. **Investigation runbook**: Document the steps to diagnose and resolve reconciliation discrepancies
