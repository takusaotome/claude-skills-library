---
description: |
  ドキュメントまたはコードを批判的視点でレビューする統合コマンド。
  対象の種類を拡張子から自動判別し、適切なペルソナで並列レビューを実行。
  - ドキュメント: Developer, PM, Customer, QA, Security, Ops の6視点
  - コード: Veteran Engineer, TDD Expert, Clean Code Expert, Bug Hunter の4視点
  Usage: /critical-review <path> [追加の指示]
allowed-tools: Read, Glob, Grep, Agent, Write, TodoWrite, AskUserQuestion
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

   **コンフィグ/スキーマ系ファイル** (.json, .yaml, .yml, .xml, .toml, .ini 等):
   `critical-code-reviewer` スキルの `references/file_type_classification.md` に準拠。
   判定優先順位: (1) ファイル名/明示パターン → (2) 拡張子ルール → (3) Content Sniffing（先頭20行）→ (4) AskUserQuestion（全て不明の場合のみ）

---

### Step 1.5: スケール判定

対象が大規模な場合:
- コード: 500行超 or 5ファイル超 → `critical-code-reviewer` の `references/scale_strategy.md` 参照
- ドキュメント: 30,000字超 or 見出し30超 → `critical-document-reviewer` の `references/scale_strategy.md` 参照

---

### Step 2: レビュータイプに応じた分岐

#### ドキュメントレビューの場合

1. **ペルソナ選択**:

   各ペルソナの詳細は対応スキルの SKILL.md を参照。

2. **文書タイプに応じたペルソナ選択**:

   ペルソナ選定は `critical-document-reviewer` スキルの `references/persona_selection_matrix.md` に準拠。

3. **並列レビュー実行**: Agent tool で選定したペルソナのレビューを並列実行
   - 各 Agent には `references/agents/{persona}.md` の内容をプロンプトとして渡す
   - レビュー対象文書をインラインで含める

4. **参照リソース**（`critical-document-reviewer` スキルディレクトリ内）:
   - `references/agents/*.md` - ペルソナプロンプト（6ファイル）
   - `references/critical_analysis_framework.md`
   - `references/evidence_evaluation_criteria.md`
   - `references/red_flag_patterns.md`
   - `references/persona_selection_matrix.md`
   - `references/severity_criteria.md`

5. **レポートテンプレート**:
   - `assets/review_report_template.md`

#### コードレビューの場合

1. **言語検出**: 追加チェックの適用判断
   - Python → 型ヒント、Pythonic patterns チェック
   - JavaScript/TypeScript → 型安全性、async patterns チェック

2. **ペルソナ（4種類）**:

   各ペルソナの詳細は対応スキルの SKILL.md を参照。

3. **並列レビュー実行**: Agent tool で4つのレビューを並列実行
   - 各 Agent には `references/agents/{persona}.md` の内容をプロンプトとして渡す
   - レビュー対象コードをインラインで含める

4. **参照リソース**（`critical-code-reviewer` スキルディレクトリ内）:
   - `references/agents/*.md` - ペルソナプロンプト（4ファイル）
   - `references/code_smell_patterns.md`
   - `references/review_framework.md`
   - `references/language_specific_checks.md`
   - `references/severity_criteria.md`
   - `references/file_type_classification.md`

5. **レポートテンプレート**:
   - `assets/code_review_report_template.md`

---

### Step 3: 結果統合

1. レビュー結果を収集
2. 重複する指摘を統合（複数ペルソナからの指摘として記録）
3. 重大度は各スキルの `references/severity_criteria.md` を参照して判定する。

4. 統合レビューレポートを生成

---

### Step 4: レポート出力

- デフォルト: 標準出力でユーザーに表示
- ファイル保存: ユーザーが明示的に指示した場合のみ

---

## 関連コマンド

直接呼び出しも可能:
- `/critical-document-reviewer` - ドキュメント専用（6ペルソナ、文書タイプで選択）
- `/critical-code-reviewer` - コード専用（4ペルソナ、言語別チェック付き）

---

## 重要な指示

- **並列実行**: サブエージェントは必ず並列で起動すること
- **ultrathink**: 各サブエージェントは ultrathink モードで深い分析を行う
- **ペルソナ選択**: ドキュメントは文書タイプに応じて適切な3-6ペルソナを選択
- **建設的**: 問題の指摘だけでなく、改善の方向性も示す
- **良い点も認める**: 問題だけでなく、良い設計/表現も指摘する
