---
name: qa-bug-analyzer
description: This skill should be used when analyzing bug ticket data to identify quality trends, assess software quality status, and provide improvement recommendations. Use when a user provides bug lists (CSV, Excel, JSON, or Markdown format) and needs comprehensive quality analysis from a QA manager perspective. Generates statistical analysis, identifies quality hotspots, provides actionable recommendations, and produces professional Markdown reports suitable for project managers and executive leadership. Ideal for IT system development, migration, and implementation projects.
---

# QA Bug Analyzer

## Overview

This skill enables comprehensive bug ticket analysis from a QA management perspective. Analyze bug data to identify quality trends, assess project health, pinpoint problem areas, and generate actionable improvement recommendations. The skill produces professional Markdown reports suitable for project managers, development managers, and executive leadership.

**Key capabilities:**
- Statistical analysis of bug distributions (severity, category, module, resolution time)
- Quality trend identification and hotspot detection
- Root cause pattern analysis
- Prioritized improvement recommendations
- Professional report generation for stakeholders

## When to Use This Skill

Use this skill when:

1. **User provides bug ticket data** in CSV, Excel, JSON, or Markdown format
2. **Quality assessment is needed** for project reviews, milestone gates, or release readiness
3. **Trend analysis is requested** to understand quality patterns over time
4. **Stakeholder reporting is required** for project managers or executive leadership
5. **Improvement recommendations are needed** based on objective data analysis
6. **User mentions:**
   - "Analyze bug trends"
   - "Quality report for management"
   - "Which modules have the most bugs?"
   - "How long does it take to fix bugs?"
   - "What areas should we focus on?"
   - "Generate quality analysis report"

**Example scenarios:**
- "I have a CSV file with 200 bug tickets. Can you analyze the quality trends?"
- "Generate a quality report for our project manager based on these bugs"
- "Analyze this bug data and tell me what areas need improvement"
- "Create an executive summary of our bug situation"

## Workflow Decision Tree

Follow this decision tree to determine the appropriate workflow:

```
User provides bug data
    │
    ├─→ Data in CSV/JSON format
    │   └─→ Use Automated Analysis Workflow (Section 3)
    │
    ├─→ Data in multiple Markdown files (from bug-ticket-creator)
    │   └─→ Use Markdown Aggregation Workflow (Section 4)
    │
    └─→ User wants custom analysis or specific focus
        └─→ Use Custom Analysis Workflow (Section 5)
```

After analysis, always:
1. Review quality_metrics_guide.md for metric interpretation
2. Review analysis_methodology.md for analysis best practices
3. Generate comprehensive Markdown report using report_template.md

## Core Workflows

### Workflow 1: Quick Analysis (CSV/JSON Input)

**When to use:** User provides a single CSV or JSON file with bug data

**Steps:**

1. **Receive and validate data**
   - Confirm file format (CSV or JSON)
   - Check for required fields (at minimum: ID, title, status, severity)
   - Note any data quality issues

2. **Run analysis script**
   ```bash
   python3 scripts/analyze_bugs.py <input_file> --output analysis_results.json
   ```

   The script will:
   - Load and normalize bug data
   - Calculate severity distribution
   - Analyze module/component distribution
   - Compute resolution time metrics
   - Identify status distribution
   - Detect quality issues
   - Generate recommendations

3. **Review analysis results**
   - Load the JSON output
   - Read `references/quality_metrics_guide.md` for metric interpretation guidelines
   - Identify key findings and issues

4. **Generate professional report**
   - Use `assets/report_template.md` as the structure
   - Populate all sections with analysis results
   - Include visualizations (text-based tables and charts)
   - Add context-specific insights
   - Tailor recommendations to project phase and stakeholder needs

5. **Deliver report to user**
   - Create new Markdown file with completed report
   - Provide executive summary
   - Highlight top 3-5 recommendations
   - Suggest next steps

**Expected output:** Comprehensive Markdown report with:
- Executive summary (1 page)
- Quantitative metrics with visualizations
- Quality issues identified
- Prioritized recommendations
- Action items

### Workflow 2: Comprehensive Analysis (Markdown Bug Tickets)

**When to use:** User has multiple Markdown bug tickets (e.g., from bug-ticket-creator skill)

**Steps:**

1. **Aggregate bug data**
   - Use Glob to find all bug ticket Markdown files
   - Read each file to extract structured data
   - Parse key fields:
     - Bug ID / Title
     - Severity / Priority
     - Status
     - Category / Type
     - Module / Component
     - Created Date
     - Resolved Date
     - Description (for root cause insights)

2. **Convert to analysis format**
   - Create CSV or JSON structure from parsed data
   - Normalize field values (severity levels, status values)
   - Handle missing or inconsistent data

3. **Run analysis**
   - Follow steps 2-5 from Workflow 1
   - Pay special attention to rich descriptions for root cause analysis

**Expected output:** Same as Workflow 1, with enhanced root cause insights

### Workflow 3: Custom Analysis Focus

**When to use:** User requests specific analysis dimensions or has particular concerns

**Steps:**

1. **Clarify analysis objectives**
   - Use AskUserQuestion to understand specific needs:
     - Which metrics are most important?
     - Are there specific modules/teams to focus on?
     - What time period should be analyzed?
     - Who is the report audience?

2. **Load relevant references**
   - Read `references/quality_metrics_guide.md` for applicable metrics
   - Read `references/analysis_methodology.md` for analysis approach
   - Understand benchmarks and thresholds

3. **Perform targeted analysis**
   - Run automated analysis (if CSV/JSON available)
   - Supplement with manual deep-dive analysis
   - Focus on user-specified areas

4. **Generate customized report**
   - Adapt report_template.md structure
   - Emphasize relevant sections
   - Add custom visualizations or analysis
   - Tailor language and detail level to audience

**Example custom analyses:**
- Module-specific deep dive
- Time-based trend analysis
- Severity-focused assessment
- Team performance comparison
- Release readiness evaluation

### Workflow 4: Iterative Analysis Refinement

**When to use:** User wants to refine or expand initial analysis

**Steps:**

1. **Review initial findings**
   - Recap previous analysis results
   - Identify areas needing deeper investigation

2. **Conduct additional analysis**
   - Drill down into specific modules or categories
   - Perform correlation analysis
   - Calculate additional metrics
   - Investigate outliers or anomalies

3. **Update report**
   - Add new sections or insights
   - Refine recommendations
   - Include comparative analysis

4. **Validate with user**
   - Confirm analysis addresses concerns
   - Gather feedback on recommendations

## Analysis Best Practices

### Data Quality Considerations

**Always check for and handle:**
- Missing dates (created, resolved)
- Inconsistent severity labels
- Empty module/component fields
- Unclear status values

**Data normalization guidelines:**

Severity mapping:
```
Critical, Blocker, P0, Severity 1 → Critical
High, Major, P1, Severity 2 → High
Medium, Normal, P2, Severity 3 → Medium
Low, Minor, P3, Severity 4 → Low
```

Status mapping:
```
Open, New, Submitted → Open
In Progress, Assigned, Working → In Progress
Resolved, Fixed, Completed → Resolved
Closed, Verified → Closed
```

### Metric Interpretation Guidelines

Refer to `references/quality_metrics_guide.md` for detailed guidance. Key thresholds:

**Severity Distribution (Healthy):**
- Critical: 5-10%
- High: 15-20%
- Medium: 40-50%
- Low: 20-30%

**Resolution Time Targets:**
- Critical: <2 days
- High: <5 days
- Medium: <14 days
- Low: <30 days

**Quality Status (RAG):**
- 🟢 Green: Closure rate >80%, avg resolution <14 days, <10% Critical+High
- 🟡 Yellow: Closure rate 60-80%, avg resolution 14-21 days, 10-25% Critical+High
- 🔴 Red: Closure rate <60%, avg resolution >21 days, >25% Critical+High

### Recommendation Formulation

**Effective recommendations include:**

1. **Context:** What is the problem?
2. **Evidence:** What data supports this?
3. **Recommendation:** What specific action to take?
4. **Expected Impact:** What will improve?
5. **Implementation Guidance:** How to execute?
6. **Success Metrics:** How to measure effectiveness?

**Prioritization framework:**

- **High Priority:** Addresses Critical/High severity issues, high impact, quick wins
- **Medium Priority:** Addresses moderate issues, requires coordination/resources
- **Low Priority:** Nice-to-have improvements, preventive measures

### Report Tailoring by Audience

**For Executive Leadership:**
- Focus on business impact and ROI
- High-level metrics and trends
- Risk assessment and mitigation
- Resource needs

**For Project Managers:**
- Schedule impact and milestone risks
- Resource allocation needs
- Action item tracking
- Team performance

**For Development Managers:**
- Module-specific details
- Technical root causes
- Code quality metrics
- Tooling recommendations

**For QA Managers:**
- Test coverage gaps
- Process improvements
- Testing strategy
- Skill development needs

## Resources

### scripts/analyze_bugs.py

Python script for automated bug data analysis. Performs comprehensive statistical analysis and generates structured JSON output.

**Usage:**
```bash
python3 scripts/analyze_bugs.py <input_file> [--output results.json] [--format csv|json|auto]
```

**Capabilities:**
- Loads CSV or JSON bug data
- Calculates severity, category, module distributions
- Computes resolution time metrics (avg, median, percentiles)
- Analyzes status distribution and closure rates
- Identifies quality issues automatically
- Generates prioritized recommendations
- Exports results as JSON

**Expected input fields** (flexible field names):
- Bug ID
- Title/Summary
- Status
- Severity/Priority
- Module/Component (optional but recommended)
- Category/Type (optional but recommended)
- Created Date (optional, for resolution time analysis)
- Resolved Date (optional, for resolution time analysis)

**Output structure:**
```json
{
  "metadata": {
    "total_bugs": 150,
    "analysis_date": "2025-01-15 10:30:00"
  },
  "severity_distribution": { ... },
  "module_distribution": { ... },
  "resolution_time": { ... },
  "quality_issues": [ ... ],
  "recommendations": [ ... ]
}
```

### references/quality_metrics_guide.md

Comprehensive guide to quality metrics for bug analysis. Load this when interpreting analysis results or explaining metrics to users.

**Key sections:**
- Defect density metrics and benchmarks
- Severity distribution guidelines
- Resolution time (MTTR) targets and SLAs
- Bug closure rate interpretation
- Defect escape rate calculations
- Quality gates and thresholds (Red/Yellow/Green)
- Reporting best practices

**When to read:**
- Before generating report to understand metric interpretation
- When user asks about metric meaning or benchmarks
- When setting quality gates or thresholds
- When explaining findings to stakeholders

### references/analysis_methodology.md

Detailed methodology for conducting bug analysis. Load this when performing complex or custom analysis.

**Key sections:**
- Phase 1: Data preparation and validation
- Phase 2: Quantitative analysis techniques
- Phase 3: Pattern recognition and root cause analysis
- Phase 4: Quality issue identification
- Phase 5: Recommendation development
- Phase 6: Report generation

**When to read:**
- When performing custom or in-depth analysis
- When user requests specific analysis approach
- When troubleshooting data quality issues
- When formulating complex recommendations

### assets/report_template.md

Professional Markdown report template for bug analysis reports. Use this as the structure for all final reports.

**Key sections:**
- Executive Summary (with RAG status)
- Analysis Overview
- Quantitative Metrics (severity, module, category, resolution time, status)
- Quality Issues Identified
- Trend Analysis
- Recommendations (High/Medium/Low priority)
- Quality Metrics Dashboard
- Root Cause Analysis Summary
- Comparison and Benchmarking
- Action Items Summary
- Conclusion

**Customization guidance:**
- Replace all [PLACEHOLDER] values with actual data
- Remove sections not applicable to analysis
- Add custom sections as needed
- Include visualizations (text-based tables, charts)
- Tailor language and detail to audience

**Output format:**
- Save as new Markdown file with descriptive name (e.g., `bug_analysis_report_2025_Q1.md`)
- Use clear section headers and formatting
- Include tables for structured data
- Use bullet points for lists
- Add emphasis (bold/italic) for key points

## Tips for Effective Analysis

1. **Start with data validation:** Check data quality before analysis to avoid misleading conclusions

2. **Provide context:** Always compare metrics to benchmarks, targets, or historical trends

3. **Be objective:** Focus on data-driven insights, avoid bias or assumptions

4. **Link to impact:** Connect findings to business/project impact for stakeholder relevance

5. **Prioritize recommendations:** Not all issues are equal - focus on high-impact actions

6. **Make recommendations actionable:** Provide specific steps, not vague suggestions

7. **Visualize effectively:** Use tables, charts, and formatting to enhance clarity

8. **Tailor to audience:** Adjust detail level and focus based on who will read the report

9. **Follow up:** Track previous recommendations and measure their effectiveness

10. **Continuous improvement:** Refine analysis approach based on feedback and results

## Example Usage

### Example 1: Quick CSV Analysis

**User:** "Here's a CSV file with our bug data from the last sprint. Can you analyze it and tell me what we should focus on?"

**Claude response:**
1. Load and validate the CSV file
2. Run `scripts/analyze_bugs.py bugs_sprint_10.csv --output analysis.json`
3. Review analysis results, noting:
   - 35% of bugs are in the Authentication module (hotspot)
   - Average resolution time is 18 days (above target)
   - 28% of bugs are Critical/High severity
4. Read `references/quality_metrics_guide.md` for threshold interpretation
5. Generate report using `assets/report_template.md`
6. Deliver report to user highlighting:
   - **Top finding:** Authentication module quality hotspot
   - **Key metric:** Resolution time 29% above target
   - **Top recommendation:** Conduct focused code review of Authentication module

### Example 2: Executive Report Generation

**User:** "I need to present our quality status to the VP of Engineering. Can you create an executive summary from this bug data?"

**Claude response:**
1. Perform comprehensive analysis
2. Calculate overall quality health score (RAG status)
3. Identify top 3-5 findings with business impact
4. Read `references/quality_metrics_guide.md` for benchmarking
5. Generate executive-focused report:
   - 1-page executive summary
   - RAG status with clear indicators
   - Business impact of quality issues
   - High-level recommendations
   - Risk assessment
6. Use concise language, focus on outcomes, include comparisons to benchmarks

### Example 3: Module Deep Dive

**User:** "The Payment module has a lot of bugs. Can you do a deep analysis of just that module?"

**Claude response:**
1. Filter bug data to Payment module only
2. Perform targeted analysis:
   - Severity distribution within Payment module
   - Resolution time for Payment bugs
   - Category breakdown (UI, logic, integration, etc.)
   - Trend over time if historical data available
3. Compare Payment module metrics to overall averages
4. Read `references/analysis_methodology.md` for root cause analysis techniques
5. Investigate:
   - Code complexity indicators
   - Recent changes or features
   - Test coverage
   - Team expertise
6. Generate focused report with module-specific recommendations:
   - Code review of complex areas
   - Increase unit test coverage
   - Refactoring considerations
   - Additional QA resources

## Quality Assurance

When using this skill, always:

✓ Validate data quality and note limitations
✓ Provide objective, evidence-based analysis
✓ Include context (benchmarks, trends, comparisons)
✓ Make recommendations specific and actionable
✓ Tailor report to intended audience
✓ Use professional, clear language
✓ Include success metrics for recommendations
✓ Focus on improvement, not blame

✗ Don't cherry-pick data to support preconceived notions
✗ Don't present metrics without interpretation
✗ Don't make recommendations without supporting evidence
✗ Don't use overly technical jargon for non-technical audiences
✗ Don't ignore data quality issues
✗ Don't present analysis without actionable next steps

---

*This skill follows industry standards from ISTQB, ISO/IEC 25010, and IEEE 982.1 for software quality measurement and analysis.*
