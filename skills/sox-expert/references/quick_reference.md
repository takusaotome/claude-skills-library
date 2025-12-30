# SoX Quick Reference

コピペで使えるSoXコマンド集です。

## 基本構文

```bash
sox [global-options] [input-options] input-file [output-options] output-file [effects...]
```

## ファイル情報確認

```bash
# 全情報表示
soxi input.wav

# サンプルレート
soxi -r input.wav

# チャンネル数
soxi -c input.wav

# ビット深度
soxi -b input.wav

# 再生時間（HH:MM:SS.ss）
soxi -d input.wav

# 再生時間（秒）
soxi -D input.wav

# サンプル数
soxi -s input.wav

# エンコード方式
soxi -e input.wav

# ファイルタイプ
soxi -t input.wav
```

## フォーマット変換

```bash
# 基本変換（拡張子で自動判別）
sox input.wav output.mp3
sox input.mp3 output.wav
sox input.wav output.flac
sox input.wav output.ogg

# MP3ビットレート指定（kbps）
sox input.wav -C 128 output.mp3
sox input.wav -C 192 output.mp3
sox input.wav -C 320 output.mp3

# MP3 VBR（可変ビットレート）
sox input.wav -C -4.2 output.mp3

# FLAC圧縮レベル（0-8）
sox input.wav -C 8 output.flac
```

## サンプルレート変換

```bash
# 44.1kHz（CD品質）
sox input.wav -r 44100 output.wav

# 48kHz（DVD品質）
sox input.wav -r 48000 output.wav

# 96kHz（高品質）
sox input.wav -r 96000 output.wav

# 22.05kHz（低品質）
sox input.wav -r 22050 output.wav

# 高品質リサンプリング
sox input.wav -r 44100 output.wav rate -v
```

## ビット深度変換

```bash
# 16ビット
sox input.wav -b 16 output.wav

# 24ビット
sox input.wav -b 24 output.wav

# 32ビット
sox input.wav -b 32 output.wav

# ディザリング付き
sox input.wav -b 16 output.wav dither -s
```

## チャンネル操作

```bash
# モノラルに変換
sox input.wav output.wav channels 1

# ステレオに変換
sox input.wav output.wav channels 2

# 左チャンネルのみ
sox input.wav output.wav remix 1

# 右チャンネルのみ
sox input.wav output.wav remix 2

# L/R入れ替え
sox input.wav output.wav remix 2 1

# ミックスダウン（L+R平均）
sox input.wav output.wav remix 1,2
```

## トリミング・カット

```bash
# 先頭から30秒
sox input.wav output.wav trim 0 30

# 1分から2分まで
sox input.wav output.wav trim 1:00 1:00

# MM:SS形式
sox input.wav output.wav trim 0:30 1:30

# 最後の10秒を除外
sox input.wav output.wav trim 0 -10

# 最後の30秒のみ
sox input.wav output.wav trim -30

# 複数区間を抽出
sox input.wav output.wav trim 0 10 trim 20 10
```

## 結合

```bash
# 複数ファイルを結合
sox file1.wav file2.wav file3.wav output.wav

# 異なるフォーマットの結合
sox file1.mp3 file2.wav output.wav
```

## 分割

```bash
# 30秒ごとに分割
sox input.wav output.wav trim 0 30 : newfile : restart

# 無音で自動分割
sox input.wav output.wav silence 1 0.5 1% 1 0.5 1% : newfile : restart
```

## フェード

```bash
# フェードイン3秒
sox input.wav output.wav fade t 3

# フェードアウト5秒
sox input.wav output.wav fade t 0 0:0 5

# フェードイン3秒 + フェードアウト5秒
sox input.wav output.wav fade t 3 0:0 5

# フェードタイプ
# t = linear（デフォルト）
# q = quarter sine
# h = half sine
# l = logarithmic
# p = parabolic
sox input.wav output.wav fade q 3
```

## パディング（無音追加）

```bash
# 先頭に1秒
sox input.wav output.wav pad 1 0

# 末尾に2秒
sox input.wav output.wav pad 0 2

# 両端に無音
sox input.wav output.wav pad 1 2
```

## 音量操作

```bash
# 音量調整（dB）
sox input.wav output.wav vol -3dB
sox input.wav output.wav vol +6dB

# 音量調整（倍率）
sox input.wav output.wav vol 0.5
sox input.wav output.wav vol 2.0

# ピークノーマライズ（0dB）
sox input.wav output.wav norm

# ヘッドルーム付きノーマライズ
sox input.wav output.wav norm -3
sox input.wav output.wav norm -6

# ゲイン調整
sox input.wav output.wav gain -3
sox input.wav output.wav gain +6
```

## イコライザー

```bash
# 低音ブースト
sox input.wav output.wav bass +6
sox input.wav output.wav bass -3

# 高音ブースト
sox input.wav output.wav treble +3
sox input.wav output.wav treble -6

# バンドEQ（周波数, Q, ゲイン）
sox input.wav output.wav equalizer 1000 1q +6
sox input.wav output.wav equalizer 100 2q -3

# ハイパスフィルタ
sox input.wav output.wav highpass 80
sox input.wav output.wav highpass 100

# ローパスフィルタ
sox input.wav output.wav lowpass 12000
sox input.wav output.wav lowpass 8000

# バンドパスフィルタ
sox input.wav output.wav bandpass 1000 200

# バンドリジェクト（ノッチ）
sox input.wav output.wav bandreject 60 10
```

## リバーブ・空間系

```bash
# リバーブ（基本）
sox input.wav output.wav reverb 50

# リバーブ（詳細）
# reverb [reverberance] [HF-damping] [room-scale] [stereo-depth] [pre-delay] [wet-gain]
sox input.wav output.wav reverb 50 50 100 100 0 0

# エコー
# echo [gain-in] [gain-out] [delay-ms] [decay]
sox input.wav output.wav echo 0.8 0.9 500 0.3

# 複数エコー
sox input.wav output.wav echo 0.8 0.9 500 0.3 echo 0.8 0.9 1000 0.25

# コーラス
sox input.wav output.wav chorus 0.7 0.9 55 0.4 0.25 2 -t

# フランジャー
sox input.wav output.wav flanger

# フェイザー
sox input.wav output.wav phaser 0.89 0.85 1 0.24 2 -t
```

## ダイナミクス（コンプレッサー）

```bash
# 基本コンプレッサー
sox input.wav output.wav compand 0.3,1 6:-70,-60,-20 -5 -90 0.2

# リミッター
sox input.wav output.wav compand 0.1,0.2 -inf,-50.1,-inf,-50,-50 0 -90 0.1

# コントラスト
sox input.wav output.wav contrast 75
```

## ピッチ・テンポ

```bash
# ピッチアップ（半音単位、100=半音）
sox input.wav output.wav pitch 100
sox input.wav output.wav pitch 200

# ピッチダウン
sox input.wav output.wav pitch -100
sox input.wav output.wav pitch -200

# テンポアップ（ピッチ維持）
sox input.wav output.wav tempo 1.2
sox input.wav output.wav tempo 1.5

# テンポダウン
sox input.wav output.wav tempo 0.8
sox input.wav output.wav tempo 0.5

# スピード変更（ピッチも変化）
sox input.wav output.wav speed 1.5
sox input.wav output.wav speed 0.5
```

## ノイズ除去

```bash
# Step 1: ノイズプロファイル作成
sox noisy.wav -n trim 0 0.5 noiseprof noise.prof

# Step 2: ノイズ除去
sox noisy.wav clean.wav noisered noise.prof 0.21

# 強度調整（0.0-1.0）
sox noisy.wav clean.wav noisered noise.prof 0.1   # 弱
sox noisy.wav clean.wav noisered noise.prof 0.21  # 標準
sox noisy.wav clean.wav noisered noise.prof 0.3   # 強

# ワンライナー
sox input.wav -n trim 0 0.5 noiseprof | sox input.wav output.wav noisered
```

## 無音処理

```bash
# 先頭の無音を除去
sox input.wav output.wav silence 1 0.1 1%

# 末尾の無音を除去
sox input.wav output.wav reverse silence 1 0.1 1% reverse

# 両端の無音を除去
sox input.wav output.wav silence 1 0.1 1% reverse silence 1 0.1 1% reverse
```

## 分析

```bash
# 基本統計
sox input.wav -n stat

# 詳細統計
sox input.wav -n stats

# スペクトログラム
sox input.wav -n spectrogram -o spectrogram.png

# カスタムスペクトログラム
sox input.wav -n spectrogram -x 1000 -y 500 -z 80 -t "Title" -o spec.png
```

## 再生・録音

```bash
# 再生
play input.wav

# エフェクト付き再生
play input.wav reverb 50
play input.wav vol -6dB

# 録音
rec output.wav
rec -c 1 -r 44100 -b 16 output.wav

# 録音（5秒）
rec output.wav trim 0 5
```

## 組み合わせ例

```bash
# ポッドキャスト処理
sox input.wav output.mp3 \
  highpass 80 \
  compand 0.3,1 6:-70,-60,-20 -5 -90 0.2 \
  norm -3

# ノイズ除去 + ノーマライズ
sox noisy.wav clean.wav noisered noise.prof 0.21 norm -3

# 電話音声風
sox input.wav output.wav lowpass 3400 highpass 300

# ラジオ風
sox input.wav output.wav lowpass 5000 highpass 300 compand 0.3,1 6:-70,-60,-20 -5 -90 0.2
```

## バッチ処理

```bash
# 全WAVをMP3に変換
for f in *.wav; do sox "$f" -C 320 "${f%.wav}.mp3"; done

# 全ファイルをノーマライズ
for f in *.wav; do sox "$f" "norm_$f" norm -3; done

# サンプルレート変換
for f in *.wav; do sox "$f" -r 44100 "44k_$f"; done
```

## グローバルオプション

```bash
# 詳細出力
sox -V input.wav output.mp3

# 超詳細出力
sox -V3 input.wav output.mp3

# 進捗表示
sox -S input.wav output.mp3

# バッファサイズ指定
sox --buffer 131072 input.wav output.mp3
```
