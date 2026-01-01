---
description: |
  ドキュメントまたはコードを批判的視点でレビューする統合コマンド。
  対象の種類を拡張子から自動判別し、適切なペルソナで並列レビューを実行。
  - ドキュメント: Developer, PM, Customer の3視点
  - コード: Veteran Engineer, TDD Expert, Clean Code Expert の3視点
  Usage: /critical-review <path> [追加の指示]
allowed-tools: Read, Glob, Grep, Task, Write, TodoWrite, AskUserQuestion
argument-hint: <path> [追加の指示]
---

# Critical Review Command (統合版)

## 引数

```
$ARGUMENTS
```

**引数の解釈**:
- ファイルパスが含まれる場合: そのファイルをレビュー対象とする
- ディレクトリパスが含まれる場合: そのディレクトリ内をレビュー対象とする
- 追加の指示がある場合: レビュー時の重点項目として考慮する
- 引数が空の場合: ユーザーにレビュー対象を確認する

**使用例**:
- `/critical-review docs/design.md` → design.md をドキュメントレビュー
- `/critical-review src/main.py` → main.py をコードレビュー
- `/critical-review src/` → src/ ディレクトリをコードレビュー
- `/critical-review docs/analysis.md 根拠の妥当性を重点的に` → 根拠重視でレビュー
- `/critical-review src/api.py テスト容易性を重点的に` → テスト容易性重視でレビュー
- `/critical-review` → 対象を確認してからレビュー

---

## 実行手順

### Step 1: 対象の読み込みと種類の自動判別

1. **パスの確認**: 引数からファイル/ディレクトリパスを抽出
   - 追加の指示があれば抽出（レビュー重点項目として使用）
   - 引数が空または不明確な場合は、ユーザーにレビュー対象を確認する

2. **拡張子による自動判別**:

   **ドキュメント**:
   ```
   .md, .txt, .docx, .pdf, .rtf, .rst, .adoc, .html, .htm
   ```

   **コード**:
   ```
   .py, .js, .ts, .jsx, .tsx, .java, .go, .rs, .c, .cpp, .h, .hpp,
   .cs, .rb, .php, .swift, .kt, .scala, .sh, .bash, .zsh, .sql,
   .vue, .svelte, .css, .scss, .less
   ```

   **ディレクトリの場合**: 配下ファイルの拡張子分布で判定
   - コード系が多数 → コードレビュー
   - ドキュメント系が多数 → ドキュメントレビュー
   - 混在 → AskUserQuestion で確認

   **判定不可** (`.json`, `.yaml`, `.xml` 等): AskUserQuestion で確認

---

### Step 2: レビュータイプに応じた分岐

#### ドキュメントレビューの場合

1. **ペルソナ**:
   - Developer（開発者/実装者視点）
   - PM（プロジェクトマネージャー視点）
   - Customer（顧客/ステークホルダー視点）

2. **並列レビュー実行**: Task tool で3つのサブエージェントを並列起動
   - `document-reviewer-developer`
   - `document-reviewer-pm`
   - `document-reviewer-customer`

3. **参照リソース**:
   - `skills/critical-document-reviewer/references/critical_analysis_framework.md`
   - `skills/critical-document-reviewer/references/evidence_evaluation_criteria.md`
   - `skills/critical-document-reviewer/references/persona_definitions.md`
   - `skills/critical-document-reviewer/references/red_flag_patterns.md`

4. **レポートテンプレート**:
   - `skills/critical-document-reviewer/assets/review_report_template.md`

#### コードレビューの場合

1. **言語検出**: 追加チェックの適用判断
   - Python → 型ヒント、Pythonic patterns チェック
   - JavaScript/TypeScript → 型安全性、async patterns チェック

2. **ペルソナ**:
   - Veteran Engineer（20年ベテラン視点）
   - TDD Expert（テスト容易性視点）
   - Clean Code Expert（可読性/SOLID視点）

3. **並列レビュー実行**: Task tool で3つのサブエージェントを並列起動
   - `code-reviewer-veteran-engineer`
   - `code-reviewer-tdd-expert`
   - `code-reviewer-clean-code-expert`

4. **参照リソース**:
   - `skills/critical-code-reviewer/references/persona_definitions.md`
   - `skills/critical-code-reviewer/references/code_smell_patterns.md`
   - `skills/critical-code-reviewer/references/review_framework.md`
   - `skills/critical-code-reviewer/references/language_specific_checks.md`

5. **レポートテンプレート**:
   - `skills/critical-code-reviewer/assets/code_review_report_template.md`

---

### Step 3: 結果統合

1. 3つのレビュー結果を収集
2. 重複する指摘を統合（複数ペルソナからの指摘として記録）
3. 重大度を付与:

| 重大度 | 定義 |
|--------|------|
| **Critical** | このまま進めると失敗リスク大。バグ、データ損失、セキュリティ問題 |
| **Major** | 重大な問題。根拠不十分、重大な設計欠陥 |
| **Minor** | 改善推奨だが緊急ではない |
| **Info** | 参考情報、ベストプラクティス提案 |

4. 統合レビューレポートを生成

---

### Step 4: レポート出力

- 対象と同じディレクトリに保存（推奨）
  - ドキュメント: `REVIEW_REPORT_<文書名>.md`
  - コード: `CODE_REVIEW_REPORT_<ファイル/ディレクトリ名>.md`
- または標準出力でユーザーに表示

---

## 関連コマンド

直接呼び出しも可能:
- `/critical-document-reviewer` - ドキュメント専用（ペルソナ選択可能）
- `/critical-code-reviewer` - コード専用（言語別チェック付き）

---

## 重要な指示

- **並列実行**: 3つのサブエージェントは必ず並列で起動すること
- **ultrathink**: 各サブエージェントは ultrathink モードで深い分析を行う
- **建設的**: 問題の指摘だけでなく、改善の方向性も示す
- **良い点も認める**: 問題だけでなく、良い設計/表現も指摘する
