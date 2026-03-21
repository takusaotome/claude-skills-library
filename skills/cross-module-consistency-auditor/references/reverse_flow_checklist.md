# Reverse Flow Checklist

## Purpose

This reference provides a systematic checklist for verifying that reverse flows (refund, void, delete, cancellation, correction, undo) are implemented consistently and symmetrically with their corresponding forward flows. Reverse flow defects are among the most common cross-module consistency issues because reverse flows are often implemented later, by different developers, and with less testing attention than forward flows.

## Forward/Reverse Flow Pairs

### Create / Delete

The most fundamental forward/reverse pair. When an entity is created, there should be a defined process to delete (or soft-delete) it.

**Symmetry Requirements:**

| Aspect | Create (Forward) | Delete (Reverse) | Verification |
|--------|-------------------|-------------------|--------------|
| Primary record | INSERT into main table | DELETE or SET status='deleted' | Record no longer appears in active queries |
| Child records | INSERT related records | DELETE or CASCADE related records | No orphaned child records remain |
| Audit trail | Audit log entry created | Audit log entry for deletion created | Both events are traceable |
| Aggregation | Included in totals | Excluded from totals | Totals decrease by the deleted amount |
| Search index | Added to search index | Removed from search index | Deleted entity not returned in search |
| Cache | Cache populated | Cache invalidated | Stale data not served after deletion |
| External sync | Sync event sent (created) | Sync event sent (deleted) | External system reflects deletion |
| Notifications | Creation notification sent | Cancellation notification sent (if applicable) | Stakeholders informed |
| File/attachment | Files uploaded and linked | Files marked for cleanup or archived | No orphaned files |
| Permission | Access granted to new entity | Access revoked or entity removed from ACL | No unauthorized access to deleted entity |

### Update / Revert

When an entity is updated, there should be a mechanism to revert to the previous state (either explicitly or via correction entry).

**Symmetry Requirements:**

| Aspect | Update (Forward) | Revert (Reverse) | Verification |
|--------|-------------------|-------------------|--------------|
| Field values | New values written | Previous values restored | Entity matches pre-update state |
| Version/history | New version created | Revert version created (not deletion of update) | Full history preserved |
| Dependent calculations | Recalculated with new values | Recalculated with reverted values | All derived values consistent |
| Downstream notifications | "Updated" event published | "Reverted" event published | Downstream systems reflect revert |
| Validation | New values pass validation | Reverted values pass current validation rules | No validation errors on revert |

### Entry / Refund

Financial entries and their refunds must be perfectly symmetric in terms of amounts, components, and accounting treatment.

**Symmetry Requirements:**

| Aspect | Entry (Forward) | Refund (Reverse) | Verification |
|--------|-----------------|-------------------|--------------|
| Base amount | +$100.00 | -$100.00 | Net = $0.00 |
| Tax amount | +$8.00 (calculated at entry rate) | -$8.00 (same rate, not recalculated) | Net tax = $0.00 |
| Discount | -$5.00 | +$5.00 (discount reversed) | Net discount = $0.00 |
| Surcharge/fee | +$2.00 | -$2.00 | Net fee = $0.00 |
| Rounding adjustment | +$0.02 | -$0.02 | Net rounding = $0.00 |
| Payment method | Cash/card captured | Cash/card refunded | Same payment method |
| GL posting | Debit revenue, credit receivable | Credit revenue, debit receivable | Journal entries balance |
| Inventory | Stock decremented | Stock incremented | Inventory restored |
| Loyalty points | Points earned | Points deducted | Points balance restored |
| Commission | Commission accrued | Commission reversed | Net commission = $0.00 |

### Entry / Void

Voids are typically same-day cancellations before settlement, whereas refunds occur after settlement.

**Symmetry Requirements (in addition to Entry/Refund above):**

| Aspect | Entry (Forward) | Void (Reverse) | Key Difference from Refund |
|--------|-----------------|-----------------|---------------------------|
| Timing | Any time | Before settlement/batch close | Time-bounded operation |
| Settlement impact | Included in batch | Excluded from batch | No money movement occurs |
| Receipt | Original receipt | Void receipt (may reference original) | Different receipt format |
| Reporting | Appears in transaction log | Appears as voided | May be excluded from revenue reports |
| Authorization | Payment authorized | Authorization reversed (not refunded) | Different payment processor call |

### Entry / Suspend (Hold)

Suspend operations temporarily remove an entry from active processing without deleting or refunding it.

**Symmetry Requirements:**

| Aspect | Entry (Forward) | Suspend (Reverse) | Resume (Re-forward) |
|--------|-----------------|---------------------|----------------------|
| Status | Active | Suspended | Active (restored) |
| Aggregation | Included in totals | Excluded from totals | Re-included in totals |
| Processing | Eligible for batch jobs | Skipped by batch jobs | Re-eligible for batch jobs |
| Visibility | Visible to all authorized users | Visible with "suspended" indicator | Visible as active again |
| Time tracking | Active duration counting | Duration paused | Duration resumed |

## Positive/Negative Symmetry Verification

### The Symmetry Test

For every forward/reverse pair, execute the following test:

```
1. Create a forward entry with known values
2. Execute the reverse operation on that entry
3. Verify net result:
   - For full reversal: all component nets should be zero
   - For partial reversal: net should equal the unreversed portion
4. Verify aggregation impact:
   - Totals that included the forward entry should reflect the reversal
5. Verify audit trail:
   - Both forward and reverse operations are logged
   - The reverse operation references the forward operation
```

### Component-by-Component Verification

Do not verify only the total. Verify each component independently:

```
For each component C in {base, tax, discount, surcharge, rounding, fee, ...}:
  forward_C + reverse_C == expected_net_C

Then verify:
  SUM(forward_components) + SUM(reverse_components) == expected_net_total
```

This catches defects where the total happens to be correct due to offsetting errors in individual components.

### Sign Convention Verification

Verify that the sign convention is consistent:

| Convention | Forward | Reverse | Common In |
|-----------|---------|---------|-----------|
| Positive/Negative | +amount | -amount | Accounting systems, GL |
| Absolute + Flag | amount, type=SALE | amount, type=REFUND | POS systems, some APIs |
| Separate columns | debit=amount | credit=amount | Double-entry accounting |

Whichever convention is used, it must be consistent across:
- Database storage
- API responses
- Report display
- Aggregation queries
- Export files

A common defect is that the database uses positive/negative but the API returns absolute values with a type flag, and the aggregation query sums the database column (getting the sign right) while the report sums the API response (ignoring the sign).

## Comprehensive Reverse Flow Checklist

Use this checklist for every forward/reverse flow pair:

### Data Integrity
- [ ] Every component of the forward entry has a corresponding reverse component
- [ ] Reverse amounts are exact negatives of forward amounts (not recalculated)
- [ ] Tax on reversal uses the original rate, not the current rate
- [ ] Rounding adjustments are reversed, not recalculated
- [ ] No orphaned child records after reversal
- [ ] Foreign key relationships remain valid after reversal

### Aggregation Impact
- [ ] All aggregation queries that include the forward entry also process the reversal correctly
- [ ] Net of forward + reverse produces the expected result in every aggregation
- [ ] Report totals reflect the reversal
- [ ] Drill-down shows both forward and reverse entries
- [ ] Cross-report reconciliation still holds after reversal

### State Management
- [ ] Status transition from active to reversed is defined and enforced
- [ ] Reversed entries cannot be reversed again (or double-reversal is handled)
- [ ] Reversed entries cannot be edited
- [ ] Status is consistent across all views (UI, API, reports, exports)

### Audit and Traceability
- [ ] Reverse operation is logged in the audit trail
- [ ] Reverse entry references the original forward entry (by ID or link)
- [ ] Timestamp of reversal is recorded
- [ ] User/system that initiated the reversal is recorded
- [ ] Reason for reversal is captured (if applicable)

### External System Impact
- [ ] Sync events for the reversal are sent to all integrated external systems
- [ ] External systems process the reversal correctly
- [ ] Payment gateway reversal (void or refund) is initiated
- [ ] Inventory system is notified to restock (for physical goods)
- [ ] Loyalty/rewards system is notified to adjust points

### Permission and Authorization
- [ ] Reverse operation requires appropriate authorization (may be higher than forward operation)
- [ ] Authorization requirements are documented
- [ ] Unauthorized reversal attempts produce appropriate error responses
- [ ] Authorization is checked at the same points as forward operation authorization

## Anti-Patterns to Watch For

### 1. "Just Negate the Total"
Reversing only the total amount without reversing individual components. This causes component-level aggregation to be incorrect even though the total appears correct.

### 2. "Recalculate on Reversal"
Recalculating tax, rounding, or fees on the reversal amount instead of reversing the original calculated values. This introduces discrepancies when rates or rules have changed between the original entry and the reversal.

### 3. "Delete Instead of Reverse"
Physically deleting the forward entry instead of creating a reverse entry. This destroys audit trail, creates gaps in sequences, and makes reconciliation impossible.

### 4. "Reverse Flow as Afterthought"
Implementing the reverse flow months after the forward flow, by a different developer, without referencing the forward flow's implementation. This almost always produces symmetry violations.

### 5. "Test Forward Only"
Testing the forward flow thoroughly but only smoke-testing the reverse flow (or not testing it at all). Reverse flows should receive equal testing rigor.
