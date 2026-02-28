---
name: operations-manual-creator
description: >
  業務システムの操作手順書を構造化して作成するスキル。STEPフォーマット
  （Specific/Target/Expected/Proceed）による手順記述、ANSI Z535準拠の
  注意・警告分類、トラブルシューティングガイドを含む包括的な操作マニュアルを
  生成する。Use when creating operations manuals, standard operating procedures (SOP),
  user guides, or system operation guides. Triggers: "operations manual",
  "操作マニュアル", "手順書作成", "SOP", "操作手順", "standard operating procedure",
  "ユーザーガイド", "作業手順書", "運用マニュアル"
---

# Operations Manual Creator（操作マニュアル作成）

## Overview

This skill creates structured, professional operations manuals for business systems. It follows the STEP format (Specific/Target/Expected/Proceed) for procedure writing, ANSI Z535-inspired caution/warning classification, and includes comprehensive troubleshooting guides.

The skill produces complete, ready-to-use operations manuals in both Japanese and English, suitable for enterprise environments.

## When to Use

- 業務システムの操作マニュアルを作成する
- 標準作業手順書(SOP)を作成する
- システム運用マニュアルを作成する
- ユーザーガイドを作成する
- 作業手順書を作成する

## Workflows

### Workflow 1: Scope and Audience Definition（スコープ・対象者定義）

**Purpose**: Establish the boundaries and target audience for the manual.

1. Ask the user to clarify:
   - What system is being documented?
   - What operations need to be covered?
   - Who is the target audience?
2. Determine skill level of the audience:
   - **Beginner**: New users, include every click and screenshot placeholder
   - **Intermediate**: Regular users, focus on complex operations
   - **Advanced**: Power users/admins, focus on edge cases and configuration
3. Define document scope:
   - Full manual (all operations for the system)
   - Specific procedures (selected operations only)
   - Quick-start guide (essential operations for onboarding)
4. Identify prerequisites:
   - Access rights and permissions required
   - Required software and versions
   - Prior knowledge or training required
   - Related documents to reference

### Workflow 2: Operations Inventory（操作一覧の棚卸し）

**Purpose**: Create a comprehensive list of all operations to document.

1. List all operations to be documented
2. Categorize each operation by:
   - **Frequency**: Daily / Weekly / Monthly / Quarterly / Ad-hoc
   - **Role**: Administrator / Operator / General User / Approver
   - **Dependency**: Which operations must be completed first
3. Assign operation IDs using the format: `OP-001`, `OP-002`, `OP-003`...
4. Create an operation dependency map:
   - Identify prerequisite operations (e.g., OP-001 must be done before OP-003)
   - Note parallel operations that can be done independently
5. Estimate time for each operation (in minutes)
6. Output the operations inventory table:

| OP-ID | Operation Name | Category | Frequency | Target Role | Est. Time | Prerequisites |
|-------|---------------|----------|-----------|-------------|-----------|---------------|
| OP-001 | ... | ... | ... | ... | ... min | - |

### Workflow 3: Procedure Writing（手順記述）

**Purpose**: Write detailed step-by-step procedures using the STEP format.

Load `references/procedure_writing_guide.md` for detailed STEP format guidance.

For each operation (OP-ID), use `assets/procedure_template.md` as the structure:

1. Write each step using the **STEP format**:
   - **S**pecific: What exactly to do (use precise action verbs: click, type, select, check, drag)
   - **T**arget: Which UI element (button name, field label, menu path like Menu > Submenu > Item)
   - **E**xpected: What should happen after this step (screen change, message display, data update)
   - **P**roceed: How to confirm success and transition to the next step
2. Use step numbering conventions:
   - Main steps: 1, 2, 3...
   - Sub-steps: 1.1, 1.2, 1.3...
   - Conditional branches: 1a (if condition A), 1b (if condition B)
3. Include screenshot placeholders where needed: `[Screenshot: {description}]`
4. Add verification checkpoints at critical points in the procedure

### Workflow 4: Caution/Warning Notes（注意・警告の付与）

**Purpose**: Add appropriate safety and caution labels to procedures.

Load `references/caution_note_classification.md` for ANSI Z535-inspired classification rules.

Apply the following classification:

| Level | Color | Use When |
|-------|-------|----------|
| DANGER | Red | Risk of irreversible data destruction, account termination |
| WARNING | Orange | Changes affecting all users, bulk operations, permission changes |
| CAUTION | Yellow | Risk of unexpected results, unsaved data loss, long-running processes |
| NOTE | Blue | Helpful tips, best practices, access requirements |

**Rules**:
- Place notes **BEFORE** the step they relate to (never after)
- Include the consequence description (what happens if the warning is ignored)
- Use Markdown callout syntax for visual formatting

### Workflow 5: Troubleshooting Guide Creation（トラブルシューティング）

**Purpose**: Create comprehensive troubleshooting resources.

Load `references/troubleshooting_guide.md` for troubleshooting methodology.

1. Create a **Symptom-Cause-Resolution table** for common issues:

| # | Symptom | Probable Cause | Resolution | Related OP |
|---|---------|---------------|------------|------------|
| T-001 | ... | ... | ... | OP-xxx |

2. Create **decision trees** for complex troubleshooting scenarios
3. Define **escalation procedure**:
   - L1 (Self-service): User can resolve with the manual
   - L2 (Helpdesk): Contact information and expected response time
   - L3 (Engineering): Critical issues requiring developer intervention
4. Specify **information to collect** before escalation:
   - Error message (exact text or screenshot)
   - Timestamp of occurrence
   - User ID and role
   - Steps taken before the error
   - Browser/device information

### Workflow 6: Manual Assembly and Review（組み立て・レビュー）

**Purpose**: Assemble all components into a complete manual and perform quality review.

1. Select the appropriate template:
   - Japanese: `assets/operations_manual_template_ja.md`
   - English: `assets/operations_manual_template_en.md`
2. Assemble all procedures into the template structure
3. Generate table of contents with page/section references
4. Run the **Quality Checklist**:
   - [ ] All operations in inventory have corresponding procedures
   - [ ] All steps follow STEP format consistently
   - [ ] Screenshot placeholders are included for UI-dependent steps
   - [ ] Caution/Warning notes are placed BEFORE relevant steps
   - [ ] Troubleshooting covers common error scenarios
   - [ ] Prerequisites are clearly stated for each operation
   - [ ] Terminology is consistent throughout the document
   - [ ] All cross-references (OP-IDs, section numbers) are valid
   - [ ] Contact information and escalation paths are complete
   - [ ] Version information and revision history are up to date

## Resources

| File | Purpose | When to Load |
|------|---------|-------------|
| `references/procedure_writing_guide.md` | STEP format detailed explanation, step numbering, screenshot guidelines, good/bad examples | Workflow 3: Procedure Writing |
| `references/caution_note_classification.md` | ANSI Z535-inspired classification for software documentation, decision flowchart | Workflow 4: Caution/Warning Notes |
| `references/troubleshooting_guide.md` | Symptom-Cause-Resolution format, decision trees, escalation procedures, common error patterns | Workflow 5: Troubleshooting Guide |
| `assets/operations_manual_template_ja.md` | Complete Japanese operations manual template (12 sections) | Workflow 6: Manual Assembly (Japanese) |
| `assets/operations_manual_template_en.md` | Complete English operations manual template (12 sections) | Workflow 6: Manual Assembly (English) |
| `assets/procedure_template.md` | Individual procedure template for each OP-ID with STEP format table | Workflow 3: Procedure Writing |

---

## Best Practices

### Do's
- 1ステップ=1アクション。複合操作は分解する
- UI要素は正確な名称（「保存」ではなく「画面右上の青い『保存』ボタン」）で指定する
- 注意・警告は該当ステップの**前**に配置する
- スクリーンショットプレースホルダーを必ず入れる（後から実画像を差し替え）
- 検証チェックポイントを各手順の最後に設ける

### Don'ts
- 「適宜」「適切に」「必要に応じて」などの曖昧表現を使わない
- WARNING/CAUTIONの過剰使用を避ける（重要度が薄れる）
- 暗黙知を前提とした手順を書かない（「いつもの方法で」は禁止）
- トラブルシューティングを省略しない

---

## Examples

### 例1: 在庫管理システム操作マニュアル

```
User: 在庫管理システムの操作マニュアルを作成してください。
      対象者: 倉庫スタッフ（ITリテラシー低め）

Claude:
1. [Workflow 1] スコープ定義 → 対象: 入荷/出荷/棚卸、スキルレベル: 初級
2. [Workflow 2] 操作棚卸し → OP-001(入荷登録), OP-002(出荷処理), OP-003(棚卸し), ...
3. [Workflow 3] STEP形式で各手順を記述（スクリーンショットプレースホルダー付き）
4. [Workflow 4] WARNING: 出荷確定後の取消不可、CAUTION: 棚卸し中のデータ変更禁止
5. [Workflow 5] トラブルシューティング: バーコード読取エラー、在庫不一致 等
6. [Workflow 6] operations_manual_template_ja.md で組み立て
```

### 例2: SaaS管理画面のSOP

```
User: CRM管理画面のユーザー管理SOPを作ってください。

Claude:
1. [Workflow 1] スコープ: ユーザー追加/変更/削除/権限設定、対象: IT管理者
2. [Workflow 2] OP-001(新規ユーザー追加), OP-002(権限変更), OP-003(アカウント無効化)
3. [Workflow 3] STEP形式: 各アクションの具体的操作手順
4. [Workflow 4] WARNING: 管理者権限の付与は要承認、NOTE: パスワードポリシー
5. [Workflow 6] procedure_template.md で個別手順として出力
```
