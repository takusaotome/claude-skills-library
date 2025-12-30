# SoX Effects Guide

SoXエフェクトの詳細ガイドです。

## エフェクト基本構文

```bash
sox input.wav output.wav effect1 [params] effect2 [params] ...
```

エフェクトは左から右へ順番に適用されます。

---

## 1. 音量系エフェクト

### vol（音量調整）

音量を調整します。

```bash
# 構文
vol <gain> [type]

# dBで指定
sox input.wav output.wav vol -3dB
sox input.wav output.wav vol +6dB

# 倍率で指定
sox input.wav output.wav vol 0.5
sox input.wav output.wav vol 2.0

# 振幅で指定
sox input.wav output.wav vol 0.5 amplitude
```

**パラメータ:**
- `gain`: 音量値（dB、倍率、振幅）
- `type`: amplitude（デフォルト）, power, dB

### norm（ノーマライズ）

ピークを指定レベルに正規化します。

```bash
# 構文
norm [dB-level]

# 0dBに正規化
sox input.wav output.wav norm

# -3dBに正規化（ヘッドルーム確保）
sox input.wav output.wav norm -3

# -6dBに正規化
sox input.wav output.wav norm -6
```

**推奨値:**
- 音楽: `-1` dB
- ポッドキャスト: `-3` dB
- 放送: `-6` dB

### gain（ゲイン）

ゲインを調整します。normと異なり、ピーク検出なし。

```bash
# 構文
gain [flags] [gain-dB]

# ゲイン調整
sox input.wav output.wav gain -3
sox input.wav output.wav gain +6

# フラグ
sox input.wav output.wav gain -n -3  # ノーマライズ後にゲイン
sox input.wav output.wav gain -l -3  # リミッター付き
sox input.wav output.wav gain -e -3  # イコライズ後にゲイン
```

### compand（コンプレッサー/エキスパンダー）

ダイナミックレンジを制御します。

```bash
# 構文
compand <attack,decay> <soft-knee-dB>:<point,point...> [gain] [initial-volume] [delay]

# 基本コンプレッサー
sox input.wav output.wav compand 0.3,1 6:-70,-60,-20 -5 -90 0.2

# リミッター
sox input.wav output.wav compand 0.1,0.2 -inf,-50.1,-inf,-50,-50 0 -90 0.1

# ノイズゲート
sox input.wav output.wav compand 0.1,0.2 -inf,-40.1,-inf,-40,-40 0 -90 0.1
```

**パラメータ詳細:**
- `attack,decay`: アタック/リリースタイム（秒）
- `soft-knee-dB`: ニー幅
- `point,point`: 入力dB,出力dB のペア
- `gain`: メイクアップゲイン
- `initial-volume`: 初期音量（dB）
- `delay`: 先読み時間（秒）

**ポッドキャスト向け設定:**
```bash
sox input.wav output.wav compand 0.3,1 6:-70,-60,-20 -5 -90 0.2
```

**音楽マスタリング向け設定:**
```bash
sox input.wav output.wav compand 0.02,0.2 6:-70,-60,-20 -8 -90 0.05
```

### contrast（コントラスト強調）

音声のコントラストを強調します。

```bash
# 構文
contrast [enhancement-amount]

# 標準（75）
sox input.wav output.wav contrast 75

# 弱め
sox input.wav output.wav contrast 50

# 強め
sox input.wav output.wav contrast 100
```

---

## 2. フィルタ系エフェクト

### highpass（ハイパスフィルタ）

指定周波数以下をカットします。

```bash
# 構文
highpass [-1|-2] frequency [width]

# 基本
sox input.wav output.wav highpass 80

# 2次フィルタ（急峻）
sox input.wav output.wav highpass -2 80

# 帯域幅指定
sox input.wav output.wav highpass 80 1q
```

**推奨値:**
- 音声: 80-100Hz
- 電話音声: 300Hz
- FM放送風: 50Hz

### lowpass（ローパスフィルタ）

指定周波数以上をカットします。

```bash
# 構文
lowpass [-1|-2] frequency [width]

# 基本
sox input.wav output.wav lowpass 12000

# 2次フィルタ
sox input.wav output.wav lowpass -2 8000

# 電話音声風
sox input.wav output.wav lowpass 3400
```

**推奨値:**
- 高品質: 15000-20000Hz
- AM放送風: 5000Hz
- 電話音声: 3400Hz

### bandpass（バンドパスフィルタ）

指定帯域のみを通過させます。

```bash
# 構文
bandpass [-c] frequency width

# 基本
sox input.wav output.wav bandpass 1000 200

# 定Q帯域
sox input.wav output.wav bandpass -c 1000 2q
```

### bandreject（バンドリジェクト/ノッチフィルタ）

指定帯域をカットします。ハムノイズ除去に有効。

```bash
# 構文
bandreject frequency width

# 60Hzハム除去（US）
sox input.wav output.wav bandreject 60 10

# 50Hzハム除去（EU/日本）
sox input.wav output.wav bandreject 50 10
```

### equalizer（パラメトリックEQ）

特定周波数帯域のゲインを調整します。

```bash
# 構文
equalizer frequency width gain

# 1kHzを+6dBブースト
sox input.wav output.wav equalizer 1000 1q +6

# 低域ブースト
sox input.wav output.wav equalizer 100 2q +3

# 中域カット
sox input.wav output.wav equalizer 2000 1q -3
```

**パラメータ:**
- `frequency`: 中心周波数（Hz）
- `width`: 帯域幅（Q値 or Hz）
- `gain`: ゲイン（dB）

### bass（低音調整）

低音をシンプルにブースト/カットします。

```bash
# 構文
bass gain [frequency [width]]

# +6dBブースト
sox input.wav output.wav bass +6

# 周波数指定
sox input.wav output.wav bass +6 100

# カット
sox input.wav output.wav bass -3
```

### treble（高音調整）

高音をシンプルにブースト/カットします。

```bash
# 構文
treble gain [frequency [width]]

# +3dBブースト
sox input.wav output.wav treble +3

# 周波数指定
sox input.wav output.wav treble +3 3000

# カット
sox input.wav output.wav treble -6
```

---

## 3. 空間系エフェクト

### reverb（リバーブ）

残響効果を追加します。

```bash
# 構文
reverb [reverberance%] [HF-damping%] [room-scale%] [stereo-depth%] [pre-delay-ms] [wet-gain-dB]

# 基本リバーブ
sox input.wav output.wav reverb 50

# ホール風
sox input.wav output.wav reverb 75 50 100 100 10 0

# 小部屋風
sox input.wav output.wav reverb 30 80 30 50 5 0

# 大聖堂風
sox input.wav output.wav reverb 90 30 100 100 50 0
```

**パラメータ:**
- `reverberance%`: リバーブ量（0-100）
- `HF-damping%`: 高周波減衰（0-100）
- `room-scale%`: 部屋サイズ（0-100）
- `stereo-depth%`: ステレオ広がり（0-100）
- `pre-delay-ms`: プリディレイ（ms）
- `wet-gain-dB`: ウェット音のゲイン

### echo（エコー）

反響効果を追加します。

```bash
# 構文
echo gain-in gain-out <delay decay>...

# シンプルエコー
sox input.wav output.wav echo 0.8 0.9 500 0.3

# マルチタップエコー
sox input.wav output.wav echo 0.8 0.7 700 0.25 700 0.3 1000 0.2
```

**パラメータ:**
- `gain-in`: 入力ゲイン
- `gain-out`: 出力ゲイン
- `delay`: 遅延時間（ms）
- `decay`: 減衰量

### chorus（コーラス）

音に厚みを加えます。

```bash
# 構文
chorus gain-in gain-out <delay decay speed depth [-s|-t]>...

# 基本コーラス
sox input.wav output.wav chorus 0.7 0.9 55 0.4 0.25 2 -t

# 厚めのコーラス
sox input.wav output.wav chorus 0.6 0.9 50 0.4 0.25 2 -t 60 0.32 0.4 1.3 -s
```

**パラメータ:**
- `gain-in/out`: 入出力ゲイン
- `delay`: 遅延（ms）
- `decay`: 減衰
- `speed`: モジュレーション速度（Hz）
- `depth`: モジュレーション深度（ms）
- `-s/-t`: 正弦波/三角波

### flanger（フランジャー）

ジェット機のような効果を追加します。

```bash
# 構文
flanger [delay [depth [regen [width [speed [shape [phase [interp]]]]]]]]

# 基本フランジャー
sox input.wav output.wav flanger

# カスタム
sox input.wav output.wav flanger 0 2 0 71 0.5 sine 25 linear
```

### phaser（フェイザー）

位相変調効果を追加します。

```bash
# 構文
phaser gain-in gain-out delay decay speed [-s|-t]

# 基本フェイザー
sox input.wav output.wav phaser 0.89 0.85 1 0.24 2 -t

# 速いフェイザー
sox input.wav output.wav phaser 0.9 0.8 2 0.3 5 -s
```

### tremolo（トレモロ）

音量を周期的に変化させます。

```bash
# 構文
tremolo speed [depth]

# 基本トレモロ
sox input.wav output.wav tremolo 6 40

# 速いトレモロ
sox input.wav output.wav tremolo 10 60
```

---

## 4. ピッチ/テンポ系エフェクト

### pitch（ピッチシフト）

音程を変更します（テンポ維持）。

```bash
# 構文
pitch shift [segment [search [overlap]]]

# 半音アップ（+100セント）
sox input.wav output.wav pitch 100

# 半音ダウン
sox input.wav output.wav pitch -100

# 1オクターブアップ
sox input.wav output.wav pitch 1200

# 1オクターブダウン
sox input.wav output.wav pitch -1200
```

**値の目安:**
- 100 = 半音
- 1200 = 1オクターブ

### tempo（テンポ変更）

テンポを変更します（ピッチ維持）。

```bash
# 構文
tempo [factor [segment [search [overlap]]]]

# 1.2倍速
sox input.wav output.wav tempo 1.2

# 0.8倍速
sox input.wav output.wav tempo 0.8

# 2倍速
sox input.wav output.wav tempo 2.0

# 高品質設定
sox input.wav output.wav tempo -q 1.2
```

### speed（スピード変更）

再生速度を変更します（ピッチも変化）。

```bash
# 構文
speed factor

# 1.5倍速
sox input.wav output.wav speed 1.5

# 0.5倍速（スロー）
sox input.wav output.wav speed 0.5
```

### stretch（ストレッチ）

時間を伸縮します（tempoの逆）。

```bash
# 構文
stretch factor [window]

# 2倍に伸ばす
sox input.wav output.wav stretch 2

# 0.5倍に縮める
sox input.wav output.wav stretch 0.5
```

### bend（ピッチベンド）

時間経過でピッチを変化させます。

```bash
# 構文
bend [-f frame] [-o over] {start,cents,end}

# 上昇ベンド
sox input.wav output.wav bend 0,100,0.5

# 下降ベンド
sox input.wav output.wav bend 0,-100,0.5
```

---

## 5. ノイズ処理エフェクト

### noisered（ノイズリダクション）

ノイズプロファイルを使用してノイズを除去します。

```bash
# 構文
noisered [profile-file [amount]]

# Step 1: プロファイル作成
sox noisy.wav -n trim 0 0.5 noiseprof noise.prof

# Step 2: ノイズ除去
sox noisy.wav clean.wav noisered noise.prof 0.21
```

**強度（amount）の目安:**
- 0.1: 軽度（音質重視）
- 0.21: 標準
- 0.3: 強度（ノイズ除去重視）
- 0.5以上: 非推奨（音質劣化）

### noiseprof（ノイズプロファイル作成）

ノイズプロファイルを作成します。

```bash
# 構文
noiseprof [profile-file]

# プロファイル作成
sox noise_sample.wav -n noiseprof noise.prof

# 入力ファイルの一部から作成
sox input.wav -n trim 0 0.5 noiseprof noise.prof
```

---

## 6. 時間系エフェクト

### trim（トリミング）

音声の一部を切り出します。

```bash
# 構文
trim start [length]

# 先頭から30秒
sox input.wav output.wav trim 0 30

# 1分から1分30秒間
sox input.wav output.wav trim 1:00 0:30

# 最後の30秒
sox input.wav output.wav trim -30
```

### pad（パディング）

無音を追加します。

```bash
# 構文
pad [start-pad] [end-pad]

# 先頭に1秒
sox input.wav output.wav pad 1 0

# 末尾に2秒
sox input.wav output.wav pad 0 2

# 特定位置に
sox input.wav output.wav pad 0@1:00
```

### fade（フェード）

フェードイン/アウトを追加します。

```bash
# 構文
fade [type] fade-in-length [stop-time [fade-out-length]]

# フェードイン3秒
sox input.wav output.wav fade t 3

# フェードアウト5秒
sox input.wav output.wav fade t 0 0:0 5

# 両方
sox input.wav output.wav fade t 3 0:0 5
```

**タイプ:**
- `t`: linear（デフォルト）
- `q`: quarter sine
- `h`: half sine
- `l`: logarithmic
- `p`: parabolic

### silence（無音処理）

無音を検出・除去します。

```bash
# 構文
silence [above_periods] [duration] [threshold] [below_periods] [duration] [threshold]

# 先頭の無音除去
sox input.wav output.wav silence 1 0.1 1%

# 両端の無音除去
sox input.wav output.wav silence 1 0.1 1% reverse silence 1 0.1 1% reverse

# 無音で分割
sox input.wav output.wav silence 1 0.5 1% 1 0.5 1% : newfile : restart
```

### repeat（繰り返し）

音声を繰り返します。

```bash
# 構文
repeat count

# 3回繰り返し
sox input.wav output.wav repeat 3
```

### reverse（逆再生）

音声を逆再生します。

```bash
# 構文
reverse

sox input.wav output.wav reverse
```

---

## 7. エフェクトチェーンのベストプラクティス

### 推奨順序

```
1. ノイズ除去（noisered）
2. DCオフセット除去
3. ハイパスフィルタ（低域ノイズカット）
4. イコライザー（音質調整）
5. コンプレッサー（ダイナミクス制御）
6. ノーマライズ（最終レベル調整）
```

### ポッドキャスト処理チェーン

```bash
sox input.wav output.mp3 \
  noisered noise.prof 0.21 \
  highpass 80 \
  compand 0.3,1 6:-70,-60,-20 -5 -90 0.2 \
  norm -3
```

### 音楽マスタリングチェーン

```bash
sox input.wav output.wav \
  highpass 30 \
  bass +2 \
  treble +1 \
  compand 0.02,0.2 6:-70,-60,-20 -8 -90 0.05 \
  norm -1
```

### 音声クリーンアップチェーン

```bash
# プロファイル作成
sox input.wav -n trim 0 0.5 noiseprof noise.prof

# クリーンアップ
sox input.wav output.wav \
  noisered noise.prof 0.21 \
  highpass 100 \
  lowpass 12000 \
  norm -3
```

### 電話/ラジオ風チェーン

```bash
sox input.wav output.wav \
  lowpass 3400 \
  highpass 300 \
  compand 0.3,1 6:-70,-60,-20 -5 -90 0.2
```
