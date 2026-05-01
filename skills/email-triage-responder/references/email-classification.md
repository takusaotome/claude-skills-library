# Email Classification Reference

## Topic Taxonomy

### Primary Categories

| Category | Description | Keywords & Patterns |
|----------|-------------|---------------------|
| `client_followup` | Client-initiated communication requiring response | client, customer, account, project status, deliverable |
| `internal_request` | Requests from colleagues or management | request, need, please, can you, would you, help with |
| `vendor_inquiry` | Communication from vendors or suppliers | invoice, quote, proposal, pricing, renewal, contract |
| `meeting_scheduling` | Calendar and meeting coordination | meeting, call, schedule, availability, calendar, invite |
| `fyi_informational` | No action required, information only | FYI, for your information, heads up, newsletter, update |
| `approval_required` | Requires sign-off or decision | approve, approval, sign off, authorize, confirm |
| `escalation` | Elevated priority from normal channels | escalate, urgent, ASAP, immediately, critical |
| `delegation_candidate` | Can be forwarded to team member | routine, standard, process, procedure |

### Secondary Tags

- `has_attachment`: Email contains files
- `is_reply`: Part of existing thread
- `external_sender`: From outside organization
- `vip_sender`: From flagged important contacts
- `has_deadline`: Contains explicit due date
- `bulk_recipient`: Sent to large distribution list

## Urgency Markers

### High Urgency Indicators (Score: 0.8-1.0)

| Marker Type | Examples |
|-------------|----------|
| Explicit keywords | "URGENT", "ASAP", "immediately", "critical", "emergency" |
| Time constraints | "by EOD", "within 24 hours", "before the meeting", "today" |
| Escalation language | "second request", "following up again", "still waiting" |
| Sender signals | Reply-to from executive, marked high importance |
| Subject prefixes | [URGENT], [ACTION REQUIRED], [TIME SENSITIVE] |

### Medium Urgency Indicators (Score: 0.4-0.7)

| Marker Type | Examples |
|-------------|----------|
| Soft deadlines | "this week", "when you get a chance", "soon" |
| Standard requests | "please review", "let me know", "can you check" |
| Meeting-related | "before our meeting", "for tomorrow's call" |
| Follow-up language | "checking in", "wanted to follow up" |

### Low Urgency Indicators (Score: 0.0-0.3)

| Marker Type | Examples |
|-------------|----------|
| Informational | "FYI", "no action needed", "for your records" |
| Bulk distribution | newsletters, announcements, CC-heavy emails |
| Future planning | "next quarter", "for future reference", "eventually" |

## Importance Scoring

### Sender-Based Importance

| Sender Type | Base Score | Notes |
|-------------|------------|-------|
| Direct manager | 0.9 | Always high priority |
| Executive (C-level) | 0.95 | Highest priority |
| Key client contact | 0.85 | Revenue-impacting |
| Team member | 0.5 | Normal priority |
| External vendor | 0.4 | Unless contract-critical |
| Unknown external | 0.3 | May be spam or cold outreach |
| Automated system | 0.2 | Usually informational |

### Content-Based Importance Modifiers

| Content Signal | Modifier |
|----------------|----------|
| Direct "To:" recipient (not CC) | +0.1 |
| Only recipient | +0.15 |
| Mentions deadline | +0.1 |
| Contains financial terms | +0.1 |
| Contains legal terms | +0.15 |
| Part of active project | +0.1 |
| First contact (no history) | -0.05 |

## Action Type Detection

### Response Required

Signals that a reply is expected:
- Direct questions ("Can you...?", "What is...?", "When will...?")
- Request language ("please", "would you", "could you")
- Explicit ask ("I need", "we need", "send me")
- Awaiting confirmation ("let me know", "confirm", "acknowledge")

### Review Required

Signals that review/approval is needed:
- Attachment with review request
- "Please review" or "for your approval"
- Document versioning language ("v2", "revised", "updated")
- Sign-off requests

### Delegation Candidate

Signals that forwarding may be appropriate:
- Generic inbox (info@, support@)
- Outside your area of expertise
- Routine/procedural requests
- Team member mentioned who could handle

### Archive/No Action

Signals that filing without response is appropriate:
- Newsletter or automated digest
- BCC recipient only
- "No reply needed"
- Completed thread (contains "Thanks!" as final message)

## VIP Contact Management

### VIP Identification Criteria

1. **Executive contacts**: CEO, CFO, CTO, VP-level
2. **Key accounts**: Top 10 clients by revenue
3. **Strategic partners**: Named partnership contacts
4. **Board members**: Directors and advisors
5. **User-flagged**: Manually marked as important

### VIP Handling Rules

- Always classify as minimum Q2 (Important)
- Generate draft response even for FYI emails
- Alert if no response within 24 hours
- Track response time metrics separately

## Language Detection

### Supported Languages

| Language | Detection Patterns |
|----------|-------------------|
| English (EN) | Default if Latin script with English keywords |
| Japanese (JA) | Hiragana, Katakana, Kanji presence |
| Spanish (ES) | Spanish-specific characters (ñ, ¿, ¡) |
| French (FR) | French accents (é, è, ê, ç) |
| German (DE) | German characters (ß, ü, ö, ä) |
| Chinese (ZH) | Chinese characters without Japanese kana |

### Response Language Rules

1. **Match sender language**: Reply in the language the email was written in
2. **Organization default**: Fall back to organization's primary language
3. **User preference**: Override with user's preferred language if set
4. **Mixed language**: Use the dominant language (>60% of content)

## Thread Analysis

### Thread Position Detection

| Position | Indicators |
|----------|------------|
| New thread | No "Re:" prefix, no In-Reply-To header |
| Reply | "Re:" prefix, has In-Reply-To |
| Forward | "Fwd:" prefix, forwarded headers |
| Thread continuation | Multiple "Re:" levels |

### Thread Context Extraction

For replies, extract from thread:
1. Original sender's name and role
2. Original request/question
3. Key decisions made in thread
4. Open action items
5. Tone of previous exchanges
