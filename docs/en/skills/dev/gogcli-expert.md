---
layout: default
title: "Gogcli Expert"
grand_parent: English
parent: Software Development
nav_order: 19
lang_peer: /ja/skills/dev/gogcli-expert/
permalink: /en/skills/dev/gogcli-expert/
---

# Gogcli Expert
{: .no_toc }

gogcli（gog コマンド）の専門家スキル。Google Workspaceの13サービス（Gmail, Calendar, Drive, Sheets, Docs, Slides, Contacts, Tasks, Chat, Groups, Keep, Classroom, People）をターミナルから操作するGoベースCLIツールの使い方を支援。OAuth2/サービスアカウント認証、マルチアカウント管理、自動化パターンを提供。Use when working with Google Workspace services via CLI, managing Gmail/Calendar/Drive/Sheets, automating Google Workspace tasks, or setting up gogcli authentication.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/gogcli-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/gogcli-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

gogcli（コマンド名: `gog`）は、Google Workspaceの13サービスをターミナルから操作するGoベースのCLIツールです。steipete/gogcli リポジトリで開発されています。

**対応サービス:**

| カテゴリ | サービス |
|---------|---------|
| Communication | Gmail, Calendar, Chat [Workspace only] |
| Productivity | Drive, Sheets, Docs, Slides, Tasks, Keep [Workspace + SA only] |
| Workspace Admin | Groups [Workspace only], Classroom, People, Contacts |
| Utility | Time（UTC/ローカル時刻表示） |

**主要特徴:**
- OAuth2 + サービスアカウント認証
- マルチアカウント・マルチクライアント対応
- `--json` / `--plain` 出力（パイプライン統合に最適）
- OSキーリングまたは暗号化ファイルによる認証情報の安全な保管
- シェル補完（Bash, Zsh, Fish, PowerShell）

---

## 2. Prerequisites

このスキルを使用する前に以下を準備してください:

1. **gogcli のインストール**
   - macOS/Linux: `brew install steipete/tap/gogcli`
   - または GitHub からソースビルド

2. **Google Cloud Console でのセットアップ**
   - Google Cloud プロジェクト（作成済みまたは新規）
   - 必要な API の有効化（Gmail API, Calendar API, Drive API 等）
   - OAuth 同意画面の設定（テストユーザー追加）
   - OAuth2 クライアント ID（デスクトップアプリケーションタイプ）の作成
   - クレデンシャル JSON のダウンロード

3. **初期認証**
   - `gog auth credentials <path-to-json>` でクレデンシャル登録
   - `gog auth add <email>` でアカウント認証

---

## 3. Quick Start

```bash
1. セットアップ
   └─> gog auth credentials ~/client_secret.json
   └─> gog auth add user@gmail.com
   └─> gog auth status  # 認証確認

2. 日常操作
   ├─> Gmail: gog gmail threads / gog gmail send
   ├─> Calendar: gog calendar events --today
   ├─> Drive: gog drive list / gog drive download
   └─> Sheets: gog sheets get <id>

3. 自動化・スクリプト統合
   └─> --json 出力 + jq でパース
   └─> CI/CD: GOG_KEYRING_PASSWORD + --no-input

4. マルチアカウント管理
   └─> gog auth alias set work user@company.com
   └─> gog --account work <command>
```

---

## 4. How It Works

gogcli を使った基本的なワークフロー:

```
1. セットアップ
   └─> gog auth credentials ~/client_secret.json
   └─> gog auth add user@gmail.com
   └─> gog auth status  # 認証確認

2. 日常操作
   ├─> Gmail: gog gmail threads / gog gmail send
   ├─> Calendar: gog calendar events --today
   ├─> Drive: gog drive list / gog drive download
   └─> Sheets: gog sheets get <id>

3. 自動化・スクリプト統合
   └─> --json 出力 + jq でパース
   └─> CI/CD: GOG_KEYRING_PASSWORD + --no-input

4. マルチアカウント管理
   └─> gog auth alias set work user@company.com
   └─> gog --account work <command>
```

---

## 5. Usage Examples

- gogcli（gog コマンド）のインストール・セットアップ方法を知りたい
- Google Workspace サービスをCLIから操作したい
- Gmail の検索・送信・ラベル管理をターミナルで行いたい
- Calendar のイベント管理・空き時間確認をCLIで行いたい
- Drive のファイル操作・権限管理をCLIで自動化したい
- Sheets の読み書き・書式設定をスクリプトで行いたい

---

## 6. Understanding the Output

### Output Formats

```bash
# 人間可読形式（デフォルト）
gog gmail threads

# JSON出力（パイプライン統合に最適）
gog gmail threads --json
gog gmail threads --json | jq '.[] | .subject'

# プレーン出力（TSV形式）
gog gmail threads --plain

# 進捗メッセージは stderr に出力されるため、stdout をクリーンにパイプ可能
gog drive list --json 2>/dev/null | jq '.[] | .name'
```

### Global Flags

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/gogcli-expert/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: troubleshooting.md, workspace_admin_services.md, productivity_services.md.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/dev/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.

---

## 10. Reference

**References:**

- `skills/gogcli-expert/references/communication_services.md`
- `skills/gogcli-expert/references/productivity_services.md`
- `skills/gogcli-expert/references/quick_reference.md`
- `skills/gogcli-expert/references/troubleshooting.md`
- `skills/gogcli-expert/references/workspace_admin_services.md`
