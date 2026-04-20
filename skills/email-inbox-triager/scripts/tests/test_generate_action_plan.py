"""
Tests for action plan generation.
"""

import json
from pathlib import Path

import pytest
from generate_action_plan import ActionPlanGenerator


@pytest.fixture
def generator():
    """Action plan generator with default 60 min budget."""
    return ActionPlanGenerator(time_budget=60)


@pytest.fixture
def sample_report():
    """Sample classification report for testing."""
    return {
        "schema_version": "1.0",
        "generated_at": "2025-01-15T09:30:00Z",
        "total_emails": 10,
        "summary": {
            "urgent_response": 2,
            "response_needed": 3,
            "fyi_read": 3,
            "delegatable": 1,
            "archive": 1,
        },
        "emails": [
            {
                "id": "msg_1",
                "thread_id": "thread_1",
                "from_addr": "CEO <ceo@company.com>",
                "subject": "Q4 Budget Review - URGENT",
                "snippet": "Please review...",
                "date": "2025-01-15T08:15:00Z",
                "classification": "urgent-response",
                "urgency_score": 95,
                "signals": ["vip_sender", "deadline_keyword"],
                "suggested_action": "Reply with budget feedback by 5pm",
                "estimated_minutes": 15,
            },
            {
                "id": "msg_2",
                "thread_id": "thread_2",
                "from_addr": "client@keyclient.org",
                "subject": "Contract Question",
                "snippet": "Need clarification...",
                "date": "2025-01-15T08:00:00Z",
                "classification": "urgent-response",
                "urgency_score": 75,
                "signals": ["vip_sender", "direct_question"],
                "suggested_action": "Clarify contract terms",
                "estimated_minutes": 10,
            },
            {
                "id": "msg_3",
                "thread_id": "thread_3",
                "from_addr": "team@company.com",
                "subject": "Sprint Planning",
                "snippet": "Confirm availability...",
                "date": "2025-01-15T09:00:00Z",
                "classification": "response-needed",
                "urgency_score": 45,
                "signals": ["reply_expected"],
                "suggested_action": "Confirm availability",
                "estimated_minutes": 5,
            },
            {
                "id": "msg_4",
                "thread_id": "thread_4",
                "from_addr": "colleague@company.com",
                "subject": "Document Review",
                "snippet": "Please review when you can...",
                "date": "2025-01-15T07:00:00Z",
                "classification": "response-needed",
                "urgency_score": 40,
                "signals": ["direct_question"],
                "suggested_action": "Review document",
                "estimated_minutes": 10,
            },
            {
                "id": "msg_5",
                "thread_id": "thread_5",
                "from_addr": "hr@company.com",
                "subject": "Meeting Request",
                "snippet": "Schedule meeting...",
                "date": "2025-01-15T06:30:00Z",
                "classification": "response-needed",
                "urgency_score": 35,
                "signals": [],
                "suggested_action": "Schedule meeting",
                "estimated_minutes": 3,
            },
            {
                "id": "msg_6",
                "thread_id": "thread_6",
                "from_addr": "vendor@supplier.com",
                "subject": "Invoice #12345",
                "snippet": "Payment reminder...",
                "date": "2025-01-14T14:00:00Z",
                "classification": "delegatable",
                "urgency_score": 20,
                "signals": [],
                "suggested_action": "Forward to finance@",
                "estimated_minutes": 2,
                "delegate_to": "finance@",
            },
            {
                "id": "msg_7",
                "thread_id": "thread_7",
                "from_addr": "newsletter@marketing.com",
                "subject": "Weekly Digest",
                "snippet": "This week's updates...",
                "date": "2025-01-15T07:00:00Z",
                "classification": "fyi-read",
                "urgency_score": 5,
                "signals": ["fyi_indicator"],
                "suggested_action": "Skim and archive",
                "estimated_minutes": 1,
            },
            {
                "id": "msg_8",
                "thread_id": "thread_8",
                "from_addr": "updates@service.com",
                "subject": "Service Update",
                "snippet": "New features...",
                "date": "2025-01-15T06:00:00Z",
                "classification": "fyi-read",
                "urgency_score": 3,
                "signals": ["fyi_indicator"],
                "suggested_action": "Skim and archive",
                "estimated_minutes": 1,
            },
            {
                "id": "msg_9",
                "thread_id": "thread_9",
                "from_addr": "alerts@system.com",
                "subject": "System Notification",
                "snippet": "Automated alert...",
                "date": "2025-01-15T05:00:00Z",
                "classification": "fyi-read",
                "urgency_score": 2,
                "signals": ["fyi_indicator"],
                "suggested_action": "Skim and archive",
                "estimated_minutes": 1,
            },
            {
                "id": "msg_10",
                "thread_id": "thread_10",
                "from_addr": "promo@shop.com",
                "subject": "50% Off Sale!",
                "snippet": "Limited time offer...",
                "date": "2025-01-15T04:00:00Z",
                "classification": "archive",
                "urgency_score": 0,
                "signals": ["fyi_indicator"],
                "suggested_action": "Archive",
                "estimated_minutes": 0,
            },
        ],
    }


class TestGroupByCategory:
    """Tests for email grouping by category."""

    def test_groups_all_categories(self, generator, sample_report):
        """Should create groups for all categories."""
        groups = generator.group_by_category(sample_report["emails"])

        assert "urgent-response" in groups
        assert "response-needed" in groups
        assert "fyi-read" in groups
        assert "delegatable" in groups
        assert "archive" in groups

    def test_correct_group_counts(self, generator, sample_report):
        """Should place emails in correct groups."""
        groups = generator.group_by_category(sample_report["emails"])

        assert len(groups["urgent-response"]) == 2
        assert len(groups["response-needed"]) == 3
        assert len(groups["delegatable"]) == 1
        assert len(groups["fyi-read"]) == 3
        assert len(groups["archive"]) == 1

    def test_unknown_category_goes_to_fyi(self, generator):
        """Unknown categories should go to fyi-read."""
        emails = [{"classification": "unknown-category"}]
        groups = generator.group_by_category(emails)

        assert len(groups["fyi-read"]) == 1


class TestTimeAllocation:
    """Tests for time allocation calculation."""

    def test_calculates_total_minutes(self, generator, sample_report):
        """Should calculate total minutes per category."""
        groups = generator.group_by_category(sample_report["emails"])
        allocation = generator.calculate_time_allocation(groups)

        # Urgent: 15 + 10 = 25 minutes
        assert allocation["urgent-response"]["minutes"] == 25
        assert allocation["urgent-response"]["count"] == 2

        # Response needed: 5 + 10 + 3 = 18 minutes
        assert allocation["response-needed"]["minutes"] == 18
        assert allocation["response-needed"]["count"] == 3


class TestMarkdownGeneration:
    """Tests for markdown action plan generation."""

    def test_generates_header(self, generator, sample_report):
        """Should include header with date and summary."""
        md = generator.generate_markdown(sample_report)

        assert "# Daily Email Action Plan" in md
        assert "Time Budget" in md
        assert "Priority Emails" in md

    def test_includes_urgent_section(self, generator, sample_report):
        """Should include urgent response section."""
        md = generator.generate_markdown(sample_report)

        assert "## Urgent Response" in md
        assert "Q4 Budget Review" in md
        assert "Contract Question" in md

    def test_includes_response_section(self, generator, sample_report):
        """Should include response needed section."""
        md = generator.generate_markdown(sample_report)

        assert "## Response Needed" in md
        assert "Sprint Planning" in md

    def test_includes_delegate_section(self, generator, sample_report):
        """Should include delegate section with targets."""
        md = generator.generate_markdown(sample_report)

        assert "## Delegate" in md
        assert "Invoice #12345" in md
        assert "finance@" in md

    def test_includes_fyi_section(self, generator, sample_report):
        """Should include FYI section."""
        md = generator.generate_markdown(sample_report)

        assert "## FYI / Read Later" in md
        assert "Weekly Digest" in md

    def test_includes_archive_section(self, generator, sample_report):
        """Should include archive section."""
        md = generator.generate_markdown(sample_report)

        assert "## Archive" in md
        assert "50% Off Sale!" in md

    def test_includes_summary_table(self, generator, sample_report):
        """Should include summary statistics table."""
        md = generator.generate_markdown(sample_report)

        assert "## Summary" in md
        assert "| Category | Count |" in md
        assert "| **Total** | **10** |" in md

    def test_time_budget_warning(self, sample_report):
        """Should warn when estimated time exceeds budget."""
        generator = ActionPlanGenerator(time_budget=10)  # Low budget
        md = generator.generate_markdown(sample_report)

        assert "Warning" in md
        assert "exceeds budget" in md


class TestJSONGeneration:
    """Tests for JSON action plan generation."""

    def test_generates_schema_version(self, generator, sample_report):
        """Should include schema version."""
        plan = generator.generate_json(sample_report)

        assert plan["schema_version"] == "1.0"
        assert "generated_at" in plan

    def test_includes_time_budget(self, generator, sample_report):
        """Should include time budget."""
        plan = generator.generate_json(sample_report)

        assert plan["time_budget_minutes"] == 60

    def test_includes_action_plan_structure(self, generator, sample_report):
        """Should include structured action plan."""
        plan = generator.generate_json(sample_report)

        assert "action_plan" in plan
        assert "urgent_response" in plan["action_plan"]
        assert "response_needed" in plan["action_plan"]
        assert "delegate" in plan["action_plan"]
        assert "fyi_count" in plan["action_plan"]
        assert "archive_count" in plan["action_plan"]

    def test_urgent_response_details(self, generator, sample_report):
        """Should include details for urgent emails."""
        plan = generator.generate_json(sample_report)
        urgent = plan["action_plan"]["urgent_response"]

        assert len(urgent) == 2
        assert urgent[0]["id"] == "msg_1"
        assert "Q4 Budget Review" in urgent[0]["subject"]
        assert urgent[0]["minutes"] == 15


class TestEmailLineFormatting:
    """Tests for email line formatting."""

    def test_extracts_sender_name(self, generator):
        """Should extract name from email address."""
        email = {
            "from_addr": "John Doe <john@example.com>",
            "subject": "Test Subject",
            "suggested_action": "Review",
            "estimated_minutes": 5,
        }
        line = generator.format_email_line(email)

        assert "John Doe" in line
        assert "Test Subject" in line

    def test_truncates_long_subjects(self, generator):
        """Should truncate subjects longer than 50 chars."""
        email = {
            "from_addr": "sender@example.com",
            "subject": "This is a very long subject line that should be truncated because it exceeds fifty characters",
            "suggested_action": "Review",
            "estimated_minutes": 5,
        }
        line = generator.format_email_line(email)

        assert "..." in line
        assert len(line) < 200

    def test_includes_time_estimate(self, generator):
        """Should include time estimate when requested."""
        email = {
            "from_addr": "sender@example.com",
            "subject": "Test",
            "suggested_action": "Review",
            "estimated_minutes": 10,
        }
        line = generator.format_email_line(email, include_time=True)
        assert "(10 min)" in line

        line_no_time = generator.format_email_line(email, include_time=False)
        assert "(10 min)" not in line_no_time


class TestFileOutput:
    """Tests for file output."""

    def test_markdown_output(self, generator, sample_report, tmp_path):
        """Should write markdown to file."""
        output_file = tmp_path / "plan.md"
        md = generator.generate_markdown(sample_report)

        with open(output_file, "w") as f:
            f.write(md)

        assert output_file.exists()
        content = output_file.read_text()
        assert "# Daily Email Action Plan" in content

    def test_json_output(self, generator, sample_report, tmp_path):
        """Should write valid JSON to file."""
        output_file = tmp_path / "plan.json"
        plan = generator.generate_json(sample_report)

        with open(output_file, "w") as f:
            json.dump(plan, f, indent=2)

        assert output_file.exists()

        # Verify valid JSON
        with open(output_file, "r") as f:
            loaded = json.load(f)

        assert loaded["schema_version"] == "1.0"
