---
layout: default
title: "SoX Expert"
grand_parent: English
parent: Software Development
nav_order: 29
lang_peer: /ja/skills/dev/sox-expert/
permalink: /en/skills/dev/sox-expert/
---

# SoX Expert
{: .no_toc }

SoX（Sound eXchange）を使用した音声処理の専門スキル。音声ファイルの変換、編集、エフェクト適用を効率的に支援。フォーマット変換（WAV/MP3/FLAC/OGG/AIFF等）、音声編集（トリム、結合、分割、フェード）、エフェクト（ノイズ除去、ノーマライズ、EQ、リバーブ、コンプレッサー）、分析（soxi、stat、spectrogram）など幅広い操作をカバー。Use when converting audio formats, applying audio effects, trimming/splitting audio files, normalizing volume, removing noise, generating spectrograms, or processing audio for podcasts/music production.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/sox-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/sox-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

SoX（Sound eXchange）は「音声のスイスアーミーナイフ」と呼ばれる、最も強力なコマンドライン音声処理ツールです。このスキルは、SoXを使用した効率的な音声変換、エフェクト適用、ノイズ除去、音声分析を支援します。

**FFmpegとの使い分け:**
- **SoX推奨**: 音声のみの処理、複雑なエフェクトチェーン、ノイズ除去、バッチ変換
- **FFmpeg推奨**: 動画からの音声抽出、動画＋音声の同時処理、ストリーミング

---

## 2. Prerequisites

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

---

## 3. Quick Start

```bash
1. 入力ファイル確認（soxi） → 2. 出力形式の選択 → 3. 品質設定 → 4. 変換実行
```

---

## 4. How It Works

<!-- TODO: Describe the internal pipeline/algorithm -->

---

## 5. Usage Examples

<!-- TODO: Add 4-6 real-world usage scenarios -->

---

## 6. Understanding the Output

<!-- TODO: Describe output file format and field definitions -->

---

## 7. Tips & Best Practices

<!-- TODO: Add expert advice for getting the most value -->

---

## 8. Combining with Other Skills

<!-- TODO: Add multi-skill workflow table -->

---

## 9. Troubleshooting

<!-- TODO: Add common errors and fixes -->

---

## 10. Reference

**References:**

- `skills/sox-expert/references/effects_guide.md`
- `skills/sox-expert/references/format_conversion.md`
- `skills/sox-expert/references/quick_reference.md`
- `skills/sox-expert/references/troubleshooting.md`

**Scripts:**

- `skills/sox-expert/scripts/soxi_analyzer.py`
