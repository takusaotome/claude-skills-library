"""
Tests for ffprobe_analyzer.py

Unit tests for MediaAnalyzer, CompatibilityChecker, and EncodingRecommender classes.
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ffprobe_analyzer import CompatibilityChecker, EncodingRecommender, MediaAnalyzer, generate_report


class TestMediaAnalyzerFormatHelpers:
    """Test helper methods in MediaAnalyzer"""

    def test_format_duration_zero(self):
        result = MediaAnalyzer._format_duration(0)
        assert result == "00:00:00.00"

    def test_format_duration_seconds(self):
        result = MediaAnalyzer._format_duration(65.5)
        assert result == "00:01:05.50"

    def test_format_duration_hours(self):
        result = MediaAnalyzer._format_duration(3723.75)
        assert result == "01:02:03.75"

    def test_format_size_zero(self):
        result = MediaAnalyzer._format_size(0)
        assert result == "0 B"

    def test_format_size_bytes(self):
        result = MediaAnalyzer._format_size(500)
        assert result == "500.00 B"

    def test_format_size_kb(self):
        result = MediaAnalyzer._format_size(2048)
        assert result == "2.00 KB"

    def test_format_size_mb(self):
        result = MediaAnalyzer._format_size(5 * 1024 * 1024)
        assert result == "5.00 MB"

    def test_format_size_gb(self):
        result = MediaAnalyzer._format_size(2 * 1024 * 1024 * 1024)
        assert result == "2.00 GB"

    def test_format_bitrate_zero(self):
        result = MediaAnalyzer._format_bitrate(0)
        assert result == "N/A"

    def test_format_bitrate_bps(self):
        result = MediaAnalyzer._format_bitrate(500)
        assert result == "500 bps"

    def test_format_bitrate_kbps(self):
        result = MediaAnalyzer._format_bitrate(128000)
        assert result == "128 kbps"

    def test_format_bitrate_mbps(self):
        result = MediaAnalyzer._format_bitrate(5000000)
        assert result == "5.00 Mbps"


class TestMediaAnalyzerWithMock:
    """Test MediaAnalyzer with mocked ffprobe output"""

    @pytest.fixture
    def sample_ffprobe_output(self):
        return {
            "format": {
                "filename": "test.mp4",
                "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
                "format_long_name": "QuickTime / MOV",
                "duration": "120.5",
                "size": "10485760",
                "bit_rate": "696320",
                "nb_streams": "2",
            },
            "streams": [
                {
                    "index": 0,
                    "codec_type": "video",
                    "codec_name": "h264",
                    "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
                    "profile": "High",
                    "width": 1920,
                    "height": 1080,
                    "pix_fmt": "yuv420p",
                    "r_frame_rate": "30/1",
                    "bit_rate": "500000",
                    "color_space": "bt709",
                },
                {
                    "index": 1,
                    "codec_type": "audio",
                    "codec_name": "aac",
                    "codec_long_name": "AAC (Advanced Audio Coding)",
                    "sample_rate": "48000",
                    "channels": 2,
                    "channel_layout": "stereo",
                    "bit_rate": "192000",
                },
            ],
        }

    def test_get_format_info(self, sample_ffprobe_output):
        analyzer = MediaAnalyzer("test.mp4")
        analyzer._probe_data = sample_ffprobe_output

        fmt = analyzer.get_format_info()

        assert fmt["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
        assert fmt["duration"] == 120.5
        assert fmt["size"] == 10485760
        assert fmt["nb_streams"] == 2

    def test_get_video_streams(self, sample_ffprobe_output):
        analyzer = MediaAnalyzer("test.mp4")
        analyzer._probe_data = sample_ffprobe_output

        streams = analyzer.get_video_streams()

        assert len(streams) == 1
        assert streams[0]["codec_name"] == "h264"
        assert streams[0]["width"] == 1920
        assert streams[0]["height"] == 1080
        assert streams[0]["frame_rate"] == 30.0

    def test_get_audio_streams(self, sample_ffprobe_output):
        analyzer = MediaAnalyzer("test.mp4")
        analyzer._probe_data = sample_ffprobe_output

        streams = analyzer.get_audio_streams()

        assert len(streams) == 1
        assert streams[0]["codec_name"] == "aac"
        assert streams[0]["sample_rate"] == 48000
        assert streams[0]["channels"] == 2


class TestCompatibilityChecker:
    """Test CompatibilityChecker class"""

    @pytest.fixture
    def compatible_analyzer(self):
        analyzer = MediaAnalyzer("test.mp4")
        analyzer._probe_data = {
            "format": {"format_name": "mp4"},
            "streams": [
                {
                    "index": 0,
                    "codec_type": "video",
                    "codec_name": "h264",
                    "profile": "High",
                    "width": 1920,
                    "height": 1080,
                },
                {"index": 1, "codec_type": "audio", "codec_name": "aac"},
            ],
        }
        return analyzer

    @pytest.fixture
    def incompatible_analyzer(self):
        analyzer = MediaAnalyzer("test.avi")
        analyzer._probe_data = {
            "format": {"format_name": "avi"},
            "streams": [
                {"index": 0, "codec_type": "video", "codec_name": "mpeg4", "width": 1920, "height": 1080},
                {"index": 1, "codec_type": "audio", "codec_name": "pcm_s16le"},
            ],
        }
        return analyzer

    def test_browser_compatible_file(self, compatible_analyzer):
        checker = CompatibilityChecker(compatible_analyzer)
        issues = checker.check_browser_compatibility()

        # Should have info about faststart, but no errors
        errors = [i for i in issues if i["severity"] == "error"]
        assert len(errors) == 0

    def test_browser_incompatible_video_codec(self, incompatible_analyzer):
        checker = CompatibilityChecker(incompatible_analyzer)
        issues = checker.check_browser_compatibility()

        video_errors = [i for i in issues if "video" in i["message"].lower() and i["severity"] == "error"]
        assert len(video_errors) > 0

    def test_mobile_compatible_file(self, compatible_analyzer):
        checker = CompatibilityChecker(compatible_analyzer)
        issues = checker.check_mobile_compatibility()

        # Should be ok
        ok_messages = [i for i in issues if i["severity"] == "ok"]
        assert len(ok_messages) > 0


class TestEncodingRecommender:
    """Test EncodingRecommender class"""

    @pytest.fixture
    def analyzer(self):
        analyzer = MediaAnalyzer("input.mp4")
        analyzer._probe_data = {
            "format": {
                "duration": "120.0",
                "size": "104857600",
                "bit_rate": "6990507",
            },
            "streams": [
                {
                    "index": 0,
                    "codec_type": "video",
                    "codec_name": "h264",
                    "width": 1920,
                    "height": 1080,
                    "r_frame_rate": "30/1",
                },
                {
                    "index": 1,
                    "codec_type": "audio",
                    "codec_name": "aac",
                    "sample_rate": "48000",
                    "channels": 2,
                },
            ],
        }
        return analyzer

    def test_recommend_for_web(self, analyzer):
        recommender = EncodingRecommender(analyzer)
        rec = recommender.recommend_for_web()

        assert rec["use_case"] == "web"
        assert "libx264" in rec["command"]
        assert "faststart" in rec["command"]
        assert "yuv420p" in rec["command"]

    def test_recommend_for_mobile(self, analyzer):
        recommender = EncodingRecommender(analyzer)
        rec = recommender.recommend_for_mobile()

        assert rec["use_case"] == "mobile"
        assert "720" in rec["command"]
        assert "96k" in rec["command"]

    def test_recommend_for_archive(self, analyzer):
        recommender = EncodingRecommender(analyzer)
        rec = recommender.recommend_for_archive()

        assert rec["use_case"] == "archive"
        assert "libx265" in rec["command"]
        assert "flac" in rec["command"]

    def test_recommend_for_streaming(self, analyzer):
        recommender = EncodingRecommender(analyzer)
        rec = recommender.recommend_for_streaming()

        assert rec["use_case"] == "streaming"
        assert "hls_time" in rec["command"]
        assert "m3u8" in rec["command"]


class TestGenerateReport:
    """Test report generation"""

    @pytest.fixture
    def analyzer(self):
        analyzer = MediaAnalyzer("test.mp4")
        analyzer._probe_data = {
            "format": {
                "filename": "test.mp4",
                "format_name": "mp4",
                "format_long_name": "MPEG-4 Part 14",
                "duration": "60.0",
                "size": "5242880",
                "bit_rate": "699050",
                "nb_streams": "2",
            },
            "streams": [
                {
                    "index": 0,
                    "codec_type": "video",
                    "codec_name": "h264",
                    "codec_long_name": "H.264",
                    "profile": "High",
                    "width": 1280,
                    "height": 720,
                    "pix_fmt": "yuv420p",
                    "r_frame_rate": "30/1",
                    "bit_rate": "500000",
                    "color_space": "",
                },
                {
                    "index": 1,
                    "codec_type": "audio",
                    "codec_name": "aac",
                    "codec_long_name": "AAC",
                    "sample_rate": "44100",
                    "channels": 2,
                    "channel_layout": "stereo",
                    "bit_rate": "128000",
                },
            ],
        }
        return analyzer

    def test_report_contains_sections(self, analyzer):
        report = generate_report(analyzer)

        assert "# Media Analysis Report" in report
        assert "## Container Information" in report
        assert "## Video Streams" in report
        assert "## Audio Streams" in report
        assert "## Compatibility Check" in report

    def test_report_with_suggestions(self, analyzer):
        report = generate_report(analyzer, suggest_commands=True)

        assert "## Encoding Recommendations" in report
        assert "ffmpeg" in report

    def test_report_with_use_case(self, analyzer):
        report = generate_report(analyzer, use_case="web", suggest_commands=True)

        assert "Web配信用" in report
