# CX Error Evaluation Methodology

## Overview

This document defines the comprehensive evaluation methodology for assessing error scenarios from a customer experience (CX) perspective. The framework uses 6 evaluation axes, each scored on a 1-5 scale, with defined weights to produce a composite CX Score.

---

## Evaluation Axes

### Axis 1: Impact Severity (影響度) - Weight: 25%

Measures how severely the error disrupts the user's intended task or workflow.

| Score | Level | Description | Examples |
|-------|-------|-------------|----------|
| 5 | Critical | Complete task failure, data loss, no workaround exists | Payment processed but order not created; user data permanently deleted; form submission destroys draft |
| 4 | Major | Major disruption, partial task failure, workaround is difficult or unreliable | File upload fails after 30 min upload; checkout resets entire cart; multi-step form loses all progress |
| 3 | Moderate | Moderate disruption, workaround available but inconvenient | Search returns no results due to encoding issue; filter resets on page navigation; need to re-enter 3+ fields |
| 2 | Minor | Minor inconvenience, easy workaround readily apparent | Date picker rejects valid format; dropdown selection clears on scroll; cosmetic rendering glitch |
| 1 | Negligible | Cosmetic or trivial issue, user barely notices | Tooltip flickers briefly; icon misalignment on error state; loading spinner shows for 100ms extra |

**Scoring Guidelines:**
- Consider the user's primary goal and how far the error sets them back
- Account for data loss risk (unsaved work, partial submissions)
- Evaluate whether the user can complete their task at all
- Consider cumulative impact if the error occurs during a multi-step process

### Axis 2: Frequency (頻度) - Weight: 20%

Measures how often users encounter this error in practice.

| Score | Level | Description | Data Threshold |
|-------|-------|-------------|----------------|
| 5 | Very Frequent | Encountered by a large proportion of users regularly | >10% of sessions affected |
| 4 | Frequent | Common occurrence affecting many users | 5-10% of sessions affected |
| 3 | Occasional | Happens periodically, noticeable in aggregate | 1-5% of sessions affected |
| 2 | Rare | Infrequent, requires specific conditions | <1% of sessions affected |
| 1 | Very Rare | Isolated cases, extremely unlikely to occur | <0.1% of sessions or isolated reports |

**Data Sources for Frequency Assessment:**
- Error monitoring tools (Sentry, Datadog, New Relic)
- Server-side error logs and HTTP status code distribution
- Client-side error tracking and JavaScript exception reports
- Support ticket volume by error category
- User session replay data (FullStory, Hotjar)
- QA regression test failure rates

**Scoring Guidelines:**
- Use actual data whenever available; estimate only as a last resort
- Consider both absolute count and percentage of affected users
- Account for seasonal or event-driven spikes (e.g., sale periods, end of month)
- Distinguish between unique user frequency and total occurrence count

### Axis 3: Recovery Ease (復旧容易性, inverse) - Weight: 15%

Measures how difficult it is for the user to recover from the error and continue their task. This axis uses **inverse scoring**: higher score = harder to recover = worse CX.

| Score | Level | Description | Examples |
|-------|-------|-------------|----------|
| 5 | Unrecoverable | Must restart entire flow, contact support, or abandon task | Account locked with no self-service unlock; corrupted data requiring admin intervention; payment charged but service not provisioned |
| 4 | Difficult | Multiple non-obvious steps required, recovery path unclear | Must clear cache/cookies, re-authenticate, re-enter form from scratch; error persists across retries with no guidance |
| 3 | Moderate | Some steps required, recovery path somewhat clear | Retry after waiting, re-enter a few fields, navigate back and try alternative path |
| 2 | Easy | One retry or simple correction resolves the issue | Fix highlighted field and resubmit; click retry button; select different option |
| 1 | Automatic | System auto-recovers, user intervention minimal or unnecessary | Automatic retry succeeds transparently; graceful fallback to cached data; seamless redirect to alternative |

**Scoring Guidelines:**
- Evaluate the number of steps required to reach a recovered state
- Consider whether the recovery path is discoverable without external help
- Account for technical knowledge required (clearing cache vs. clicking a button)
- Factor in whether the user loses progress during recovery

### Axis 4: Message Quality (メッセージ品質, inverse) - Weight: 15%

Measures the quality and helpfulness of the current error message. This axis uses **inverse scoring**: higher score = poorer message quality = worse CX.

| Score | Level | Description | Examples |
|-------|-------|-------------|----------|
| 5 | Cryptic/Technical | Error code only, stack trace, or raw technical jargon | "Error 500: NullPointerException at line 342"; "SQLSTATE[HY000]"; "ERR_CONNECTION_REFUSED" |
| 4 | Vague | Generic message with no specific information | "Something went wrong"; "An error occurred"; "Operation failed"; "Please try again later" |
| 3 | Partial | Identifies the problem area but provides no actionable guidance | "Your file could not be uploaded"; "Payment was declined"; "Invalid input" |
| 2 | Good | Clear problem description with suggested corrective action | "Your file exceeds the 10MB limit. Please compress or choose a smaller file."; "Your session has expired. Please log in again to continue." |
| 1 | Excellent | Clear problem + specific action + alternative path + reassurance | "Your payment could not be processed. Your card was not charged. Please check your card details or try a different payment method. Need help? Contact support at..." |

**Evaluation Criteria:**
- **Clarity**: Is the message written in plain, user-friendly language?
- **Specificity**: Does it identify the exact problem?
- **Actionability**: Does it tell the user what to do next?
- **Alternatives**: Does it offer alternative paths if the primary action fails?
- **Reassurance**: Does it address potential user concerns (e.g., "your data is safe")?
- **Tone**: Is it empathetic and non-blaming?

### Axis 5: Emotional Impact (感情的影響) - Weight: 10%

Measures the emotional response the error is likely to trigger in the user.

| Score | Level | Description | Trigger Contexts |
|-------|-------|-------------|------------------|
| 5 | Anxiety/Fear | User fears data loss, financial impact, or security breach | Payment errors with unclear charge status; "account compromised" warnings; data deletion confirmations that appear as errors |
| 4 | Strong Frustration | User has invested significant effort that appears wasted | Long form submission fails; upload fails after extended wait; repeated failures on critical task |
| 3 | Moderate Frustration | Unexpected behavior disrupts flow | Feature works differently than expected; search returns wrong results; UI element behaves inconsistently |
| 2 | Mild Annoyance | Minor inconvenience, quickly resolved | Extra click required; minor delay; cosmetic issue during error state |
| 1 | Neutral | Error handled gracefully, user barely reacts | Smooth fallback; helpful guidance; quick resolution with no lost progress |

**Emotional Impact Amplifiers:**
- **Financial context**: Errors involving money amplify anxiety (2x emotional weight)
- **Time investment**: Errors after lengthy input amplify frustration
- **Repetition**: Same error occurring repeatedly compounds negative emotion
- **Urgency**: Errors during time-sensitive tasks (deadlines, limited offers) intensify impact
- **Public context**: Errors during presentations or shared screens increase embarrassment

### Axis 6: Business Cost (ビジネスコスト) - Weight: 15%

Measures the direct and indirect business impact of the error.

| Score | Level | Description | Cost Indicators |
|-------|-------|-------------|-----------------|
| 5 | Critical | Direct revenue loss, measurable customer churn | Checkout abandonment; subscription cancellation triggered by error; lost transactions |
| 4 | High | High support cost, requires engineering escalation | Tier 2/3 support tickets; engineering hotfix required; SLA breaches |
| 3 | Moderate | Moderate support cost, customer complaints | Tier 1 support tickets; negative reviews mentioning the error; social media complaints |
| 2 | Low | Low support cost, users self-resolve | Occasional inquiry; FAQ page visit spike; minor friction in funnel |
| 1 | Negligible | No measurable business impact | No support tickets; no funnel impact; no complaints |

**Business Cost Assessment Factors:**
- Support ticket volume and average handling time per ticket
- Customer acquisition cost (CAC) at risk due to churn
- Revenue per transaction at risk
- Brand reputation impact (social media, review sites)
- Engineering cost for hotfixes and workarounds
- Opportunity cost of delayed feature work

---

## Error Classification Taxonomy

### Classification Categories

| Category | Code | Description | Typical Triggers |
|----------|------|-------------|------------------|
| Validation | VAL | Input validation failures | Format errors, required fields, range violations, type mismatches |
| System | SYS | Internal system errors | Server crashes, database failures, memory exhaustion, disk full |
| Network | NET | Network-related failures | Timeouts, connection drops, DNS failures, SSL errors |
| Auth | AUTH | Authentication/Authorization | Login failure, session expiry, insufficient permissions, token invalid |
| Business Logic | BIZ | Business rule violations | Insufficient balance, item out of stock, duplicate submission, limit exceeded |
| External | EXT | Third-party service failures | Payment gateway errors, API rate limits, integration timeouts, data sync failures |

### Classification Decision Tree

```
Error Occurred
├── Is it related to user input?
│   └── YES → Validation (VAL)
├── Is it an authentication or permission issue?
│   └── YES → Auth (AUTH)
├── Is it a network connectivity issue?
│   └── YES → Network (NET)
├── Is it a third-party service issue?
│   └── YES → External (EXT)
├── Is it a business rule violation?
│   └── YES → Business Logic (BIZ)
└── Otherwise → System (SYS)
```

---

## User Journey Stage Mapping

### Journey Stages

| Stage | Description | Common Error Types | CX Sensitivity |
|-------|-------------|--------------------|----------------|
| Discovery | Browsing, searching, exploring | NET, SYS | Medium - user may leave silently |
| Onboarding | Registration, initial setup, first-time experience | VAL, AUTH | High - first impression is critical |
| Core Task | Primary feature usage, main workflow | All types | Very High - user is invested in the task |
| Checkout | Purchase, submission, finalization | VAL, BIZ, EXT | Critical - direct revenue impact |
| Support | Help access, account management, settings | AUTH, SYS | High - user is already frustrated |

### Stage-Specific Considerations

**Discovery Stage:**
- Users have low commitment; errors may cause silent abandonment
- Focus on graceful degradation and fallback content
- Search errors should still show partial or suggested results

**Onboarding Stage:**
- First impressions set expectations for the entire product
- Validation errors must be extremely clear and helpful
- Progressive disclosure: do not overwhelm with all requirements upfront

**Core Task Stage:**
- Users have invested time and effort; errors are costly
- Draft saving and auto-recovery are essential
- Partial completion should be preserved whenever possible

**Checkout Stage:**
- Highest revenue impact; every error is a potential lost transaction
- Payment errors require explicit charge status communication
- Alternative payment methods should be prominently offered

**Support Stage:**
- User is already in a problem-solving mindset; additional errors compound frustration
- Self-service recovery paths reduce support load
- Clear escalation paths must be available

---

## Data Collection Guidance

### Quantitative Data Sources

1. **Error Monitoring Platforms**: Sentry, Bugsnag, Datadog, New Relic
   - Error frequency, stack traces, affected user counts
2. **Analytics Platforms**: Google Analytics, Mixpanel, Amplitude
   - Funnel drop-off rates correlated with error events
3. **Support Systems**: Zendesk, Intercom, Freshdesk
   - Ticket volume, categories, resolution time, customer satisfaction
4. **APM Tools**: Application Performance Monitoring
   - Response times, error rates, throughput by endpoint

### Qualitative Data Sources

1. **User Interviews**: Direct feedback on error experiences
2. **Session Replays**: FullStory, Hotjar, LogRocket
3. **Support Transcripts**: Common complaints and frustration indicators
4. **App Store / Review Site Reviews**: Mentions of specific error experiences
5. **Social Media Monitoring**: Complaints and feedback on public channels

### Data Collection Best Practices

- Collect at least 2 weeks of data for frequency assessment (account for weekly patterns)
- Segment data by user type (new vs. returning, free vs. paid)
- Track error sequences (errors that commonly co-occur or cascade)
- Record the timestamp and context of each error occurrence
- Preserve user journey state at the time of error for recovery analysis
