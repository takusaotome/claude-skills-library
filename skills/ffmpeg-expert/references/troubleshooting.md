# FFmpeg Troubleshooting Guide

よくあるエラーと解決策。

## 目次

- [インストール・環境問題](#インストール環境問題)
- [入力ファイル問題](#入力ファイル問題)
- [エンコード問題](#エンコード問題)
- [カット・結合問題](#カット結合問題)
- [音声問題](#音声問題)
- [ハードウェアアクセラレーション問題](#ハードウェアアクセラレーション問題)
- [メモリ・パフォーマンス問題](#メモリパフォーマンス問題)
- [互換性問題](#互換性問題)

---

## インストール・環境問題

### "ffmpeg: command not found"

**原因**: FFmpegがインストールされていない、またはPATHに含まれていない

**解決策**:

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# CentOS/RHEL (EPEL必要)
sudo yum install epel-release
sudo yum install ffmpeg

# Windows (Chocolatey)
choco install ffmpeg

# Windows (Scoop)
scoop install ffmpeg

# インストール確認
ffmpeg -version
```

### "Unknown encoder 'libx264'" / "Unknown encoder 'libx265'"

**原因**: FFmpegが該当コーデックサポートなしでビルドされている

**解決策**:

```bash
# 利用可能なエンコーダを確認
ffmpeg -encoders | grep x264
ffmpeg -encoders | grep x265

# macOS: 再インストール
brew reinstall ffmpeg

# Ubuntu: フル版インストール
sudo apt install ffmpeg libavcodec-extra

# 代替コーデックを使用
# libx264 の代わりに: h264_nvenc (NVIDIA), h264_qsv (Intel), h264_videotoolbox (Mac)
```

### "Unknown decoder/encoder '<codec_name>'"

**原因**: 指定したコーデックがビルドに含まれていない

**解決策**:

```bash
# 利用可能なエンコーダ一覧
ffmpeg -encoders

# 利用可能なデコーダ一覧
ffmpeg -decoders

# 特定コーデック検索
ffmpeg -encoders | grep <keyword>
ffmpeg -decoders | grep <keyword>

# ビルド設定確認
ffmpeg -buildconf
```

---

## 入力ファイル問題

### "No such file or directory"

**原因**: ファイルパスが間違っている、または特殊文字を含む

**解決策**:

```bash
# パスをダブルクォートで囲む
ffmpeg -i "path with spaces/video.mp4" output.mp4

# 日本語ファイル名
ffmpeg -i "動画ファイル.mp4" output.mp4

# 絶対パスを使用
ffmpeg -i "/Users/name/Videos/input.mp4" output.mp4

# ファイル存在確認
ls -la "input.mp4"
```

### "Invalid data found when processing input"

**原因**: ファイルが破損している、またはサポートされていない形式

**解決策**:

```bash
# ファイル情報を確認
ffprobe -v error -show_format -show_streams input.mp4

# 破損ファイルの修復試行
ffmpeg -err_detect ignore_err -i input.mp4 -c copy output.mp4

# エラーを無視して変換
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4

# 別形式に変換を試す
ffmpeg -i input.mp4 -c:v mpeg4 -c:a mp3 output.avi
```

### "moov atom not found"

**原因**: MP4のメタデータ（moov atom）が欠落している（録画が中断された等）

**解決策**:

```bash
# untrunc ツールを使用して修復（別途インストール必要）
# https://github.com/anthonydiego/untrunc

# または別の正常なMP4をリファレンスにして修復
untrunc reference.mp4 broken.mp4

# FFmpegで再エンコード
ffmpeg -i broken.mp4 -c:v libx264 -c:a aac output.mp4
```

### "Could not find codec parameters"

**原因**: ストリーム情報が正しく読み取れない

**解決策**:

```bash
# 分析時間を延長
ffmpeg -analyzeduration 100M -probesize 100M -i input.mp4 output.mp4

# 特定のストリームのみ処理
ffmpeg -i input.mp4 -map 0:v:0 -map 0:a:0 -c copy output.mp4
```

---

## エンコード問題

### "height not divisible by 2" / "width not divisible by 2"

**原因**: H.264/H.265は偶数解像度を要求する

**解決策**:

```bash
# 自動で偶数に調整（幅基準）
ffmpeg -i input.mp4 -vf "scale=1280:-2" output.mp4

# 自動で偶数に調整（高さ基準）
ffmpeg -i input.mp4 -vf "scale=-2:720" output.mp4

# 手動で偶数を指定
ffmpeg -i input.mp4 -vf "scale=1280:720" output.mp4

# クロップで調整
ffmpeg -i input.mp4 -vf "crop=trunc(iw/2)*2:trunc(ih/2)*2" output.mp4
```

### 画質が悪い / ファイルサイズが大きすぎる

**原因**: CRF値またはビットレート設定が不適切

**解決策**:

```bash
# CRF値を下げる（低い = 高品質）
# H.264: 推奨 18-28（デフォルト23）
ffmpeg -i input.mp4 -c:v libx264 -crf 20 output.mp4

# H.265: 推奨 22-32（デフォルト28）
ffmpeg -i input.mp4 -c:v libx265 -crf 24 output.mp4

# 2パスエンコードで品質安定
ffmpeg -i input.mp4 -c:v libx264 -b:v 5M -pass 1 -an -f null /dev/null
ffmpeg -i input.mp4 -c:v libx264 -b:v 5M -pass 2 -c:a aac output.mp4

# プリセットを遅くして圧縮効率向上
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset slow output.mp4
```

### エンコードが遅い

**原因**: プリセットが遅い、またはハードウェアアクセラレーション未使用

**解決策**:

```bash
# プリセットを速くする
ffmpeg -i input.mp4 -c:v libx264 -preset fast output.mp4
# ultrafast > superfast > veryfast > faster > fast > medium > slow > slower > veryslow

# ハードウェアアクセラレーション使用（NVIDIA）
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc output.mp4

# ハードウェアアクセラレーション使用（Mac）
ffmpeg -i input.mp4 -c:v h264_videotoolbox output.mp4

# ハードウェアアクセラレーション使用（Intel QSV）
ffmpeg -hwaccel qsv -i input.mp4 -c:v h264_qsv output.mp4

# スレッド数指定
ffmpeg -threads 8 -i input.mp4 -c:v libx264 output.mp4
```

### "Discarding ID3 tags" / "PPS unavailable"

**原因**: ストリームの不整合、通常無視可能な警告

**解決策**:

```bash
# 警告を抑制（動作に問題なければ）
ffmpeg -loglevel error -i input.mp4 output.mp4

# 再エンコードで解消
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4
```

---

## カット・結合問題

### カット位置がずれる

**原因**: `-c copy` 使用時、キーフレーム位置でしかカットできない

**解決策**:

```bash
# 精密カット（再エンコード必要だが正確）
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:03:00 -c:v libx264 -c:a aac output.mp4

# -ss を -i の後に置く（より正確だが遅い）
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:03:00 -c:v libx264 output.mp4

# キーフレーム間隔を確認
ffprobe -v error -select_streams v -show_entries frame=pict_type,pts_time -of csv input.mp4 | head -100
```

### 結合時に音ズレ / 再生が止まる

**原因**: ファイル間でコーデック、フレームレート、解像度が異なる

**解決策**:

```bash
# 事前に統一フォーマットに変換
for f in part*.mp4; do
  ffmpeg -i "$f" -c:v libx264 -r 30 -c:a aac -ar 48000 "fixed_$f"
done

# 変換後のファイルでlist.txt作成
ls fixed_part*.mp4 | sed 's/^/file /' > list.txt

# 結合
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# 最終手段: 強制再エンコード
ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac output.mp4
```

### "Discarding packets" / 結合後に映像と音声の長さが違う

**原因**: タイムスタンプの不整合

**解決策**:

```bash
# タイムスタンプをリセットして結合
ffmpeg -f concat -safe 0 -i list.txt -c copy -fflags +genpts output.mp4

# 再エンコードで解消
ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac output.mp4
```

---

## 音声問題

### 音声がない / "Stream mapping" エラー

**原因**: 音声ストリームが存在しない、またはマッピングミス

**解決策**:

```bash
# ストリーム確認
ffprobe -v error -show_streams input.mp4 | grep codec_type

# 音声があれば明示的にマップ
ffmpeg -i input.mp4 -map 0:v:0 -map 0:a:0 -c copy output.mp4

# 音声がない場合（オプショナルマップ）
ffmpeg -i input.mp4 -map 0:v -map 0:a? -c copy output.mp4
```

### 音ズレ

**原因**: 非同期タイムスタンプ、可変フレームレート、コンテナ問題

**解決策**:

```bash
# 音声を遅らせる（0.5秒）
ffmpeg -i input.mp4 -itsoffset 0.5 -i input.mp4 -map 0:v -map 1:a -c copy output.mp4

# 音声を早める（0.5秒）
ffmpeg -i input.mp4 -itsoffset -0.5 -i input.mp4 -map 1:v -map 0:a -c copy output.mp4

# 再エンコードで同期
ffmpeg -i input.mp4 -async 1 -c:v copy -c:a aac output.mp4

# 可変フレームレートを固定
ffmpeg -i input.mp4 -vsync cfr -r 30 -c:a copy output.mp4
```

### 音声コーデックエラー / "Invalid audio stream"

**原因**: サポートされていない音声フォーマット

**解決策**:

```bash
# 音声を再エンコード
ffmpeg -i input.mp4 -c:v copy -c:a aac output.mp4

# 音声削除して映像のみ
ffmpeg -i input.mp4 -an -c:v copy output.mp4

# 別の音声コーデックを試す
ffmpeg -i input.mp4 -c:v copy -c:a mp3 output.mp4
```

---

## ハードウェアアクセラレーション問題

### "Cannot load <hwaccel>" / "No NVENC capable devices found"

**原因**: GPUドライバーが古い、非対応GPU、または環境設定不備

**解決策**:

```bash
# 利用可能なハードウェアアクセラレータ確認
ffmpeg -hwaccels

# NVIDIA: ドライバー確認
nvidia-smi

# Intel: VA-API確認
vainfo

# ソフトウェアエンコードにフォールバック
ffmpeg -i input.mp4 -c:v libx264 output.mp4
```

### ハードウェアエンコード時に画質が悪い

**原因**: ハードウェアエンコーダはソフトウェアより品質が劣る場合がある

**解決策**:

```bash
# NVENC: 品質設定を調整
ffmpeg -i input.mp4 -c:v h264_nvenc -preset p7 -cq 20 output.mp4
# -cq: CRF相当の品質設定（低い = 高品質）

# ビットレートを高めに設定
ffmpeg -i input.mp4 -c:v h264_nvenc -b:v 10M output.mp4

# B-frameを有効化（品質向上）
ffmpeg -i input.mp4 -c:v h264_nvenc -preset p7 -b_ref_mode middle output.mp4
```

### "No VA display" (Intel QSV on Linux)

**原因**: VA-APIドライバーが正しくインストールされていない

**解決策**:

```bash
# VA-APIドライバーインストール（Ubuntu）
sudo apt install intel-media-va-driver-non-free vainfo

# 確認
vainfo

# 環境変数設定
export LIBVA_DRIVER_NAME=iHD
```

---

## メモリ・パフォーマンス問題

### "Out of memory" / クラッシュ

**原因**: 高解像度動画や複雑なフィルタでメモリ不足

**解決策**:

```bash
# スレッド数制限
ffmpeg -threads 4 -i input.mp4 output.mp4

# 入力バッファサイズ制限
ffmpeg -thread_queue_size 512 -i input.mp4 output.mp4

# フィルタ処理を分割
# 1. まず変換
ffmpeg -i input.mp4 -c:v libx264 temp.mp4
# 2. 次にフィルタ適用
ffmpeg -i temp.mp4 -vf "complex_filter" output.mp4
```

### CPU使用率100%でシステムが重い

**原因**: リソース過負荷

**解決策**:

```bash
# nice値で優先度下げる
nice -n 19 ffmpeg -i input.mp4 output.mp4

# スレッド数制限
ffmpeg -threads 2 -i input.mp4 output.mp4

# バックグラウンドで実行
nohup ffmpeg -i input.mp4 output.mp4 &
```

### ディスク容量不足

**原因**: 出力ファイルが大きすぎる

**解決策**:

```bash
# 事前にサイズ見積もり（ビットレート × 時間）
# 例: 5Mbps × 3600秒 = 2.25GB

# 空き容量確認
df -h

# CRF値を上げて圧縮
ffmpeg -i input.mp4 -c:v libx264 -crf 28 output.mp4

# 解像度を下げる
ffmpeg -i input.mp4 -vf "scale=-2:720" output.mp4
```

---

## 互換性問題

### "Could not write header" (HLS/DASH)

**原因**: 出力ディレクトリが存在しない

**解決策**:

```bash
# ディレクトリ事前作成
mkdir -p output_hls

# HLS生成
ffmpeg -i input.mp4 -c:v libx264 -c:a aac -hls_time 10 output_hls/playlist.m3u8
```

### ブラウザで再生できない

**原因**: コーデック・プロファイル・コンテナの互換性問題

**解決策**:

```bash
# Web互換設定（H.264 Baseline）
ffmpeg -i input.mp4 -c:v libx264 -profile:v baseline -level 3.0 -c:a aac -movflags +faststart output.mp4

# より広い互換性
ffmpeg -i input.mp4 -c:v libx264 -profile:v main -level 3.1 -pix_fmt yuv420p -c:a aac -movflags +faststart output.mp4

# Fast Start有効化（ストリーミング対応）
ffmpeg -i input.mp4 -c copy -movflags +faststart output.mp4
```

### iPhone/Androidで再生できない

**原因**: コーデックまたはプロファイルが非対応

**解決策**:

```bash
# iOS/Android互換（H.264 Main Profile）
ffmpeg -i input.mp4 -c:v libx264 -profile:v main -level 3.1 -c:a aac -b:a 128k -movflags +faststart output.mp4

# 4K動画をHEVCで（新しいデバイス向け）
ffmpeg -i input_4k.mp4 -c:v libx265 -tag:v hvc1 -c:a aac output.mp4
# -tag:v hvc1 は Apple デバイス互換に必要
```

### QuickTime / Final Cut Pro で開けない

**原因**: コーデックまたはコンテナの互換性

**解決策**:

```bash
# ProRes に変換
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 3 -c:a pcm_s16le output.mov

# H.264 MOVコンテナ
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mov
```

---

## デバッグTips

### 詳細ログ出力

```bash
# 最大詳細度
ffmpeg -v debug -i input.mp4 output.mp4

# ログをファイルに保存
ffmpeg -v debug -i input.mp4 output.mp4 2> ffmpeg_log.txt
```

### ストリーム情報の詳細確認

```bash
# 全情報をJSON形式で取得
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# 特定情報のみ
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate -of csv=p=0 input.mp4
```

### ドライラン（実行せずにコマンド確認）

```bash
# -t 1 で1秒だけテスト
ffmpeg -i input.mp4 -t 1 -c:v libx264 -c:a aac test_output.mp4

# フレーム数制限でテスト
ffmpeg -i input.mp4 -frames:v 100 -c:v libx264 test_output.mp4
```
