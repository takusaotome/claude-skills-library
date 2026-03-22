---
layout: default
title: Safe By Default Architect
grand_parent: 日本語
parent: ソフトウェア開発
nav_order: 11
lang_peer: /en/skills/dev/safe-by-default-architect/
permalink: /ja/skills/dev/safe-by-default-architect/
---

# Safe By Default Architect
{: .no_toc }

再発する危険パターンを安全デフォルト設計と強制ルールに変換する。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/safe-by-default-architect.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/safe-by-default-architect){: .btn .fs-5 .mb-4 .mb-md-0 }
<span class="badge badge-workflow">ワークフロー</span>

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 概要

Safe By Default Architect は、繰り返し発生する危険な実装パターンを**安全なアーキテクチャデフォルト**と**強制可能な標準**に変換するスキルです。レビューで危険コードを見つけるのではなく、**危険コードを書きにくくする設計**を作ります。

コア哲学: **開発者が事故で危険なコードを書けるなら、アーキテクチャが失敗している。** 安全な方法が最も簡単な方法になるように設計し、危険な方法には意図的な努力が必要になるようにします。

## いつ使うか

- 同じ種類の欠陥が複数のPRやサービスで繰り返し発生している
- 生SQL、オプトイン認可、直接パス構築がコントローラ層に存在する
- クロスカッティング関心事（認証、ファイルI/O、日時処理）の共通サービス層がない
- RCA結果を強制可能なコーディング標準に変換したい
- 静的解析ルール（lint/semgrep/カスタムチェック）を設計する必要がある
- 「禁止パターン一覧」に承認された代替案を対にしたい
- ADR（アーキテクチャ決定記録）で安全デフォルトを文書化したい
- 新規プロジェクトで最初から安全基盤を構築したい

## ワークフロー

6段階のワークフローで安全デフォルト設計を進めます。

### 1. 再発パターン集約

RCAレポート、バグチケット、レビュー所見、セキュリティスキャン結果から危険パターンを収集・統合します。パターン名、発生頻度、実際のコード例、影響コンポーネントを記録し、重複を排除して10-30件の独立パターンに整理します。

### 2. 危険理由分類

各パターンを脅威メカニズムで分類します。

| カテゴリ | 説明 |
|:---------|:-----|
| **注入/バイパス/走査** | 攻撃者制御の入力がセンシティブな操作に到達 |
| **サイレント破壊** | エラーや通知なしにデータが変更・消失 |
| **環境乖離** | dev/staging/production間で挙動が異なる |
| **隠れ依存** | 変更時に壊れる暗黙的結合 |
| **ヒューマンエラー増幅** | ミスを容易にし、回復を困難にする設計 |
| **検証不能** | テストだけでは正しさを確認できない |

`頻度 x 影響範囲 x 検出困難度` でランキングします。

### 3. 標準パターン定義

各禁止パターンに対して承認された安全な代替パターンを定義します。禁止事項、承認パターン、必要な抽象化（共通層・ラッパー）、最低限のコントラクトテスト、静的ルール候補、レビューチェックポイントを文書化します。

### 4. 安全デフォルト決定

プロジェクト全体の安全デフォルトを確立します。

| 領域 | デフォルト |
|:-----|:---------|
| クエリ構築 | ORM/パラメータ化クエリのみ、生SQL禁止 |
| 認可 | deny-by-default、全エンドポイントに明示的許可が必要 |
| ファイル操作 | サービス層抽象化のみ、直接パス構築禁止 |
| 永続化確認 | DB保存確認後にのみUI成功表示 |
| 日時処理 | 永続化境界でUTC-aware正規化 |
| 依存性ロード | 明示的インジェクション、暗黙的サービスロケーター禁止 |

各デフォルトにエスケープハッチ（正当な理由で上書きする方法）と強制メカニズムを定義します。

### 5. 共通層+例外条件設計

安全デフォルトを実現する共通インフラを設計し、例外ポリシーを定義します。例外はレビュー必要（ピアレビューで可）、承認必要（テックリード/セキュリティ署名）、禁止（例外不可）の3段階に分類されます。

### 6. ルール運用化

標準を強制可能な運用ルールに変換します。lint/semgrepルール候補、コーディング標準エントリ、レビューチェックリスト追補を作成し、ロールアウト戦略（Warning -> Error -> 全体強制）を計画します。

## 主な出力物

| 成果物 | 内容 |
|:-------|:-----|
| 安全パターンカタログ | カテゴリ別の承認パターン |
| 禁止パターン一覧 | 危険分類と代替案付きアンチパターン |
| 共通層設計 | 共有サービスと抽象化の推奨 |
| 静的ルール候補一覧 | lint/semgrepルール提案と誤検出評価 |
| 例外処理ルール | 逸脱の承認条件と手続き |
| レビューチェックリスト追補 | 既存レビューチェックリストへの追加項目 |

## リソース一覧

| リソース | 種類 | 目的 |
|:---------|:-----|:-----|
| `references/safe_pattern_catalog.md` | リファレンス | カテゴリ別安全パターン |
| `references/forbidden_patterns.md` | リファレンス | 禁止パターンと危険分類 |
| `references/boundary_hardening_guide.md` | リファレンス | 境界別強化テクニック |
| `references/static_rule_design_guide.md` | リファレンス | 静的解析ルール設計 |
| `references/exception_policy.md` | リファレンス | 例外条件と承認レベル |
| `assets/safe_standard_template.md` | テンプレート | ルール別ドキュメント |
| `assets/forbidden_to_safe_mapping_template.md` | テンプレート | 禁止→安全マッピング表 |
| `assets/static_rule_candidate_template.md` | テンプレート | 静的解析ルール仕様 |
| `assets/architecture_decision_record_template.md` | テンプレート | ADR |

## ベストプラクティス

- **安全な方法を最も簡単な方法にする** -- 安全パターンが危険パターンよりコード量や手間がかかるなら、採用は失敗する。ラッパーや抽象化を便利に設計すること。
- **非推奨ではなく禁止** -- 「ORMを推奨」は無視される。「生SQLはCIで失敗する」は強制される。提案ではなく強制メカニズムを使うこと。
- **全ての禁止に代替を対にする** -- 代替案のない禁止リストはフラストレーションと回避策を生む。
- **段階的に導入** -- 最も頻度・影響度の高い3-5ルールから開始し、Warning -> Error -> 全体強制と段階的にロールアウト。
- **例外は健全** -- 例外ゼロは通常ルールが緩すぎることを意味する。例外にはコード内の正当化コメントとADRを必須とする。

## 関連スキル

- [Critical Code Reviewer]({{ '/ja/skills/dev/critical-code-reviewer/' | relative_url }}) -- 標準に対する既存コードのレビュー
- [Hidden Contract Investigator]({{ '/ja/skills/dev/hidden-contract-investigator/' | relative_url }}) -- 既存コードの暗黙契約調査
