# Error UX Best Practices

## Overview

This reference guide covers proven design principles, patterns, and practices for creating error experiences that minimize user frustration, support recovery, and maintain trust. Use this guide when designing improved error messages and recovery flows.

---

## Error Message Design Principles

### The 4-Part Error Message Framework

Every effective error message should address four questions:

1. **What happened?** (in user language, not technical jargon)
2. **Why did it happen?** (brief, relevant explanation)
3. **What should the user do next?** (specific, actionable step)
4. **What alternatives exist?** (if the primary path is blocked)

### Principle 1: Speak Human Language

**Do:**
- Use plain, conversational language the user understands
- Describe the outcome from the user's perspective
- Use terminology consistent with the rest of the product

**Don't:**
- Expose error codes, status codes, or technical identifiers as the primary message
- Use developer jargon (null, exception, timeout, 500, segfault)
- Reference internal system names or component identifiers

| Bad | Good |
|-----|------|
| "Error 500: Internal Server Error" | "We couldn't save your changes right now. Please try again in a moment." |
| "NullPointerException in PaymentService" | "We couldn't process your payment. Please check your card details and try again." |
| "ETIMEDOUT: connection timed out" | "The connection is taking longer than expected. Please check your internet and try again." |
| "Validation failed: field 'email' does not match pattern" | "Please enter a valid email address (e.g., name@example.com)." |

### Principle 2: Be Specific and Actionable

**Do:**
- Identify the exact field, item, or action that caused the error
- Provide a concrete next step the user can take immediately
- Include specific values, limits, or requirements when relevant

**Don't:**
- Use vague language ("something went wrong", "an error occurred")
- Assume the user knows what to fix
- Provide instructions that require technical knowledge

| Bad | Good |
|-----|------|
| "Invalid input" | "The phone number must be 10 digits. You entered 8 digits." |
| "File too large" | "Your file is 25MB. The maximum allowed size is 10MB. Try compressing the image or choosing a smaller file." |
| "Operation failed" | "We couldn't send your message because the recipient's inbox is full. Try again later or contact them through a different channel." |

### Principle 3: Offer Alternatives

When the primary path is blocked, suggest alternative routes to the user's goal.

**Examples:**
- Payment declined: "Try a different card, use PayPal, or contact your bank"
- File upload failed: "Try a smaller file, different format, or paste the content directly"
- Feature unavailable: "This feature is temporarily offline. You can still [alternative action]"
- Search no results: "Try different keywords, browse categories, or check spelling"

### Principle 4: Provide Reassurance

Address the user's likely concerns proactively, especially in high-stakes contexts.

**Reassurance Patterns:**
- **Financial errors**: "Your card has not been charged"
- **Data errors**: "Your draft has been saved automatically"
- **Account errors**: "Your account is secure. No unauthorized access was detected"
- **Submission errors**: "Your previous entries have been preserved"

---

## Tone and Voice Guidelines for Errors

### Core Tone Principles

| Principle | Description | Example |
|-----------|-------------|---------|
| **Empathetic** | Acknowledge the user's situation | "We understand this is frustrating" |
| **Humble** | Take responsibility, never blame the user | "We couldn't process..." not "You entered wrong..." |
| **Calm** | Use steady, measured language | Avoid exclamation marks, urgency words, ALL CAPS |
| **Helpful** | Focus on the solution, not the problem | Lead with what the user CAN do |
| **Honest** | Be transparent about the situation | "This usually resolves within 5 minutes" |

### Language Patterns to Avoid

| Avoid | Instead Use | Reason |
|-------|-------------|--------|
| "You entered an invalid..." | "The [field] needs to be..." | Blaming the user |
| "Error!", "Failed!", "Oops!" | "We couldn't complete..." | Alarming or trivializing |
| "Please try again later" (alone) | "Please try again in a few minutes. If this continues, contact support." | Vague, no timeframe, no escalation |
| "Contact your administrator" | "Contact our support team at [specific channel]" | Passing responsibility |
| "Unexpected error" | "Something didn't work as planned" | Technical jargon |

### Japanese Error Message Tone Guidelines

| Principle | Example |
|-----------|---------|
| Polite but not overly formal | "申し訳ありませんが、処理を完了できませんでした" |
| Action-oriented | "もう一度お試しいただくか、別の方法をお選びください" |
| Reassuring | "入力内容は保存されています" |
| Specific | "ファイルサイズが上限（10MB）を超えています。圧縮してから再度アップロードしてください" |

---

## Recovery Flow Design Patterns

### Pattern 1: Inline Validation (Prevent Errors Before Submission)

**When to use:** Form inputs, data entry, configuration settings

**Implementation:**
- Validate on blur (when user leaves a field), not on every keystroke
- Show validation state visually (green checkmark for valid, red indicator for invalid)
- Display the error message adjacent to the field, not in a separate location
- Keep the error message visible until the issue is corrected
- For complex validations (e.g., username availability), use async validation with loading indicator

**Best Practices:**
- Validate early, but not too early (do not show errors on empty required fields before the user has interacted)
- Group related validations (e.g., password strength meter instead of multiple separate rules)
- Preserve user input even when validation fails

### Pattern 2: Retry with Exponential Backoff (Transient Errors)

**When to use:** Network errors, server timeouts, rate limiting

**Implementation:**
- Offer an immediate manual retry button
- If auto-retrying, show progress and attempt count to the user
- Use exponential backoff: 1s, 2s, 4s, 8s, with max retry limit
- After max retries, show a clear failure message with alternative actions

**User Communication:**
- "Retrying... (Attempt 2 of 3)"
- "Connection restored. Your request has been completed."
- "We were unable to connect after several attempts. Please check your internet connection and try again."

### Pattern 3: Graceful Degradation (Partial Functionality)

**When to use:** Non-critical feature failures, third-party service outages

**Implementation:**
- Continue operating with reduced functionality rather than failing entirely
- Clearly communicate which features are temporarily unavailable
- Provide alternative ways to accomplish the task if possible
- Automatically restore full functionality when the underlying issue resolves

**Examples:**
- Image loading fails: Show placeholder with "Image unavailable" and a retry link
- Recommendation engine down: Show popular/recent items instead
- Real-time sync fails: Switch to periodic sync with notification

### Pattern 4: Draft Saving / Auto-Save (Prevent Data Loss)

**When to use:** Long forms, content creation, multi-step workflows

**Implementation:**
- Auto-save drafts at regular intervals (every 30-60 seconds)
- Save to local storage as a fallback when server save fails
- Show clear save status indicator ("Saved", "Saving...", "Unsaved changes")
- On error, explicitly confirm that the draft is preserved
- Provide "Restore draft" option on return

**User Communication:**
- "Your progress has been saved. You can continue where you left off."
- "We couldn't save to the server, but your work is saved locally on this device."

### Pattern 5: Undo Capability

**When to use:** Destructive actions, irreversible operations, batch operations

**Implementation:**
- Delay destructive actions with an undo window (5-10 seconds)
- Show a prominent undo button/toast after the action
- For batch operations, allow undoing the entire batch
- Consider soft-delete patterns (trash/archive) instead of hard-delete

---

## Error Page Design Patterns

### 404 - Not Found

**Design Guidelines:**
- Acknowledge the page doesn't exist without alarming the user
- Provide navigation options: home, search, popular pages, back to previous page
- Consider showing related content suggestions
- Include a "Report broken link" option

**Message Template:**
> We couldn't find the page you were looking for. It may have been moved or removed.
> You can [go back to the homepage], [search for what you need], or [browse our help center].

### 500 - Server Error

**Design Guidelines:**
- Apologize and take responsibility
- Provide a realistic timeframe if known
- Offer a retry option and alternative contact method
- Log the error ID for support reference (but keep it secondary, not the headline)

**Message Template:**
> Something went wrong on our end. We're working to fix it.
> Please try again in a few minutes. If the issue persists, contact our support team.
> Reference: #ERR-20240115-001

### Maintenance Page

**Design Guidelines:**
- Announce scheduled maintenance in advance via in-app notification
- Provide expected completion time
- Offer status page link for real-time updates
- Include alternative contact channels

### Timeout Page

**Design Guidelines:**
- Explain what was being processed when the timeout occurred
- Clarify whether the action may have partially completed
- Provide clear next steps (check status, retry, contact support)

---

## Emotional Design in Error States

### When Humor is Appropriate

- **Do use humor:** 404 pages, minor/cosmetic issues, beta feature glitches
- **Do NOT use humor:** Financial errors, data loss, security issues, checkout failures, account problems

**Guidelines for Humor:**
- Keep it light and brief (one line maximum)
- Never make the user feel silly for encountering the error
- Ensure the humor doesn't obscure the actual message or action
- Always pair humor with a helpful, actionable message below it

### Illustrations and Visual Design

- Use friendly, non-alarming illustrations for error states
- Maintain brand consistency in error page design
- Use color intentionally: red for critical, yellow/orange for warnings, blue for informational
- Ensure illustrations do not trivialize serious errors

### Reassurance Techniques

| Context | Reassurance Message |
|---------|---------------------|
| After failed payment | "Your card has not been charged. Please try again or use a different payment method." |
| After form submission error | "Don't worry, your entries have been saved. Just fix the highlighted fields and submit again." |
| After session timeout | "Your work has been auto-saved. Log back in to continue where you left off." |
| After failed file upload | "The upload didn't complete, but your original file is unchanged. You can try uploading again." |
| After account error | "Your account is secure. This error doesn't affect your data or settings." |

---

## Accessibility Considerations for Error Messages

### ARIA and Screen Reader Support

- Use `role="alert"` or `aria-live="assertive"` for critical error messages
- Use `aria-live="polite"` for non-critical validation messages
- Associate error messages with their fields using `aria-describedby`
- Ensure error messages are announced by screen readers when they appear
- Provide `aria-invalid="true"` on form fields with errors

### Visual Accessibility

- **Never rely on color alone** to indicate errors; always include text and/or icons
- Ensure error text meets WCAG 2.1 AA contrast ratio (minimum 4.5:1)
- Use icons with `alt` text (e.g., a warning triangle with alt="Error")
- Provide sufficient font size for error messages (minimum 14px)
- Ensure focus is moved to the first error on form submission failure

### Keyboard Navigation

- Error messages and retry buttons must be keyboard-focusable
- On form validation failure, set focus to the first invalid field
- Ensure dismiss/close buttons on error banners are reachable via keyboard
- Provide keyboard shortcuts for common recovery actions (e.g., Ctrl+Z for undo)

### Color-Blind Safe Error Design

| Element | Don't | Do |
|---------|-------|----|
| Error indicator | Red text only | Red text + error icon + "Error:" prefix |
| Success indicator | Green text only | Green text + checkmark icon + "Success:" prefix |
| Warning indicator | Yellow background only | Yellow background + warning icon + "Warning:" prefix |
| Field validation | Red border only | Red border + error icon + descriptive text below field |

---

## Error Message Examples by Category

### Validation Errors

| Scenario | Bad Message | Good Message |
|----------|-------------|--------------|
| Empty required field | "Required" | "Please enter your email address to continue" |
| Invalid email | "Invalid email" | "This doesn't look like a valid email. Please check for typos (e.g., name@example.com)" |
| Password too short | "Password invalid" | "Your password needs at least 8 characters. You've entered 5." |
| File type not supported | "Invalid file type" | "We support JPG, PNG, and PDF files. Your file is a .bmp. Please convert it or choose a different file." |

### System Errors

| Scenario | Bad Message | Good Message |
|----------|-------------|--------------|
| Server error | "Error 500" | "We're having trouble on our end. Please try again in a few minutes." |
| Database timeout | "Request timeout" | "This is taking longer than usual. We're working on it. Your data is safe." |
| Service unavailable | "503 Service Unavailable" | "We're temporarily down for maintenance. We expect to be back by [time]. Check our status page for updates." |

### Network Errors

| Scenario | Bad Message | Good Message |
|----------|-------------|--------------|
| Connection lost | "Network error" | "It looks like you're offline. Your changes will be saved and synced when you reconnect." |
| Timeout | "ETIMEDOUT" | "The connection is taking too long. Please check your internet and try again." |
| DNS failure | "DNS_PROBE_FINISHED_NXDOMAIN" | "We can't reach the server right now. Please check your internet connection or try again shortly." |

### Auth Errors

| Scenario | Bad Message | Good Message |
|----------|-------------|--------------|
| Wrong password | "Invalid credentials" | "The password you entered doesn't match our records. Please try again or reset your password." |
| Session expired | "401 Unauthorized" | "Your session has expired for security. Please log in again. Your recent work has been saved." |
| Permission denied | "403 Forbidden" | "You don't have access to this page. Contact your workspace admin to request access." |

### Business Logic Errors

| Scenario | Bad Message | Good Message |
|----------|-------------|--------------|
| Out of stock | "Error: item unavailable" | "This item just sold out. We'll notify you when it's back. Meanwhile, here are similar items." |
| Insufficient funds | "Transaction failed" | "Your payment couldn't be completed due to insufficient funds. Try a different payment method or adjust your order." |
| Duplicate submission | "Duplicate entry" | "It looks like you've already submitted this. Check your submissions to see the existing entry." |

### External Service Errors

| Scenario | Bad Message | Good Message |
|----------|-------------|--------------|
| Payment gateway down | "Payment service error" | "Our payment system is temporarily unavailable. Your cart is saved. Please try again in a few minutes or contact support." |
| API rate limit | "429 Too Many Requests" | "You've made a lot of requests in a short time. Please wait a moment before trying again." |
| Integration failure | "External service unavailable" | "We're having trouble connecting to [service name]. This feature may be limited until the connection is restored." |
