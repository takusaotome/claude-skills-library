---
layout: default
title: "SoX Expert"
grand_parent: English
parent: Software Development
nav_order: 30
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

### Workflow 1: フォーマット変換

```
1. 入力ファイル確認（soxi） → 2. 出力形式の選択 → 3. 品質設定 → 4. 変換実行
```

**Step 1: 入力ファイルの確認**

```bash
# 詳細情報を確認
soxi input.wav

# 特定項目のみ取得
soxi -r input.wav   # サンプルレート
soxi -c input.wav   # チャンネル数
soxi -b input.wav   # ビット深度
soxi -d input.wav   # 再生時間
soxi -D input.wav   # 再生時間（秒）
```

**Step 2: 基本変換**

```bash
# 最もシンプルな変換（自動設定）

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- 音声フォーマットを変換したい（WAV, MP3, FLAC, OGG, AIFF等）
- 音声をトリミング・カットしたい
- 複数の音声ファイルを結合したい
- 音声にフェードイン/アウトを追加したい
- ノイズを除去したい
- 音量を正規化（ノーマライズ）したい

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 4 guide file(s).
- Script-assisted execution using 1 helper command(s) where applicable.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/sox-expert/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: troubleshooting.md, effects_guide.md, format_conversion.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: soxi_analyzer.py.
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
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/sox-expert/references/effects_guide.md`
- `skills/sox-expert/references/format_conversion.md`
- `skills/sox-expert/references/quick_reference.md`
- `skills/sox-expert/references/troubleshooting.md`

**Scripts:**

- `skills/sox-expert/scripts/soxi_analyzer.py`
