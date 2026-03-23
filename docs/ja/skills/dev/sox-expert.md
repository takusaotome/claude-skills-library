---
layout: default
title: "SoX Expert"
grand_parent: 日本語
parent: ソフトウェア開発
nav_order: 29
lang_peer: /en/skills/dev/sox-expert/
permalink: /ja/skills/dev/sox-expert/
---

# SoX Expert
{: .no_toc }

SoX（Sound eXchange）を使用した音声処理の専門スキル。音声ファイルの変換、編集、エフェクト適用を効率的に支援。フォーマット変換（WAV/MP3/FLAC/OGG/AIFF等）、音声編集（トリム、結合、分割、フェード）、エフェクト（ノイズ除去、ノーマライズ、EQ、リバーブ、コンプレッサー）、分析（soxi、stat、spectrogram）など幅広い操作をカバー。Use when converting audio formats, applying audio effects, trimming/splitting audio files, normalizing volume, removing noise, generating spectrograms, or processing audio for podcasts/music production.
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/sox-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/sox-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

SoX（Sound eXchange）は「音声のスイスアーミーナイフ」と呼ばれる、最も強力なコマンドライン音声処理ツールです。このスキルは、SoXを使用した効率的な音声変換、エフェクト適用、ノイズ除去、音声分析を支援します。

**FFmpegとの使い分け:**
- **SoX推奨**: 音声のみの処理、複雑なエフェクトチェーン、ノイズ除去、バッチ変換
- **FFmpeg推奨**: 動画からの音声抽出、動画＋音声の同時処理、ストリーミング

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

### macOS (Homebrew)

```bash
# 基本インストール
brew install sox

# MP3サポート付き（推奨）
brew install sox --with-lame
```

### Linux (apt/dnf)

```bash
# Ubuntu/Debian（全フォーマットサポート）
sudo apt update && sudo apt install sox libsox-fmt-all

# Fedora
sudo dnf install sox sox-plugins-freeworld

# CentOS/RHEL
sudo yum install sox
```

### Windows

```bash
# Chocolatey
choco install sox.portable

# Scoop
scoop install sox

# または公式サイトからダウンロード
# https://sourceforge.net/projects/sox/
```

### 確認コマンド

```bash
# バージョン確認
sox --version

# 対応フォーマット確認
sox --help-format all

# ヘルプ（エフェクト一覧）
sox --help-effect all

# ファイル情報確認ツール
soxi --version
```

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

```bash
1. 入力ファイル確認（soxi） → 2. 出力形式の選択 → 3. 品質設定 → 4. 変換実行
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

- `skills/sox-expert/references/effects_guide.md`
- `skills/sox-expert/references/format_conversion.md`
- `skills/sox-expert/references/quick_reference.md`
- `skills/sox-expert/references/troubleshooting.md`

**Scripts:**

- `skills/sox-expert/scripts/soxi_analyzer.py`
