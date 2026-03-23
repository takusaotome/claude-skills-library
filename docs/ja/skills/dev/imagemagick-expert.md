---
layout: default
title: "Imagemagick Expert"
grand_parent: 日本語
parent: ソフトウェア開発
nav_order: 20
lang_peer: /en/skills/dev/imagemagick-expert/
permalink: /ja/skills/dev/imagemagick-expert/
---

# Imagemagick Expert
{: .no_toc }

ImageMagick CLIを使用した画像処理の専門家スキル。フォーマット変換、リサイズ、トリミング、回転、フィルタ適用、アニメーションGIF作成、PDF処理、バッチ処理を支援。Use when processing images via CLI, converting formats, resizing, cropping, applying filters, creating animations, or batch processing images.
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/imagemagick-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/imagemagick-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

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

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

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

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

1. **Identify Requirements** - Determine the desired operation (convert, resize, filter, etc.) and output format
2. **Select Command** - Choose appropriate ImageMagick command (`magick`, `mogrify`, `identify`, etc.)
3. **Build Command** - Construct command with options and parameters based on Core Operations examples
4. **Execute** - Run the command via Bash tool
5. **Verify Output** - Check the result using `identify` or visual inspection
6. **Iterate** - Adjust parameters if needed based on output quality

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

- `skills/imagemagick-expert/references/batch_processing.md`
- `skills/imagemagick-expert/references/format_conversion.md`
- `skills/imagemagick-expert/references/image_manipulation.md`
