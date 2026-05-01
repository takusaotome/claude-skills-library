# Quote Deadline Reminder Template

## Japanese Version

### 件名

【リマインダー】{{PROJECT_NAME}} お見積回答期限のご案内

### 本文（1週間前）

```
{{VENDOR_CONTACT_NAME}} 様

いつもお世話になっております。
{{SENDER_COMPANY}}の{{SENDER_NAME}}でございます。

先日ご依頼いたしました「{{PROJECT_NAME}}」のお見積につきまして、
回答期限が近づいておりますので、リマインドのご連絡をさせていただきます。

■ 回答期限: {{DEADLINE}}（{{DEADLINE_DAY}}）

ご準備の状況はいかがでしょうか。
ご不明点等ございましたら、お気軽にお問い合わせください。

ご多忙の中恐縮ですが、引き続きよろしくお願いいたします。

{{SENDER_NAME}}
{{SENDER_COMPANY}}
```

### 本文（3日前・最終リマインダー）

```
{{VENDOR_CONTACT_NAME}} 様

いつもお世話になっております。
{{SENDER_COMPANY}}の{{SENDER_NAME}}でございます。

「{{PROJECT_NAME}}」のお見積回答期限が迫っておりますので、
最終のご確認をお願いいたします。

■ 回答期限: {{DEADLINE}}（{{DEADLINE_DAY}}）
■ 残り日数: {{DAYS_REMAINING}}日

期限内のご提出が難しい場合は、その旨ご連絡いただけますと幸いです。

何卒よろしくお願いいたします。

{{SENDER_NAME}}
{{SENDER_COMPANY}}
```

---

## English Version

### Subject

[Reminder] {{PROJECT_NAME}} - Quotation Deadline Approaching

### Body (1 Week Before)

```
Dear {{VENDOR_CONTACT_NAME}},

I hope this email finds you well.

This is a friendly reminder regarding the Request for Quotation for
"{{PROJECT_NAME}}" that was sent on {{RFQ_SENT_DATE}}.

## Deadline: {{DEADLINE}}

Please let us know if you have any questions or if you need any
clarification regarding the requirements.

We look forward to receiving your proposal.

Best regards,
{{SENDER_NAME}}
{{SENDER_COMPANY}}
```

### Body (3 Days Before - Final Reminder)

```
Dear {{VENDOR_CONTACT_NAME}},

This is a final reminder that the quotation deadline for "{{PROJECT_NAME}}"
is approaching.

## Deadline: {{DEADLINE}}
## Days Remaining: {{DAYS_REMAINING}}

If you are unable to submit your proposal by the deadline, please let us
know as soon as possible.

Thank you for your attention to this matter.

Best regards,
{{SENDER_NAME}}
{{SENDER_COMPANY}}
```

---

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| PROJECT_NAME | Project name | ERP System Modernization |
| VENDOR_CONTACT_NAME | Recipient name | John Smith |
| SENDER_COMPANY | Sender company | ABC Corporation |
| SENDER_NAME | Sender name | Jane Doe |
| DEADLINE | Response deadline | March 15, 2024 |
| DEADLINE_DAY | Day of week | Friday |
| RFQ_SENT_DATE | Original RFQ date | March 1, 2024 |
| DAYS_REMAINING | Days until deadline | 3 |

## Usage Guidelines

### When to Send Reminders

| Timing | Template | Purpose |
|--------|----------|---------|
| 7 days before | 1 Week Before | Gentle reminder, offer help |
| 3 days before | Final Reminder | Urgency, confirm participation |
| 1 day before | (Optional) | Only if vendor confirmed but not submitted |

### Best Practices

1. **Consistent Timing**: Send reminders at same time of day as original RFQ
2. **Track Opens**: If email tracking available, prioritize non-openers
3. **Phone Follow-up**: Consider calling if no response to reminders
4. **Document Everything**: Log all reminder communications
