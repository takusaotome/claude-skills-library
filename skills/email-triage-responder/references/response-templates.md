# Response Templates Reference

## Template Structure

Each template follows this structure:
- **Tone variants**: Professional, Friendly, Formal
- **Language support**: EN, JA (with examples)
- **Placeholder syntax**: `{{variable_name}}`

## Acknowledgment Templates

### Simple Acknowledgment

**Use when**: Confirming receipt, no immediate action needed

**Professional (EN)**:
```
Thank you for your email. I've received {{document_type}} and will review it by {{target_date}}.

I'll follow up with any questions or feedback.

Best regards,
{{sender_name}}
```

**Professional (JA)**:
```
メールをいただきありがとうございます。{{document_type}}を受領いたしました。{{target_date}}までに確認させていただきます。

ご質問やフィードバックがございましたら、改めてご連絡いたします。

よろしくお願いいたします。
{{sender_name}}
```

### Acknowledgment with Timeline

**Use when**: Need to set expectations for response time

**Professional (EN)**:
```
Thank you for reaching out regarding {{topic}}.

I'm currently reviewing this and will provide a detailed response by {{target_date}}. If you need anything sooner, please let me know.

Best regards,
{{sender_name}}
```

## Information Request Templates

### Clarification Request

**Use when**: Need more details before proceeding

**Professional (EN)**:
```
Thank you for your email about {{topic}}.

To ensure I can assist you effectively, could you please clarify:

1. {{question_1}}
2. {{question_2}}
3. {{question_3}}

Once I have this information, I'll be able to {{next_action}}.

Best regards,
{{sender_name}}
```

**Friendly (EN)**:
```
Thanks for getting in touch about {{topic}}!

I'd love to help, but I need a bit more info first:

- {{question_1}}
- {{question_2}}

Let me know and I'll get right on it!

Cheers,
{{sender_name}}
```

### Missing Attachment Follow-up

**Use when**: Referenced attachment is missing

**Professional (EN)**:
```
Thank you for your email regarding {{topic}}.

It appears the attachment you referenced may not have come through. Could you please resend it?

I'll review it as soon as I receive it.

Best regards,
{{sender_name}}
```

## Meeting Response Templates

### Meeting Acceptance

**Professional (EN)**:
```
Thank you for the meeting invitation.

I confirm my attendance for {{meeting_topic}} on {{meeting_date}} at {{meeting_time}}.

{{#if agenda_comment}}
Regarding the agenda, {{agenda_comment}}.
{{/if}}

Looking forward to the discussion.

Best regards,
{{sender_name}}
```

### Meeting Decline with Alternative

**Professional (EN)**:
```
Thank you for the meeting invitation for {{meeting_topic}}.

Unfortunately, I have a conflict at the proposed time. Would any of these alternatives work?

- {{alternative_1}}
- {{alternative_2}}

Please let me know what works best for your schedule.

Best regards,
{{sender_name}}
```

### Meeting Reschedule Request

**Professional (EN)**:
```
I hope this message finds you well.

Due to {{reason}}, I need to request a reschedule of our meeting originally planned for {{original_date}}.

Would {{proposed_date}} work for you instead? I apologize for any inconvenience.

Best regards,
{{sender_name}}
```

## Vendor Communication Templates

### Quote Request Response

**Professional (EN)**:
```
Thank you for providing the quote for {{service_product}}.

I've reviewed the proposal and {{#if approved}}we'd like to proceed{{else}}have some questions{{/if}}:

{{#if questions}}
1. {{question_1}}
2. {{question_2}}
{{/if}}

{{#if approved}}
Please send the contract and we can move forward with the next steps.
{{/if}}

Best regards,
{{sender_name}}
```

### Invoice Acknowledgment

**Professional (EN)**:
```
Thank you for sending invoice #{{invoice_number}} dated {{invoice_date}}.

I've forwarded this to our accounts payable team for processing. Payment will be made according to our standard {{payment_terms}} terms.

Please let me know if you have any questions.

Best regards,
{{sender_name}}
```

## Delegation Templates

### Forwarding to Colleague

**Professional (EN)**:
```
Hi {{colleague_name}},

I'm forwarding the email below regarding {{topic}} as this falls within your area.

Could you please respond to {{original_sender}} by {{target_date}}?

Key points:
- {{key_point_1}}
- {{key_point_2}}

Let me know if you need any additional context.

Thanks,
{{sender_name}}
```

### CC Introduction

**Professional (EN)**:
```
Hi {{original_sender}},

I'm looping in {{colleague_name}} who handles {{area_of_expertise}} on our team.

{{colleague_first_name}}, could you please assist with {{request_summary}}?

I'll let you two take it from here, but feel free to include me if needed.

Best regards,
{{sender_name}}
```

## Follow-up Templates

### Status Update Request

**Professional (EN)**:
```
Hi {{recipient_name}},

I wanted to follow up on {{topic}} that we discussed on {{original_date}}.

Could you provide an update on the current status? Specifically, I'm wondering about:

- {{status_question_1}}
- {{status_question_2}}

Please let me know if there's anything you need from my end.

Best regards,
{{sender_name}}
```

### Reminder (First)

**Professional (EN)**:
```
Hi {{recipient_name}},

I wanted to gently follow up on my previous email regarding {{topic}} sent on {{original_date}}.

I understand you may be busy, but I'd appreciate an update when you have a moment.

{{#if deadline}}
As a reminder, the deadline for this is {{deadline}}.
{{/if}}

Best regards,
{{sender_name}}
```

### Reminder (Second/Escalation)

**Professional (EN)**:
```
Hi {{recipient_name}},

I'm following up again on {{topic}} - this is my second attempt to reach you regarding this matter.

{{#if impact}}
Without a response, {{impact_description}}.
{{/if}}

Could you please respond by {{final_deadline}} or let me know who else I should contact?

Thank you,
{{sender_name}}
```

## Tone Modifiers

### Professional to Friendly Conversion

| Professional | Friendly |
|--------------|----------|
| "Thank you for your email" | "Thanks for reaching out!" |
| "I hope this message finds you well" | "Hope you're doing well!" |
| "Please let me know" | "Just let me know" |
| "Best regards" | "Cheers" / "Thanks!" |
| "I would appreciate" | "I'd love it if" |
| "At your earliest convenience" | "When you get a chance" |

### Professional to Formal Conversion

| Professional | Formal |
|--------------|--------|
| "Thank you for your email" | "Thank you for your correspondence" |
| "I've received" | "I acknowledge receipt of" |
| "Please let me know" | "Kindly advise" |
| "Best regards" | "Respectfully" |
| "I'll follow up" | "I shall provide further communication" |

## Variable Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `{{sender_name}}` | User's name | "John Smith" |
| `{{recipient_name}}` | Original sender's name | "Jane Doe" |
| `{{topic}}` | Email subject/topic | "Q4 budget review" |
| `{{target_date}}` | Expected response date | "Friday, January 19" |
| `{{document_type}}` | Type of attachment | "proposal", "invoice" |
| `{{meeting_date}}` | Meeting date | "January 20, 2024" |
| `{{meeting_time}}` | Meeting time | "2:00 PM EST" |
| `{{colleague_name}}` | Name of person being delegated to | "Bob Johnson" |
| `{{deadline}}` | Hard deadline if exists | "January 15, 2024" |
