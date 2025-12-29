# Claude Code Windows Installer

[日本語](#日本語) | [English](#english)

---

## 日本語

### 概要

このスクリプトは、Windows環境でClaude Codeを簡単にインストールするための自動化ツールです。非エンジニアの方でもダブルクリックで実行できます。

### 機能

- Git for Windowsのインストール確認
- Claude Codeの自動インストール
- PATH環境変数の自動設定
- インストール結果の確認

### 使い方

1. `install-claude-code.bat` をダブルクリック
2. 画面の指示に従ってください
3. インストール完了後、**新しいターミナル（コマンドプロンプト）を開いて** `claude` を実行

### 前提条件

- Windows 10 (20H2以降) または Windows 11
- インターネット接続

### トラブルシューティング

**Q: 「Gitがインストールされていません」と表示される**

A: Git for Windowsをインストールしてください。スクリプトが自動的にダウンロードページを開きます。インストール時に「Git from the command line and also from 3rd-party software」を選択してください。

**Q: インストール後も `claude` コマンドが認識されない**

A: 新しいターミナルを開いて再試行してください。それでも動作しない場合は、以下のパスを手動で確認してください：
- `%USERPROFILE%\.local\bin\claude.exe`
- `%LOCALAPPDATA%\Programs\claude-code\claude.exe`

---

## English

### Overview

This script is an automation tool for easily installing Claude Code on Windows. Non-technical users can run it with a simple double-click.

### Features

- Git for Windows installation check
- Automatic Claude Code installation
- Automatic PATH environment variable configuration
- Installation verification

### Usage

1. Double-click `install-claude-code.bat`
2. Follow the on-screen instructions
3. After installation completes, **open a NEW terminal (Command Prompt)** and run `claude`

### Prerequisites

- Windows 10 (20H2 or later) or Windows 11
- Internet connection

### Troubleshooting

**Q: "Git is not installed" message appears**

A: Install Git for Windows. The script will automatically open the download page. During installation, select "Git from the command line and also from 3rd-party software".

**Q: `claude` command is not recognized after installation**

A: Open a new terminal and try again. If it still doesn't work, manually check these paths:
- `%USERPROFILE%\.local\bin\claude.exe`
- `%LOCALAPPDATA%\Programs\claude-code\claude.exe`

---

## License

MIT License
