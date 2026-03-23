---
layout: default
title: "FFmpeg Expert"
grand_parent: 日本語
parent: ソフトウェア開発
nav_order: 18
lang_peer: /en/skills/dev/ffmpeg-expert/
permalink: /ja/skills/dev/ffmpeg-expert/
---

# FFmpeg Expert
{: .no_toc }

FFmpegを使用したマルチメディア処理の専門スキル。動画・音声の変換、編集、最適化を効率的に支援。フォーマット変換、コーデック選択、フィルタ適用、ストリーミング準備、ハードウェアアクセラレーションなど幅広い操作をカバー。Use when converting video/audio formats, transcoding codecs, trimming/cutting media, creating GIFs, extracting audio, adding watermarks, preparing for streaming (HLS/DASH), or optimizing media files for web/mobile.
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/ffmpeg-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/ffmpeg-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

FFmpegは、動画・音声の変換、編集、ストリーミング処理を行う最も強力なオープンソースツールです。このスキルは、FFmpegを使用した効率的なマルチメディア処理、最適なコーデック選択、フィルタ適用、パフォーマンス最適化を支援します。

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

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

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

```bash
1. 入力ファイル確認（ffprobe） → 2. 出力形式の選択 → 3. コーデック選択 → 4. 変換実行
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

- `skills/ffmpeg-expert/references/codec_guide.md`
- `skills/ffmpeg-expert/references/filter_reference.md`
- `skills/ffmpeg-expert/references/quick_reference.md`
- `skills/ffmpeg-expert/references/troubleshooting.md`

**Scripts:**

- `skills/ffmpeg-expert/scripts/ffprobe_analyzer.py`
