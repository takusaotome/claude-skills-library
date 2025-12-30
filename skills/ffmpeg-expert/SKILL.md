---
name: ffmpeg-expert
description: FFmpegを使用したマルチメディア処理の専門スキル。動画・音声の変換、編集、最適化を効率的に支援。フォーマット変換、コーデック選択、フィルタ適用、ストリーミング準備、ハードウェアアクセラレーションなど幅広い操作をカバー。Use when converting video/audio formats, transcoding codecs, trimming/cutting media, creating GIFs, extracting audio, adding watermarks, preparing for streaming (HLS/DASH), or optimizing media files for web/mobile.
---

# FFmpeg Expert

## Overview

FFmpegは、動画・音声の変換、編集、ストリーミング処理を行う最も強力なオープンソースツールです。このスキルは、FFmpegを使用した効率的なマルチメディア処理、最適なコーデック選択、フィルタ適用、パフォーマンス最適化を支援します。

## When to Use This Skill

- 動画フォーマットを変換したい（MP4, WebM, MKV, MOV, AVI等）
- コーデックを変更したい（H.264, H.265/HEVC, VP9, AV1, ProRes）
- 動画をトリミング・カットしたい
- 動画を結合したい
- 解像度やフレームレートを変更したい
- 音声を抽出・変換したい（MP3, AAC, FLAC, WAV）
- GIFを作成したい
- サムネイルを生成したい
- ストリーミング用に準備したい（HLS/DASH）
- ハードウェアアクセラレーションを使いたい（NVENC, QSV, VideoToolbox）
- フィルタを適用したい（ぼかし、色補正、字幕、ウォーターマーク等）

**Example triggers:**
- "この動画をMP4に変換して"
- "動画から音声だけ抽出したい"
- "動画をGIFにしたい"
- "1分から3分までカットして"
- "H.265で圧縮したい"
- "HLS用にセグメント化して"
- "ウォーターマークを追加して"
- "動画を720pにリサイズして"
- "ffmpegコマンドを教えて"

## Installation & Prerequisites

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

## Core Workflows

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

# H.264で変換（汎用性最高）
ffmpeg -i input.avi -c:v libx264 -c:a aac output.mp4
```

**Step 3: 品質調整**

```bash
# CRF値で品質指定（低い=高品質、推奨: 18-28）
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -c:a aac output.mp4

# プリセットで速度/圧縮効率調整
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium output.mp4
# プリセット: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
```

### Workflow 2: 動画編集（カット・結合）

```
1. タイムスタンプ確認 → 2. カット方法の選択 → 3. 実行
```

**カット（トリミング）**

```bash
# 開始時間から指定時間（再エンコードなし・高速だがキーフレーム依存）
ffmpeg -ss 00:01:00 -i input.mp4 -t 00:02:00 -c copy output.mp4

# 開始時間から終了時間まで
ffmpeg -ss 00:01:00 -i input.mp4 -to 00:03:00 -c copy output.mp4

# 精密カット（再エンコード必要だが正確）
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:03:00 -c:v libx264 -c:a aac output.mp4
```

**結合**

```bash
# Step 1: ファイルリストを作成
cat > list.txt << EOF
file 'part1.mp4'
file 'part2.mp4'
file 'part3.mp4'
EOF

# Step 2: 結合（同じコーデックなら再エンコードなし）
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4
```

### Workflow 3: 音声処理

```
1. 入力確認 → 2. 出力形式・品質設定 → 3. 変換/抽出
```

**音声抽出**

```bash
# MP3で抽出
ffmpeg -i input.mp4 -vn -acodec mp3 -ab 192k output.mp3

# AACで抽出
ffmpeg -i input.mp4 -vn -acodec aac -ab 256k output.aac

# 無圧縮WAVで抽出
ffmpeg -i input.mp4 -vn output.wav

# 元のコーデックのまま抽出
ffmpeg -i input.mp4 -vn -c:a copy output.m4a
```

**音声操作**

```bash
# 音声削除
ffmpeg -i input.mp4 -an output.mp4

# 音声置換
ffmpeg -i video.mp4 -i new_audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4

# 音量調整（2倍）
ffmpeg -i input.mp4 -af "volume=2.0" output.mp4

# 音量正規化（ラウドネス基準）
ffmpeg -i input.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11" output.mp4
```

### Workflow 4: GIF・画像生成

```
1. 区間指定 → 2. パレット生成（高品質の場合） → 3. GIF生成
```

**シンプルGIF生成**

```bash
# 基本GIF（最初の5秒、10fps、幅320px）
ffmpeg -i input.mp4 -t 5 -vf "fps=10,scale=320:-1" output.gif
```

**高品質GIF生成（パレット使用）**

```bash
# Step 1: パレット生成
ffmpeg -i input.mp4 -t 5 -vf "fps=10,scale=320:-1,palettegen" palette.png

# Step 2: パレット適用してGIF生成
ffmpeg -i input.mp4 -i palette.png -t 5 -lavfi "fps=10,scale=320:-1[x];[x][1:v]paletteuse" output.gif
```

**サムネイル・フレーム抽出**

```bash
# 指定位置から1フレーム抽出
ffmpeg -ss 00:00:10 -i input.mp4 -frames:v 1 thumbnail.jpg

# 毎秒1フレーム抽出
ffmpeg -i input.mp4 -vf "fps=1" frame_%04d.jpg

# シーン変化で自動抽出
ffmpeg -i input.mp4 -vf "select='gt(scene,0.4)'" -vsync vfr scene_%04d.jpg
```

### Workflow 5: ストリーミング準備

```
1. 入力分析 → 2. エンコード設定 → 3. HLS/DASH生成
```

**HLS (HTTP Live Streaming) 生成**

```bash
# 基本HLS
ffmpeg -i input.mp4 -c:v libx264 -c:a aac -hls_time 10 -hls_list_size 0 output.m3u8

# 複数ビットレート（Adaptive Bitrate）
ffmpeg -i input.mp4 \
  -map 0:v -map 0:a -c:v libx264 -c:a aac \
  -b:v:0 5M -s:v:0 1920x1080 \
  -b:v:1 3M -s:v:1 1280x720 \
  -b:v:2 1M -s:v:2 640x360 \
  -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" \
  -hls_time 10 -hls_list_size 0 \
  -master_pl_name master.m3u8 \
  stream_%v.m3u8
```

**DASH (Dynamic Adaptive Streaming over HTTP) 生成**

```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac -f dash output.mpd
```

## Video Operations Reference

### 解像度・スケーリング

```bash
# 固定解像度
ffmpeg -i input.mp4 -vf "scale=1920:1080" output.mp4

# アスペクト比維持（幅基準）
ffmpeg -i input.mp4 -vf "scale=1280:-1" output.mp4

# アスペクト比維持（偶数保証）
ffmpeg -i input.mp4 -vf "scale=1280:-2" output.mp4

# 高品質スケーリング（Lanczos）
ffmpeg -i input.mp4 -vf "scale=1920:1080:flags=lanczos" output.mp4
```

### フレームレート変換

```bash
# 30fpsに変換
ffmpeg -i input.mp4 -vf "fps=30" output.mp4

# 24fps（映画風）
ffmpeg -i input.mp4 -vf "fps=24" output.mp4
```

### 回転・反転

```bash
# 時計回り90度
ffmpeg -i input.mp4 -vf "transpose=1" output.mp4

# 反時計回り90度
ffmpeg -i input.mp4 -vf "transpose=2" output.mp4

# 180度回転
ffmpeg -i input.mp4 -vf "transpose=1,transpose=1" output.mp4

# 水平反転
ffmpeg -i input.mp4 -vf "hflip" output.mp4

# 垂直反転
ffmpeg -i input.mp4 -vf "vflip" output.mp4
```

### クロップ

```bash
# 中央から640x480をクロップ
ffmpeg -i input.mp4 -vf "crop=640:480" output.mp4

# 左上から640x480をクロップ
ffmpeg -i input.mp4 -vf "crop=640:480:0:0" output.mp4

# 16:9にクロップ
ffmpeg -i input.mp4 -vf "crop=ih*16/9:ih" output.mp4
```

### 速度変更

```bash
# 2倍速
ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" -af "atempo=2.0" output.mp4

# 0.5倍速（スローモーション）
ffmpeg -i input.mp4 -vf "setpts=2.0*PTS" -af "atempo=0.5" output.mp4

# 4倍速（音声は2回atempo適用）
ffmpeg -i input.mp4 -vf "setpts=0.25*PTS" -af "atempo=2.0,atempo=2.0" output.mp4
```

## Audio Operations Reference

### フォーマット変換

```bash
# MP3変換（高品質）
ffmpeg -i input.wav -acodec mp3 -ab 320k output.mp3

# AAC変換
ffmpeg -i input.mp3 -acodec aac -ab 256k output.m4a

# FLAC（ロスレス）
ffmpeg -i input.wav -acodec flac output.flac

# Opus（Web/VoIP向け高効率）
ffmpeg -i input.mp3 -acodec libopus -ab 128k output.opus
```

### サンプルレート・チャンネル変換

```bash
# サンプルレート変更
ffmpeg -i input.mp3 -ar 44100 output.mp3

# モノラルに変換
ffmpeg -i input.mp3 -ac 1 output.mp3

# ステレオに変換
ffmpeg -i input.mp3 -ac 2 output.mp3
```

## Advanced Operations

### ハードウェアアクセラレーション

**NVIDIA NVENC (CUDA)**

```bash
# H.264 NVENC
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc -preset p7 output.mp4

# H.265/HEVC NVENC
ffmpeg -hwaccel cuda -i input.mp4 -c:v hevc_nvenc -preset p7 output.mp4
```

**Intel QSV (Quick Sync Video)**

```bash
# H.264 QSV
ffmpeg -hwaccel qsv -i input.mp4 -c:v h264_qsv -preset veryslow output.mp4

# H.265/HEVC QSV
ffmpeg -hwaccel qsv -i input.mp4 -c:v hevc_qsv output.mp4
```

**Apple VideoToolbox (macOS)**

```bash
# H.264 VideoToolbox
ffmpeg -i input.mp4 -c:v h264_videotoolbox -b:v 5M output.mp4

# H.265/HEVC VideoToolbox
ffmpeg -i input.mp4 -c:v hevc_videotoolbox -b:v 5M output.mp4
```

### 2パスエンコード

```bash
# Pass 1
ffmpeg -i input.mp4 -c:v libx264 -b:v 5M -pass 1 -an -f null /dev/null

# Pass 2
ffmpeg -i input.mp4 -c:v libx264 -b:v 5M -pass 2 -c:a aac -b:a 192k output.mp4
```

### ウォーターマーク・オーバーレイ

```bash
# 右下にロゴ配置
ffmpeg -i video.mp4 -i logo.png -filter_complex "[1:v]scale=100:-1[logo];[0:v][logo]overlay=W-w-10:H-h-10" output.mp4

# 中央に半透明ロゴ
ffmpeg -i video.mp4 -i logo.png -filter_complex "[1:v]scale=200:-1,format=rgba,colorchannelmixer=aa=0.5[logo];[0:v][logo]overlay=(W-w)/2:(H-h)/2" output.mp4
```

### 字幕

```bash
# SRT字幕を焼き込み
ffmpeg -i input.mp4 -vf "subtitles=subtitle.srt" output.mp4

# ASS字幕を焼き込み（スタイル保持）
ffmpeg -i input.mp4 -vf "ass=subtitle.ass" output.mp4

# 字幕ストリームとして追加
ffmpeg -i input.mp4 -i subtitle.srt -c copy -c:s mov_text output.mp4
```

## Common Patterns

### Pattern 1: Web用最適化

```bash
ffmpeg -i input.mp4 \
  -c:v libx264 -crf 23 -preset medium \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  -pix_fmt yuv420p \
  output_web.mp4
```

### Pattern 2: モバイル用最適化

```bash
ffmpeg -i input.mp4 \
  -c:v libx264 -crf 26 -preset fast \
  -vf "scale=-2:720" \
  -c:a aac -b:a 96k \
  -movflags +faststart \
  output_mobile.mp4
```

### Pattern 3: アーカイブ用高品質

```bash
ffmpeg -i input.mp4 \
  -c:v libx265 -crf 22 -preset slow \
  -c:a flac \
  output_archive.mkv
```

### Pattern 4: SNS投稿用（Instagram/Twitter）

```bash
# Instagram（正方形、60秒以内）
ffmpeg -i input.mp4 \
  -t 60 \
  -vf "crop=min(iw\,ih):min(iw\,ih),scale=1080:1080" \
  -c:v libx264 -crf 23 \
  -c:a aac -b:a 128k \
  output_instagram.mp4

# Twitter（16:9推奨）
ffmpeg -i input.mp4 \
  -t 140 \
  -vf "scale=1280:720" \
  -c:v libx264 -crf 23 \
  -c:a aac -b:a 128k \
  output_twitter.mp4
```

### Pattern 5: バッチ処理

```bash
# 全MP4をWebM(VP9)に変換
for f in *.mp4; do
  ffmpeg -i "$f" -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus "${f%.mp4}.webm"
done

# ディレクトリ内の動画をサムネイル生成
for f in *.mp4; do
  ffmpeg -ss 00:00:05 -i "$f" -frames:v 1 "${f%.mp4}_thumb.jpg"
done
```

## Best Practices

1. **入力ファイルを先にffprobeで確認する**
   - コーデック、解像度、ビットレートを把握してから変換

2. **コーデックコピー（-c copy）を活用**
   - フォーマット変換のみなら再エンコード不要で高速

3. **CRF値で品質を制御する**
   - ビットレート指定より品質が安定
   - H.264: 18-28（23がデフォルト）
   - H.265: 22-32（28がデフォルト）

4. **2パスエンコードで品質を安定させる**
   - 特にビットレート制限がある場合に有効

5. **ハードウェアアクセラレーションで高速化**
   - 大量の動画処理時に特に効果的
   - ただしソフトウェアエンコードより品質が劣る場合あり

6. **faststart フラグを使用**
   - Web配信用MP4には必須（-movflags +faststart）
   - メタデータを先頭に移動してストリーミング開始を高速化

7. **出力先のディスク容量を確認**
   - 大きな動画の変換前に十分な空き容量を確保

## Troubleshooting

よくある問題と解決策の詳細は `references/troubleshooting.md` を参照してください。

**主なエラー:**
- "Unknown encoder" → コーデック未インストール、`ffmpeg -encoders` で確認
- "height not divisible by 2" → `-vf "scale=1280:-2"` で偶数に調整
- カット位置のズレ → `-c copy` ではキーフレーム依存、精密カットは再エンコード
- 音ズレ → ファイル間のコーデック/フレームレート統一が必要

## Resources

### scripts/

- `ffprobe_analyzer.py`: メディアファイルの分析と最適エンコード設定の提案

### references/

- `quick_reference.md`: よく使うコマンドのチートシート
- `codec_guide.md`: コーデック選択ガイド
- `filter_reference.md`: フィルタ構文とサンプル
- `troubleshooting.md`: トラブルシューティングガイド

### assets/

このスキルにはアセットファイルは含まれません。
