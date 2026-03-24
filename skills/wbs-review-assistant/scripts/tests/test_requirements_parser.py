"""
Tests for requirements_parser.py
"""

from pathlib import Path

import pytest
from requirements_parser import RequirementsParser


@pytest.fixture
def sample_requirements_md(tmp_path):
    """Create a sample requirements markdown file"""
    content = """# Project Requirements

## Functional Requirements

- REQ-001: User authentication with email and password
- REQ-002: User profile management
- FR-003: Data export to CSV format

## Non-Functional Requirements

- NFR-001: System must support 1000 concurrent users
- NFR-002: Response time < 200ms

## Technology Stack

- Frontend: React
- Backend: Django
- Database: PostgreSQL

## Scope

### In-Scope
- User registration and login
- Profile editing
- Data export functionality

### Out-of-Scope
- Third-party OAuth integration
- Mobile app development
"""

    req_file = tmp_path / "requirements.md"
    req_file.write_text(content, encoding="utf-8")
    return req_file


@pytest.fixture
def japanese_requirements_md(tmp_path):
    """Create a Japanese requirements file"""
    content = """# プロジェクト要件

## 機能要件

- 要件-001: ユーザー認証機能
- 機能-002: データエクスポート機能

## スコープ

### 対象範囲
- ユーザー登録
- データ出力

### 対象外
- モバイルアプリ
"""

    req_file = tmp_path / "requirements_ja.md"
    req_file.write_text(content, encoding="utf-8")
    return req_file


class TestRequirementsParser:
    """Test cases for RequirementsParser"""

    def test_parse_english_requirements(self, sample_requirements_md):
        """Test parsing English requirements"""
        parser = RequirementsParser(str(sample_requirements_md))
        result = parser.parse()

        # Check requirements extracted
        assert len(result["requirements"]) >= 5
        req_ids = [req["req_id"] for req in result["requirements"]]
        assert "REQ-001" in req_ids
        assert "REQ-002" in req_ids
        assert "FR-003" in req_ids
        assert "NFR-001" in req_ids

    def test_parse_japanese_requirements(self, japanese_requirements_md):
        """Test parsing Japanese requirements"""
        parser = RequirementsParser(str(japanese_requirements_md))
        result = parser.parse()

        # Check Japanese requirement IDs extracted
        assert len(result["requirements"]) >= 2
        req_ids = [req["req_id"] for req in result["requirements"]]
        assert "要件-001" in req_ids
        assert "機能-002" in req_ids

    def test_extract_scope(self, sample_requirements_md):
        """Test scope extraction"""
        parser = RequirementsParser(str(sample_requirements_md))
        result = parser.parse()

        # Check in-scope items
        assert len(result["scope_in"]) > 0
        assert any("registration" in item.lower() for item in result["scope_in"])

        # Check out-of-scope items
        assert len(result["scope_out"]) > 0
        assert any("oauth" in item.lower() or "mobile" in item.lower() for item in result["scope_out"])

    def test_extract_tech_stack(self, sample_requirements_md):
        """Test technology stack extraction"""
        parser = RequirementsParser(str(sample_requirements_md))
        result = parser.parse()

        tech_stack = result["tech_stack"]

        # Check technology mentions
        assert "frontend" in tech_stack or "mentioned" in tech_stack
        if "mentioned" in tech_stack:
            assert "React" in tech_stack["mentioned"]
            assert "Django" in tech_stack["mentioned"]
            assert "PostgreSQL" in tech_stack["mentioned"]

    def test_categorize_requirements(self, sample_requirements_md):
        """Test requirement categorization"""
        parser = RequirementsParser(str(sample_requirements_md))
        result = parser.parse()

        # Check categories assigned
        for req in result["requirements"]:
            assert "category" in req
            assert req["category"] in ["functional", "non_functional", "general", "use_case", "unknown"]

        # Check specific categorizations
        req_dict = {req["req_id"]: req for req in result["requirements"]}
        if "FR-003" in req_dict:
            assert req_dict["FR-003"]["category"] == "functional"
        if "NFR-001" in req_dict:
            assert req_dict["NFR-001"]["category"] == "non_functional"

    def test_file_not_found(self):
        """Test handling of non-existent file"""
        with pytest.raises(FileNotFoundError):
            RequirementsParser("/nonexistent/file.md")

    def test_duplicate_requirement_ids(self, tmp_path):
        """Test handling of duplicate requirement IDs"""
        content = """
# Requirements

- REQ-001: First mention
- REQ-002: Second requirement
- REQ-001: Duplicate mention (should be deduplicated)
"""
        req_file = tmp_path / "dup_requirements.md"
        req_file.write_text(content)

        parser = RequirementsParser(str(req_file))
        result = parser.parse()

        # Check duplicates removed
        req_ids = [req["req_id"] for req in result["requirements"]]
        assert req_ids.count("REQ-001") == 1  # Only one instance

    def test_extract_requirement_descriptions(self, sample_requirements_md):
        """Test that requirement descriptions are extracted"""
        parser = RequirementsParser(str(sample_requirements_md))
        result = parser.parse()

        # Find REQ-001 and check description
        req_001 = next((req for req in result["requirements"] if req["req_id"] == "REQ-001"), None)
        assert req_001 is not None
        assert "description" in req_001
        assert len(req_001["description"]) > 0
        assert "authentication" in req_001["description"].lower() or "email" in req_001["description"].lower()
