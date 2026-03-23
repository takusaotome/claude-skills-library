---
name: critical-code-reviewer
description: |
  4人の異なる専門家ペルソナ（20年ベテランエンジニア、TDDエキスパート、Clean Codeエキスパート、バグハンター）で
  ソースコードを批判的にレビューするスキル。設計判断、テスト容易性、可読性、バグ検出の観点から
  コードの問題を検出し、改善提案を行う。Python/JavaScriptに対しては追加のチェックポイントを適用。
  バグハンターは状態遷移、例外パス、依存関係、非同期競合に特化し、本番環境での問題を事前に検出する。
  Use when reviewing source code from multiple expert perspectives to find design flaws,
  testability issues, code quality problems, and runtime bugs. Triggers: "critical code review",
  "multi-persona code review", "expert code review", "code quality assessment", "find bugs".
---

# Critical Code Reviewer

## When to Use

このスキルは以下の場合に使用します：

- **コードレビュー依頼時**: 「このコードをレビューして」「コードの品質をチェックして」
- **PRレビュー時**: マージ前の包括的なコード品質評価
- **リファクタリング前**: 既存コードの問題点を特定したい場合
- **バグ探索時**: 「このコードにバグがないか確認して」「本番で問題が起きそうな箇所を探して」
- **設計評価時**: コードの設計品質、保守性を評価したい場合

**トリガーワード**: "critical code review", "multi-persona code review", "expert code review",
"code quality assessment", "find bugs", "コードレビュー", "品質チェック"

## Prerequisites

- **Agent tool**: 4つのサブエージェントを並列起動するために必要
- **Read tool**: レビュー対象ファイルの読み込み
- **Grep/Glob tools**: 依存関係の事前チェック（関数内import検出等）

## Overview

このスキルは、ソースコードを4人の異なる専門家の視点から批判的にレビューします：

| Persona | Focus | Key Question |
|---------|-------|--------------|
| **Veteran Engineer** | 設計判断、アンチパターン、長期保守性 | 「これを5年後も保守できるか？」 |
| **TDD Expert** | テスト容易性、依存関係管理、リファクタリング安全性 | 「これを単独でテストできるか？」 |
| **Clean Code Expert** | 命名、可読性、SOLID原則 | 「一目で理解できるか？」 |
| **Bug Hunter** | 状態遷移、例外パス、依存関係、非同期競合 | 「本番で壊れないか？」 |

## Multi-Persona Review Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                    スキル（オーケストレーター）                           │
│  ┌────────────────────────────────────────────────────────────┐      │
│  │ Phase 1: 準備                                               │      │
│  │ - レビュー対象コードの特定                                     │      │
│  │ - 言語の検出（Python/JavaScript の場合は追加チェック）          │      │
│  │ - 依存関係事前チェック（関数内import検出、requirements.txt照合）│      │
│  │ - ペルソナ確認                                               │      │
│  └────────────────────────────────────────────────────────────┘      │
│                              │                                        │
│       ┌──────────────┬───────┴───────┬──────────────┐                │
│       ▼              ▼               ▼              ▼                │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐ ┌──────────┐            │
│  │ Veteran  │ │   TDD    │ │ Clean Code   │ │   Bug    │  並列実行 │
│  │ Engineer │ │  Expert  │ │   Expert     │ │  Hunter  │            │
│  │(20年経験)│ │(和田氏的)│ │ (可読性)     │ │(バグ検出)│            │
│  └──────────┘ └──────────┘ └──────────────┘ └──────────┘            │
│       │              │               │              │                │
│       └──────────────┴───────┬───────┴──────────────┘                │
│                              ▼                                        │
│  ┌────────────────────────────────────────────────────────────┐      │
│  │ Phase 3: 統合                                               │      │
│  │ - 重複排除（複数ペルソナからの同一指摘を統合）                 │      │
│  │ - 重大度付与                                                 │      │
│  │ - 統合レビューレポート生成                                     │      │
│  └────────────────────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────────────────┘
```

## Workflow

### Phase 1: 準備（Preparation）

1. **レビュー対象の特定**
   - ファイル、ディレクトリ、特定の関数/クラス
   - PR全体、特定のコミット範囲

2. **言語の検出**
   - 汎用チェック: すべての言語に適用
   - Python: 追加の型ヒント、Pythonic patterns チェック
   - JavaScript/TypeScript: 追加の型安全性、async patterns チェック

3. **依存関係事前チェック**（Bug Hunter向け）
   - `grep` で関数内importを検出
   - requirements.txt/pyproject.tomlとの照合

4. **コンテキストの収集**（任意）
   - 関連する設計書があれば参照
   - 既存のテストコードがあれば参照

5. **ファイルタイプの確認**
   - `references/file_type_classification.md` を参照してファイルの分類を確認
   - 設定ファイル（Dockerfile, K8s, Terraform 等）も Config tier としてレビュー対象

### Phase 1.5: スケール判定

対象が大規模な場合（500行超 or 5ファイル超）:
- `references/scale_strategy.md` を参照
- ホットスポット抽出 → 重点レビュー の2段階で実行

### Phase 2: 並列レビュー（Parallel Review）

4つのレビューを Agent tool を使って**並列実行**します。

各レビューの Agent prompt 構成:
1. `references/agents/{persona}.md` の全内容（ペルソナプロンプト）
2. レビュー対象コード
3. ペルソナ固有リファレンス（推奨、Token Budget Strategy 参照）

```
Agent tool を使用して4つのレビューを並列実行：

1. references/agents/veteran-engineer.md をプロンプトとして使用
   + 推奨リファレンス: references/code_smell_patterns.md

2. references/agents/tdd-expert.md をプロンプトとして使用

3. references/agents/clean-code-expert.md をプロンプトとして使用

4. references/agents/bug-hunter.md をプロンプトとして使用
   + 推奨リファレンス: references/review_framework.md（検出テクニック部分）
```

**Agent には severity を付けさせない。** 各 Agent は Issue ごとに Impact（影響の説明）を出力する。
Severity の最終判定は Phase 3（統合）で行う。

### Phase 3: 統合（Integration）

1. **指摘事項の収集**
   - 4つのレビュー結果を収集
   - 各指摘事項を構造化

2. **重複排除**
   - 同じ問題を異なる視点で指摘している場合は統合
   - 視点の違いは「関連ペルソナ」として記録

3. **重大度の最終判定**

   `references/severity_criteria.md` を参照し、各 Issue の Impact 記述に基づいて
   Critical / Major / Minor / Info を判定する。

   ※Agent 側では severity を付けない。統合フェーズが authoritative criteria を参照して一貫性を保証する。

4. **部分失敗ハンドリング**

   - 1件以上の Agent が結果を返せば統合レポートを生成する
   - 失敗した Agent はレポートに明記し、該当ペルソナの観点が欠落している旨を注記する
   - 全 Agent 失敗時のみ中断しエラーを報告する

5. **統合レビューレポート生成**
   - assets/code_review_report_template.md を使用

## Differentiation from design-implementation-reviewer

| 観点 | design-implementation-reviewer | critical-code-reviewer |
|------|-------------------------------|----------------------|
| **主な目的** | 実装の正確性検証 | 設計品質 + バグ検出の両方 |
| **アプローチ** | 単一視点、3層フレームワーク | 4ペルソナ並列実行 |
| **主な質問** | 「設計通りに動くか？」 | 「良いコードか？本番で壊れないか？」 |
| **出力** | バグ指摘中心 | 品質改善 + バグ検出の両方 |
| **使用場面** | PR前のバグ確認 | 包括的コードレビュー |

**推奨ワークフロー**:
- `critical-code-reviewer` を使用すれば、品質評価とバグ検出の両方をカバー
- Bug Hunterペルソナが状態遷移、例外パス、依存関係、非同期競合を検出
- より詳細な実装検証が必要な場合は `design-implementation-reviewer` も併用

## Language Support

### 汎用チェック（全言語）
- 設計パターン/アンチパターン
- SOLID原則
- 命名規則
- 関数/クラスの責務分離
- エラーハンドリング

### Python 追加チェック
- 型ヒント（Type Hints）の有無と適切さ
- Pythonic patterns（list comprehension, context manager等）
- 例外処理の適切さ
- `Optional` の適切な使用

### JavaScript/TypeScript 追加チェック
- 型安全性（TypeScript）
- `any` の乱用
- async/await の正しい使用
- Promise の適切なエラーハンドリング
- `this` バインディングの問題

### Language Tier 分類

`references/file_type_classification.md` の Tier 分類を参照:
- **Tier 1** (Python, JS/TS): 詳細チェック（`references/language_specific_checks.md` 適用）
- **Tier 2** (Go, Java, Rust, C/C++): 基本パターンチェック
- **Tier 3** (その他): 汎用チェックのみ
- **Config** (Dockerfile, K8s, Terraform, CI/CD): インフラ/設定固有チェック

## Output Format

レビュー結果は以下の形式で出力：

```markdown
# Critical Code Review Report

## Review Information
- Target: [レビュー対象]
- Languages: [検出された言語]
- Date: [日付]
- Reviewers: Veteran Engineer, TDD Expert, Clean Code Expert, Bug Hunter

## Executive Summary

| Severity | Count |
|----------|-------|
| Critical | X |
| Major | X |
| Minor | X |
| Info | X |

**Overall Assessment**: [総合評価]
**Merge Readiness**: Ready / Conditional / Not Ready

## Findings

### Critical
[指摘事項]

### Major
[指摘事項]

### Minor
[指摘事項]

## Persona-Specific Insights

### Veteran Engineer Perspective
[経験に基づく総評]

### TDD Expert Perspective
[テスト容易性の総評]

### Clean Code Expert Perspective
[可読性の総評]

### Bug Hunter Perspective
[バグ検出の総評]

## Improvement Recommendations
[改善推奨事項のリスト]
```

## Usage Example

```
User: このPythonコードをレビューしてください。
[コード]

Claude:
1. [Phase 1] Python と判定。追加チェックを有効化。
2. [Phase 2] 4つのサブエージェントを並列起動:
   - Veteran Engineer: 設計判断をレビュー
   - TDD Expert: テスト容易性をレビュー
   - Clean Code Expert: 可読性をレビュー
   - Bug Hunter: バグ検出をレビュー
3. [Phase 3] 結果を統合し、レビューレポートを生成。
```

## Token Budget Strategy

### Agent Prompt 構成（優先度順）
1. **必須**: `references/agents/{persona}.md`（ペルソナプロンプト）
2. **必須**: レビュー対象コード
3. **推奨**: ペルソナ固有リファレンス
   - Veteran Engineer → `references/code_smell_patterns.md`
   - Bug Hunter → `references/review_framework.md`（検出テクニック部分）
   - 他ペルソナ → プロンプト内の知識で十分
4. **Agent には渡さない**: `references/severity_criteria.md` → 統合フェーズでのみ使用

### 大規模入力時（scale_strategy 発動時）
- ホットスポットのみ渡す
- ペルソナ固有リファレンスも省略可

## Resources

### References（参照ドキュメント）

| File | Purpose |
|------|---------|
| `references/agents/veteran-engineer.md` | Veteran Engineer ペルソナプロンプト |
| `references/agents/tdd-expert.md` | TDD Expert ペルソナプロンプト |
| `references/agents/clean-code-expert.md` | Clean Code Expert ペルソナプロンプト |
| `references/agents/bug-hunter.md` | Bug Hunter ペルソナプロンプト |
| `references/code_smell_patterns.md` | コードスメル・アンチパターン集 |
| `references/review_framework.md` | 批判的コード分析フレームワーク |
| `references/language_specific_checks.md` | Python/JavaScript固有チェック |
| `references/severity_criteria.md` | 重大度判定基準（統合フェーズ用） |
| `references/file_type_classification.md` | ファイルタイプ分類・Tier定義 |
| `references/scale_strategy.md` | 大規模入力向けスケール戦略 |

### Assets（出力テンプレート）

| File | Purpose |
|------|---------|
| `assets/code_review_report_template.md` | レビューレポートテンプレート |
