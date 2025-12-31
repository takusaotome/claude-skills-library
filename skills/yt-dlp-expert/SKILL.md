---
name: yt-dlp-expert
description: yt-dlpを使用した動画ダウンロードの専門スキル。YouTube、ニコニコ動画、Twitter/X、TikTok等1000以上のサイトから動画・音声・字幕をダウンロード。フォーマット選択、プレイリスト処理、メタデータ抽出を効率的に支援。Use when downloading videos, extracting audio, getting subtitles, or fetching metadata from YouTube and other video sites.
---

# yt-dlp Expert

## 概要

yt-dlpは、youtube-dlから派生した強力なコマンドラインダウンローダーです。YouTube、ニコニコ動画、Twitter/X、TikTok、Instagram、Vimeo、Twitch、bilibiliなど1000以上のサイトから動画・音声・字幕をダウンロードできます。

**主な特徴：**
- 高速ダウンロード（並列接続、フラグメント処理）
- 柔軟なフォーマット選択（解像度、コーデック、ファイルサイズ）
- 字幕取得（自動生成・手動、多言語対応）
- メタデータ抽出（JSON出力、サムネイル）
- プレイリスト・チャンネル一括処理
- Cookie認証対応（メンバー限定・年齢制限コンテンツ）

## このスキルを使うタイミング

以下のような場面で発動します：

**発動トリガー例：**
- 「YouTube動画をダウンロードしたい」
- 「動画から音声だけ抽出したい」
- 「字幕をダウンロードしたい」
- 「プレイリストを一括ダウンロードしたい」
- 「動画のメタデータを取得したい」
- 「yt-dlpのコマンドを教えて」
- 「最高画質でダウンロードするには？」
- 「Twitter/Xの動画を保存したい」

## インストール

### macOS (Homebrew)
```bash
brew install yt-dlp
```

### Linux / macOS (pip)
```bash
pip install yt-dlp
# または
pip3 install yt-dlp
```

### Windows (winget)
```bash
winget install yt-dlp
```

### Windows (Scoop)
```bash
scoop install yt-dlp
```

### 直接ダウンロード
```bash
# Linux/macOS
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o ~/.local/bin/yt-dlp
chmod +x ~/.local/bin/yt-dlp

# Windows
# GitHubリリースページからyt-dlp.exeをダウンロード
```

### 更新
```bash
yt-dlp -U
```

### ffmpegのインストール（推奨）

音声抽出や動画結合にはffmpegが必要です：

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows (winget)
winget install ffmpeg
```

## 基本操作

### 単一動画のダウンロード
```bash
# 最もシンプルな使い方
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"

# 保存先を指定
yt-dlp -P ~/Downloads "URL"
```

### フォーマット確認
```bash
# 利用可能なフォーマット一覧を表示
yt-dlp -F "URL"
```

出力例：
```
ID      EXT   RESOLUTION FPS CH │   FILESIZE   TBR PROTO │ VCODEC          VBR ACODEC      ABR
─────────────────────────────────────────────────────────────────────────────────────────────
sb2     mhtml 48x27        0    │                  mhtml │ images
...
140     m4a   audio only       2 │   3.51MiB   130k https │ audio only          mp4a.40.2  130k
251     webm  audio only       2 │   3.75MiB   139k https │ audio only          opus       139k
136     mp4   1280x720    30    │   7.87MiB   292k https │ avc1.64001f    292k video only
137     mp4   1920x1080   30    │  14.25MiB   529k https │ avc1.640028    529k video only
```

### フォーマット選択
```bash
# 特定のフォーマットIDを指定
yt-dlp -f 137+140 "URL"

# 最高画質（映像+音声を自動結合）
yt-dlp -f "bestvideo+bestaudio/best" "URL"

# 最高画質（MP4形式限定）
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" "URL"

# 解像度指定（1080p以下で最高）
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" "URL"

# 720p固定
yt-dlp -f "bestvideo[height=720]+bestaudio" "URL"

# ファイルサイズ制限（100MB以下）
yt-dlp -f "best[filesize<100M]" "URL"
```

### 音声のみ抽出
```bash
# 音声のみダウンロード（最高音質）
yt-dlp -f "bestaudio" "URL"

# MP3に変換（ffmpeg必要）
yt-dlp -x --audio-format mp3 "URL"

# 音質指定（0=最高、9=最低）
yt-dlp -x --audio-format mp3 --audio-quality 0 "URL"

# M4A形式
yt-dlp -x --audio-format m4a "URL"

# FLAC形式（ロスレス）
yt-dlp -x --audio-format flac "URL"

# Opus形式（高効率）
yt-dlp -x --audio-format opus "URL"
```

## 字幕のダウンロード

### 利用可能な字幕を確認
```bash
yt-dlp --list-subs "URL"
```

### 字幕をダウンロード
```bash
# 自動生成字幕を含めてダウンロード
yt-dlp --write-auto-sub "URL"

# 手動字幕をダウンロード
yt-dlp --write-sub "URL"

# 両方ダウンロード
yt-dlp --write-sub --write-auto-sub "URL"

# 字幕のみダウンロード（動画なし）
yt-dlp --skip-download --write-sub "URL"
yt-dlp --skip-download --write-auto-sub "URL"
```

### 言語を指定
```bash
# 日本語字幕
yt-dlp --write-sub --sub-lang ja "URL"

# 英語字幕
yt-dlp --write-sub --sub-lang en "URL"

# 複数言語
yt-dlp --write-sub --sub-lang "ja,en,ko" "URL"

# すべての言語
yt-dlp --write-sub --sub-lang all "URL"
```

### 字幕フォーマット指定
```bash
# SRT形式
yt-dlp --write-sub --sub-format srt "URL"

# VTT形式
yt-dlp --write-sub --sub-format vtt "URL"

# ASS形式
yt-dlp --write-sub --sub-format ass "URL"

# 自動変換（SRTがない場合VTTから変換）
yt-dlp --write-sub --sub-format "srt/vtt/best" --convert-subs srt "URL"
```

### 字幕を動画に埋め込む
```bash
# 字幕を動画ファイルに埋め込む
yt-dlp --embed-subs "URL"

# 日本語字幕のみ埋め込み
yt-dlp --embed-subs --sub-lang ja "URL"
```

## メタデータの取得

### 動画情報をJSON出力
```bash
# 動画情報を標準出力
yt-dlp -j "URL"

# ファイルに保存
yt-dlp -j "URL" > video_info.json

# プレイリスト全体の情報
yt-dlp -J "URL" > playlist_info.json

# 整形して出力
yt-dlp -j "URL" | jq .

# 特定フィールドのみ
yt-dlp -j "URL" | jq '{title, duration, view_count}'
```

### 特定情報の抽出
```bash
# タイトルのみ
yt-dlp --print title "URL"

# タイトルと再生時間
yt-dlp --print "%(title)s - %(duration)s秒" "URL"

# サムネイルURL
yt-dlp --print thumbnail "URL"

# アップロード日
yt-dlp --print upload_date "URL"
```

### サムネイル取得
```bash
# サムネイルをダウンロード
yt-dlp --write-thumbnail "URL"

# 動画なし、サムネイルのみ
yt-dlp --skip-download --write-thumbnail "URL"

# 動画にサムネイルを埋め込む
yt-dlp --embed-thumbnail "URL"
```

### 説明文の保存
```bash
# 説明文を.descriptionファイルに保存
yt-dlp --write-description "URL"
```

## プレイリスト処理

### プレイリスト全体をダウンロード
```bash
# プレイリスト全体
yt-dlp "https://www.youtube.com/playlist?list=PLAYLIST_ID"

# 並列ダウンロード（高速化）
yt-dlp -N 4 "PLAYLIST_URL"
```

### 範囲指定
```bash
# 最初の5本
yt-dlp --playlist-items 1:5 "PLAYLIST_URL"

# 10番目から15番目
yt-dlp --playlist-items 10:15 "PLAYLIST_URL"

# 特定のインデックス
yt-dlp --playlist-items 1,3,5,7 "PLAYLIST_URL"

# 最後の3本
yt-dlp --playlist-items -3: "PLAYLIST_URL"

# 最初と最後だけ
yt-dlp --playlist-items 1,-1 "PLAYLIST_URL"
```

### プレイリスト処理オプション
```bash
# プレイリストを逆順で
yt-dlp --playlist-reverse "PLAYLIST_URL"

# ランダム順
yt-dlp --playlist-random "PLAYLIST_URL"

# 動画として扱う（プレイリストでなく）
yt-dlp --no-playlist "VIDEO_URL_WITH_LIST_PARAM"

# プレイリストとして扱う
yt-dlp --yes-playlist "URL"
```

## ファイル名テンプレート

### 基本的なテンプレート
```bash
# タイトル（デフォルト）
yt-dlp -o "%(title)s.%(ext)s" "URL"

# タイトル_ID形式
yt-dlp -o "%(title)s_%(id)s.%(ext)s" "URL"

# 日付_タイトル形式
yt-dlp -o "%(upload_date)s_%(title)s.%(ext)s" "URL"

# チャンネル名/タイトル形式
yt-dlp -o "%(channel)s/%(title)s.%(ext)s" "URL"
```

### プレイリスト用テンプレート
```bash
# プレイリスト名/番号_タイトル
yt-dlp -o "%(playlist)s/%(playlist_index)s_%(title)s.%(ext)s" "PLAYLIST_URL"

# 3桁ゼロパディング
yt-dlp -o "%(playlist)s/%(playlist_index)03d_%(title)s.%(ext)s" "PLAYLIST_URL"
```

### よく使うテンプレート変数
| 変数 | 説明 |
|------|------|
| `%(title)s` | 動画タイトル |
| `%(id)s` | 動画ID |
| `%(ext)s` | 拡張子 |
| `%(channel)s` | チャンネル名 |
| `%(upload_date)s` | アップロード日 (YYYYMMDD) |
| `%(upload_date>%Y-%m-%d)s` | 日付フォーマット指定 |
| `%(duration)s` | 再生時間（秒） |
| `%(view_count)s` | 再生回数 |
| `%(playlist)s` | プレイリスト名 |
| `%(playlist_index)s` | プレイリスト内番号 |
| `%(playlist_count)s` | プレイリスト内総数 |
| `%(resolution)s` | 解像度 |

### ファイル名の安全処理
```bash
# 特殊文字を置換
yt-dlp -o "%(title)s.%(ext)s" --restrict-filenames "URL"

# Windowsで使えない文字を置換
yt-dlp -o "%(title)s.%(ext)s" --windows-filenames "URL"
```

## 認証・Cookie

### ブラウザからCookieを使用
```bash
# Chrome
yt-dlp --cookies-from-browser chrome "URL"

# Firefox
yt-dlp --cookies-from-browser firefox "URL"

# Safari
yt-dlp --cookies-from-browser safari "URL"

# Edge
yt-dlp --cookies-from-browser edge "URL"

# Brave
yt-dlp --cookies-from-browser brave "URL"
```

### Cookieファイルを使用
```bash
# Netscape形式のcookies.txtを使用
yt-dlp --cookies cookies.txt "URL"
```

### 認証が必要なケース
- メンバーシップ/有料コンテンツ
- 年齢制限動画
- 非公開プレイリスト
- ログインユーザー限定コンテンツ

### ユーザー名・パスワード認証（一部サイト）
```bash
# ユーザー名とパスワード
yt-dlp -u USERNAME -p PASSWORD "URL"

# 対話的にパスワード入力
yt-dlp -u USERNAME "URL"
```

## よく使うパターン

### YouTube高画質ダウンロード
```bash
# 最高画質でMP4形式
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" \
  --merge-output-format mp4 \
  -o "%(title)s.%(ext)s" \
  "URL"
```

### YouTube音楽ダウンロード
```bash
# MP3最高音質
yt-dlp -x --audio-format mp3 --audio-quality 0 \
  --embed-thumbnail \
  -o "%(title)s.%(ext)s" \
  "URL"
```

### プレイリスト一括処理
```bash
# 音声のみ、番号付きファイル名
yt-dlp -x --audio-format mp3 \
  -o "%(playlist)s/%(playlist_index)03d_%(title)s.%(ext)s" \
  "PLAYLIST_URL"
```

### 日本語字幕付きダウンロード
```bash
yt-dlp --write-sub --write-auto-sub \
  --sub-lang ja \
  --embed-subs \
  -f "bestvideo+bestaudio" \
  "URL"
```

### Twitter/X動画保存
```bash
yt-dlp -o "%(uploader)s_%(id)s.%(ext)s" "TWITTER_URL"
```

### ニコニコ動画
```bash
# Cookie認証が必要
yt-dlp --cookies-from-browser chrome "https://www.nicovideo.jp/watch/sm..."
```

### TikTok
```bash
yt-dlp -o "%(uploader)s_%(id)s.%(ext)s" "TIKTOK_URL"
```

### アーカイブ（重複回避）
```bash
# ダウンロード済みを記録
yt-dlp --download-archive downloaded.txt "URL"

# 次回実行時はスキップ
yt-dlp --download-archive downloaded.txt "PLAYLIST_URL"
```

## トラブルシューティング

### 一般的な問題

**「Video unavailable」エラー**
```bash
# 年齢制限の可能性 → Cookie認証
yt-dlp --cookies-from-browser chrome "URL"

# 地域制限の可能性 → プロキシ使用
yt-dlp --proxy "socks5://127.0.0.1:1080" "URL"
```

**「Unable to extract」エラー**
```bash
# yt-dlpを最新版に更新
yt-dlp -U

# キャッシュをクリア
yt-dlp --rm-cache-dir
```

**ダウンロードが遅い**
```bash
# 並列接続数を増やす
yt-dlp -N 4 "URL"

# 別フォーマットを試す
yt-dlp -f "best" "URL"
```

**ffmpegエラー**
```bash
# ffmpegがインストールされているか確認
ffmpeg -version

# ffmpegのパスを明示的に指定
yt-dlp --ffmpeg-location /usr/local/bin/ffmpeg "URL"
```

**Cookieが読み取れない**
```bash
# ブラウザを閉じてから再試行
# または、別のブラウザを試す
yt-dlp --cookies-from-browser firefox "URL"
```

### デバッグ
```bash
# 詳細なログを出力
yt-dlp -v "URL"

# さらに詳細
yt-dlp -v --print-traffic "URL"

# ドライラン（実際にはダウンロードしない）
yt-dlp -s "URL"
```

## 設定ファイル

よく使うオプションは設定ファイルに保存できます：

### 設定ファイルの場所
- Linux/macOS: `~/.config/yt-dlp/config`
- Windows: `%APPDATA%\yt-dlp\config.txt`

### 設定例
```
# ~/.config/yt-dlp/config

# デフォルト出力先
-P ~/Downloads/yt-dlp

# ファイル名テンプレート
-o %(title)s.%(ext)s

# 最高画質
-f bestvideo+bestaudio/best

# 字幕を埋め込み
--embed-subs
--sub-lang ja,en

# サムネイル埋め込み
--embed-thumbnail

# アーカイブ
--download-archive ~/Downloads/yt-dlp/archive.txt
```

## リソース

### 公式ドキュメント
- GitHub: https://github.com/yt-dlp/yt-dlp
- サポートサイト一覧: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

### このスキルに含まれるリファレンス
- `references/download_options.md` - フォーマット選択の詳細ガイド
- `references/subtitle_extraction.md` - 字幕取得の完全ガイド
- `references/authentication.md` - Cookie認証の詳細設定
