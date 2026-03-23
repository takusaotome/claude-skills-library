# Change Impact Map

## Change Kernel

| Attribute | Description |
|-----------|-------------|
| **Change ID** | [Ticket/PR/Feature ID] |
| **What** | [Precise description of the change] |
| **Where (Source of Truth)** | [File/module/function that is the canonical implementation] |
| **Why** | [Business requirement or defect driving the change] |
| **Invariant** | [The consistency rule that must hold everywhere this change touches] |
| **Compound?** | [YES/NO -- if YES, decompose into sub-kernels below] |

### Sub-Kernels (if compound)

| Sub-Kernel ID | What | Source of Truth |
|---------------|------|-----------------|
| K1 | [Sub-change description] | [Location] |
| K2 | [Sub-change description] | [Location] |

---

## Source of Truth

| Attribute | Value |
|-----------|-------|
| **Module** | [Module name] |
| **File** | [File path] |
| **Function/Class** | [Function or class name] |
| **Test Coverage** | [Existing test file and coverage level] |
| **Owner** | [Team or individual responsible] |

---

## Affected Modules

### Input Flows

| Module | File/Endpoint | Read/Write | Copy or Reference? | Test Coverage | Risk |
|--------|---------------|------------|---------------------|---------------|------|
| Sale entry | `src/flows/sale.py:process_payment()` | Write | Copy of source | Unit tests exist | Medium |
| [Module name] | [File path] | [Read/Write] | [Copy/Reference] | [Coverage level] | [H/M/L] |

### Persistence

| Module | Table/Store | Operation | Impact Description | Test Coverage | Risk |
|--------|-------------|-----------|---------------------|---------------|------|
| Order service | `orders.line_items` | UPDATE | Rounding adjustment column added | Integration tests exist | High |
| [Module name] | [Table name] | [INSERT/UPDATE/DELETE] | [What changes] | [Coverage level] | [H/M/L] |

### Aggregation

| Module | Aggregation Type | Includes Change? | Filter Condition | Test Coverage | Risk |
|--------|------------------|-------------------|------------------|---------------|------|
| Daily sales report | SUM(line_total) | YES | WHERE date = today | Report test exists | High |
| [Module name] | [SUM/COUNT/GROUP BY] | [YES/NO/TBD] | [WHERE clause or filter] | [Coverage level] | [H/M/L] |

### Display / Reports

| Report/Screen | Data Source | Shows Affected Data? | Format Impact | Test Coverage | Risk |
|---------------|-------------|----------------------|---------------|---------------|------|
| POS receipt | `receipt_query` view | YES | Rounding adjustment line added | No automated test | High |
| [Report name] | [Query/view/API] | [YES/NO/TBD] | [New column/row/section] | [Coverage level] | [H/M/L] |

### API / Export

| Endpoint/Export | Method | Payload Impact | Consumer(s) | Test Coverage | Risk |
|-----------------|--------|----------------|-------------|---------------|------|
| `/api/v1/orders/{id}` | GET | `rounding_adjustment` field added | HQ sync, mobile app | Contract test exists | Medium |
| [Endpoint path] | [GET/POST/PUT] | [New field/changed value] | [Consumer list] | [Coverage level] | [H/M/L] |

### Reverse Flow

| Flow | Forward Counterpart | Reversal Mechanism | Symmetry Verified? | Test Coverage | Risk |
|------|---------------------|--------------------|---------------------|---------------|------|
| Refund | Sale entry | Negative rounding adjustment line | NO — needs verification | None | High |
| [Refund flow] | [Sale flow] | [Negative line item] | [YES/NO/TBD] | [Coverage level] | [H/M/L] |

### Permission / Visibility

| Module/View | Role Affected | Visibility Rule | Consistent with Other Views? | Test Coverage | Risk |
|-------------|---------------|-----------------|-------------------------------|---------------|------|
| Manager dashboard | store_manager | Show rounding column | TBD — cashier view hides it | None | Low |
| [Module name] | [Role name] | [Show/Hide/Mask] | [YES/NO/TBD] | [Coverage level] | [H/M/L] |

### Downstream Jobs

| Job/Process | Trigger | Processes Affected Data? | Impact Description | Test Coverage | Risk |
|-------------|---------|--------------------------|---------------------|---------------|------|
| [Job name] | [Schedule/event] | [YES/NO/TBD] | [What changes] | [Coverage level] | [H/M/L] |

---

## Affected Outputs

| Output Type | Output Name | Change Description | Owner | Status |
|-------------|-------------|--------------------|-------|--------|
| Report | [Report name] | [New line/column, changed total] | [Owner] | [Not started/In progress/Done] |
| API response | [Endpoint] | [New field, changed value] | [Owner] | [Status] |
| Export file | [File type] | [New column, changed format] | [Owner] | [Status] |
| Notification | [Notification type] | [New content, changed trigger] | [Owner] | [Status] |

---

## Affected Tests

| Test Type | Test File/Suite | Current Coverage | Gap Description | Action Required |
|-----------|-----------------|------------------|-----------------|-----------------|
| Unit | [Test file path] | [Covered/Partial/None] | [What is missing] | [Write new/Update existing] |
| Integration | [Test file path] | [Covered/Partial/None] | [What is missing] | [Write new/Update existing] |
| E2E | [Test file path] | [Covered/Partial/None] | [What is missing] | [Write new/Update existing] |
| Manual | [Test case ID] | [Covered/Partial/None] | [What is missing] | [Write new/Update existing] |

---

## Affected Documentation

| Document Type | Document Name/Path | Change Required | Owner | Status |
|---------------|---------------------|-----------------|-------|--------|
| Tech spec | [Document path] | [Section to update] | [Owner] | [Status] |
| API doc | [Document path] | [Endpoint to update] | [Owner] | [Status] |
| User guide | [Document path] | [Section to update] | [Owner] | [Status] |
| Runbook | [Document path] | [Procedure to update] | [Owner] | [Status] |

---

## Risk Notes

| Risk ID | Description | Affected Modules | Likelihood | Impact | Mitigation |
|---------|-------------|------------------|------------|--------|------------|
| R1 | [Risk description] | [Module list] | [H/M/L] | [H/M/L] | [Mitigation action] |

---

## Summary

| Category | Count | With Test Coverage | Without Test Coverage | Needs Confirmation |
|----------|-------|--------------------|----------------------|---------------------|
| Input Flows | [N] | [N] | [N] | [N] |
| Persistence | [N] | [N] | [N] | [N] |
| Aggregation | [N] | [N] | [N] | [N] |
| Display/Reports | [N] | [N] | [N] | [N] |
| API/Export | [N] | [N] | [N] | [N] |
| Reverse Flow | [N] | [N] | [N] | [N] |
| Permission/Visibility | [N] | [N] | [N] | [N] |
| Downstream Jobs | [N] | [N] | [N] | [N] |
| **Total** | **[N]** | **[N]** | **[N]** | **[N]** |

**Copy Implementations**: [N] copies of source of truth logic
**Shared Reference Implementations**: [N] modules referencing the source of truth

---

## Appendix: Open Questions / Missing Modules

Items that may be affected but lack confirmation. Each must be resolved before the change is considered fully audited.

| OQ-ID | Question | Affected Area | Blocking? | Owner | Due Date | Resolution |
|-------|----------|---------------|-----------|-------|----------|------------|
| OQ-001 | Does the loyalty points module use the same rounding rule? | Aggregation | Yes | Backend team | 2026-04-01 | Pending |
| OQ-002 | [Question description] | [Area] | [Yes/No] | [Owner] | [Date] | [Pending/Resolved: answer] |
