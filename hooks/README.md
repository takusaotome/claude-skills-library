# Claude Code Hooks Collection

Claude Codeの便利なhook設定集です。

## 使い方

1. 使いたいhook設定をコピー
2. `~/.claude/settings.json` の `hooks` セクションに追加
3. Claude Codeを再起動または新しいセッションを開始

## 利用可能なHooks

### 1. 現在日時をコンテキストに追加 (`current-datetime.json`)

**問題:** Claudeが日付を勘違いすることがある

**解決策:** 毎回のプロンプト送信時に現在日時をClaudeのコンテキストに自動追加

```json
{
  "UserPromptSubmit": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "echo \"[現在: $(date '+%Y年%m月%d日 (%a) %H:%M')]\""
        }
      ]
    }
  ]
}
```

**効果:** Claudeに `[現在: 2025年12月26日 (木) 08:45]` のような情報が毎回渡される

### 2. 通知音 (`notification-sound.json`)

**問題:** 長時間タスクの完了に気づかない

**解決策:** 通知時にシステム音を再生

```json
{
  "Notification": [
    {
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": "afplay /System/Library/Sounds/Glass.aiff"
        }
      ]
    }
  ]
}
```

**注:** macOS用。Linux/Windowsでは別のコマンドに変更が必要

---

## Hook設定の基本

### 利用可能なイベント

| イベント | タイミング | 用途 |
|---------|-----------|------|
| `SessionStart` | セッション開始時 | 環境設定、初期化 |
| `UserPromptSubmit` | プロンプト送信時 | コンテキスト追加 |
| `PreToolUse` | ツール実行前 | 検証、ブロック |
| `PostToolUse` | ツール実行後 | ログ、通知 |
| `Notification` | 通知時 | アラート音 |
| `Stop` | 応答完了時 | 完了通知 |

### 設定場所

- **ユーザー設定:** `~/.claude/settings.json`
- **プロジェクト設定:** `.claude/settings.json`

### 基本構文

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",  // PreToolUse等で必要
        "hooks": [
          {
            "type": "command",
            "command": "実行するコマンド"
          }
        ]
      }
    ]
  }
}
```

## 参考リンク

- [Claude Code Hooks公式ドキュメント](https://docs.anthropic.com/en/docs/claude-code/hooks)
