# Procedure Writing Guide（手順記述ガイド）

## Purpose

This guide defines the STEP format for writing clear, unambiguous, and actionable operating procedures for business systems. All procedures in the operations manual MUST follow the conventions described here.

---

## 1. The STEP Format

Every procedural step is described using four dimensions:

| Dimension | Abbreviation | Question Answered | Description |
|-----------|-------------|-------------------|-------------|
| Specific | S | What to do? | The exact action the user must perform |
| Target | T | Where to do it? | The specific UI element or system component |
| Expected | E | What happens next? | The observable result after performing the action |
| Proceed | P | How to continue? | Confirmation of success and transition to next step |

### 1.1 Specific (S) - Action Description

Use **precise action verbs** to describe what the user must do. Avoid vague language.

#### Recommended Verbs (Japanese / English)

| Japanese | English | Context |
|----------|---------|---------|
| クリックする | Click | Mouse single-click on a button, link, or icon |
| ダブルクリックする | Double-click | Open an item, edit in-place |
| 右クリックする | Right-click | Open context menu |
| 入力する | Enter / Type | Type text into a field |
| 選択する | Select | Choose from a dropdown, radio button, or list |
| チェックを入れる | Check | Enable a checkbox |
| チェックを外す | Uncheck | Disable a checkbox |
| ドラッグする | Drag | Move an element by click-and-hold |
| スクロールする | Scroll | Scroll the page or panel |
| 切り替える | Toggle | Switch between ON/OFF states |
| アップロードする | Upload | Attach a file |
| ダウンロードする | Download | Save a file locally |
| コピーする | Copy | Copy text or data |
| 貼り付ける | Paste | Paste copied content |
| 確認する | Verify / Confirm | Check that a condition is met |
| 待機する | Wait | Wait for processing to complete |
| ログインする | Log in | Authenticate with credentials |
| ログアウトする | Log out | End the session |

#### Rules for Specific

- Use ONE verb per step (avoid "click and then type..." as a single step)
- Use imperative mood: "Click the Save button" not "You should click the Save button"
- Be explicit about the action type: "Type `admin@example.com`" not "Enter the email"
- For keyboard shortcuts, use the format: `Ctrl + S` or `Command + S (Mac)`
- Quantify when possible: "Wait approximately 5 seconds" not "Wait a moment"

### 1.2 Target (T) - UI Element Identification

Identify the exact UI element the user must interact with.

#### Navigation Path Format

Use the `>` separator for menu navigation:

```
Main Menu > Sub Menu > Menu Item
```

Examples:
- `Settings > User Management > Add User`
- `File > Export > CSV Format`
- `ダッシュボード > レポート > 月次売上レポート`

#### Element Identification Rules

1. **Use the exact label text** as displayed on screen (case-sensitive)
2. **Bold the element name**: Click the **Save** button
3. **Include the element type**: Click the **Save** button, Select from the **Department** dropdown
4. **Specify location when ambiguous**: Click the **Delete** button in the upper-right corner of the dialog
5. **Use field labels for input fields**: In the **Email Address** field, type...

#### Element Type Vocabulary

| Element Type | Japanese | Use For |
|-------------|----------|---------|
| Button | ボタン | Clickable action buttons |
| Link | リンク | Text hyperlinks |
| Dropdown | ドロップダウン | Select/combobox elements |
| Checkbox | チェックボックス | Boolean toggle boxes |
| Radio button | ラジオボタン | Single-selection option buttons |
| Text field | テキストフィールド | Single-line input |
| Text area | テキストエリア | Multi-line input |
| Tab | タブ | Tab navigation elements |
| Icon | アイコン | Clickable icons |
| Menu | メニュー | Navigation menus |
| Dialog | ダイアログ | Modal/popup windows |
| Panel | パネル | Collapsible/expandable sections |
| Toggle switch | トグルスイッチ | ON/OFF switches |

### 1.3 Expected (E) - Observable Result

Describe what the user should observe after performing the action.

#### Types of Expected Results

| Result Type | Example |
|-------------|---------|
| Screen transition | "The User Detail screen appears" |
| Message display | "A success message 'Saved successfully' appears at the top" |
| Data update | "The table refreshes and shows the new record" |
| Visual change | "The button changes from gray to blue" |
| Download start | "A file download begins automatically" |
| Loading indicator | "A spinner appears while data is being processed" |
| Dialog open/close | "The confirmation dialog closes automatically" |

#### Rules for Expected

- Describe only **observable** results (what the user can see or hear)
- Be specific about messages: quote the exact message text when known
- Note the location of the result: "at the top of the page", "in the status bar"
- Include timing when relevant: "within 2-3 seconds", "after processing completes"

### 1.4 Proceed (P) - Confirmation and Transition

Describe how the user confirms success and moves to the next step.

#### Confirmation Patterns

| Pattern | Example |
|---------|---------|
| Visual confirmation | "Confirm that the green checkmark icon appears next to the record" |
| Data verification | "Verify that the created date shows today's date" |
| Count verification | "Confirm that the total count has increased by 1" |
| Status check | "Verify that the status column shows 'Active'" |
| Proceed instruction | "Once confirmed, proceed to Step 3" |
| Conditional branch | "If the error message appears, go to Step 2a. Otherwise, proceed to Step 3" |

---

## 2. Step Numbering Conventions

### Main Steps

Use sequential integers for primary procedure steps:

```
Step 1: ...
Step 2: ...
Step 3: ...
```

### Sub-Steps

Use decimal notation for steps that are part of a larger step:

```
Step 3: Configure user settings
  Step 3.1: Set the username
  Step 3.2: Set the email address
  Step 3.3: Set the role
```

### Conditional Branches

Use letter suffixes for alternative paths:

```
Step 4: Check the approval status
  Step 4a: If status is "Approved" → Proceed to Step 5
  Step 4b: If status is "Rejected" → Go to Step 6
  Step 4c: If status is "Pending" → Wait and repeat Step 4 after 10 minutes
```

### Looping / Repetition

Use explicit loop notation:

```
Step 7: Repeat Steps 4-6 for each remaining item in the list
```

---

## 3. Screenshot Guidelines

### When to Include Screenshots

Include a screenshot placeholder for:
- First-time screen appearance (the user has not seen this screen before)
- Complex UI layouts with many elements
- Steps where the target element is difficult to locate
- Before-and-after comparisons for data changes
- Error messages and unusual states
- Configuration screens with many options

### Screenshot Placeholder Format

```
[Screenshot: {Brief description of what the screenshot should show}]
```

Examples:
```
[Screenshot: Login screen with username and password fields highlighted]
[Screenshot: Dashboard main screen after successful login]
[Screenshot: User creation form with all required fields marked]
[Screenshot: Success message after saving the record]
[Screenshot: Error dialog when validation fails]
```

### Screenshot Naming Convention

When actual screenshots are added later, use the following naming convention:

```
{OP-ID}_{step-number}_{description}.png
```

Examples:
```
OP-001_01_login-screen.png
OP-001_02_dashboard-after-login.png
OP-003_05_error-validation-failed.png
```

### Annotation Guidelines

- Use **red rectangles** to highlight the target UI element
- Use **numbered callouts** (1, 2, 3) for steps involving multiple elements
- Use **arrows** to indicate sequence or flow
- Keep annotations minimal: highlight only what is relevant to the current step
- Avoid cluttering the screenshot with too many annotations

---

## 4. Good vs Bad Examples

### Example: Creating a New User

#### Bad Example (Vague, Missing STEP Components)

```
1. Go to user management and add a new user.
2. Fill in the information.
3. Save it.
```

**Problems**: No specific actions, no target elements identified, no expected results, no confirmation steps.

#### Good Example (Complete STEP Format)

```
Step 1:
  S: Click
  T: The **User Management** link in the left navigation menu
  E: The User Management screen appears, displaying a list of existing users
  P: Confirm the page title shows "User Management"

Step 2:
  S: Click
  T: The **+ Add User** button in the upper-right corner of the User Management screen
  E: The "New User" dialog opens with empty input fields
  P: Confirm the dialog title shows "New User"

[Screenshot: New User dialog with all input fields visible]

> NOTE: All fields marked with an asterisk (*) are required.

Step 3:
  S: Type the user's full name (e.g., `Tanaka Taro`)
  T: The **Full Name** text field in the New User dialog
  E: The entered name appears in the field
  P: Verify the name is spelled correctly before proceeding

Step 4:
  S: Type the user's email address (e.g., `tanaka@example.com`)
  T: The **Email Address** text field
  E: The entered email appears in the field
  P: Verify the email format is correct (contains @ and domain)

> WARNING: The email address must be unique. If a duplicate email is entered,
> the system will reject the registration and display an error.

Step 5:
  S: Select the appropriate role
  T: The **Role** dropdown menu
  E: The dropdown expands showing available roles: Admin, Editor, Viewer
  P: Confirm the selected role appears in the dropdown field

Step 6:
  S: Click
  T: The **Save** button at the bottom-right of the dialog
  E: The dialog closes, and a success message "User created successfully" appears.
     The new user is visible in the user list.
  P: Confirm the new user appears in the list with the correct name, email, and role
```

---

## 5. Handling Conditional Paths

When a procedure has branching logic, clearly indicate:

1. **The decision point**: What condition determines the branch
2. **Each branch**: Clearly labeled with the condition
3. **Merge point**: Where branches rejoin (if applicable)

### Format for Conditional Steps

```
Step 5: Check the validation result
  Condition: Review the message displayed at the top of the form

  Step 5a [If "Validation successful" message appears]:
    S: Click
    T: The **Submit** button
    E: The form is submitted and a confirmation screen appears
    P: Proceed to Step 6

  Step 5b [If "Validation failed" message appears]:
    S: Review the error messages listed below the form
    T: The **Error Details** section (highlighted in red)
    E: One or more error descriptions are displayed
    P: Correct each error, then return to Step 4 to re-validate
```

---

## 6. Verification Checkpoints

Insert verification checkpoints at critical stages of a procedure. These are pauses where the user confirms that everything is correct before continuing.

### Checkpoint Format

```
--- Verification Checkpoint ---
Before proceeding, confirm the following:
- [ ] The record status shows "Draft"
- [ ] All required fields are filled (no red highlights)
- [ ] The total amount matches the expected value
- [ ] The assigned approver is correct
If any item is not confirmed, do NOT proceed. Review the previous steps.
---
```

### When to Insert Checkpoints

- Before submitting or saving critical data
- Before operations that affect other users or systems
- Before irreversible operations (deletions, approvals, transmissions)
- At the end of a multi-step configuration sequence
- Before transitioning to a different system or module

---

## 7. Writing Style Rules

### General Principles

1. **Consistency**: Use the same term for the same element throughout the document
2. **Brevity**: Keep each step focused on one action
3. **Precision**: Use exact names, paths, and values
4. **Neutrality**: Avoid subjective language ("easy", "simple", "just")
5. **Active voice**: "Click the button" not "The button should be clicked"

### Prohibited Phrases

| Prohibited | Replacement |
|-----------|-------------|
| "Simply click..." | "Click..." |
| "Just enter..." | "Enter..." |
| "You should see..." | "The screen displays..." |
| "Easy to use" | (Remove entirely) |
| "Obviously" | (Remove entirely) |
| "As you know" | (Remove entirely) |
| "etc." | List all items explicitly |

### Document-Wide Terminology Control

Maintain a terminology table at the end of the manual to ensure consistency:

| Term | Definition | Notes |
|------|-----------|-------|
| User | A person who accesses the system | Do not use "operator" interchangeably |
| Record | A single data entry in the system | Do not use "item" or "entry" |
| Save | Store changes to the database | Do not use "submit" unless it triggers workflow |
