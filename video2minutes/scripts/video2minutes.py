#!/usr/bin/env python3
"""
video2minutes.py - 議事録作成ツール

動画ファイルから自動的に文字起こしを行い、AI議事録を生成するスクリプト。

使用例:
    python video2minutes.py -i meeting.mp4 --date 2025-01-13 --attendees "A様, B様, C様"
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Third-party imports
try:
    import openai
except ImportError:
    openai = None

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = lambda: None

load_dotenv()

# ---------------------------------------------------------------------------
# 議事録生成用プロンプトテンプレート
# ---------------------------------------------------------------------------
PROMPT_TEMPLATE = """##### ① ロール定義（変更不要）
あなたは「戦略系コンサルの議事録ライター」です。
- 文字起こし全文から要点を抽出し、読み手が 3 分で全体像と次のアクションを把握できる議事録を作成してください。
- 未決事項や検討タスクがあれば「アクションアイテム」として必ず表にまとめ、担当者と期限を推論・記載します。
- 決定事項・議論の経緯・論点・参考情報は「議事内容の詳細」に整理します。
- 出力は **Markdown** 形式で。
{context_section}
##### ② 出力仕様（変更不要）
**出力フォーマット**
1. 会議情報
   - **会議名**: {meeting_name}
   - **開催日**: {date}
   - **出席者**: {attendees}

2. アクションアイテム
   | No. | アクションアイテム | 担当 | 重要度 | 期限 | 備考 |
   |-----|------------------|------|------|------|------|
   | {{自動生成}} |

   **重要度凡例**
   🔴: 高   🟡: 中   🟢: 低

3. 議事内容の詳細
   - ### 決定事項
     - {{箇条書き}}
   - ### 主要議題と論点
     1. **{{議題1}}**
        - 背景: …
        - 主な発言要旨: …
     2. **{{議題2}}**
        - …
   - ### 次回以降へのメモ / その他
     - …

##### ③ 入力欄（ここだけ毎回差し替え）
以下にミーティングの文字起こし全文を <<Transcript>> タグで囲んで貼り付けてください。

<<Transcript>>
{transcript}
<<Transcript>>
"""

# ---------------------------------------------------------------------------
# ユーティリティ関数
# ---------------------------------------------------------------------------
def run(cmd: list[str], *, check: bool = True) -> None:
    """Run a subprocess and stream output."""
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=check)


def ensure_dir(path: Path) -> None:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)


def derive_name(original: Path, suffix: str, new_ext: str) -> Path:
    """Create <stem>_<suffix><new_ext> in the same directory."""
    return original.with_stem(f"{original.stem}_{suffix}").with_suffix(new_ext)


def sanitize_filename(name: str) -> str:
    """Sanitize filename for safe file system use."""
    safe = "".join(c if c.isalnum() or c in ("-", "_", " ") else "_" for c in name).strip()
    return safe.replace(" ", "_") or "output"


# ---------------------------------------------------------------------------
# 音声抽出（FFmpeg）
# ---------------------------------------------------------------------------
def extract_audio(
    video_path: Path,
    audio_out: Path,
    *,
    bitrate_kbps: int,
    sample_rate: int = 16_000,
    channels: int = 1,
) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-ar",
        str(sample_rate),
        "-ac",
        str(channels),
        "-c:a",
        "libmp3lame",
        "-b:a",
        f"{bitrate_kbps}k",
        str(audio_out),
    ]
    run(cmd)


# ---------------------------------------------------------------------------
# 文字起こし（OpenAI Whisper API）
# ---------------------------------------------------------------------------
def transcribe_api(
    audio_path: Path,
    transcript_out: Path,
    *,
    language: str,
    response_format: str,
    api_key: Optional[str],
    temperature: float = 0.1,
    model: str = "whisper-1",
) -> None:
    if openai is None:
        raise RuntimeError("`openai` package not installed. Run: pip install openai")

    # API キーを優先順位で決定
    openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise RuntimeError("OpenAI API key not provided. Set it in .env, ENV, or --api-key")

    with audio_path.open("rb") as f:
        transcript = openai.audio.transcriptions.create(
            file=f,
            model=model,
            language=language,
            response_format=response_format,
            temperature=temperature,
        )

    transcript_out.write_text(transcript, encoding="utf-8")
    print(f"✓ Transcript saved → {transcript_out}")


# ---------------------------------------------------------------------------
# 議事録生成（OpenAI Chat API）
# ---------------------------------------------------------------------------
def strip_code_fence(md: str) -> str:
    """Remove markdown code fences from the response."""
    md = md.strip()
    if md.startswith("```"):
        md = re.sub(r"^```(?:[a-zA-Z0-9_+-]*)?\n", "", md)
        md = re.sub(r"\n```\s*$", "", md)
    return md.lstrip("\n")


def is_reasoning_model(model: str) -> bool:
    """Check if model is a reasoning model (o1/o3/o4 series)."""
    return model.startswith('o1') or model.startswith('o3') or model.startswith('o4')


def call_chat_completion(prompt: str, prefer_model: str) -> str:
    """Call OpenAI Chat API with fallback."""
    for mdl in (prefer_model, "gpt-4.1", "gpt-4.1-mini"):
        try:
            # Reasoning models don't support temperature parameter
            if is_reasoning_model(mdl):
                resp = openai.chat.completions.create(
                    model=mdl,
                    messages=[{"role": "user", "content": prompt}],
                )
            else:
                resp = openai.chat.completions.create(
                    model=mdl,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                )
            print(f"[info] Minutes generated with model: {mdl}")
            return resp.choices[0].message.content
        except openai.NotFoundError as exc:
            print(f"[warn] Model '{mdl}' not available – trying fallback…", file=sys.stderr)
            last_exc = exc
        except openai.OpenAIError:
            raise
    raise last_exc


def generate_minutes(
    transcript_text: str,
    minutes_out: Path,
    *,
    meeting_name: str,
    date: str,
    attendees: str,
    context: Optional[str] = None,
    model: str = "gpt-4.1",
) -> None:
    """Generate meeting minutes from transcript."""
    # Build context section if provided
    if context and context.strip():
        context_section = f"""
##### 会議の背景・コンテキスト
以下の背景情報を考慮して議事録を作成してください：
{context.strip()}

"""
    else:
        context_section = "\n"

    prompt = PROMPT_TEMPLATE.format(
        meeting_name=meeting_name.strip(),
        date=date.strip(),
        attendees=attendees.strip(),
        context_section=context_section,
        transcript=transcript_text.strip(),
    )
    
    minutes_md = strip_code_fence(call_chat_completion(prompt, model))
    minutes_out.write_text(minutes_md, encoding="utf-8")
    print(f"✓ Minutes saved → {minutes_out}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Extract audio, transcribe, and generate meeting minutes from video"
    )
    
    # 入力ファイル
    p.add_argument("-i", "--input", type=Path, required=True, help="Input video/audio file")
    
    # 会議情報
    p.add_argument("--meeting-name", help="Meeting title (default: input filename)")
    p.add_argument("--date", required=True, help="Meeting date (YYYY-MM-DD)")
    p.add_argument("--attendees", required=True, help="Comma/semicolon-separated attendee list")
    
    # 出力設定
    p.add_argument("--transcript-dir", type=Path, default=Path("transcript"),
                   help="Directory for transcript output (default: transcript)")
    p.add_argument("--minutes-dir", type=Path, default=Path("minutes"),
                   help="Directory for minutes output (default: minutes)")
    
    # オプション設定
    p.add_argument("--language", default="ja", help="ISO 639-1 language code (default: ja)")
    p.add_argument("--bitrate", type=int, default=30, help="MP3 bitrate kbps (default: 30)")
    p.add_argument("--model", default="gpt-4.1", help="Preferred OpenAI model for minutes (default: gpt-4.1)")
    p.add_argument("--api-key", help="OpenAI API key (overrides ENV/.env)")
    p.add_argument("--keep-audio", action="store_true", help="Keep intermediate audio file")
    p.add_argument("--context", help="Meeting background/context (e.g., project info, purpose, special instructions)")

    return p.parse_args()


# ---------------------------------------------------------------------------
# メイン処理
# ---------------------------------------------------------------------------
def main() -> None:
    args = parse_args()
    
    # 入力ファイルの確認
    video_path = args.input.expanduser().resolve()
    if not video_path.exists():
        sys.exit(f"Input not found: {video_path}")
    
    # 会議名の決定
    meeting_name = args.meeting_name or video_path.stem
    safe_name = sanitize_filename(meeting_name)
    
    # 出力ディレクトリの作成
    ensure_dir(args.transcript_dir)
    ensure_dir(args.minutes_dir)
    
    # 出力ファイルパスの決定
    audio_out = derive_name(video_path, f"{args.bitrate}k", ".mp3")
    transcript_out = args.transcript_dir / f"{safe_name}_transcript.txt"
    minutes_out = args.minutes_dir / f"{safe_name}.md"
    
    try:
        print("=== Step 1/3: 音声抽出 (FFmpeg) ===")
        extract_audio(video_path, audio_out, bitrate_kbps=args.bitrate)
        
        print("\n=== Step 2/3: 文字起こし (Whisper API) ===")
        transcribe_api(
            audio_out,
            transcript_out,
            language=args.language,
            response_format="text",
            api_key=args.api_key,
        )
        
        print("\n=== Step 3/3: 議事録生成 (Chat API) ===")
        transcript_text = transcript_out.read_text(encoding="utf-8")
        generate_minutes(
            transcript_text,
            minutes_out,
            meeting_name=meeting_name,
            date=args.date,
            attendees=args.attendees,
            context=args.context,
            model=args.model,
        )
        
        print("\n✓ 処理完了!")
        print(f"  - 文字起こし: {transcript_out}")
        print(f"  - 議事録: {minutes_out}")
        
    finally:
        # 中間ファイルの削除（オプション）
        if not args.keep_audio and audio_out.exists():
            audio_out.unlink()
            print(f"  - 音声ファイルを削除: {audio_out}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.exit(f"External command failed (exit {e.returncode})")
    except Exception as exc:
        sys.exit(str(exc))