# yt-dlp 字幕取得完全ガイド

## 字幕の種類

YouTubeなどの動画サイトには2種類の字幕があります：

| 種類 | 説明 | オプション |
|------|------|-----------|
| 手動字幕 | 投稿者がアップロードした字幕 | `--write-sub` |
| 自動字幕 | 音声認識で自動生成された字幕 | `--write-auto-sub` |

## 字幕の確認

### 利用可能な字幕を一覧表示

```bash
yt-dlp --list-subs "URL"
```

出力例：
```
[youtube] Extracting URL: https://www.youtube.com/watch?v=...
[youtube] ...: Downloading webpage
Available subtitles for ...:
Language  Name                      Formats
ja        Japanese                  vtt, ttml, srv3, srv2, srv1, json3
en        English                   vtt, ttml, srv3, srv2, srv1, json3

Available automatic captions for ...:
Language  Name                      Formats
ja        Japanese (auto-generated) vtt, ttml, srv3, srv2, srv1, json3
en        English (auto-generated)  vtt, ttml, srv3, srv2, srv1, json3
ko        Korean (auto-generated)   vtt, ttml, srv3, srv2, srv1, json3
zh-Hans   Chinese (Simplified)      vtt, ttml, srv3, srv2, srv1, json3
```

## 基本的な字幕ダウンロード

### 手動字幕をダウンロード

```bash
# 動画と一緒にダウンロード
yt-dlp --write-sub "URL"

# 字幕のみダウンロード
yt-dlp --skip-download --write-sub "URL"
```

### 自動字幕をダウンロード

```bash
# 動画と一緒にダウンロード
yt-dlp --write-auto-sub "URL"

# 字幕のみダウンロード
yt-dlp --skip-download --write-auto-sub "URL"
```

### 両方ダウンロード

```bash
yt-dlp --write-sub --write-auto-sub "URL"
```

## 言語の指定

### 単一言語

```bash
# 日本語
yt-dlp --write-sub --sub-lang ja "URL"

# 英語
yt-dlp --write-sub --sub-lang en "URL"

# 中国語（簡体字）
yt-dlp --write-sub --sub-lang zh-Hans "URL"

# 韓国語
yt-dlp --write-sub --sub-lang ko "URL"
```

### 複数言語

```bash
# 日本語と英語
yt-dlp --write-sub --sub-lang "ja,en" "URL"

# 日本語、英語、韓国語
yt-dlp --write-sub --sub-lang "ja,en,ko" "URL"
```

### すべての言語

```bash
# すべての手動字幕
yt-dlp --write-sub --sub-lang all "URL"

# すべての自動字幕
yt-dlp --write-auto-sub --sub-lang all "URL"
```

### 言語コードの例

| コード | 言語 |
|--------|------|
| `ja` | 日本語 |
| `en` | 英語 |
| `en-US` | 英語（アメリカ） |
| `en-GB` | 英語（イギリス） |
| `ko` | 韓国語 |
| `zh-Hans` | 中国語（簡体字） |
| `zh-Hant` | 中国語（繁体字） |
| `es` | スペイン語 |
| `fr` | フランス語 |
| `de` | ドイツ語 |
| `pt` | ポルトガル語 |
| `ru` | ロシア語 |
| `ar` | アラビア語 |
| `hi` | ヒンディー語 |

## 字幕フォーマット

### 利用可能なフォーマット

| フォーマット | 説明 | 用途 |
|-------------|------|------|
| `vtt` | WebVTT | Web標準、ブラウザ向け |
| `srt` | SubRip | 最も広くサポート |
| `ass` / `ssa` | Advanced SubStation Alpha | 高度なスタイリング |
| `json3` | YouTube JSON | 生データ |
| `ttml` | TTML | XML形式 |
| `srv1`, `srv2`, `srv3` | YouTube内部形式 | 特殊用途 |

### フォーマット指定

```bash
# SRT形式
yt-dlp --write-sub --sub-format srt "URL"

# VTT形式
yt-dlp --write-sub --sub-format vtt "URL"

# ASS形式
yt-dlp --write-sub --sub-format ass "URL"
```

### フォーマット優先順位

```bash
# SRTを優先、なければVTT、なければbest
yt-dlp --write-sub --sub-format "srt/vtt/best" "URL"
```

### 字幕の変換

```bash
# VTTをSRTに変換
yt-dlp --write-sub --sub-format vtt --convert-subs srt "URL"

# すべての字幕をSRTに変換
yt-dlp --write-sub --sub-format best --convert-subs srt "URL"

# ASSに変換
yt-dlp --write-sub --convert-subs ass "URL"
```

## 字幕の埋め込み

### 動画に字幕を埋め込む

```bash
# 字幕を動画ファイルに埋め込む
yt-dlp --embed-subs "URL"

# 特定言語のみ埋め込み
yt-dlp --embed-subs --sub-lang ja "URL"

# 複数言語を埋め込み
yt-dlp --embed-subs --sub-lang "ja,en" "URL"
```

### 埋め込みの注意点

- MP4形式: テキストトラックとして埋め込み
- MKV形式: 複数字幕をサポート
- 再生時に字幕を切り替え可能

```bash
# MKV形式で複数字幕を埋め込み
yt-dlp --embed-subs --sub-lang "ja,en,ko" --merge-output-format mkv "URL"
```

## 高度なオプション

### 字幕ファイル名

字幕ファイルは動画と同じ名前で保存されます：

```
動画タイトル.mp4
動画タイトル.ja.srt
動画タイトル.en.srt
```

カスタマイズ：

```bash
# 出力テンプレートを指定
yt-dlp --write-sub -o "%(title)s.%(ext)s" "URL"
```

### 自動字幕の翻訳

YouTubeの自動翻訳機能を使用：

```bash
# 英語動画の日本語自動翻訳字幕
yt-dlp --write-auto-sub --sub-lang ja "URL"
```

### 字幕のみ取得（動画なし）

```bash
# 字幕ファイルのみ
yt-dlp --skip-download --write-sub "URL"

# 自動字幕ファイルのみ
yt-dlp --skip-download --write-auto-sub "URL"

# 両方
yt-dlp --skip-download --write-sub --write-auto-sub "URL"
```

## プレイリストでの字幕取得

```bash
# プレイリスト全体の字幕
yt-dlp --write-sub --sub-lang ja "PLAYLIST_URL"

# 字幕のみ一括ダウンロード
yt-dlp --skip-download --write-sub --sub-lang ja "PLAYLIST_URL"
```

## 実用的なパターン

### 日本語字幕付き動画ダウンロード

```bash
yt-dlp \
  --write-sub --write-auto-sub \
  --sub-lang ja \
  --embed-subs \
  -f "bestvideo+bestaudio" \
  "URL"
```

### 多言語字幕を別ファイルで保存

```bash
yt-dlp \
  --write-sub --write-auto-sub \
  --sub-lang "ja,en,ko" \
  --sub-format srt \
  "URL"
```

### 字幕をテキストとして抽出

```bash
# VTTファイルから純粋なテキストを抽出（タイムスタンプ除去）
yt-dlp --skip-download --write-sub --sub-format vtt "URL"
# 後処理
sed '/^[0-9]/d; /-->/d; /^$/d' video.ja.vtt > transcript.txt
```

### 字幕検索用

```bash
# すべての動画の字幕をダウンロード
yt-dlp --skip-download --write-auto-sub --sub-lang ja "PLAYLIST_URL"

# grep で検索
grep -l "キーワード" *.srt
```

## トラブルシューティング

### 字幕が見つからない

```bash
# 利用可能な字幕を確認
yt-dlp --list-subs "URL"

# 自動字幕を試す
yt-dlp --write-auto-sub "URL"

# 別の言語を試す
yt-dlp --write-auto-sub --sub-lang en "URL"
```

### 字幕が文字化け

```bash
# UTF-8エンコーディングを確認
file subtitle.srt

# 変換
iconv -f ISO-8859-1 -t UTF-8 subtitle.srt > subtitle_utf8.srt
```

### 埋め込みがうまくいかない

```bash
# ffmpegのバージョン確認
ffmpeg -version

# MKV形式を試す
yt-dlp --embed-subs --merge-output-format mkv "URL"
```

### 自動字幕の品質が低い

自動字幕は音声認識の精度に依存します。以下を試してください：

1. 手動字幕がないか確認 (`--list-subs`)
2. 別の言語の自動字幕を試す
3. 英語原音の場合、英語自動字幕の方が精度が高いことが多い

## 字幕フォーマットの詳細

### SRT形式

```
1
00:00:01,000 --> 00:00:04,000
最初のセリフ

2
00:00:05,000 --> 00:00:08,500
2番目のセリフ
```

### VTT形式

```
WEBVTT

00:00:01.000 --> 00:00:04.000
最初のセリフ

00:00:05.000 --> 00:00:08.500
2番目のセリフ
```

### ASS形式

```
[Script Info]
Title: Subtitle
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, ...
Style: Default,Arial,20,...

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:01.00,0:00:04.00,Default,,0,0,0,,最初のセリフ
```

## 関連オプション一覧

| オプション | 説明 |
|-----------|------|
| `--write-sub` | 手動字幕をダウンロード |
| `--write-auto-sub` | 自動字幕をダウンロード |
| `--sub-lang LANG` | 字幕言語を指定 |
| `--sub-format FMT` | 字幕フォーマットを指定 |
| `--convert-subs FMT` | 字幕を変換 |
| `--embed-subs` | 字幕を動画に埋め込む |
| `--list-subs` | 利用可能な字幕を表示 |
| `--skip-download` | 動画をダウンロードしない |
| `--all-subs` | すべての字幕をダウンロード（非推奨、`--sub-lang all`を使用） |
