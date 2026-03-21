---
layout: default
title: Cross Module Consistency Auditor
grand_parent: 日本語
parent: メタ・品質
nav_order: 11
lang_peer: /en/skills/meta/cross-module-consistency-auditor/
permalink: /ja/skills/meta/cross-module-consistency-auditor/
---

# Cross Module Consistency Auditor
{: .no_toc }

変更が波及する全モジュール・全フローの横断整合性を監査する。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>
<span class="badge badge-workflow">ワークフロー</span>

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 概要

Cross Module Consistency Auditor は、単一の変更が複数のモジュール・フロー・レポート・API・コピペ実装に波及する際の**横断整合性**を監査するスキルです。変更の影響範囲をマッピングし、全タッチポイントで保持すべき整合性ルールを定義し、コピペコードの効率的なレビュー戦略を策定します。

このスキルが防ぐ欠陥クラス: 「修正は1箇所で正しく適用されたが、他の箇所で漏れた、または不整合に適用された」-- 集計不一致、符号反転バグ、レポートとドリルダウンの食い違い、不完全な逆フロー実装の根本原因です。

## いつ使うか

- 仕様変更が複数の画面・レポート・API・バッチジョブに影響する
- 同一ロジックを複数フロー（例: 6種類の取引タイプ）に複製する必要がある
- 返金・取消・修正が符号反転や逆仕訳を必要とする
- レポートの合計とドリルダウンの合計が一致しなければならない
- 正規実装がコピーされた複数箇所の効率的なレビュー戦略が必要
- DBスキーマ変更がビュー、ストアドプロシージャ、API、UIに波及する
- 状態遷移ルールが全エントリポイントで一貫して適用されているか確認したい
- 税計算や端数処理が全計算パスで同一であることを保証したい

## ワークフロー

6段階で横断整合性を監査します。

### 1. 変更核定義

変更の最小単位と正規表現（source of truth）を特定します。変更の内容（What）、正規実装の場所（Where）、ビジネス要件（Why）、全箇所で保持すべき不変条件（Invariant）を文書化します。複合的な変更は分解して個別に処理します。

### 2. 影響レンズ適用

8つの影響レンズで影響範囲を体系的に展開します。

| レンズ | 対象 |
|:-------|:-----|
| 入力フロー | フォーム、APIエンドポイント、ファイルインポート |
| 永続化 | DB書き込み、キャッシュ更新、監査ログ |
| 集計 | 合計、グルーピング、ロールアップ、マテリアライズドビュー |
| 表示/レポート | UI画面、ダッシュボード、PDF、Excel、メール |
| API/エクスポート | REST/GraphQLレスポンス、ファイルエクスポート |
| 逆フロー | 返金、取消、削除、修正、逆仕訳 |
| 権限/可視性 | ロールベースアクセス、テナント分離 |
| 下流ジョブ | バッチ処理、同期ジョブ、外部連携 |

### 3. Impact Map作成

レンズ分析から構造化されたImpact Mapを作成します。影響モジュール、影響出力、影響テスト、影響ドキュメントを網羅し、テストカバレッジのないモジュールや不確実な影響を明示します。

### 4. Consistency Rules定義

全影響モジュールで保持すべき整合性ルールを定義します。集計合計、状態遷移、符号反転、税/端数処理、可視性/権限、命名/定数、レポートvsドリルダウンの一致などのカテゴリで、ルール x モジュールのマトリクスを作成し、各セルをPASS/FAIL/NOT TESTED/NOT APPLICABLEで評価します。

### 5. Copy Propagationレビュー戦略

コピペ実装の効率的なレビュー計画を作成します。正規実装（canonical）にフルレビューを実施し、他のコピーは正規実装との差分レビューのみ行います。許容される差異（エンティティタイプ、フィールド名）と同一でなければならない部分（計算式、バリデーション、符号処理）を明確に分離します。コピー数が3を超え許容差異が最小の場合、共通モジュールへの抽出を推奨します。

### 6. テスト観点変換

整合性ルールをテスト可能なチェックリストに変換します。クロスモジュールアサーション、合計照合、符号反転チェック、レポートvsドリルダウン一致、逆フロー対称性をUnit/Integration/E2E/Manualの各層に割り当てます。

## 主な出力物

| 成果物 | 内容 |
|:-------|:-----|
| Change Impact Map | 変更核から影響モジュール・出力・テスト・文書への可視化 |
| Cross-Module Consistency Matrix | ルール x モジュールのグリッド（期待値・現状・ギャップ） |
| Copy Propagation Review Plan | 正規レビュー + 差分レビューの効率的戦略 |
| Cross-Module Test Checklist | 整合性ルールをテスト可能なアサーションに変換 |
| Open Questions / Missing Modules List | 未解決事項と影響が不確実なモジュール |

## リソース一覧

| リソース | 種類 | 目的 |
|:---------|:-----|:-----|
| `references/change_impact_analysis_guide.md` | リファレンス | 影響伝播パス追跡技法 |
| `references/consistency_rule_catalog.md` | リファレンス | 整合性ルールカテゴリのカタログ |
| `references/copy_propagation_strategy.md` | リファレンス | 正規レビュー・差分レビュー戦略 |
| `references/aggregation_reconciliation_guide.md` | リファレンス | 合計/小計/ドリルダウン照合ルール |
| `references/reverse_flow_checklist.md` | リファレンス | 逆フローの対称性チェックリスト |
| `assets/impact_map_template.md` | テンプレート | Impact Map |
| `assets/consistency_matrix_template.md` | テンプレート | 整合性マトリクス |
| `assets/copy_propagation_review_template.md` | テンプレート | Copy Propagationレビュー計画 |
| `assets/cross_module_test_checklist_template.md` | テンプレート | テストチェックリスト |

## ベストプラクティス

- **Source of Truthの規律** -- あらゆるロジックにただ1つの正規実装を。コピーは文書化し追跡する。コピー数が3を超えたら共通モジュールへの抽出を推奨。
- **深さよりも網羅性** -- 1モジュールの深い分析よりも全影響モジュールの特定が重要。8つの影響レンズを「たぶん関係ない」と省略しない。
- **逆フローは省略不可** -- データを生成する全正フローに逆フローを特定する。逆フローがなければギャップとして記録。正フローと同等のリガーでテストする。
- **整合性ルールはテスト可能に** -- Pass/Failアサーションとして表現できない整合性ルールは曖昧すぎる。具体的なモジュール・フィールド・期待値を参照すること。

## 関連スキル

- [Critical Code Reviewer]({{ '/ja/skills/dev/critical-code-reviewer/' | relative_url }}) -- 単一モジュールのコード品質レビュー
- [Hidden Contract Investigator]({{ '/ja/skills/dev/hidden-contract-investigator/' | relative_url }}) -- 既存コードの暗黙契約調査
