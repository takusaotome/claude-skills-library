#!/usr/bin/env python3
"""
FFprobe Media Analyzer

メディアファイルを分析し、詳細情報と最適なエンコード設定を提案するスクリプト。

Usage:
    python ffprobe_analyzer.py <input_file> [options]

Examples:
    python ffprobe_analyzer.py video.mp4
    python ffprobe_analyzer.py video.mp4 --use-case web
    python ffprobe_analyzer.py video.mp4 --output report.md
    python ffprobe_analyzer.py video.mp4 --suggest-commands
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class MediaAnalyzer:
    """ffprobeを使用したメディアファイル分析クラス"""

    def __init__(self, file_path: str):
        """
        初期化

        Args:
            file_path: 分析対象ファイルパス
        """
        self.file_path = file_path
        self._probe_data: Optional[Dict] = None

    def _run_ffprobe(self) -> Dict:
        """ffprobeを実行して結果を取得"""
        if self._probe_data is not None:
            return self._probe_data

        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", self.file_path]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self._probe_data = json.loads(result.stdout)
            return self._probe_data
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"ffprobe failed: {e.stderr}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse ffprobe output: {e}")

    def get_format_info(self) -> Dict[str, Any]:
        """コンテナフォーマット情報を取得"""
        data = self._run_ffprobe()
        fmt = data.get("format", {})

        duration = float(fmt.get("duration", 0))
        size = int(fmt.get("size", 0))
        bit_rate = int(fmt.get("bit_rate", 0))

        return {
            "filename": fmt.get("filename", ""),
            "format_name": fmt.get("format_name", ""),
            "format_long_name": fmt.get("format_long_name", ""),
            "duration": duration,
            "duration_formatted": self._format_duration(duration),
            "size": size,
            "size_formatted": self._format_size(size),
            "bit_rate": bit_rate,
            "bit_rate_formatted": self._format_bitrate(bit_rate),
            "nb_streams": int(fmt.get("nb_streams", 0)),
        }

    def get_video_streams(self) -> List[Dict[str, Any]]:
        """ビデオストリーム情報を取得"""
        data = self._run_ffprobe()
        streams = []

        for stream in data.get("streams", []):
            if stream.get("codec_type") != "video":
                continue

            # フレームレート計算
            frame_rate_str = stream.get("r_frame_rate", "0/1")
            try:
                num, den = map(int, frame_rate_str.split("/"))
                frame_rate = round(num / den, 2) if den > 0 else 0
            except (ValueError, ZeroDivisionError):
                frame_rate = 0

            streams.append(
                {
                    "index": stream.get("index"),
                    "codec_name": stream.get("codec_name", ""),
                    "codec_long_name": stream.get("codec_long_name", ""),
                    "profile": stream.get("profile", ""),
                    "width": stream.get("width", 0),
                    "height": stream.get("height", 0),
                    "resolution": f"{stream.get('width', 0)}x{stream.get('height', 0)}",
                    "pix_fmt": stream.get("pix_fmt", ""),
                    "frame_rate": frame_rate,
                    "frame_rate_str": frame_rate_str,
                    "bit_rate": int(stream.get("bit_rate", 0)),
                    "bit_rate_formatted": self._format_bitrate(int(stream.get("bit_rate", 0))),
                    "color_space": stream.get("color_space", ""),
                    "color_transfer": stream.get("color_transfer", ""),
                    "color_primaries": stream.get("color_primaries", ""),
                    "nb_frames": stream.get("nb_frames", "N/A"),
                }
            )

        return streams

    def get_audio_streams(self) -> List[Dict[str, Any]]:
        """オーディオストリーム情報を取得"""
        data = self._run_ffprobe()
        streams = []

        for stream in data.get("streams", []):
            if stream.get("codec_type") != "audio":
                continue

            streams.append(
                {
                    "index": stream.get("index"),
                    "codec_name": stream.get("codec_name", ""),
                    "codec_long_name": stream.get("codec_long_name", ""),
                    "profile": stream.get("profile", ""),
                    "sample_rate": int(stream.get("sample_rate", 0)),
                    "channels": stream.get("channels", 0),
                    "channel_layout": stream.get("channel_layout", ""),
                    "bit_rate": int(stream.get("bit_rate", 0)),
                    "bit_rate_formatted": self._format_bitrate(int(stream.get("bit_rate", 0))),
                    "bits_per_sample": stream.get("bits_per_sample", 0),
                }
            )

        return streams

    def get_subtitle_streams(self) -> List[Dict[str, Any]]:
        """字幕ストリーム情報を取得"""
        data = self._run_ffprobe()
        streams = []

        for stream in data.get("streams", []):
            if stream.get("codec_type") != "subtitle":
                continue

            streams.append(
                {
                    "index": stream.get("index"),
                    "codec_name": stream.get("codec_name", ""),
                    "codec_long_name": stream.get("codec_long_name", ""),
                    "language": stream.get("tags", {}).get("language", ""),
                }
            )

        return streams

    @staticmethod
    def _format_duration(seconds: float) -> str:
        """秒数を HH:MM:SS.ms 形式に変換"""
        if seconds <= 0:
            return "00:00:00.00"
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:05.2f}"

    @staticmethod
    def _format_size(bytes_size: int) -> str:
        """バイト数を人間が読みやすい形式に変換"""
        if bytes_size <= 0:
            return "0 B"
        units = ["B", "KB", "MB", "GB", "TB"]
        unit_index = 0
        size = float(bytes_size)
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        return f"{size:.2f} {units[unit_index]}"

    @staticmethod
    def _format_bitrate(bps: int) -> str:
        """ビットレートを人間が読みやすい形式に変換"""
        if bps <= 0:
            return "N/A"
        if bps >= 1_000_000:
            return f"{bps / 1_000_000:.2f} Mbps"
        elif bps >= 1_000:
            return f"{bps / 1_000:.0f} kbps"
        else:
            return f"{bps} bps"


class CompatibilityChecker:
    """互換性チェッククラス"""

    # ブラウザ互換コーデック
    BROWSER_COMPATIBLE_VIDEO = ["h264", "vp8", "vp9", "av1"]
    BROWSER_COMPATIBLE_AUDIO = ["aac", "mp3", "opus", "vorbis"]

    # モバイル互換コーデック
    MOBILE_COMPATIBLE_VIDEO = ["h264", "hevc", "h265"]
    MOBILE_COMPATIBLE_AUDIO = ["aac", "mp3"]

    def __init__(self, analyzer: MediaAnalyzer):
        self.analyzer = analyzer

    def check_browser_compatibility(self) -> List[Dict[str, Any]]:
        """ブラウザ互換性チェック"""
        issues = []
        video_streams = self.analyzer.get_video_streams()
        audio_streams = self.analyzer.get_audio_streams()

        for vs in video_streams:
            codec = vs["codec_name"].lower()
            if codec not in self.BROWSER_COMPATIBLE_VIDEO:
                issues.append(
                    {
                        "severity": "error",
                        "message": f"Video codec '{codec}' is not browser compatible",
                        "recommendation": "Re-encode to H.264 or VP9 for browser playback",
                    }
                )
            elif codec == "h264":
                profile = vs.get("profile", "").lower()
                if "high 4:4:4" in profile or "high 10" in profile:
                    issues.append(
                        {
                            "severity": "warning",
                            "message": f"H.264 profile '{profile}' may not be supported in all browsers",
                            "recommendation": "Use High, Main, or Baseline profile",
                        }
                    )

        for aus in audio_streams:
            codec = aus["codec_name"].lower()
            if codec not in self.BROWSER_COMPATIBLE_AUDIO:
                issues.append(
                    {
                        "severity": "error",
                        "message": f"Audio codec '{codec}' is not browser compatible",
                        "recommendation": "Re-encode to AAC or MP3",
                    }
                )

        # faststart チェック
        fmt = self.analyzer.get_format_info()
        if "mp4" in fmt["format_name"].lower() or "mov" in fmt["format_name"].lower():
            # Note: ffprobe doesn't directly report moov position
            issues.append(
                {
                    "severity": "info",
                    "message": "Ensure -movflags +faststart is used for streaming optimization",
                    "recommendation": "Add -movflags +faststart when encoding",
                }
            )

        if not issues:
            issues.append(
                {"severity": "ok", "message": "File appears to be browser compatible", "recommendation": None}
            )

        return issues

    def check_mobile_compatibility(self) -> List[Dict[str, Any]]:
        """モバイル互換性チェック"""
        issues = []
        video_streams = self.analyzer.get_video_streams()
        audio_streams = self.analyzer.get_audio_streams()

        for vs in video_streams:
            codec = vs["codec_name"].lower()
            if codec not in self.MOBILE_COMPATIBLE_VIDEO:
                issues.append(
                    {
                        "severity": "error",
                        "message": f"Video codec '{codec}' may not play on mobile devices",
                        "recommendation": "Re-encode to H.264 for maximum compatibility",
                    }
                )

            # 解像度チェック
            width = vs.get("width", 0)
            height = vs.get("height", 0)
            if width > 3840 or height > 2160:
                issues.append(
                    {
                        "severity": "warning",
                        "message": f"Resolution {width}x{height} may be too high for some devices",
                        "recommendation": "Consider providing lower resolution versions",
                    }
                )

        for aus in audio_streams:
            codec = aus["codec_name"].lower()
            if codec not in self.MOBILE_COMPATIBLE_AUDIO:
                issues.append(
                    {
                        "severity": "warning",
                        "message": f"Audio codec '{codec}' may not play on some mobile devices",
                        "recommendation": "Re-encode to AAC for maximum compatibility",
                    }
                )

        if not issues:
            issues.append({"severity": "ok", "message": "File appears to be mobile compatible", "recommendation": None})

        return issues


class EncodingRecommender:
    """エンコード推奨設定生成クラス"""

    def __init__(self, analyzer: MediaAnalyzer):
        self.analyzer = analyzer

    def recommend_for_web(self) -> Dict[str, Any]:
        """Web配信用の推奨設定"""
        video_streams = self.analyzer.get_video_streams()
        fmt = self.analyzer.get_format_info()

        vs = video_streams[0] if video_streams else {}
        width = vs.get("width", 1920)
        height = vs.get("height", 1080)

        # 解像度調整
        target_width = min(width, 1920)
        target_height = -2  # アスペクト比維持

        command = f"""ffmpeg -i "{self.analyzer.file_path}" \\
  -c:v libx264 -crf 23 -preset medium \\
  -vf "scale={target_width}:{target_height}" \\
  -c:a aac -b:a 128k \\
  -movflags +faststart \\
  -pix_fmt yuv420p \\
  output_web.mp4"""

        # サイズ推定（CRF 23で約50-70%圧縮と仮定）
        original_size = fmt.get("size", 0)
        estimated_size = int(original_size * 0.6)

        return {
            "use_case": "web",
            "description": "Web配信用最適化（H.264 + AAC）",
            "command": command,
            "estimated_size": MediaAnalyzer._format_size(estimated_size),
            "notes": [
                "faststart有効でストリーミング開始が高速",
                "yuv420pで最大互換性",
                "CRF 23は品質とサイズのバランス",
            ],
        }

    def recommend_for_mobile(self) -> Dict[str, Any]:
        """モバイル用の推奨設定"""
        video_streams = self.analyzer.get_video_streams()
        fmt = self.analyzer.get_format_info()

        command = f"""ffmpeg -i "{self.analyzer.file_path}" \\
  -c:v libx264 -crf 26 -preset fast \\
  -vf "scale=-2:720" \\
  -c:a aac -b:a 96k \\
  -movflags +faststart \\
  output_mobile.mp4"""

        original_size = fmt.get("size", 0)
        estimated_size = int(original_size * 0.3)

        return {
            "use_case": "mobile",
            "description": "モバイル用最適化（720p + 低ビットレート）",
            "command": command,
            "estimated_size": MediaAnalyzer._format_size(estimated_size),
            "notes": ["720p解像度でデータ通信量削減", "CRF 26で高圧縮", "音声96kbpsでモバイル品質十分"],
        }

    def recommend_for_archive(self) -> Dict[str, Any]:
        """アーカイブ用の推奨設定"""
        video_streams = self.analyzer.get_video_streams()
        fmt = self.analyzer.get_format_info()

        command = f"""ffmpeg -i "{self.analyzer.file_path}" \\
  -c:v libx265 -crf 22 -preset slow \\
  -c:a flac \\
  output_archive.mkv"""

        original_size = fmt.get("size", 0)
        estimated_size = int(original_size * 0.5)

        return {
            "use_case": "archive",
            "description": "アーカイブ用高品質（H.265 + FLAC）",
            "command": command,
            "estimated_size": MediaAnalyzer._format_size(estimated_size),
            "notes": ["H.265で高圧縮・高品質", "FLACでロスレス音声", "slowプリセットで最高圧縮効率"],
        }

    def recommend_for_streaming(self) -> Dict[str, Any]:
        """ストリーミング用の推奨設定（HLS）"""
        command = f"""ffmpeg -i "{self.analyzer.file_path}" \\
  -c:v libx264 -crf 23 -preset medium \\
  -c:a aac -b:a 128k \\
  -hls_time 10 \\
  -hls_list_size 0 \\
  -hls_segment_filename 'segment_%03d.ts' \\
  output.m3u8"""

        return {
            "use_case": "streaming",
            "description": "HLSストリーミング用",
            "command": command,
            "estimated_size": "Original + overhead",
            "notes": [
                "10秒セグメント",
                "全セグメントをプレイリストに含む",
                "アダプティブビットレートには別途設定が必要",
            ],
        }


def generate_report(analyzer: MediaAnalyzer, use_case: Optional[str] = None, suggest_commands: bool = False) -> str:
    """Markdownレポートを生成"""
    md = []

    # ヘッダー
    md.append("# Media Analysis Report")
    md.append("")
    md.append(f"**File:** `{analyzer.file_path}`")
    md.append(f"**Generated:** {datetime.now().isoformat()}")
    md.append("")

    # フォーマット情報
    fmt = analyzer.get_format_info()
    md.append("## Container Information")
    md.append("")
    md.append("| Property | Value |")
    md.append("|----------|-------|")
    md.append(f"| Format | {fmt['format_long_name']} ({fmt['format_name']}) |")
    md.append(f"| Duration | {fmt['duration_formatted']} |")
    md.append(f"| Size | {fmt['size_formatted']} |")
    md.append(f"| Bitrate | {fmt['bit_rate_formatted']} |")
    md.append(f"| Streams | {fmt['nb_streams']} |")
    md.append("")

    # ビデオストリーム
    video_streams = analyzer.get_video_streams()
    if video_streams:
        md.append("## Video Streams")
        md.append("")
        for i, vs in enumerate(video_streams):
            md.append(f"### Video Stream #{i}")
            md.append("")
            md.append("| Property | Value |")
            md.append("|----------|-------|")
            md.append(f"| Codec | {vs['codec_name']} ({vs['codec_long_name']}) |")
            if vs["profile"]:
                md.append(f"| Profile | {vs['profile']} |")
            md.append(f"| Resolution | {vs['resolution']} |")
            md.append(f"| Frame Rate | {vs['frame_rate']} fps |")
            md.append(f"| Bitrate | {vs['bit_rate_formatted']} |")
            md.append(f"| Pixel Format | {vs['pix_fmt']} |")
            if vs["color_space"]:
                md.append(f"| Color Space | {vs['color_space']} |")
            md.append("")

    # オーディオストリーム
    audio_streams = analyzer.get_audio_streams()
    if audio_streams:
        md.append("## Audio Streams")
        md.append("")
        for i, aus in enumerate(audio_streams):
            md.append(f"### Audio Stream #{i}")
            md.append("")
            md.append("| Property | Value |")
            md.append("|----------|-------|")
            md.append(f"| Codec | {aus['codec_name']} ({aus['codec_long_name']}) |")
            md.append(f"| Sample Rate | {aus['sample_rate']} Hz |")
            md.append(f"| Channels | {aus['channels']} ({aus['channel_layout']}) |")
            md.append(f"| Bitrate | {aus['bit_rate_formatted']} |")
            md.append("")

    # 字幕ストリーム
    subtitle_streams = analyzer.get_subtitle_streams()
    if subtitle_streams:
        md.append("## Subtitle Streams")
        md.append("")
        for i, ss in enumerate(subtitle_streams):
            md.append(f"- Stream #{i}: {ss['codec_name']} ({ss.get('language', 'unknown')})")
        md.append("")

    # 互換性チェック
    checker = CompatibilityChecker(analyzer)

    md.append("## Compatibility Check")
    md.append("")

    md.append("### Browser Compatibility")
    md.append("")
    for issue in checker.check_browser_compatibility():
        icon = {"ok": "[OK]", "info": "[INFO]", "warning": "[WARN]", "error": "[ERR]"}.get(issue["severity"], "[?]")
        md.append(f"- {icon} {issue['message']}")
        if issue["recommendation"]:
            md.append(f"  - Recommendation: {issue['recommendation']}")
    md.append("")

    md.append("### Mobile Compatibility")
    md.append("")
    for issue in checker.check_mobile_compatibility():
        icon = {"ok": "[OK]", "info": "[INFO]", "warning": "[WARN]", "error": "[ERR]"}.get(issue["severity"], "[?]")
        md.append(f"- {icon} {issue['message']}")
        if issue["recommendation"]:
            md.append(f"  - Recommendation: {issue['recommendation']}")
    md.append("")

    # エンコード推奨
    if suggest_commands:
        recommender = EncodingRecommender(analyzer)

        md.append("## Encoding Recommendations")
        md.append("")

        recommendations = []
        if use_case:
            if use_case == "web":
                recommendations.append(recommender.recommend_for_web())
            elif use_case == "mobile":
                recommendations.append(recommender.recommend_for_mobile())
            elif use_case == "archive":
                recommendations.append(recommender.recommend_for_archive())
            elif use_case == "streaming":
                recommendations.append(recommender.recommend_for_streaming())
        else:
            recommendations = [
                recommender.recommend_for_web(),
                recommender.recommend_for_mobile(),
                recommender.recommend_for_archive(),
            ]

        for rec in recommendations:
            md.append(f"### {rec['description']}")
            md.append("")
            md.append("```bash")
            md.append(rec["command"])
            md.append("```")
            md.append("")
            md.append(f"**Estimated Size:** {rec['estimated_size']}")
            md.append("")
            if rec["notes"]:
                md.append("**Notes:**")
                for note in rec["notes"]:
                    md.append(f"- {note}")
                md.append("")

    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(
        description="FFprobe Media Analyzer - Comprehensive media file analysis tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python ffprobe_analyzer.py video.mp4
    python ffprobe_analyzer.py video.mp4 --use-case web --suggest-commands
    python ffprobe_analyzer.py video.mp4 --output report.md
    python ffprobe_analyzer.py video.mp4 --format json
        """,
    )

    parser.add_argument("input_file", help="Input media file path")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument(
        "--format", "-f", choices=["markdown", "json"], default="markdown", help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--use-case",
        "-u",
        choices=["web", "mobile", "archive", "streaming"],
        help="Specific use case for recommendations",
    )
    parser.add_argument("--suggest-commands", "-s", action="store_true", help="Include encoding command suggestions")

    args = parser.parse_args()

    # ファイル存在確認
    if not Path(args.input_file).exists():
        print(f"Error: File not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)

    try:
        analyzer = MediaAnalyzer(args.input_file)

        if args.format == "json":
            result = {
                "file_path": args.input_file,
                "analysis_timestamp": datetime.now().isoformat(),
                "format": analyzer.get_format_info(),
                "video_streams": analyzer.get_video_streams(),
                "audio_streams": analyzer.get_audio_streams(),
                "subtitle_streams": analyzer.get_subtitle_streams(),
            }
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = generate_report(analyzer, use_case=args.use_case, suggest_commands=args.suggest_commands)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Report saved to: {args.output}")
        else:
            print(output)

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
