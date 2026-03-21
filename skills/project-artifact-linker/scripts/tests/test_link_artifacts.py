"""
Tests for link_artifacts.py
"""

import pytest
from link_artifacts import ArtifactLinker


class TestKeywordExtraction:
    """Tests for keyword extraction functionality."""

    def test_extract_keywords_basic(self):
        """Test basic keyword extraction."""
        linker = ArtifactLinker({})
        keywords = linker._extract_keywords("Review the security requirements")
        assert "review" in keywords
        assert "security" in keywords
        assert "requirements" in keywords

    def test_extract_keywords_removes_stopwords(self):
        """Test that stopwords are removed."""
        linker = ArtifactLinker({})
        keywords = linker._extract_keywords("The system will have authentication")
        assert "the" not in keywords
        assert "will" not in keywords
        assert "have" not in keywords
        assert "system" in keywords
        assert "authentication" in keywords

    def test_extract_keywords_empty_text(self):
        """Test keyword extraction from empty text."""
        linker = ArtifactLinker({})
        keywords = linker._extract_keywords("")
        assert keywords == set()


class TestSimilarityCalculations:
    """Tests for similarity calculation functions."""

    def test_jaccard_identical_sets(self):
        """Test Jaccard similarity with identical sets."""
        linker = ArtifactLinker({})
        sim = linker._jaccard_similarity({"a", "b", "c"}, {"a", "b", "c"})
        assert sim == 1.0

    def test_jaccard_disjoint_sets(self):
        """Test Jaccard similarity with disjoint sets."""
        linker = ArtifactLinker({})
        sim = linker._jaccard_similarity({"a", "b"}, {"c", "d"})
        assert sim == 0.0

    def test_jaccard_partial_overlap(self):
        """Test Jaccard similarity with partial overlap."""
        linker = ArtifactLinker({})
        sim = linker._jaccard_similarity({"a", "b", "c"}, {"b", "c", "d"})
        # Intersection: {b, c} = 2, Union: {a, b, c, d} = 4
        assert sim == 0.5

    def test_jaccard_empty_sets(self):
        """Test Jaccard similarity with empty sets."""
        linker = ArtifactLinker({})
        sim = linker._jaccard_similarity(set(), set())
        assert sim == 0.0


class TestOwnerMatching:
    """Tests for owner name matching."""

    def test_exact_owner_match(self):
        """Test exact owner name match."""
        linker = ArtifactLinker({})
        score = linker._owner_match_score("Alice Smith", "Alice Smith")
        assert score == 1.0

    def test_case_insensitive_match(self):
        """Test case-insensitive owner matching."""
        linker = ArtifactLinker({})
        score = linker._owner_match_score("alice smith", "Alice Smith")
        assert score == 1.0

    def test_first_name_partial_match(self):
        """Test partial match on first name."""
        linker = ArtifactLinker({})
        score = linker._owner_match_score("Alice", "Alice Smith")
        assert score == 0.7

    def test_no_match(self):
        """Test non-matching owners."""
        linker = ArtifactLinker({})
        score = linker._owner_match_score("Alice", "Bob")
        assert score == 0.0

    def test_none_owner(self):
        """Test with None owner."""
        linker = ArtifactLinker({})
        score = linker._owner_match_score(None, "Alice")
        assert score == 0.0


class TestDomainDetection:
    """Tests for domain category detection."""

    def test_security_domain(self):
        """Test detection of security domain."""
        linker = ArtifactLinker({})
        domain = linker._get_domain("Implement OAuth2 authentication")
        assert domain == "security"

    def test_performance_domain(self):
        """Test detection of performance domain."""
        linker = ArtifactLinker({})
        domain = linker._get_domain("Optimize response time latency")
        assert domain == "performance"

    def test_data_domain(self):
        """Test detection of data domain."""
        linker = ArtifactLinker({})
        domain = linker._get_domain("Database schema migration")
        assert domain == "data"

    def test_no_domain(self):
        """Test text with no clear domain."""
        linker = ArtifactLinker({})
        domain = linker._get_domain("Generic task description")
        assert domain is None


class TestDateProximity:
    """Tests for date proximity scoring."""

    def test_same_date(self):
        """Test proximity score for same date."""
        linker = ArtifactLinker({})
        score = linker._date_proximity_score("2024-01-15", "2024-01-15")
        assert score == 1.0

    def test_date_within_range(self):
        """Test proximity score for dates within range."""
        linker = ArtifactLinker({})
        score = linker._date_proximity_score("2024-01-15", "2024-01-25", max_days=30)
        assert 0 < score < 1

    def test_date_beyond_range(self):
        """Test proximity score for dates beyond range."""
        linker = ArtifactLinker({})
        score = linker._date_proximity_score("2024-01-15", "2024-03-15", max_days=30)
        assert score == 0.0

    def test_invalid_date(self):
        """Test proximity score with invalid date."""
        linker = ArtifactLinker({})
        score = linker._date_proximity_score("invalid", "2024-01-15")
        assert score == 0.0


class TestActionItemToWBSLinking:
    """Tests for action item to WBS task linking."""

    def test_link_by_owner_match(self):
        """Test linking action items to tasks by owner."""
        artifacts = {
            "meetings": [
                {
                    "id": "MTG-001",
                    "action_items": [
                        {
                            "id": "AI-001",
                            "description": "Review requirements",
                            "owner": "Alice",
                        }
                    ],
                }
            ],
            "wbs_tasks": [
                {
                    "id": "WBS-1.1",
                    "name": "Requirements Analysis",
                    "owner": "Alice",
                }
            ],
        }
        linker = ArtifactLinker(artifacts)
        links = linker.link_action_items_to_wbs()

        assert len(links) >= 1
        assert links[0].source_type == "action_item"
        assert links[0].target_type == "wbs_task"

    def test_link_by_keyword_overlap(self):
        """Test linking by keyword overlap."""
        artifacts = {
            "meetings": [
                {
                    "id": "MTG-001",
                    "action_items": [
                        {
                            "id": "AI-001",
                            "description": "Implement authentication module",
                            "owner": "Bob",
                        }
                    ],
                }
            ],
            "wbs_tasks": [
                {
                    "id": "WBS-1.1",
                    "name": "Authentication implementation",
                    "owner": "Charlie",
                }
            ],
        }
        linker = ArtifactLinker(artifacts)
        links = linker.link_action_items_to_wbs()

        # Should find link due to keyword overlap (authentication, implement)
        assert len(links) >= 1


class TestDecisionToRequirementLinking:
    """Tests for decision to requirement linking."""

    def test_link_by_keyword_match(self):
        """Test linking decisions to requirements by keyword."""
        artifacts = {
            "meetings": [
                {
                    "id": "MTG-001",
                    "decisions": [
                        {
                            "id": "DEC-001",
                            "description": "Adopt OAuth2 for authentication",
                        }
                    ],
                }
            ],
            "decisions": [],
            "requirements": [
                {
                    "id": "REQ-SEC-001",
                    "description": "System shall support OAuth2 authentication",
                }
            ],
        }
        linker = ArtifactLinker(artifacts)
        links = linker.link_decisions_to_requirements()

        assert len(links) >= 1
        assert links[0].source_type == "decision"
        assert links[0].target_type == "requirement"


class TestFullLinkBuilding:
    """Tests for complete link building."""

    def test_build_all_links(self):
        """Test building all types of links."""
        artifacts = {
            "meetings": [
                {
                    "id": "MTG-001",
                    "date": "2024-01-15",
                    "attendees": ["Alice", "Bob"],
                    "action_items": [
                        {
                            "id": "AI-001",
                            "description": "Review security specs",
                            "owner": "Alice",
                        }
                    ],
                    "decisions": [
                        {
                            "id": "DEC-001",
                            "description": "Use OAuth2 authentication",
                        }
                    ],
                }
            ],
            "wbs_tasks": [
                {
                    "id": "WBS-1.1",
                    "name": "Security review",
                    "owner": "Alice",
                    "start_date": "2024-01-10",
                    "end_date": "2024-01-20",
                }
            ],
            "requirements": [
                {
                    "id": "REQ-SEC-001",
                    "description": "OAuth2 authentication required",
                }
            ],
            "decisions": [],
        }
        linker = ArtifactLinker(artifacts)
        links = linker.build_all_links()

        # Should have created various link types
        assert len(links) > 0

        # Check output format
        result = linker.to_dict()
        assert "schema_version" in result
        assert "link_date" in result
        assert "links" in result


class TestLinkConfidence:
    """Tests for link confidence scoring."""

    def test_high_confidence_link(self):
        """Test that strong matches get high confidence."""
        artifacts = {
            "meetings": [
                {
                    "id": "MTG-001",
                    "action_items": [
                        {
                            "id": "AI-001",
                            "description": "Alice to complete security authentication task WBS-1.1",
                            "owner": "Alice",
                            "due_date": "2024-01-20",
                        }
                    ],
                }
            ],
            "wbs_tasks": [
                {
                    "id": "WBS-1.1",
                    "name": "Security authentication implementation",
                    "owner": "Alice",
                    "end_date": "2024-01-20",
                }
            ],
            "decisions": [],
            "requirements": [],
        }
        linker = ArtifactLinker(artifacts)
        links = linker.link_action_items_to_wbs()

        if links:
            # Should have high confidence due to multiple matching criteria
            assert links[0].confidence >= 0.5

    def test_low_confidence_filtered(self):
        """Test that weak matches are filtered out."""
        artifacts = {
            "meetings": [
                {
                    "id": "MTG-001",
                    "action_items": [
                        {
                            "id": "AI-001",
                            "description": "Order office supplies",
                            "owner": "Alice",
                        }
                    ],
                }
            ],
            "wbs_tasks": [
                {
                    "id": "WBS-1.1",
                    "name": "Database migration",
                    "owner": "Bob",
                }
            ],
            "decisions": [],
            "requirements": [],
        }
        linker = ArtifactLinker(artifacts)
        links = linker.link_action_items_to_wbs()

        # No link should be created due to low similarity
        assert len(links) == 0
