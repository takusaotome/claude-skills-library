# Cross-Module Consistency Matrix

## Change Reference

| Attribute | Value |
|-----------|-------|
| **Change ID** | [Ticket/PR/Feature ID] |
| **Change Kernel** | [Brief description] |
| **Date** | [Audit date] |
| **Auditor** | [Name] |

---

## Matrix Legend

| Status | Meaning |
|--------|---------|
| PASS | Verified consistent -- no gap detected |
| FAIL | Inconsistency detected -- action required |
| NOT TESTED | Not yet verified -- testing pending |
| N/A | Rule does not apply to this module/flow |

---

## Consistency Matrix

### Aggregation Totals

| Module / Flow / Report | Rule | Expected Behavior | Current State | Gap | Status | Owner | Action Item |
|------------------------|------|-------------------|---------------|-----|--------|-------|-------------|
| Daily cash summary | SUM(line items) == report total | Total includes rounding adjustments | Rounding adjustments included in SUM | None | PASS | @backend-team | -- |
| HQ consolidation report | SUM(store totals) == HQ total | All stores included | [To verify] | [TBD] | NOT TESTED | @reporting-team | Verify query includes all store IDs |
| [Module/flow/report] | [Rule description] | [Expected] | [Current] | [Gap description] | [Status] | [Owner] | [Action] |

### Status Transitions

| Module / Entry Point | Rule | Expected Behavior | Current State | Gap | Status | Owner | Action Item |
|----------------------|------|-------------------|---------------|-----|--------|-------|-------------|
| API endpoint POST /orders | Status guard: only PENDING to CONFIRMED allowed | Rejects CANCELLED to CONFIRMED | [To verify] | [TBD] | NOT TESTED | @api-team | Add integration test |
| [Module/entry point] | [Rule description] | [Expected] | [Current] | [Gap description] | [Status] | [Owner] | [Action] |

### Sign Inversion

| Module / Flow | Rule | Expected Behavior | Current State | Gap | Status | Owner | Action Item |
|---------------|------|-------------------|---------------|-----|--------|-------|-------------|
| Refund flow | sale_amount + refund_amount == 0 | Refund creates negative line items | Refund negates base but not rounding adj | Rounding adj not reversed | FAIL | @payments-team | Add rounding reversal to refund flow |
| [Module/flow] | [Rule description] | [Expected] | [Current] | [Gap description] | [Status] | [Owner] | [Action] |

### Tax / Rounding

| Module / Flow | Rule | Expected Behavior | Current State | Gap | Status | Owner | Action Item |
|---------------|------|-------------------|---------------|-----|--------|-------|-------------|
| Sale flow | Round to nearest 0.05 using HALF_UP | Cash total rounded after tax | [To verify] | [TBD] | NOT TESTED | @payments-team | Write unit test for rounding |
| [Module/flow] | [Rule description] | [Expected] | [Current] | [Gap description] | [Status] | [Owner] | [Action] |

### Visibility / Permission

| Module / View | Rule | Expected Behavior | Current State | Gap | Status | Owner | Action Item |
|---------------|------|-------------------|---------------|-----|--------|-------|-------------|
| [Module/view] | [Rule description] | [Expected] | [Current] | [Gap description] | [Status] | [Owner] | [Action] |

### Naming / Constants

| Module / Location | Rule | Expected Behavior | Current State | Gap | Status | Owner | Action Item |
|-------------------|------|-------------------|---------------|-----|--------|-------|-------------|
| [Module/location] | [Rule description] | [Expected] | [Current] | [Gap description] | [Status] | [Owner] | [Action] |

### Report vs Drill-Down

| Report Pair | Rule | Expected Behavior | Current State | Gap | Status | Owner | Action Item |
|-------------|------|-------------------|---------------|-----|--------|-------|-------------|
| Daily summary vs transaction detail | Summary total == SUM(detail rows) | Totals match | Summary excludes voided but detail shows them | Voided transactions in detail but not summary | FAIL | @reporting-team | Add void filter to detail query or include voids in summary |
| [Report pair] | [Rule description] | [Expected] | [Current] | [Gap description] | [Status] | [Owner] | [Action] |

---

## Gap Summary

| Category | Total Rules | PASS | FAIL | NOT TESTED | N/A |
|----------|-------------|------|------|------------|-----|
| Aggregation Totals | [N] | [N] | [N] | [N] | [N] |
| Status Transitions | [N] | [N] | [N] | [N] | [N] |
| Sign Inversion | [N] | [N] | [N] | [N] | [N] |
| Tax / Rounding | [N] | [N] | [N] | [N] | [N] |
| Visibility / Permission | [N] | [N] | [N] | [N] | [N] |
| Naming / Constants | [N] | [N] | [N] | [N] | [N] |
| Report vs Drill-Down | [N] | [N] | [N] | [N] | [N] |
| **Total** | **[N]** | **[N]** | **[N]** | **[N]** | **[N]** |

---

## Action Items from FAIL Status

| ID | Category | Module | Gap Description | Owner | Priority | Deadline | Status |
|----|----------|--------|-----------------|-------|----------|----------|--------|
| A1 | Sign Inversion | Refund flow | Rounding adjustment not reversed | @payments-team | High | [Date] | Open |
| A2 | Report vs Drill-Down | Daily summary | Voided transactions inconsistency | @reporting-team | Medium | [Date] | Open |
| [ID] | [Category] | [Module] | [Gap] | [Owner] | [H/M/L] | [Date] | [Status] |

---

## Open Questions

| ID | Question | Context | Assigned To | Due Date | Resolution |
|----|----------|---------|-------------|----------|------------|
| Q1 | [Question that needs business/technical clarification] | [Why it matters] | [Person] | [Date] | [Pending/Resolved: answer] |
