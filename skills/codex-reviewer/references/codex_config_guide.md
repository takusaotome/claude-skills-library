# Codex CLI 設定ガイド

このドキュメントでは、OpenAI Codex CLIの設定方法について説明します。

## インストール

### npm経由（推奨）

```bash
npm install -g @openai/codex
```

### Homebrew経由（macOS）

```bash
brew install --cask codex
```

### アップグレード

```bash
codex --upgrade
```

## 認証

### OAuth認証（推奨）

```bash
codex login
```

ChatGPT Plus、Pro、Business、Edu、Enterpriseアカウントでサインインできます。

### APIキー認証

```bash
codex login --with-api-key
# プロンプトでAPIキーを入力
```

### ログアウト

```bash
codex logout
```

## 設定ファイル

設定ファイルは `~/.codex/config.toml` に配置します。

### 基本設定

```toml
# デフォルトモデル（レビュー用に最高性能モデルを推奨）
model = "gpt-5.3-codex-max"

# デフォルト推論レベル
model_reasoning_effort = "high"

# 承認ポリシー
# - "untrusted": すべての操作で承認を求める
# - "on-failure": 失敗時のみ承認を求める
# - "on-request": リクエスト時のみ承認を求める
# - "never": 承認を求めない
approval_policy = "on-request"

# デフォルトプロファイル
profile = "deep-review"
```

### プロファイル設定

プロファイルを使用すると、用途別の設定セットを簡単に切り替えられます。

```toml
# ルートレベル設定（デフォルト）
model = "gpt-5.3-codex-max"
model_reasoning_effort = "high"
approval_policy = "on-request"

# 標準レビュー用プロファイル（推奨）
[profiles.deep-review]
model = "gpt-5.3-codex-max"
model_reasoning_effort = "high"
approval_policy = "never"

# 超詳細分析用プロファイル
[profiles.xhigh-review]
model = "gpt-5.3-codex-max"
model_reasoning_effort = "xhigh"
approval_policy = "never"

# 軽量レビュー用プロファイル（高速）
[profiles.quick-review]
model = "gpt-5-codex"
model_reasoning_effort = "medium"
approval_policy = "never"
```

## モデルオプション

### 利用可能なモデル

| モデル | 特徴 | 用途 |
|--------|------|------|
| `gpt-5.3-codex-max` | **最高性能モデル（推奨）** | 詳細レビュー、複雑な分析 |
| `gpt-5-codex` | デフォルトモデル、バランス重視 | 日常的なコーディング支援 |
| `gpt-5` | 汎用モデル | 一般的なタスク |
| `gpt-4.1` | 軽量モデル | 単純なタスク、高速応答 |

### 推論レベル（Reasoning Effort）

| レベル | 説明 | 用途 |
|--------|------|------|
| `minimal` | 最小限の思考 | 非常に単純なタスク |
| `low` | 軽い思考 | 単純なコード修正 |
| `medium` | 標準的な思考 | 日常的なタスク |
| `high` | **深い思考（推奨）** | 複雑な問題、詳細レビュー |
| `xhigh` | 最大限の思考 | 最も複雑な分析（遅い） |

## CLI オプション

### 基本的なフラグ

```bash
# モデル指定
codex --model gpt-5.3-codex-max "プロンプト"

# プロファイル指定
codex --profile deep-review "プロンプト"

# 作業ディレクトリ指定
codex -C /path/to/project "プロンプト"

# 設定オーバーライド
codex --config model_reasoning_effort="high" "プロンプト"
```

### 非対話モード（exec）

```bash
# 基本的な実行
codex exec "プロンプト"

# 出力をファイルに保存
codex exec -o output.md "プロンプト"

# JSON出力
codex exec --json "プロンプト"

# 標準入力からプロンプト
echo "プロンプト" | codex exec -
```

### サンドボックスモード

```bash
# 読み取り専用
codex --sandbox read-only "プロンプト"

# ワークスペース書き込み許可
codex --sandbox workspace-write "プロンプト"

# フルアクセス（危険）
codex --sandbox danger-full-access "プロンプト"
```

### 承認モード

```bash
# 常に承認を求める
codex --ask-for-approval untrusted "プロンプト"

# 失敗時のみ承認
codex --ask-for-approval on-failure "プロンプト"

# 承認なし
codex --ask-for-approval never "プロンプト"

# フルオート（ワークスペース書き込み + 失敗時承認）
codex --full-auto "プロンプト"
```

## レビュー用の推奨設定

### config.toml の推奨設定

```toml
# ~/.codex/config.toml

# デフォルトは最高性能モデル
model = "gpt-5.3-codex-max"
model_reasoning_effort = "high"
approval_policy = "on-request"

# 標準レビュー用（推奨）
[profiles.deep-review]
model = "gpt-5.3-codex-max"
model_reasoning_effort = "high"
approval_policy = "never"

# 超詳細分析用（非常に遅いが最も深い分析）
[profiles.xhigh-review]
model = "gpt-5.3-codex-max"
model_reasoning_effort = "xhigh"
approval_policy = "never"

# 軽量レビュー用（高速）
[profiles.quick-review]
model = "gpt-5-codex"
model_reasoning_effort = "medium"
approval_policy = "never"
```

### レビュー実行コマンド例

```bash
# コードレビュー（標準: gpt-5.3-codex-max + high）
codex exec --profile deep-review \
  -C /path/to/project \
  -o ./reviews/review_$(date +%Y%m%d).md \
  "src/main.pyのセキュリティとパフォーマンスをレビューしてください"

# ドキュメントレビュー
codex exec --profile deep-review \
  -o ./reviews/doc_review.md \
  "docs/api_spec.mdの完全性と正確性をレビューしてください"

# 超詳細分析（xhigh推論）
codex exec --profile xhigh-review \
  -o ./reviews/deep_analysis.md \
  "システムアーキテクチャの全体的なレビューを行ってください"
```

## MCP（Model Context Protocol）統合

### MCP サーバーの追加

```toml
# config.toml
[[mcp.servers]]
name = "custom-tool"
command = ["node", "/path/to/mcp-server.js"]
```

### MCP コマンド

```bash
# MCPサーバー一覧
codex mcp list

# MCPサーバー追加
codex mcp add <name> <command>

# MCPサーバー削除
codex mcp remove <name>
```

## トラブルシューティング

### よくある問題

1. **認証エラー**
   ```bash
   codex logout
   codex login
   ```

2. **タイムアウト**
   - 推論レベルを下げる（xhigh → high → medium）
   - プロンプトを簡潔にする
   - `quick-review`プロファイルを使用

3. **モデルが見つからない**
   - 最新バージョンにアップグレード
   - 利用可能なモデルを確認

### ログの確認

```bash
# デバッグモード
CODEX_DEBUG=1 codex "プロンプト"
```

## 参考リンク

- [Codex CLI 公式ドキュメント](https://developers.openai.com/codex/cli/)
- [CLI リファレンス](https://developers.openai.com/codex/cli/reference/)
- [GitHub リポジトリ](https://github.com/openai/codex)
- [設定ドキュメント](https://developers.openai.com/codex/local-config/)
