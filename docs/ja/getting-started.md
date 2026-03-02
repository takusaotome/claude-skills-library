---
layout: default
title: はじめに
parent: 日本語
nav_order: 1
lang_peer: /en/getting-started/
permalink: /ja/getting-started/
---

# はじめに
{: .no_toc }

数分で Claude Skills をインストールして使い始められます。
{: .fs-6 .fw-300 }

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 前提条件

{: .prerequisite }
> - **Claude Code CLI** がインストール・認証済みであること（[インストールガイド](https://docs.anthropic.com/en/docs/claude-code)）
> - `bash` または `zsh` が使えるターミナル
> - Git（リポジトリのクローン用）

---

## 1. リポジトリをクローン

```bash
git clone https://github.com/takusaotome/claude-skills-library.git
cd claude-skills-library
```

---

## 2. スキルをインストール

スキルディレクトリを Claude のスキルフォルダにコピーします:

```bash
cp -r ./skills/critical-code-reviewer ~/.claude/skills/
```

上記は **critical-code-reviewer** スキルのインストール例です。スキル名を変更すれば、[スキル一覧]({{ '/ja/skill-catalog/' | relative_url }})にある任意のスキルをインストールできます。

{: .warning }
> スキルディレクトリを `~/.claude/commands/` に配置**しないでください**。このフォルダは `.md` スラッシュコマンドファイル専用です。

---

## 3. インストールの確認

`SKILL.md` ファイルが存在することを確認します:

```bash
ls ~/.claude/skills/critical-code-reviewer/SKILL.md
```

---

## 4. スキルを使う

インストール後、Claude Code はスキルを**自動検出**し、コンテキストに合致した場面で適用します。例:

```
> この Python ファイルのバグとコード品質をレビューして。
```

Claude はコードレビューのコンテキストを認識し、`critical-code-reviewer` スキルを起動します。バグハンティング、クリーンコード、TDD、アーキテクチャの 4 つの視点からマルチペルソナレビューを実行します。

---

## 複数スキルの一括インストール

```bash
for skill in critical-code-reviewer tdd-developer data-scientist markdown-to-pdf; do
  cp -r ./skills/$skill ~/.claude/skills/
done
```

---

## スキルのアンインストール

スキルディレクトリを削除するだけです:

```bash
rm -rf ~/.claude/skills/critical-code-reviewer
```

---

## スキルの構造

すべてのスキルは一貫した 3 層構造に従います:

```
skill-name/
├── SKILL.md        # メインドキュメント（メタデータ + ワークフロー）
├── scripts/        # 自動化スクリプト（Python/Bash）
├── references/     # コンテキストに読み込む方法論ガイド
└── assets/         # 出力生成に使うテンプレート
```

- **SKILL.md** -- エントリポイント。YAML フロントマターでスキルの起動条件を定義し、詳細なワークフローを記述します。
- **scripts/** -- Claude が実行できる自動化コード（例: `auto_eda.py`、`project_health_check.py`）。
- **references/** -- Claude が推論の根拠として読み込むドメイン知識ドキュメント。
- **assets/** -- Claude が出力生成時に使用するテンプレートとボイラープレート。

---

## 次のステップ

- [スキル一覧]({{ '/ja/skill-catalog/' | relative_url }})で使えるスキルを探す
- 個別スキルのガイドページで詳細な使い方を確認する
- 独自スキルの開発に貢献する -- リポジトリ README に開発ガイドラインがあります
