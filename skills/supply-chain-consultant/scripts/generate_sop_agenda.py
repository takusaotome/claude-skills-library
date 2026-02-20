#!/usr/bin/env python3
"""Generate an S&OP Executive Meeting Agenda in Markdown format.

Usage:
    python3 generate_sop_agenda.py --date 2025-05-05 --next-date 2025-06-02 -o agenda.md
    python3 generate_sop_agenda.py --date 2025-05-05 --topics "Capacity expansion,Product phase-out"

All arguments are optional; defaults produce a generic agenda template.
"""

import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Optional


DEFAULT_ATTENDEES = "CEO, CFO, COO, VP Sales, VP Marketing, VP Supply Chain"
DEFAULT_TIME = "9:00 AM - 11:00 AM"


def generate_agenda(
    date: str,
    next_date: str,
    attendees: str,
    time_range: str,
    topics: Optional[List[str]] = None,
) -> str:
    strategic_section = ""
    if topics:
        topic_lines = "\n".join(f"- {t}" for t in topics)
        strategic_section = f"""## 7. Strategic Topics (15 min)
{topic_lines}
- **Decision Required**: Approve strategic initiatives"""
    else:
        strategic_section = """## 7. Strategic Topics (15 min)
- [Topic 1]
- [Topic 2]
- **Decision Required**: [Specific decision]"""

    return f"""# Executive S&OP Meeting Agenda

**Date**: {date}
**Time**: {time_range}
**Attendees**: {attendees}

---

## 1. Previous Meeting Follow-Up (10 min)
- Review action items from previous S&OP meeting
- Status of ongoing initiatives

## 2. Business Review (15 min)
- Financial performance vs. plan (CFO)
- Market trends and competitive landscape (VP Marketing)
- Key customer feedback (VP Sales)

## 3. Demand Review (20 min)
- Next-quarter demand plan by product family
- Forecast accuracy review (last 3 months)
- Key assumptions and risks
- **Decision Required**: Approve demand plan

## 4. Supply Review (20 min)
- Next-quarter supply plan and capacity utilization
- Supply constraints and bottlenecks
- Inventory plan and targets
- **Decision Required**: Approve supply plan

## 5. Gap Analysis & Trade-Offs (20 min)
- Demand-supply gap analysis
- Scenario analysis and recommendations
- **Decision Required**: Approve resolution plan

## 6. New Product Launch Review (15 min)
- Launch readiness assessment
- Demand ramp-up assumptions
- Supply readiness (materials, capacity, training)
- **Decision Required**: Approve launch date or delay

{strategic_section}

## 8. Wrap-Up (5 min)
- Summary of decisions made
- Action items and owners
- Next meeting: {next_date}

---

**Pre-Read Materials** (distribute 2 days before meeting):
- S&OP Demand Plan
- S&OP Supply Plan
- Gap Analysis & Scenarios
- Financial Summary
"""


def main():
    parser = argparse.ArgumentParser(description="Generate S&OP Meeting Agenda")
    parser.add_argument("--date", default="YYYY-MM-DD", help="Meeting date")
    parser.add_argument("--next-date", default="YYYY-MM-DD", help="Next meeting date")
    parser.add_argument("--attendees", default=DEFAULT_ATTENDEES, help="Attendee list")
    parser.add_argument("--time", default=DEFAULT_TIME, help="Meeting time range")
    parser.add_argument("--topics", help="Comma-separated strategic topics")
    parser.add_argument("-o", "--output", help="Output markdown file (default: stdout)")
    args = parser.parse_args()

    topics = [t.strip() for t in args.topics.split(",")] if args.topics else None
    agenda = generate_agenda(args.date, args.next_date, args.attendees, args.time, topics)

    if args.output:
        Path(args.output).write_text(agenda, encoding="utf-8")
        print(f"Agenda written to {args.output}")
    else:
        print(agenda)


if __name__ == "__main__":
    main()
