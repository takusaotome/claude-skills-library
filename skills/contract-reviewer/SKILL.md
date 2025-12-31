---
name: contract-reviewer
description: Professional contract review skill for business agreements including NDAs, MSAs, SLAs, SOWs, and software license agreements. Provides systematic clause-by-clause analysis, risk assessment with quantified scoring, red flag detection, and negotiation guidance. Use this skill when reviewing vendor contracts, partnership agreements, service agreements, or any business contract requiring risk evaluation and negotiation preparation. Triggers include "review this contract", "analyze this NDA", "check this agreement for risks", "prepare for contract negotiation", or when evaluating terms and conditions.
---

# Contract Reviewer

## Overview

This skill provides a structured methodology for reviewing business contracts from a risk and negotiation perspective. It helps identify unfavorable terms, quantify risks, and prepare negotiation strategies.

**Important Disclaimer**: This skill provides business-focused contract analysis, NOT legal advice. Always consult qualified legal counsel for binding decisions and jurisdiction-specific requirements.

## When to Use This Skill

- Reviewing vendor contracts before signing
- Evaluating NDAs and confidentiality agreements
- Analyzing Master Service Agreements (MSAs)
- Reviewing Service Level Agreements (SLAs)
- Evaluating software license terms
- Preparing for contract negotiations
- Assessing renewal terms and conditions
- Conducting due diligence on partner agreements

## Supported Contract Types

| Type | Abbreviation | Primary Focus |
|------|--------------|---------------|
| Non-Disclosure Agreement | NDA | Confidentiality, information protection |
| Master Service Agreement | MSA | Overall service terms, liability allocation |
| Statement of Work / Service Agreement | SOW | Scope, deliverables, acceptance criteria |
| Service Level Agreement | SLA | Performance metrics, remedies, credits |
| Software License Agreement | License | Usage rights, restrictions, compliance |

## Core Capabilities

1. **Initial Triage**: Quick assessment to determine review depth needed
2. **Clause-by-Clause Analysis**: Systematic review of all contract provisions
3. **Risk Assessment**: Quantified risk scoring with prioritization
4. **Negotiation Preparation**: Identify leverage points and alternative language
5. **Final Report**: Executive summary with actionable recommendations

---

## Workflow 1: Initial Triage

**Purpose**: Quickly assess the contract and determine the appropriate review depth.
**Duration**: 15-30 minutes

### Step 1.1: Contract Classification

Identify the contract type and gather basic information:

```markdown
## Contract Classification

**Contract Type**: [NDA / MSA / SOW / SLA / License / Other: ___]
**Contract Title**:
**Parties**:
  - Party A (typically our organization):
  - Party B (counterparty):
**Effective Date**:
**Term**:
**Value/Amount**: [if applicable]
**Reviewer**:
**Review Date**:
```

### Step 1.2: Quick Red Flag Check

Perform a rapid scan for the following 10 critical red flags. If 3+ flags are triggered, escalate to Deep Review.

| # | Red Flag | Check | Status |
|---|----------|-------|--------|
| 1 | Unlimited liability exposure | Look for missing caps or "unlimited" language | [ ] |
| 2 | One-sided indemnification | Indemnity only flows one direction | [ ] |
| 3 | Automatic renewal with difficult opt-out | Notice periods >60 days, evergreen clauses | [ ] |
| 4 | Unilateral amendment rights | Other party can change terms without consent | [ ] |
| 5 | Problematic governing law | Unfavorable jurisdiction, foreign courts | [ ] |
| 6 | Broad IP assignment | Assigns rights beyond deliverables | [ ] |
| 7 | Missing limitation on consequential damages | No carve-out for indirect damages | [ ] |
| 8 | Excessive termination penalties | Penalties exceed reasonable costs | [ ] |
| 9 | Non-compete or exclusivity restrictions | Limits on business operations | [ ] |
| 10 | Inadequate data protection provisions | GDPR/privacy gaps, data breach handling | [ ] |

**Red Flags Triggered**: ___ / 10

### Step 1.3: Determine Review Depth

Based on the red flag count and contract value/risk:

| Criteria | Quick Review | Standard Review | Deep Review |
|----------|--------------|-----------------|-------------|
| Red flags | 0-1 | 2-3 | 4+ |
| Contract value | <$50K | $50K-$500K | >$500K |
| Strategic importance | Low | Medium | High |
| Renewal/existing | Routine renewal | New vendor | Strategic partnership |

**Selected Review Depth**: [ ] Quick  [ ] Standard  [ ] Deep

---

## Workflow 2: Clause-by-Clause Analysis

**Purpose**: Systematically review all contract provisions using appropriate checklists.
**Duration**: 1-4 hours (varies by contract complexity)

### Step 2.1: Load Reference Materials

Load the following references based on contract type:
- `references/clause_analysis_guide.md` - Clause-specific analysis criteria
- `references/red_flag_patterns.md` - Detailed red flag patterns

### Step 2.2: Core Clause Analysis

Review each clause category systematically. For each clause, assess:
- **Presence**: Is the clause present? Is it complete?
- **Balance**: Are obligations mutual or one-sided?
- **Risk**: What is the potential exposure?
- **Market**: Is this language standard or non-standard?

#### 2.2.1 Fundamental Clauses

| Clause | Key Questions | Notes |
|--------|---------------|-------|
| **Definitions** | Are key terms clearly defined? Any ambiguous terms? | |
| **Scope/Purpose** | Is the scope clearly bounded? Any scope creep risks? | |
| **Term & Renewal** | Auto-renewal? Notice period? Renewal terms? | |
| **Termination** | Termination rights balanced? Termination consequences clear? | |

#### 2.2.2 Risk Allocation Clauses

| Clause | Key Questions | Notes |
|--------|---------------|-------|
| **Limitation of Liability** | Cap amount? Excluded damages? Carve-outs? | |
| **Indemnification** | Mutual or one-sided? Scope of indemnity? Caps? | |
| **Insurance** | Required coverage types? Minimum amounts? Certificate requirements? | |
| **Warranties** | Express vs. implied? Warranty disclaimers? Remedies? | |

#### 2.2.3 Operational Clauses

| Clause | Key Questions | Notes |
|--------|---------------|-------|
| **Payment Terms** | Payment timing? Late fees? Currency? | |
| **Performance/SLA** | Metrics defined? Measurement method? Remedies/credits? | |
| **Acceptance** | Acceptance criteria? Testing period? Deemed acceptance? | |
| **Change Management** | Change process? Pricing for changes? | |

#### 2.2.4 Legal/Compliance Clauses

| Clause | Key Questions | Notes |
|--------|---------------|-------|
| **Confidentiality** | Definition scope? Duration? Return/destruction? | |
| **Data Protection** | GDPR compliance? Data processor terms? Breach notification? | |
| **IP Rights** | Ownership clear? License grants appropriate? Work product rights? | |
| **Governing Law** | Jurisdiction acceptable? Dispute resolution mechanism? | |

#### 2.2.5 Contract Type-Specific Clauses

**For NDAs**: Refer to `clause_analysis_guide.md` Section 5.1
**For MSAs**: Refer to `clause_analysis_guide.md` Section 5.2
**For SOWs**: Refer to `clause_analysis_guide.md` Section 5.3
**For SLAs**: Refer to `clause_analysis_guide.md` Section 5.4
**For License Agreements**: Refer to `clause_analysis_guide.md` Section 5.5

### Step 2.3: Document Findings

For each issue identified, document using this format:

```markdown
### Finding #[ID]: [Brief Title]

**Severity**: [Critical / High / Medium / Low]
**Clause Reference**: Section/Article [X.X]
**Clause Text**: "[Relevant excerpt]"

**Issue**:
[Describe the problem with this clause]

**Risk**:
[Explain the potential business/legal/financial impact]

**Recommendation**:
[Proposed action - accept, negotiate, or reject]

**Alternative Language**:
[If applicable, suggest revised wording]
```

---

## Workflow 3: Risk Assessment

**Purpose**: Quantify and prioritize identified risks.
**Duration**: 30-60 minutes

### Step 3.1: Load Risk Framework

Load `references/risk_assessment_framework.md` for detailed scoring criteria.

### Step 3.2: Score Each Finding

For each finding from Workflow 2, assign scores:

**Likelihood Score (1-5)**:
| Score | Description |
|-------|-------------|
| 1 | Rare - Unlikely to occur |
| 2 | Unlikely - Could occur but not expected |
| 3 | Possible - Might occur |
| 4 | Likely - Expected to occur |
| 5 | Almost Certain - Will occur |

**Impact Score (1-5)**:
| Score | Description |
|-------|-------------|
| 1 | Negligible - Minimal impact |
| 2 | Minor - Some impact, easily managed |
| 3 | Moderate - Noticeable impact |
| 4 | Major - Significant impact |
| 5 | Severe - Critical impact, potential deal-breaker |

**Risk Score** = Likelihood × Impact (range: 1-25)

### Step 3.3: Create Risk Matrix

Map all findings to the risk matrix:

```
                    IMPACT
           1    2    3    4    5
         +----+----+----+----+----+
       5 | M  | H  | H  | C  | C  |
         +----+----+----+----+----+
       4 | M  | M  | H  | H  | C  |
L      +----+----+----+----+----+
I    3 | L  | M  | M  | H  | H  |
K      +----+----+----+----+----+
E    2 | L  | L  | M  | M  | H  |
L      +----+----+----+----+----+
I    1 | L  | L  | L  | M  | M  |
H      +----+----+----+----+----+
O
O       L = Low  M = Medium  H = High  C = Critical
D
```

### Step 3.4: Calculate Overall Risk Score

Aggregate findings into an Overall Contract Risk Score (0-100):

```
Overall Score = Σ(Finding Risk Scores) × Weight Factor / Maximum Possible Score × 100

Weight Factors:
- Critical findings: 3x
- High findings: 2x
- Medium findings: 1x
- Low findings: 0.5x
```

**Interpretation**:
| Score Range | Risk Level | Recommendation |
|-------------|------------|----------------|
| 0-25 | Low | Acceptable with minor negotiation |
| 26-50 | Moderate | Negotiate key terms before signing |
| 51-75 | High | Significant negotiation required; escalate to legal |
| 76-100 | Critical | Do not sign without major revisions; consider alternatives |

### Step 3.5: Risk Summary Table

Create a summary of top 10 risks:

| Rank | Finding ID | Title | L | I | Score | Category |
|------|------------|-------|---|---|-------|----------|
| 1 | | | | | | |
| 2 | | | | | | |
| ... | | | | | | |

---

## Workflow 4: Negotiation Preparation

**Purpose**: Develop negotiation strategy with prioritized requests and alternatives.
**Duration**: 30-60 minutes

### Step 4.1: Load Negotiation Guide

Load `references/negotiation_strategies.md` for alternative clause language library.

### Step 4.2: Categorize Findings for Negotiation

Sort findings into negotiation categories:

#### 4.2.1 Deal Breakers (Must Change)

Issues that would prevent signing if not resolved:

| Finding ID | Issue | Minimum Acceptable Resolution |
|------------|-------|------------------------------|
| | | |

#### 4.2.2 High Priority (Should Change)

Issues with significant risk that should be negotiated:

| Finding ID | Issue | Preferred Resolution | Acceptable Alternative |
|------------|-------|---------------------|----------------------|
| | | | |

#### 4.2.3 Nice to Have (Could Change)

Lower priority items that improve the contract but aren't essential:

| Finding ID | Issue | Requested Change |
|------------|-------|-----------------|
| | | |

#### 4.2.4 Accept As-Is

Standard terms acceptable without modification.

### Step 4.3: Prepare Alternative Language

For each negotiation item, prepare:

1. **Preferred language** - Ideal wording
2. **Alternative language** - Acceptable compromise
3. **Minimum position** - Lowest acceptable terms

Reference `negotiation_strategies.md` for clause-specific alternatives.

### Step 4.4: Identify Leverage Points

Consider these negotiation factors:

- Contract value and strategic importance to counterparty
- Competitive alternatives available
- Urgency of deal for each party
- Precedent from other agreements
- Industry standards and market terms

### Step 4.5: Create Negotiation Summary

```markdown
## Negotiation Summary

**Overall Negotiation Priority**: [High / Medium / Low]

### Must Change (Deal Breakers)
1. [Issue summary] - [Required resolution]

### Should Change (High Priority)
1. [Issue summary] - [Preferred resolution]

### Could Change (Nice to Have)
1. [Issue summary] - [Requested change]

### Key Talking Points
-
-

### Anticipated Pushback
| Our Request | Expected Response | Counter-Strategy |
|-------------|-------------------|------------------|
| | | |
```

---

## Workflow 5: Final Report

**Purpose**: Generate comprehensive review report for decision-makers.
**Duration**: 30 minutes

### Step 5.1: Load Report Template

Load `assets/review_report_template.md` as the output structure.

### Step 5.2: Compile Executive Summary

Create a 1-page executive summary including:

- **Contract Overview**: Type, parties, term, value
- **Overall Assessment**: Risk score, recommendation
- **Key Findings**: Top 3-5 critical issues
- **Recommended Action**: Approve / Conditional Approve / Revise / Reject

### Step 5.3: Populate Detailed Findings

Transfer all findings from Workflow 2 into the report template, organized by severity.

### Step 5.4: Include Risk Assessment

Add the risk matrix and summary table from Workflow 3.

### Step 5.5: Add Negotiation Guidance

Include the negotiation summary and alternative language from Workflow 4.

### Step 5.6: Final Recommendation

Provide a clear recommendation:

| Recommendation | Criteria |
|----------------|----------|
| **Approve** | Overall risk score <25, no Critical/High findings |
| **Conditional Approve** | Risk score 25-50, High findings have acceptable alternatives |
| **Revise & Resubmit** | Risk score 51-75, multiple High findings require changes |
| **Reject** | Risk score >75, deal breakers present, or fundamental misalignment |

### Step 5.7: Next Steps

Define clear next actions:

```markdown
## Next Steps

1. [ ] [Action item with owner and due date]
2. [ ] [Action item with owner and due date]
3. [ ] [Action item with owner and due date]

**Legal Review Required**: [Yes / No]
**Escalation Required**: [Yes / No] - [To whom]
```

---

## Quick Reference: Severity Definitions

| Severity | Definition | Example |
|----------|------------|---------|
| **Critical** | Deal breaker; unacceptable risk | Unlimited liability, IP assignment of all company IP |
| **High** | Significant risk requiring attention | One-sided indemnification, unfavorable jurisdiction |
| **Medium** | Notable issue but manageable | Missing SLA credits, short cure periods |
| **Low** | Minor concern, nice to improve | Non-standard payment terms, minor definitional issues |

---

## Automation Support

Use `scripts/analyze_contract.py` for automated preliminary analysis:

```bash
# Basic analysis
python analyze_contract.py contract.pdf --output report.md

# With contract type specification
python analyze_contract.py contract.pdf --type nda --output nda_review.md

# Full analysis with all options
python analyze_contract.py contract.pdf \
  --type msa \
  --party-name "Our Company Inc." \
  --output detailed_review.md \
  --verbose
```

The script performs:
- Contract type auto-detection
- Key clause extraction
- Red flag pattern matching
- Preliminary risk scoring
- Markdown report generation

**Note**: Automated analysis is a starting point. Always perform manual review using the full workflow for final assessment.

---

## Related Resources

- `references/clause_analysis_guide.md` - Detailed clause analysis criteria
- `references/red_flag_patterns.md` - Comprehensive red flag catalog
- `references/risk_assessment_framework.md` - Risk scoring methodology
- `references/contract_review_methodology.md` - Process deep dive
- `references/negotiation_strategies.md` - Alternative clause library
- `assets/review_report_template.md` - Report output template
- `assets/clause_checklist.md` - Interactive review checklist
