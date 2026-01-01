# Critical Code Reviewer

ソースコードを4人の専門家（20年ベテラン、TDDエキスパート、Clean Codeエキスパート、バグハンター）の視点で批判的にレビューします。

> **Tip**: `/critical-review` で自動判別も可能です。ドキュメントレビューには `/critical-document-reviewer` を使用。

## 引数

```
$ARGUMENTS
```

**引数の解釈**:
- ファイルパスが含まれる場合: そのファイルをレビュー対象とする
- ディレクトリパスが含まれる場合: そのディレクトリ内のコードをレビュー対象とする
- 追加の指示がある場合: レビュー時の重点項目として考慮する
- 引数が空の場合: ユーザーにレビュー対象を確認する

**使用例**:
- `/critical-code-reviewer src/main.py` → src/main.py をレビュー
- `/critical-code-reviewer src/` → src/ ディレクトリをレビュー
- `/critical-code-reviewer src/api.py テスト容易性を重点的に` → 指定ファイルをテスト容易性重視でレビュー
- `/critical-code-reviewer` → 対象を確認してからレビュー

## 実行手順

1. **スキル読み込み**: `skills/critical-code-reviewer/SKILL.md` を読み込んでワークフローを理解する

2. **引数の解析とレビュー対象の確認**:
   - 引数からファイルパス/ディレクトリパスを抽出
   - 追加の指示事項があれば抽出
   - 引数が空または不明確な場合は、ユーザーにレビュー対象を確認する

3. **言語の検出**: コードの言語を判定
   - Python の場合: 型ヒント、Pythonic patterns の追加チェック
   - JavaScript/TypeScript の場合: 型安全性、async patterns の追加チェック
   - 該当する場合は `skills/critical-code-reviewer/references/language_specific_checks.md` を参照

4. **並列レビュー実行**: Task ツールで4つのサブエージェントを**並列**起動

   ```
   Task tool を使用して以下を並列実行（1つのメッセージで4つのツールコール）：

   1. code-reviewer-veteran-engineer: 20年ベテランエンジニア視点
      - 設計判断の妥当性
      - アンチパターンの検出
      - 運用・保守性の観点

   2. code-reviewer-tdd-expert: TDDエキスパート視点
      - テスト容易性
      - 依存関係の管理
      - リファクタリング安全性

   3. code-reviewer-clean-code-expert: Clean Codeエキスパート視点
      - 命名の適切さ
      - 関数/クラス設計
      - SOLID原則の遵守

   4. code-reviewer-bug-hunter: バグハンター視点
      - 失敗モード分析（境界条件、null、タイムアウト等）
      - 影響範囲の探索（呼び出し元、後方互換性）
      - 冪等性・並行実行の問題
      - P0/P1優先度付け（壊れる・漏れる・戻せない）
   ```

   各サブエージェントには以下を渡す：
   - レビュー対象コード
   - 言語固有チェックリスト（該当する場合）

5. **結果統合**: 4つのレビュー結果を統合
   - 重複する指摘は統合（複数ペルソナからの指摘として記録）
   - 重大度を付与: Critical / Major / Minor / Info
   - `skills/critical-code-reviewer/assets/code_review_report_template.md` の形式でレポート作成

## 参照リソース

レビュー実行時に以下を参照：
- `skills/critical-code-reviewer/references/persona_definitions.md` - ペルソナ詳細定義
- `skills/critical-code-reviewer/references/code_smell_patterns.md` - コードスメル・アンチパターン
- `skills/critical-code-reviewer/references/review_framework.md` - レビューフレームワーク
- `skills/critical-code-reviewer/references/severity_criteria.md` - 重大度判定基準
- `skills/critical-code-reviewer/references/failure_mode_patterns.md` - 失敗モードパターン集（Bug Hunter用）

## 重要な指示

- **並列実行**: 4つのサブエージェントは必ず並列で起動すること（効率化のため）
- **ultrathink**: 各サブエージェントは ultrathink モードで深い分析を行う
- **言語固有チェック**: Python/JavaScript の場合は追加チェックを適用
- **建設的**: 問題の指摘だけでなく、具体的な改善コード例も示す
- **良い点も認める**: 問題だけでなく、良い設計/コードも指摘する

## 出力

最終的に `Critical Code Review Report` を生成し、以下を含める：
- エグゼクティブサマリー（重大度別件数、コード品質スコア）
- 指摘事項一覧（重大度順、コード例付き）
- ペルソナ別レビュー詳細
- 改善推奨事項のチェックリスト
- 良い点のハイライト

## 既存スキルとの使い分け

| スキル | 目的 | いつ使う |
|--------|------|---------|
| `design-implementation-reviewer` | バグ検出、動作正確性 | PR前のバグ確認 |
| `critical-code-reviewer` | 設計品質、保守性 | コードレビュー、品質向上 |

推奨フロー:
1. まず `design-implementation-reviewer` でバグを検出
2. 次に `critical-code-reviewer` で品質を評価
