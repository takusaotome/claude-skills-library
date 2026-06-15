# Thread Analysis Patterns

Reference document for email thread analysis patterns, including action item extraction, status detection, and decision identification.

## Action Item Detection Patterns

### Commitment Patterns (First Person)

These patterns indicate the sender is committing to an action:

| Pattern | Example | Confidence |
|---------|---------|------------|
| `I will [verb]` | "I will send the report by Friday" | High |
| `I'll [verb]` | "I'll review this tomorrow" | High |
| `I'm going to [verb]` | "I'm going to schedule a meeting" | High |
| `Let me [verb]` | "Let me check with the team" | Medium |
| `I can [verb]` | "I can prepare the slides" | Medium |
| `I'll take care of` | "I'll take care of the deployment" | High |

### Request Patterns (Second Person)

These patterns indicate a request for someone else to act:

| Pattern | Example | Confidence |
|---------|---------|------------|
| `Can you [verb]` | "Can you review this document?" | High |
| `Could you [verb]` | "Could you send me the file?" | High |
| `Please [verb]` | "Please update the spreadsheet" | High |
| `Would you [verb]` | "Would you check the numbers?" | Medium |
| `[Name], please [verb]` | "John, please confirm the date" | High |
| `Action required:` | "Action required: approve the PR" | High |
| `TODO:` | "TODO: Update the config" | High |

### Deadline Patterns

Extract due dates from these patterns:

| Pattern | Example | Notes |
|---------|---------|-------|
| `by [date]` | "by Friday", "by EOD", "by March 15" | Explicit deadline |
| `before [date]` | "before the meeting" | Relative deadline |
| `within [timeframe]` | "within 2 days" | Duration-based |
| `due [date]` | "due next Monday" | Explicit |
| `ASAP` | "Please respond ASAP" | Urgent, no specific date |
| `EOD` / `COB` | "Need this by EOD" | Same-day deadline |
| `EOM` / `EOW` | "Complete by EOM" | End of month/week |

## Status Classification Patterns

### Resolution Indicators

High-confidence resolution signals:

```
- "This is resolved"
- "Issue has been fixed"
- "Problem solved"
- "Closing this thread"
- "Thanks for resolving"
- "Thank you for your help"
- "That worked!"
- "All set now"
- "We're good"
- "Done"
- "Completed"
```

### Escalation Indicators

Signals that a thread has been escalated:

```
- CC additions to management (detect title patterns: VP, Director, Manager, C-suite)
- "Escalating this to [name]"
- "Looping in [name] for visibility"
- "Adding [name] who can help"
- Subject line changes: "URGENT:", "ESCALATION:", "[ACTION REQUIRED]"
- "This needs immediate attention"
- "We need to escalate"
```

### Stale Thread Indicators

Conditions suggesting a thread is stale:

1. **Time-based**: No activity for 7+ business days
2. **Unanswered questions**: Last message contains `?` with no response
3. **Pending commitments**: "I will..." statements without follow-up
4. **Explicit delays**: "I'll get back to you", "Will follow up" without resolution

### Awaiting Response Indicators

The thread is waiting for someone to respond:

```
- Last message ends with a question
- Last message contains explicit request patterns
- Last message mentions "waiting for", "pending your"
- "Let me know"
- "Please advise"
- "Your thoughts?"
- "Any updates?"
```

## Decision Identification Patterns

### Explicit Decision Language

| Pattern | Example |
|---------|---------|
| `We decided to` | "We decided to go with option A" |
| `The decision is` | "The decision is to postpone" |
| `We've agreed to` | "We've agreed to the timeline" |
| `Final decision:` | "Final decision: approved" |
| `Going with` | "Going with the vendor proposal" |
| `Approved` | "Budget approved" |
| `Confirmed` | "Meeting time confirmed" |

### Implicit Decision Language

Lower confidence, requires context:

```
- "Let's do [action]"
- "We should [action]"
- "The plan is to [action]"
- "Moving forward with [action]"
- "Proceeding with [action]"
```

## Supersession Detection

### Contradiction Patterns

Identify when later messages invalidate earlier ones:

| Indicator | Example |
|-----------|---------|
| `Actually,` | "Actually, the deadline moved to Friday" |
| `Correction:` | "Correction: the amount is $5000, not $4000" |
| `Update:` | "Update: the meeting is now at 3pm" |
| `Disregard` | "Please disregard my previous message" |
| `Instead,` | "Instead, we'll use the new vendor" |
| `Changed to` | "The date has changed to next week" |
| `No longer` | "This is no longer required" |
| `Never mind` | "Never mind the previous request" |

### Timeline Supersession

When the same topic is discussed multiple times:
1. Track statements about specific entities (dates, amounts, decisions)
2. If later message addresses same entity with different value, mark earlier as superseded
3. Preserve both statements in output with supersession relationship

## Participant Role Detection

### Initiator Identification

The initiator is typically:
- Sender of the first message in thread
- Person who poses the original question/request
- May not be the most frequent participant

### Role Assignment Rules

| Role | Criteria |
|------|----------|
| **Initiator** | First message sender |
| **Primary Responder** | Most messages, or first to respond |
| **CC/Observer** | Only appears in CC, no direct messages |
| **Escalation Target** | Added mid-thread, especially if senior |
| **Subject Matter Expert** | Provides technical/detailed responses |

## Message Type Classification

Classify each message in the thread:

| Type | Indicators |
|------|------------|
| **Request** | Contains request patterns, questions |
| **Response** | Replies to request, provides information |
| **Decision** | Contains decision language |
| **Escalation** | Adds new recipients, urgent language |
| **Resolution** | Contains resolution indicators |
| **FYI/Update** | "Just wanted to let you know", "FYI:" |
| **Follow-up** | "Following up on", "Any updates?" |

## Language-Specific Notes

### Japanese Email Patterns

| Pattern | Meaning | Type |
|---------|---------|------|
| `ご確認お願いします` | Please confirm | Request |
| `対応します` | I will handle | Commitment |
| `完了しました` | Completed | Resolution |
| `お手数ですが` | Polite request | Request |
| `取り急ぎ` | Quick note | FYI |

### Formal vs Informal Detection

Formality affects interpretation:
- Formal: More likely to contain explicit commitments
- Informal: May use shorthand ("will do", "on it")
- Thread formality often set by initiator

## Edge Cases

### Multi-Thread Conversations

- Same participants may have multiple parallel threads
- Cross-reference by subject similarity and time overlap
- Maintain separate analysis but note relationships

### Forwarded Messages

- Detect "Forwarded message" / "Begin forwarded message" markers
- Attribute original content to original sender
- Track forwarding as a distinct event type

### Reply-All Chains

- Participant list may grow significantly
- Later participants may not have full context
- Track when participants join the thread
