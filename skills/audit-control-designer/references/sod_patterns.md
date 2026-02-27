# Segregation of Duties (SoD) Patterns

This document defines the five primary SoD pairs that should be evaluated in any control design, along with risk ratings, recommended separation methods, and compensating controls for small organizations.

---

## Overview

Segregation of Duties (SoD) is a foundational principle of internal control. It ensures that no single individual can both commit and conceal errors or fraud. The principle requires separating:

- **Authorization** from **Execution**
- **Custody** from **Record-keeping**
- **One phase** of a transaction from **another phase**

---

## SoD Pair 1: Entry and Approval Separation

### Description

The person who enters/creates a transaction should not be the same person who approves it.

### Applicable Processes

| Process | Entry Role | Approval Role |
|---|---|---|
| Invoice entry → Invoice approval | Clerk / Location staff | Supervisor / Manager |
| Adjustment entry → Adjustment approval | Accounting staff | Accounting manager |
| Price change request → Price change approval | Procurement | Procurement/Accounting manager |

### Risk If Not Separated

- **Fraud risk**: An individual could create fictitious transactions and approve them
- **Error risk**: Self-review does not catch errors effectively

### Risk Level Assessment

| Scenario | Rating |
|---|---|
| Same person enters and approves invoices | **High** |
| Same person enters and approves adjustments | **High** |
| Same person enters and approves price changes | **Medium** |

### Recommended Separation

- Assign entry and approval to different individuals
- System-enforced workflow: entry creates a pending item, different user approves
- Minimum: approval by someone at a higher authority level

### Compensating Controls (Small Organizations)

- Weekly batch review by an independent reviewer (owner, external accountant)
- Dual signature requirement on all entries above a threshold
- Periodic rotation of entry and approval roles
- External audit sampling of self-approved entries

---

## SoD Pair 2: Ordering and Receiving Separation

### Description

The person who places a purchase order should not be the same person who confirms receipt of goods.

### Applicable Processes

| Process | Ordering Role | Receiving Role |
|---|---|---|
| Purchase order → Goods receipt | Procurement | Warehouse / Location staff |
| Special order → Delivery confirmation | Manager | Receiving clerk |

### Risk If Not Separated

- **Fraud risk**: An individual could order goods to a personal address and confirm receipt
- **Collusion risk**: Easier to arrange kickback schemes with vendors

### Risk Level Assessment

| Scenario | Rating |
|---|---|
| Same person orders and receives goods | **High** |
| Ordering and receiving are in same small team | **Medium** |
| Organizational separation but no system enforcement | **Low** |

### Recommended Separation

- Procurement function handles ordering; location/warehouse staff handle receiving
- Three-way match (PO, delivery receipt, invoice) by a third party (accounting)
- System-enforced: receiving confirmation requires a user who is not the PO creator

### Compensating Controls (Small Organizations)

- Manager reviews all receiving reports against POs weekly
- Vendor confirmation of delivery (signed delivery receipts)
- Periodic surprise checks of received goods vs. PO quantities
- Require photos of delivered goods for high-value items

---

## SoD Pair 3: Recording and Custody Separation

### Description

The person who records transactions should not have physical custody of the related assets.

### Applicable Processes

| Process | Recording Role | Custody Role |
|---|---|---|
| Cash recording → Cash handling | Accounting | Cashier / Store staff |
| Inventory ledger → Physical stock | Accounting | Warehouse / Location staff |
| Asset register → Physical assets | Accounting | Operations |

### Risk If Not Separated

- **Theft risk**: An individual could steal assets and alter records to conceal the theft
- **Manipulation risk**: Inventory counts could be inflated to hide shrinkage

### Risk Level Assessment

| Scenario | Rating |
|---|---|
| Same person handles cash and records transactions | **High** |
| Same person manages inventory and records adjustments | **High** |
| Partial separation with shared access | **Medium** |

### Recommended Separation

- Accounting records transactions; operations handles physical assets
- Access controls: accounting cannot modify inventory counts; warehouse cannot modify financial records
- Independent reconciliation by a third party

### Compensating Controls (Small Organizations)

- Daily cash reconciliation with independent verification
- Surprise cash/inventory counts by owner or manager
- CCTV in storage and cash-handling areas
- Mandatory vacation policy (forces handover)

---

## SoD Pair 4: Counting and Booking Separation

### Description

The person who performs physical counts (inventory, cash) should not be the same person who posts the results to the books.

### Applicable Processes

| Process | Counting Role | Booking Role |
|---|---|---|
| Inventory stocktake → Adjustment posting | Count team | Accounting |
| Cash count → Cash journal entry | Cashier / Manager | Accounting |
| Cycle count → Variance adjustment | Location staff | Accounting |

### Risk If Not Separated

- **Concealment risk**: An individual could manipulate counts to match book values, hiding shrinkage or errors
- **Self-correction risk**: Counts adjusted to eliminate variances rather than investigating root causes

### Risk Level Assessment

| Scenario | Rating |
|---|---|
| Same person counts inventory and posts adjustments | **High** |
| Counter posts preliminary results, accounting verifies | **Medium** |
| Counter submits count, separate team processes adjustments | **Low** |

### Recommended Separation

- Count teams submit signed count sheets to accounting
- Accounting compares count results against book values and processes adjustments
- Count team members do not have access to book quantities before counting (blind count)
- Require dual approval for adjustments above materiality threshold

### Compensating Controls (Small Organizations)

- Dual-person count teams (counter + recorder)
- Manager observes counting and signs off on count sheets
- Accounting reviews all adjustments with supporting documentation
- External auditor involvement in period-end stocktakes

---

## SoD Pair 5: Calculation and Verification Separation

### Description

The person who performs a calculation should not be the same person who verifies/approves the result.

### Applicable Processes

| Process | Calculation Role | Verification Role |
|---|---|---|
| COGS calculation → COGS approval | Accounting staff | Accounting manager |
| Tax calculation → Tax review | Tax preparer | Tax reviewer |
| Reconciliation → Reconciliation sign-off | Preparer | Reviewer |

### Risk If Not Separated

- **Error propagation**: Calculation errors are not caught through self-review
- **Manipulation risk**: Results could be adjusted without independent verification
- **Reproducibility risk**: Without independent verification, calculation errors may persist across periods

### Risk Level Assessment

| Scenario | Rating |
|---|---|
| Same person calculates and approves COGS | **Medium** |
| Same person calculates and reports without any review | **High** |
| Calculator and approver are different but in same small team | **Low** |

### Recommended Separation

- Calculator prepares the result; a different person reviews inputs, formulas, and outputs
- Reviewer should have sufficient knowledge to identify errors
- For critical calculations (COGS, tax): require formal sign-off by a senior person
- Maintain both the calculation file and the review record

### Compensating Controls (Small Organizations)

- Template-based calculations with locked formulas (reduce calculation discretion)
- Trend analysis: compare current period result with prior periods and investigate significant variances
- Quarterly external review of calculations
- Automated reasonableness checks (e.g., COGS as % of revenue within expected range)

---

## SoD Assessment Template

Use this template to assess SoD compliance in a control design:

| # | SoD Pair | Current Assignment | Separation Status | Risk Level | Compensating Controls | Action Required |
|---|---|---|---|---|---|---|
| 1 | Entry / Approval | | Separated / Not Separated | H/M/L | | |
| 2 | Ordering / Receiving | | Separated / Not Separated | H/M/L | | |
| 3 | Recording / Custody | | Separated / Not Separated | H/M/L | | |
| 4 | Counting / Booking | | Separated / Not Separated | H/M/L | | |
| 5 | Calculation / Verification | | Separated / Not Separated | H/M/L | | |

### Assessment Guidelines

1. **Identify current roles** for each duty pair based on the process inventory
2. **Determine if duties are separated** (different individuals, different departments)
3. **Rate the risk level** based on the scenarios described above
4. **Specify compensating controls** for any pair that is not fully separated
5. **Document action items** for improving separation where feasible

### Special Considerations for Small Organizations

In organizations with fewer than 50 employees, complete SoD may not be feasible. In such cases:

1. Focus on the highest-risk pairs first (Pairs 1 and 3)
2. Implement compensating controls from the lists above
3. Document the SoD limitation and compensating controls explicitly
4. Plan for system-enforced SoD as the organization grows
5. Ensure external audit is aware of SoD limitations
