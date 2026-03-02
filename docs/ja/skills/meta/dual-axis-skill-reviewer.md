---
layout: default
title: Dual-Axis Skill Reviewer
grand_parent: 日本語
parent: メタ・品質
nav_order: 1
lang_peer: /en/skills/meta/dual-axis-skill-reviewer/
permalink: /ja/skills/meta/dual-axis-skill-reviewer/
---

# Dual-Axis Skill Reviewer
{: .no_toc }

決定論的チェックと LLM ディープレビューによる、再現性のあるスキル品質スコアリング。
{: .fs-6 .fw-300 }

<span class="badge badge-scripts">スクリプト</span> <span class="badge badge-workflow">ワークフロー</span>

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 概要

Dual-Axis Skill Reviewer は、Claude スキルを 2 つの補完的な軸で評価します。

| 軸 | 手法 | チェック内容 |
|:---|:-----|:------------|
| **Auto 軸** | 決定論的 Python スクリプト | 構造、メタデータ、スクリプト、テスト、実行安全性、成果物の有無 |
| **LLM 軸** | AI によるディープレビュー | コンテンツ品質、正確性、リスク、不足ロジック、保守性 |

最終スコアは両軸の加重平均です。90 点未満のスキルには具体的な改善項目リストが付与されます。CI/CD パイプラインでの品質ゲートやスキル PR のマージ前チェックに最適です。

## いつ使うか

- `SKILL.md` を持つ任意のスキルに対して**再現性のある品質スコアリング**が必要
- 最低スコア閾値 (例: 90 以上) で**マージをゲート**したい
- 低スコアスキルの**具体的な改善項目**が必要
- **構造的チェック** (決定論的) と**定性的レビュー** (LLM) の両方が必要
- レビュアーのインストール先とは**別プロジェクト**のスキルをレビューしたい

## 前提条件

- Python 3.9+
- `uv` (推奨) -- インラインメタデータで `pyyaml` 依存を自動解決
- テスト実行には: `uv sync --extra dev` または対象プロジェクトの同等設定
- `dual-axis-skill-reviewer` スキルが `~/.claude/skills/` にコピー済み (または同一プロジェクト内に存在)

Auto 軸に外部 API キーは不要です。LLM 軸は Claude 自体をレビュアーとして使用します。

## 仕組み

レビューは 3 ステップで実行されます。

1. **Auto 軸 + LLM プロンプト生成** -- Python スクリプト (`run_dual_axis_review.py`) がスキルディレクトリをスキャンし、決定論的チェックを実行、5 次元でスコアリングし、オプションで LLM レビュー用プロンプトを生成します。
2. **LLM レビュー** -- Claude が生成されたプロンプトを読み、コンテンツのディープレビューを実行、構造化 JSON レスポンスを生成します。
3. **マージ** -- スクリプトが設定可能な重み (デフォルト 50/50) で Auto と LLM のスコアをマージし、最終レポートを生成します。

### Auto 軸の評価次元

Auto 軸は 5 つの領域を評価します。

- **メタデータ** -- SKILL.md フロントマターの完全性と正確性
- **ワークフローカバレッジ** -- 文書化されたワークフローの有無と品質
- **実行安全性** -- スクリプトのエラーハンドリング、入力バリデーション
- **成果物の有無** -- 必須ディレクトリ (scripts/, references/, assets/)
- **テスト健全性** -- テストファイルの存在とパス状況

ナレッジのみのスキル (スクリプトなし) は、不公平なペナルティを避けるため期待値が調整されます。

### スコアリング

| スコア | 意味 |
|:-------|:-----|
| 90--100 | プロダクション対応、全品質基準を満たす |
| 70--89 | 機能するが特定領域で改善が必要 |
| 70 未満 | マージ前に対処すべき重大なギャップあり |

## 使用例

### 例 1: 単一スキルのクイック品質チェック

```
dual-axis-skill-reviewer で financial-analyst スキルをレビューしてください。
```

Claude が Auto 軸を実行し、LLM レビューを行い、スコアをマージして最終スコアと改善項目を含むレポートを提示します。

### 例 2: 全スキルの一括レビューとスコア閾値チェック

```
このプロジェクトの全スキルに対して dual-axis-skill-reviewer を実行してください。
90 点未満のスキルをフラグしてください。
```

Claude が `skills/*/SKILL.md` を巡回し、各スキルをスコアリング、注意が必要なスキルをハイライトしたサマリーテーブルを生成します。

### 例 3: クロスプロジェクトレビュー

```
~/other-project/ のスキルを dual-axis-skill-reviewer でレビューしてください。
--project-root ~/other-project/ を使い、レポートは ~/other-project/reports/ に保存してください。
```

Claude が `--project-root` フラグで別プロジェクトディレクトリを指定してスクリプトを実行します。

## ヒントとベストプラクティス

- **まず Auto 軸のみ** (`--skip-tests` で高速化) で構造的な評価を行い、その後 LLM レビューに進みましょう。
- **重みを調整** -- 構造的ゲートを厳しくするなら `--auto-weight` を増加、コンテンツの深さを重視するなら `--llm-weight` を増加。
- **`--seed` を使用** -- CI 実行時のランダムスキル選択に再現性を持たせます。
- **生成されたプロンプトを確認** -- LLM ステップ実行前に、何が評価されるかの全コンテキストを確認できます。
- **CI に統合** -- JSON 出力を使用して、スキルを変更する PR に最低スコア閾値を適用しましょう。

## 関連スキル

- [Critical Code Reviewer]({{ '/ja/skills/dev/critical-code-reviewer/' | relative_url }}) -- ソースファイルのマルチペルソナコードレビュー
- [Critical Document Reviewer]({{ '/ja/skills/ops/critical-document-reviewer/' | relative_url }}) -- ドキュメント品質のマルチペルソナレビュー
