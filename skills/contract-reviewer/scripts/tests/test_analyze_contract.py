"""
Tests for analyze_contract.py

Run with: python -m pytest skills/contract-reviewer/scripts/tests/test_analyze_contract.py -v
"""

import sys
from pathlib import Path

import pytest

# Add scripts directory to path for imports
scripts_dir = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_dir))

from analyze_contract import (
    AnalysisResult,
    ContractInfo,
    RedFlag,
    _has_negation_context,
    analyze_contract,
    calculate_risk_score,
    check_clause_coverage,
    detect_contract_type,
    detect_red_flags,
    extract_contract_info,
    generate_recommendations,
    generate_report,
    main,
    read_file,
)
from pattern_definitions import CLAUSE_PATTERNS, CONTRACT_TYPE_PATTERNS, RED_FLAG_PATTERNS


class TestContractTypeDetection:
    """Tests for contract type detection."""

    def test_detect_nda(self):
        text = "This Non-Disclosure Agreement is entered into between..."
        assert detect_contract_type(text) == "NDA"

    def test_detect_msa(self):
        text = "This Master Services Agreement governs the relationship..."
        assert detect_contract_type(text) == "MSA"

    def test_detect_sow(self):
        text = "This Statement of Work describes the services to be provided..."
        assert detect_contract_type(text) == "SOW"

    def test_detect_sla(self):
        text = "This Service Level Agreement defines uptime guarantees..."
        assert detect_contract_type(text) == "SLA"

    def test_detect_license(self):
        text = "This Software License Agreement grants the licensee..."
        assert detect_contract_type(text) == "License"

    def test_detect_unknown(self):
        text = "Random text without contract keywords."
        assert detect_contract_type(text) == "Unknown"

    def test_override_type(self):
        text = "This is actually a license agreement."
        assert detect_contract_type(text, override_type="nda") == "NDA"


class TestRedFlagDetection:
    """Tests for red flag pattern detection."""

    def test_detect_unlimited_liability(self):
        text = "The customer shall have unlimited liability for any damages."
        red_flags = detect_red_flags(text)
        assert any(rf.pattern_id == "RF001" for rf in red_flags)

    def test_detect_one_sided_indemnification(self):
        text = "Customer shall indemnify, defend, and hold harmless the vendor."
        red_flags = detect_red_flags(text)
        assert any(rf.pattern_id == "RF002" for rf in red_flags)

    def test_detect_auto_renewal_long_notice(self):
        text = "This agreement shall automatically renew unless notice is given 120 days prior."
        red_flags = detect_red_flags(text)
        assert any(rf.pattern_id == "RF003" for rf in red_flags)

    def test_detect_unilateral_amendment(self):
        text = "Provider may modify the terms of this agreement at any time."
        red_flags = detect_red_flags(text)
        assert any(rf.pattern_id == "RF004" for rf in red_flags)

    def test_no_false_positives_on_clean_contract(self):
        text = """
        This Agreement is between Party A and Party B.
        Each party shall maintain reasonable liability insurance.
        Termination requires 30 days written notice.
        """
        red_flags = detect_red_flags(text)
        # Should not detect critical red flags in standard language
        critical_flags = [rf for rf in red_flags if rf.severity == "Critical"]
        assert len(critical_flags) == 0

    # --- RF003 boundary tests (HIGH-1) ---

    def test_rf003_does_not_match_90_days(self):
        """90 days is the threshold boundary - should NOT trigger RF003."""
        text = "This agreement shall automatically renew unless notice is given 90 days prior."
        red_flags = detect_red_flags(text)
        assert not any(rf.pattern_id == "RF003" for rf in red_flags)

    def test_rf003_matches_91_days(self):
        """91 days exceeds threshold - should trigger RF003."""
        text = "This agreement shall automatically renew unless notice is given 91 days prior."
        red_flags = detect_red_flags(text)
        assert any(rf.pattern_id == "RF003" for rf in red_flags)

    def test_rf003_matches_120_days(self):
        """120 days clearly exceeds threshold - should trigger RF003."""
        text = "This agreement shall automatically renew unless notice is given 120 days prior."
        red_flags = detect_red_flags(text)
        assert any(rf.pattern_id == "RF003" for rf in red_flags)

    # --- RF005 absence tests (HIGH-3) ---

    def test_rf005_no_flag_when_exclusion_present(self):
        """When consequential damages ARE excluded, RF005 should not fire."""
        text = "Consequential damages shall be excluded from any liability under this agreement."
        red_flags = detect_red_flags(text)
        assert not any(rf.pattern_id == "RF005" for rf in red_flags)

    def test_rf005_flags_when_no_exclusion(self):
        """When consequential damages are mentioned but NOT excluded, RF005 should fire."""
        text = "The vendor shall be liable for consequential damages arising from breach."
        red_flags = detect_red_flags(text)
        assert any(rf.pattern_id == "RF005" for rf in red_flags)

    def test_rf005_no_flag_with_waiver(self):
        """When consequential damages are waived, RF005 should not fire."""
        text = "Each party waives any claim for consequential damages."
        red_flags = detect_red_flags(text)
        assert not any(rf.pattern_id == "RF005" for rf in red_flags)

    def test_rf005_no_flag_when_no_mention(self):
        """When consequential damages are not mentioned at all, RF005 should not fire."""
        text = "This agreement covers basic service terms and payment schedules."
        red_flags = detect_red_flags(text)
        assert not any(rf.pattern_id == "RF005" for rf in red_flags)

    # --- RF007 absence tests (HIGH-2) ---

    def test_rf007_no_flag_when_convenience_granted(self):
        """When termination for convenience IS present, RF007 should not fire."""
        text = "Either party may terminate this agreement for convenience upon 30 days notice."
        red_flags = detect_red_flags(text)
        assert not any(rf.pattern_id == "RF007" for rf in red_flags)

    def test_rf007_flags_when_no_convenience_right(self):
        """When termination exists but no convenience right, RF007 should fire."""
        text = "This agreement may be terminated only for material breach."
        red_flags = detect_red_flags(text)
        assert any(rf.pattern_id == "RF007" for rf in red_flags)

    def test_rf007_no_flag_with_at_will(self):
        """'At will' termination should satisfy the convenience requirement."""
        text = "Either party may terminate this agreement at will with 30 days notice."
        red_flags = detect_red_flags(text)
        assert not any(rf.pattern_id == "RF007" for rf in red_flags)

    def test_rf007_no_flag_when_termination_not_mentioned(self):
        """When termination is not mentioned at all, RF007 should not fire."""
        text = "This agreement covers basic service terms and payment schedules."
        red_flags = detect_red_flags(text)
        assert not any(rf.pattern_id == "RF007" for rf in red_flags)

    # --- RF002 absence tests (MEDIUM-7) ---

    def test_rf002_no_flag_when_mutual_indemnification(self):
        """When mutual indemnification exists, RF002 should not fire."""
        text = (
            "Customer shall indemnify vendor for customer's breach. "
            "Vendor shall indemnify customer for vendor's breach."
        )
        red_flags = detect_red_flags(text)
        assert not any(rf.pattern_id == "RF002" for rf in red_flags)

    def test_rf002_flags_one_sided_indemnification(self):
        """When only customer indemnifies, RF002 should fire."""
        text = "Customer shall indemnify, defend, and hold harmless the vendor against all claims."
        red_flags = detect_red_flags(text)
        assert any(rf.pattern_id == "RF002" for rf in red_flags)

    def test_rf002_no_flag_when_each_party_indemnifies(self):
        """'Each party shall indemnify' should satisfy the mutual requirement."""
        text = "Customer shall indemnify vendor for breach. Each party shall indemnify the other for its negligence."
        red_flags = detect_red_flags(text)
        assert not any(rf.pattern_id == "RF002" for rf in red_flags)

    # --- Absence mode duplicate prevention (review concern #1) ---

    def test_absence_mode_produces_max_one_flag(self):
        """prerequisite that matches multiple times should still produce only 1 red flag."""
        text = (
            "Customer shall indemnify vendor for breach. "
            "Customer shall indemnify vendor for negligence. "
            "Customer shall indemnify vendor for IP claims."
        )
        red_flags = detect_red_flags(text)
        rf002_count = sum(1 for rf in red_flags if rf.pattern_id == "RF002")
        assert rf002_count == 1

    # --- RF006/RF008/RF009/RF010 tests (MEDIUM-5) ---

    def test_rf006_broad_ip_assignment(self):
        text = "Customer agrees to assign all intellectual property rights to the vendor."
        red_flags = detect_red_flags(text)
        assert any(rf.pattern_id == "RF006" for rf in red_flags)

    def test_rf006_no_false_positive_on_limited_ip(self):
        text = "Customer retains all intellectual property rights to pre-existing work."
        red_flags = detect_red_flags(text)
        assert not any(rf.pattern_id == "RF006" for rf in red_flags)

    def test_rf008_excessive_termination_penalty(self):
        text = "Early termination fee shall be 100% of all remaining contract payments."
        red_flags = detect_red_flags(text)
        assert any(rf.pattern_id == "RF008" for rf in red_flags)

    def test_rf008_no_false_positive_on_reasonable_penalty(self):
        text = "Early termination fee shall be a prorated portion of the monthly fee."
        red_flags = detect_red_flags(text)
        assert not any(rf.pattern_id == "RF008" for rf in red_flags)

    def test_rf009_residual_knowledge(self):
        text = "Information retained in unaided memory may be used freely without restriction."
        red_flags = detect_red_flags(text)
        assert any(rf.pattern_id == "RF009" for rf in red_flags)

    def test_rf010_sole_exclusive_remedy(self):
        text = "The sole and exclusive remedy for any SLA breach shall be a service level credit."
        red_flags = detect_red_flags(text)
        assert any(rf.pattern_id == "RF010" for rf in red_flags)

    def test_rf010_no_false_positive_on_additional_remedies(self):
        text = "In addition to service credits, customer may pursue additional remedies at law."
        red_flags = detect_red_flags(text)
        assert not any(rf.pattern_id == "RF010" for rf in red_flags)


class TestContractInfoExtraction:
    """Tests for contract information extraction."""

    def test_extract_parties(self):
        text = "This Agreement is between Acme Corporation and Beta LLC."
        info = extract_contract_info(text)
        assert info.parties == ["Acme Corporation", "Beta LLC"]

    def test_extract_effective_date(self):
        text = "This Agreement is effective as of January 1, 2024."
        info = extract_contract_info(text)
        assert info.effective_date == "January 1, 2024"

    def test_detect_auto_renewal(self):
        text = "This Agreement shall automatically renew for successive one-year terms."
        info = extract_contract_info(text)
        assert info.auto_renewal is True

    def test_detect_no_auto_renewal(self):
        text = "This Agreement shall not automatically renew."
        info = extract_contract_info(text)
        assert info.auto_renewal is False

    def test_extract_governing_law(self):
        text = "This Agreement shall be governed by the laws of Delaware."
        info = extract_contract_info(text)
        assert info.governing_law == "Delaware"

    def test_extract_mutual_indemnification(self):
        text = "Each party shall indemnify the other party against claims."
        info = extract_contract_info(text)
        assert info.indemnification_type == "Mutual"


class TestClauseCoverage:
    """Tests for clause coverage checking."""

    def test_detect_liability_clause(self):
        text = "The limitation of liability for this agreement shall not exceed..."
        coverage = check_clause_coverage(text)
        assert coverage.get("Liability") is True

    def test_detect_indemnification_clause(self):
        text = "Party A shall indemnify Party B against all claims."
        coverage = check_clause_coverage(text)
        assert coverage.get("Indemnification") is True

    def test_detect_confidentiality_clause(self):
        text = "All confidential information shall be protected."
        coverage = check_clause_coverage(text)
        assert coverage.get("Confidentiality") is True

    def test_detect_governing_law_clause(self):
        text = "The governing law for this agreement shall be..."
        coverage = check_clause_coverage(text)
        assert coverage.get("Governing Law") is True

    def test_missing_clauses(self):
        text = "This is a very short agreement with minimal terms."
        coverage = check_clause_coverage(text)
        # Most clauses should be missing
        missing = sum(1 for v in coverage.values() if not v)
        assert missing >= 5


class TestRiskScoreCalculation:
    """Tests for risk score calculation."""

    def test_zero_red_flags(self):
        score, level = calculate_risk_score([])
        assert score == 0
        assert level == "Low"

    def test_critical_red_flag(self):
        red_flags = [
            RedFlag(
                pattern_id="RF001",
                title="Test",
                severity="Critical",
                category="Financial",
                clause_text="",
                location="",
                description="",
                recommendation="",
            )
        ]
        score, level = calculate_risk_score(red_flags)
        assert score == 20
        assert level == "Low"  # Single critical = 20, still Low

    def test_multiple_critical_flags(self):
        red_flags = [
            RedFlag(
                pattern_id=f"RF{i}",
                title="Test",
                severity="Critical",
                category="Financial",
                clause_text="",
                location="",
                description="",
                recommendation="",
            )
            for i in range(4)
        ]
        score, level = calculate_risk_score(red_flags)
        assert score == 80
        assert level == "Critical"

    def test_score_capped_at_100(self):
        red_flags = [
            RedFlag(
                pattern_id=f"RF{i}",
                title="Test",
                severity="Critical",
                category="Financial",
                clause_text="",
                location="",
                description="",
                recommendation="",
            )
            for i in range(10)
        ]
        score, level = calculate_risk_score(red_flags)
        assert score == 100


class TestRecommendations:
    """Tests for recommendation generation."""

    def test_recommendations_from_red_flags(self):
        red_flags = [
            RedFlag(
                pattern_id="RF001",
                title="Unlimited Liability",
                severity="Critical",
                category="Financial",
                clause_text="",
                location="",
                description="",
                recommendation="Negotiate cap",
            )
        ]
        coverage = {"Liability": True, "Indemnification": True, "Termination": True, "Governing Law": True}
        recs = generate_recommendations(red_flags, coverage)
        assert len(recs) >= 1
        assert any("Unlimited Liability" in r["issue"] for r in recs)

    def test_recommendations_from_missing_clauses(self):
        red_flags = []
        coverage = {"Liability": False, "Indemnification": True, "Termination": True, "Governing Law": True}
        recs = generate_recommendations(red_flags, coverage)
        assert any("Missing Liability" in r["issue"] for r in recs)


class TestFileReading:
    """Tests for file reading functionality."""

    def test_read_txt_file(self, tmp_path):
        f = tmp_path / "contract.txt"
        f.write_text("Test contract content")
        content = read_file(f)
        assert content == "Test contract content"

    def test_read_md_file(self, tmp_path):
        f = tmp_path / "agreement.md"
        f.write_text("# Test Agreement\n\nContent here.")
        content = read_file(f)
        assert "Test Agreement" in content

    def test_read_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            read_file(Path("/nonexistent/file.txt"))


class TestHasNegationContext:
    """Tests for _has_negation_context helper function."""

    def test_detects_negation(self):
        text = "the company shall not have unlimited liability"
        match_start = text.index("unlimited")
        assert _has_negation_context(text, match_start) is True

    def test_no_negation(self):
        text = "the company has unlimited liability for damages"
        match_start = text.index("unlimited")
        assert _has_negation_context(text, match_start) is False

    def test_negation_within_context_window(self):
        text = "shall not " + "x" * 15 + "unlimited liability"
        match_start = text.index("unlimited")
        assert _has_negation_context(text, match_start, context_chars=30) is True

    def test_negation_outside_context_window(self):
        text = "shall not " + "x" * 50 + "unlimited liability"
        match_start = text.index("unlimited")
        assert _has_negation_context(text, match_start, context_chars=30) is False


class TestGenerateReport:
    """Tests for report generation."""

    def _make_result(self, red_flags=None):
        info = ContractInfo(
            contract_type="MSA",
            parties=["Acme Corp", "Beta LLC"],
            effective_date="January 1, 2024",
            governing_law="Delaware",
        )
        rfs = red_flags or []
        score, level = calculate_risk_score(rfs)
        coverage = {"Liability": True, "Termination": True, "Confidentiality": False}
        recs = generate_recommendations(rfs, coverage)
        return AnalysisResult(
            contract_info=info,
            red_flags=rfs,
            risk_score=score,
            risk_level=level,
            clause_coverage=coverage,
            recommendations=recs,
        )

    def test_report_has_header(self):
        result = self._make_result()
        report = generate_report(result, Path("test.txt"))
        assert "# Preliminary Contract Analysis Report" in report

    def test_report_critical_warning(self):
        rfs = [RedFlag("RF001", "Unlimited Liability", "Critical", "Financial", "", "", "", "") for _ in range(5)]
        result = self._make_result(red_flags=rfs)
        report = generate_report(result, Path("test.txt"))
        assert "WARNING" in report

    def test_report_red_flag_details(self):
        rfs = [
            RedFlag(
                "RF001",
                "Unlimited Liability",
                "Critical",
                "Financial",
                "clause text",
                "line 5",
                "desc",
                "rec",
            )
        ]
        result = self._make_result(red_flags=rfs)
        report = generate_report(result, Path("test.txt"))
        assert "Unlimited Liability" in report
        assert "Critical" in report

    def test_report_no_red_flags_message(self):
        result = self._make_result()
        report = generate_report(result, Path("test.txt"))
        assert "No red flags detected" in report


class TestAnalyzeContract:
    """Integration tests for analyze_contract function."""

    def test_simple_contract(self, tmp_path):
        f = tmp_path / "simple.txt"
        f.write_text(
            "This Agreement is between Acme Corp and Beta LLC. "
            "This Agreement shall be governed by the laws of Delaware. "
            "Termination requires 30 days written notice."
        )
        result = analyze_contract(f)
        assert isinstance(result, AnalysisResult)
        assert result.risk_score >= 0

    def test_risky_contract(self, tmp_path):
        f = tmp_path / "risky.txt"
        f.write_text(
            "The customer shall have unlimited liability for any damages. "
            "Provider may modify the terms of this agreement at any time. "
            "Customer shall indemnify vendor for all losses."
        )
        result = analyze_contract(f)
        assert len(result.red_flags) >= 1
        assert result.risk_score > 0

    def test_type_override(self, tmp_path):
        f = tmp_path / "generic.txt"
        f.write_text("This is a generic contract document with minimal terms.")
        result = analyze_contract(f, contract_type="nda")
        assert result.contract_info.contract_type == "NDA"


class TestMain:
    """Tests for main() CLI entry point."""

    def test_file_not_found(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["analyze_contract.py", "/nonexistent/file.txt"])
        exit_code = main()
        assert exit_code == 1

    def test_output_file(self, tmp_path, monkeypatch):
        contract = tmp_path / "contract.txt"
        contract.write_text("This is a simple agreement between parties.")
        output = tmp_path / "report.md"
        monkeypatch.setattr(
            "sys.argv",
            ["analyze_contract.py", str(contract), "--output", str(output)],
        )
        exit_code = main()
        assert exit_code in (0, 1, 2, 3)
        assert output.exists()

    def test_stdout_output(self, tmp_path, monkeypatch, capsys):
        contract = tmp_path / "contract.txt"
        contract.write_text("This is a simple agreement between parties.")
        monkeypatch.setattr("sys.argv", ["analyze_contract.py", str(contract)])
        exit_code = main()
        assert exit_code in (0, 1, 2, 3)
        captured = capsys.readouterr()
        assert "Preliminary Contract Analysis Report" in captured.out


class TestPatternDefinitions:
    """Tests for pattern definition completeness."""

    def test_red_flag_patterns_have_required_fields(self):
        required_fields = ["id", "title", "pattern", "severity", "category", "description", "recommendation"]
        for pattern in RED_FLAG_PATTERNS:
            for field in required_fields:
                assert field in pattern, f"Pattern {pattern.get('id', 'unknown')} missing {field}"

    def test_red_flag_severities_valid(self):
        valid_severities = {"Critical", "High", "Medium", "Low"}
        for pattern in RED_FLAG_PATTERNS:
            assert pattern["severity"] in valid_severities

    def test_contract_type_patterns_exist(self):
        expected_types = {"NDA", "MSA", "SOW", "SLA", "License"}
        assert set(CONTRACT_TYPE_PATTERNS.keys()) == expected_types

    def test_clause_patterns_exist(self):
        expected_clauses = {
            "Definitions",
            "Term",
            "Termination",
            "Liability",
            "Indemnification",
            "Confidentiality",
            "IP Rights",
            "Data Protection",
            "Governing Law",
            "Force Majeure",
            "Assignment",
            "Amendment",
        }
        assert set(CLAUSE_PATTERNS.keys()) == expected_clauses

    def test_red_flag_detection_modes_valid(self):
        """All detection_mode values must be 'regex' or 'absence'."""
        valid_modes = {"regex", "absence"}
        for pattern in RED_FLAG_PATTERNS:
            mode = pattern.get("detection_mode", "regex")
            assert mode in valid_modes, f"Pattern {pattern['id']} has invalid detection_mode: {mode}"

    def test_absence_patterns_have_prerequisite(self):
        """Patterns with detection_mode='absence' must have prerequisite_pattern."""
        for pattern in RED_FLAG_PATTERNS:
            if pattern.get("detection_mode") == "absence":
                assert "prerequisite_pattern" in pattern, (
                    f"Pattern {pattern['id']} has absence mode but no prerequisite_pattern"
                )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
