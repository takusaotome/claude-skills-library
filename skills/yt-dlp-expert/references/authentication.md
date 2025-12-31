# yt-dlp 認証・Cookie設定ガイド

## 認証が必要なケース

以下のコンテンツには認証（ログイン）が必要です：

- **YouTubeメンバーシップ限定動画**
- **年齢制限のある動画**
- **非公開・限定公開のプレイリスト**
- **ニコニコ動画の高画質版**
- **有料コンテンツ**
- **ログインユーザー限定コンテンツ**

## ブラウザからCookieを使用（推奨）

最も簡単で安全な方法です。ブラウザでログイン済みの状態を利用します。

### 基本コマンド

```bash
# Chrome
yt-dlp --cookies-from-browser chrome "URL"

# Firefox
yt-dlp --cookies-from-browser firefox "URL"

# Safari (macOS)
yt-dlp --cookies-from-browser safari "URL"

# Edge
yt-dlp --cookies-from-browser edge "URL"

# Brave
yt-dlp --cookies-from-browser brave "URL"

# Opera
yt-dlp --cookies-from-browser opera "URL"

# Chromium
yt-dlp --cookies-from-browser chromium "URL"

# Vivaldi
yt-dlp --cookies-from-browser vivaldi "URL"
```

### プロファイル指定

複数のブラウザプロファイルがある場合：

```bash
# Chrome の特定プロファイル
yt-dlp --cookies-from-browser chrome:Profile1 "URL"

# Firefox の特定プロファイル
yt-dlp --cookies-from-browser firefox:default-release "URL"
```

### キーチェーン/キーリング

macOSやLinuxでは、ブラウザがシステムのキーチェーンを使用している場合があります：

```bash
# macOS Keychain アクセスが必要な場合
yt-dlp --cookies-from-browser chrome "URL"
# → パスワード入力を求められることがあります

# Linuxでgnome-keyringを使用
yt-dlp --cookies-from-browser chrome "URL"
```

### コンテナ/プロファイル（Firefox）

```bash
# Firefoxのコンテナを指定
yt-dlp --cookies-from-browser firefox::Container "URL"
```

## Cookieファイルを使用

ブラウザからCookieをエクスポートして使用する方法です。

### Cookieファイルの形式

Netscape形式（cookies.txt）：

```
# Netscape HTTP Cookie File
.youtube.com	TRUE	/	TRUE	1735689600	LOGIN_INFO	AFmmF2swRQ...
.youtube.com	TRUE	/	FALSE	1735689600	PREF	f6=40000000
.youtube.com	TRUE	/	TRUE	1735689600	SID	g.a000jg...
```

### Cookieファイルの取得方法

#### ブラウザ拡張機能を使用（推奨）

**Chrome:**
- [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
- [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)

**Firefox:**
- [cookies.txt](https://addons.mozilla.org/firefox/addon/cookies-txt/)

#### 手順

1. 対象サイト（YouTube等）にログイン
2. 拡張機能でCookieをエクスポート
3. `cookies.txt`として保存
4. yt-dlpで使用：

```bash
yt-dlp --cookies cookies.txt "URL"
```

### Cookieファイルの注意点

- **有効期限**: Cookieには有効期限があります
- **セキュリティ**: Cookieファイルは認証情報を含むため、安全に保管してください
- **更新**: ログアウトするとCookieは無効になります

## ユーザー名・パスワード認証

一部のサイトでは直接認証できます：

```bash
# ユーザー名とパスワード
yt-dlp -u USERNAME -p PASSWORD "URL"

# 対話的にパスワード入力
yt-dlp -u USERNAME "URL"

# .netrcファイルから認証情報を読み込み
yt-dlp --netrc "URL"
```

### .netrcファイル

`~/.netrc`（Linux/macOS）または`%HOME%\_netrc`（Windows）に認証情報を保存：

```
machine youtube login YOUR_EMAIL password YOUR_PASSWORD
machine niconico login YOUR_EMAIL password YOUR_PASSWORD
```

権限設定（Linux/macOS）：

```bash
chmod 600 ~/.netrc
```

### 対応サイト

ユーザー名・パスワード認証をサポートするサイト：

- Vimeo
- ニコニコ動画
- Dailymotion
- その他（サイトにより異なる）

**注意**: YouTube/Googleはこの方法では認証できません。Cookieを使用してください。

## 年齢制限コンテンツ

### YouTube年齢制限

```bash
# Cookie認証で年齢制限を回避
yt-dlp --cookies-from-browser chrome "URL"

# または
yt-dlp --cookies cookies.txt "URL"
```

### 年齢確認なしで試行（非推奨）

```bash
# 年齢ゲートをスキップ（成功しないことが多い）
yt-dlp --no-check-certificate "URL"
```

## サイト別設定

### YouTube

```bash
# メンバーシップ動画
yt-dlp --cookies-from-browser chrome "https://www.youtube.com/watch?v=MEMBER_VIDEO"

# プレミアム限定高画質
yt-dlp --cookies-from-browser chrome -f "bestvideo+bestaudio" "URL"

# 非公開プレイリスト
yt-dlp --cookies-from-browser chrome "https://www.youtube.com/playlist?list=PRIVATE_LIST"
```

### ニコニコ動画

```bash
# Cookie認証（高画質ダウンロード）
yt-dlp --cookies-from-browser chrome "https://www.nicovideo.jp/watch/sm..."

# ユーザー名・パスワード
yt-dlp -u YOUR_EMAIL -p YOUR_PASSWORD "https://www.nicovideo.jp/watch/sm..."
```

### Twitter/X

```bash
# ログインが必要なコンテンツ
yt-dlp --cookies-from-browser chrome "TWITTER_URL"
```

### Instagram

```bash
# 非公開アカウントのコンテンツ
yt-dlp --cookies-from-browser chrome "INSTAGRAM_URL"
```

### Twitch

```bash
# サブスクライバー限定VOD
yt-dlp --cookies-from-browser chrome "TWITCH_VOD_URL"
```

## プロキシとVPN

地域制限のあるコンテンツにアクセス：

```bash
# HTTPプロキシ
yt-dlp --proxy "http://proxy.example.com:8080" "URL"

# SOCKS5プロキシ
yt-dlp --proxy "socks5://127.0.0.1:1080" "URL"

# プロキシ認証
yt-dlp --proxy "http://user:pass@proxy.example.com:8080" "URL"
```

## 二段階認証（2FA）

二段階認証を有効にしている場合：

1. **ブラウザでログイン**して2FAを完了
2. `--cookies-from-browser`でそのセッションを使用

```bash
# 2FA完了済みのブラウザからCookieを使用
yt-dlp --cookies-from-browser chrome "URL"
```

または、アプリパスワードを生成（サービスが対応している場合）。

## トラブルシューティング

### Cookieが読み取れない

```bash
# ブラウザを完全に終了してから再試行
# （ブラウザがCookieデータベースをロックしている可能性）

# 別のブラウザを試す
yt-dlp --cookies-from-browser firefox "URL"

# デバッグ出力
yt-dlp -v --cookies-from-browser chrome "URL"
```

### 「Sign in to confirm your age」エラー

```bash
# Cookie認証が必要
yt-dlp --cookies-from-browser chrome "URL"
```

### 「This video is private」エラー

```bash
# プレイリスト所有者のアカウントでログイン済みのブラウザを使用
yt-dlp --cookies-from-browser chrome "URL"
```

### 「Members-only content」エラー

```bash
# メンバーシップに加入しているアカウントのCookieを使用
yt-dlp --cookies-from-browser chrome "URL"
```

### Cookieの有効期限切れ

```bash
# ブラウザで再ログイン後、再試行
yt-dlp --cookies-from-browser chrome "URL"

# Cookieファイルを再エクスポート
```

### macOSキーチェーンアクセス

```bash
# キーチェーンアクセスを許可
# → セキュリティ設定でyt-dlpのアクセスを許可

# または、Cookieファイルを使用
yt-dlp --cookies cookies.txt "URL"
```

## セキュリティに関する注意

1. **Cookieファイルの保護**
   - 認証情報を含むため、安全な場所に保存
   - 適切な権限設定（600）
   - 共有しない

2. **パスワードの取り扱い**
   - コマンド履歴に残る可能性
   - `.netrc`ファイルを使用するか、対話的に入力

3. **公共のPCでの使用**
   - Cookie認証は避ける
   - 使用後はCookieファイルを削除

## 設定ファイルでの認証

`~/.config/yt-dlp/config`に保存：

```
# デフォルトでChromeのCookieを使用
--cookies-from-browser chrome

# または、Cookieファイルを使用
# --cookies ~/secure/cookies.txt
```

## 関連オプション一覧

| オプション | 説明 |
|-----------|------|
| `--cookies-from-browser BROWSER[:PROFILE][:CONTAINER]` | ブラウザからCookieを読み込む |
| `--cookies FILE` | Cookieファイルを使用 |
| `-u, --username USERNAME` | ユーザー名 |
| `-p, --password PASSWORD` | パスワード |
| `--netrc` | .netrcファイルを使用 |
| `--netrc-location PATH` | .netrcファイルのパス |
| `--proxy URL` | プロキシを使用 |
| `--no-check-certificate` | SSL証明書を検証しない |
