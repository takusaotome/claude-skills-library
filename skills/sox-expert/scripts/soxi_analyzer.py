#!/usr/bin/env python3
"""
SoX Audio File Analyzer

Analyzes audio files using soxi and sox commands, generates quality reports,
and provides processing recommendations.

Usage:
    python soxi_analyzer.py input.wav
    python soxi_analyzer.py input.wav -o report.md
    python soxi_analyzer.py input.wav -o report.md -s  # include statistics
    python soxi_analyzer.py *.wav -o batch_report.md   # batch analysis

Requirements:
    - sox installed (brew install sox / apt install sox)
    - Python 3.7+
"""

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class AudioInfo:
    """Container for audio file information."""
    file_path: str
    file_type: str = ""
    sample_rate: int = 0
    channels: int = 0
    bit_depth: int = 0
    encoding: str = ""
    duration_seconds: float = 0.0
    duration_formatted: str = ""
    num_samples: int = 0
    file_size_bytes: int = 0
    bitrate: Optional[int] = None
    compression: Optional[str] = None


@dataclass
class AudioStatistics:
    """Container for audio statistics from sox stat/stats."""
    dc_offset: float = 0.0
    min_amplitude: float = 0.0
    max_amplitude: float = 0.0
    midline_amplitude: float = 0.0
    mean_norm: float = 0.0
    mean_amplitude: float = 0.0
    rms_amplitude: float = 0.0
    max_delta: float = 0.0
    min_delta: float = 0.0
    mean_delta: float = 0.0
    rms_delta: float = 0.0
    rough_frequency: float = 0.0
    volume_adjustment: float = 0.0
    peak_level_db: float = 0.0
    rms_level_db: float = 0.0
    crest_factor: float = 0.0
    flat_factor: float = 0.0
    pk_count: int = 0


@dataclass
class QualityIssue:
    """Container for quality issues."""
    severity: str  # "high", "medium", "low"
    category: str  # "clipping", "dc_offset", "noise", "level", "format"
    message: str
    recommendation: str


@dataclass
class ProcessingRecommendation:
    """Container for processing recommendations."""
    category: str
    description: str
    command: str
    priority: int  # 1=high, 2=medium, 3=low


class AudioAnalyzer:
    """Analyzes audio files using SoX tools."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        self._info: Optional[AudioInfo] = None
        self._stats: Optional[AudioStatistics] = None

    def _run_command(self, cmd: List[str]) -> str:
        """Run a command and return output."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Command timed out: {' '.join(cmd)}")
        except FileNotFoundError:
            raise RuntimeError("sox/soxi not found. Please install SoX.")

    def get_file_info(self) -> AudioInfo:
        """Get basic file information using soxi."""
        if self._info is not None:
            return self._info

        info = AudioInfo(file_path=str(self.file_path))

        # Get individual properties
        soxi_flags = {
            '-t': 'file_type',
            '-r': 'sample_rate',
            '-c': 'channels',
            '-b': 'bit_depth',
            '-e': 'encoding',
            '-D': 'duration_seconds',
            '-d': 'duration_formatted',
            '-s': 'num_samples',
        }

        for flag, attr in soxi_flags.items():
            try:
                output = self._run_command(['soxi', flag, str(self.file_path)])
                value = output.strip()
                if value:
                    if attr in ('sample_rate', 'channels', 'bit_depth', 'num_samples'):
                        setattr(info, attr, int(value))
                    elif attr == 'duration_seconds':
                        setattr(info, attr, float(value))
                    else:
                        setattr(info, attr, value)
            except (ValueError, RuntimeError):
                pass

        # Get file size
        info.file_size_bytes = self.file_path.stat().st_size

        # Calculate bitrate for compressed formats
        if info.duration_seconds > 0:
            info.bitrate = int((info.file_size_bytes * 8) / info.duration_seconds / 1000)

        self._info = info
        return info

    def get_statistics(self) -> AudioStatistics:
        """Get audio statistics using sox stat."""
        if self._stats is not None:
            return self._stats

        stats = AudioStatistics()

        # Run sox stat
        try:
            output = self._run_command([
                'sox', str(self.file_path), '-n', 'stat'
            ])

            # Parse stat output
            for line in output.split('\n'):
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()

                    try:
                        if 'dc offset' in key:
                            stats.dc_offset = float(value)
                        elif 'min level' in key or 'minimum amplitude' in key:
                            stats.min_amplitude = float(value)
                        elif 'max level' in key or 'maximum amplitude' in key:
                            stats.max_amplitude = float(value)
                        elif 'midline amplitude' in key:
                            stats.midline_amplitude = float(value)
                        elif 'mean norm' in key:
                            stats.mean_norm = float(value)
                        elif 'mean amplitude' in key:
                            stats.mean_amplitude = float(value)
                        elif 'rms amplitude' in key:
                            stats.rms_amplitude = float(value)
                        elif 'maximum delta' in key:
                            stats.max_delta = float(value)
                        elif 'minimum delta' in key:
                            stats.min_delta = float(value)
                        elif 'mean delta' in key:
                            stats.mean_delta = float(value)
                        elif 'rms delta' in key:
                            stats.rms_delta = float(value)
                        elif 'rough frequency' in key:
                            stats.rough_frequency = float(value)
                        elif 'volume adjustment' in key:
                            stats.volume_adjustment = float(value)
                    except ValueError:
                        pass
        except RuntimeError:
            pass

        # Run sox stats for additional metrics
        try:
            output = self._run_command([
                'sox', str(self.file_path), '-n', 'stats'
            ])

            for line in output.split('\n'):
                line = line.strip()
                if 'Pk lev dB' in line:
                    try:
                        stats.peak_level_db = float(line.split()[-1])
                    except (ValueError, IndexError):
                        pass
                elif 'RMS lev dB' in line:
                    try:
                        stats.rms_level_db = float(line.split()[-1])
                    except (ValueError, IndexError):
                        pass
                elif 'Crest factor' in line:
                    try:
                        stats.crest_factor = float(line.split()[-1])
                    except (ValueError, IndexError):
                        pass
                elif 'Flat factor' in line:
                    try:
                        stats.flat_factor = float(line.split()[-1])
                    except (ValueError, IndexError):
                        pass
                elif 'Pk count' in line:
                    try:
                        stats.pk_count = int(line.split()[-1])
                    except (ValueError, IndexError):
                        pass
        except RuntimeError:
            pass

        self._stats = stats
        return stats

    def analyze_quality(self) -> List[QualityIssue]:
        """Analyze audio quality and identify issues."""
        issues = []
        info = self.get_file_info()
        stats = self.get_statistics()

        # Check for clipping
        if abs(stats.max_amplitude) >= 1.0 or abs(stats.min_amplitude) >= 1.0:
            issues.append(QualityIssue(
                severity="high",
                category="clipping",
                message=f"Audio is clipping (max: {stats.max_amplitude:.4f}, min: {stats.min_amplitude:.4f})",
                recommendation="Apply gain reduction before processing: sox input.wav output.wav gain -3"
            ))
        elif abs(stats.max_amplitude) >= 0.95 or abs(stats.min_amplitude) >= 0.95:
            issues.append(QualityIssue(
                severity="medium",
                category="clipping",
                message=f"Audio is near clipping (max: {stats.max_amplitude:.4f})",
                recommendation="Consider normalizing with headroom: sox input.wav output.wav norm -3"
            ))

        # Check for DC offset
        if abs(stats.dc_offset) > 0.01:
            issues.append(QualityIssue(
                severity="medium",
                category="dc_offset",
                message=f"Significant DC offset detected: {stats.dc_offset:.6f}",
                recommendation="Remove DC offset: sox input.wav output.wav highpass 20"
            ))

        # Check for low volume
        if stats.rms_amplitude > 0 and stats.rms_amplitude < 0.05:
            issues.append(QualityIssue(
                severity="medium",
                category="level",
                message=f"Audio level is very low (RMS: {stats.rms_amplitude:.4f})",
                recommendation="Normalize audio: sox input.wav output.wav norm -3"
            ))

        # Check sample rate
        if info.sample_rate < 44100:
            issues.append(QualityIssue(
                severity="low",
                category="format",
                message=f"Sample rate is below CD quality ({info.sample_rate} Hz)",
                recommendation=f"Consider upsampling if source quality allows: sox input.wav -r 44100 output.wav rate -v"
            ))

        # Check bit depth
        if info.bit_depth < 16:
            issues.append(QualityIssue(
                severity="medium",
                category="format",
                message=f"Bit depth is low ({info.bit_depth}-bit)",
                recommendation="Consider converting to higher bit depth for processing: sox input.wav -b 24 output.wav"
            ))

        # Check for potential noise (high crest factor may indicate noise)
        if stats.crest_factor > 0 and stats.crest_factor < 3:
            issues.append(QualityIssue(
                severity="low",
                category="noise",
                message=f"Low crest factor ({stats.crest_factor:.2f}) may indicate noise or compression",
                recommendation="Consider noise reduction if applicable"
            ))

        return issues


class ProcessingRecommender:
    """Provides processing recommendations based on audio analysis."""

    def __init__(self, analyzer: AudioAnalyzer):
        self.analyzer = analyzer
        self.info = analyzer.get_file_info()
        self.stats = analyzer.get_statistics()

    def recommend_normalization(self) -> ProcessingRecommendation:
        """Recommend normalization settings."""
        if abs(self.stats.max_amplitude) >= 0.95:
            return ProcessingRecommendation(
                category="normalization",
                description="Audio is at or near peak level. Normalize with headroom.",
                command=f"sox \"{self.info.file_path}\" output.wav norm -3",
                priority=2
            )
        elif self.stats.rms_amplitude < 0.1:
            return ProcessingRecommendation(
                category="normalization",
                description="Audio level is low. Normalize to increase volume.",
                command=f"sox \"{self.info.file_path}\" output.wav norm -1",
                priority=1
            )
        else:
            return ProcessingRecommendation(
                category="normalization",
                description="Audio levels are acceptable. Optional normalization.",
                command=f"sox \"{self.info.file_path}\" output.wav norm -3",
                priority=3
            )

    def recommend_noise_reduction(self) -> ProcessingRecommendation:
        """Recommend noise reduction settings."""
        # Estimate noise based on statistics
        if self.stats.mean_amplitude > 0.01 and self.stats.crest_factor < 6:
            return ProcessingRecommendation(
                category="noise_reduction",
                description="Possible noise detected. Create noise profile from silent section.",
                command=f"# Step 1: Extract noise profile from first 0.5s\n"
                        f"sox \"{self.info.file_path}\" -n trim 0 0.5 noiseprof noise.prof\n"
                        f"# Step 2: Apply noise reduction\n"
                        f"sox \"{self.info.file_path}\" output.wav noisered noise.prof 0.21",
                priority=2
            )
        else:
            return ProcessingRecommendation(
                category="noise_reduction",
                description="Noise levels appear acceptable. Optional noise reduction.",
                command=f"# Create noise profile from quiet section first\n"
                        f"sox \"{self.info.file_path}\" -n trim START DURATION noiseprof noise.prof\n"
                        f"sox \"{self.info.file_path}\" output.wav noisered noise.prof 0.15",
                priority=3
            )

    def recommend_format_conversion(self, target_use: str = "general") -> ProcessingRecommendation:
        """Recommend format conversion based on intended use."""
        use_cases = {
            "cd": ("CD distribution", f"sox \"{self.info.file_path}\" -r 44100 -b 16 -c 2 output.wav dither -s", 2),
            "podcast": ("Podcast distribution", f"sox \"{self.info.file_path}\" -C 192 -r 44100 output.mp3", 2),
            "web": ("Web streaming", f"sox \"{self.info.file_path}\" -C 128 -r 44100 output.mp3", 2),
            "archive": ("Archive/lossless", f"sox \"{self.info.file_path}\" -C 8 output.flac", 2),
            "voip": ("VoIP/telephony", f"sox \"{self.info.file_path}\" -r 8000 -c 1 -b 16 output.wav", 2),
            "hires": ("High-resolution audio", f"sox \"{self.info.file_path}\" -r 96000 -b 24 output.wav rate -v", 3),
            "video": ("Video editing", f"sox \"{self.info.file_path}\" -r 48000 -b 16 -c 2 output.wav", 2),
        }

        if target_use in use_cases:
            desc, cmd, priority = use_cases[target_use]
            return ProcessingRecommendation(
                category="format_conversion",
                description=f"Convert for {desc}",
                command=cmd,
                priority=priority
            )
        else:
            return ProcessingRecommendation(
                category="format_conversion",
                description="General format conversion",
                command=f"sox \"{self.info.file_path}\" output.wav",
                priority=3
            )

    def get_all_recommendations(self) -> List[ProcessingRecommendation]:
        """Get all applicable recommendations."""
        recommendations = [
            self.recommend_normalization(),
            self.recommend_noise_reduction(),
        ]

        # Add format-specific recommendations based on current format
        if self.info.sample_rate != 44100 or self.info.bit_depth != 16:
            recommendations.append(ProcessingRecommendation(
                category="format_standardization",
                description="Convert to CD-quality standard format",
                command=f"sox \"{self.info.file_path}\" -r 44100 -b 16 output.wav rate -v dither -s",
                priority=2
            ))

        # DC offset removal
        if abs(self.stats.dc_offset) > 0.001:
            recommendations.append(ProcessingRecommendation(
                category="dc_offset_removal",
                description="Remove DC offset",
                command=f"sox \"{self.info.file_path}\" output.wav highpass 20",
                priority=2
            ))

        # Sort by priority
        recommendations.sort(key=lambda x: x.priority)
        return recommendations


def generate_report(
    analyzers: List[AudioAnalyzer],
    include_stats: bool = True
) -> str:
    """Generate markdown report for analyzed files."""
    lines = [
        "# Audio Analysis Report",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"Files analyzed: {len(analyzers)}",
        "",
    ]

    for analyzer in analyzers:
        info = analyzer.get_file_info()
        issues = analyzer.analyze_quality()
        recommender = ProcessingRecommender(analyzer)

        lines.extend([
            f"## {Path(info.file_path).name}",
            "",
            "### File Information",
            "",
            "| Property | Value |",
            "|----------|-------|",
            f"| File Path | `{info.file_path}` |",
            f"| Format | {info.file_type} |",
            f"| Sample Rate | {info.sample_rate:,} Hz |",
            f"| Channels | {info.channels} |",
            f"| Bit Depth | {info.bit_depth}-bit |",
            f"| Encoding | {info.encoding} |",
            f"| Duration | {info.duration_formatted} ({info.duration_seconds:.2f}s) |",
            f"| Samples | {info.num_samples:,} |",
            f"| File Size | {info.file_size_bytes:,} bytes ({info.file_size_bytes/1024/1024:.2f} MB) |",
        ])

        if info.bitrate:
            lines.append(f"| Bitrate | ~{info.bitrate} kbps |")

        lines.append("")

        if include_stats:
            stats = analyzer.get_statistics()
            lines.extend([
                "### Audio Statistics",
                "",
                "| Metric | Value |",
                "|--------|-------|",
                f"| DC Offset | {stats.dc_offset:.6f} |",
                f"| Min Amplitude | {stats.min_amplitude:.6f} |",
                f"| Max Amplitude | {stats.max_amplitude:.6f} |",
                f"| RMS Amplitude | {stats.rms_amplitude:.6f} |",
                f"| Mean Amplitude | {stats.mean_amplitude:.6f} |",
                f"| Peak Level | {stats.peak_level_db:.2f} dB |",
                f"| RMS Level | {stats.rms_level_db:.2f} dB |",
                f"| Crest Factor | {stats.crest_factor:.2f} |",
                f"| Volume Adjustment | {stats.volume_adjustment:.4f} |",
                "",
            ])

        if issues:
            lines.extend([
                "### Quality Issues",
                "",
            ])
            for issue in issues:
                icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(issue.severity, "⚪")
                lines.extend([
                    f"#### {icon} {issue.category.replace('_', ' ').title()} ({issue.severity})",
                    "",
                    f"**Issue:** {issue.message}",
                    "",
                    f"**Recommendation:** `{issue.recommendation}`",
                    "",
                ])
        else:
            lines.extend([
                "### Quality Issues",
                "",
                "✅ No significant quality issues detected.",
                "",
            ])

        recommendations = recommender.get_all_recommendations()
        lines.extend([
            "### Processing Recommendations",
            "",
        ])
        for i, rec in enumerate(recommendations, 1):
            priority_label = {1: "High", 2: "Medium", 3: "Low"}.get(rec.priority, "Unknown")
            lines.extend([
                f"#### {i}. {rec.category.replace('_', ' ').title()} (Priority: {priority_label})",
                "",
                f"{rec.description}",
                "",
                "```bash",
                rec.command,
                "```",
                "",
            ])

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze audio files using SoX tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.wav                    # Basic analysis
  %(prog)s input.wav -o report.md       # Save report to file
  %(prog)s input.wav -s                 # Include detailed statistics
  %(prog)s *.wav -o batch_report.md     # Analyze multiple files
  %(prog)s input.wav --json             # Output as JSON
"""
    )

    parser.add_argument(
        "input_files",
        nargs="+",
        help="Audio file(s) to analyze"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: stdout)"
    )
    parser.add_argument(
        "-s", "--stats",
        action="store_true",
        help="Include detailed audio statistics"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of Markdown"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress messages"
    )

    args = parser.parse_args()

    # Analyze files
    analyzers = []
    for file_path in args.input_files:
        path = Path(file_path)
        if not path.exists():
            if not args.quiet:
                print(f"Warning: File not found: {file_path}", file=sys.stderr)
            continue

        try:
            if not args.quiet:
                print(f"Analyzing: {file_path}", file=sys.stderr)
            analyzer = AudioAnalyzer(str(path))
            analyzers.append(analyzer)
        except Exception as e:
            if not args.quiet:
                print(f"Error analyzing {file_path}: {e}", file=sys.stderr)

    if not analyzers:
        print("No valid audio files to analyze.", file=sys.stderr)
        sys.exit(1)

    # Generate output
    if args.json:
        output_data = []
        for analyzer in analyzers:
            info = analyzer.get_file_info()
            stats = analyzer.get_statistics() if args.stats else None
            issues = analyzer.analyze_quality()
            recommender = ProcessingRecommender(analyzer)

            file_data = {
                "file_path": info.file_path,
                "info": {
                    "file_type": info.file_type,
                    "sample_rate": info.sample_rate,
                    "channels": info.channels,
                    "bit_depth": info.bit_depth,
                    "encoding": info.encoding,
                    "duration_seconds": info.duration_seconds,
                    "duration_formatted": info.duration_formatted,
                    "num_samples": info.num_samples,
                    "file_size_bytes": info.file_size_bytes,
                    "bitrate": info.bitrate,
                },
                "issues": [
                    {
                        "severity": issue.severity,
                        "category": issue.category,
                        "message": issue.message,
                        "recommendation": issue.recommendation,
                    }
                    for issue in issues
                ],
                "recommendations": [
                    {
                        "category": rec.category,
                        "description": rec.description,
                        "command": rec.command,
                        "priority": rec.priority,
                    }
                    for rec in recommender.get_all_recommendations()
                ],
            }

            if stats:
                file_data["statistics"] = {
                    "dc_offset": stats.dc_offset,
                    "min_amplitude": stats.min_amplitude,
                    "max_amplitude": stats.max_amplitude,
                    "rms_amplitude": stats.rms_amplitude,
                    "mean_amplitude": stats.mean_amplitude,
                    "peak_level_db": stats.peak_level_db,
                    "rms_level_db": stats.rms_level_db,
                    "crest_factor": stats.crest_factor,
                    "volume_adjustment": stats.volume_adjustment,
                }

            output_data.append(file_data)

        output = json.dumps(output_data, indent=2, ensure_ascii=False)
    else:
        output = generate_report(analyzers, include_stats=args.stats)

    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output, encoding="utf-8")
        if not args.quiet:
            print(f"Report saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
