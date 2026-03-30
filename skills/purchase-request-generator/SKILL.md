---
name: purchase-request-generator
description: Generate formal IT/hardware purchase request documents from informal requirements. Use when creating purchase justifications, cost-benefit analyses, ROI calculations, vendor comparisons, or MARP presentation slides for management approval.
---

# Purchase Request Generator

## Overview

Generate structured IT/hardware purchase request documents from informal purchase specifications. This skill transforms product details, pricing, and justification notes into formal approval documents including cost-benefit analysis, ROI justification, vendor comparison matrices, and MARP presentation slides suitable for management approval workflows.

## When to Use

- Creating formal purchase requests from informal product/price specifications
- Generating cost-benefit analysis for IT equipment or software purchases
- Building ROI justification documents for budget approvals
- Comparing multiple vendors for procurement decisions
- Preparing MARP presentation slides for purchase approval meetings
- Converting product research notes into approval-ready documentation

## Prerequisites

- Python 3.9+
- No API keys required
- Dependencies: None (standard library only)

## Workflow

### Step 1: Gather Purchase Information

Collect the following information from the user:
- **Product/Service**: Name, model, specifications
- **Vendor(s)**: Vendor name(s), pricing, terms
- **Quantity**: Number of units required
- **Total Cost**: Unit price and total price
- **Justification**: Business need, problem being solved
- **Timeline**: Urgency, implementation timeline
- **Alternatives Considered**: Other options evaluated (if any)

### Step 2: Generate Purchase Request Document

Run the purchase request generator script to create the formal document:

```bash
python3 scripts/generate_purchase_request.py \
  --product "Product Name" \
  --vendor "Vendor Name" \
  --unit-price 1000 \
  --quantity 5 \
  --justification "Business justification text" \
  --requester "Requester Name" \
  --department "Department Name" \
  --output purchase_request.md
```

### Step 3: Generate Cost-Benefit Analysis

Create a detailed cost-benefit analysis using the CBA generator:

```bash
python3 scripts/generate_cba.py \
  --product "Product Name" \
  --total-cost 5000 \
  --useful-life-years 5 \
  --annual-benefit 2000 \
  --benefit-description "Productivity improvement" \
  --output cost_benefit_analysis.md
```

### Step 4: Create Vendor Comparison (if multiple vendors)

If comparing multiple vendors, generate a comparison matrix:

```bash
python3 scripts/generate_vendor_comparison.py \
  --vendors "Vendor A:4500,Vendor B:5000,Vendor C:4800" \
  --criteria "Price,Support,Warranty,Delivery" \
  --scores "Vendor A:4,5,4,3|Vendor B:3,4,5,4|Vendor C:4,3,4,5" \
  --output vendor_comparison.md
```

### Step 5: Generate MARP Presentation Slides

Create presentation slides for management approval meetings:

```bash
python3 scripts/generate_marp_slides.py \
  --title "Purchase Request: Product Name" \
  --product "Product Name" \
  --total-cost 5000 \
  --roi-percent 200 \
  --payback-months 30 \
  --key-benefits "Benefit 1,Benefit 2,Benefit 3" \
  --output purchase_presentation.md
```

### Step 6: Review and Finalize

1. Review generated documents for accuracy
2. Add any company-specific information or templates
3. Attach supporting documentation (quotes, specifications)
4. Submit through appropriate approval workflow

## Output Format

### Purchase Request Document (Markdown)

```markdown
# Purchase Request

## Request Information
- Request ID: PR-YYYYMMDD-001
- Date: YYYY-MM-DD
- Requester: [Name]
- Department: [Department]

## Product Details
- Product: [Name]
- Vendor: [Vendor]
- Quantity: [N]
- Unit Price: $[X]
- Total Cost: $[Y]

## Business Justification
[Detailed justification]

## Budget Information
- Budget Code: [Code]
- Fiscal Year: [FY]

## Approval Status
| Approver | Status | Date |
|----------|--------|------|
| Manager  | Pending | - |
| Director | Pending | - |
```

### Cost-Benefit Analysis (Markdown)

```markdown
# Cost-Benefit Analysis

## Executive Summary
[Brief summary of recommendation]

## Cost Analysis
- Initial Cost: $[X]
- Annual Operating Cost: $[Y]
- Total Cost of Ownership (5 years): $[Z]

## Benefit Analysis
- Annual Benefit: $[A]
- Total Benefit (5 years): $[B]

## Financial Metrics
- ROI: [X]%
- Payback Period: [Y] months
- NPV: $[Z]
```

### MARP Presentation (Markdown)

```markdown
---
marp: true
theme: default
paginate: true
---

# Purchase Request: [Product Name]
## [Department] - [Date]

---

# Executive Summary
- Total Cost: $[X]
- ROI: [Y]%
- Payback: [Z] months

---

# Business Justification
[Key points]

---

# Cost-Benefit Analysis
[Visual summary]

---

# Recommendation
**Approval Requested**
```

## Resources

- `scripts/generate_purchase_request.py` -- Generate formal purchase request documents
- `scripts/generate_cba.py` -- Generate cost-benefit analysis with ROI/NPV calculations
- `scripts/generate_vendor_comparison.py` -- Create vendor comparison matrices
- `scripts/generate_marp_slides.py` -- Generate MARP presentation slides
- `references/purchase_request_guide.md` -- Best practices for purchase justifications
- `assets/marp_template.md` -- MARP slide template with corporate styling

## Key Principles

1. **Completeness**: Include all information approvers need to make decisions
2. **Quantification**: Express benefits in measurable terms where possible
3. **Clarity**: Use clear, concise language appropriate for management review
4. **Accuracy**: Verify all pricing, calculations, and vendor information
5. **Alignment**: Frame justifications in terms of business objectives and strategy
