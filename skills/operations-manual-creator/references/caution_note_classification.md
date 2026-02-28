# Caution and Note Classification Guide（注意・警告分類ガイド）

## Purpose

This guide defines a classification system for caution, warning, and informational notes in software operations manuals. The system is inspired by ANSI Z535 safety signage standards, adapted for business system documentation.

All notes in the operations manual MUST follow these classification rules.

---

## 1. Classification Levels

### Overview Table

| Level | Signal Word | Color | Severity | Software Context |
|-------|------------|-------|----------|-----------------|
| DANGER | DANGER / 危険 | Red | Critical - Irreversible harm | Data destruction, account termination, security breach |
| WARNING | WARNING / 警告 | Orange | Serious - Significant impact | System-wide changes, bulk operations, permission escalation |
| CAUTION | CAUTION / 注意 | Yellow | Moderate - Unexpected results | Data inconsistency, unsaved changes, process interruption |
| NOTE | NOTE / 補足 | Blue | Informational | Tips, best practices, prerequisites, shortcuts |

---

## 2. DANGER（危険）- Red

### Definition

Use DANGER for operations that can cause **irreversible destruction** of data, system components, or user accounts. The consequences cannot be undone through normal system operations.

### Software Contexts

- Permanent deletion of production databases or tables
- Account termination or permanent deactivation
- Overwriting master data without backup
- Executing destructive scripts in production environments
- Revoking encryption keys or security certificates
- Purging audit logs or compliance records

### Format

**Markdown Callout Syntax:**

```markdown
> [!DANGER]
> **DANGER / 危険**: この操作はデータベースを完全に削除します。復元はできません。
> 実行前に必ずバックアップを取得してください。
>
> **Consequence**: All data in the database will be permanently destroyed.
> No recovery is possible after this operation completes.
```

**Rendered Example:**

> [!DANGER]
> **DANGER / 危険**: この操作はデータベースを完全に削除します。復元はできません。
> 実行前に必ずバックアップを取得してください。
>
> **Consequence**: All data in the database will be permanently destroyed.
> No recovery is possible after this operation completes.

### Rules for DANGER

1. Use sparingly - most software operations do NOT warrant DANGER level
2. MUST include a specific consequence description
3. MUST include a mitigation instruction (e.g., "take a backup first")
4. MUST be placed BEFORE the step, with visual separation
5. Consider adding a verification checkpoint BEFORE the dangerous step

---

## 3. WARNING（警告）- Orange

### Definition

Use WARNING for operations that can cause **significant negative impact** on multiple users, system configuration, or data integrity. The consequences may be reversible but require significant effort.

### Software Contexts

- Configuration changes that affect all users in the system
- Bulk data operations (mass update, mass delete, bulk import)
- Permission or role changes for groups of users
- System-wide settings changes (email templates, notification rules)
- Integration or API key changes affecting connected systems
- Workflow rule modifications in production
- Cache clearing or session invalidation affecting active users
- Scheduled job modifications that affect automated processes

### Format

**Markdown Callout Syntax:**

```markdown
> [!WARNING]
> **WARNING / 警告**: この設定変更は全ユーザーに即時反映されます。
> 変更前に影響範囲を確認し、必要に応じて事前通知を行ってください。
>
> **Consequence**: All active users will be affected immediately.
> Incorrect settings may disrupt ongoing work across the organization.
```

**Rendered Example:**

> [!WARNING]
> **WARNING / 警告**: この設定変更は全ユーザーに即時反映されます。
> 変更前に影響範囲を確認し、必要に応じて事前通知を行ってください。
>
> **Consequence**: All active users will be affected immediately.
> Incorrect settings may disrupt ongoing work across the organization.

### Rules for WARNING

1. MUST describe who/what is affected (scope of impact)
2. MUST include consequence description
3. SHOULD include a recommended mitigation or preparation step
4. MUST be placed BEFORE the associated step
5. Consider recommending off-hours execution for high-impact changes

---

## 4. CAUTION（注意）- Yellow

### Definition

Use CAUTION for operations where the user may experience **unexpected results**, data inconsistency, or minor disruption if the step is not performed carefully.

### Software Contexts

- Long-running processes where closing the browser causes data loss
- Operations sensitive to timezone or locale settings
- Steps where unsaved changes will be lost on navigation
- Operations that behave differently in different browsers
- Data entry fields with strict format requirements
- Concurrent editing scenarios (two users editing the same record)
- Operations that depend on external system availability
- Calculations affected by rounding or precision settings
- Import operations where duplicate handling varies by setting
- Steps that require specific network conditions (VPN, intranet)

### Format

**Markdown Callout Syntax:**

```markdown
> [!CAUTION]
> **CAUTION / 注意**: 処理中にブラウザを閉じるとデータが失われる可能性があります。
> 処理完了メッセージが表示されるまでブラウザを閉じないでください。
>
> **Consequence**: Partial data may be saved, resulting in inconsistent records
> that require manual cleanup.
```

**Rendered Example:**

> [!CAUTION]
> **CAUTION / 注意**: 処理中にブラウザを閉じるとデータが失われる可能性があります。
> 処理完了メッセージが表示されるまでブラウザを閉じないでください。
>
> **Consequence**: Partial data may be saved, resulting in inconsistent records
> that require manual cleanup.

### Rules for CAUTION

1. MUST describe the specific risk (what could go wrong)
2. MUST describe the consequence
3. SHOULD provide the correct way to avoid the problem
4. MUST be placed BEFORE the associated step
5. Include timing or duration information when relevant

---

## 5. NOTE（補足）- Blue

### Definition

Use NOTE for **helpful information** that improves the user's understanding or efficiency. Notes do not indicate risk but provide context, tips, or prerequisites.

### Software Contexts

- Features available only to specific roles or permission levels
- Keyboard shortcuts and efficiency tips
- Default values and how they are determined
- Data retention periods and archival policies
- Related features or alternative approaches
- Explanation of terminology used in the interface
- Browser recommendations and known compatibility notes
- Performance expectations (e.g., "Large exports may take up to 5 minutes")
- Links to related procedures or documentation

### Format

**Markdown Callout Syntax:**

```markdown
> [!NOTE]
> **NOTE / 補足**: この機能は管理者権限でのみ利用可能です。
> 権限がない場合は、システム管理者に権限付与を依頼してください。
```

**Rendered Example:**

> [!NOTE]
> **NOTE / 補足**: この機能は管理者権限でのみ利用可能です。
> 権限がない場合は、システム管理者に権限付与を依頼してください。

### Rules for NOTE

1. Keep notes concise and actionable
2. MUST be placed near the relevant step (before or after as appropriate)
3. Do NOT use NOTE for risk-related information (use CAUTION or higher)
4. Limit to 2-3 sentences
5. Group related notes together rather than scattering them

---

## 6. Placement Rules

### General Principle

**All DANGER, WARNING, and CAUTION notes MUST be placed BEFORE the step they relate to.** The user must read the warning before performing the action.

### Placement Hierarchy

When multiple notes apply to the same step, order them from highest to lowest severity:

```
> [!DANGER] ...
> [!WARNING] ...
> [!CAUTION] ...

Step N: Perform the action
```

### Spacing and Visual Separation

- Leave one blank line before and after each note block
- Do NOT embed notes inside step descriptions
- Use horizontal rules (`---`) to separate DANGER notes from surrounding content for maximum visibility

### Example of Correct Placement

```markdown
---

> [!DANGER]
> **DANGER / 危険**: This operation permanently deletes all records in the selected table.
> Ensure you have a current backup before proceeding.
>
> **Consequence**: All data will be irretrievably lost.

---

> [!WARNING]
> **WARNING / 警告**: This operation will lock the table during execution.
> Other users will be unable to access the data until the process completes.

Step 7:
  S: Click
  T: The **Delete All Records** button
  E: A final confirmation dialog appears asking "Are you sure?"
  P: Review the confirmation message carefully before responding
```

### Example of INCORRECT Placement

```markdown
Step 7:
  S: Click
  T: The **Delete All Records** button
  E: A final confirmation dialog appears

> [!DANGER]                     ← WRONG: After the step, user may have already clicked
> This operation permanently deletes all records.
```

---

## 7. Decision Flowchart

Use the following decision process to choose the correct classification level:

```
Start: Evaluate the step for potential risks
  │
  ├── Is the operation irreversible (no undo, no recovery)?
  │     ├── YES → Is production data or system integrity at risk?
  │     │           ├── YES → DANGER
  │     │           └── NO  → WARNING
  │     └── NO  → Continue evaluation
  │
  ├── Does the operation affect multiple users or system-wide settings?
  │     ├── YES → WARNING
  │     └── NO  → Continue evaluation
  │
  ├── Could the user experience unexpected results or minor data issues?
  │     ├── YES → CAUTION
  │     └── NO  → Continue evaluation
  │
  ├── Is there helpful context, a tip, or a prerequisite to mention?
  │     ├── YES → NOTE
  │     └── NO  → No note needed
  │
  └── End
```

---

## 8. Frequency Guidelines

### Expected Distribution

A well-written operations manual typically has the following note distribution:

| Level | Expected Frequency |
|-------|-------------------|
| DANGER | 0-2 per manual (rare) |
| WARNING | 3-10 per manual |
| CAUTION | 10-30 per manual |
| NOTE | 20-50 per manual |

### Over-Use Indicators

- If DANGER appears more than 5 times, the system design may need review
- If WARNING appears on every page, consider whether the classification is too aggressive
- If CAUTION is absent, the manual may be missing important risk communication
- If NOTE is absent, the manual may lack helpful context for users

### Under-Use Indicators

- Any step involving data deletion without a DANGER or WARNING
- Bulk operations without a WARNING
- Browser-dependent behavior without a CAUTION
- Role-restricted features without a NOTE

---

## 9. Bilingual Note Format

For bilingual manuals, use the following pattern:

```markdown
> [!WARNING]
> **WARNING / 警告**
>
> EN: This setting change will affect all active users immediately.
> Please verify the impact scope before applying.
>
> JA: この設定変更は全アクティブユーザーに即時反映されます。
> 適用前に影響範囲を確認してください。
>
> **Consequence / 影響**: Ongoing user sessions may be disrupted.
> 進行中のユーザーセッションが中断される可能性があります。
```

---

## 10. Quick Reference Card

| Ask Yourself | If YES | Classification |
|-------------|--------|---------------|
| Can this destroy data permanently? | Yes | DANGER |
| Does this affect all users or the entire system? | Yes | WARNING |
| Could the user get unexpected results? | Yes | CAUTION |
| Is there a helpful tip or prerequisite? | Yes | NOTE |
| None of the above? | - | No note needed |
