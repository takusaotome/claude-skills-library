# SoX Format Conversion Guide

SoXでの音声フォーマット変換ガイドです。

## 対応フォーマット一覧

### 主要フォーマット

| フォーマット | 拡張子 | タイプ | 説明 |
|-------------|--------|--------|------|
| WAV | .wav | 非圧縮 | Windows標準、最高品質 |
| AIFF | .aiff, .aif | 非圧縮 | Mac標準 |
| FLAC | .flac | ロスレス圧縮 | 高品質アーカイブ向け |
| MP3 | .mp3 | 非可逆圧縮 | 最も汎用的 |
| OGG Vorbis | .ogg | 非可逆圧縮 | オープンソース |
| Opus | .opus | 非可逆圧縮 | 低ビットレートで高品質 |
| RAW | .raw | 生データ | ヘッダーなし |

### 対応フォーマット確認

```bash
# 全対応フォーマット表示
sox --help-format all

# 特定フォーマットの詳細
sox --help-format mp3
sox --help-format flac
```

## フォーマット比較

### 品質 vs ファイルサイズ

| フォーマット | 品質 | 圧縮率 | 用途 |
|-------------|------|--------|------|
| WAV (16bit) | ★★★★★ | 1x | マスター、編集作業 |
| WAV (24bit) | ★★★★★+ | 1.5x | プロ音楽制作 |
| FLAC | ★★★★★ | 0.5-0.7x | アーカイブ、配布 |
| MP3 320kbps | ★★★★☆ | 0.1-0.15x | 高品質配布 |
| MP3 192kbps | ★★★☆☆ | 0.08-0.1x | 一般配布 |
| MP3 128kbps | ★★☆☆☆ | 0.05-0.08x | ストリーミング |
| OGG q6 | ★★★★☆ | 0.1-0.15x | Web、ゲーム |
| Opus 128kbps | ★★★★☆ | 0.05-0.1x | VoIP、ストリーミング |

## 基本変換

### WAV変換

```bash
# MP3からWAVへ
sox input.mp3 output.wav

# FLACからWAVへ
sox input.flac output.wav

# サンプルレート指定
sox input.mp3 -r 44100 output.wav

# ビット深度指定
sox input.flac -b 16 output.wav

# 両方指定
sox input.flac -r 44100 -b 16 output.wav
```

### MP3変換

```bash
# 基本変換
sox input.wav output.mp3

# ビットレート指定（CBR）
sox input.wav -C 128 output.mp3   # 128kbps
sox input.wav -C 192 output.mp3   # 192kbps
sox input.wav -C 320 output.mp3   # 320kbps

# VBR（可変ビットレート）
sox input.wav -C -4.2 output.mp3  # VBR, quality 4.2

# 高品質設定
sox input.wav -C 320 -r 44100 output.mp3
```

**MP3ビットレートの目安:**
- 128kbps: 一般的な品質、ストリーミング
- 192kbps: 良好な品質、一般配布
- 256kbps: 高品質
- 320kbps: 最高品質（CBR最大）

### FLAC変換

```bash
# 基本変換
sox input.wav output.flac

# 圧縮レベル指定（0-8）
sox input.wav -C 0 output.flac   # 最速、低圧縮
sox input.wav -C 5 output.flac   # バランス
sox input.wav -C 8 output.flac   # 最高圧縮

# 高品質保持
sox input.wav -b 24 -r 96000 output.flac
```

### OGG Vorbis変換

```bash
# 基本変換
sox input.wav output.ogg

# 品質指定（-1〜10）
sox input.wav -C 3 output.ogg    # 低品質
sox input.wav -C 6 output.ogg    # 標準
sox input.wav -C 10 output.ogg   # 最高品質
```

### AIFF変換

```bash
# 基本変換
sox input.wav output.aiff

# Mac互換設定
sox input.wav -b 16 -r 44100 output.aiff
```

## サンプルレート変換

### 一般的なサンプルレート

| サンプルレート | 用途 |
|---------------|------|
| 8000 Hz | 電話品質 |
| 22050 Hz | 低品質音声 |
| 44100 Hz | CD品質（標準） |
| 48000 Hz | DVD、放送 |
| 96000 Hz | ハイレゾ |
| 192000 Hz | スタジオマスター |

### 変換コマンド

```bash
# CD品質（44.1kHz）
sox input.wav -r 44100 output.wav

# DVD品質（48kHz）
sox input.wav -r 48000 output.wav

# ハイレゾ（96kHz）
sox input.wav -r 96000 output.wav

# 高品質リサンプリング
sox input.wav -r 44100 output.wav rate -v

# 超高品質リサンプリング
sox input.wav -r 44100 output.wav rate -v -L
```

### リサンプリング品質オプション

```bash
# rate エフェクトのオプション
-q    # quick（低品質、高速）
-l    # low（低品質）
-m    # medium（中品質）
-h    # high（高品質、デフォルト）
-v    # very high（超高品質）

# 例
sox input.wav -r 44100 output.wav rate -v
```

## ビット深度変換

### 一般的なビット深度

| ビット深度 | ダイナミックレンジ | 用途 |
|-----------|-------------------|------|
| 8 bit | 48 dB | 電話、古い機器 |
| 16 bit | 96 dB | CD、一般配布 |
| 24 bit | 144 dB | プロ音楽制作 |
| 32 bit | 192 dB | 内部処理 |

### 変換コマンド

```bash
# 16ビットに変換
sox input.wav -b 16 output.wav

# 24ビットに変換
sox input.wav -b 24 output.wav

# ディザリング付きダウンサンプル
sox input.wav -b 16 output.wav dither -s

# 高品質ディザリング
sox input.wav -b 16 output.wav dither -S
```

### ディザリングオプション

```bash
# dither エフェクトのオプション
-s    # shaped（標準）
-S    # shaped with high-pass（高品質）
-f    # filtered（フィルタ付き）

# 例
sox input_24bit.wav -b 16 output.wav dither -s
```

## チャンネル変換

### モノラル/ステレオ変換

```bash
# ステレオ → モノラル
sox input.wav output.wav channels 1

# モノラル → ステレオ（デュアルモノラル）
sox input.wav output.wav channels 2
```

### チャンネル操作（remix）

```bash
# 左チャンネルのみ
sox input.wav output.wav remix 1

# 右チャンネルのみ
sox input.wav output.wav remix 2

# L/R入れ替え
sox input.wav output.wav remix 2 1

# ミックスダウン（L+R平均）
sox input.wav output.wav remix 1,2

# カスタムミックス（L: 70% L + 30% R）
sox input.wav output.wav remix 1v0.7,2v0.3 1v0.3,2v0.7
```

## 用途別推奨設定

### CD制作用

```bash
sox input.wav -r 44100 -b 16 -c 2 output.wav dither -s
```

### ポッドキャスト配布用

```bash
sox input.wav -C 192 -r 44100 output.mp3
```

### Web配信用

```bash
sox input.wav -C 128 -r 44100 output.mp3
```

### アーカイブ用

```bash
sox input.wav -C 8 output.flac
```

### 電話/VoIP用

```bash
sox input.wav -r 8000 -c 1 -b 16 output.wav
```

### 高品質音楽配布用

```bash
# MP3
sox input.wav -C 320 -r 44100 output.mp3

# FLAC
sox input.wav -C 8 -r 44100 -b 16 output.flac
```

### 動画編集用

```bash
sox input.wav -r 48000 -b 16 -c 2 output.wav
```

## バッチ変換

### 全ファイル変換

```bash
# WAV → MP3（320kbps）
for f in *.wav; do
  sox "$f" -C 320 "${f%.wav}.mp3"
done

# WAV → FLAC
for f in *.wav; do
  sox "$f" -C 8 "${f%.wav}.flac"
done

# MP3 → WAV
for f in *.mp3; do
  sox "$f" "${f%.mp3}.wav"
done
```

### 品質統一

```bash
# 全ファイルを44.1kHz/16bit/ステレオに統一
for f in *.wav; do
  sox "$f" -r 44100 -b 16 -c 2 "normalized_$f" dither -s
done
```

## トラブルシューティング

### MP3が作成できない

```bash
# Linux: libsox-fmt-mp3をインストール
sudo apt install libsox-fmt-mp3

# macOS: lameをインストール
brew install lame
```

### 対応していないフォーマット

```bash
# Linux: 全フォーマットサポートをインストール
sudo apt install libsox-fmt-all
```

### サンプルレートエラー

```bash
# 明示的にリサンプリング
sox input.wav -r 44100 output.wav rate -v
```

### クリッピング警告

```bash
# ノーマライズを先に実行
sox input.wav output.wav norm -3
```
