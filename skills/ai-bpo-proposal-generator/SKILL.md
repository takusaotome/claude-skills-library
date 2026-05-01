---
name: ai-bpo-proposal-generator
description: Generate AI-powered BPO service proposals for Japanese companies in the US market. Use when creating outsourcing proposals with AI service menus, ROI estimation, implementation roadmaps, and bilingual (JA/EN) proposal documents for 在米日系企業向けAI実装.
---

# AI-Powered BPO Proposal Generator

## Overview

Generate comprehensive BPO (Business Process Outsourcing) service proposals tailored for Japanese companies operating in the US market. This skill creates professional proposals that combine AI-powered service offerings with traditional BPO services, including ROI analysis, implementation roadmaps, and bilingual documentation. The output targets "在米日系企業向けAI実装" market positioning.

## When to Use

- Creating BPO service proposals for Japanese subsidiaries in the US
- Developing AI-enhanced outsourcing offerings for traditional business processes
- Estimating ROI for AI implementation in back-office operations
- Building implementation roadmaps for phased AI adoption
- Generating bilingual (Japanese/English) proposal documents
- Positioning AI services for the 在米日系企業 market segment

## Prerequisites

- Python 3.9+
- No API keys required (calculations are local)
- Dependencies: pandas, jinja2 (for template rendering)

## Workflow

### Step 1: Gather Client Requirements

Collect client information using the intake questionnaire:

1. Company profile (industry, size, US operation scale)
2. Current pain points (manual processes, error rates, processing volumes)
3. Budget range and timeline expectations
4. Language requirements (primary communication language)
5. Compliance requirements (SOX, J-SOX, data residency)

Reference the client intake template:
```bash
cat references/client-intake-template.md
```

### Step 2: Select Applicable Service Modules

Review the AI-BPO service catalog and select relevant modules:

```bash
python3 scripts/select_services.py \
  --industry "manufacturing" \
  --pain-points "invoice_processing,expense_reporting" \
  --output proposal_services.json
```

Service categories include:
- **Finance & Accounting**: AP/AR automation, expense management, reconciliation
- **HR & Payroll**: Onboarding, time tracking, benefits administration
- **Customer Support**: Ticket routing, FAQ automation, sentiment analysis
- **Data Processing**: Document digitization, data entry, validation
- **Procurement**: Vendor management, PO processing, contract analysis

### Step 3: Calculate ROI Estimation

Generate ROI projections based on selected services and client volumes:

```bash
python3 scripts/calculate_roi.py \
  --services proposal_services.json \
  --volumes '{"invoices_per_month": 5000, "employees": 200}' \
  --output roi_analysis.json
```

The ROI calculation includes:
- Current state cost analysis (FTE, error rates, processing time)
- Future state projections (automation rates, accuracy improvements)
- Implementation costs (setup, training, integration)
- Payback period and 3-year NPV

### Step 4: Generate Implementation Roadmap

Create a phased implementation plan:

```bash
python3 scripts/generate_roadmap.py \
  --services proposal_services.json \
  --start-date "2025-04-01" \
  --output roadmap.json
```

Standard phases:
1. **Discovery & Assessment** (2-4 weeks): Process mapping, data audit
2. **Pilot Implementation** (4-6 weeks): Single process, limited scope
3. **Phased Rollout** (8-12 weeks): Expand to additional processes
4. **Optimization** (Ongoing): Model tuning, process refinement

### Step 5: Generate Proposal Document

Create the final bilingual proposal document:

```bash
python3 scripts/generate_proposal.py \
  --client-name "ABC Corporation" \
  --services proposal_services.json \
  --roi roi_analysis.json \
  --roadmap roadmap.json \
  --language "bilingual" \
  --output proposal_ABC_Corporation.md
```

## Output Format

### JSON Service Selection

```json
{
  "schema_version": "1.0",
  "generated_at": "2025-04-15T10:30:00Z",
  "client_industry": "manufacturing",
  "selected_services": [
    {
      "service_id": "fin-001",
      "service_name": "Invoice Processing Automation",
      "category": "finance_accounting",
      "ai_components": ["document_extraction", "validation", "approval_routing"],
      "estimated_automation_rate": 0.85,
      "monthly_fee_usd": 5000
    }
  ]
}
```

### JSON ROI Analysis

```json
{
  "schema_version": "1.0",
  "analysis_date": "2025-04-15",
  "current_state": {
    "annual_cost_usd": 250000,
    "fte_equivalent": 3.5,
    "error_rate_pct": 4.2
  },
  "future_state": {
    "annual_cost_usd": 120000,
    "fte_equivalent": 1.0,
    "error_rate_pct": 0.5
  },
  "implementation_cost_usd": 75000,
  "annual_savings_usd": 130000,
  "payback_months": 7,
  "three_year_npv_usd": 285000,
  "roi_percentage": 173
}
```

### Markdown Proposal Structure

```markdown
# AI-BPO Service Proposal / AI-BPOサービス提案書

## Executive Summary / エグゼクティブサマリー
## Company Understanding / 貴社の理解
## Proposed Solution / ご提案ソリューション
## Service Details / サービス詳細
## ROI Analysis / ROI分析
## Implementation Roadmap / 導入ロードマップ
## Pricing / 価格
## Terms & Conditions / 契約条件
## Next Steps / 次のステップ
```

## Resources

- `scripts/select_services.py` -- Service module selection based on industry and pain points
- `scripts/calculate_roi.py` -- ROI calculation with NPV, payback period
- `scripts/generate_roadmap.py` -- Implementation roadmap generator
- `scripts/generate_proposal.py` -- Bilingual proposal document generator
- `references/service-catalog.md` -- Complete AI-BPO service catalog with pricing
- `references/client-intake-template.md` -- Client requirements questionnaire
- `references/roi-methodology.md` -- ROI calculation methodology and benchmarks
<!-- proposal-template-bilingual.md was referenced but never shipped; the template
     is generated dynamically by generate_proposal.py instead. -->


## Key Principles

1. **Bilingual by Default**: All client-facing documents include both Japanese and English
2. **Conservative ROI Estimates**: Use industry-standard automation rates, not best-case scenarios
3. **Phased Implementation**: Recommend pilot-first approach to minimize risk
4. **Compliance-Aware**: Consider J-SOX, SOX, and data residency requirements
5. **Cultural Sensitivity**: Understand Japanese business practices and decision-making processes

## Industry Benchmarks

| Process | Typical Automation Rate | Error Reduction | Cost Savings |
|---------|------------------------|-----------------|--------------|
| Invoice Processing | 80-90% | 85-95% | 50-70% |
| Expense Reporting | 70-85% | 80-90% | 40-60% |
| Employee Onboarding | 60-75% | 70-85% | 35-50% |
| Customer Ticket Routing | 85-95% | N/A | 60-75% |
| Data Entry | 90-98% | 95-99% | 70-85% |

## Pricing Tiers

| Tier | Monthly Volume | Base Fee (USD) | Per-Transaction |
|------|---------------|----------------|-----------------|
| Starter | < 1,000 | $3,000 | $1.50 |
| Growth | 1,000 - 5,000 | $8,000 | $0.80 |
| Enterprise | 5,000+ | $15,000 | $0.40 |
