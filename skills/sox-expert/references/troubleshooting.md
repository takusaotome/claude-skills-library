# SoX Troubleshooting Guide

SoXの一般的な問題と解決策です。

## インストール・環境問題

### soxコマンドが見つからない

**エラー:**
```
sox: command not found
```

**解決策:**

```bash
# macOS
brew install sox

# Ubuntu/Debian
sudo apt install sox

# Fedora
sudo dnf install sox

# パスを確認
which sox
```

### MP3サポートがない

**エラー:**
```
sox FAIL formats: no handler for file extension `mp3'
```

**解決策:**

```bash
# Ubuntu/Debian
sudo apt install libsox-fmt-mp3

# または全フォーマットサポート
sudo apt install libsox-fmt-all

# macOS（lameが必要）
brew install lame

# 確認
sox --help-format mp3
```

### FLACサポートがない

**エラー:**
```
sox FAIL formats: no handler for file extension `flac'
```

**解決策:**

```bash
# Ubuntu/Debian
sudo apt install libsox-fmt-all

# macOS
brew install sox

# 確認
sox --help-format flac
```

### OGGサポートがない

**解決策:**

```bash
# Ubuntu/Debian
sudo apt install libsox-fmt-all

# macOS
brew install sox

# 確認
sox --help-format ogg
```

## 入力ファイル問題

### ファイルが開けない

**エラー:**
```
sox FAIL formats: can't open input file `input.wav': No such file or directory
```

**解決策:**

```bash
# ファイルの存在確認
ls -la input.wav

# パスにスペースがある場合は引用符で囲む
sox "path with spaces/input.wav" output.wav

# 絶対パスを使用
sox /full/path/to/input.wav output.wav
```

### ファイル形式が認識されない

**エラー:**
```
sox FAIL formats: can't determine type of `input.xyz'
```

**解決策:**

```bash
# 対応フォーマット確認
sox --help-format all

# ファイルタイプを明示的に指定
sox -t wav input.xyz output.wav

# ヘッダー付きRAWファイルの場合
sox -t raw -r 44100 -b 16 -c 2 -e signed input.raw output.wav
```

### 破損したファイル

**エラー:**
```
sox FAIL formats: error reading from file header
```

**解決策:**

```bash
# ファイルの整合性確認
file input.wav
soxi input.wav

# 部分的に読める場合は無視オプション
sox -V input.wav output.wav

# 回復不可能な場合はFFmpegを試す
ffmpeg -i input.wav -c copy output_fixed.wav
```

## フォーマット・エンコード問題

### サンプルレートの不一致

**エラー:**
```
sox WARN rate: rate clipped 123 samples
```

**解決策:**

```bash
# 明示的にリサンプリング
sox input.wav -r 44100 output.wav rate -v

# 入力レベルを下げてから
sox input.wav output.wav gain -3 rate -v 44100
```

### ビット深度の問題

**エラー:**
```
sox WARN dither: dither clipped 45 samples
```

**解決策:**

```bash
# ノーマライズしてからダウンサンプル
sox input.wav output.wav norm -3 dither -s

# ゲインを下げる
sox input.wav output.wav gain -6 dither -s
```

### チャンネル数の不一致

**エラー:**
```
sox FAIL formats: can't write 6-channel file
```

**解決策:**

```bash
# ステレオにダウンミックス
sox input.wav output.wav remix 1,2,3 4,5,6

# モノラルに
sox input.wav output.wav remix -
```

### エンコードタイプの問題

**解決策:**

```bash
# エンコードを明示的に指定
sox input.raw -e signed -b 16 output.wav
sox input.raw -e unsigned -b 8 output.wav
sox input.raw -e float -b 32 output.wav

# 利用可能なエンコード確認
sox --help-format wav
```

## エフェクト問題

### ノイズ除去が効かない

**問題:** ノイズが残る

**解決策:**

```bash
# より良いノイズプロファイルを取得
# ノイズのみの区間（1秒以上推奨）を選ぶ
sox noisy.wav -n trim 5 1 noiseprof better_noise.prof

# 強度を調整
sox noisy.wav clean.wav noisered noise.prof 0.3  # 強め

# 複数回適用
sox noisy.wav temp.wav noisered noise.prof 0.2
sox temp.wav clean.wav noisered noise.prof 0.1
```

**問題:** 音質が劣化する

**解決策:**

```bash
# 強度を下げる
sox noisy.wav clean.wav noisered noise.prof 0.1

# 周波数帯域を限定
sox noisy.wav clean.wav highpass 100 noisered noise.prof 0.15
```

### コンプレッサーが効きすぎる

**問題:** 音が潰れる

**解決策:**

```bash
# アタック/リリースを調整
sox input.wav output.wav compand 0.5,1.5 6:-70,-60,-20 -5 -90 0.2

# レシオを緩める
sox input.wav output.wav compand 0.3,1 6:-70,-60,-30 -5 -90 0.2
```

### リバーブが強すぎる

**解決策:**

```bash
# リバーブ量を下げる
sox input.wav output.wav reverb 30

# ウェットゲインを下げる
sox input.wav output.wav reverb 50 50 100 100 0 -6
```

### ピッチ/テンポ変更で音質劣化

**解決策:**

```bash
# 高品質設定
sox input.wav output.wav tempo -q 1.2

# セグメントサイズを調整
sox input.wav output.wav tempo 1.2 82 14 12
```

## パフォーマンス問題

### 処理が遅い

**解決策:**

```bash
# バッファサイズを増やす
sox --buffer 262144 input.wav output.mp3

# 低品質リサンプリング（高速）
sox input.wav -r 44100 output.wav rate -l
```

### メモリ不足

**解決策:**

```bash
# 分割処理
sox input.wav part1.wav trim 0 300
sox input.wav part2.wav trim 300 300
# 個別に処理後、結合

# ストリーミング処理（パイプ）
sox input.wav -t wav - norm | sox -t wav - output.mp3
```

### 大きなファイルの処理

**解決策:**

```bash
# 分割して処理
sox bigfile.wav -p trim 0 600 | sox -p output1.wav norm
sox bigfile.wav -p trim 600 600 | sox -p output2.wav norm

# 最後に結合
sox output1.wav output2.wav final.wav
```

## 出力問題

### 出力ファイルが作成されない

**確認事項:**

```bash
# 権限確認
ls -la ./

# ディスク容量確認
df -h

# 出力先が存在するか
ls -la /path/to/output/
```

### 出力がクリッピングする

**エラー:**
```
sox WARN norm: clipped 234 samples
```

**解決策:**

```bash
# ノーマライズ前にヘッドルームを確保
sox input.wav output.wav gain -3 norm -3

# コンプレッサーを使用
sox input.wav output.wav compand 0.1,0.2 -inf,-50.1,-inf,-50,-50 0 -90 0.1 norm -3
```

### 出力が無音

**確認事項:**

```bash
# 入力の統計確認
sox input.wav -n stat

# 音量が0でないか確認
soxi input.wav

# エフェクトチェーンを確認（vol 0など）
sox input.wav -n stat vol 1
```

## 一般的なエラーメッセージ

### "rate clipped X samples"

入力レベルが高すぎる。

```bash
sox input.wav output.wav gain -6 rate 44100
```

### "dither clipped X samples"

ビット深度変換時のクリッピング。

```bash
sox input.wav output.wav norm -3 dither -s
```

### "no handler for file extension"

フォーマットサポートがインストールされていない。

```bash
sudo apt install libsox-fmt-all
```

### "input buffer too small"

バッファサイズを増やす。

```bash
sox --buffer 262144 input.wav output.wav
```

## デバッグ方法

### 詳細出力

```bash
# 詳細レベル1
sox -V input.wav output.wav

# 詳細レベル3（最大）
sox -V3 input.wav output.wav

# 進捗表示
sox -S input.wav output.wav
```

### エフェクトチェーンの確認

```bash
# 各ステップの出力を確認
sox input.wav -n stat
sox input.wav temp1.wav effect1
sox temp1.wav -n stat
sox temp1.wav temp2.wav effect2
sox temp2.wav -n stat
```

### ファイル情報の詳細確認

```bash
# soxi で詳細確認
soxi input.wav

# file コマンド
file input.wav

# mediainfo（インストール要）
mediainfo input.wav
```

## よくある質問

### Q: WAVとAIFFどちらを使うべき？

**A:**
- Windows環境: WAV
- Mac環境: AIFF
- クロスプラットフォーム: WAV（より広くサポート）

### Q: MP3のビットレートはどれくらい必要？

**A:**
- 一般的な音楽: 192-256kbps
- 高品質: 320kbps
- ポッドキャスト: 128-192kbps
- 電話品質: 64kbps

### Q: ノイズ除去の最適な強度は？

**A:**
- 軽いノイズ: 0.1-0.15
- 通常: 0.2-0.25
- 重いノイズ: 0.3-0.4
- 0.5以上は音質劣化のリスクあり

### Q: なぜsoxではなくffmpegを使うべき場合がある？

**A:**
- 動画+音声の同時処理
- ストリーミング形式（HLS/DASH）
- 特定のコーデック（AAC HE等）
- コンテナフォーマット変換
