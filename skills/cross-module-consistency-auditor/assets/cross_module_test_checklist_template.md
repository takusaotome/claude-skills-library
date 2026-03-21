# Cross-Module Test Checklist

## Change Reference

| Attribute | Value |
|-----------|-------|
| **Change ID** | [Ticket/PR/Feature ID] |
| **Change Kernel** | [Brief description] |
| **Source Consistency Matrix** | [Link or reference to the consistency matrix that generated these test items] |
| **Date** | [Date] |

---

## Test Tier Legend

| Tier | Scope | Typical Tool | Execution |
|------|-------|--------------|-----------|
| **Unit** | Single module, isolated logic | pytest, JUnit, Jest | Automated, runs on every commit |
| **Integration** | Two or more modules interacting | pytest + DB, API test framework | Automated, runs on PR merge |
| **E2E** | Full system flow from input to output | Selenium, Cypress, Playwright | Automated or scheduled |
| **Manual** | Human verification required | Checklist, visual inspection | Manual, per release |

---

## Test Checklist

### Cross-Module Assertions

Tests that verify the same input produces the same output across all affected modules.

| ID | Rule | Test Description | Tier | Expected Assertion | Data Set | Owner | Status |
|----|------|------------------|------|--------------------|----------|-------|--------|
| CM-01 | All 6 flows use identical rounding | Apply cash rounding to $100.03 in Sale, Return, Exchange, Layaway Payment, Layaway Pickup, Account Payment | Integration | `rounded_total == 100.05` for all 6 flows | Standard: amount=$100.03, payment=cash | @payments-team | Not started |
| CM-02 | [Rule from consistency matrix] | [Test description] | [Tier] | [Expected result] | [Data set reference] | [Owner] | [Status] |

### Totals Reconciliation

Tests that verify aggregation totals match across reports and views.

| ID | Rule | Test Description | Tier | Expected Assertion | Data Set | Owner | Status |
|----|------|------------------|------|--------------------|----------|-------|--------|
| TR-01 | Daily summary == SUM(transactions) | Create 10 transactions with known amounts, verify daily summary total | Integration | `daily_summary_total == SUM(transaction_amounts)` | Mixed: 5 sales, 3 returns, 2 exchanges with known amounts | @reporting-team | Not started |
| TR-02 | [Rule from consistency matrix] | [Test description] | [Tier] | [Expected result] | [Data set reference] | [Owner] | [Status] |

### Sign Inversion Checks

Tests that verify forward and reverse operations produce symmetric results.

| ID | Rule | Test Description | Tier | Expected Assertion | Data Set | Owner | Status |
|----|------|------------------|------|--------------------|----------|-------|--------|
| SI-01 | Sale + Refund nets to zero | Create sale for $103.02 (with rounding adj), then full refund | Integration | `sale_total + refund_total == 0` for each component (base, tax, discount, rounding) | Forward: sale $100 + tax $8 - discount $5 + rounding $0.02; Reverse: full refund | @payments-team | Not started |
| SI-02 | [Rule from consistency matrix] | [Test description] | [Tier] | [Expected result] | [Data set reference] | [Owner] | [Status] |

### Before/After Snapshot Diffs

Tests that verify system state changes match specification after applying the change.

| ID | Rule | Test Description | Tier | Expected Assertion | Data Set | Owner | Status |
|----|------|------------------|------|--------------------|----------|-------|--------|
| BA-01 | [Rule from consistency matrix] | [Test description] | [Tier] | [Expected state after change] | [Before state + change action] | [Owner] | [Status] |

### Report vs Drill-Down Match

Tests that verify summary numbers match the sum of detail rows.

| ID | Rule | Test Description | Tier | Expected Assertion | Data Set | Owner | Status |
|----|------|------------------|------|--------------------|----------|-------|--------|
| RD-01 | Summary total == SUM(detail rows) | Generate daily summary and detail view for same date range | Integration | For each category: `summary_category_total == SUM(detail_rows WHERE category = X)` | 20 transactions across 4 categories | @reporting-team | Not started |
| RD-02 | [Rule from consistency matrix] | [Test description] | [Tier] | [Expected result] | [Data set reference] | [Owner] | [Status] |

### Reverse Flow Symmetry Checks

Tests that verify create/delete, entry/refund, entry/void produce symmetric results.

| ID | Rule | Test Description | Tier | Expected Assertion | Data Set | Owner | Status |
|----|------|------------------|------|--------------------|----------|-------|--------|
| RF-01 | Create + Delete restores original state | Create entity, verify it appears in queries, delete entity, verify it is removed from queries | Integration | Query count before == query count after create+delete | Standard entity with all fields populated | @backend-team | Not started |
| RF-02 | Entry + Void excludes from settlement | Create transaction, then void before batch close | Integration | Voided transaction not in settlement batch; batch total unchanged | Single transaction, void before settlement | @payments-team | Not started |
| RF-03 | [Rule from consistency matrix] | [Test description] | [Tier] | [Expected result] | [Data set reference] | [Owner] | [Status] |

---

## Data Set Definitions

Define reusable data sets referenced in the test checklist above.

| Data Set ID | Name | Description | Key Characteristics |
|-------------|------|-------------|---------------------|
| DS-01 | Standard sale | Basic sale transaction with all components | Amount=$100.00, Tax=$8.00, Discount=$0, Rounding=$0.00, Payment=Cash |
| DS-02 | Rounding boundary | Transaction requiring cash rounding | Amount=$100.03, Tax=$8.02, Rounding adj=+$0.00 to +$0.05 range |
| DS-03 | Mixed transactions | Set of transactions across all flows | 5 sales, 3 returns, 2 exchanges, 1 void, 1 layaway; varying amounts |
| DS-04 | Zero amount | Transaction with zero total | Amount=$0.00 (e.g., even exchange) |
| DS-05 | Maximum value | Transaction at system maximum | Amount=$999,999.99 or system max |
| DS-06 | Multi-period | Transactions spanning period boundary | 5 transactions on last day of period, 5 on first day of next period |
| [DS-ID] | [Name] | [Description] | [Characteristics] |

---

## Test Execution Summary

| Tier | Total Tests | Passed | Failed | Not Run | Blocked |
|------|-------------|--------|--------|---------|---------|
| Unit | [N] | [N] | [N] | [N] | [N] |
| Integration | [N] | [N] | [N] | [N] | [N] |
| E2E | [N] | [N] | [N] | [N] | [N] |
| Manual | [N] | [N] | [N] | [N] | [N] |
| **Total** | **[N]** | **[N]** | **[N]** | **[N]** | **[N]** |

---

## Failed Tests -- Action Items

| Test ID | Failure Description | Root Cause | Fix Owner | Priority | Deadline | Status |
|---------|---------------------|------------|-----------|----------|----------|--------|
| [Test ID] | [What failed] | [Why it failed] | [Owner] | [H/M/L] | [Date] | [Open/Fixed/Verified] |

---

## Coverage Gap Analysis

Tests that should exist but do not yet:

| Gap ID | Description | Affected Module(s) | Test Tier Needed | Priority | Owner |
|--------|-------------|---------------------|------------------|----------|-------|
| G1 | [Description of missing test coverage] | [Module list] | [Tier] | [H/M/L] | [Owner] |
