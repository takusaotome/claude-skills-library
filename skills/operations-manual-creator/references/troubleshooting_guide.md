# Troubleshooting Guide Methodology（トラブルシューティングガイド方法論）

## Purpose

This guide defines the methodology and format for creating troubleshooting sections in operations manuals. It covers Symptom-Cause-Resolution tables, decision trees, common error patterns, and escalation procedures.

---

## 1. Symptom-Cause-Resolution Table Format

### Standard Table Structure

Every troubleshooting entry follows this format:

| Field | Description | Example |
|-------|------------|---------|
| ID | Unique identifier (T-001, T-002...) | T-001 |
| Symptom | What the user observes (exact error message or behavior) | "Login failed: Invalid credentials" message appears |
| Probable Cause | Most likely reason for the symptom | User entered incorrect password or account is locked |
| Resolution | Step-by-step fix instructions | 1. Verify username spelling. 2. Click "Forgot Password" link. 3. Follow reset instructions. |
| Related OP | Link to the relevant operation procedure | OP-001 (Login) |
| Severity | Impact level: Critical / High / Medium / Low | Medium |

### Full Table Template

```markdown
| ID | Symptom | Probable Cause | Resolution | Related OP | Severity |
|----|---------|---------------|------------|------------|----------|
| T-001 | {Exact error message or behavior} | {Root cause description} | {Numbered resolution steps} | OP-{xxx} | {Critical/High/Medium/Low} |
```

### Severity Definitions

| Severity | Definition | Response Time Target |
|----------|-----------|---------------------|
| Critical | System is unusable, no workaround exists | Immediate (< 1 hour) |
| High | Major feature is broken, workaround exists but is impractical | Same business day |
| Medium | Feature is impaired, reasonable workaround exists | Within 2 business days |
| Low | Minor inconvenience, cosmetic issue | Next scheduled maintenance |

### Writing Effective Symptom Descriptions

**Good symptoms** are specific and observable:
- "Error message 'Session expired. Please log in again.' appears after 30 minutes of inactivity"
- "The Save button is grayed out and cannot be clicked"
- "The exported CSV file contains garbled characters in Japanese text columns"

**Bad symptoms** are vague:
- "It doesn't work" (What doesn't work?)
- "There's an error" (What error?)
- "The system is slow" (How slow? On which screen?)

### Writing Effective Resolution Steps

1. Start with the most common/simplest fix
2. Use numbered steps for multi-step resolutions
3. Include verification: "After completing these steps, confirm that..."
4. Provide alternative resolutions if the first does not work
5. End with escalation instruction if self-service resolution fails

**Example:**

```markdown
**Resolution for T-003 (CSV export garbled characters):**

1. Open the exported CSV file in a text editor (e.g., Notepad++, VS Code)
2. Verify the file encoding by checking the status bar (should show UTF-8)
3. If the encoding is not UTF-8:
   a. In Excel, use Data > From Text/CSV import
   b. Set File Origin to "65001: Unicode (UTF-8)"
   c. Click Load
4. If the issue persists, re-export from the system:
   a. Navigate to the export screen
   b. Select "UTF-8 with BOM" from the encoding dropdown
   c. Click Export
5. Verify: Open the new file and confirm Japanese characters display correctly
6. If still unresolved, escalate to L2 (Helpdesk) with the original file attached
```

---

## 2. Decision Tree Methodology

### When to Use Decision Trees

Use decision trees for complex troubleshooting scenarios where:
- Multiple symptoms lead to different root causes
- The resolution depends on a sequence of diagnostic checks
- Simple table format cannot capture the branching logic

### Decision Tree Format (Markdown)

Use indented text with arrows to represent branches:

```markdown
### Decision Tree: Login Failures

Start: User cannot log in
  │
  ├── Is the login page visible?
  │     ├── NO → Check network connection
  │     │         ├── VPN connected? → Reconnect VPN and retry
  │     │         └── Internet working? → Contact IT for network support (L2)
  │     │
  │     └── YES → Continue diagnosis
  │
  ├── What error message appears?
  │     ├── "Invalid credentials"
  │     │     ├── Caps Lock on? → Disable Caps Lock and retry
  │     │     ├── Correct username? → Verify with admin and retry
  │     │     └── Still failing? → Reset password via "Forgot Password" link
  │     │
  │     ├── "Account locked"
  │     │     └── Contact system administrator to unlock account (L2)
  │     │
  │     ├── "Session expired"
  │     │     └── Clear browser cache and cookies, then retry login
  │     │
  │     └── No error message (blank screen)
  │           ├── Try a different browser → If works, clear original browser cache
  │           └── Try incognito mode → If works, disable browser extensions
  │
  └── If none of the above resolves the issue → Escalate to L3 (Engineering)
```

### Decision Tree Design Principles

1. Start with the most observable symptom
2. Ask binary (yes/no) or categorical questions at each node
3. Keep tree depth to 4 levels maximum
4. Provide a resolution at every leaf node
5. Always include an escalation path as the final fallback
6. Order branches from most common to least common (left to right or top to bottom)

---

## 3. Common Error Patterns in Business Systems

### 3.1 Authentication and Authorization Errors

| ID | Symptom | Probable Cause | Resolution |
|----|---------|---------------|------------|
| T-AUTH-01 | "Invalid credentials" on login | Incorrect password or username | Verify credentials, use password reset if needed |
| T-AUTH-02 | "Account locked" after multiple attempts | Exceeded login attempt limit (typically 5) | Wait 30 minutes for auto-unlock, or contact admin |
| T-AUTH-03 | "Access denied" on specific feature | Insufficient role or permission | Verify user role, request permission from admin |
| T-AUTH-04 | "Session expired" during operation | Session timeout due to inactivity | Log in again; save work frequently |
| T-AUTH-05 | SSO redirect loop | SAML/OIDC configuration mismatch | Clear browser cookies, try incognito mode, contact IT |
| T-AUTH-06 | "Token expired" API error | Authentication token has expired | Log out and log in again to refresh token |

### 3.2 Timeout and Connection Errors

| ID | Symptom | Probable Cause | Resolution |
|----|---------|---------------|------------|
| T-CONN-01 | "Request timed out" on form submit | Large data payload or slow server | Reduce data volume, retry during off-peak hours |
| T-CONN-02 | "Connection refused" error | Server is down or maintenance | Check system status page, wait and retry |
| T-CONN-03 | Spinner never stops loading | Network interruption or JavaScript error | Refresh the page (F5), check network connection |
| T-CONN-04 | "502 Bad Gateway" or "503 Service Unavailable" | Server overload or deployment in progress | Wait 5 minutes and retry |
| T-CONN-05 | Intermittent connection drops | VPN instability or firewall blocking | Switch to wired connection, reconnect VPN |

### 3.3 Data Validation Errors

| ID | Symptom | Probable Cause | Resolution |
|----|---------|---------------|------------|
| T-VAL-01 | "Required field" error on submit | Mandatory field left blank | Fill in all fields marked with asterisk (*) |
| T-VAL-02 | "Invalid format" on date field | Date format mismatch (YYYY/MM/DD vs MM/DD/YYYY) | Use the date picker instead of typing manually |
| T-VAL-03 | "Value out of range" on numeric field | Number exceeds allowed minimum/maximum | Check field constraints and enter valid value |
| T-VAL-04 | "Duplicate record" on save | Record with same unique key already exists | Search for existing record and update instead |
| T-VAL-05 | Special characters cause errors | Input contains prohibited characters | Remove special characters (<, >, &, quotes) |

### 3.4 Permission-Related Issues

| ID | Symptom | Probable Cause | Resolution |
|----|---------|---------------|------------|
| T-PERM-01 | Menu item is not visible | User role does not include this feature | Confirm required role with admin, request role change |
| T-PERM-02 | Button is grayed out (disabled) | Record is locked or user lacks edit permission | Check record owner/status, request unlock from owner |
| T-PERM-03 | "Insufficient privileges" on delete | Delete permission not granted for this role | Request elevated permission or ask an admin to perform |
| T-PERM-04 | Cannot see other department's data | Data visibility restricted by sharing rules | Contact admin to adjust sharing settings if needed |

### 3.5 Browser and Device Compatibility Issues

| ID | Symptom | Probable Cause | Resolution |
|----|---------|---------------|------------|
| T-BROWSER-01 | Layout is broken or misaligned | Unsupported browser or outdated version | Use a supported browser (Chrome, Edge, Firefox latest) |
| T-BROWSER-02 | PDF does not download | Pop-up blocker preventing download | Allow pop-ups for the application URL |
| T-BROWSER-03 | File upload fails | File exceeds size limit or unsupported format | Check allowed file types and size limits |
| T-BROWSER-04 | Copy-paste not working | Browser security restrictions | Use Ctrl+Shift+V for plain text paste, or type manually |
| T-BROWSER-05 | Mobile layout unusable | Application not optimized for mobile | Use desktop or tablet device for this operation |

---

## 4. Escalation Procedures

### Three-Tier Escalation Model

```
L1: Self-Service (User)
  ↓ If unresolved
L2: Helpdesk / Support Team
  ↓ If unresolved
L3: Engineering / Development Team
```

### L1: Self-Service（ユーザー自己解決）

**Scope**: Issues that can be resolved by the user using this manual.

**Actions**:
1. Look up the symptom in the Troubleshooting table
2. Follow the resolution steps
3. If the decision tree is available, follow it to a resolution
4. Retry the operation after applying the fix
5. If still unresolved after 2 attempts, escalate to L2

**Typical L1 Issues**:
- Password reset
- Browser cache clearing
- Incorrect data entry correction
- Session timeout re-login
- Format/encoding adjustments

### L2: Helpdesk / Support Team（ヘルプデスク）

**Scope**: Issues beyond user self-service capability, requiring system access or configuration changes.

**Contact Information Template**:

```markdown
| Item | Details |
|------|---------|
| Contact Method | {Email / Phone / Chat / Ticket System} |
| Email | {helpdesk@example.com} |
| Phone | {03-XXXX-XXXX} |
| Ticket URL | {https://support.example.com/} |
| Business Hours | {Mon-Fri 9:00-18:00 JST} |
| After-Hours | {Emergency line: 090-XXXX-XXXX} |
| Expected Response | {Within 4 business hours} |
```

**Typical L2 Issues**:
- Account unlock / password administration
- Permission and role changes
- Data correction (records locked by system)
- Configuration changes
- Bug report triage

### L3: Engineering / Development Team（開発チーム）

**Scope**: System defects, infrastructure issues, or problems requiring code changes.

**Escalation Criteria** (any one triggers L3):
- System is completely down for all users
- Data corruption or loss has occurred
- Security vulnerability has been identified
- The issue cannot be reproduced or diagnosed by L2
- A code-level fix or database intervention is required

**Typical L3 Issues**:
- System outages
- Database recovery
- Security incidents
- Performance degradation (server-side)
- Integration failures with external systems

---

## 5. Information Collection Before Escalation

### Required Information Checklist

Before escalating from L1 to L2 (or L2 to L3), collect the following:

```markdown
## Escalation Report

### Basic Information
- **Reporter Name**: {Your name}
- **Reporter Contact**: {Email or phone}
- **Date/Time of Issue**: {YYYY-MM-DD HH:MM timezone}
- **User ID / Account**: {Your user ID}
- **User Role**: {Admin / Editor / Viewer / etc.}

### Environment
- **System/Application**: {Application name and version}
- **URL**: {The URL where the issue occurred}
- **Browser**: {Chrome 120 / Edge 120 / Firefox 121 / Safari 17}
- **OS**: {Windows 11 / macOS 14 / etc.}
- **Network**: {Office LAN / VPN / Remote / Mobile}

### Issue Description
- **Summary**: {One-line summary of the issue}
- **Symptom**: {Exact error message or behavior observed}
- **Steps to Reproduce**:
  1. {Step 1}
  2. {Step 2}
  3. {Step 3}
- **Expected Behavior**: {What should have happened}
- **Actual Behavior**: {What actually happened}
- **Frequency**: {Always / Intermittent / One-time}

### Self-Service Attempted
- **Troubleshooting steps tried**: {List what you already tried}
- **Result of each attempt**: {What happened when you tried}

### Attachments
- [ ] Screenshot of the error
- [ ] Browser console log (F12 > Console tab)
- [ ] Network log if applicable (F12 > Network tab)
- [ ] Related data export if applicable
```

### Quick Collection Guide

For users unfamiliar with technical collection:

1. **Screenshot**: Press `Print Screen` (Windows) or `Command + Shift + 4` (Mac)
2. **Error message**: Copy the exact text of any error message
3. **Timestamp**: Note the exact time when the issue occurred
4. **URL**: Copy the URL from the browser address bar
5. **Browser console** (if requested by L2):
   - Press `F12` to open Developer Tools
   - Click the **Console** tab
   - Screenshot any red error messages

---

## 6. FAQ Section Template

### FAQ Format

```markdown
## FAQ（よくある質問）

### Q1: {Question in natural language}

**A**: {Answer with specific steps or information}

> [!NOTE]
> {Additional context or tip if needed}

---

### Q2: {Question}

**A**: {Answer}

---
```

### Recommended FAQ Categories

1. **Account and Access**: Login, password, permissions
2. **Data Entry**: Input rules, formats, limitations
3. **Output and Reports**: Exports, prints, downloads
4. **Performance**: Speed, loading times, timeouts
5. **Mobile and Remote Access**: VPN, mobile browser, offline
6. **General**: Business rules, terminology, process questions

### Writing Effective FAQs

- Write questions in the user's voice: "How do I reset my password?" not "Password Reset Procedure"
- Keep answers concise (3-5 sentences)
- Link to the relevant procedure (OP-ID) for detailed steps
- Include the most frequently asked questions first (top 10 from helpdesk data)
- Review and update FAQs quarterly based on new helpdesk tickets

---

## 7. Troubleshooting Section Assembly

### Recommended Section Order

```markdown
## 8. Troubleshooting（トラブルシューティング）

### 8.1 Common Issues and Resolutions
{Symptom-Cause-Resolution table, organized by category}

### 8.2 Decision Trees
{Visual decision trees for complex scenarios}

### 8.3 Escalation Procedure
{L1 → L2 → L3 escalation path with contact information}

### 8.4 Information Collection Guide
{What to collect before escalating}

## 9. FAQ（よくある質問）
{Categorized FAQ entries}
```

### Cross-Referencing

- Every troubleshooting entry (T-xxx) should reference the related operation (OP-xxx)
- Every operation procedure should reference potential troubleshooting entries
- FAQs should link to both operations and troubleshooting entries

### Maintenance

- Review troubleshooting content quarterly
- Add new entries based on helpdesk ticket analysis
- Remove entries for issues that have been permanently fixed
- Update resolution steps when system updates change the UI or behavior
