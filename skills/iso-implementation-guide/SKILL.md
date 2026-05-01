---
name: iso-implementation-guide
description: |
  ISO規格（ISO 9001品質、ISO 27001情報セキュリティ、ISO 22301事業継続等）の認証取得支援スキル。
  ギャップ分析、文書化支援、内部監査、認証準備を提供。
  Use when pursuing ISO certification, conducting gap analysis, or implementing ISO-compliant management systems.
  Triggers: "ISO 9001", "ISO 27001", "ISO 22301", "ISO certification", "quality management", "ISMS", "gap analysis".
---

# ISO Implementation Guide（ISO認証取得支援）

## Overview

This skill provides expert guidance for implementing ISO management system standards and achieving certification. Supports ISO 9001 (Quality), ISO 27001 (Information Security), ISO 22301 (Business Continuity), and other ISO standards.

**Primary language**: Japanese (default), English supported
**Supported Standards**: ISO 9001, ISO 27001, ISO 22301, ISO 45001, ISO 14001
**Output format**: Gap analysis reports, implementation roadmaps, document templates, audit checklists

---

## When to Use

Use this skill when:
- **Planning ISO certification**: Organization is pursuing ISO 9001, 27001, 22301, or other certification
- **Conducting gap analysis**: Need to assess current state vs. ISO requirements
- **Developing documentation**: Creating policies, procedures, and work instructions
- **Preparing for audits**: Getting ready for Stage 1/Stage 2 certification audits
- **Implementing management systems**: Building quality, security, or continuity systems
- **Integrating multiple standards**: Combining ISO 9001 + 27001 + 22301 using HLS

**Triggers**: "ISO 9001", "ISO 27001", "ISO 22301", "ISO certification", "quality management", "ISMS", "BCMS", "gap analysis", "internal audit", "certification audit"

---

## Prerequisites

1. **Python 3.9+** for running automation scripts
2. **Access to target ISO standard** (official document recommended)
3. **Stakeholder access** for interviews during gap analysis
4. **Existing documentation** (policies, procedures, records) for assessment

---

## Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    ISO Implementation                        │
├─────────────────────────────────────────────────────────────┤
│  1. Gap Analysis    →  Assess current state vs requirements │
│  2. Roadmap         →  Plan phased implementation          │
│  3. Documentation   →  Create policies, procedures         │
│  4. Internal Audit  →  Verify compliance internally        │
│  5. Certification   →  Stage 1 + Stage 2 external audit    │
└─────────────────────────────────────────────────────────────┘
```

**Typical Timeline**: 6-18 months depending on starting maturity

---

## Output

This skill generates:

| Output | Description | Format |
|--------|-------------|--------|
| Gap Analysis Report | Clause-by-clause compliance assessment | Markdown/CSV |
| Implementation Roadmap | Phased plan with milestones | Markdown/Mermaid |
| Maturity Score | 0-5 score per clause, overall average | Numeric |
| Action Plan | Prioritized gaps with owners and effort | Table |
| Internal Audit Checklist | Clause-specific audit questions | Markdown |
| Document Templates | Policy, procedure, record templates | Markdown |

---

## Resources

### Reference Documents
- `references/iso-hls-structure.md` - ISO High-Level Structure (Annex SL) guide
- `references/gap-analysis-methodology.md` - Systematic gap analysis process

### Automation Scripts
- `scripts/gap_analysis.py` - Generate templates and reports from CSV input

### Usage Examples

```bash
# Generate blank gap analysis template for ISO 27001
python3 scripts/gap_analysis.py template --standard ISO_27001 --output gap_template.csv

# Fill in the template with assessment scores, then generate report
python3 scripts/gap_analysis.py report \
  --input completed_assessment.csv \
  --standard ISO_27001 \
  --organization "ACME Corp" \
  --assessor "John Smith" \
  --scope "IT Department" \
  --output gap_report.md

# Generate JSON output for integration
python3 scripts/gap_analysis.py report \
  --input assessment.csv \
  --format json \
  --output report.json
```

---

## Supported ISO Standards

### 1. ISO 9001:2015 - Quality Management System (QMS)

**Purpose**: Ensure consistent quality of products and services

**Key Requirements**:
- Context of the organization
- Leadership commitment
- Risk-based thinking
- Process approach
- Customer focus
- Continual improvement

**Benefits**:
- Improved customer satisfaction
- Consistent quality
- Operational efficiency
- Competitive advantage

### 2. ISO 27001:2022 - Information Security Management System (ISMS)

**Purpose**: Protect information assets through systematic risk management

**Key Requirements**:
- Information security policy
- Risk assessment and treatment
- 93 controls (Annex A)
- Security awareness training
- Incident management

**Benefits**:
- Enhanced information security
- Regulatory compliance
- Customer trust
- Reduced security incidents

### 3. ISO 22301:2019 - Business Continuity Management System (BCMS)

**Purpose**: Ensure business continuity during disruptions

**Key Requirements**:
- Business impact analysis (BIA)
- Risk assessment
- Business continuity strategies
- Testing and exercises
- Continual improvement

**Benefits**:
- Organizational resilience
- Faster recovery from disruptions
- Stakeholder confidence

### 4. ISO 45001:2018 - Occupational Health and Safety (OH&S)

**Purpose**: Improve employee safety and reduce workplace risks

**Key Requirements**:
- Hazard identification
- Risk assessment
- Worker participation
- Incident investigation
- Emergency preparedness

### 5. ISO 14001:2015 - Environmental Management System (EMS)

**Purpose**: Minimize environmental impact

**Key Requirements**:
- Environmental aspects and impacts
- Legal compliance
- Environmental objectives
- Pollution prevention
- Continual improvement

---

## Core Workflows

### Workflow 1: Gap Analysis

**Purpose**: Assess current state vs. ISO requirements and identify gaps.

#### Step 1: Document Review
- Collect existing policies, procedures, records
- Review organizational structure and processes
- Understand current practices

#### Step 2: Requirement Mapping
Create a checklist of all ISO requirements and assess compliance:

**Example (ISO 9001 Clause 4.1 - Understanding the Organization)**:
```
Requirement: The organization shall determine external and internal issues relevant to its purpose.

Current State:
- No formal process for identifying issues
- Ad-hoc discussion in management meetings
- No documentation

Gap: HIGH
Action Required:
1. Establish process for identifying internal/external issues
2. Document issues in context analysis
3. Review quarterly
```

#### Step 3: Gap Scoring
```
Compliance Level:
5 - Fully compliant (evidence available)
4 - Mostly compliant (minor gaps)
3 - Partially compliant (significant gaps)
2 - Minimally compliant (major gaps)
1 - Not compliant (no evidence)
0 - Not applicable

Overall Maturity = Average of all applicable clauses
```

#### Step 4: Prioritize Gaps
**Priority Matrix**:
```
       High Risk
         │
  High  │  High
Priority│Priority
         │
  ───────┼───────
         │
  Medium│  Low
Priority│Priority
         │
      Low Compliance
```

**Output**: Gap Analysis Report with prioritized action plan

### Workflow 2: Implementation Roadmap

**Purpose**: Create phased implementation plan.

#### Phase 1: Foundation (Months 1-3)
- **Management Commitment**: Executive buy-in, policy approval
- **Scope Definition**: What will be certified?
- **Team Formation**: Implementation team, roles
- **Gap Analysis**: Detailed assessment
- **Quick Wins**: Easy improvements

#### Phase 2: Documentation (Months 4-6)
- **Policy Manual**: Top-level policies
- **Procedures**: Detailed procedures
- **Work Instructions**: Step-by-step guides
- **Forms and Templates**: Standardized records
- **Document Control**: Version control system

#### Phase 3: Implementation (Months 7-9)
- **Training**: Awareness and role-specific training
- **Process Rollout**: Implement new processes
- **Record Keeping**: Start collecting evidence
- **Internal Communication**: Regular updates

#### Phase 4: Internal Audit (Month 10)
- **Internal Audit Planning**: Audit schedule and scope
- **Audit Execution**: Conduct audits
- **Nonconformity Management**: Identify and correct issues
- **Management Review**: Present to leadership

#### Phase 5: Certification (Months 11-12)
- **Pre-Assessment** (Optional): Mock audit
- **Stage 1 Audit**: Documentation review
- **Stage 2 Audit**: On-site verification
- **Certification**: Receive certificate (valid 3 years)

### Workflow 3: Document Hierarchy

**Purpose**: Create compliant documentation structure.

#### Documentation Levels:

**Level 1: Policy Manual**
- Strategic direction
- Management commitment
- Scope and objectives
- Audience: All employees

**Level 2: Procedures**
- What, who, when, where
- Process flows
- Responsibilities (RACI)
- Audience: Process owners, managers

**Level 3: Work Instructions**
- Step-by-step "how-to"
- Screenshots, checklists
- Audience: Operators, end users

**Level 4: Forms and Records**
- Templates for data collection
- Evidence of compliance
- Audience: All users

#### Document Control Requirements:
- Unique document ID
- Version control
- Approval workflow
- Review schedule
- Distribution control
- Obsolete document management

### Workflow 4: Internal Audit Program

**Purpose**: Verify compliance and identify improvements.

#### Step 1: Audit Planning
**Annual Audit Schedule**:
```
| Month | Scope | Lead Auditor | Auditee |
|-------|-------|--------------|---------|
| Jan | Clauses 4-6 | A. Tanaka | Management |
| Apr | Clauses 7-8 | B. Sato | Operations |
| Jul | Clause 9 | C. Suzuki | Quality Dept |
| Oct | Clause 10 | A. Tanaka | All Depts |
```

#### Step 2: Auditor Competence
- **Training**: ISO 19011 (Auditing Guidelines)
- **Independence**: Auditors shall not audit their own work
- **Skills**: Communication, analysis, objectivity

#### Step 3: Audit Execution
**Audit Process**:
1. Opening meeting
2. Document review
3. Interviews and observations
4. Evidence collection
5. Findings documentation
6. Closing meeting

**Finding Types**:
- **Major Nonconformity**: Significant failure, affects certification
- **Minor Nonconformity**: Isolated lapse, requires correction
- **Observation**: Opportunity for improvement

#### Step 4: Corrective Action
**8D Problem Solving**:
1. Form team
2. Describe problem
3. Implement containment
4. Identify root cause (5 Whys, Fishbone)
5. Develop corrective actions
6. Implement and verify
7. Prevent recurrence
8. Recognize team

### Workflow 5: Certification Audit Preparation

**Purpose**: Prepare for external certification audit.

#### Stage 1 Audit (Documentation Review)
**What auditors check**:
- Management system documentation complete?
- Scope appropriate?
- Internal audits conducted?
- Management review completed?
- Ready for Stage 2?

**Preparation**:
- Ensure all documents approved and current
- Prepare document index
- Schedule Stage 2 audit

#### Stage 2 Audit (On-Site Verification)
**What auditors check**:
- Processes implemented as documented?
- Records demonstrate compliance?
- Employees aware of policies?
- Continual improvement evidence?

**Preparation**:
- Mock audit (optional but recommended)
- Train employees on what to expect
- Prepare evidence (records, logs)
- Assign escorts for auditors
- Book meeting rooms

**Common Audit Questions**:
- "Show me your quality policy. Where is it displayed?"
- "Walk me through your incident response process."
- "How do you identify risks?"
- "Show me records from last month's management review."

---

## Deliverable Templates

### 1. Gap Analysis Report

```markdown
# ISO [Standard] Gap Analysis Report

## Executive Summary
- Current maturity score: X.X/5.0
- Major gaps: [Count]
- Estimated effort: [Months]
- Certification target: [Date]

## Clause-by-Clause Assessment

### Clause 4: Context of the Organization
**4.1 Understanding the organization and its context**
- Compliance: 2/5 (Minimally compliant)
- Gap: No formal process for identifying internal/external issues
- Evidence: None
- Action: Develop context analysis procedure
- Priority: High
- Effort: 2 weeks

[Repeat for all clauses]

## Summary by Compliance Level
- Fully Compliant (5): X clauses
- Mostly Compliant (4): X clauses
- Partially Compliant (3): X clauses
- Minimally Compliant (2): X clauses
- Not Compliant (1): X clauses

## Prioritized Action Plan
[List of high-priority actions with owners and deadlines]

## Recommendations
[Strategic recommendations for achieving certification]
```

### 2. Implementation Roadmap

```markdown
# ISO [Standard] Implementation Roadmap

## Project Charter
- Objective: Achieve ISO [Standard] certification
- Scope: [Organizational units, locations]
- Timeline: 12 months
- Budget: [Amount]
- Sponsor: [Executive Name]

## Phase Plan

### Phase 1: Foundation (Months 1-3)
**Milestones**:
- ✅ Management kick-off meeting
- ✅ Gap analysis completed
- ✅ Implementation team formed
- 🔄 Scope document approved

**Deliverables**:
- Gap analysis report
- Scope statement
- Project plan

[Repeat for all phases]

## Gantt Chart
[Mermaid or table format]

## Resource Plan
- Project Manager: 50% FTE
- Quality Manager: 25% FTE
- Internal Auditors: 3 persons (trained)
- Consultant: 10 days (optional)

## Budget
- Training: $X
- Consultant (optional): $X
- Certification audit: $X
- Tools/Software: $X
- Total: $X
```

### 3. Internal Audit Checklist

```markdown
# Internal Audit Checklist: ISO [Standard]

## Audit Information
- Date: [Date]
- Auditor: [Name]
- Auditee: [Department]
- Scope: Clauses [X-Y]

## Clause 4: Context of the Organization

### 4.1 Understanding the organization and its context
- [ ] Does the organization have a documented understanding of external issues?
- [ ] Does the organization have a documented understanding of internal issues?
- [ ] Are these issues reviewed periodically?
- [ ] Evidence reviewed: [Context analysis document, management review minutes]
- [ ] Finding: [NC/OBS/None]
- [ ] Notes: [Details]

[Repeat for all requirements]

## Summary
- Nonconformities (Major): X
- Nonconformities (Minor): X
- Observations: X
- Strengths: [List]

## Signature
- Auditor: [Name, Date]
- Auditee: [Name, Date]
```

---

## Best Practices

### 1. Management Commitment is Critical
ISO certification requires visible, active support from top management.

### 2. Keep Documentation Simple
Don't over-document. "Say what you do, do what you say."

### 3. Integrate with Existing Processes
Don't create parallel processes. Build ISO into daily work.

### 4. Train Everyone
Awareness training for all, detailed training for process owners.

### 5. Use Templates and Tools
Leverage templates to accelerate documentation.

### 6. Conduct Mock Audits
Practice before the real certification audit.

### 7. Focus on Continual Improvement
ISO is not just certification—it's about ongoing improvement.

### 8. Maintain After Certification
Annual surveillance audits require ongoing compliance.

---

## Common Pitfalls

### ❌ Documentation Overload
Creating excessive documentation that nobody uses.
**Solution**: Minimum necessary documentation.

### ❌ Lack of Management Involvement
Treating ISO as "Quality Department's project."
**Solution**: Engage executives from day one.

### ❌ Certification as the Goal
Viewing certification as the end, not the means.
**Solution**: Focus on benefits, not just the certificate.

### ❌ Insufficient Training
Employees don't understand their role.
**Solution**: Comprehensive training program.

### ❌ Poor Record Keeping
No evidence to show during audits.
**Solution**: Systematic record keeping from day one.

---

このスキルの目的は、組織がISO規格に準拠し、認証を取得し、継続的に改善することを支援することです。適切な計画、実装、監査を通じて、ISO認証を成功裏に達成してください。
