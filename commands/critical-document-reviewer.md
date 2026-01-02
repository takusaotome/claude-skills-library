# Critical Document Reviewer

設計文書、分析レポート、報告書などを6人の専門家（Developer, PM, Customer, QA, Security, Ops）の視点で批判的にレビューします。

> **Tip**: `/critical-review` で自動判別も可能です。コードレビューには `/critical-code-reviewer` を使用。

## 引数

```
$ARGUMENTS
```

**引数の解釈**:
- ファイルパスが含まれる場合: そのファイルをレビュー対象とする
- 複数のパスがある場合: 最初のパスがレビュー対象、以降は関連文書として扱う
- 追加の指示がある場合: レビュー時の重点項目として考慮する
- 引数が空の場合: ユーザーにレビュー対象を確認する

**使用例**:
- `/critical-document-reviewer docs/design.md` → design.md をレビュー
- `/critical-document-reviewer docs/design.md docs/requirements.md` → design.md をレビュー、requirements.md を関連文書として参照
- `/critical-document-reviewer docs/analysis.md 根拠の妥当性を重点的に` → 根拠重視でレビュー
- `/critical-document-reviewer` → 対象を確認してからレビュー

## 利用可能なペルソナ（6種類）

| ペルソナ | 視点 | 適した文書 |
|---------|------|-----------|
| **Developer** | 実装者視点：技術的正確性、実装可能性 | 設計書、技術仕様書 |
| **PM** | プロジェクト視点：リスク、整合性、実現性 | 計画書、提案書、要件定義 |
| **Customer** | 顧客視点：要件充足、ビジネス価値 | 提案書、報告書、要件定義 |
| **QA** | 品質保証視点：テスト可能性、受入基準 | 設計書、要件定義、仕様書 |
| **Security** | セキュリティ視点：脆弱性、コンプライアンス | セキュリティ設計、認証設計 |
| **Ops** | 運用視点：運用準備度、障害対応 | 運用設計、インフラ設計 |

## 実行手順

1. **スキル読み込み**: `skills/critical-document-reviewer/SKILL.md` を読み込んでワークフローを理解する

2. **引数の解析とレビュー対象の確認**:
   - 引数からファイルパスを抽出（最初のパスがレビュー対象、以降は関連文書）
   - 追加の指示事項があれば抽出
   - 引数が空または不明確な場合は、ユーザーにレビュー対象を確認する

3. **文書タイプの特定とペルソナ選択**: 文書の種類に応じて適切なペルソナを選択

   | 文書タイプ | 推奨ペルソナ |
   |-----------|-------------|
   | 設計文書（一般） | Developer, QA, PM |
   | セキュリティ設計 | Developer, Security, Ops |
   | インフラ/運用設計 | Developer, Ops, Security |
   | 要件定義書 | Developer, PM, Customer |
   | 提案書/企画書 | PM, Customer, Developer |
   | 不具合分析レポート | Developer, QA, PM |
   | その他 | Developer, PM, Customer（デフォルト） |

4. **並列レビュー実行**: Task ツールでサブエージェントを**並列**起動

   ```
   Task tool を使用して以下を並列実行（文書タイプに応じて3-6エージェント）：

   - document-reviewer-developer: 開発メンバー/実装者視点
   - document-reviewer-pm: PM視点
   - document-reviewer-customer: お客様/ステークホルダー視点
   - document-reviewer-qa: QA/テスター視点
   - document-reviewer-security: セキュリティ/コンプライアンス視点
   - document-reviewer-ops: 運用/SRE視点

   各サブエージェントには以下を渡す：
   - レビュー対象文書の内容
   - 関連文書の内容（あれば）
   - ペルソナに応じた指示
   ```

5. **結果統合**: レビュー結果を統合
   - 重複する指摘は統合（複数ペルソナからの指摘として記録）
   - 重大度を付与: Critical / Major / Minor / Info
   - `skills/critical-document-reviewer/assets/review_report_template.md` の形式でレポート作成

## 参照リソース

レビュー実行時に以下を参照：
- `skills/critical-document-reviewer/references/critical_analysis_framework.md` - 批判的分析フレームワーク
- `skills/critical-document-reviewer/references/evidence_evaluation_criteria.md` - 根拠評価基準
- `skills/critical-document-reviewer/references/persona_definitions.md` - ペルソナ詳細定義
- `skills/critical-document-reviewer/references/red_flag_patterns.md` - 危険表現パターン

## 重要な指示

- **並列実行**: サブエージェントは必ず並列で起動すること（効率化のため）
- **ultrathink**: 各サブエージェントは ultrathink モードで深い分析を行う
- **ペルソナ選択**: 文書タイプに応じて最適な3-6ペルソナを選択
- **根拠重視**: 「〜と思われる」「おそらく」などの推測表現は必ず指摘
- **建設的**: 問題の指摘だけでなく、改善の方向性も示す

## 出力

最終的に `批判的レビューレポート` を生成し、以下を含める：
- エグゼクティブサマリー（重大度別件数、総合評価）
- 指摘事項一覧（重大度順）
- ペルソナ別レビュー詳細
- 推奨アクション一覧
