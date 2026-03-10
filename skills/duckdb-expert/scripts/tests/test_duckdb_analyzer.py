"""Tests for DuckDB Analyzer."""

import json
import tempfile
from pathlib import Path

import pytest

# Skip all tests if duckdb is not installed
duckdb = pytest.importorskip("duckdb")

import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from duckdb_analyzer import DuckDBAnalyzer


@pytest.fixture
def analyzer():
    """Create a DuckDBAnalyzer instance."""
    return DuckDBAnalyzer(memory_limit="1GB")


@pytest.fixture
def sample_csv(tmp_path):
    """Create a sample CSV file for testing."""
    csv_content = """id,name,value,category
1,Alice,100.5,A
2,Bob,200.0,B
3,Charlie,150.75,A
4,Diana,300.25,C
5,Eve,,A
"""
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)


@pytest.fixture
def sample_json(tmp_path):
    """Create a sample JSON file for testing."""
    data = [
        {"id": 1, "name": "Alice", "score": 85},
        {"id": 2, "name": "Bob", "score": 92},
        {"id": 3, "name": "Charlie", "score": 78},
    ]
    json_file = tmp_path / "sample.json"
    json_file.write_text(json.dumps(data))
    return str(json_file)


class TestDuckDBAnalyzerInit:
    """Tests for DuckDBAnalyzer initialization."""

    def test_init_default(self):
        """Test default initialization."""
        analyzer = DuckDBAnalyzer()
        assert analyzer.con is not None
        analyzer.close()

    def test_init_with_memory_limit(self):
        """Test initialization with custom memory limit."""
        analyzer = DuckDBAnalyzer(memory_limit="2GB")
        assert analyzer.con is not None
        analyzer.close()

    def test_init_with_threads(self):
        """Test initialization with custom thread count."""
        analyzer = DuckDBAnalyzer(threads=2)
        assert analyzer.con is not None
        analyzer.close()


class TestAnalyzeFile:
    """Tests for analyze_file method."""

    def test_analyze_csv_dict_format(self, analyzer, sample_csv):
        """Test analyzing CSV with dict output format."""
        result = analyzer.analyze_file(sample_csv, output_format="dict")

        assert isinstance(result, dict)
        assert result["file_format"] == "csv"
        assert "basic_info" in result
        assert "schema" in result
        assert "statistics" in result
        assert "quality" in result
        assert "sample_data" in result

    def test_analyze_csv_basic_info(self, analyzer, sample_csv):
        """Test that basic info contains correct row/column counts."""
        result = analyzer.analyze_file(sample_csv, output_format="dict")

        assert result["basic_info"]["total_row_count"] == 5
        assert result["basic_info"]["column_count"] == 4

    def test_analyze_csv_schema(self, analyzer, sample_csv):
        """Test that schema detection works correctly."""
        result = analyzer.analyze_file(sample_csv, output_format="dict")

        schema = result["schema"]
        column_names = [col["column_name"] for col in schema]
        assert "id" in column_names
        assert "name" in column_names
        assert "value" in column_names
        assert "category" in column_names

    def test_analyze_csv_quality_metrics(self, analyzer, sample_csv):
        """Test quality metrics calculation."""
        result = analyzer.analyze_file(sample_csv, output_format="dict")

        quality = result["quality"]
        assert quality["total_rows"] == 5
        assert "null_counts" in quality
        assert "null_percentages" in quality
        assert "completeness" in quality
        # value column has 1 NULL (Eve's value)
        assert quality["null_counts"]["value"] == 1
        assert quality["null_percentages"]["value"] == 20.0

    def test_analyze_csv_markdown_format(self, analyzer, sample_csv):
        """Test analyzing CSV with markdown output format."""
        result = analyzer.analyze_file(sample_csv, output_format="markdown")

        assert isinstance(result, str)
        assert "# Data Profile Report" in result
        assert "## Basic Information" in result
        assert "## Schema" in result
        assert "## Data Quality" in result

    def test_analyze_csv_json_format(self, analyzer, sample_csv):
        """Test analyzing CSV with JSON output format."""
        result = analyzer.analyze_file(sample_csv, output_format="json")

        assert isinstance(result, str)
        parsed = json.loads(result)
        assert "file_format" in parsed
        assert parsed["file_format"] == "csv"

    def test_analyze_json_file(self, analyzer, sample_json):
        """Test analyzing JSON file."""
        result = analyzer.analyze_file(sample_json, output_format="dict")

        assert result["file_format"] == "json"
        assert result["basic_info"]["total_row_count"] == 3
        assert result["basic_info"]["column_count"] == 3

    def test_analyze_with_sample_size(self, analyzer, sample_csv):
        """Test analyzing with sample size specified."""
        result = analyzer.analyze_file(sample_csv, sample_size=3, output_format="dict")

        # Quality metrics should still be on full data
        assert result["quality"]["total_rows"] == 5
        # Statistics may be sampled
        assert result["analysis_config"]["sample_size_for_statistics"] == 3


class TestRunQuery:
    """Tests for run_query method."""

    def test_run_query_with_file(self, analyzer, sample_csv):
        """Test running custom query with file reference."""
        result = analyzer.run_query("SELECT COUNT(*) as cnt FROM data", file_path=sample_csv)
        row = result.fetchone()
        assert row[0] == 5

    def test_run_query_aggregation(self, analyzer, sample_csv):
        """Test running aggregation query."""
        result = analyzer.run_query(
            "SELECT category, COUNT(*) as cnt FROM data GROUP BY category ORDER BY category",
            file_path=sample_csv,
        )
        rows = result.fetchall()
        # A: 3, B: 1, C: 1
        assert len(rows) == 3
        assert rows[0] == ("A", 3)


class TestBuildReadFunction:
    """Tests for _build_read_function method."""

    def test_parquet_read_function(self, analyzer):
        """Test Parquet read function generation."""
        result = analyzer._build_read_function("data.parquet", ".parquet")
        assert "read_parquet" in result
        assert "union_by_name=true" in result

    def test_csv_read_function(self, analyzer):
        """Test CSV read function generation."""
        result = analyzer._build_read_function("data.csv", ".csv")
        assert "read_csv" in result
        assert "auto_detect=true" in result

    def test_json_read_function(self, analyzer):
        """Test JSON read function generation."""
        result = analyzer._build_read_function("data.json", ".json")
        assert "read_json" in result
        assert "auto_detect=true" in result

    def test_ndjson_read_function(self, analyzer):
        """Test newline-delimited JSON read function generation."""
        result = analyzer._build_read_function("data.ndjson", ".ndjson")
        assert "read_json" in result
        assert "newline_delimited" in result

    def test_tsv_read_function(self, analyzer):
        """Test TSV read function generation."""
        result = analyzer._build_read_function("data.tsv", ".tsv")
        assert "read_csv" in result
        assert "delim='\\t'" in result


class TestCleanup:
    """Tests for resource cleanup."""

    def test_close_connection(self):
        """Test that close properly cleans up resources."""
        analyzer = DuckDBAnalyzer()
        analyzer.close()
        # Connection should be closed
        with pytest.raises(Exception):
            analyzer.con.execute("SELECT 1")
