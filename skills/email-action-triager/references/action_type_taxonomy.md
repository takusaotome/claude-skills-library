# Action Type Taxonomy

## Overview

This taxonomy defines the classification system for email actions. Each incoming email is assigned exactly one primary action type based on content analysis and contextual signals.

## Action Types

### RESPOND

**Definition**: Email requires a direct reply from you.

**Detection Signals:**
- Direct question addressed to you
- Request for information you possess
- Explicit "please reply" or "let me know"
- You are sole recipient (To: field only)
- Thread waiting for your response

**Sub-categories:**
| Sub-type | Description | Response Template |
|----------|-------------|-------------------|
| Answer Question | Factual question asked | Provide direct answer |
| Provide Opinion | Seeking your input/preference | Share perspective with reasoning |
| Confirm/Deny | Yes/no decision needed | Clear affirmation/rejection |
| Acknowledge | Sender expects confirmation | Brief "received" or "understood" |

**Examples:**
- "What time works for you tomorrow?"
- "Can you share the Q3 report?"
- "Do you approve this approach?"

---

### REVIEW

**Definition**: Email contains content requiring your evaluation, not just a reply.

**Detection Signals:**
- Document attachment (PDF, DOCX, XLSX)
- "Please review" or "for your approval"
- Draft or proposal shared
- Sign-off or approval workflow
- Legal or compliance documents

**Sub-categories:**
| Sub-type | Description | Action |
|----------|-------------|--------|
| Approve/Reject | Formal approval needed | Decision + feedback |
| Provide Feedback | Input on draft | Detailed comments |
| Fact Check | Verify accuracy | Confirm or correct |
| Risk Assessment | Evaluate for issues | Risk analysis |

**Examples:**
- "Please review the attached contract before signing"
- "Draft proposal for your feedback"
- "PR ready for code review"

---

### DELEGATE

**Definition**: Email should be forwarded to another person who is better suited to handle it.

**Detection Signals:**
- Technical content outside your expertise
- Operational request for another team
- Administrative task
- Sender misrouted email
- CC'd stakeholder could own response

**Delegation Decision Matrix:**
| Content Type | Delegate To | Condition |
|--------------|-------------|-----------|
| Technical/Engineering | Tech Lead/Developer | Code, infrastructure, bugs |
| Financial/Accounting | Finance Team | Budget, expenses, invoices |
| HR/Personnel | HR Manager | Hiring, benefits, policies |
| Customer Support | Support Team | Product questions, issues |
| Scheduling/Logistics | Admin/EA | Meeting coordination |
| Legal/Compliance | Legal Team | Contracts, policies |

**Delegation Templates:**
```
Standard: "Looping in [NAME] who can better assist with this."

With Context: "Forwarding to [NAME] on the [TEAM] team.
Adding context: [BRIEF SUMMARY]"

Urgent: "[NAME] - could you please prioritize this?
[SENDER] needs [ACTION] by [DEADLINE]."
```

---

### SCHEDULE

**Definition**: Email involves calendar coordination or event planning.

**Detection Signals:**
- Meeting invitation (ICS attachment)
- Time/date discussion
- "When are you available?"
- Conference/event registration
- Recurring meeting changes

**Sub-categories:**
| Sub-type | Action Required |
|----------|-----------------|
| Accept Invite | Confirm attendance |
| Decline Invite | Reject with reason |
| Propose Alternative | Suggest new time |
| Coordinate | Find mutual availability |
| Reschedule | Move existing event |

**Response Patterns:**
- Check calendar conflicts before accepting
- Provide alternative times when declining
- Include timezone when coordinating cross-region

---

### TASK

**Definition**: Email creates an action item that requires work beyond email response.

**Detection Signals:**
- Explicit task assignment
- Project deliverable request
- Multi-step work required
- External system action needed
- Non-email outcome expected

**Task Extraction:**
| Signal | Task Created |
|--------|--------------|
| "Please prepare..." | Create document/presentation |
| "Update the..." | Modify existing system/document |
| "Research..." | Investigation task |
| "Schedule..." | Calendar task |
| "Call..." | Phone/communication task |

**Task Properties to Extract:**
- Title (from subject/request)
- Description (from body)
- Due date (detected deadline)
- Project association
- Priority (from urgency score)
- Dependencies (mentioned blockers)

---

### FYI

**Definition**: Email is informational only; no action expected from you.

**Detection Signals:**
- CC'd (not in To: field)
- Newsletter/digest format
- "For your information"
- "No action required"
- Team update/announcement
- External notification (not personalized)

**Sub-categories:**
| Sub-type | Recommended Handling |
|----------|---------------------|
| Team Update | Skim, archive |
| Newsletter | Batch read weekly |
| CC'd Thread | Monitor, archive |
| Announcement | Read, acknowledge if needed |
| Report/Metrics | Review at designated time |

**FYI Processing Rules:**
1. Quick scan for unexpected action items
2. Archive immediately if pure informational
3. Star/flag if may need reference later
4. Unsubscribe from unwanted newsletters

---

### ARCHIVE

**Definition**: Email requires no action and no reading; can be immediately archived.

**Detection Signals:**
- Automated notification
- Build/deploy status
- Subscription confirmation
- Social media alerts
- Marketing/promotional
- Out-of-office replies

**Auto-Archive Patterns:**
```yaml
archive_patterns:
  - from: "noreply@*"
    subject_not_contains: ["error", "fail", "urgent"]
  - from: "*@notifications.*"
  - subject_contains: ["unsubscribe", "newsletter"]
  - from: "mailer-daemon@*"
```

**Exception Handling:**
- Error notifications → Escalate to REVIEW
- Security alerts → Escalate to CRITICAL RESPOND
- Unsubscribe confirmations → Verify, then archive

---

## Action Type Decision Flow

```
                    ┌─────────────────┐
                    │  Incoming Email │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Is Automated?   │
                    └────────┬────────┘
                      Yes    │    No
                    ┌────────┴────────┐
           ┌────────▼───────┐ ┌───────▼────────┐
           │    ARCHIVE     │ │ You in To:?    │
           └────────────────┘ └───────┬────────┘
                               Yes    │    No
                             ┌────────┴────────┐
                    ┌────────▼────────┐ ┌──────▼───────┐
                    │ Question to you?│ │    FYI       │
                    └────────┬────────┘ └──────────────┘
                      Yes    │    No
                    ┌────────┴────────┐
           ┌────────▼────────┐ ┌──────▼───────────┐
           │    RESPOND      │ │ Review request?  │
           └─────────────────┘ └───────┬──────────┘
                                Yes    │    No
                              ┌────────┴────────┐
                     ┌────────▼───────┐ ┌───────▼────────┐
                     │    REVIEW      │ │ Meeting invite?│
                     └────────────────┘ └───────┬────────┘
                                         Yes    │    No
                                       ┌────────┴────────┐
                              ┌────────▼───────┐ ┌───────▼────────┐
                              │   SCHEDULE     │ │ Delegatable?   │
                              └────────────────┘ └───────┬────────┘
                                                  Yes    │    No
                                                ┌────────┴────────┐
                                       ┌────────▼───────┐ ┌───────▼────────┐
                                       │   DELEGATE     │ │    TASK        │
                                       └────────────────┘ └────────────────┘
```

## Priority Matrix by Action Type

| Action Type | Default Priority | Typical Response Time |
|-------------|-----------------|----------------------|
| RESPOND (VIP) | CRITICAL | < 1 hour |
| RESPOND (External) | HIGH | < 4 hours |
| REVIEW (Approval) | HIGH | < 24 hours |
| SCHEDULE | MEDIUM | < 24 hours |
| DELEGATE | MEDIUM | < 4 hours (forward) |
| TASK | Varies | By deadline |
| FYI | LOW | Batch process |
| ARCHIVE | MINIMAL | Immediate |

## Conflict Resolution

When multiple action types could apply:

1. **Security concerns override all** → REVIEW immediately
2. **VIP sender elevates priority** → Use sender's preferred type
3. **Explicit deadline wins** → Use most time-sensitive type
4. **When unclear** → Default to RESPOND to clarify
