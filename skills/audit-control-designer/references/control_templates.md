# Layer 2: Control Templates

This document defines 8 generalized control pattern templates derived from real audit engagements. Each template is customizable by industry, scale, and system environment.

---

## Template T-AP-01: Invoice Entry Completeness Check

| Field | Value |
|---|---|
| **Pattern ID** | T-AP-01 |
| **Business Pattern** | AP (Accounts Payable) |
| **Control Type** | Detective |
| **Objective** | Verify that all received invoices are entered into the system/ledger without omission |
| **Target Assertion** | Completeness |

### Procedure

1. Maintain a daily invoice receipt log (paper or electronic) recording all invoices received
2. At end of each day/period, compare the receipt log against actual entries in the ledger/system
3. Identify any unmatched items (received but not entered)
4. Investigate and resolve unmatched items within the same business day
5. Record resolution details on the reconciliation checklist

### Roles and Frequency

| Role | Responsibility | Frequency |
|---|---|---|
| Entry clerk / Location staff | Enter invoices and maintain receipt log | Daily |
| Supervisor / Location manager | Verify reconciliation of receipt log vs. entries | Daily |

### Evidence

- Invoice receipt log (date, vendor, invoice number, amount)
- Reconciliation checklist (matched, unmatched, resolution)

### Remediation

- Unmatched invoices must be entered within the same business day
- Record the remediation action and timestamp
- Escalate to supervisor if entry cannot be completed same-day

### Customization by Industry

| Industry | Adjustment |
|---|---|
| **F&B** | High volume (daily deliveries per location) — consider batch reconciliation at day-end |
| **Retail** | EDI invoices may auto-enter — focus receipt log on non-EDI vendors |
| **Manufacturing** | Partial deliveries require tracking receipt vs. PO line items |

### Customization by Scale

| Scale | Adjustment |
|---|---|
| **Small** | Single person may handle both entry and verification — add weekly supervisor review as compensating control |
| **Medium** | Separate entry and verification roles |
| **Large** | System-enforced workflow with automatic receipt log from scanning/OCR |

---

## Template T-AP-02: Invoice Matching and Variance Resolution

| Field | Value |
|---|---|
| **Pattern ID** | T-AP-02 |
| **Business Pattern** | AP (Accounts Payable) |
| **Control Type** | Detective |
| **Objective** | Verify accuracy and completeness of invoiced amounts through N-way matching, and properly accrue unmatched deliveries |
| **Target Assertions** | Completeness, Accuracy |

### Procedure

1. For each invoice, perform matching against available documents:
   - 2-way match: Invoice vs. Purchase Order
   - 3-way match: Invoice vs. Purchase Order vs. Delivery Receipt
   - The matching method should be determined based on control effectiveness requirements
2. Record all variances with: invoice number, variance amount, variance type, investigation status
3. Resolve variances within defined SLA (e.g., same day for amount variances, 3 business days for quantity variances)
4. At period end, identify all delivered-but-not-invoiced items
5. Accrue GRNI (Goods Received Not Invoiced) based on delivery records for unmatched deliveries
6. Document the GRNI estimate basis and amount

### Roles and Frequency

| Role | Responsibility | Frequency |
|---|---|---|
| Accounting staff | Perform matching and record variances | Daily |
| Accounting manager | Review open variances and approve GRNI accruals | Weekly/Monthly |

### Evidence

- Matching log (invoice number, PO number, delivery receipt, variance amount, status)
- GRNI accrual schedule with estimate basis

### Remediation

- Unresolved variances at period-end: flag as open items with estimated impact
- If unmatched deliveries exceed materiality threshold: accounting manager escalation required
- **Provisional rule**: If GRNI policy is pending formal confirmation, apply accrual approach as interim treatment

### Customization by Industry

| Industry | Adjustment |
|---|---|
| **F&B** | Template inconsistency across locations increases matching effort — standardize templates first |
| **Retail** | EDI matching may be automated — focus on exception handling |
| **Manufacturing** | Partial delivery matching requires line-item level reconciliation |

---

## Template T-INV-01: Physical Inventory Count (Stocktake)

| Field | Value |
|---|---|
| **Pattern ID** | T-INV-01 |
| **Business Pattern** | Inventory |
| **Control Type** | Preventive |
| **Objective** | Verify physical existence and accuracy of inventory through standardized counting procedures |
| **Target Assertions** | Existence, Accuracy |

### Procedure

1. Distribute standardized count sheets with item descriptions (no pre-printed quantities — blind count)
2. Assign count teams of 2+ persons; counter and recorder must be different people
3. Count all items following the standard procedure document
4. For designated high-value or high-risk items, perform double-count (independent re-count by a different team)
5. Compare physical counts against book quantities
6. Flag variances exceeding threshold for re-count
7. Obtain counter and recorder signatures on count sheets

### Roles and Frequency

| Role | Responsibility | Frequency |
|---|---|---|
| Count team (2+ persons) | Perform physical count | Monthly/Quarterly |
| Supervisor / Manager | Oversee count, verify double-count items, sign off | Monthly/Quarterly |
| Accounting | Receive count results and process variances | Monthly/Quarterly |

### Evidence

- Signed count sheets (counter + recorder signatures)
- Double-count records for designated items
- Variance report (item, book qty, counted qty, variance, re-count result)

### Remediation

- Items with variance exceeding threshold: mandatory re-count
- If total variance (all items, dollar-weighted) exceeds materiality threshold: escalate to accounting manager
- Document re-count results and final accepted quantities

### Customization by Industry

| Industry | Adjustment |
|---|---|
| **F&B** | Include semi-finished/WIP items, perishable items require weight-based counting |
| **Retail** | SKU-level counting, barcode scanning recommended for high SKU counts |
| **Manufacturing** | WIP counting requires stage-of-completion assessment, raw materials vs. finished goods separation |

---

## Template T-INV-02: Inventory Adjustment Approval

| Field | Value |
|---|---|
| **Pattern ID** | T-INV-02 |
| **Business Pattern** | Inventory |
| **Control Type** | Detective |
| **Objective** | Ensure inventory adjustment entries are properly justified, approved, and recorded |
| **Target Assertions** | Existence, Valuation |

### Procedure

1. For each adjustment entry, require: adjustment reason, supporting evidence, amount
2. Adjustments below threshold: single approval by location manager
3. Adjustments at or above threshold: dual approval by location manager AND accounting manager
4. Record all adjustment entries with: date, item, quantity, value, reason, approver(s)
5. Monthly summary of adjustments reviewed by accounting manager for patterns

### Roles and Frequency

| Role | Responsibility | Frequency |
|---|---|---|
| Location staff | Prepare adjustment entry with reason | As needed |
| Location manager | First-level approval | As needed |
| Accounting manager | Second-level approval for material amounts; monthly review | Monthly |

### Evidence

- Approved adjustment vouchers (reason + signature(s))
- Monthly adjustment summary report

### Remediation

- Unapproved adjustments: exclude from COGS calculation until approved
- Pattern of recurring adjustments in same category: investigate root cause

---

## Template T-CO-01: Returns/Credits Cut-off Verification

| Field | Value |
|---|---|
| **Pattern ID** | T-CO-01 |
| **Business Pattern** | Returns/Credits |
| **Control Type** | Detective |
| **Objective** | Verify that returns and credits near period-end are attributed to the correct accounting period |
| **Target Assertions** | Cut-off, Completeness |

### Procedure

1. Define the accounting base date for returns (recommended: shipment date from the company's location)
2. At period end, extract all return transactions within ±5 business days of the period boundary
3. For each transaction, verify: return date, vendor receipt date, credit note date, and accounting base date
4. Determine correct period attribution based on the defined base date
5. Identify and correct any mis-attributed transactions
6. Accounting manager approves the cut-off verification list

### Roles and Frequency

| Role | Responsibility | Frequency |
|---|---|---|
| Accounting staff | Extract and verify cut-off transactions | Monthly (daily near period-end) |
| Accounting manager | Approve cut-off verification list | Monthly |

### Evidence

- Cut-off verification list (transaction date, base date, attributed month, verifier, result)
- Exception approval records for ambiguous cases

### Remediation

- Transactions attributed to wrong period: post correcting entry
- If base date is not yet defined (TBD): use individual case-by-case judgment with accounting manager approval and full documentation

### Open Question

The accounting base date must be formally defined. Options:
- A) Shipment date from company location (recommended — closest to risk transfer)
- B) Vendor receipt date
- C) Credit note issuance date

Until formally decided, apply option A provisionally with explicit documentation.

---

## Template T-VAL-01: Price Revision Change Control

| Field | Value |
|---|---|
| **Pattern ID** | T-VAL-01 |
| **Business Pattern** | Price Management |
| **Control Type** | Preventive |
| **Objective** | Ensure unit cost changes are approved, timely reflected, and fully documented |
| **Target Assertion** | Valuation |

### Procedure

1. Upon receiving a price revision notice: log the notice with date, vendor, affected items, old price, new price, effective date
2. Submit change request for approval within 2 business days of receipt
3. Approver reviews: vendor notification, effective date, impact analysis
4. After approval: update price master within 5 business days of receipt
5. Record: change date, changed-by, old value, new value, approval reference
6. Verify that subsequent transactions use the updated price

### Roles and Frequency

| Role | Responsibility | Frequency |
|---|---|---|
| Procurement | Receive notice, log, submit for approval | As needed |
| Procurement/Accounting manager | Approve price change | As needed |
| Accounting | Verify transaction prices post-change | Monthly |

### Evidence

- Price revision notice (vendor document)
- Price master change log (before/after/date/approver)
- Approval record

### Remediation

- Late updates (beyond 5 business days): escalate to accounting manager
- If transactions occurred at old price after effective date: calculate and post adjustment

---

## Template T-CALC-01: Cost Calculation Template Management

| Field | Value |
|---|---|
| **Pattern ID** | T-CALC-01 |
| **Business Pattern** | COGS Calculation |
| **Control Type** | Preventive |
| **Objective** | Ensure cost calculations are reproducible by separating input data from formulas and maintaining version control |
| **Target Assertion** | Accuracy |

### Procedure

1. Maintain a standardized calculation template with:
   - Input cells clearly designated (data entry area)
   - Formula cells locked/protected (calculation area)
   - Output cells clearly designated (result area)
2. Before each period-end calculation:
   - Save a copy of the previous period template as an archive
   - Use a clean copy of the current template for the new period
3. Apply naming convention: `[Process]_[YYYY-MM]_v[NN]` (e.g., `COGS_2026-01_v01`)
4. After calculation: save with version number and lock the file
5. Any subsequent changes create a new version (never overwrite)

### Roles and Frequency

| Role | Responsibility | Frequency |
|---|---|---|
| Accounting staff | Perform calculation using template | Monthly |
| Accounting manager | Verify template integrity (formulas unchanged) | Quarterly |

### Evidence

- Versioned calculation files with timestamps
- Template integrity check record (quarterly)

### Remediation

- If template formulas are found to be modified: investigate, correct, and re-run calculation
- Document any formula changes with justification

---

## Template T-CALC-02: Re-Calculation Change Management

| Field | Value |
|---|---|
| **Pattern ID** | T-CALC-02 |
| **Business Pattern** | COGS Calculation |
| **Control Type** | Detective |
| **Objective** | Ensure all re-calculations are justified, documented, and approved before results are used in reporting |
| **Target Assertion** | Accuracy |

### Procedure

1. When a re-calculation is required:
   - Document the reason (e.g., late invoice, count correction, price adjustment)
   - Identify the specific inputs or parameters that changed
   - Record the before and after values of the affected output
2. Submit change request with:
   - Change reason document
   - Before/after comparison
   - Impact assessment (materiality)
3. Accounting manager reviews and approves before the re-calculated result replaces the original
4. Retain both original and re-calculated versions

### Roles and Frequency

| Role | Responsibility | Frequency |
|---|---|---|
| Accounting staff | Prepare change request with documentation | As needed |
| Accounting manager | Review and approve re-calculation | As needed |

### Evidence

- Change reason document (before/after values, reason, impact)
- Approval record (approver signature/timestamp)
- Both original and re-calculated files retained

### Remediation

- Unapproved re-calculations: do not use in reporting
- Recurring re-calculations: investigate root cause and address upstream (e.g., late invoice submission)
