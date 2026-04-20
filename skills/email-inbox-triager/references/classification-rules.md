# Email Classification Rules

This document defines the NLP-based heuristics and signal weights used to classify emails into action categories.

## Classification Categories

### 1. Urgent Response

**Definition**: Emails requiring immediate attention with time-sensitive implications.

**Signals** (cumulative scoring):

| Signal | Weight | Detection Pattern |
|--------|--------|-------------------|
| VIP sender | +30 | Matches `--vip-senders` or `--vip-domains` list |
| Deadline keyword | +25 | "EOD", "end of day", "ASAP", "urgent", "immediately", "by tomorrow", "deadline" |
| Reply-expected | +15 | "Please reply", "let me know", "your thoughts?", "awaiting your response" |
| Direct question | +10 | Subject or body contains "?" directed at recipient |
| Escalation signal | +20 | "following up", "second request", "still waiting", "reminder:" |
| Time-specific | +15 | Contains date/time like "by 5pm", "before Friday", "this week" |

**Threshold**: Urgency score >= 60

### 2. Response Needed

**Definition**: Emails requiring a reply but without immediate time pressure.

**Signals**:

| Signal | Weight | Detection Pattern |
|--------|--------|-------------------|
| Direct question | +20 | Question mark with personal pronoun "you", "your" |
| Action request | +15 | "Please", "Could you", "Would you", "Can you" + verb |
| Feedback request | +15 | "Thoughts?", "feedback", "review this", "your opinion" |
| Meeting/calendar | +10 | "Schedule", "availability", "meet", "call" |
| Single recipient | +10 | Only one person in To: field (not CC'd) |

**Threshold**: Score >= 30 AND < 60 urgency

### 3. FYI / Read Later

**Definition**: Informational emails not requiring direct action.

**Signals** (negative scoring for action):

| Signal | Weight | Detection Pattern |
|--------|--------|-------------------|
| CC'd recipient | -20 | Recipient in CC field, not To field |
| Newsletter format | -25 | "Unsubscribe", list headers, bulk sender |
| Notification | -20 | "notification", "alert", "automated", "noreply@" |
| Status update | -15 | "Update:", "Status:", "Report:", "Weekly" |
| Distribution list | -15 | To: contains "all@", "team@", "dept@" |

**Threshold**: Score < 30

### 4. Delegatable

**Definition**: Emails that can be forwarded to another team member.

**Signals**:

| Signal | Weight | Detection Pattern |
|--------|--------|-------------------|
| Department-specific | +20 | "Invoice", "billing" → finance; "bug", "issue" → engineering |
| Not addressed personally | +15 | Generic greeting or no greeting |
| External vendor | +10 | Domain not in organization list |
| Routine request | +15 | "Password reset", "access request", "equipment" |

**Delegation mapping**:
- Finance keywords: invoice, payment, billing, expense, receipt
- HR keywords: leave, vacation, benefits, onboarding
- IT keywords: access, password, system, software, hardware
- Legal keywords: contract, agreement, compliance, NDA

### 5. Archive

**Definition**: Low-value emails safe to archive without reading.

**Signals**:

| Signal | Weight | Detection Pattern |
|--------|--------|-------------------|
| Marketing/promo | +30 | "Sale", "offer", "% off", "limited time", promotional headers |
| Social media | +25 | LinkedIn, Twitter, Facebook notification patterns |
| Automated digest | +20 | "Daily digest", "weekly summary", aggregated content |
| Duplicate/thread | +15 | Same thread already classified higher |
| Old email | +10 | > 7 days old and still unread |

**Threshold**: Archive signals >= 30 AND no response signals

## Urgency Score Calculation

```python
def calculate_urgency_score(email: dict, config: dict) -> int:
    score = 0

    # VIP sender check
    if is_vip_sender(email['from'], config):
        score += 30

    # Deadline keywords
    deadline_patterns = [
        r'\bEOD\b', r'\bASAP\b', r'\burgent\b',
        r'\bdeadline\b', r'\bby tomorrow\b', r'\bimmediately\b'
    ]
    for pattern in deadline_patterns:
        if re.search(pattern, email['subject'] + email['snippet'], re.I):
            score += 25
            break

    # Reply-expected signals
    reply_patterns = [
        r'please reply', r'let me know', r'your thoughts\??',
        r'awaiting your', r'get back to me'
    ]
    for pattern in reply_patterns:
        if re.search(pattern, email['snippet'], re.I):
            score += 15
            break

    # Direct question
    if '?' in email['subject'] or re.search(r'\byou\b.*\?', email['snippet'], re.I):
        score += 10

    # Escalation signals
    escalation_patterns = [
        r'following up', r'second request', r'still waiting',
        r'reminder:', r'haven\'t heard'
    ]
    for pattern in escalation_patterns:
        if re.search(pattern, email['snippet'], re.I):
            score += 20
            break

    return min(score, 100)  # Cap at 100
```

## Time Estimation Rules

| Classification | Base Minutes | Adjustment Factors |
|----------------|--------------|-------------------|
| urgent-response | 10 | +5 if attachment, +5 if multiple questions |
| response-needed | 5 | +3 if meeting scheduling, +5 if document review |
| fyi-read | 1 | +2 if lengthy newsletter |
| delegatable | 2 | Forwarding time only |
| archive | 0 | Batch archive |

## VIP Configuration

VIP senders and domains should be configured based on:

1. **Executive team**: CEO, CFO, CTO, direct manager
2. **Key clients**: Primary customer contacts
3. **Important stakeholders**: Board members, investors
4. **Critical vendors**: Legal counsel, key partners

Example configuration:
```
--vip-domains "company.com,keyclient.org"
--vip-senders "ceo@company.com,boss@company.com,investor@vc.com"
```

## Signal Combination Rules

1. **Additive scoring**: Most signals stack (VIP + deadline = 55)
2. **Mutual exclusivity**: An email is classified into ONE category only
3. **Priority order**: urgent-response > response-needed > delegatable > fyi-read > archive
4. **Override rules**: VIP sender emails are never classified as archive

## Edge Cases

### Thread Handling
- Classify based on latest message in thread
- If thread has mixed signals, use highest urgency from recent 24h

### Auto-Replies
- Detect "Out of office", "Auto-reply" patterns
- Classify as FYI unless thread continuation

### Calendar Invites
- Treat as response-needed (accept/decline action)
- Boost urgency if meeting is within 24 hours
