"""Tests for KPI Framework Generator."""

import json
import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from generate_kpi_framework import (
    KPI,
    IndicatorType,
    KPIFramework,
    KPIFrameworkGenerator,
    KPIValidator,
    SMARTScore,
    SMARTValidation,
)


class TestKPI:
    """Tests for KPI dataclass."""

    def test_kpi_creation(self):
        kpi = KPI(name="Revenue Growth", description="YoY revenue growth")
        assert kpi.name == "Revenue Growth"
        assert kpi.description == "YoY revenue growth"
        assert kpi.indicator_type == IndicatorType.LAGGING

    def test_kpi_to_dict(self):
        kpi = KPI(
            name="NPS",
            description="Net Promoter Score",
            formula="% Promoters - % Detractors",
            indicator_type=IndicatorType.LEADING,
        )
        result = kpi.to_dict()
        assert result["name"] == "NPS"
        assert result["indicator_type"] == "Leading"
        assert "formula" in result


class TestSMARTValidation:
    """Tests for SMART validation scoring."""

    def test_overall_score_all_pass(self):
        validation = SMARTValidation(
            kpi_name="Test KPI",
            specific=SMARTScore.PASS,
            measurable=SMARTScore.PASS,
            achievable=SMARTScore.PASS,
            relevant=SMARTScore.PASS,
            time_bound=SMARTScore.PASS,
        )
        assert validation.overall_score == 100
        assert validation.status == "Strong"

    def test_overall_score_mixed(self):
        validation = SMARTValidation(
            kpi_name="Test KPI",
            specific=SMARTScore.PASS,
            measurable=SMARTScore.PARTIAL,
            achievable=SMARTScore.PASS,
            relevant=SMARTScore.FAIL,
            time_bound=SMARTScore.PARTIAL,
        )
        # 20 + 10 + 20 + 0 + 10 = 60
        assert validation.overall_score == 60
        assert validation.status == "Acceptable"

    def test_overall_score_all_fail(self):
        validation = SMARTValidation(kpi_name="Test KPI")
        assert validation.overall_score == 0
        assert validation.status == "Weak"

    def test_status_thresholds(self):
        # Test each threshold boundary
        cases = [
            (80, "Strong"),
            (79, "Acceptable"),
            (60, "Acceptable"),
            (59, "Needs Improvement"),
            (40, "Needs Improvement"),
            (39, "Weak"),
        ]
        for score, expected_status in cases:
            v = SMARTValidation(kpi_name="Test")
            # Mock score by setting criteria
            # Score 80 = 4 PASS + 0 PARTIAL
            v.specific = SMARTScore.PASS if score >= 20 else SMARTScore.FAIL
            v.measurable = SMARTScore.PASS if score >= 40 else SMARTScore.FAIL
            v.achievable = SMARTScore.PASS if score >= 60 else SMARTScore.FAIL
            v.relevant = SMARTScore.PASS if score >= 80 else SMARTScore.FAIL
            v.time_bound = SMARTScore.PASS if score >= 100 else SMARTScore.FAIL


class TestKPIValidator:
    """Tests for KPI validation logic."""

    @pytest.fixture
    def validator(self):
        return KPIValidator()

    def test_validate_specific_kpi(self, validator):
        """KPIs with rate/score terms should pass Specific criteria."""
        result = validator.validate_kpi("Customer Churn Rate")
        assert result.specific == SMARTScore.PASS

    def test_validate_vague_kpi(self, validator):
        """Vague KPI names should get partial Specific score."""
        result = validator.validate_kpi("Improve Customer Experience")
        assert result.specific == SMARTScore.PARTIAL

    def test_validate_measurable_with_number(self, validator):
        """KPIs with numeric values should pass Measurable."""
        result = validator.validate_kpi("Achieve 95% Uptime")
        assert result.measurable == SMARTScore.PASS

    def test_validate_measurable_with_score_keyword(self, validator):
        """KPIs with 'score' keyword should pass Measurable."""
        result = validator.validate_kpi("Net Promoter Score")
        assert result.measurable == SMARTScore.PASS

    def test_validate_unmeasurable(self, validator):
        """KPIs without measurable components should fail."""
        result = validator.validate_kpi("Customer Happiness")
        assert result.measurable == SMARTScore.PARTIAL

    def test_validate_achievable_extreme(self, validator):
        """Extreme targets should get partial Achievable score."""
        result = validator.validate_kpi("Achieve 100% Customer Satisfaction")
        assert result.achievable == SMARTScore.PARTIAL

    def test_validate_relevant_business_term(self, validator):
        """KPIs with business terms should pass Relevant."""
        result = validator.validate_kpi("Customer Retention Rate")
        assert result.relevant == SMARTScore.PASS

    def test_validate_time_bound_with_frequency(self, validator):
        """KPIs with time keywords should pass Time-bound."""
        result = validator.validate_kpi("Monthly Active Users")
        assert result.time_bound == SMARTScore.PASS

    def test_validate_time_bound_missing(self, validator):
        """KPIs without time reference should fail Time-bound."""
        result = validator.validate_kpi("Revenue Growth")
        assert result.time_bound == SMARTScore.FAIL

    def test_validate_multiple_kpis(self, validator):
        """Validate multiple KPIs at once."""
        kpis = ["NPS", "Churn Rate", "Revenue"]
        results = validator.validate_kpis(kpis)
        assert len(results) == 3
        assert all(isinstance(r, SMARTValidation) for r in results)

    def test_validation_notes_populated(self, validator):
        """Notes should be populated for failed criteria."""
        result = validator.validate_kpi("General Performance")
        assert len(result.notes) > 0

    def test_to_markdown_format(self, validator):
        """Markdown output should be properly formatted."""
        validations = validator.validate_kpis(["NPS", "Revenue Growth"])
        md = validator.to_markdown(validations)
        assert "# KPI SMART Validation Report" in md
        assert "| KPI | Score | Status | Notes |" in md
        assert "NPS" in md


class TestKPIFrameworkGenerator:
    """Tests for KPI framework generation."""

    @pytest.fixture
    def generator(self):
        return KPIFrameworkGenerator(
            objectives=["Increase revenue 20%", "Improve customer satisfaction"],
            industry="SaaS",
            level="Company",
        )

    def test_categorize_revenue_objective(self, generator):
        categories = generator._categorize_objective("Increase revenue by 20%")
        assert "revenue" in categories

    def test_categorize_customer_objective(self, generator):
        categories = generator._categorize_objective("Improve customer satisfaction")
        assert "customer" in categories

    def test_categorize_efficiency_objective(self, generator):
        categories = generator._categorize_objective("Reduce operational costs")
        assert "efficiency" in categories

    def test_categorize_quality_objective(self, generator):
        categories = generator._categorize_objective("Reduce defect rate")
        assert "quality" in categories

    def test_categorize_default(self, generator):
        """Unknown objectives should default to revenue."""
        categories = generator._categorize_objective("Do something amazing")
        assert categories == ["revenue"]

    def test_generate_framework_structure(self, generator):
        framework = generator.generate_framework()
        assert isinstance(framework, KPIFramework)
        assert framework.industry == "SaaS"
        assert framework.level == "Company"
        assert len(framework.objectives) == 2

    def test_generate_framework_has_kpis(self, generator):
        framework = generator.generate_framework()
        total_kpis = len(framework.strategic_kpis) + len(framework.tactical_kpis) + len(framework.operational_kpis)
        assert total_kpis > 0

    def test_to_markdown_contains_sections(self, generator):
        framework = generator.generate_framework()
        md = generator.to_markdown(framework)

        assert "# KPI Framework:" in md
        assert "## Strategic Objectives" in md
        assert "## KPI Hierarchy" in md
        assert "### Tier 1: Strategic KPIs" in md
        assert "### Tier 2: Tactical KPIs" in md
        assert "### Tier 3: Operational KPIs" in md
        assert "## KPI Definitions" in md
        assert "## Next Steps" in md

    def test_to_markdown_includes_objectives(self, generator):
        framework = generator.generate_framework()
        md = generator.to_markdown(framework)
        assert "Increase revenue 20%" in md
        assert "Improve customer satisfaction" in md


class TestIntegration:
    """Integration tests for the full workflow."""

    def test_full_framework_generation_workflow(self):
        """Test complete framework generation from objectives to markdown."""
        objectives = [
            "Grow revenue by 30%",
            "Reduce customer churn to under 5%",
            "Improve operational efficiency",
        ]
        generator = KPIFrameworkGenerator(objectives, "SaaS", "Company")
        framework = generator.generate_framework()
        markdown = generator.to_markdown(framework)

        # Verify structure
        assert framework.name == "SaaS KPI Framework"
        assert len(framework.objectives) == 3

        # Verify markdown output
        assert "| KPI | Type | Formula | Frequency |" in markdown
        assert "**Type**:" in markdown
        assert "**Formula**:" in markdown

    def test_full_validation_workflow(self):
        """Test complete validation from KPI names to report."""
        kpis = [
            "Monthly Recurring Revenue",
            "Customer Satisfaction Score",
            "Improve Quality",
        ]
        validator = KPIValidator()
        validations = validator.validate_kpis(kpis)
        markdown = validator.to_markdown(validations)

        # First KPI should score well
        assert validations[0].overall_score >= 40

        # Last KPI (vague) should score lower
        assert validations[2].overall_score < validations[0].overall_score

        # Markdown should contain all KPIs
        for kpi in kpis:
            assert kpi in markdown


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
