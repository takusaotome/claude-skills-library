---
name: vendor-procurement-coordinator
description: End-to-end vendor procurement workflow orchestrating RFQ creation, email sending, vendor response tracking, and client-facing estimate generation. Use this skill when managing the full quote-request-to-client-estimate pipeline, coordinating between vendor-rfq-creator and vendor-estimate-creator skills with email automation and status tracking.
---

# Vendor Procurement Coordinator

## Overview

This skill orchestrates the complete vendor procurement lifecycle from initial RFQ creation through vendor response tracking to final client-facing estimate generation. It integrates with existing `vendor-rfq-creator` and `vendor-estimate-creator` skills while adding email automation, response tracking, and procurement status management capabilities.

**Primary language**: Japanese (default), English supported
**Output format**: Markdown, JSON, Email templates

## When to Use

- Managing multiple vendor solicitations for a single project
- Tracking vendor quote responses and deadlines
- Converting received vendor quotes into client-facing estimates
- Automating RFQ distribution to vendor email lists
- Coordinating the end-to-end procurement pipeline
- Comparing vendor responses and creating evaluation summaries
- Generating procurement status reports for stakeholders

## Prerequisites

- Python 3.9+
- Standard library + `pyyaml` for configuration
- Email credentials (SMTP) for sending RFQs (optional, manual mode available)
- Access to `vendor-rfq-creator` and `vendor-estimate-creator` skills (recommended)

## Workflow

### Step 1: Initialize Procurement Project

Create a new procurement tracking project with metadata.

```bash
python3 scripts/init_procurement.py \
  --project-name "ERP System Replacement" \
  --client "Acme Corporation" \
  --output-dir ./procurement/erp-2024
```

This creates the procurement project structure:
```
procurement/erp-2024/
├── procurement.yaml       # Project configuration and status
├── rfq/                   # RFQ documents (from vendor-rfq-creator)
├── quotes/                # Received vendor quotes
├── estimates/             # Client-facing estimates (from vendor-estimate-creator)
└── communications/        # Email templates and tracking
```

### Step 2: Create RFQ Document

Use `vendor-rfq-creator` skill to generate the RFQ document. Save the output to the `rfq/` directory.

Reference: See `references/procurement_workflow_guide.md` for RFQ best practices.

### Step 3: Register Vendors

Register vendors to receive the RFQ and track responses.

```bash
python3 scripts/manage_vendors.py add \
  --project-dir ./procurement/erp-2024 \
  --vendor-name "Tech Solutions Inc." \
  --contact-email "sales@techsolutions.example.com" \
  --contact-name "John Smith"
```

Bulk import from CSV:

```bash
python3 scripts/manage_vendors.py import \
  --project-dir ./procurement/erp-2024 \
  --csv-file vendors.csv
```

### Step 4: Send RFQ to Vendors

Generate and optionally send RFQ emails to registered vendors.

```bash
python3 scripts/send_rfq.py \
  --project-dir ./procurement/erp-2024 \
  --rfq-file rfq/rfq_document.md \
  --deadline 2024-03-15 \
  --mode preview
```

Modes:
- `preview`: Generate email content for manual sending
- `send`: Send via SMTP (requires email configuration)

Email template customization available via `assets/email_templates/`.

### Step 5: Track Vendor Responses

Log received vendor quotes and update tracking status.

```bash
python3 scripts/track_responses.py log \
  --project-dir ./procurement/erp-2024 \
  --vendor-name "Tech Solutions Inc." \
  --quote-file "quotes/tech_solutions_quote.pdf" \
  --amount 15000000 \
  --currency JPY \
  --delivery-date 2024-06-30
```

View tracking dashboard:

```bash
python3 scripts/track_responses.py status \
  --project-dir ./procurement/erp-2024
```

### Step 6: Compare and Evaluate Quotes

Generate a vendor comparison report.

```bash
python3 scripts/compare_quotes.py \
  --project-dir ./procurement/erp-2024 \
  --output quotes/comparison_report.md
```

Reference: See `references/vendor_evaluation_criteria.md` for evaluation framework.

### Step 7: Create Client-Facing Estimate

Convert the selected vendor quote(s) into a client-facing estimate using `vendor-estimate-creator` skill.

Apply markup and consolidation:

```bash
python3 scripts/create_client_estimate.py \
  --project-dir ./procurement/erp-2024 \
  --vendor-quote "quotes/tech_solutions_quote.pdf" \
  --markup-percent 15 \
  --output estimates/client_estimate.md
```

### Step 8: Generate Procurement Report

Create final procurement summary for stakeholders.

```bash
python3 scripts/generate_report.py \
  --project-dir ./procurement/erp-2024 \
  --output procurement_summary.md
```

## Output Format

### Procurement Status (YAML)

```yaml
project:
  name: "ERP System Replacement"
  client: "Acme Corporation"
  created: "2024-02-01"
  status: "quotes_received"  # initialized | rfq_sent | quotes_received | evaluation | completed

rfq:
  document: "rfq/rfq_document.md"
  sent_date: "2024-02-05"
  deadline: "2024-03-15"

vendors:
  - name: "Tech Solutions Inc."
    email: "sales@techsolutions.example.com"
    status: "quote_received"  # pending | contacted | quote_received | declined | selected
    quote:
      file: "quotes/tech_solutions_quote.pdf"
      amount: 15000000
      currency: "JPY"
      received_date: "2024-03-01"
  - name: "Digital Systems Corp."
    email: "info@digitalsystems.example.com"
    status: "contacted"
    quote: null

timeline:
  - date: "2024-02-01"
    event: "Project initialized"
  - date: "2024-02-05"
    event: "RFQ sent to 3 vendors"
  - date: "2024-03-01"
    event: "Quote received from Tech Solutions Inc."
```

### Vendor Comparison Report (Markdown)

```markdown
# Vendor Comparison Report

## Project: ERP System Replacement
Generated: 2024-03-20

## Summary

| Vendor | Quote Amount | Delivery | Score |
|--------|-------------|----------|-------|
| Tech Solutions Inc. | ¥15,000,000 | 2024-06-30 | 85/100 |
| Digital Systems Corp. | ¥18,500,000 | 2024-07-15 | 78/100 |

## Detailed Evaluation

### Tech Solutions Inc.
- **Price**: 30/30 (Most competitive)
- **Technical Capability**: 25/25 (Strong track record)
- **Delivery Timeline**: 15/20 (Within deadline)
- **Support & Maintenance**: 15/25 (Standard SLA)

[Additional details...]
```

## Resources

### scripts/

- `init_procurement.py` -- Initialize procurement project structure
- `manage_vendors.py` -- Add, edit, remove, import vendor contacts
- `send_rfq.py` -- Generate and send RFQ emails
- `track_responses.py` -- Log and track vendor quote responses
- `compare_quotes.py` -- Generate vendor comparison report
- `create_client_estimate.py` -- Convert vendor quote to client estimate
- `generate_report.py` -- Create procurement summary report

### references/

- `procurement_workflow_guide.md` -- Complete procurement process guide with best practices
- `vendor_evaluation_criteria.md` -- Evaluation framework and scoring methodology

### assets/

- `email_templates/rfq_email_ja.md` -- Japanese RFQ email template
- `email_templates/rfq_email_en.md` -- English RFQ email template
- `email_templates/reminder_email.md` -- Quote deadline reminder template

## Integration with Related Skills

### vendor-rfq-creator

Use before Step 2 to generate comprehensive RFQ documents:
- Transform vague requirements into structured RFQs
- Apply 150+ item checklist for completeness
- Generate professional Japanese/English RFQs

### vendor-estimate-creator

Use in Step 7 to create client-facing estimates:
- Apply WBS methodology to vendor quotes
- Add markup and consolidation
- Include ROI analysis for client justification

## Key Principles

1. **Track Everything**: Maintain complete audit trail of all vendor communications
2. **Fair Process**: Send identical RFQs to all vendors with same deadlines
3. **Transparent Evaluation**: Use consistent, documented evaluation criteria
4. **Timely Follow-up**: Monitor deadlines and send reminders proactively
5. **Professional Communication**: Use standardized email templates for consistency

## Common Pitfalls

1. Missing vendor response deadlines without follow-up
2. Sending different RFQ versions to different vendors
3. Not documenting verbal communications
4. Skipping formal evaluation when vendor preference exists
5. Incomplete quote comparison (missing non-price factors)
6. Not tracking quote validity periods

## Quick Reference

### Procurement Status Workflow

```
initialized → rfq_sent → quotes_received → evaluation → completed
                ↓              ↓
            (reminders)    (follow-ups)
```

### Vendor Status Workflow

```
pending → contacted → quote_received → selected
              ↓             ↓            ↓
          declined      withdrawn    contracted
```

### 10-Step Procurement Checklist

1. [ ] Initialize procurement project
2. [ ] Create RFQ document (vendor-rfq-creator)
3. [ ] Register all candidate vendors
4. [ ] Send RFQ with clear deadline
5. [ ] Track responses and send reminders
6. [ ] Log all received quotes
7. [ ] Create vendor comparison report
8. [ ] Evaluate and select vendor(s)
9. [ ] Create client-facing estimate (vendor-estimate-creator)
10. [ ] Generate final procurement report

---

## Version History

- **v1.0** (2025-01-08): Initial release
  - 7 workflow steps with automation scripts
  - Vendor tracking and status management
  - Email template system
  - Integration with vendor-rfq-creator and vendor-estimate-creator
  - Comparison report generation
