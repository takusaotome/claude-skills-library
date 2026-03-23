---
layout: default
title: "Imagemagick Expert"
grand_parent: English
parent: Software Development
nav_order: 20
lang_peer: /ja/skills/dev/imagemagick-expert/
permalink: /en/skills/dev/imagemagick-expert/
---

# Imagemagick Expert
{: .no_toc }

ImageMagick CLIを使用した画像処理の専門家スキル。フォーマット変換、リサイズ、トリミング、回転、フィルタ適用、アニメーションGIF作成、PDF処理、バッチ処理を支援。Use when processing images via CLI, converting formats, resizing, cropping, applying filters, creating animations, or batch processing images.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/imagemagick-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/imagemagick-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

ImageMagickは画像の作成、編集、合成、変換を行うための強力なCLIツールセットです。200以上の画像フォーマットをサポートし、リサイズ、回転、トリミング、色調整、フィルタ適用、アニメーション作成など幅広い画像処理が可能です。

### Primary Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `magick` | メインコマンド（v7+）、画像変換・処理 | `magick input.png output.jpg` |
| `convert` | 画像変換・処理（レガシー、v6互換） | `convert input.png output.jpg` |
| `identify` | 画像情報の取得 | `identify -verbose image.png` |
| `mogrify` | 画像のインプレース変換 | `mogrify -resize 50% *.jpg` |
| `composite` | 画像の合成 | `composite overlay.png base.png result.png` |
| `montage` | 複数画像のモンタージュ作成 | `montage *.jpg -tile 3x3 montage.jpg` |

---

## 2. Prerequisites

```bash
# Check installation
magick --version

# macOS (Homebrew)
brew install imagemagick

# Linux (Ubuntu/Debian)
sudo apt-get install imagemagick

# Linux (CentOS/RHEL)
sudo yum install ImageMagick
```

---

## 3. Quick Start

1. **Identify Requirements** - Determine the desired operation (convert, resize, filter, etc.) and output format
2. **Select Command** - Choose appropriate ImageMagick command (`magick`, `mogrify`, `identify`, etc.)
3. **Build Command** - Construct command with options and parameters based on Core Operations examples
4. **Execute** - Run the command via Bash tool
5. **Verify Output** - Check the result using `identify` or visual inspection
6. **Iterate** - Adjust parameters if needed based on output quality

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

- `skills/imagemagick-expert/references/batch_processing.md`
- `skills/imagemagick-expert/references/format_conversion.md`
- `skills/imagemagick-expert/references/image_manipulation.md`
