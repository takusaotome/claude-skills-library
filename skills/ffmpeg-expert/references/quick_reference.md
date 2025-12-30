# FFmpeg Quick Reference

コピペで使える一般的なFFmpegコマンド集。

## 目次

- [フォーマット変換](#フォーマット変換)
- [コーデック変換](#コーデック変換)
- [トリミング・カット](#トリミングカット)
- [結合](#結合)
- [解像度変更](#解像度変更)
- [音声操作](#音声操作)
- [GIF生成](#gif生成)
- [サムネイル・フレーム抽出](#サムネイルフレーム抽出)
- [ハードウェアアクセラレーション](#ハードウェアアクセラレーション)
- [ストリーミング](#ストリーミング)
- [ファイル情報確認](#ファイル情報確認)

---

## フォーマット変換

### 基本変換

```bash
# AVI → MP4
ffmpeg -i input.avi output.mp4

# MKV → MP4（コーデックコピー・高速）
ffmpeg -i input.mkv -c copy output.mp4

# MOV → MP4
ffmpeg -i input.mov -c:v libx264 -c:a aac output.mp4

# MP4 → WebM
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus output.webm

# MP4 → MKV
ffmpeg -i input.mp4 -c copy output.mkv

# WMV → MP4
ffmpeg -i input.wmv -c:v libx264 -c:a aac output.mp4

# FLV → MP4
ffmpeg -i input.flv -c copy output.mp4
```

### Web最適化MP4

```bash
# Web配信用（faststart付き）
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -c:a aac -movflags +faststart output.mp4
```

---

## コーデック変換

### H.264 (libx264)

```bash
# 高品質（CRF 18）
ffmpeg -i input.mp4 -c:v libx264 -crf 18 -preset slow output.mp4

# バランス（CRF 23・推奨）
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium output.mp4

# 高圧縮（CRF 28）
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset fast output.mp4
```

### H.265 / HEVC (libx265)

```bash
# 高品質
ffmpeg -i input.mp4 -c:v libx265 -crf 22 -preset slow output.mp4

# バランス（推奨）
ffmpeg -i input.mp4 -c:v libx265 -crf 28 -preset medium output.mp4

# 高圧縮
ffmpeg -i input.mp4 -c:v libx265 -crf 32 -preset fast output.mp4
```

### VP9 (WebM)

```bash
# シングルパス
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 output.webm

# 2パスエンコード（推奨）
ffmpeg -i input.mp4 -c:v libvpx-vp9 -b:v 0 -crf 30 -pass 1 -an -f null /dev/null
ffmpeg -i input.mp4 -c:v libvpx-vp9 -b:v 0 -crf 30 -pass 2 -c:a libopus output.webm
```

### AV1 (最新・最高圧縮)

```bash
# libaom-av1（高品質・遅い）
ffmpeg -i input.mp4 -c:v libaom-av1 -crf 30 -cpu-used 4 output.mkv

# libsvtav1（高速・推奨）
ffmpeg -i input.mp4 -c:v libsvtav1 -crf 30 -preset 6 output.mkv
```

### ProRes (編集用)

```bash
# ProRes 422 LT
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 1 output.mov

# ProRes 422（標準）
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 2 output.mov

# ProRes 422 HQ（高品質）
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 3 output.mov

# ProRes 4444（アルファチャンネル対応）
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 4 output.mov
```

---

## トリミング・カット

### 時間指定カット

```bash
# 開始時間から指定時間（-t: duration）
# 再エンコードなし・高速（キーフレーム依存）
ffmpeg -ss 00:01:00 -i input.mp4 -t 00:02:00 -c copy output.mp4

# 開始時間から終了時間まで（-to: end time）
ffmpeg -ss 00:01:00 -i input.mp4 -to 00:03:00 -c copy output.mp4

# 精密カット（再エンコード・正確）
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:03:00 -c:v libx264 -c:a aac output.mp4

# 秒数指定
ffmpeg -ss 60 -i input.mp4 -t 120 -c copy output.mp4
```

### 先頭・末尾カット

```bash
# 最初の10秒をスキップ
ffmpeg -ss 10 -i input.mp4 -c copy output.mp4

# 最後の10秒を削除（動画長が60秒の場合）
ffmpeg -i input.mp4 -t 50 -c copy output.mp4
```

---

## 結合

### ファイルリストで結合

```bash
# Step 1: list.txt を作成
cat > list.txt << EOF
file 'part1.mp4'
file 'part2.mp4'
file 'part3.mp4'
EOF

# Step 2: 結合（同じコーデックなら再エンコードなし）
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# 異なるコーデックの場合は再エンコード
ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac output.mp4
```

### パイプで直接結合（同一形式）

```bash
ffmpeg -i "concat:part1.ts|part2.ts|part3.ts" -c copy output.ts
```

---

## 解像度変更

```bash
# 固定解像度（1920x1080）
ffmpeg -i input.mp4 -vf "scale=1920:1080" output.mp4

# 幅指定でアスペクト比維持
ffmpeg -i input.mp4 -vf "scale=1280:-1" output.mp4

# 幅指定でアスペクト比維持（偶数保証）
ffmpeg -i input.mp4 -vf "scale=1280:-2" output.mp4

# 高さ指定でアスペクト比維持
ffmpeg -i input.mp4 -vf "scale=-2:720" output.mp4

# 高品質スケーリング（Lanczos）
ffmpeg -i input.mp4 -vf "scale=1920:1080:flags=lanczos" output.mp4

# 4K → 1080p
ffmpeg -i input_4k.mp4 -vf "scale=1920:1080:flags=lanczos" output_1080p.mp4

# 1080p → 720p
ffmpeg -i input.mp4 -vf "scale=-2:720" output_720p.mp4
```

---

## 音声操作

### 音声抽出

```bash
# MP3で抽出（192kbps）
ffmpeg -i input.mp4 -vn -acodec mp3 -ab 192k output.mp3

# MP3で抽出（320kbps・高品質）
ffmpeg -i input.mp4 -vn -acodec mp3 -ab 320k output.mp3

# AACで抽出
ffmpeg -i input.mp4 -vn -acodec aac -ab 256k output.aac

# 無圧縮WAVで抽出
ffmpeg -i input.mp4 -vn output.wav

# 元のコーデックのまま抽出
ffmpeg -i input.mp4 -vn -c:a copy output.m4a

# FLAC（ロスレス）で抽出
ffmpeg -i input.mp4 -vn -acodec flac output.flac
```

### 音声削除

```bash
ffmpeg -i input.mp4 -an output.mp4
```

### 音声置換

```bash
# 新しい音声で置換
ffmpeg -i video.mp4 -i new_audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4

# BGM追加（元の音声と合成）
ffmpeg -i video.mp4 -i bgm.mp3 -filter_complex "[0:a]volume=1.0[va];[1:a]volume=0.3[bgm];[va][bgm]amix=inputs=2:duration=first" -c:v copy output.mp4
```

### 音量調整

```bash
# 音量2倍
ffmpeg -i input.mp4 -af "volume=2.0" output.mp4

# 音量半分
ffmpeg -i input.mp4 -af "volume=0.5" output.mp4

# dB指定（+10dB）
ffmpeg -i input.mp4 -af "volume=10dB" output.mp4

# 音量正規化（EBU R128基準）
ffmpeg -i input.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11" output.mp4
```

### 音声フォーマット変換

```bash
# WAV → MP3
ffmpeg -i input.wav -acodec mp3 -ab 320k output.mp3

# MP3 → AAC
ffmpeg -i input.mp3 -acodec aac -ab 256k output.m4a

# FLAC → MP3
ffmpeg -i input.flac -acodec mp3 -ab 320k output.mp3

# WAV → FLAC（ロスレス圧縮）
ffmpeg -i input.wav -acodec flac output.flac
```

---

## GIF生成

### シンプルGIF

```bash
# 基本GIF（最初の5秒、10fps、幅320px）
ffmpeg -i input.mp4 -t 5 -vf "fps=10,scale=320:-1" output.gif

# 指定区間からGIF
ffmpeg -ss 00:00:30 -i input.mp4 -t 5 -vf "fps=10,scale=320:-1" output.gif
```

### 高品質GIF（パレット使用）

```bash
# Step 1: パレット生成
ffmpeg -i input.mp4 -t 5 -vf "fps=10,scale=320:-1,palettegen" palette.png

# Step 2: パレット適用してGIF生成
ffmpeg -i input.mp4 -i palette.png -t 5 -lavfi "fps=10,scale=320:-1[x];[x][1:v]paletteuse" output.gif

# ワンライナー（一時ファイルなし）
ffmpeg -i input.mp4 -t 5 -filter_complex "[0:v]fps=10,scale=320:-1,split[a][b];[a]palettegen[p];[b][p]paletteuse" output.gif
```

---

## サムネイル・フレーム抽出

```bash
# 指定位置から1フレーム抽出
ffmpeg -ss 00:00:10 -i input.mp4 -frames:v 1 thumbnail.jpg

# 指定位置からPNG抽出
ffmpeg -ss 00:00:10 -i input.mp4 -frames:v 1 thumbnail.png

# 毎秒1フレーム抽出
ffmpeg -i input.mp4 -vf "fps=1" frame_%04d.jpg

# 毎分1フレーム抽出
ffmpeg -i input.mp4 -vf "fps=1/60" frame_%04d.jpg

# シーン変化で自動抽出
ffmpeg -i input.mp4 -vf "select='gt(scene,0.4)'" -vsync vfr scene_%04d.jpg

# 最初の10フレームを抽出
ffmpeg -i input.mp4 -frames:v 10 frame_%04d.jpg

# サムネイルグリッド生成（4x4）
ffmpeg -i input.mp4 -vf "select='not(mod(n,100))',scale=320:180,tile=4x4" -frames:v 1 grid.jpg
```

---

## ハードウェアアクセラレーション

### NVIDIA NVENC

```bash
# H.264 NVENC
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc -preset p7 output.mp4

# H.265/HEVC NVENC
ffmpeg -hwaccel cuda -i input.mp4 -c:v hevc_nvenc -preset p7 output.mp4

# 品質指定（-cq: CRF相当）
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc -preset p7 -cq 20 output.mp4
```

### Intel QSV

```bash
# H.264 QSV
ffmpeg -hwaccel qsv -i input.mp4 -c:v h264_qsv -preset veryslow output.mp4

# H.265/HEVC QSV
ffmpeg -hwaccel qsv -i input.mp4 -c:v hevc_qsv output.mp4
```

### Apple VideoToolbox (macOS)

```bash
# H.264 VideoToolbox
ffmpeg -i input.mp4 -c:v h264_videotoolbox -b:v 5M output.mp4

# H.265/HEVC VideoToolbox
ffmpeg -i input.mp4 -c:v hevc_videotoolbox -b:v 5M output.mp4

# ProRes（VideoToolbox）
ffmpeg -i input.mp4 -c:v prores_videotoolbox output.mov
```

### AMD VCE/VCN

```bash
# H.264 AMF
ffmpeg -hwaccel d3d11va -i input.mp4 -c:v h264_amf output.mp4

# H.265/HEVC AMF
ffmpeg -hwaccel d3d11va -i input.mp4 -c:v hevc_amf output.mp4
```

---

## ストリーミング

### HLS生成

```bash
# 基本HLS（10秒セグメント）
ffmpeg -i input.mp4 -c:v libx264 -c:a aac -hls_time 10 -hls_list_size 0 output.m3u8

# 既存コーデック維持
ffmpeg -i input.mp4 -c copy -hls_time 10 -hls_list_size 0 output.m3u8

# セグメントファイル命名
ffmpeg -i input.mp4 -c:v libx264 -c:a aac -hls_time 10 -hls_segment_filename 'segment_%03d.ts' output.m3u8
```

### DASH生成

```bash
# 基本DASH
ffmpeg -i input.mp4 -c:v libx264 -c:a aac -f dash output.mpd

# セグメント時間指定
ffmpeg -i input.mp4 -c:v libx264 -c:a aac -seg_duration 10 -f dash output.mpd
```

---

## ファイル情報確認

```bash
# 詳細情報
ffprobe -v error -show_format -show_streams input.mp4

# 簡易情報
ffprobe -v error -show_entries format=duration,size,bit_rate -of default=noprint_wrappers=1 input.mp4

# JSON形式
ffprobe -v error -show_format -show_streams -of json input.mp4

# 動画の長さのみ
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp4

# 解像度のみ
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 input.mp4

# コーデック確認
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 input.mp4
```
