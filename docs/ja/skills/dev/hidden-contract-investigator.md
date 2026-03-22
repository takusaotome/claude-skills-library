---
layout: default
title: Hidden Contract Investigator
grand_parent: 日本語
parent: ソフトウェア開発
nav_order: 10
lang_peer: /en/skills/dev/hidden-contract-investigator/
permalink: /ja/skills/dev/hidden-contract-investigator/
---

# Hidden Contract Investigator
{: .no_toc }

既存コードの暗黙契約を抽出し、再利用リスクを可視化する。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/hidden-contract-investigator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/hidden-contract-investigator){: .btn .fs-5 .mb-4 .mb-md-0 }
<span class="badge badge-workflow">ワークフロー</span>

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 概要

Hidden Contract Investigator は、既存コードを再利用する前に**暗黙の契約**を体系的に抽出するスキルです。関数名やコメント、型注釈を額面通りに信用せず、実際のコードパスを追跡して「本当の戻り値」「隠れた副作用」「暗黙の前提条件」「環境依存の挙動」を明らかにします。

多くの本番障害は新規コードのバグではなく、**再利用コードの実際の挙動を誤解したこと**が原因です。`keepTwoDecimal()` がカンマ付き文字列を返す、`isValid()` が副作用を持つ、`getUser()` がキャッシュの古いデータを返す -- こうした暗黙契約がインテグレーション障害の真因です。

## いつ使うか

- 既存の関数・モジュール・サービスを新機能で再利用する前に
- レガシーコードの名前やコメントが信用できないとき
- 実際の戻り値の型、副作用、例外パスをインテグレーション前に把握したいとき
- 既存コード資産をそのまま再利用して安全かどうか評価したいとき
- 重要なインテグレーションポイントにコントラクトテストを準備したいとき
- 不慣れなコードベースにオンボーディングし、実際の挙動を理解したいとき

## ワークフロー

6段階のワークフローで暗黙契約を調査します。

### 1. 対象特定

再利用候補を特定し、粒度（単一関数、クラス、サービス境界、DB永続化境界、外部API呼び出しなど）を決定します。呼び出し元の把握、最終更新日、テスト有無を記録し、調査優先順位を設定します。

### 2. 見た目の契約記録

名前・ドキュメント・型注釈・呼び出し元の利用パターンから「表面的に約束されている契約」を記録します。この段階ではすべてを **UNVERIFIED** とマークし、何も信用しません。

### 3. 実際の契約抽出

実装コードを読み込み、実際の挙動を抽出します。戻り値の実際の型やフォーマット、副作用（DB書き込み、キャッシュ更新、イベント発火）、暗黙の前提条件（呼び出し順序、初期化状態）、例外パス、環境依存の挙動を調査します。

### 4. 不一致分類

表面的な契約と実際の契約を比較し、6カテゴリで不一致を分類します。

| カテゴリ | 説明 | 例 |
|:---------|:-----|:---|
| **命名不一致** | 名前が示す挙動と実際が異なる | `keepTwoDecimal()` がカンマ付き文字列を返す |
| **型不一致** | 戻り値/引数型が期待と異なる | `float` 注釈だが実際は `str` を返す |
| **スコープ不一致** | 同名の識別子が別スコープに存在 | モジュール変数と関数内変数が混同される |
| **状態依存** | 外部のミュータブルな状態に依存 | グローバルキャッシュの内容で結果が変わる |
| **環境依存** | 環境によって挙動が変わる | dev (SQLite) では動くが prod (PostgreSQL) で失敗 |
| **隠れた副作用** | ドキュメントにない書き込み・変更 | `calculate_total()` がDBレコードを更新する |

各不一致に重大度・発生可能性・影響範囲を付与します。

### 5. 再利用可否判定

5段階の再利用分類を適用します。

| レベル | 判定 | 意味 |
|:-------|:-----|:-----|
| **A** | そのまま再利用 | 契約一致、挙動確認済み |
| **B** | ラッパー付き再利用 | コアロジックは正しいがインターフェース適合が必要 |
| **C** | アダプター付き再利用 | インターフェース不一致が大きいがロジックは健全 |
| **D** | コントラクトテスト後に判断 | 挙動が不確実、検証が先 |
| **E** | 再利用不可/再設計 | 根本的な不一致または許容不能なリスク |

### 6. 検証設計

重大な不一致に対してコントラクトテストを設計します。最小テストケース、境界データセット、テスト失敗が意味する契約違反、回帰防止価値を明確にします。

## 主な出力物

| 成果物 | 内容 |
|:-------|:-----|
| 暗黙契約シート | 表面的契約 vs 実際の契約を証拠付きで記録 |
| 再利用リスクレジスタ | 再利用候補ごとのリスク評価 |
| コントラクトテスト案 | 重要な契約を固定するテスト設計 |
| 採用推奨 | ガードレールと前提条件付きの再利用判定 |

## リソース一覧

| リソース | 種類 | 目的 |
|:---------|:-----|:-----|
| `references/contract_extraction_guide.md` | リファレンス | 抽出手法、証拠優先順位 |
| `references/hidden_spec_patterns.md` | リファレンス | 不一致パターンのカタログ |
| `references/runtime_boundary_checklist.md` | リファレンス | 境界別チェックリスト |
| `references/reuse_risk_classification.md` | リファレンス | 5段階再利用分類フレームワーク |
| `references/environment_behavior_guide.md` | リファレンス | 環境依存挙動パターン |
| `assets/implicit_contract_sheet_template.md` | テンプレート | 暗黙契約シート |
| `assets/reuse_risk_register_template.md` | テンプレート | リスクレジスタ |
| `assets/contract_test_idea_template.md` | テンプレート | テスト設計 |
| `assets/adoption_recommendation_template.md` | テンプレート | 採用推奨 |

## ベストプラクティス

- **名前よりも挙動を信じる** -- 関数名やコメントは実装からドリフトする。実装コードが唯一の真実の源泉。
- **テストを最初に読む** -- テストのアサーションは機械的に検証された契約であり、コメントよりも信頼度が高い。
- **呼び出し元をコメントより先に読む** -- 既存呼び出し元の利用パターンが実際の契約を最も確実に示す。
- **境界にこそ危険な暗黙契約がある** -- 関数、モジュール、サービス、DB、シリアライゼーションの境界でデータが越境するたびに契約がシフトしうる。
- **すべての重大な不一致にコントラクトテストを** -- コントラクトテストはユニットテストではなく、インターフェースの約束を検証するもの。

## 関連スキル

- [Critical Code Reviewer]({{ '/ja/skills/dev/critical-code-reviewer/' | relative_url }}) -- 既に書かれたコードのレビュー
- [TDD Developer]({{ '/ja/skills/dev/tdd-developer/' | relative_url }}) -- コントラクトテストの実装
