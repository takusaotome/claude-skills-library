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

レビューは 3 ステップで実行され、各ステップが前のステップの出力を基にします。

### ステップ 1: Auto 軸 + LLM プロンプト生成

Python スクリプト (`run_dual_axis_review.py`) が対象スキルディレクトリをスキャンし、5 次元の決定論的チェックを実行します。JSON スコアファイルを生成し、`--emit-llm-prompt` が設定されている場合は次のステップ用の Markdown プロンプトファイルも生成します。

デフォルトではスキルをランダムに選択します。`--skill <name>` で固定ターゲットを指定、`--all` でプロジェクト内の全スキルをレビューできます。

### ステップ 2: LLM レビュー

Claude (または他の LLM) が生成されたプロンプトを読み、コンテンツのディープレビューを実行します。出力は `references/llm_review_schema.md` のスキーマに従う構造化 JSON オブジェクトである必要があります。

```json
{
  "score": 85,
  "summary": "1 段落の評価",
  "findings": [
    {
      "severity": "high",
      "path": "skills/example/scripts/main.py",
      "line": 42,
      "message": "エラーハンドリングなしのファイルオープン",
      "improvement": "try/except でラップしエラーをログ出力"
    }
  ]
}
```

Claude Code 内で実行する場合、Claude がオーケストレーターとレビュアーの両方を担当します -- プロンプトを読み、JSON を生成し、マージステップ用に保存します。

### ステップ 3: マージ

スクリプトが設定可能な重み (デフォルト 50/50) で Auto と LLM のスコアをマージします。最終 JSON レポートと人間が読める Markdown レポートを生成します。最終スコアが 90 未満の場合、両軸の改善項目が統合されてリストアップされます。

### Auto 軸: 5 次元スコアリング詳細

Auto 軸は 5 つの領域を評価し、各次元にはスキル品質における重要度を反映した重みが設定されています。

| 次元 | 配点 | 評価内容 |
|:-----|:-----|:---------|
| **メタデータ & ユースケース** | 20 点 | SKILL.md フロントマターの完全性: `name`、`description` フィールドの存在と情報量。Claude が正しくスキルを呼び出すための明確なトリガー条件。 |
| **ワークフローカバレッジ** | 25 点 | 文書化されたワークフローの有無と品質: ステップバイステップのセクション、入出力仕様、具体例。コアセクションの欠落は実使用時の曖昧さを生む。 |
| **実行安全性 & 再現性** | 25 点 | コマンド例が正しい構文を使用、パスが相対パス (ハードコードでない)、スクリプトがエラーを適切にハンドリング、結果が環境間で再現可能。 |
| **サポート成果物** | 10 点 | 必須ディレクトリ (`scripts/`、`references/`、`assets/`) が存在し、意味のあるコンテンツを含む。成果物はスキル品質を支えるが定義はしないため、低めの配点。 |
| **テスト健全性** | 20 点 | `scripts/tests/` 配下にテストファイルが存在し、実行時にパスする。ランタイムの信頼性は重要 -- テストのパスはオートメーションへの信頼を大きく高める。 |

**合計: 100 点。** Auto 軸スコアは全次元スコアの直接合計です。

**ナレッジのみスキルの扱い:** 実行可能スクリプトのないスキル (`scripts/*.py` が存在しない) は `knowledge_only` に分類されます。スクリプト関連チェック (`supporting_artifacts`、`test_health`) が調整され、スクリプト/テストの欠如によるペナルティが不公平にならないようにします。ただし、`When to Use`、`Prerequisites`、ワークフロー構造は引き続き必須です。

### LLM 軸スコアリング

LLM 軸は 0--100 のスケールでスキルをスコアリングし、以下に焦点を当てます。

- **正確性** -- 指示やスクリプトが主張通りに動作するか
- **リスク** -- セキュリティ、データ損失、信頼性のリスクがないか
- **不足ロジック** -- カバーされていないエッジケースやエラーパスがないか
- **保守性** -- スキルの更新、拡張、デバッグが容易か

各検出事項には重要度 (high / medium / low)、影響を受けるファイルと行番号、問題説明、およびアクション可能な改善提案が含まれます。

### 最終スコア計算

```
最終スコア = (Auto スコア x auto_weight) + (LLM スコア x llm_weight)
```

デフォルト重み: `auto_weight = 0.5`、`llm_weight = 0.5`。CLI フラグで調整可能です。

### スコア閾値

| スコア | 意味 | アクション |
|:-------|:-----|:----------|
| 90--100 | プロダクション対応 | マージ安全。全品質基準を満たす |
| 80--89 | 使用可能 | 重点的な改善を推奨 |
| 70--79 | 注目すべきギャップ | 通常使用前に強化が必要 |
| 70 未満 | 高リスク | ドラフトとして扱い、マージ前に修正を優先 |

最終スコアが 90 未満の場合、改善項目はレポート出力に**必須**です。

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

### 例 4: クイックトリアージ用の Auto 軸のみ実行

```
bug-ticket-creator スキルの構造チェックだけ実行してください。
テストと LLM レビューはスキップ -- Auto 軸のみで。
```

Claude が `--skip-tests` を付け `--emit-llm-prompt` なしでスクリプトを実行し、数秒で構造スコアを出力します。

## CI/CD 統合

Dual-Axis Reviewer は自動化パイプラインに統合でき、スキル PR に品質ゲートを適用できます。

### GitHub Actions の例

```yaml
name: Skill Quality Gate
on:
  pull_request:
    paths:
      - 'skills/**'

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Run auto axis review
        run: |
          uv run skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py \
            --project-root . \
            --all \
            --skip-tests \
            --output-dir reports/

      - name: Check minimum score
        run: |
          python3 -c "
          import json, glob, sys
          for f in glob.glob('reports/skill_review_*.json'):
              data = json.load(open(f))
              score = data.get('auto_score', 0)
              name = data.get('skill_name', f)
              print(f'{name}: {score}')
              if score < 70:
                  print(f'FAIL: {name} scored {score} (minimum: 70)')
                  sys.exit(1)
          print('All skills passed minimum threshold.')
          "
```

### 主要な統合パターン

- **PR ゲート (Auto 軸のみ)**: `skills/` を変更する PR ごとに `--all --skip-tests` を実行。高速で決定論的 -- 数秒で完了。
- **夜間フルレビュー**: スケジュールで 3 ステップのフルワークフロー (Auto + LLM + マージ) を実行。`--seed $(date +%j)` で日次の再現性を確保。
- **リリース前監査**: リリースタグ前に両軸で `--all` を実行。全スキルの最低最終スコア 90 を要件とする。
- **自動化用 JSON 出力**: `skill_review_*.json` ファイルをプログラムで解析し、スコアの経時変化を追跡したり PR コメントとして結果を投稿。

## トラブルシューティング

### "No skills found" でスクリプトが失敗する

**症状**: スクリプトがプロジェクト内にスキルが見つからないというエラーで終了する。

**解決策**: `--project-root` が `skills/` サブディレクトリを含むディレクトリを指していることを確認してください。各スキルには `SKILL.md` ファイルが必要です。`ls <project-root>/skills/*/SKILL.md` でパスを確認してください。

### LLM マージがスキーマ検証エラーで失敗する

**症状**: マージステップが LLM レビュー JSON を検証エラーで拒否する。

**解決策**: JSON が要求されるスキーマに正確に従っていることを確認してください。トップレベルに `score` (整数 0--100)、`summary` (文字列)、`findings` (`severity`、`path`、`line`、`message`、`improvement` を持つオブジェクトの配列) が必要です。`line` フィールドは `null` でも構いませんが存在は必須です。JSON を Markdown コードブロックでラップしないでください。

### テストファイルがあるのにテスト健全性スコアが 0

**症状**: テストファイルが存在するにもかかわらず、Auto 軸がテスト健全性を 0 と報告する。

**解決策**: スクリプトは `scripts/tests/test_*.py` に一致するテストファイルを探します。テストファイルがこの命名規則に従い、`scripts/tests/` サブディレクトリ (スキルルートの `tests/` ではなく) に配置されていることを確認してください。また、`uv run pytest skills/<skill-name>/scripts/tests/ -v` で手動実行時にテストがパスすることも確認してください。

## ヒントとベストプラクティス

- **まず Auto 軸のみ** (`--skip-tests` で高速化) で構造的な評価を行い、その後 LLM レビューに進みましょう。
- **重みを調整** -- 構造的ゲートを厳しくするなら `--auto-weight` を増加、コンテンツの深さを重視するなら `--llm-weight` を増加。
- **`--seed` を使用** -- CI 実行時のランダムスキル選択に再現性を持たせます。
- **生成されたプロンプトを確認** -- LLM ステップ実行前に、何が評価されるかの全コンテキストを確認できます。
- **CI に統合** -- JSON 出力を使用して、スキルを変更する PR に最低スコア閾値を適用しましょう。

## 関連スキル

- [Critical Code Reviewer]({{ '/ja/skills/dev/critical-code-reviewer/' | relative_url }}) -- ソースファイルのマルチペルソナコードレビュー
- **Critical Document Reviewer** -- ドキュメント品質のマルチペルソナレビュー
