# Risk Control Matrix (RCM) Template

## Document Information

| Item | Content |
|------|---------|
| Document Number | RCM-[Process Name]-[YYYY]-[Sequential#] |
| Process | [Process Name] |
| Prepared By | [Name] |
| Prepared Date | [YYYY-MM-DD] |
| Reviewed By | [Name] |
| Approved Date | [YYYY-MM-DD] |
| Version | [X.X] |

---

## 1. Process Overview

### 1.1 Process Information

| Item | Content |
|------|---------|
| Process Name | [e.g., Revenue Recognition Process] |
| Process Owner | [Department / Name] |
| Related Accounts | [e.g., Revenue, Accounts Receivable, Deferred Revenue] |
| Related Systems | [e.g., Sales System, ERP, Billing System] |
| Transaction Volume (Annual) | [Count] |
| Dollar Volume (Annual) | [Amount] |

### 1.2 Process Flow Summary

```
[Start] → [Order Entry] → [Shipment] → [Invoicing] → [Cash Receipt] → [Application] → [End]
```

### 1.3 Relevant Assertions

| Assertion | Code | Description | Applicable |
|-----------|------|-------------|:----------:|
| Existence | E | Recorded transactions/balances actually exist | ☐ |
| Completeness | C | All transactions/balances are recorded | ☐ |
| Rights & Obligations | R/O | Assets are rights; liabilities are obligations | ☐ |
| Valuation & Allocation | V | Recorded at appropriate amounts | ☐ |
| Presentation & Disclosure | P/D | Properly classified and disclosed | ☐ |
| Occurrence | O | Recorded transactions actually occurred | ☐ |
| Accuracy | A | Transactions recorded at correct amounts | ☐ |
| Cutoff | CO | Transactions recorded in correct period | ☐ |

---

## 2. Risk Control Matrix

### 2.1 RCM Summary

| Risk Count | Control Count | Key Controls |
|------------|---------------|--------------|
| [Count] | [Count] | [Count] |

### 2.2 Detailed RCM

#### Process: [Process Name]

| Risk ID | Risk Description | Assertion | Control ID | Control Description | Type | Freq | Owner | Key | Test Procedure | Sample |
|---------|------------------|:---------:|------------|---------------------|:----:|:----:|-------|:---:|----------------|:------:|
| R-001 | [Specific risk description] | E/C/V/O/A | C-001 | [Detailed control activity] | P/D | D/W/M/Q/A | [Title] | ☐ | [Test method] | [n] |
| R-002 | | | C-002 | | | | | ☐ | | |
| R-003 | | | C-003 | | | | | ☐ | | |

**Legend:**
- Type: P = Preventive, D = Detective
- Freq: D = Daily, W = Weekly, M = Monthly, Q = Quarterly, A = Annual
- Assertions: E = Existence, C = Completeness, V = Valuation, O = Occurrence, A = Accuracy, CO = Cutoff, R/O = Rights & Obligations, P/D = Presentation & Disclosure

---

## 3. Process-Specific RCM Details

### 3.1 Order Entry Process

| Risk ID | Risk Description | Assertion | Control ID | Control Description | Type | Freq | Owner | Key |
|---------|------------------|:---------:|------------|---------------------|:----:|:----:|-------|:---:|
| R-ORD-001 | Fictitious orders are entered | O | C-ORD-001 | Order entry requires customer PO and sales manager approval | P | Per Trans | Sales Rep | ☐ |
| R-ORD-002 | Order terms changed without approval | A | C-ORD-002 | Price/term changes require supervisor approval | P | Per Trans | Sales Mgr | ☐ |
| R-ORD-003 | Orders exceed credit limits | V | C-ORD-003 | System alerts on credit limit breach; Credit dept approval required | P | Per Trans | Credit Dept | ☐ |

### 3.2 Shipping Process

| Risk ID | Risk Description | Assertion | Control ID | Control Description | Type | Freq | Owner | Key |
|---------|------------------|:---------:|------------|---------------------|:----:|:----:|-------|:---:|
| R-SHP-001 | Unauthorized shipments occur | O | C-SHP-001 | Shipping requires approved sales order | P | Per Trans | Warehouse | ☐ |
| R-SHP-002 | Shipped quantity differs from ordered | A | C-SHP-002 | System validates shipped qty against order qty | P | Per Trans | Warehouse | ☐ |
| R-SHP-003 | Shipments not recorded timely | CO | C-SHP-003 | Shipment data auto-syncs to sales system | P | Per Trans | System | ☐ |

### 3.3 Revenue Recognition Process

| Risk ID | Risk Description | Assertion | Control ID | Control Description | Type | Freq | Owner | Key |
|---------|------------------|:---------:|------------|---------------------|:----:|:----:|-------|:---:|
| R-REV-001 | Revenue is recorded twice | O | C-REV-001 | Daily reconciliation of shipping and revenue data | D | Daily | Accounting | ☐ |
| R-REV-002 | Revenue recorded in wrong period | CO | C-REV-002 | Monthly cutoff review of ship date vs. recognition date | D | Monthly | Controller | ☐ |
| R-REV-003 | Revenue recorded at wrong amount | A | C-REV-003 | Revenue detail to invoice reconciliation | D | Monthly | Accounting | ☐ |

### 3.4 Invoicing Process

| Risk ID | Risk Description | Assertion | Control ID | Control Description | Type | Freq | Owner | Key |
|---------|------------------|:---------:|------------|---------------------|:----:|:----:|-------|:---:|
| R-INV-001 | Shipments not invoiced | C | C-INV-001 | Weekly review of shipped-not-invoiced report | D | Weekly | Accounting | ☐ |
| R-INV-002 | Invoice amounts are incorrect | A | C-INV-002 | Pre-billing validation against sales order | P | Per Trans | Accounting | ☐ |
| R-INV-003 | Invoices sent to wrong customer | E | C-INV-003 | Customer master changes require supervisor approval | P | Per Trans | Controller | ☐ |

### 3.5 Cash Receipts & Application Process

| Risk ID | Risk Description | Assertion | Control ID | Control Description | Type | Freq | Owner | Key |
|---------|------------------|:---------:|------------|---------------------|:----:|:----:|-------|:---:|
| R-REC-001 | Cash not applied to receivables | C | C-REC-001 | Weekly review of unapplied cash report | D | Weekly | Accounting | ☐ |
| R-REC-002 | Cash applied to wrong invoice | A | C-REC-002 | Invoice number matching during cash application | P | Per Trans | Accounting | ☐ |
| R-REC-003 | AR balance does not agree to actual | E | C-REC-003 | Annual customer balance confirmations | D | Annual | Controller | ☐ |

---

## 4. Control Testing Plan

### 4.1 Sample Size Guidelines

| Control Frequency | Minimum Sample | Recommended Sample |
|-------------------|----------------|-------------------|
| Annual | 1 | 1 |
| Quarterly | 2 | 2 |
| Monthly | 2 | 5 |
| Weekly | 5 | 15 |
| Daily | 20 | 40 |
| Per Transaction | 25 | 60 |

### 4.2 Testing Procedure Types

| Procedure | Code | Description | When to Use |
|-----------|------|-------------|-------------|
| Inquiry | IQ | Questions to control performer | Understanding, supplemental |
| Observation | OB | Watch control being performed | Real-time controls |
| Inspection | IN | Review documents/records | Documented controls |
| Re-performance | RE | Re-execute the control | High-risk controls |

### 4.3 Test Results Log

| Control ID | Test Date | Tester | Sample Size | Exceptions | Result | Notes |
|------------|-----------|--------|-------------|------------|:------:|-------|
| C-001 | [Date] | [Name] | [n] | [n] | ☐Effective ☐Needs Improvement ☐Deficient | |
| C-002 | | | | | | |
| C-003 | | | | | | |

---

## 5. Deficiency Management

### 5.1 Identified Deficiencies

| Def ID | Control ID | Description | Root Cause | Classification | Owner | Due Date | Status |
|--------|------------|-------------|------------|----------------|-------|----------|--------|
| D-001 | C-001 | [Specific deficiency] | [Root cause analysis] | ☐Material Weakness ☐Significant Deficiency ☐Control Deficiency | [Name] | [Date] | ☐Open ☐In Progress ☐Closed |
| D-002 | | | | | | | |

### 5.2 Remediation Plan

| Def ID | Remediation Action | Responsible | Target Date | Actual Close | Validation Date |
|--------|-------------------|-------------|-------------|--------------|-----------------|
| D-001 | [Specific remediation] | [Name] | [Date] | [Date] | [Date] |
| D-002 | | | | | |

---

## 6. Residual Risk Assessment

### 6.1 Residual Risk Calculation

| Risk ID | Inherent Risk | Control Effectiveness | Residual Risk | Acceptable |
|---------|---------------|----------------------|---------------|------------|
| R-001 | High (20) | 80% | Low (4) | ☐Yes ☐No |
| R-002 | Medium (12) | 70% | Low (3.6) | ☐Yes ☐No |
| R-003 | High (16) | 50% | Medium (8) | ☐Yes ☐No |

**Residual Risk = Inherent Risk Score × (1 - Control Effectiveness %)**

### 6.2 Risk Heat Map

```
Impact
  5 │ ○   ○   ●   ●   ●
  4 │ ○   ○   ●   ●   ●
  3 │ ○   ○   ○   ●   ●
  2 │ ○   ○   ○   ○   ●
  1 │ ○   ○   ○   ○   ○
    └─────────────────────
      1   2   3   4   5  Likelihood

○ = Low Risk (Acceptable)
● = Medium-High Risk (Action Required)
```

---

## 7. Approval Section

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Preparer | | | |
| Reviewer | | | |
| Process Owner | | | |
| Internal Control Officer | | | |

---

## 8. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Name] | Initial creation |
| 1.1 | | | |
