---
layout: default
title: Production Parity Test Designer
grand_parent: 日本語
parent: メタ・品質
nav_order: 12
lang_peer: /en/skills/meta/production-parity-test-designer/
permalink: /ja/skills/meta/production-parity-test-designer/
---

# Production Parity Test Designer
{: .no_toc }

本番と同じ失敗を本番前に検出するテスト階層を設計する。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/production-parity-test-designer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/production-parity-test-designer){: .btn .fs-5 .mb-4 .mb-md-0 }
<span class="badge badge-workflow">ワークフロー</span>

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 概要

Production Parity Test Designer は、**本番での障害を本番前に検出する**テスト設計スキルです。テスト数を増やすのではなく、**どのテスト階層がどの本番ギャップをカバーすべきか**に集中し、プロキシメトリクス（テストは通るが実際の障害を見逃す）を排除して、PR CIからリリースパッケージングまでの多層防御を構築します。

コア哲学: **テストは本番の障害モードを再現するために存在する。** 本番と同じ方法で失敗できないテストは、偽の安心を提供しているだけです。

## いつ使うか

- PR CIが軽すぎて本番差分を検出できない
- SQLiteとPostgreSQLのようなDB方言差がある
- UIが成功表示するのにDBに書かれていない問題がある
- mockによりruntime import errorが隠れている
- timezone/locale/OS/dependencyの差分が本番で初めて顕在化する
- 「何をunitで、何をsmokeで見るか」が曖昧
- 過去の重大欠陥を再発禁止テストとして構造化したい
- packaging/container buildの整合性を保証したい

## ワークフロー

8ステップでテスト階層を設計します。

### Step 1: 本番差分の棚卸し

開発/CI環境と本番環境の全差分を列挙します。DB方言、OS/コンテナ、依存パッケージのインストール方式、環境変数、timezone/locale、Real vs Mock、シリアライゼーション、パッケージング/デプロイの各カテゴリで差分を文書化します。

### Step 2: 失敗モードの列挙

各本番ギャップに対して具体的な壊れ方を定義します。例: SQLiteでは通るがPostgreSQLで構文エラー、UIが成功表示するがINSERTが暗黙に失敗、`import cv2` がdevでは動くが本番コンテナでネイティブライブラリ不足で失敗。各失敗モードを可視性（サイレント/ラウド）、影響範囲、検出困難度で分類します。

### Step 3: テスト階層への配賦

各失敗モードを最適なテスト階層に割り当てます。

| 階層 | 対象 |
|:-----|:-----|
| **Unit** | 純粋ロジック、境界値、入力検証 |
| **Integration** | 実DB操作、リポジトリ操作、マルチコンポーネント |
| **E2E** | UIアクション → 永続化検証 → ビジネス可視結果 |
| **Smoke** | PR CIでの最低限の本番同等性チェック |
| **Packaging** | インストール、import、ビルド、コンテナイメージ整合性 |
| **Nightly/Heavy** | フル本番同等性スイート、パフォーマンスベースライン |

### Step 4: プロキシメトリクスの排除

偽の安心を提供するテストを特定・修正します。UI表示のみ検証（DBを確認しない）、全外部呼び出しをmock（実依存をテストしない）、カバレッジシアター（行カバレッジは高いが型不一致や境界テストなし）などのパターンを検出します。

### Step 5: PR必須スモークセットの決定

全PRで実行すべき最低限の本番同等性チェックを定義します。ランタイム予算（2-5分を目標）内で、DB方言smoke、import smoke、永続化smoke、timezone smoke、シリアライゼーションsmokeを選定します。

### Step 6: 再発禁止テストバックログ

過去の欠陥と攻撃パターンからリグレッションテストを設計します。各過去障害に対して、exploit/失敗パターン、最小再現シナリオ、期待される防御挙動、回帰スコープを定義します。

### Step 7: パッケージング・依存整合性チェック

アプリケーションが本番同等環境で正しくビルド・インストール・importできることを検証するチェックリストを作成します。lockfileの整合性、クリーンインストール、全top-level importの成功、メインエントリポイントの起動、コンテナイメージの一致を確認します。

### Step 8: 実行コマンドの固定

各実行コンテキスト（ローカル高速、PR CI必須、ナイトリー、ステージングE2E、リリースパッケージング）の名前付きコマンドを定義します。

## 主な出力物

| 成果物 | 内容 |
|:-------|:-----|
| Production Gap Inventory | 開発/CI vs 本番の差分一覧 |
| Test Tier Allocation Matrix | 失敗モード → テスト階層の配賦表 |
| PR Smoke Suite Proposal | PR必須の最低限の本番同等性チェック |
| Adversarial Regression Backlog | 過去欠陥からの再発禁止テスト |
| Packaging / Dependency Integrity Checklist | インストール・import・ビルド検証 |
| Standard Test Command Map | 実行コンテキスト別の固定コマンド |

## リソース一覧

| リソース | 種類 | 目的 |
|:---------|:-----|:-----|
| `references/production_gap_catalog.md` | リファレンス | 本番ギャップの分類体系 |
| `references/test_tier_strategy.md` | リファレンス | テスト階層の責務とトレードオフ |
| `references/adversarial_test_patterns.md` | リファレンス | 攻撃・障害パターンのカタログ |
| `references/persistence_verification_guide.md` | リファレンス | 永続化検証パターン |
| `references/packaging_integrity_guide.md` | リファレンス | パッケージング・依存整合性 |
| `references/timezone_dialect_boundary_guide.md` | リファレンス | timezone・DB方言・locale |
| `assets/test_tier_matrix_template.md` | テンプレート | テスト階層配賦表 |
| `assets/smoke_suite_template.md` | テンプレート | スモークスイート仕様 |
| `assets/adversarial_regression_template.md` | テンプレート | リグレッションバックログ |
| `assets/packaging_checklist_template.md` | テンプレート | パッケージングチェックリスト |
| `assets/command_map_template.md` | テンプレート | コマンドマップ |

## ベストプラクティス

- **本番ギャップ優先、テスト数は二の次** -- 「テストをいくつ書くべきか」ではなく「現在のテストで見えない本番障害は何か」から始める。
- **表示より永続化** -- UIの成功表示を確認するE2Eテストは、必ずDBの行もアサートする。「成功トーストが出た」はテストアサーションとして無効。
- **ランタイム予算の規律** -- PRスモークスイートには2-5分の予算を設定。超過テストはナイトリーに降格し、スキップしない。
- **Mock最小化** -- 自分のDB、自分のファイルストレージ、自分のメッセージキューにmockを使わない。全mockに対応するインテグレーションテストを持つ。
- **CI環境の本番一致** -- CIは本番と同じDBエンジン、同じOSファミリー、同じtimezone設定にする。インメモリ代替ではなくサービスコンテナを使用する。

## 関連スキル

- [TDD Developer]({{ '/ja/skills/dev/tdd-developer/' | relative_url }}) -- テストコードの実装
- [Completion Quality Gate Designer]({{ '/ja/skills/meta/completion-quality-gate-designer/' | relative_url }}) -- 品質ゲートの設計
