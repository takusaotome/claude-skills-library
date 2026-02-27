# Assertion Mapping Rules

This document defines the five primary audit assertions and provides mapping rules for connecting assertions to business process patterns and control templates.

---

## The Five Audit Assertions

### Completeness (C)

**Definition**: All transactions and events that should have been recorded have been recorded.

**In practice**: No invoices, deliveries, returns, or adjustments are missing from the books.

| Process Pattern | How Completeness Risk Manifests |
|---|---|
| AP | Invoices received but not entered; deliveries without matching invoice |
| Inventory | Goods received but not recorded in inventory ledger |
| COGS Calculation | Input data incomplete at time of calculation |
| Returns/Credits | Credit notes not received or not posted |
| Price Management | (Indirect) Price changes not reflected may cause completeness issues in accruals |

**Primary Control Templates**: T-AP-01 (receipt log reconciliation), T-AP-02 (matching + GRNI), T-CO-01 (returns completeness)

**Key KPIs**: Invoice variance rate (K03), Exception incidence rate (K06)

---

### Accuracy (A)

**Definition**: Amounts and other data relating to recorded transactions and events have been recorded correctly.

**In practice**: The numbers in the books match the underlying evidence — quantities are right, amounts are calculated correctly.

| Process Pattern | How Accuracy Risk Manifests |
|---|---|
| AP | Transcription errors in manual invoice entry; wrong amounts posted |
| Inventory | Count errors during stocktake; unit of measure mismatches |
| COGS Calculation | Formula errors, wrong inputs, calculation mistakes |
| Returns/Credits | Wrong credit amount recorded |
| Price Management | Old price used for transactions after price revision |

**Primary Control Templates**: T-AP-02 (matching), T-INV-01 (double count), T-CALC-01 (template management), T-CALC-02 (re-calculation change management)

**Key KPIs**: Transcription error rate (K01), Stocktake variance rate (K02), Re-calculation rate (K05)

---

### Valuation (V)

**Definition**: Assets, liabilities, and equity interests are valued at appropriate amounts, and any resulting valuation adjustments are properly recorded.

**In practice**: Inventory is valued using the correct method (FIFO, weighted average), at the appropriate amount (lower-of-cost-or-NRV), and unit costs are current.

| Process Pattern | How Valuation Risk Manifests |
|---|---|
| AP | (Indirect) Wrong unit prices in invoices affect cost basis |
| Inventory | Obsolete/expired items not written down; wrong valuation method applied |
| COGS Calculation | Cost method inconsistency; valuation not aligned with accounting policy |
| Returns/Credits | (Indirect) Returned items may need revaluation |
| Price Management | Stale prices used for inventory valuation and COGS |

**Primary Control Templates**: T-VAL-01 (price revision change control), T-INV-02 (adjustment approval for write-downs)

**Key KPIs**: (Custom) Price update timeliness, Inventory write-down ratio

---

### Cut-off (CO)

**Definition**: Transactions and events have been recorded in the correct accounting period.

**In practice**: A delivery on January 31 is recorded in January, not February. A return on the last business day of the month goes to the correct period.

| Process Pattern | How Cut-off Risk Manifests |
|---|---|
| AP | Invoices for December deliveries posted in January |
| Inventory | End-of-month transfers or receipts straddling the period boundary |
| COGS Calculation | Late adjustments affecting which period COGS belongs to |
| Returns/Credits | Returns near period-end attributed to wrong month |
| Price Management | Price effective date vs. actual application date mismatch |

**Primary Control Templates**: T-CO-01 (returns cut-off verification)

**Key KPIs**: Period attribution error rate (K08)

**Note**: Cut-off is one of the most commonly tested assertions in financial audits. Period-end transactions within ±5 business days of the boundary typically receive heightened scrutiny.

---

### Existence (E)

**Definition**: Assets and liabilities exist at a given date, and recorded transactions and events actually occurred.

**In practice**: The inventory shown on the books physically exists in the warehouse. The vendor invoice relates to a real delivery.

| Process Pattern | How Existence Risk Manifests |
|---|---|
| AP | Fictitious invoices; invoices for goods never received |
| Inventory | Phantom stock (recorded but not physically present); shrinkage |
| COGS Calculation | (Indirect) COGS based on non-existent inventory is misstated |
| Returns/Credits | (Indirect) Returns claimed but goods not actually returned |
| Price Management | (Low risk) Prices exist in master but items may be discontinued |

**Primary Control Templates**: T-INV-01 (physical count), T-INV-02 (adjustment approval)

**Key KPIs**: Stocktake variance rate (K02)

---

## Assertion Coverage Matrix Template

Use this matrix to verify that all assertions are covered by at least one control. Fill in control IDs after generating the control design.

| Assertion | Primary Controls | Secondary Controls | Coverage Assessment |
|---|---|---|---|
| Completeness (C) | | | |
| Accuracy (A) | | | |
| Valuation (V) | | | |
| Cut-off (CO) | | | |
| Existence (E) | | | |

### Coverage Assessment Ratings

| Rating | Definition |
|---|---|
| **Strong** | 2+ controls directly address this assertion with clear evidence and remediation |
| **Adequate** | 1 control directly addresses this assertion |
| **Weak** | Only indirect coverage through controls targeting other assertions |
| **Gap** | No control addresses this assertion — requires immediate design |

### Minimum Coverage Requirements

- All five assertions must have at least **Adequate** coverage
- Assertions identified as high-risk in the process analysis must have **Strong** coverage
- Any **Gap** is a material control deficiency that must be addressed

---

## Mapping Process: Step by Step

1. **List all controls** from the control design table
2. **For each control**, identify which assertions it addresses (from the control template's "Target Assertions" field)
3. **Fill in the coverage matrix** with control IDs
4. **Assess coverage level** for each assertion
5. **Identify gaps** and design additional controls as needed
6. **Verify KPI alignment**: Each assertion should have at least one KPI that measures its effectiveness
