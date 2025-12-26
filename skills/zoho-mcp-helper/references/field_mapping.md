# Zoho Desk Field Mapping Reference

## Ticket Fields

### Full Response Fields (Unfiltered)
The full MCP response includes 50+ fields per ticket including:
- id, ticketNumber, subject, description, status, priority, channel
- contactId, email, phone, secondaryContacts
- departmentId, assigneeId, teamId
- productId, classification, category, subCategory
- createdTime, modifiedTime, dueDate, closedTime
- resolution, commentCount, threadCount
- cf (custom fields), customFields
- webUrl, layoutId, language
- entitySkills, tags, sharedDepartments
- And many more...

### Compact Format Fields (Filtered)
For efficient context usage, extract only:

| Field | Type | Notes |
|-------|------|-------|
| id | string | Unique ticket ID |
| ticketNumber | string | Human-readable ticket number |
| subject | string | Truncate to 80 chars |
| status | string | Open, Closed, On Hold, etc. |
| priority | string | High, Medium, Low, None |
| channel | string | Email, Phone, Web, etc. |
| email | string | Contact email |
| createdTime | datetime | ISO format |
| dueDate | datetime | ISO format, null if not set |
| assignee.firstName | string | Only first name |

### Detail Format Fields
For single ticket view, include:

| Field | Type | Notes |
|-------|------|-------|
| id | string | Unique ticket ID |
| ticketNumber | string | Human-readable ticket number |
| subject | string | Full subject |
| description | string | Truncate to 500 chars |
| status | string | Status name |
| priority | string | Priority level |
| channel | string | Channel type |
| email | string | Contact email |
| phone | string | Contact phone |
| assignee.firstName | string | Assignee name |
| createdTime | datetime | Creation time |
| modifiedTime | datetime | Last modified |
| dueDate | datetime | Due date |
| closedTime | datetime | Closed time (if closed) |
| resolution | string | Resolution notes |

## Thread Fields

### Full Response Fields
- id, channel, direction, type, status
- content, contentType, summary
- from (object with email, name), to, cc, bcc
- fromEmailAddress, toEmailAddress
- sendDateTime, createdTime
- author (object), actor (object)
- hasAttach, attachments
- visibility, isForward, isPrivate
- And more...

### Compact Format Fields

| Field | Type | Notes |
|-------|------|-------|
| id | string | Thread ID |
| direction | string | in/out |
| channel | string | EMAIL, PHONE, etc. |
| from | string | Email address |
| to | string | Recipient |
| sendDateTime | datetime | When sent |
| contentSummary | string | First 200 chars, HTML stripped |
| hasAttachment | boolean | Has attachments |

## Output Size Comparison

| Query Type | Full Response | Compact Format | Reduction |
|------------|---------------|----------------|-----------|
| 20 tickets | ~40KB | ~4KB | 90% |
| Single ticket | ~3KB | ~500B | 83% |
| 10 threads | ~15KB | ~2KB | 87% |

## Status Values

| Status | Description |
|--------|-------------|
| Open | New or in progress |
| Closed | Resolved and closed |
| On Hold | Waiting for customer/info |
| Escalated | Escalated to higher level |

## Priority Values

| Priority | Description |
|----------|-------------|
| High | Urgent attention needed |
| Medium | Standard priority |
| Low | Can wait |
| None | No priority set |

## Channel Values

| Channel | Description |
|---------|-------------|
| EMAIL | Email ticket |
| PHONE | Phone call ticket |
| WEB | Web form submission |
| CUSTOMERPORTAL | Customer portal |
| FORUMS | Community forums |
| CHAT | Live chat |
| TWITTER | Twitter/X |
| FACEBOOK | Facebook |

## Custom Field Handling

Custom fields (cf, customFields) are typically excluded from compact output.
If specific custom fields are needed, specify them explicitly:

```
Extract custom field 'cf.cf_order_number' as 'orderNumber'
```

## Date Format

All dates should be formatted as:
- Display: `YYYY-MM-DD HH:mm` (24-hour format)
- ISO: `2025-12-20T10:30:00.000Z`

For relative time, use:
- Today: "Today 10:30"
- This week: "Mon 10:30"
- Older: "Dec 15"
