---
name: critical-document-reviewer
description: |
  設計文書、分析レポート、報告書などを批判的な視点で徹底レビューするスキル。
  6つの異なる立場（開発者、PM、顧客、QA、セキュリティ、運用）のペルソナを持つサブエージェントが並列でレビューを実行し、
  「本当にそうか？」「根拠は何か？」「テストできるか？」「運用できるか？」という視点で
  曖昧さ、根拠不足、論理飛躍、テスト不能、セキュリティリスク、運用懸念を検出する。
  Use when reviewing design documents, analysis reports, incident reports, or any document requiring rigorous validation of claims and evidence.
---

# Critical Document Reviewer

## Overview

このスキルは、ドキュメントを複数の視点（6ペルソナ）から批判的にレビューし、以下を検出します：

- **根拠不足**: 主張に対する証拠がない
- **推測混入**: 検証なしの推測が事実として記載
- **論理飛躍**: A→Cの間のBが欠落
- **トレーサビリティ欠如**: 要件や元データとの紐付けがない
- **確証バイアス**: 都合の良い解釈のみ採用
- **テスト不能**: 受入基準が曖昧でテストできない
- **セキュリティリスク**: 認証・認可・データ保護の考慮漏れ
- **運用懸念**: 監視・障害対応・保守性の考慮漏れ

## When to Use

- 設計文書（システム設計書、API設計書、DB設計書など）のレビュー
- 要件定義書・仕様書のレビュー
- 不具合分析レポート・インシデントレポートのレビュー
- 提案書・企画書のレビュー
- セキュリティ設計書のレビュー
- 運用設計書・運用手順書のレビュー
- 重要文書の公開・納品前の最終チェック
- 「本当にこの内容で問題ないか？」と確認したい場面

## Prerequisites

- レビュー対象となるドキュメントファイル
- （推奨）関連文書（元の要件定義書、前工程のドキュメント、ログファイルなど）

## Resources

### References（参照ドキュメント）

| File | Purpose |
|------|---------|
| `references/agents/developer.md` | Developer/Implementer ペルソナプロンプト |
| `references/agents/pm.md` | Project Manager ペルソナプロンプト |
| `references/agents/customer.md` | Customer/Stakeholder ペルソナプロンプト |
| `references/agents/qa.md` | QA/Tester ペルソナプロンプト |
| `references/agents/security.md` | Security/Compliance ペルソナプロンプト |
| `references/agents/ops.md` | Operations/SRE ペルソナプロンプト |
| `references/critical_analysis_framework.md` | 批判的分析の詳細フレームワーク |
| `references/evidence_evaluation_criteria.md` | 証拠評価基準 |
| `references/red_flag_patterns.md` | 危険な表現パターン集 |
| `references/persona_selection_matrix.md` | ペルソナ選定マトリクス |
| `references/severity_criteria.md` | 重大度判定基準（統合フェーズ用） |
| `references/scale_strategy.md` | 大規模入力向けスケール戦略 |

### Assets（出力テンプレート）

| File | Purpose |
|------|---------|
| `assets/review_report_template.md` | レビューレポートテンプレート |

## Multi-Persona Review Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                       スキル（オーケストレーター）                           │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │ Phase 1: 準備                                                   │     │
│  │ - 文書タイプ特定 → 関連文書収集 → ペルソナ選定（3〜6ペルソナ）       │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                    │                                     │
│       ┌────────┬────────┬────────┬┴───────┬────────┬────────┐          │
│       ▼        ▼        ▼        ▼        ▼        ▼                    │
│  ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐          │
│  │Developer││   PM   ││Customer││   QA   ││Security││  Ops   │  並列    │
│  │ 開発者  ││  PM    ││ 顧客   ││ QA担当 ││セキュリティ││ 運用   │  実行    │
│  └────────┘└────────┘└────────┘└────────┘└────────┘└────────┘          │
│       │        │        │        │        │        │                    │
│       └────────┴────────┴────────┴────────┴────────┘                    │
│                                    ▼                                     │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │ Phase 3: 統合                                                   │     │
│  │ - 重複排除 → 重大度付与 → 総合レビューレポート生成                  │     │
│  └────────────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────────┘
```

### 6 Personas Overview

| ペルソナ | 視点 | 主な検出対象 |
|---------|------|-------------|
| **Developer** | 実装可能性 | 技術的曖昧さ、情報欠落 |
| **PM** | プロジェクト管理 | リスク、整合性、依存関係 |
| **Customer** | 要件充足 | 期待値整合、ビジネス価値 |
| **QA** | テスト可能性 | 受入基準不明確、エッジケース欠落 |
| **Security** | セキュリティ | 認証・認可、データ保護、コンプライアンス |
| **Ops** | 運用性 | 監視、障害対応、保守性 |

## Workflow

### Phase 1: 準備（Preparation）

1. **文書タイプの特定**
   - 設計文書（Design Document）
   - 不具合分析レポート（Incident/Bug Analysis Report）
   - 要件定義書（Requirements Document）
   - 提案書（Proposal）
   - その他報告書

2. **関連文書の収集**
   - 設計文書の場合: 元の要件定義書、前工程のドキュメント
   - 不具合分析の場合: ログファイル、データ、証拠となる資料
   - ユーザーに関連文書の有無を確認

3. **ペルソナの選定**（文書タイプに応じて3〜6ペルソナを自動選定）

   `references/persona_selection_matrix.md` の選定マトリクスに従ってペルソナを選定する。

   **ペルソナ選定ガイドライン:**
   - 最低3ペルソナ、最大6ペルソナまで選定可能
   - 文書タイプに応じて適切な組み合わせを選択
   - セキュリティ・運用の考慮が必要な文書は対応ペルソナを必ず含める

### Phase 1.5: スケール判定

対象が大規模な場合（30,000字超 or 見出し30超）:
- `references/scale_strategy.md` を参照
- セクション分割 → 重点レビュー の2段階で実行

### Phase 2: 並列レビュー（Parallel Review）

選定したペルソナのレビューを Agent tool を使って**並列実行**します。

各レビューの Agent prompt 構成:
1. `references/agents/{persona}.md` の全内容（ペルソナプロンプト）
2. レビュー対象文書
3. 関連文書（あれば）

```
Agent tool を使用して選定したペルソナのレビューを並列実行：

例1: 基本レビュー（3ペルソナ）
1. references/agents/developer.md をプロンプトとして使用
2. references/agents/qa.md をプロンプトとして使用
3. references/agents/pm.md をプロンプトとして使用

例2: セキュリティ重視レビュー（5ペルソナ）
1. references/agents/developer.md をプロンプトとして使用
2. references/agents/qa.md をプロンプトとして使用
3. references/agents/security.md をプロンプトとして使用
4. references/agents/ops.md をプロンプトとして使用
5. references/agents/pm.md をプロンプトとして使用
```

**Agent には severity を付けさせない。** 各 Agent は Issue ごとに Impact（影響の説明）を出力する。
Severity の最終判定は Phase 3（統合）で行う。

### Phase 3: 統合（Integration）

Agent からの結果を統合：

1. **指摘事項の収集**
   - 全ペルソナ（3〜6つ）のレビュー結果を収集
   - 各指摘事項を構造化

2. **重複排除**
   - 同じ問題を異なる視点で指摘している場合は統合
   - 視点の違いは「関連ペルソナ」として記録

3. **重大度の最終判定**

   重大度は `references/severity_criteria.md` を参照して統合フェーズで最終判定する。
   各 Issue の Impact 記述に基づいて Critical / Major / Minor / Info を判定する。

   ※Agent 側では severity を付けない。統合フェーズが authoritative criteria を参照して一貫性を保証する。

4. **部分失敗ハンドリング**

   - 1件以上の Agent が結果を返せば統合レポートを生成する
   - 失敗した Agent はレポートに明記し、該当ペルソナの観点が欠落している旨を注記する
   - 全 Agent 失敗時のみ中断しエラーを報告する

5. **総合レビューレポート生成**
   - assets/review_report_template.md を使用

## Persona Definitions

各ペルソナの詳細定義は `references/agents/*.md` を参照。
ペルソナの選定マトリクスは `references/persona_selection_matrix.md` を参照。

## Critical Analysis Framework

各レビュアーは以下のフレームワークを適用します：

### 1. 主張の特定（Claim Identification）

文書内の主張・結論を抽出:
- 明示的な結論（「〜である」「〜とする」）
- 暗黙の前提（言及されていないが仮定されている事項）
- 判断・決定事項

### 2. 根拠の検証（Evidence Validation）

各主張に対して:

```
┌─────────────────────────────────────────────┐
│ 主張: [主張内容]                              │
├─────────────────────────────────────────────┤
│ Q1: これは事実か、解釈か？                    │
│ Q2: 根拠は明示されているか？                  │
│ Q3: その根拠は十分か？                        │
│ Q4: 根拠の出典は信頼できるか？                │
│ Q5: 他の解釈・説明は検討されたか？            │
└─────────────────────────────────────────────┘
```

### 3. 論理の検証（Logic Validation）

- **因果関係の検証**: AがBの原因と言えるか？相関ではないか？
- **論理の連鎖**: A→B→Cの各ステップは妥当か？
- **前提条件**: 暗黙の前提は正しいか？
- **一般化の妥当性**: 特定の事例から一般化できるか？

### 4. 危険な表現パターン（Red Flag Patterns）

`references/red_flag_patterns.md` を参照。推測表現は文脈に応じて評価する。

## Output Format

レビュー結果は以下の形式で出力:

```markdown
# 批判的レビューレポート

## 文書情報
- 対象文書: [文書名]
- 文書タイプ: [タイプ]
- レビュー日: [日付]
- 関連文書: [あれば記載]

## レビューサマリー

| 重大度 | 件数 |
|--------|------|
| Critical | X |
| Major | X |
| Minor | X |
| Info | X |

## 指摘事項一覧

### Critical

#### [CR-001] [タイトル]
- **該当箇所**: [文書内の該当部分]
- **問題**: [何が問題か]
- **根拠評価**: [根拠がない/不十分な理由]
- **関連ペルソナ**: [どの視点から検出されたか]
- **推奨アクション**: [どう修正すべきか]

### Major
...

## ペルソナ別レビュー詳細

### Developer視点
[技術的実装可能性に関する指摘]

### PM視点
[リスク・整合性に関する指摘]

### Customer視点
[要件充足・ビジネス価値に関する指摘]

### QA視点（該当する場合）
[テスト可能性・受入基準に関する指摘]

### Security視点（該当する場合）
[セキュリティ・コンプライアンスに関する指摘]

### Ops視点（該当する場合）
[運用性・障害対応に関する指摘]

## 総合評価

[文書全体の評価と推奨事項]
```

## Token Budget Strategy

### Agent Prompt 構成（優先度順）
1. **必須**: `references/agents/{persona}.md`（ペルソナプロンプト）
2. **必須**: レビュー対象文書
3. **推奨**: 関連文書（あれば）
4. **Agent には渡さない**: `references/severity_criteria.md` → 統合フェーズでのみ使用

### 大規模入力時（scale_strategy 発動時）
- 重点セクションのみ渡す
- 関連文書は要約して渡すか省略可

## Usage Example

### 例1: 設計文書レビュー（基本）

```
User: この設計書をレビューしてください。要件定義書も添付します。

Claude:
1. [Phase 1] 文書を分析し、設計文書と判断。
   必須ペルソナ: Developer, QA
   推奨ペルソナ: Security, Ops → セキュリティ考慮あり、運用設計含むため追加
   → 4ペルソナでレビュー実行
2. [Phase 2] 4つのAgent を並列起動:
   - references/agents/developer.md: 実装可能性視点
   - references/agents/qa.md: テスト可能性視点
   - references/agents/security.md: セキュリティ視点
   - references/agents/ops.md: 運用性視点
3. [Phase 3] 結果を統合し、レビューレポートを生成。
```

### 例2: 要件定義書レビュー

```
User: この要件定義書をレビューしてください。

Claude:
1. [Phase 1] 文書を分析し、要件定義書と判断。
   必須ペルソナ: Developer, PM, Customer
   推奨ペルソナ: QA → テスト可能な要件確認のため追加
   → 4ペルソナでレビュー実行
2. [Phase 2] 4つのAgent を並列起動:
   - references/agents/developer.md: 実装可能性視点
   - references/agents/pm.md: リスク・整合性視点
   - references/agents/customer.md: 要件充足視点
   - references/agents/qa.md: テスト可能性視点
3. [Phase 3] 結果を統合し、レビューレポートを生成。
```

### 例3: セキュリティ設計レビュー（徹底レビュー）

```
User: この認証システムの設計書を徹底レビューしてください。

Claude:
1. [Phase 1] 文書を分析し、セキュリティ設計と判断。
   → 全6ペルソナでレビュー実行（重要文書のため）
2. [Phase 2] 6つのAgent を並列起動:
   - references/agents/developer.md
   - references/agents/pm.md
   - references/agents/customer.md
   - references/agents/qa.md
   - references/agents/security.md
   - references/agents/ops.md
3. [Phase 3] 結果を統合し、レビューレポートを生成。
```
