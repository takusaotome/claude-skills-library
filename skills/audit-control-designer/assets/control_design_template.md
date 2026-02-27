# Control Design Document (Draft)

## 1. Overview

| Item | Value |
|------|-------|
| Target Business Processes | {{PROCESS_SCOPE}} |
| Applicable Accounting Standard | {{ACCOUNTING_STANDARD}} |
| Industry / Business Type | {{INDUSTRY}} |
| Company Scale | {{SCALE}} |
| System Environment | {{SYSTEM_ENV}} |
| Regulatory Context | {{REGULATORY}} |

### Materiality Framework

| Item | Value | Basis | Status |
|------|-------|-------|--------|
| Overall Materiality | {{OVERALL_MAT}} | {{MAT_BASIS}} | Provisional |
| Performance Materiality | {{PERF_MAT}} | {{PERF_MAT_PCT}}% of Overall | Provisional |
| Clearly Trivial | {{TRIVIAL}} | {{TRIVIAL_PCT}}% of Overall | Provisional |

> Note: Formal materiality is set by the external auditor. Values above are provisional for internal control design purposes.

---

## 2. Control Table

| Control ID | Type | Objective | Procedure | Owner | Frequency | Evidence | Remediation |
|---|---|---|---|---|---|---|---|
| {{CTRL_ID}} | {{TYPE}} | {{OBJECTIVE}} | {{PROCEDURE}} | {{OWNER}} | {{FREQUENCY}} | {{EVIDENCE}} | {{REMEDIATION}} |

### Control Type Legend

| Type | Definition |
|---|---|
| **Preventive** | Stops errors/fraud before they occur (e.g., approval before posting, system validation) |
| **Detective** | Identifies errors/fraud after they occur (e.g., reconciliation, variance analysis) |

> Note: Paper+Excel environments tend to rely heavily on detective controls. The roadmap (Section 6) should address migration toward preventive controls through automation.

---

## 3. Assertion Mapping

### Coverage Matrix

| Assertion | Definition | Primary Controls | Secondary Controls | Coverage |
|---|---|---|---|---|
| Completeness (C) | All transactions recorded | {{C_PRIMARY}} | {{C_SECONDARY}} | {{C_COVERAGE}} |
| Accuracy (A) | Amounts are correct | {{A_PRIMARY}} | {{A_SECONDARY}} | {{A_COVERAGE}} |
| Valuation (V) | Appropriate valuation applied | {{V_PRIMARY}} | {{V_SECONDARY}} | {{V_COVERAGE}} |
| Cut-off (CO) | Correct period attribution | {{CO_PRIMARY}} | {{CO_SECONDARY}} | {{CO_COVERAGE}} |
| Existence (E) | Assets/transactions are real | {{E_PRIMARY}} | {{E_SECONDARY}} | {{E_COVERAGE}} |

### Coverage Assessment Scale

| Rating | Meaning |
|---|---|
| Strong | 2+ controls with clear evidence and remediation |
| Adequate | 1 control directly addressing the assertion |
| Weak | Only indirect coverage |
| Gap | No coverage — requires immediate attention |

---

## 4. Segregation of Duties (SoD) Analysis

| # | Duty Pair | Current Assignment | Separation Status | Risk Level | Compensating Controls | Action Required |
|---|---|---|---|---|---|---|
| SoD-1 | Entry / Approval | {{SOD1_ASSIGN}} | {{SOD1_STATUS}} | {{SOD1_RISK}} | {{SOD1_COMP}} | {{SOD1_ACTION}} |
| SoD-2 | Ordering / Receiving | {{SOD2_ASSIGN}} | {{SOD2_STATUS}} | {{SOD2_RISK}} | {{SOD2_COMP}} | {{SOD2_ACTION}} |
| SoD-3 | Recording / Custody | {{SOD3_ASSIGN}} | {{SOD3_STATUS}} | {{SOD3_RISK}} | {{SOD3_COMP}} | {{SOD3_ACTION}} |
| SoD-4 | Counting / Booking | {{SOD4_ASSIGN}} | {{SOD4_STATUS}} | {{SOD4_RISK}} | {{SOD4_COMP}} | {{SOD4_ACTION}} |
| SoD-5 | Calculation / Verification | {{SOD5_ASSIGN}} | {{SOD5_STATUS}} | {{SOD5_RISK}} | {{SOD5_COMP}} | {{SOD5_ACTION}} |

> Note: In organizations with fewer than 50 employees, complete SoD may not be feasible. Compensating controls are specified for such cases.

---

## 5. KPI Definitions

| KPI ID | Name | Formula | Baseline | Target | Data Source | Related Controls |
|---|---|---|---|---|---|---|
| {{KPI_ID}} | {{KPI_NAME}} | {{KPI_FORMULA}} | {{BASELINE}} | {{TARGET}} | {{DATA_SOURCE}} | {{RELATED_CTRLS}} |

### KPI Measurement Plan

| KPI ID | Measurement Start | First Review | Responsible |
|---|---|---|---|
| {{KPI_ID}} | {{MEAS_START}} | {{FIRST_REVIEW}} | {{RESPONSIBLE}} |

---

## 6. Roadmap

### Short-term (M+1 to M+4): Control Establishment

| # | Initiative | Target Controls | Owner | Target Date | Success Criteria |
|---|---|---|---|---|---|
| S{{N}} | {{INITIATIVE}} | {{CTRL_IDS}} | {{OWNER}} | M+{{N}} | {{SUCCESS}} |

### Medium-term (M+6 to M+18): Automation and Enhancement

| # | Initiative | Target | Owner | Target Date | Success Criteria |
|---|---|---|---|---|---|
| M{{N}} | {{INITIATIVE}} | {{TARGET}} | {{OWNER}} | M+{{N}} | {{SUCCESS}} |

### Expected Outcomes (Post Short-term Implementation)

| Metric | Current State | Post-Implementation Target |
|---|---|---|
| {{METRIC}} | {{CURRENT}} | {{TARGET}} |

---

## 7. Open Questions

| # | Related Control | Question | Options | Recommendation | Owner | Resolution Deadline |
|---|---|---|---|---|---|---|
| Q{{N}} | {{CTRL_ID}} | {{QUESTION}} | {{OPTIONS}} | {{RECOMMENDATION}} | {{OWNER}} | {{DEADLINE}} |

> Note: Controls referencing open questions are not fully implementable until the questions are resolved. Provisional treatments are documented in the control procedures where applicable.

---

## Appendix A: Process-to-Control Mapping

| Process ID | Process Name | Audit Relevance | Mapped Controls |
|---|---|---|---|
| {{PROC_ID}} | {{PROC_NAME}} | {{RELEVANCE}} | {{MAPPED_CTRLS}} |

## Appendix B: ITGC Considerations

| ITGC Domain | Current Relevance | Risk | Mitigation |
|---|---|---|---|
| Access Management | {{ACCESS_DESC}} | {{ACCESS_RISK}} | {{ACCESS_MIT}} |
| Change Management | {{CHANGE_DESC}} | {{CHANGE_RISK}} | {{CHANGE_MIT}} |
| Backup/Recovery | {{BACKUP_DESC}} | {{BACKUP_RISK}} | {{BACKUP_MIT}} |
| Data Integrity | {{DATA_DESC}} | {{DATA_RISK}} | {{DATA_MIT}} |

> Note: For Paper+Excel environments, ITGC considerations are limited to manual-level IT controls. Full ITGC evaluation is required when system automation is introduced (see Medium-term Roadmap).

---

*Generated by: audit-control-designer skill*
*Status: Draft — requires review and confirmation of context variables, open questions, and materiality framework*
*Recommended next step: Review with audit-doc-checker skill (target score: 70+)*
