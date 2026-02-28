# Procedure Template（操作手順テンプレート）

<!--
  This template is used for each individual operation procedure (OP-ID).
  Copy this template for each new operation and fill in the placeholders.
  All steps must follow the STEP format (Specific/Target/Expected/Proceed).
-->

---

## OP-{ID}: {OPERATION_NAME}

### Basic Information

| Item | Details |
|------|---------|
| **Operation ID** | OP-{ID} |
| **Operation Name** | {OPERATION_NAME} |
| **Description** | {OPERATION_DESCRIPTION} |
| **Category** | {CATEGORY} (Initial Setup / Daily / Weekly / Monthly / Ad-hoc / Admin) |
| **Frequency** | {FREQUENCY} (Daily / Weekly / Monthly / Quarterly / As needed) |
| **Estimated Time** | Approx. {ESTIMATED_TIME} minutes |
| **Target Role** | {TARGET_ROLE} (Administrator / Operator / General User / Approver) |
| **Prerequisites** | {PREREQUISITES} |
| **Input** | {INPUT_DATA} (data, documents, or information needed) |
| **Output** | {OUTPUT_DATA} (result of this operation) |

### Prerequisites Checklist

Before starting this operation, confirm the following:

- [ ] {PREREQUISITE_1} (e.g., Logged into the system with appropriate role)
- [ ] {PREREQUISITE_2} (e.g., Required data is prepared)
- [ ] {PREREQUISITE_3} (e.g., Preceding operation OP-{xxx} is completed)
- [ ] {PREREQUISITE_4} (e.g., Necessary approvals have been obtained)

---

### Procedure Steps

<!--
  STEP Format Reference:
  - Specific (S): Exact action verb (click, type, select, check, drag, etc.)
  - Target (T): UI element with exact label, type, and location
  - Expected (E): Observable result (screen change, message, data update)
  - Proceed (P): Confirmation check and transition to next step

  Step Numbering:
  - Main steps: 1, 2, 3...
  - Sub-steps: 1.1, 1.2, 1.3...
  - Conditional: 1a, 1b, 1c...
-->

<!-- Insert DANGER/WARNING/CAUTION notes BEFORE the step they relate to -->

| Step | Action (Specific) | Target | Expected Result | Proceed |
|------|-------------------|--------|-----------------|---------|
| 1 | {ACTION_VERB} {WHAT_TO_DO} | **{ELEMENT_LABEL}** {element_type} in {LOCATION} | {OBSERVABLE_RESULT} | {CONFIRMATION_AND_NEXT} |
| 2 | {ACTION_VERB} {WHAT_TO_DO} | **{ELEMENT_LABEL}** {element_type} | {OBSERVABLE_RESULT} | {CONFIRMATION_AND_NEXT} |
| 3 | {ACTION_VERB} {WHAT_TO_DO} | **{ELEMENT_LABEL}** {element_type} | {OBSERVABLE_RESULT} | {CONFIRMATION_AND_NEXT} |

[Screenshot: {DESCRIPTION_OF_SCREEN_STATE_AFTER_STEP_3}]

<!-- Example of a step with a WARNING note placed BEFORE the step -->

> [!WARNING]
> **WARNING / 警告**: {WARNING_MESSAGE}
>
> **Consequence**: {WHAT_HAPPENS_IF_IGNORED}

| Step | Action (Specific) | Target | Expected Result | Proceed |
|------|-------------------|--------|-----------------|---------|
| 4 | {ACTION_VERB} {WHAT_TO_DO} | **{ELEMENT_LABEL}** {element_type} | {OBSERVABLE_RESULT} | {CONFIRMATION_AND_NEXT} |

<!-- Example of conditional branching -->

**Step 5: {DECISION_POINT_DESCRIPTION}**

Condition: {WHAT_TO_CHECK}

**Step 5a** [If {CONDITION_A}]:

| Step | Action (Specific) | Target | Expected Result | Proceed |
|------|-------------------|--------|-----------------|---------|
| 5a | {ACTION_FOR_CONDITION_A} | **{ELEMENT_LABEL}** {element_type} | {RESULT_A} | Proceed to Step 6 |

**Step 5b** [If {CONDITION_B}]:

| Step | Action (Specific) | Target | Expected Result | Proceed |
|------|-------------------|--------|-----------------|---------|
| 5b | {ACTION_FOR_CONDITION_B} | **{ELEMENT_LABEL}** {element_type} | {RESULT_B} | Return to Step {N} |

<!-- Continue remaining steps -->

| Step | Action (Specific) | Target | Expected Result | Proceed |
|------|-------------------|--------|-----------------|---------|
| 6 | {ACTION_VERB} {WHAT_TO_DO} | **{ELEMENT_LABEL}** {element_type} | {OBSERVABLE_RESULT} | {CONFIRMATION_AND_NEXT} |
| 7 | {ACTION_VERB} {WHAT_TO_DO} | **{ELEMENT_LABEL}** {element_type} | {OBSERVABLE_RESULT} | Proceed to Verification |

[Screenshot: {DESCRIPTION_OF_FINAL_STATE}]

---

### Verification Checkpoint

Before considering this operation complete, confirm ALL of the following:

- [ ] {VERIFICATION_ITEM_1} (e.g., The new record appears in the list)
- [ ] {VERIFICATION_ITEM_2} (e.g., The status shows "Active")
- [ ] {VERIFICATION_ITEM_3} (e.g., The confirmation email has been sent)
- [ ] {VERIFICATION_ITEM_4} (e.g., The audit log entry has been created)

> [!CAUTION]
> **CAUTION / 注意**: If any verification item above is NOT confirmed, do NOT proceed to the next operation. Review the steps above and retry, or escalate to {ESCALATION_CONTACT}.

---

### Caution and Warning Summary

The following notes apply to this operation:

| Level | Step | Description |
|-------|------|-------------|
| {DANGER/WARNING/CAUTION/NOTE} | Before Step {N} | {BRIEF_DESCRIPTION} |
| {DANGER/WARNING/CAUTION/NOTE} | Before Step {N} | {BRIEF_DESCRIPTION} |

---

### Related Operations

| Relationship | OP-ID | Operation Name | Notes |
|-------------|-------|---------------|-------|
| Prerequisite | OP-{xxx} | {PREREQUISITE_OP_NAME} | Must be completed before this operation |
| Next step | OP-{xxx} | {NEXT_OP_NAME} | Typically performed after this operation |
| Alternative | OP-{xxx} | {ALTERNATIVE_OP_NAME} | Alternative approach for {SCENARIO} |
| Related | OP-{xxx} | {RELATED_OP_NAME} | Shares data or dependencies |

### Related Troubleshooting

| ID | Symptom | Quick Resolution |
|----|---------|-----------------|
| T-{xxx} | {SYMPTOM_1} | {QUICK_FIX_1} |
| T-{xxx} | {SYMPTOM_2} | {QUICK_FIX_2} |

---

### Screenshot Inventory

| # | Step | Filename | Description |
|---|------|----------|-------------|
| 1 | After Step 3 | OP-{ID}_03_{description}.png | {SCREENSHOT_DESCRIPTION_1} |
| 2 | After Step 7 | OP-{ID}_07_{description}.png | {SCREENSHOT_DESCRIPTION_2} |

---

### Revision Notes

| Date | Author | Change Description |
|------|--------|--------------------|
| {DATE} | {AUTHOR} | Initial creation |

---

<!--
  CHECKLIST FOR PROCEDURE AUTHOR:
  Before finalizing this procedure, verify:
  - [ ] All steps use precise action verbs (click, type, select, etc.)
  - [ ] All UI elements are identified by exact label, type, and location
  - [ ] Expected results describe observable outcomes
  - [ ] Proceed column confirms success and directs to next step
  - [ ] DANGER/WARNING/CAUTION notes are placed BEFORE the relevant step
  - [ ] Conditional branches clearly state the condition and both paths
  - [ ] Verification checkpoint covers all critical success criteria
  - [ ] Screenshot placeholders are included for key screens
  - [ ] Related operations and troubleshooting entries are cross-referenced
  - [ ] Step numbering is sequential and consistent
  - [ ] Prerequisites are specific and checkable
-->
