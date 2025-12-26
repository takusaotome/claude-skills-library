---
name: video2minutes
description: 動画ファイルから文字起こしと議事録を自動生成
allowed-tools: Bash(python3:*), Bash(source:*), Bash(cat:*), Bash(ls:*), Bash(pip3:*)
argument-hint: <動画パス> --date <YYYY-MM-DD> --attendees <参加者>
---

# Video2Minutes - 動画から議事録生成

動画ファイルから文字起こしと議事録を自動生成するスキルです。

## 前提条件

- **OPENAI_API_KEY** 環境変数が設定されていること
- Python 3.10以上
- FFmpeg がインストールされていること

## 処理フロー

1. 音声抽出（FFmpeg）→ 文字起こし（Whisper API）→ 議事録生成（GPT-4.1）

## 実行手順

### 1. 依存関係のインストール（初回のみ）

```bash
pip3 install openai python-dotenv
```

### 2. 議事録生成の実行

```bash
python3 ~/.claude/skills/video2minutes/scripts/video2minutes.py -i $ARGUMENTS
```

## 処理完了後

生成されたファイルを読み取って、ユーザーに以下を報告してください：

### 1. 文字起こし全文

```bash
ls -t ./transcript/*.txt 2>/dev/null | head -1 | xargs cat
```

### 2. 議事録

```bash
ls -t ./minutes/*.md 2>/dev/null | head -1 | xargs cat
```

## 使用例

```
/video2minutes ~/Downloads/meeting.mp4 --date 2025-12-25 --attendees "田中, 佐藤"
/video2minutes meeting.mp4 --date 2025-12-25 --attendees "A様, B様" --meeting-name "キックオフ"
/video2minutes meeting.mp4 --date 2025-12-25 --attendees "A様, B様" --context "本会議はXYZプロジェクトのフェーズ2開始に向けたキックオフ。クライアントはABC社。主な議題は要件確認とスケジュール調整。"
```

## オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `--date` | 会議日（YYYY-MM-DD）**必須** | - |
| `--attendees` | 参加者リスト **必須** | - |
| `--meeting-name` | 会議名 | ファイル名 |
| `--context` | 会議の背景・コンテキスト（プロジェクト情報、目的、特別な指示など） | - |
| `--model` | GPTモデル | gpt-4.1 |
| `--language` | 言語コード | ja |
| `--transcript-dir` | 文字起こし出力先 | ./transcript |
| `--minutes-dir` | 議事録出力先 | ./minutes |
| `--keep-audio` | 中間音声ファイルを保持 | false |

## 環境変数

| 変数名 | 説明 |
|--------|------|
| `OPENAI_API_KEY` | OpenAI APIキー（必須） |

## 出力ファイル

- `./transcript/<会議名>_transcript.txt` - 文字起こし全文
- `./minutes/<会議名>.md` - 議事録（Markdown形式）
