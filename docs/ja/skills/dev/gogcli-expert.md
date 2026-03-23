---
layout: default
title: "Gogcli Expert"
grand_parent: 日本語
parent: ソフトウェア開発
nav_order: 19
lang_peer: /en/skills/dev/gogcli-expert/
permalink: /ja/skills/dev/gogcli-expert/
---

# Gogcli Expert
{: .no_toc }

gogcli（gog コマンド）の専門家スキル。Google Workspaceの13サービス（Gmail, Calendar, Drive, Sheets, Docs, Slides, Contacts, Tasks, Chat, Groups, Keep, Classroom, People）をターミナルから操作するGoベースCLIツールの使い方を支援。OAuth2/サービスアカウント認証、マルチアカウント管理、自動化パターンを提供。Use when working with Google Workspace services via CLI, managing Gmail/Calendar/Drive/Sheets, automating Google Workspace tasks, or setting up gogcli authentication.
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/gogcli-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/gogcli-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

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

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

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

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

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

<!-- TODO: 翻訳 -->

---

## 4. 仕組み

<!-- TODO: 翻訳 -->

---

## 5. 使用例

<!-- TODO: 翻訳 -->

---

## 6. 出力の読み方

<!-- TODO: 翻訳 -->

---

## 7. Tips & ベストプラクティス

<!-- TODO: 翻訳 -->

---

## 8. 他スキルとの連携

<!-- TODO: 翻訳 -->

---

## 9. トラブルシューティング

<!-- TODO: 翻訳 -->

---

## 10. リファレンス

**References:**

- `skills/gogcli-expert/references/communication_services.md`
- `skills/gogcli-expert/references/productivity_services.md`
- `skills/gogcli-expert/references/quick_reference.md`
- `skills/gogcli-expert/references/troubleshooting.md`
- `skills/gogcli-expert/references/workspace_admin_services.md`
