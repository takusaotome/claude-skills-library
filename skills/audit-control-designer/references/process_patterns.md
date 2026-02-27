# Layer 1: Business Process Patterns

This document defines generalized business process patterns used to classify As-Is process inventories for control design. Patterns are industry-agnostic where possible, with industry-specific variations noted.

---

## Pattern: AP (Accounts Payable / Procurement)

### Definition

Processes related to purchasing goods or services, receiving invoices, matching documents, and recording payables.

### Typical Business Flow

```
Purchase Order → Goods Receipt → Invoice Receipt → Matching → Payment
```

### Representative Processes

| Process Type | Description | Frequency |
|---|---|---|
| Invoice Entry | Receive and enter invoice data (manual or electronic) | Daily |
| N-Way Matching | Match invoice against PO and/or delivery receipt (2-way or 3-way) | Daily |
| Variance Investigation | Investigate and resolve matching discrepancies | Daily/Weekly |
| GRNI Management | Accrue goods received but not yet invoiced at period end | Monthly |
| Payment Processing | Execute payment based on approved invoices | Weekly/Monthly |

### Primary Audit Assertions

| Assertion | Risk |
|---|---|
| **Completeness** | Invoices not recorded, deliveries without matching invoices |
| **Accuracy** | Transcription errors in manual entry, wrong amounts posted |

### Risk Scenarios

- **Manual Entry Risk**: High-volume manual transcription leads to structural error rates of 1-3%
- **Completeness Risk**: Invoices lost in transit (email/mail), delivery receipts not matched
- **Timing Risk**: Invoice processing delays cause period-end accrual uncertainty

### Industry Variations

| Industry | Variation |
|---|---|
| **F&B** | High frequency (daily deliveries per location), PDF/paper invoices, template inconsistency across locations |
| **Retail** | EDI-based invoicing common, vendor-managed inventory may bypass PO process |
| **Manufacturing** | BOM-based PO generation, partial deliveries common, quality inspection step before receipt |

---

## Pattern: Inventory (Inventory Management)

### Definition

Processes related to counting, tracking, valuing, and adjusting physical inventory, including cycle counts and period-end stocktakes.

### Typical Business Flow

```
Goods Receipt → Storage/FIFO → Cycle Count → Period-End Stocktake → Adjustment → Valuation
```

### Representative Processes

| Process Type | Description | Frequency |
|---|---|---|
| Goods Receipt Recording | Record received goods into inventory ledger | Daily |
| Storage Management | FIFO placement, expiry tracking, location management | Daily |
| Cycle Count | Count selected items on a rotating schedule | Weekly |
| Period-End Stocktake | Full physical inventory count | Monthly/Quarterly |
| Variance Adjustment | Investigate and post adjustments for count vs. book differences | Monthly |
| Valuation | Apply cost method (FIFO, weighted average, etc.) to inventory | Monthly |

### Primary Audit Assertions

| Assertion | Risk |
|---|---|
| **Existence** | Recorded inventory does not physically exist (phantom stock) |
| **Accuracy** | Count errors, wrong units, double-counting |
| **Valuation** | Incorrect cost method, obsolete/expired items not written down |

### Risk Scenarios

- **Count Accuracy**: Manual paper-based counting is error-prone, especially for similar items
- **Valuation Risk**: Semi-finished goods and WIP lack defined valuation methods
- **Shrinkage**: Theft, spoilage, and expired items create unrecorded inventory losses
- **Audit Readiness**: Paper count sheets are difficult to verify and susceptible to manipulation

### Industry Variations

| Industry | Variation |
|---|---|
| **F&B** | Perishable items require expiry tracking, portion-level counting, high shrinkage from waste |
| **Retail** | SKU-level tracking, seasonal obsolescence, high-volume cycle counts |
| **Manufacturing** | WIP valuation, BOM explosion for component tracking, yield-based adjustments |

---

## Pattern: COGS Calculation (Cost of Goods Sold)

### Definition

Processes related to computing the periodic cost of goods sold, including data aggregation, calculation, variance analysis, and re-close procedures.

### Typical Business Flow

```
Input Finalization → COGS Calculation → Variance Analysis → Re-Close (if needed) → Final Report
```

### Representative Processes

| Process Type | Description | Frequency |
|---|---|---|
| Input Finalization | Confirm all inputs (inventory, purchases, returns) are complete | Monthly |
| COGS Computation | Apply formula: Beginning Inventory + Net Purchases - Ending Inventory | Monthly |
| Variance Analysis | Compare actual vs. theoretical COGS, identify drivers | Monthly |
| Re-Close Processing | Recalculate after corrections or late entries | Monthly (1-3 times) |
| Reporting | Prepare final COGS report with supporting schedules | Monthly |

### Primary Audit Assertions

| Assertion | Risk |
|---|---|
| **Accuracy** | Calculation errors, formula mistakes, wrong inputs |
| **Reproducibility** | (Internal control concept) Same inputs produce different results due to manual processes |

### Risk Scenarios

- **Spreadsheet Risk**: Excel-based calculations are person-dependent and lack version control
- **Re-Close Risk**: Uncontrolled re-calculations without change documentation
- **Input Dependency**: COGS accuracy depends on AP completeness and inventory accuracy

### Industry Variations

| Industry | Variation |
|---|---|
| **F&B** | Inventory method (periodic), theoretical vs actual COGS comparison for waste detection |
| **Retail** | Retail inventory method, markdown impact, cost complement calculations |
| **Manufacturing** | Standard costing, variance analysis (price/efficiency/volume), WIP adjustments |

---

## Pattern: Returns/Credits

### Definition

Processes related to handling product returns, vendor credits, and their proper recording in inventory and accounts payable.

### Typical Business Flow

```
Return Initiation → Vendor Communication → Credit Note Receipt → Inventory Adjustment → AP Adjustment → Period Attribution
```

### Representative Processes

| Process Type | Description | Frequency |
|---|---|---|
| Return Processing | Initiate return, notify vendor, ship goods back | As needed |
| Credit Note Tracking | Track receipt and posting of vendor credit notes | As needed |
| Inventory Adjustment | Decrement inventory for returned goods | As needed |
| Period Attribution | Determine correct accounting period for the return | Monthly |
| Cut-off Verification | Verify period-end returns are attributed to the correct month | Monthly |

### Primary Audit Assertions

| Assertion | Risk |
|---|---|
| **Cut-off** | Returns near period-end attributed to wrong month |
| **Completeness** | Credit notes not received or not recorded |

### Risk Scenarios

- **Cut-off Ambiguity**: No defined base date for determining which period a return belongs to
- **Lead Time Risk**: Long processing time between return and credit note creates unrecorded receivables
- **Inventory Mismatch**: Physical goods returned but inventory ledger not updated

### Industry Variations

| Industry | Variation |
|---|---|
| **F&B** | Low volume but high complexity (quality issues, short-dated items), disposal vs. return decisions |
| **Retail** | High volume, customer returns vs. vendor returns distinction, restocking fees |
| **Manufacturing** | Quality-related returns, warranty claims, scrap vs. rework decisions |

---

## Pattern: Price Management

### Definition

Processes related to maintaining and updating unit costs in price masters, ensuring cost accuracy across transactions.

### Typical Business Flow

```
Price Revision Notice → Approval → Master Update → Effective Date Application → Transaction Verification
```

### Representative Processes

| Process Type | Description | Frequency |
|---|---|---|
| Price Revision Receipt | Receive notification of price changes from vendors | As needed |
| Approval Workflow | Review and approve price changes | As needed |
| Master Data Update | Update unit costs in price/cost master | As needed |
| Effective Date Management | Apply new prices from the correct date | As needed |
| Transaction Verification | Verify transactions use the correct unit price | Monthly |

### Primary Audit Assertions

| Assertion | Risk |
|---|---|
| **Valuation** | Incorrect unit prices lead to misstated inventory and COGS |

### Risk Scenarios

- **Timing Gap**: Price revision received but not applied promptly, causing transactions at old prices
- **Cascade Effect**: A single price error affects all transactions for that item
- **Consistency Risk**: Price method (moving average, FIFO) must be consistent with accounting policy

### Industry Variations

| Industry | Variation |
|---|---|
| **F&B** | Frequent commodity price fluctuations, seasonal pricing, contract vs. spot prices |
| **Retail** | Vendor rebates, promotional pricing, markdown management |
| **Manufacturing** | Raw material indices, long-term contracts, transfer pricing for intercompany |

---

## Pattern Classification Guidelines

### How to Classify Processes

1. Read the process description and identify its primary function
2. Match against the patterns above based on:
   - What data the process handles (invoices, inventory, costs, returns, prices)
   - What the process produces (records, reports, adjustments)
   - Who performs it (store, accounting, procurement)
3. A single process may map to multiple patterns (e.g., "invoice reconciliation" = AP + Inventory if it includes delivery receipt matching)
4. Assign a primary pattern and optional secondary patterns

### Processes That Don't Fit Standard Patterns

Some processes may not fit the five standard patterns. Common additional patterns:

| Pattern | Domain | Examples |
|---|---|---|
| Cash Management | POS reconciliation, cash variance | Store cash counts, bank deposit reconciliation |
| Revenue Recognition | Sales recording, deferred revenue | POS integration, subscription billing |
| Compliance | Tax, regulatory reporting | Qualified invoice compliance, food safety records |
| Master Data | Reference data management | Recipe masters, supplier masters, item masters |

These patterns do not have pre-built control templates but can be designed using the general control design principles from the template library.
