---
name: audit-control-designer
description: >
  Generate audit-ready internal control design documents from As-Is business process
  inventories. Produces control IDs, assertion mappings, procedures, SoD analysis,
  KPIs, materiality thresholds, and implementation roadmaps. Use when building
  internal controls for new audit engagements, SOX/J-SOX compliance, or process
  improvement initiatives.
---

# Audit Control Designer

## Overview

This skill transforms As-Is business process inventories into comprehensive internal control design documents. It leverages generalized patterns from real audit engagements across industries (F&B, retail, manufacturing) to produce draft control designs that cover all five audit assertions, segregation of duties, KPIs, and implementation roadmaps.

## When to Use

- Starting internal control design from an As-Is process inventory
- Building controls for a new audit engagement (SOX, J-SOX, PCAOB)
- Designing controls for a specific business domain (AP, Inventory, COGS, Returns)
- Reviewing and strengthening existing control frameworks
- Preparing for initial audit readiness assessment

## Prerequisites

None. This is a knowledge-based skill that uses reference documents for pattern matching and generation.

## Input Requirements

### Required: As-Is Business Process Inventory

A table or list of business processes with at minimum:
- Process ID
- Process name/description
- Primary owner/department
- Frequency (daily, weekly, monthly)
- Current tools/records used

### Optional: Context Variables

| Variable | Options | Default |
|---|---|---|
| Accounting Standard | US GAAP / IFRS / J-GAAP | US GAAP |
| Industry | F&B, Retail, Manufacturing, Services | General |
| Company Scale | Small (<50 employees), Medium (50-500), Large (500+) | Medium |
| System Environment | Paper+Excel, Partial ERP, Full ERP | Paper+Excel |
| Regulatory Context | SEC/SOX, J-SOX, Voluntary | SEC/SOX |

## Workflow

### Step 1: Confirm Context Variables

Ask the user to confirm or specify:
- Applicable accounting standard
- Industry and company scale
- Current system environment
- Regulatory requirements

If not specified, use defaults from the table above.

### Step 2: Read As-Is Process Inventory

Read the user-provided process inventory. Identify:
- Total number of processes
- Business domains covered
- Frequency distribution (daily/weekly/monthly)
- Manual risk indicators

### Step 3: Classify Processes into Business Patterns

Load `references/process_patterns.md` and classify each process into one or more patterns:

| Pattern | Domain | Key Processes |
|---|---|---|
| AP (Accounts Payable) | Invoice entry, reconciliation | Procurement, invoice processing, matching |
| Inventory | Stocktake, adjustments | Counting, valuation, shrinkage tracking |
| COGS Calculation | Cost computation | Period-end calculation, variance analysis |
| Returns/Credits | Return processing | Credit notes, period attribution, inventory adjustment |
| Price Management | Unit cost updates | Price revision, master data changes |

### Step 4: Select Control Templates

Load `references/control_templates.md` and select applicable templates based on:
- Matched business patterns from Step 3
- Risk level of each process (High/Medium/Low from the process inventory)
- Audit assertions most at risk for each process (from pattern definitions)

### Step 5: Verify Assertion Coverage

Load `references/assertion_mapping.md` and ensure all five assertions are covered:
- **C**ompleteness: All transactions recorded
- **A**ccuracy: Amounts and quantities correct
- **V**aluation: Appropriate valuation methods applied
- **C**ut-**O**ff: Correct period attribution
- **E**xistence: Assets and transactions are real

Flag any assertion gaps and recommend additional controls.

### Step 6: Perform SoD Analysis

Load `references/sod_patterns.md` and evaluate:
- Which duty pairs should be separated
- Current separation status (based on process ownership)
- Risk level (High/Medium/Low)
- Compensating controls for small organizations

### Step 7: Select KPIs

Load `references/kpi_catalog.md` and assign KPIs to each control:
- Select relevant KPIs based on control objectives
- Define calculation methods
- Set baseline and target placeholders
- Identify data sources

### Step 8: Set Materiality Thresholds

Load `references/materiality_framework.md` and define:
- Overall Materiality framework
- Performance Materiality (typically 50-75% of overall)
- Clearly Trivial threshold (typically 3-5% of overall)
- Control-specific thresholds

### Step 9: Check Accounting Standards

Load `references/accounting_standards.md` and verify:
- Control design aligns with specified accounting standard
- Inventory valuation method is appropriate
- Revenue recognition rules are followed
- Any standard-specific requirements are addressed

### Step 10: Generate Control Design Document

Use `assets/control_design_template.md` to produce the output containing:

1. **Overview**: Scope, applicable standard, materiality
2. **Control Table**: ID, type, objective, procedure, owner, frequency, evidence, remediation
3. **Assertion Mapping**: Assertion x Control coverage matrix
4. **SoD Analysis**: Duty pairs, risk, current state, recommendations
5. **KPI Definitions**: KPI ID, name, formula, baseline, target
6. **Roadmap**: Short-term (M+1 to M+4) and medium-term (M+6 to M+18) initiatives
7. **Open Questions**: Items requiring confirmation or management decision

## Output Format

The output follows the template in `assets/control_design_template.md`. Key sections:

- Control IDs follow the pattern: `C-[DOMAIN]-[NN]` (e.g., C-AP-01, C-INV-01)
- Each control specifies: Type (Preventive/Detective), Assertion coverage, Procedure steps
- SoD pairs are rated High/Medium/Low risk
- KPIs include calculation formula and data source
- Roadmap uses M+N notation (months from project start)
- Open Questions are explicitly managed with options and recommendations

## Customization Guidance

### By Industry

- **F&B**: Emphasize inventory existence, waste tracking, portion control
- **Retail**: Emphasize shrinkage, POS reconciliation, returns processing
- **Manufacturing**: Emphasize WIP valuation, BOM accuracy, yield tracking
- **Services**: Emphasize revenue recognition, project costing, time tracking

### By Scale

- **Small**: Accept compensating controls for SoD gaps, simplify procedures
- **Medium**: Full SoD where possible, standard procedures
- **Large**: Comprehensive SoD, automated controls, multi-level approval

### By System Environment

- **Paper+Excel**: Focus on detective controls, manual evidence, version management
- **Partial ERP**: Hybrid controls, interface reconciliation
- **Full ERP**: Automated preventive controls, system-enforced SoD, audit trails

## Resources

| Type | File | Purpose | When to Load |
|------|------|---------|-------------|
| Reference | `references/process_patterns.md` | 5 business process patterns (AP, Inventory, COGS, Returns, Price) with industry variations | Step 3: Classify processes |
| Reference | `references/control_templates.md` | 8 control pattern templates (T-AP-01/02, T-INV-01/02, T-CO-01, T-VAL-01, T-CALC-01/02) | Step 4: Select templates |
| Reference | `references/assertion_mapping.md` | C/A/V/CO/E definitions, process-to-assertion mapping, coverage matrix template | Step 5: Verify assertion coverage |
| Reference | `references/sod_patterns.md` | 5 SoD pairs with risk ratings and compensating controls | Step 6: Perform SoD analysis |
| Reference | `references/kpi_catalog.md` | K01-K08 KPI definitions with formulas, baselines, and targets | Step 7: Select KPIs |
| Reference | `references/materiality_framework.md` | Overall/Performance/Trivial materiality, threshold guidelines, escalation rules | Step 8: Set materiality |
| Reference | `references/accounting_standards.md` | US GAAP/IFRS/J-GAAP differences affecting control design | Step 9: Check standards |
| Asset | `assets/control_design_template.md` | Output template with 7 sections + 2 appendices | Step 10: Generate output |

## Integration with audit-doc-checker

After generating a control design document, run `audit-doc-checker` to validate quality:

1. Generate control design with this skill
2. Review with `audit-doc-checker` (target score: 70+)
3. Address findings and regenerate affected sections
4. Iterate until quality threshold is met
