# RFQ Email Template (English)

## Subject

[RFQ] Request for Quotation - {{PROJECT_NAME}}

## Body

```
Dear {{VENDOR_CONTACT_NAME}},

I hope this email finds you well. My name is {{SENDER_NAME}} from {{SENDER_COMPANY}}.

We are reaching out to request a quotation for "{{PROJECT_NAME}}" on behalf of our client.

## Project Overview
{{PROJECT_SUMMARY}}

## Attachments
- Request for Quotation (RFQ): {{RFQ_FILENAME}}
{{#if ATTACHMENTS}}
{{#each ATTACHMENTS}}
- {{this}}
{{/each}}
{{/if}}

## Submission Deadline
Please submit your quotation by {{DEADLINE}}.

## Questions
If you have any questions regarding this RFQ, please submit them by {{QA_DEADLINE}}
by replying to this email. In the interest of fairness, all questions and answers
will be shared with all vendors receiving this RFQ.

## Submission Instructions
Please send your quotation to: {{SUBMISSION_EMAIL}}
Subject line: [Quote Response] {{PROJECT_NAME}} - {{VENDOR_COMPANY_NAME}}

Please note that this RFQ has been sent to multiple vendors as part of our
competitive bidding process.

We appreciate your time and look forward to receiving your proposal.

Best regards,

{{SENDER_NAME}}
{{SENDER_DEPARTMENT}}
{{SENDER_COMPANY}}
Phone: {{SENDER_PHONE}}
Email: {{SENDER_EMAIL}}
```

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| PROJECT_NAME | Project name | ERP System Modernization |
| VENDOR_CONTACT_NAME | Recipient name | John Smith |
| VENDOR_COMPANY_NAME | Vendor company | Tech Solutions Inc. |
| SENDER_COMPANY | Sender company | ABC Corporation |
| SENDER_NAME | Sender name | Jane Doe |
| SENDER_DEPARTMENT | Sender department | IT Procurement |
| SENDER_PHONE | Sender phone | +1-555-123-4567 |
| SENDER_EMAIL | Sender email | jane.doe@abc.com |
| PROJECT_SUMMARY | Project summary (2-3 lines) | Modernization of legacy... |
| RFQ_FILENAME | RFQ file name | RFQ_ERP_Modernization_v1.0.pdf |
| ATTACHMENTS | Additional attachment list | - |
| DEADLINE | Response deadline | March 15, 2024 |
| QA_DEADLINE | Q&A deadline | March 8, 2024 |
| SUBMISSION_EMAIL | Submission email | rfq@abc.com |
