# FFmpeg Filter Reference

フィルタ構文と実用的なサンプル集。

## 目次

- [基本構文](#基本構文)
- [ビデオフィルタ](#ビデオフィルタ)
- [音声フィルタ](#音声フィルタ)
- [複合フィルタグラフ](#複合フィルタグラフ)
- [よく使うフィルタ組み合わせ](#よく使うフィルタ組み合わせ)

---

## 基本構文

### フィルタオプション

```bash
# ビデオフィルタ
-vf "filter_name=param1=value1:param2=value2"

# 音声フィルタ
-af "audio_filter=param1=value1"

# 複合フィルタグラフ（複数入力/出力）
-filter_complex "filtergraph"
```

### フィルタチェーン

```bash
# カンマで連結（順番に適用）
-vf "filter1,filter2,filter3"

# 例: スケール → クロップ → 回転
-vf "scale=1920:1080,crop=1280:720,transpose=1"
```

### 名前付きストリーム

```bash
# 複合フィルタグラフでの命名
-filter_complex "[0:v]filter1[v1];[v1]filter2[out]"

# 入力ストリーム参照
# [0:v] = 最初の入力のビデオ
# [0:a] = 最初の入力の音声
# [1:v] = 2番目の入力のビデオ
```

---

## ビデオフィルタ

### スケーリング (scale)

```bash
# 固定解像度
-vf "scale=1920:1080"

# 幅指定でアスペクト比維持
-vf "scale=1280:-1"

# 幅指定でアスペクト比維持（偶数保証）
-vf "scale=1280:-2"

# 高さ指定でアスペクト比維持
-vf "scale=-2:720"

# 高品質スケーリング（Lanczos）
-vf "scale=1920:1080:flags=lanczos"

# Bicubic（デフォルトより高品質）
-vf "scale=1920:1080:flags=bicubic"

# 最大解像度を維持しつつスケール
-vf "scale='min(1920,iw)':'min(1080,ih)':force_original_aspect_ratio=decrease"

# 黒帯追加で指定解像度に合わせる
-vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2"
```

### クロップ (crop)

```bash
# 基本構文: crop=w:h:x:y

# 中央から640x480をクロップ
-vf "crop=640:480"

# 左上から640x480をクロップ
-vf "crop=640:480:0:0"

# 右下から640x480をクロップ
-vf "crop=640:480:iw-640:ih-480"

# 16:9にクロップ（中央）
-vf "crop=ih*16/9:ih"

# 4:3にクロップ（中央）
-vf "crop=ih*4/3:ih"

# 正方形にクロップ（中央）
-vf "crop=min(iw\,ih):min(iw\,ih)"

# 上下の黒帯を検出して自動クロップ
-vf "cropdetect"
# 結果を使って実際にクロップ
-vf "crop=1920:800:0:140"
```

### 回転・反転 (transpose, hflip, vflip)

```bash
# transpose値
# 0: 反時計回り90度 + 垂直反転
# 1: 時計回り90度
# 2: 反時計回り90度
# 3: 時計回り90度 + 垂直反転

# 時計回り90度
-vf "transpose=1"

# 反時計回り90度
-vf "transpose=2"

# 180度回転
-vf "transpose=1,transpose=1"

# 水平反転（左右反転）
-vf "hflip"

# 垂直反転（上下反転）
-vf "vflip"

# 水平・垂直両方反転（180度回転と同等）
-vf "hflip,vflip"
```

### 速度変更 (setpts, atempo)

```bash
# setpts: ビデオのタイムスタンプ操作
# PTS = Presentation Time Stamp

# 2倍速
-vf "setpts=0.5*PTS" -af "atempo=2.0"

# 0.5倍速（スローモーション）
-vf "setpts=2.0*PTS" -af "atempo=0.5"

# 4倍速（音声はatempoを2回、各2倍）
-vf "setpts=0.25*PTS" -af "atempo=2.0,atempo=2.0"

# 0.25倍速（超スロー、音声は0.5を2回）
-vf "setpts=4.0*PTS" -af "atempo=0.5,atempo=0.5"

# 音声なしで速度変更
-vf "setpts=0.5*PTS" -an
```

### フレームレート (fps)

```bash
# 30fpsに変換
-vf "fps=30"

# 24fps（映画風）
-vf "fps=24"

# 60fps
-vf "fps=60"

# フレーム補間（高品質）
-vf "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
```

### ぼかし (boxblur, gblur)

```bash
# ボックスブラー（シンプル）
-vf "boxblur=10:5"
# 第1引数: 輝度のぼかし半径
# 第2引数: 彩度のぼかし半径

# ガウシアンブラー（自然なぼかし）
-vf "gblur=sigma=10"

# 強いガウシアンブラー
-vf "gblur=sigma=20"

# モザイク効果（縮小→拡大）
-vf "scale=iw/10:ih/10,scale=iw*10:ih*10:flags=neighbor"
```

### シャープ化 (unsharp)

```bash
# 基本構文: unsharp=lx:ly:la:cx:cy:ca
# lx,ly: 輝度マトリクスサイズ（奇数）
# la: 輝度シャープ量（正=シャープ、負=ぼかし）
# cx,cy,ca: 彩度（同様）

# 軽いシャープ
-vf "unsharp=5:5:1.0:5:5:0.0"

# 中程度シャープ
-vf "unsharp=5:5:1.5:5:5:0.5"

# 強いシャープ
-vf "unsharp=5:5:2.0:5:5:1.0"

# 輝度のみシャープ
-vf "unsharp=5:5:1.5"
```

### 色補正 (eq, colorbalance, curves)

```bash
# eq: 明るさ・コントラスト・彩度
-vf "eq=brightness=0.1:contrast=1.2:saturation=1.3"
# brightness: -1.0 ~ 1.0（0=変更なし）
# contrast: 0.0 ~ 2.0（1.0=変更なし）
# saturation: 0.0 ~ 3.0（1.0=変更なし）

# 明るくする
-vf "eq=brightness=0.2"

# コントラスト上げる
-vf "eq=contrast=1.3"

# 彩度上げる
-vf "eq=saturation=1.5"

# 白黒（彩度0）
-vf "eq=saturation=0"

# セピア調
-vf "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131"

# カラーバランス
-vf "colorbalance=rs=0.3:gs=-0.1:bs=0.2"
# rs,gs,bs: シャドウの赤/緑/青
# rm,gm,bm: ミッドトーンの赤/緑/青
# rh,gh,bh: ハイライトの赤/緑/青

# 色温度調整（暖色）
-vf "colortemperature=temperature=6500"

# 色温度調整（寒色）
-vf "colortemperature=temperature=3500"

# ガンマ補正
-vf "eq=gamma=1.5"
```

### テキスト・タイムコード (drawtext)

```bash
# 基本テキスト
-vf "drawtext=text='Sample Text':fontsize=48:fontcolor=white:x=10:y=10"

# 中央配置
-vf "drawtext=text='Centered':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2"

# 下中央
-vf "drawtext=text='Bottom Center':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-th-20"

# タイムコード表示
-vf "drawtext=text='%{pts\:hms}':fontsize=36:fontcolor=white:x=10:y=10"

# フレーム番号表示
-vf "drawtext=text='Frame\: %{n}':fontsize=36:fontcolor=white:x=10:y=10"

# 日時表示
-vf "drawtext=text='%{localtime\:%Y-%m-%d %H\\\:%M\\\:%S}':fontsize=24:fontcolor=white:x=10:y=10"

# 背景付きテキスト
-vf "drawtext=text='With Background':fontsize=36:fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=5:x=10:y=10"

# フォント指定
-vf "drawtext=text='Custom Font':fontfile=/path/to/font.ttf:fontsize=48:fontcolor=white:x=10:y=10"
```

### 字幕 (subtitles, ass)

```bash
# SRT字幕焼き込み
-vf "subtitles=subtitle.srt"

# SRT字幕（スタイル指定）
-vf "subtitles=subtitle.srt:force_style='FontSize=24,PrimaryColour=&HFFFFFF&'"

# ASS字幕焼き込み（スタイル保持）
-vf "ass=subtitle.ass"

# 字幕ストリームとして追加（焼き込みではない）
ffmpeg -i video.mp4 -i subtitle.srt -c copy -c:s mov_text output.mp4
```

### オーバーレイ (overlay)

```bash
# 基本構文: overlay=x:y

# 左上にロゴ
-filter_complex "[1:v]scale=100:-1[logo];[0:v][logo]overlay=10:10"

# 右上にロゴ
-filter_complex "[1:v]scale=100:-1[logo];[0:v][logo]overlay=W-w-10:10"

# 右下にロゴ
-filter_complex "[1:v]scale=100:-1[logo];[0:v][logo]overlay=W-w-10:H-h-10"

# 左下にロゴ
-filter_complex "[1:v]scale=100:-1[logo];[0:v][logo]overlay=10:H-h-10"

# 中央にロゴ
-filter_complex "[1:v]scale=200:-1[logo];[0:v][logo]overlay=(W-w)/2:(H-h)/2"

# 半透明ロゴ（50%）
-filter_complex "[1:v]scale=200:-1,format=rgba,colorchannelmixer=aa=0.5[logo];[0:v][logo]overlay=(W-w)/2:(H-h)/2"

# 全画面オーバーレイ（透過PNG）
-filter_complex "[0:v][1:v]overlay=0:0"
```

### フェード (fade)

```bash
# フェードイン（最初の2秒）
-vf "fade=t=in:st=0:d=2"

# フェードアウト（動画長が60秒の場合、最後の2秒）
-vf "fade=t=out:st=58:d=2"

# フェードイン・アウト両方
-vf "fade=t=in:st=0:d=2,fade=t=out:st=58:d=2"

# 黒からフェードイン
-vf "fade=t=in:st=0:d=2:color=black"

# 白へフェードアウト
-vf "fade=t=out:st=58:d=2:color=white"
```

### デインターレース (yadif)

```bash
# 標準デインターレース
-vf "yadif"

# フレームレート維持（インターレースフィールドを保持）
-vf "yadif=mode=0"

# フレームレート2倍（各フィールドをフレームに）
-vf "yadif=mode=1"

# bwdif（品質優先）
-vf "bwdif"
```

### ノイズ除去 (hqdn3d, nlmeans)

```bash
# hqdn3d（高品質3Dノイズ除去）
-vf "hqdn3d=4:3:6:4.5"
# 引数: luma_spatial:chroma_spatial:luma_tmp:chroma_tmp

# 軽いノイズ除去
-vf "hqdn3d=2:2:4:3"

# 強いノイズ除去
-vf "hqdn3d=8:6:12:9"

# nlmeans（Non-local Means、高品質・遅い）
-vf "nlmeans=s=3.5:p=7:r=15"
# s: denoising strength
# p: patch size
# r: research window size
```

### 手ブレ補正 (vidstabdetect, vidstabtransform)

```bash
# Step 1: 解析（transforms.trfファイル生成）
ffmpeg -i input.mp4 -vf "vidstabdetect=shakiness=5:accuracy=15" -f null -

# Step 2: 補正適用
ffmpeg -i input.mp4 -vf "vidstabtransform=smoothing=30:input=transforms.trf" output.mp4

# ワンパスで実行（低品質）
ffmpeg -i input.mp4 -vf "vidstabdetect=shakiness=5:accuracy=15:result=transforms.trf" -f null - && \
ffmpeg -i input.mp4 -vf "vidstabtransform=smoothing=30:input=transforms.trf" output.mp4
```

---

## 音声フィルタ

### 音量 (volume)

```bash
# 音量2倍
-af "volume=2.0"

# 音量半分
-af "volume=0.5"

# dB指定（+10dB）
-af "volume=10dB"

# dB指定（-6dB）
-af "volume=-6dB"
```

### 正規化 (loudnorm)

```bash
# EBU R128正規化（放送標準）
-af "loudnorm=I=-16:TP=-1.5:LRA=11"
# I: integrated loudness target (LUFS)
# TP: true peak target (dBTP)
# LRA: loudness range target (LU)

# 2パス正規化（より正確）
# Pass 1: 分析
ffmpeg -i input.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1 | grep -A20 "output_"
# Pass 2: 適用（分析結果を使用）
ffmpeg -i input.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=-23:measured_TP=-2:measured_LRA=15:measured_thresh=-34" output.mp4
```

### イコライザー (equalizer, bass, treble)

```bash
# 特定周波数をブースト/カット
-af "equalizer=f=1000:width_type=h:width=200:g=5"
# f: 中心周波数
# width_type: h=Hz, q=Q factor, o=octave
# width: 幅
# g: ゲイン(dB)

# 低音強調（100Hz +5dB）
-af "equalizer=f=100:width_type=h:width=200:g=5"

# 高音強調（3kHz +3dB）
-af "equalizer=f=3000:width_type=h:width=2000:g=3"

# 低音ブースト（簡易）
-af "bass=g=10"

# 高音ブースト（簡易）
-af "treble=g=10"

# 複数バンド
-af "equalizer=f=100:width_type=h:width=200:g=5,equalizer=f=3000:width_type=h:width=2000:g=3"
```

### フェード (afade)

```bash
# 音声フェードイン（最初の3秒）
-af "afade=t=in:st=0:d=3"

# 音声フェードアウト（57秒から3秒）
-af "afade=t=out:st=57:d=3"

# フェードイン・アウト両方
-af "afade=t=in:st=0:d=3,afade=t=out:st=57:d=3"
```

### リサンプリング (aresample)

```bash
# サンプルレート変換
-af "aresample=44100"

# 高品質リサンプリング
-af "aresample=48000:resampler=soxr"
```

### チャンネル操作 (pan, channelmap)

```bash
# ステレオ→モノラル
-af "pan=mono|c0=0.5*c0+0.5*c1"

# 左チャンネルのみ
-af "pan=mono|c0=c0"

# 右チャンネルのみ
-af "pan=mono|c0=c1"

# チャンネル入れ替え
-af "pan=stereo|c0=c1|c1=c0"

# モノラル→ステレオ
-af "pan=stereo|c0=c0|c1=c0"
```

---

## 複合フィルタグラフ

### Picture-in-Picture

```bash
# 右下に小窓
ffmpeg -i main.mp4 -i pip.mp4 -filter_complex \
  "[1:v]scale=320:-1[pip];[0:v][pip]overlay=W-w-10:H-h-10" \
  output.mp4

# 左上に小窓（枠付き）
ffmpeg -i main.mp4 -i pip.mp4 -filter_complex \
  "[1:v]scale=320:-1,pad=w=iw+4:h=ih+4:x=2:y=2:color=white[pip];[0:v][pip]overlay=10:10" \
  output.mp4
```

### グリッド表示（2x2）

```bash
ffmpeg -i input1.mp4 -i input2.mp4 -i input3.mp4 -i input4.mp4 -filter_complex \
  "[0:v]scale=640:360[v0];[1:v]scale=640:360[v1];[2:v]scale=640:360[v2];[3:v]scale=640:360[v3];\
   [v0][v1]hstack[top];[v2][v3]hstack[bottom];[top][bottom]vstack" \
  output.mp4
```

### 横並び（Side by Side）

```bash
ffmpeg -i left.mp4 -i right.mp4 -filter_complex \
  "[0:v]scale=640:-1[left];[1:v]scale=640:-1[right];[left][right]hstack" \
  output.mp4
```

### 縦並び

```bash
ffmpeg -i top.mp4 -i bottom.mp4 -filter_complex \
  "[0:v]scale=1280:-1[top];[1:v]scale=1280:-1[bottom];[top][bottom]vstack" \
  output.mp4
```

### 音声ミックス

```bash
# 動画の音声 + BGM
ffmpeg -i video.mp4 -i bgm.mp3 -filter_complex \
  "[0:a]volume=1.0[va];[1:a]volume=0.3[bgm];[va][bgm]amix=inputs=2:duration=first" \
  -c:v copy output.mp4

# 2つの音声を均等ミックス
ffmpeg -i audio1.mp3 -i audio2.mp3 -filter_complex \
  "[0:a][1:a]amix=inputs=2:duration=longest" \
  output.mp3
```

### クロスフェード

```bash
# ビデオクロスフェード（1秒）
ffmpeg -i video1.mp4 -i video2.mp4 -filter_complex \
  "[0:v][1:v]xfade=transition=fade:duration=1:offset=4[v]" \
  -map "[v]" output.mp4

# オーディオクロスフェード
ffmpeg -i audio1.mp3 -i audio2.mp3 -filter_complex \
  "[0:a][1:a]acrossfade=d=1:c1=tri:c2=tri" \
  output.mp3
```

---

## よく使うフィルタ組み合わせ

### Web用最適化

```bash
-vf "scale=1280:-2:flags=lanczos,format=yuv420p"
```

### SNS用（正方形）

```bash
-vf "crop=min(iw\,ih):min(iw\,ih),scale=1080:1080"
```

### 縦動画（9:16）

```bash
-vf "crop=ih*9/16:ih,scale=1080:1920"
```

### 映画風（レターボックス）

```bash
-vf "scale=1920:-1,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black"
```

### 高品質GIF

```bash
-filter_complex "[0:v]fps=10,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=single[p];[b][p]paletteuse=new=1"
```

### ウォーターマーク + テキスト

```bash
-filter_complex "[1:v]scale=80:-1,format=rgba,colorchannelmixer=aa=0.7[logo];[0:v][logo]overlay=W-w-10:H-h-10,drawtext=text='© 2025':fontsize=20:fontcolor=white@0.7:x=10:y=H-th-10"
```
