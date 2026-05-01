---
name: internal-email-composer
description: Compose professional internal emails for coordination tasks like vendor quote requests, task delegation, and follow-up communications. Generates bilingual (JA/EN) email drafts with proper business tone. Use when user needs to draft internal emails for vendor RFQ forwarding, quote compilation requests, status updates, or task delegation.
---

# Internal Email Composer

## Overview

This skill generates professional internal email drafts for common coordination tasks in business environments. It creates culturally-appropriate bilingual (Japanese/English) emails with proper business tone, supporting scenarios like vendor quote requests, task delegation, status updates, and follow-up communications.

## When to Use

- Drafting internal emails to request vendor quote compilation from team members
- Forwarding RFQ documents to internal stakeholders with proper context
- Delegating tasks to team members with clear instructions
- Sending status update emails for ongoing projects
- Composing follow-up emails for pending responses
- Creating escalation emails for delayed deliverables
- Requesting information gathering from multiple departments

## Prerequisites

- Python 3.9+
- No API keys required
- Standard library only (no third-party packages)

## Workflow

### Step 1: Gather Email Context

Collect the following information from the user:

1. **Email Type**: Select from supported scenarios (vendor_rfq, task_delegation, status_update, follow_up, escalation, info_request)
2. **Recipient Information**: Name, role/title, department
3. **Language**: Primary language (ja/en) with optional bilingual output
4. **Key Points**: Main content items to include
5. **Deadline**: If applicable
6. **Attachments**: List of attached files if any
7. **Urgency Level**: normal, high, urgent

### Step 2: Generate Email Draft

Run the email composition script with gathered context:

```bash
python3 scripts/compose_email.py \
  --type vendor_rfq \
  --recipient-name "Tanaka-san" \
  --recipient-role "Procurement Manager" \
  --language ja \
  --key-points "Request quote compilation for AWS infrastructure project" \
  --deadline "2024-12-20" \
  --urgency normal \
  --output email_draft.md
```

### Step 3: Review and Customize

1. Review the generated email draft
2. Adjust tone if needed (more formal/casual)
3. Add specific project details or context
4. Verify cultural appropriateness for the recipient

### Step 4: Output Final Draft

Present the final email draft in the requested format (Markdown or plain text) with:
- Subject line
- Greeting
- Body with clear structure
- Call to action
- Closing with appropriate signature block

## Supported Email Scenarios

### 1. Vendor RFQ Forwarding (vendor_rfq)

Forward RFQ documents to internal team for vendor outreach.

**Key elements**:
- Project context and scope
- RFQ document summary
- Vendor selection criteria
- Response deadline
- Contact information for queries

### 2. Task Delegation (task_delegation)

Assign specific tasks to team members with clear expectations.

**Key elements**:
- Task description and objectives
- Expected deliverables
- Timeline and milestones
- Resources and support available
- Escalation path

### 3. Status Update (status_update)

Provide project or task status to stakeholders.

**Key elements**:
- Current status summary
- Progress since last update
- Issues and blockers
- Next steps
- Action items

### 4. Follow-up Request (follow_up)

Request response or action on pending items.

**Key elements**:
- Reference to original request
- Outstanding items
- Updated deadline if applicable
- Offer of assistance

### 5. Escalation (escalation)

Escalate delayed or blocked items to management.

**Key elements**:
- Issue summary
- Impact assessment
- Actions taken
- Requested support
- Proposed timeline

### 6. Information Request (info_request)

Request information gathering from teams or departments.

**Key elements**:
- Information needed
- Purpose and context
- Format requirements
- Deadline for response

## Output Format

### Markdown Email Draft

```markdown
# Email Draft

**Type**: vendor_rfq
**Language**: Japanese
**Generated**: 2024-12-10T14:30:00

---

## Subject
見積依頼の件（AWSインフラプロジェクト）

## To
田中様（調達部マネージャー）

## Body

田中様

お疲れ様です。システム開発部の山田です。

AWSインフラプロジェクトに関する見積依頼書を送付いたします。
下記の内容をご確認の上、各ベンダーへのご連絡をお願いできますでしょうか。

【依頼内容】
- 対象ベンダー：AWS認定パートナー3社
- 見積回答期限：12月20日（金）
- 添付資料：RFQ文書一式

ご不明点がございましたら、お気軽にお問い合わせください。
よろしくお願いいたします。

---
山田太郎
システム開発部
内線: 1234
```

### JSON Structure (for programmatic use)

```json
{
  "schema_version": "1.0",
  "email_type": "vendor_rfq",
  "language": "ja",
  "generated_at": "2024-12-10T14:30:00",
  "subject": "見積依頼の件（AWSインフラプロジェクト）",
  "recipient": {
    "name": "田中様",
    "role": "調達部マネージャー"
  },
  "body": {
    "greeting": "お疲れ様です。",
    "introduction": "AWSインフラプロジェクトに関する見積依頼書を送付いたします。",
    "main_content": ["依頼内容の詳細"],
    "call_to_action": "各ベンダーへのご連絡をお願いできますでしょうか。",
    "closing": "よろしくお願いいたします。"
  },
  "signature": {
    "name": "山田太郎",
    "department": "システム開発部",
    "contact": "内線: 1234"
  }
}
```

## Cultural Considerations

### Japanese Business Email Etiquette

1. **Greetings**: Use appropriate seasonal greetings and 「お疲れ様です」
2. **Honorifics**: Use proper 敬語 (keigo) and titles (様、部長、課長)
3. **Structure**: Follow 起承転結 pattern for logical flow
4. **Closing**: Use standard closing phrases (よろしくお願いいたします)
5. **Indirection**: Use softer requests (～いただけますでしょうか)

### English Business Email Etiquette

1. **Greetings**: Use appropriate salutations (Dear, Hello, Hi based on formality)
2. **Directness**: Be clear and concise in requests
3. **Action Items**: Clearly state expected actions with deadlines
4. **Closing**: Professional sign-off (Best regards, Kind regards, Thank you)

## Resources

- `scripts/compose_email.py` -- Main email composition script with template engine
- `references/email-templates.md` -- Template patterns for each email type
- `references/business-etiquette-guide.md` -- Cultural considerations for JA/EN emails

## Key Principles

1. **Clarity First**: Ensure the purpose and action items are immediately clear
2. **Cultural Appropriateness**: Match tone and formality to recipient and culture
3. **Actionable Content**: Include specific deadlines, deliverables, and next steps
4. **Professional Tone**: Maintain appropriate business language throughout
5. **Bilingual Support**: Generate culturally-adapted versions, not literal translations
