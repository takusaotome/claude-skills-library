# yt-dlp フォーマット選択詳細ガイド

## フォーマット選択の基本

yt-dlpのフォーマット選択（`-f`オプション）は、動画のダウンロード品質とファイル形式を細かく制御するための強力な機能です。

## フォーマット一覧の確認

```bash
# 利用可能なすべてのフォーマットを表示
yt-dlp -F "URL"

# 短縮形式で表示
yt-dlp --list-formats "URL"
```

### 出力の読み方

```
ID      EXT   RESOLUTION FPS CH │   FILESIZE   TBR PROTO │ VCODEC          VBR ACODEC      ABR  ASR MORE INFO
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
sb2     mhtml 48x27        0    │                  mhtml │ images                              storyboard
sb1     mhtml 80x45        1    │                  mhtml │ images                              storyboard
sb0     mhtml 160x90       1    │                  mhtml │ images                              storyboard
233     mp4   audio only        │                  m3u8  │ audio only          mp4a.40.5
234     mp4   audio only        │                  m3u8  │ audio only          mp4a.40.2
139     m4a   audio only       2 │    1.56MiB    49k https │ audio only          mp4a.40.5   49k 22k low, m4a_dash
140     m4a   audio only       2 │    4.13MiB   130k https │ audio only          mp4a.40.2  130k 44k medium, m4a_dash
251     webm  audio only       2 │    3.58MiB   113k https │ audio only          opus       113k 48k medium, webm_dash
394     mp4   256x144     30    │    1.55MiB    49k https │ av01.0.00M.08   49k video only          144p, mp4_dash
160     mp4   256x144     30    │  949.91KiB    29k https │ avc1.4d400c     29k video only          144p, mp4_dash
278     webm  256x144     30    │    1.24MiB    39k https │ vp9             39k video only          144p, webm_dash
```

| カラム | 説明 |
|--------|------|
| ID | フォーマットID（`-f`で指定する値） |
| EXT | ファイル拡張子 |
| RESOLUTION | 解像度（`audio only`は音声のみ） |
| FPS | フレームレート |
| CH | 音声チャンネル数 |
| FILESIZE | ファイルサイズ |
| TBR | 総ビットレート |
| PROTO | プロトコル（https, m3u8等） |
| VCODEC | 映像コーデック |
| VBR | 映像ビットレート |
| ACODEC | 音声コーデック |
| ABR | 音声ビットレート |

## フォーマット選択構文

### 基本構文

```bash
# 単一フォーマット
yt-dlp -f FORMAT_ID "URL"

# 映像+音声の結合
yt-dlp -f VIDEO_ID+AUDIO_ID "URL"

# フォールバック（前者がなければ後者）
yt-dlp -f "FORMAT1/FORMAT2/FORMAT3" "URL"
```

### フォーマットID

| ID | 説明 |
|----|------|
| `best` | 最高品質（映像+音声が含まれる単一ファイル） |
| `worst` | 最低品質 |
| `bestvideo` | 最高品質の映像のみ |
| `bestaudio` | 最高品質の音声のみ |
| `worstvideo` | 最低品質の映像のみ |
| `worstaudio` | 最低品質の音声のみ |

### 条件フィルタ

フォーマットに条件を付けて絞り込めます：

```bash
# 高さ（解像度）
yt-dlp -f "bestvideo[height<=720]" "URL"
yt-dlp -f "bestvideo[height=1080]" "URL"
yt-dlp -f "bestvideo[height>=1080]" "URL"

# 幅
yt-dlp -f "bestvideo[width<=1920]" "URL"

# 拡張子
yt-dlp -f "bestvideo[ext=mp4]" "URL"
yt-dlp -f "bestaudio[ext=m4a]" "URL"

# コーデック
yt-dlp -f "bestvideo[vcodec^=avc1]" "URL"  # H.264
yt-dlp -f "bestvideo[vcodec^=vp9]" "URL"   # VP9
yt-dlp -f "bestvideo[vcodec^=av01]" "URL"  # AV1

# ファイルサイズ
yt-dlp -f "best[filesize<100M]" "URL"

# ビットレート
yt-dlp -f "bestvideo[tbr<=5000]" "URL"

# FPS
yt-dlp -f "bestvideo[fps<=30]" "URL"
yt-dlp -f "bestvideo[fps=60]" "URL"
```

### 演算子

| 演算子 | 説明 |
|--------|------|
| `=` | 等しい |
| `!=` | 等しくない |
| `<` | より小さい |
| `<=` | 以下 |
| `>` | より大きい |
| `>=` | 以上 |
| `^=` | で始まる |
| `$=` | で終わる |
| `*=` | を含む |
| `~=` | 正規表現マッチ |

### 複合条件

```bash
# AND条件（すべて満たす）
yt-dlp -f "bestvideo[height<=1080][ext=mp4]" "URL"

# 映像と音声の組み合わせ
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" "URL"

# フォールバック付き
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best" "URL"
```

## よく使うフォーマット指定パターン

### 最高品質

```bash
# 絶対最高（WebMになる可能性あり）
yt-dlp -f "bestvideo+bestaudio/best" "URL"

# MP4形式で最高
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" "URL"
```

### 解像度別

```bash
# 4K (2160p)
yt-dlp -f "bestvideo[height<=2160]+bestaudio/best" "URL"

# 1080p
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best" "URL"

# 720p
yt-dlp -f "bestvideo[height<=720]+bestaudio/best" "URL"

# 480p
yt-dlp -f "bestvideo[height<=480]+bestaudio/best" "URL"

# 360p以下（データ節約）
yt-dlp -f "bestvideo[height<=360]+bestaudio/best" "URL"
```

### 特定解像度を優先

```bash
# 1080pを優先、なければ720p、それもなければ最高
yt-dlp -f "bestvideo[height=1080]+bestaudio/bestvideo[height=720]+bestaudio/bestvideo+bestaudio" "URL"
```

### コーデック指定

```bash
# H.264（互換性重視）
yt-dlp -f "bestvideo[vcodec^=avc1]+bestaudio/best" "URL"

# VP9（品質重視）
yt-dlp -f "bestvideo[vcodec^=vp9]+bestaudio/best" "URL"

# AV1（最新、高効率）
yt-dlp -f "bestvideo[vcodec^=av01]+bestaudio/best" "URL"
```

### ファイルサイズ制限

```bash
# 50MB以下
yt-dlp -f "best[filesize<50M]/best" "URL"

# 100MB以下で最高画質
yt-dlp -f "bestvideo[filesize<100M]+bestaudio/best[filesize<100M]" "URL"
```

## 出力形式の指定

### マージ出力形式

```bash
# MP4形式で出力（結合時）
yt-dlp -f "bestvideo+bestaudio" --merge-output-format mp4 "URL"

# MKV形式で出力
yt-dlp -f "bestvideo+bestaudio" --merge-output-format mkv "URL"

# WebM形式で出力
yt-dlp -f "bestvideo+bestaudio" --merge-output-format webm "URL"
```

### 再エンコードなし結合

```bash
# コーデック互換のあるフォーマットを選んで結合
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" --merge-output-format mp4 "URL"
```

## 音声のみダウンロード

### 基本

```bash
# 最高音質
yt-dlp -f "bestaudio" "URL"

# 特定フォーマット
yt-dlp -f "bestaudio[ext=m4a]" "URL"
yt-dlp -f "bestaudio[ext=webm]" "URL"
```

### 音声抽出と変換

```bash
# MP3に変換
yt-dlp -x --audio-format mp3 "URL"

# M4A（変換なし、互換性高い）
yt-dlp -x --audio-format m4a "URL"

# FLAC（ロスレス）
yt-dlp -x --audio-format flac "URL"

# Opus（高効率）
yt-dlp -x --audio-format opus "URL"

# WAV（無圧縮）
yt-dlp -x --audio-format wav "URL"

# Vorbis
yt-dlp -x --audio-format vorbis "URL"
```

### 音質指定

```bash
# 音質（0=最高、9=最低、5=デフォルト）
yt-dlp -x --audio-format mp3 --audio-quality 0 "URL"
yt-dlp -x --audio-format mp3 --audio-quality 128K "URL"  # 128kbps
yt-dlp -x --audio-format mp3 --audio-quality 320K "URL"  # 320kbps
```

## 特殊なユースケース

### ライブ配信

```bash
# ライブ配信の開始から録画
yt-dlp --live-from-start "LIVE_URL"

# 途中から録画開始
yt-dlp "LIVE_URL"
```

### 年齢制限/メンバー限定

```bash
# Cookie認証と組み合わせ
yt-dlp --cookies-from-browser chrome -f "bestvideo+bestaudio" "URL"
```

### 複数フォーマットダウンロード

```bash
# 複数フォーマットを同時に
yt-dlp -f "bestvideo,bestaudio" "URL"

# 映像と音声を別ファイルに
yt-dlp -f "bestvideo" "URL"
yt-dlp -f "bestaudio" "URL"
```

## デバッグ

```bash
# 選択されるフォーマットを確認（ダウンロードなし）
yt-dlp -f "bestvideo+bestaudio" --print filename -s "URL"

# フォーマット選択の詳細を表示
yt-dlp -f "bestvideo+bestaudio" -v "URL" 2>&1 | grep -i format
```

## 注意事項

1. **互換性**: `bestvideo[ext=mp4]+bestaudio[ext=m4a]`は再エンコードなしでMP4に結合できる
2. **AV1/VP9**: 高品質だが再生デバイスの対応を確認
3. **m3u8**: HLS形式、ffmpegが必要
4. **Premium品質**: YouTubeプレミアム限定の高品質フォーマットはCookie認証が必要
