---
layout: default
title: "FFmpeg Expert"
grand_parent: English
parent: Software Development
nav_order: 18
lang_peer: /ja/skills/dev/ffmpeg-expert/
permalink: /en/skills/dev/ffmpeg-expert/
---

# FFmpeg Expert
{: .no_toc }

FFmpegを使用したマルチメディア処理の専門スキル。動画・音声の変換、編集、最適化を効率的に支援。フォーマット変換、コーデック選択、フィルタ適用、ストリーミング準備、ハードウェアアクセラレーションなど幅広い操作をカバー。Use when converting video/audio formats, transcoding codecs, trimming/cutting media, creating GIFs, extracting audio, adding watermarks, preparing for streaming (HLS/DASH), or optimizing media files for web/mobile.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/ffmpeg-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/ffmpeg-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

FFmpegは、動画・音声の変換、編集、ストリーミング処理を行う最も強力なオープンソースツールです。このスキルは、FFmpegを使用した効率的なマルチメディア処理、最適なコーデック選択、フィルタ適用、パフォーマンス最適化を支援します。

---

## 2. Prerequisites

### macOS (Homebrew)

```bash
# 基本インストール
brew install ffmpeg

# 全オプション付き（推奨）
brew install ffmpeg --with-fdk-aac --with-libvpx --with-libvorbis
```

### Linux (apt/dnf)

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# CentOS/RHEL (EPEL + RPM Fusion必要)
sudo yum install epel-release
sudo yum install ffmpeg
```

### Windows

```bash
# Chocolatey
choco install ffmpeg

# Scoop
scoop install ffmpeg

# winget
winget install FFmpeg
```

### 確認コマンド

```bash
# バージョン確認
ffmpeg -version

# 利用可能なエンコーダ確認
ffmpeg -encoders

# 利用可能なデコーダ確認
ffmpeg -decoders

# ハードウェアアクセラレーション確認
ffmpeg -hwaccels
```

---

## 3. Quick Start

```bash
1. 入力ファイル確認（ffprobe） → 2. 出力形式の選択 → 3. コーデック選択 → 4. 変換実行
```

---

## 4. How It Works

### Workflow 1: 動画フォーマット変換

```
1. 入力ファイル確認（ffprobe） → 2. 出力形式の選択 → 3. コーデック選択 → 4. 変換実行
```

**Step 1: 入力ファイルの確認**

```bash
# ファイル情報を確認
ffprobe -v error -show_format -show_streams input.mp4

# 簡易確認
ffprobe -v error -show_entries format=duration,size,bit_rate -of default=noprint_wrappers=1 input.mp4
```

**Step 2: 基本変換**

```bash
# 最もシンプルな変換（自動コーデック選択）
ffmpeg -i input.avi output.mp4

# コーデックをコピー（再エンコードなし・高速）
ffmpeg -i input.mkv -c copy output.mp4

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- 動画フォーマットを変換したい（MP4, WebM, MKV, MOV, AVI等）
- コーデックを変更したい（H.264, H.265/HEVC, VP9, AV1, ProRes）
- 動画をトリミング・カットしたい
- 動画を結合したい
- 解像度やフレームレートを変更したい
- 音声を抽出・変換したい（MP3, AAC, FLAC, WAV）

---

## 6. Understanding the Output

実行結果の形式:
- **分析レポート**: Markdownまたは JSON形式でメディアファイル情報を出力
- **互換性チェック結果**: Browser/Mobile互換性の警告・推奨事項
- **エンコードコマンド**: 用途別（Web/Mobile/Archive/Streaming）の推奨ffmpegコマンド

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/ffmpeg-expert/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: filter_reference.md, troubleshooting.md, codec_guide.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: ffprobe_analyzer.py.
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

- `skills/ffmpeg-expert/references/codec_guide.md`
- `skills/ffmpeg-expert/references/filter_reference.md`
- `skills/ffmpeg-expert/references/quick_reference.md`
- `skills/ffmpeg-expert/references/troubleshooting.md`

**Scripts:**

- `skills/ffmpeg-expert/scripts/ffprobe_analyzer.py`
