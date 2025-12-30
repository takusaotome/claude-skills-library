---
name: sox-expert
description: SoX（Sound eXchange）を使用した音声処理の専門スキル。音声ファイルの変換、編集、エフェクト適用を効率的に支援。フォーマット変換（WAV/MP3/FLAC/OGG/AIFF等）、音声編集（トリム、結合、分割、フェード）、エフェクト（ノイズ除去、ノーマライズ、EQ、リバーブ、コンプレッサー）、分析（soxi、stat、spectrogram）など幅広い操作をカバー。Use when converting audio formats, applying audio effects, trimming/splitting audio files, normalizing volume, removing noise, generating spectrograms, or processing audio for podcasts/music production.
---

# SoX Expert

## Overview

SoX（Sound eXchange）は「音声のスイスアーミーナイフ」と呼ばれる、最も強力なコマンドライン音声処理ツールです。このスキルは、SoXを使用した効率的な音声変換、エフェクト適用、ノイズ除去、音声分析を支援します。

**FFmpegとの使い分け:**
- **SoX推奨**: 音声のみの処理、複雑なエフェクトチェーン、ノイズ除去、バッチ変換
- **FFmpeg推奨**: 動画からの音声抽出、動画＋音声の同時処理、ストリーミング

## When to Use This Skill

- 音声フォーマットを変換したい（WAV, MP3, FLAC, OGG, AIFF等）
- 音声をトリミング・カットしたい
- 複数の音声ファイルを結合したい
- 音声にフェードイン/アウトを追加したい
- ノイズを除去したい
- 音量を正規化（ノーマライズ）したい
- イコライザーを適用したい（低音/高音調整）
- リバーブ・エコー等のエフェクトを追加したい
- サンプルレート・ビット深度を変換したい
- ステレオ/モノラル変換したい
- 音声ファイルの情報を確認したい
- スペクトログラムを生成したい
- バッチ処理で複数ファイルを一括変換したい

**Example triggers:**
- "WAVをMP3に変換して"
- "音声ファイルをトリムしたい"
- "ノイズを除去して"
- "音量を正規化したい"
- "複数の音声を結合して"
- "スペクトログラムを生成して"
- "soxコマンドを教えて"
- "音声ファイルの情報を確認したい"
- "フェードイン/フェードアウトを追加したい"

## Installation & Prerequisites

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

## Core Workflows

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
sox input.wav output.mp3

# サンプルレート指定
sox input.wav -r 44100 output.wav

# ビット深度指定
sox input.wav -b 16 output.wav

# チャンネル数指定（モノラル化）
sox input.wav output.wav channels 1
```

**Step 3: 品質調整（MP3）**

```bash
# ビットレート指定（kbps）
sox input.wav -C 192 output.mp3

# 高品質（320kbps）
sox input.wav -C 320 output.mp3

# 可変ビットレート（VBR）
sox input.wav -C -4.2 output.mp3
```

### Workflow 2: 音声編集（トリム・結合・分割）

```
1. 区間確認 → 2. 編集操作選択 → 3. 実行
```

**トリミング（カット）**

```bash
# 開始位置から指定時間（秒）
sox input.wav output.wav trim 0 30

# 開始位置から終了位置（MM:SS形式）
sox input.wav output.wav trim 0:30 1:30

# 最後の10秒を削除
sox input.wav output.wav trim 0 -10

# 最後の30秒のみ抽出
sox input.wav output.wav trim -30
```

**結合**

```bash
# 複数ファイルを順番に結合
sox file1.wav file2.wav file3.wav output.wav

# 異なるフォーマットも結合可能
sox file1.mp3 file2.wav output.wav
```

**分割**

```bash
# 30秒ごとに分割
sox input.wav output.wav trim 0 30 : newfile : restart

# 無音で自動分割
sox input.wav output.wav silence 1 0.5 1% 1 0.5 1% : newfile : restart
```

**フェード**

```bash
# フェードイン3秒
sox input.wav output.wav fade t 3

# フェードアウト5秒（全長指定必須）
sox input.wav output.wav fade t 0 0:0 5

# フェードイン3秒 + フェードアウト5秒
sox input.wav output.wav fade t 3 0:0 5

# fade タイプ: t=linear, q=quarter, h=half, l=logarithmic, p=parabolic
```

**パディング（無音追加）**

```bash
# 先頭に1秒の無音
sox input.wav output.wav pad 1 0

# 末尾に2秒の無音
sox input.wav output.wav pad 0 2

# 両端に無音追加
sox input.wav output.wav pad 1 2
```

### Workflow 3: エフェクト適用

```
1. 入力分析 → 2. エフェクト選択 → 3. パラメータ調整 → 4. 適用
```

**音量操作**

```bash
# 音量をdBで指定
sox input.wav output.wav vol -3dB

# 音量を倍率で指定
sox input.wav output.wav vol 1.5

# ピークノーマライズ（0dB）
sox input.wav output.wav norm

# ヘッドルーム付きノーマライズ（-3dB）
sox input.wav output.wav norm -3

# ゲイン調整
sox input.wav output.wav gain -3
```

**イコライザー**

```bash
# 低音ブースト（+6dB @ 100Hz）
sox input.wav output.wav bass +6

# 高音ブースト（+3dB @ 3kHz）
sox input.wav output.wav treble +3

# バンドEQ（中心周波数、帯域幅Q、ゲイン）
sox input.wav output.wav equalizer 1000 1q +6

# ハイパスフィルタ（80Hz以下カット）
sox input.wav output.wav highpass 80

# ローパスフィルタ（12kHz以上カット）
sox input.wav output.wav lowpass 12000
```

**空間系エフェクト**

```bash
# リバーブ（リバーブ量、HFダンピング、ルームスケール）
sox input.wav output.wav reverb 50

# 詳細リバーブ
sox input.wav output.wav reverb 50 50 100 100 0 0

# エコー（ゲイン、遅延ms、減衰）
sox input.wav output.wav echo 0.8 0.9 500 0.3

# コーラス
sox input.wav output.wav chorus 0.7 0.9 55 0.4 0.25 2 -t
```

**ダイナミクス**

```bash
# コンプレッサー（基本）
sox input.wav output.wav compand 0.3,1 6:-70,-60,-20 -5 -90 0.2

# リミッター
sox input.wav output.wav compand 0.1,0.2 -inf,-50.1,-inf,-50,-50 0 -90 0.1
```

**ピッチ・テンポ**

```bash
# ピッチを半音上げる
sox input.wav output.wav pitch 100

# ピッチを半音下げる
sox input.wav output.wav pitch -100

# テンポを速くする（ピッチ維持）
sox input.wav output.wav tempo 1.2

# テンポを遅くする
sox input.wav output.wav tempo 0.8

# 速度変更（ピッチも変化）
sox input.wav output.wav speed 1.5
```

### Workflow 4: ノイズ除去

```
1. ノイズプロファイル取得 → 2. プロファイル適用 → 3. 強度調整
```

**Step 1: ノイズプロファイル取得**

```bash
# ノイズのみの部分（無音区間）からプロファイル生成
sox noisy_input.wav -n trim 0 0.5 noiseprof noise.prof

# または別のノイズサンプルから
sox noise_sample.wav -n noiseprof noise.prof
```

**Step 2: ノイズ除去適用**

```bash
# 基本のノイズ除去（0.21 = 21%の強度）
sox noisy_input.wav clean_output.wav noisered noise.prof 0.21

# 強めのノイズ除去
sox noisy_input.wav clean_output.wav noisered noise.prof 0.3

# 弱めのノイズ除去（音質重視）
sox noisy_input.wav clean_output.wav noisered noise.prof 0.1
```

**ワンライナー（プロファイル取得＋適用）**

```bash
# 先頭0.5秒をノイズとして使用
sox input.wav -n trim 0 0.5 noiseprof | sox input.wav output.wav noisered
```

### Workflow 5: 音声分析

```
1. ファイル情報取得 → 2. 統計分析 → 3. 可視化
```

**ファイル情報**

```bash
# 全情報表示
soxi input.wav

# 特定情報
soxi -r input.wav   # サンプルレート
soxi -c input.wav   # チャンネル数
soxi -b input.wav   # ビット深度
soxi -e input.wav   # エンコード方式
soxi -d input.wav   # 再生時間（HH:MM:SS.ss）
soxi -D input.wav   # 再生時間（秒）
soxi -s input.wav   # サンプル数
```

**統計情報**

```bash
# 基本統計（RMS、ピーク等）
sox input.wav -n stat

# 詳細統計
sox input.wav -n stats

# 波形の特性
sox input.wav -n stat -v
```

**スペクトログラム生成**

```bash
# 基本スペクトログラム
sox input.wav -n spectrogram -o spectrogram.png

# カスタマイズ
sox input.wav -n spectrogram \
  -x 1000 \          # 幅（ピクセル）
  -y 500 \           # 高さ
  -z 80 \            # ダイナミックレンジ（dB）
  -t "Audio Analysis" \  # タイトル
  -o spectrogram.png
```

## Audio Operations Reference

### サンプルレート変換

```bash
# CD品質（44.1kHz）
sox input.wav -r 44100 output.wav

# DVD品質（48kHz）
sox input.wav -r 48000 output.wav

# 高品質リサンプリング
sox input.wav -r 44100 output.wav rate -v
```

### ビット深度変換

```bash
# 16ビット
sox input.wav -b 16 output.wav

# 24ビット
sox input.wav -b 24 output.wav

# ディザリング付き（高品質ダウンサンプル）
sox input.wav -b 16 output.wav dither -s
```

### チャンネル操作

```bash
# モノラルに変換
sox input.wav output.wav channels 1

# ステレオに変換
sox input.wav output.wav channels 2

# 左チャンネルのみ抽出
sox input.wav output.wav remix 1

# 右チャンネルのみ抽出
sox input.wav output.wav remix 2

# L/Rを入れ替え
sox input.wav output.wav remix 2 1

# ミックスダウン（L+R）
sox input.wav output.wav remix 1,2
```

## Effects Reference

### 音量系エフェクト

| エフェクト | 構文 | 説明 |
|-----------|------|------|
| vol | `vol <gain>` | 音量調整（dB or 倍率） |
| norm | `norm [dB]` | ピークノーマライズ |
| gain | `gain [dB]` | ゲイン調整 |
| compand | `compand <attack,decay> <soft-knee-dB> <gain> <initial-vol> <delay>` | コンプレッサー/エキスパンダー |
| contrast | `contrast [amount]` | コントラスト強調 |

### フィルタ系エフェクト

| エフェクト | 構文 | 説明 |
|-----------|------|------|
| highpass | `highpass <freq>` | ハイパスフィルタ |
| lowpass | `lowpass <freq>` | ローパスフィルタ |
| bandpass | `bandpass <freq> <width>` | バンドパスフィルタ |
| equalizer | `equalizer <freq> <width> <gain>` | パラメトリックEQ |
| bass | `bass <gain>` | 低音調整 |
| treble | `treble <gain>` | 高音調整 |

### 空間系エフェクト

| エフェクト | 構文 | 説明 |
|-----------|------|------|
| reverb | `reverb [reverb%] [HF-damping%] [room-scale%]` | リバーブ |
| echo | `echo <gain-in> <gain-out> <delay> <decay>` | エコー |
| chorus | `chorus <gain-in> <gain-out> <delay> <decay> <speed> <depth>` | コーラス |
| flanger | `flanger [delay] [depth] [regen] [width] [speed]` | フランジャー |
| phaser | `phaser <gain-in> <gain-out> <delay> <decay> <speed>` | フェイザー |

### 時間系エフェクト

| エフェクト | 構文 | 説明 |
|-----------|------|------|
| trim | `trim <start> [length]` | トリミング |
| pad | `pad <start-silence> [end-silence]` | 無音追加 |
| fade | `fade [type] <fade-in> [stop] [fade-out]` | フェードイン/アウト |
| repeat | `repeat <count>` | 繰り返し |
| reverse | `reverse` | 逆再生 |
| silence | `silence <above-periods> <duration> <threshold>` | 無音検出・除去 |

## Common Patterns

### Pattern 1: ポッドキャスト音声処理

```bash
sox input.wav output.mp3 \
  highpass 80 \
  compand 0.3,1 6:-70,-60,-20 -5 -90 0.2 \
  norm -3 \
  rate 44100
```

### Pattern 2: 音楽マスタリング

```bash
sox input.wav output.wav \
  bass +2 \
  treble +1 \
  compand 0.3,1 6:-70,-60,-20 -5 -90 0.2 \
  norm -1
```

### Pattern 3: 音声クリーンアップ

```bash
# Step 1: ノイズプロファイル取得（先頭の無音部分）
sox noisy.wav -n trim 0 0.5 noiseprof noise.prof

# Step 2: ノイズ除去 + ノーマライズ
sox noisy.wav clean.wav noisered noise.prof 0.21 norm -3
```

### Pattern 4: 電話音声シミュレーション

```bash
sox input.wav output.wav \
  lowpass 3400 \
  highpass 300 \
  compand 0.3,1 6:-70,-60,-20 -5 -90 0.2
```

### Pattern 5: バッチ変換

```bash
# 全WAVをMP3に変換（320kbps）
for f in *.wav; do
  sox "$f" -C 320 "${f%.wav}.mp3"
done

# 全音声をノーマライズ
for f in *.wav; do
  sox "$f" "normalized_$f" norm -3
done

# 一括サンプルレート変換
for f in *.wav; do
  sox "$f" -r 44100 "44k_$f"
done
```

### Pattern 6: 無音分割（音声ファイルを無音区間で分割）

```bash
sox input.wav output.wav silence 1 0.5 1% 1 0.5 1% : newfile : restart
```

### Pattern 7: 再生（確認用）

```bash
# 音声再生
play input.wav

# エフェクトをプレビュー
play input.wav reverb 50

# 音量調整して再生
play input.wav vol -6dB
```

## Best Practices

1. **入力ファイルをsoxiで確認してから処理する**
   - サンプルレート、ビット深度、チャンネル数を把握

2. **ロスレスフォーマット（WAV/FLAC）で編集、最後にMP3等へ変換**
   - 中間処理での品質劣化を防ぐ

3. **エフェクトチェーンの順序に注意**
   - 推奨順序: ノイズ除去 → EQ → コンプ → ノーマライズ

4. **normは処理チェーンの最後に適用**
   - 他のエフェクトでレベルが変わるため

5. **ノイズ除去は適切なプロファイルと強度設定**
   - 強すぎると音質劣化、弱すぎると効果なし
   - 0.1〜0.3の範囲で調整

6. **高品質リサンプリングには`rate -v`オプション**
   - デフォルトより高品質な変換

7. **バックアップを取ってから処理**
   - 元ファイルを上書きしない

8. **playコマンドでプレビュー**
   - 処理前にエフェクトを確認できる

## Troubleshooting

よくある問題と解決策の詳細は `references/troubleshooting.md` を参照してください。

**主なエラー:**
- "sox FAIL formats: no handler for file extension" → 対応フォーマットをインストール（`libsox-fmt-all`）
- "sox WARN rate: rate clipped X samples" → 入力レベルが高すぎる、normで調整
- MP3が作成できない → `libsox-fmt-mp3` または `lame` をインストール
- "can't open input file" → ファイルパスを確認、スペースは引用符で囲む

## Resources

### scripts/

- `soxi_analyzer.py`: 音声ファイルの分析と最適処理設定の提案

### references/

- `quick_reference.md`: よく使うコマンドのチートシート
- `effects_guide.md`: エフェクト詳細ガイド
- `format_conversion.md`: フォーマット変換ガイド
- `troubleshooting.md`: トラブルシューティングガイド

### assets/

このスキルにはアセットファイルは含まれません。
