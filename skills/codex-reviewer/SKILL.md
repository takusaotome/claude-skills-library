---
name: codex-reviewer
description: OpenAI Codex CLIを使用してドキュメントやコードのレビューを依頼するスキル。GPT-5.3-Codexモデルを高推論モード(high)で呼び出し、最も深い分析によるレビューを実行。レビュー結果を指定フォルダに出力し、その内容を確認・分析する機能を提供。コードレビュー、ドキュメントレビュー、設計書レビュー、テスト計画レビューなど、専門的なレビューが必要な場面で使用。
---

# Codex Reviewer

## Overview

OpenAI Codex CLIを活用して、コードやドキュメントの専門的なレビューを実行するスキルです。レビュータイプに応じて最適なモデルを自動選択し、**xhigh推論モード**で徹底的な分析を行います。

- **コード/テスト**: GPT-5.3-Codex（エージェント型コーディングモデル）
- **ドキュメント/設計**: GPT-5.3-Thinking（深い推論モデル）

## When to Use

- コードの品質レビュー、セキュリティレビュー、パフォーマンスレビューが必要な時
- 設計書、仕様書、技術ドキュメントのレビューが必要な時
- テスト計画、テストケースのレビューが必要な時
- プルリクエストの詳細レビューが必要な時
- 外部の専門的な視点でのレビューを得たい時

## ファイル拡張子とレビュータイプの対応

ユーザーからファイルパスが指示された場合、以下の対応表に基づいて `--type` を自動選択すること：

| 拡張子/パターン | --type | 使用モデル |
|----------------|--------|-----------|
| `.py`, `.js`, `.ts`, `.tsx`, `.java`, `.go`, `.rs`, `.cpp`, `.c`, `.rb`, `.php` | code | gpt-5.3-codex |
| `.md`, `.txt`, `.rst`, `.docx`, `.pdf`, `仕様書`, `要件定義` | document | gpt-5.3-thinking |
| `design/`, `architecture/`, `設計書`, `アーキテクチャ` | design | gpt-5.3-thinking |
| `tests/`, `test_*`, `*.test.*`, `*_test.*`, `*.spec.*` | test | gpt-5.3-codex |

**例:**
- 「`src/main.py`をレビューして」→ `--type code`
- 「`docs/spec.md`をレビューして」→ `--type document`
- 「`design/architecture.md`をレビューして」→ `--type design`
- 「`tests/test_api.py`をレビューして」→ `--type test`

**軽量レビュー（クイックレビュー）の指示:**
- 「軽量レビュー」「クイックレビュー」「高速で」「quick」などのキーワードが含まれる場合 → `--profile quick-review` を追加

## Prerequisites

1. **Codex CLIのインストール**
   ```bash
   npm install -g @openai/codex
   # または
   brew install --cask codex
   ```

2. **認証設定**
   ```bash
   codex login
   ```

3. **推奨: プロファイル設定** (`~/.codex/config.toml`)
   ```toml
   # デフォルトプロファイル
   [profiles.deep-review]
   model = "gpt-5.3-codex"
   model_reasoning_effort = "high"
   approval_policy = "never"
   ```

## Workflow

### Phase 1: レビュー依頼の準備

1. **レビュー対象の確認**
   - ファイルパスまたはディレクトリパスを特定
   - レビュータイプを決定（コード/ドキュメント/設計/テスト）
   - レビュー観点を明確化

2. **出力先フォルダの準備**
   - レビュー結果を保存するフォルダを作成または確認
   - 例: `./reviews/`, `./code-reviews/`, `./doc-reviews/`

### Phase 2: Codex CLIによるレビュー実行

> **重要**: `run_codex_review.py` スクリプトは常に **`--full-auto` モード**で実行されます。
> これにより、ユーザー承認なしでCodexがコマンドを自動実行します。
> また、スクリプトは**内部定義のプロファイル**を使用するため、`~/.codex/config.toml` のプロファイル設定は参照されません。

**スクリプトを使用したレビュー（推奨）:**
```bash
# コードレビュー
python3 skills/codex-reviewer/scripts/run_codex_review.py \
  --type code \
  --target src/ \
  --output ./reviews

# ドキュメントレビュー
python3 skills/codex-reviewer/scripts/run_codex_review.py \
  --type document \
  --target docs/spec.md \
  --output ./reviews
```

**Codex CLIを直接使用する場合:**
```bash
codex exec --profile deep-review \
  -o <output-file> \
  "<review-prompt>"
```

**コードレビューの例（直接実行）:**
```bash
codex exec --profile deep-review \
  -C /path/to/project \
  -o ./reviews/code_review_$(date +%Y%m%d_%H%M%S).md \
  "以下のコードを詳細にレビューしてください。セキュリティ、パフォーマンス、保守性、ベストプラクティスの観点から問題点と改善提案を報告してください。対象ファイル: src/main.py"
```

**ドキュメントレビューの例（直接実行）:**
```bash
codex exec --profile deep-review \
  -o ./reviews/doc_review_$(date +%Y%m%d_%H%M%S).md \
  "以下のドキュメントをレビューしてください。完全性、正確性、明確性、一貫性の観点から評価し、改善点を提案してください。対象: docs/architecture.md"
```

### Phase 3: レビュー結果の確認

1. **結果ファイルの読み取り**
   - 指定した出力フォルダからレビュー結果を読み込み
   - Markdown形式で構造化された結果を確認

2. **結果の分析と要約**
   - 重要な指摘事項の抽出
   - 優先度による分類
   - アクションアイテムの整理

## Review Types

### 1. コードレビュー

```bash
# 自動的にgpt-5.3-codex + xhighを使用
python3 skills/codex-reviewer/scripts/run_codex_review.py \
  --type code \
  --target src/ \
  --output ./reviews \
  --focus "security,performance,maintainability"
```

**レビュー観点:**
- セキュリティ脆弱性
- パフォーマンス問題
- コードの可読性・保守性
- ベストプラクティス準拠
- エラーハンドリング
- テスト可能性

### 2. ドキュメントレビュー

```bash
# 自動的にgpt-5.3-thinking + xhighを使用（深い推論）
python3 skills/codex-reviewer/scripts/run_codex_review.py \
  --type document \
  --target docs/specification.md \
  --output ./reviews \
  --focus "completeness,accuracy,clarity"
```

**レビュー観点:**
- 完全性（必要な情報の網羅）
- 正確性（技術的な正しさ）
- 明確性（理解しやすさ）
- 一貫性（用語・フォーマット）
- 実装可能性

### 3. 設計レビュー

```bash
# 自動的にgpt-5.3-thinking + xhighを使用（深い推論）
python3 skills/codex-reviewer/scripts/run_codex_review.py \
  --type design \
  --target docs/design/ \
  --output ./reviews \
  --focus "architecture,scalability,patterns"
```

**レビュー観点:**
- アーキテクチャの妥当性
- スケーラビリティ
- デザインパターンの適用
- 結合度・凝集度
- 拡張性・保守性

### 4. テスト計画レビュー

```bash
python3 skills/codex-reviewer/scripts/run_codex_review.py \
  --type test \
  --target tests/ \
  --output ./reviews \
  --focus "coverage,edge-cases,quality"
```

**レビュー観点:**
- テストカバレッジ
- エッジケースの網羅
- テストの独立性
- テストデータの妥当性
- 自動化可能性

## Result Analysis

レビュー結果を確認・分析するには:

```bash
python3 skills/codex-reviewer/scripts/analyze_review.py \
  --input ./reviews/code_review_20251130_120000.md \
  --format summary
```

**分析オプション:**
- `--format summary`: 要約レポート生成
- `--format issues`: 問題点リスト抽出
- `--format actions`: アクションアイテム抽出
- `--format all`: 全形式で出力

## Advanced Configuration

### モデルと推論レベルの選択

| 用途 | 推奨モデル | 推論レベル |
|------|-----------|-----------|
| コードレビュー | gpt-5.3-codex | xhigh |
| テストレビュー | gpt-5.3-codex | xhigh |
| ドキュメントレビュー | gpt-5.3-thinking | xhigh |
| 設計レビュー | gpt-5.3-thinking | xhigh |

### スクリプト内蔵プロファイル

`run_codex_review.py` は以下の内蔵プロファイルを使用します（`~/.codex/config.toml` は参照されません）:

| プロファイル | モデル | 推論レベル | 説明 |
|-------------|--------|-----------|------|
| `deep-review` | gpt-5.3-codex | xhigh | 標準レビュー（推奨） |
| `quick-review` | gpt-5-codex | medium | 軽量レビュー（高速） |

**使用例:**
```bash
# コードレビュー（自動的にgpt-5.3-codex + xhighを使用）
python3 skills/codex-reviewer/scripts/run_codex_review.py --type code --target src/ --output ./reviews

# ドキュメントレビュー（自動的にgpt-5.3-thinking + xhighを使用）
python3 skills/codex-reviewer/scripts/run_codex_review.py --type document --target docs/ --output ./reviews

# 軽量レビュー（高速）
python3 skills/codex-reviewer/scripts/run_codex_review.py --type code --target src/ --output ./reviews --profile quick-review

# モデルと推論レベルを直接指定（オーバーライド）
python3 skills/codex-reviewer/scripts/run_codex_review.py --type code --target src/ --output ./reviews --model gpt-5-codex --reasoning medium
```

### Codex CLI直接使用時のプロファイル例

Codex CLIを直接使用する場合は、以下のプロファイルを `~/.codex/config.toml` に設定できます:

```toml
# ~/.codex/config.toml

# デフォルト設定
model = "gpt-5.3-codex"
model_reasoning_effort = "xhigh"
approval_policy = "on-request"

# 標準レビュー用プロファイル（推奨）
[profiles.deep-review]
model = "gpt-5.3-codex"
model_reasoning_effort = "xhigh"
approval_policy = "never"

# 軽量レビュー用（高速）
[profiles.quick-review]
model = "gpt-5-codex"
model_reasoning_effort = "medium"
approval_policy = "never"
```

## Output

レビュー実行後、以下のファイルが生成されます:

| 出力ファイル | 形式 | 説明 |
|------------|------|------|
| `<type>_review_<target>_<timestamp>.md` | Markdown | Codexによるレビュー結果（重要度別・カテゴリ別の指摘事項） |

**出力例:**
```
reviews/
├── code_review_main_20251130_120000.md
├── document_review_spec_20251130_121500.md
└── design_review_architecture_20251130_123000.md
```

**レビュー結果の構造:**
```markdown
## レビュー結果

### Critical
- **重要度**: Critical
- **カテゴリ**: セキュリティ
- **場所**: src/auth.py:45
- **問題**: SQLインジェクションの脆弱性
- **推奨**: パラメータ化クエリを使用

### High
...
```

**分析結果の形式:**
- `summary`: 要約レポート（重要度別分布、カテゴリ別分布、要対応事項）
- `issues`: 問題点リスト（重要度順に整理）
- `actions`: アクションアイテムリスト（チェックリスト形式）
- `json`: JSON形式（プログラム連携用）
- `all`: 全形式を統合

## Resources

### scripts/
- `skills/codex-reviewer/scripts/run_codex_review.py`: Codex CLIを呼び出してレビューを実行するメインスクリプト
- `skills/codex-reviewer/scripts/analyze_review.py`: レビュー結果を分析・要約するスクリプト

### references/
- `skills/codex-reviewer/references/review_prompts.md`: レビュータイプ別のプロンプトテンプレート
- `skills/codex-reviewer/references/codex_config_guide.md`: Codex CLI設定ガイド

### assets/
- `skills/codex-reviewer/assets/review_report_template.md`: レビュー結果レポートのテンプレート
