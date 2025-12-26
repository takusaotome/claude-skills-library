# Claude Code Hooks Collection

A collection of useful hook configurations for Claude Code.

## Usage

1. Copy the desired hook configuration
2. Add it to the `hooks` section in `~/.claude/settings.json`
3. Restart Claude Code or start a new session

## Available Hooks

### 1. Current DateTime Context (`current-datetime.json`)

**Problem:** Claude sometimes confuses today's date

**Solution:** Automatically add current datetime to Claude's context on every prompt submission

```json
{
  "UserPromptSubmit": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "echo \"[Current: $(date '+%Y-%m-%d (%a) %H:%M')]\""
        }
      ]
    }
  ]
}
```

**Effect:** Claude receives `[Current: 2025-12-26 (Thu) 08:45]` with every prompt

### 2. Notification Sound (`notification-sound-macos.json`)

**Problem:** Missing completion of long-running tasks

**Solution:** Play system sound on notifications

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

**Note:** macOS only. Modify command for Linux/Windows.

---

## Hook Basics

### Available Events

| Event | Timing | Use Case |
|-------|--------|----------|
| `SessionStart` | Session start | Environment setup |
| `UserPromptSubmit` | Prompt submission | Context injection |
| `PreToolUse` | Before tool execution | Validation, blocking |
| `PostToolUse` | After tool execution | Logging, notifications |
| `Notification` | On notification | Alert sounds |
| `Stop` | Response complete | Completion notification |

### Configuration Locations

- **User settings:** `~/.claude/settings.json`
- **Project settings:** `.claude/settings.json`

### Basic Syntax

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "shell command to execute"
          }
        ]
      }
    ]
  }
}
```

## References

- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)
