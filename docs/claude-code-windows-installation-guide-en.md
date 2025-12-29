# Claude Code Windows Installation Guide

A step-by-step guide for installing Claude Code on Windows, designed for everyday Windows users.

> **Target Audience**: You don't need prior experience with Command Prompt (the black window), but should be comfortable installing software on your computer.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Before You Begin](#2-before-you-begin)
3. [Choosing Your Authentication Method](#3-choosing-your-authentication-method)
4. [Method A: Install via Command Prompt (Recommended)](#4-method-a-install-via-command-prompt-recommended)
5. [Method B: Install via PowerShell](#5-method-b-install-via-powershell)
6. [Method C: Automated Installation Script](#6-method-c-automated-installation-script)
7. [Installing Claude Desktop App (Optional)](#7-installing-claude-desktop-app-optional)
8. [Troubleshooting](#8-troubleshooting)
9. [Uninstallation](#9-uninstallation)
10. [FAQ](#10-faq)
11. [Glossary](#11-glossary)

---

## 1. Introduction

### What is Claude Code?

Claude Code is a tool that lets you use Anthropic's AI "Claude" from your computer's **Command Prompt** (the black window).

**What you can do:**
- Show files on your computer to Claude and ask questions about them
- Have Claude write or modify program code
- Get help with file organization and editing

> **What's Command Prompt?**: It's a text-based interface for controlling your computer. You type commands instead of clicking with a mouse. It appears as a black window with white text.

### Claude Desktop vs Claude Code

| Feature | Claude Desktop | Claude Code |
|---------|---------------|-------------|
| Interface | Regular app window | Black window (Command Prompt) |
| How to use | Click with mouse | Type with keyboard |
| Primary use | Chat, writing, Q&A | File operations, programming |
| File access | Limited | Direct access to local files |

**For Pro/Max subscribers**: Both tools are included in your subscription at no extra cost.

---

## 2. Before You Begin

### Requirements

| Item | Requirement | How to Check |
|------|-------------|--------------|
| **OS** | Windows 10 (version 20H2+) or Windows 11 | Press `Win + R` → type "winver" |
| **Internet** | Required | If you can browse websites, you're good |
| **Git for Windows** | Required (installation covered below) | Run `git --version` in Command Prompt |
| **Disk Space** | ~500MB | - |
| **Admin Rights** | Usually not required | - |

### Common Misconceptions (Good to Know)

- **Node.js is NOT required** - Older guides may say it's needed, but not anymore
- **WSL (Windows Subsystem for Linux) is NOT required** - No Linux knowledge needed
- **Programming experience is NOT required** - You don't need to be a developer to use Claude Code

### Security Notice

This guide involves **downloading and running programs from the internet**. Please note:

1. **Trusted sources only**: This guide uses only official sources: Anthropic (claude.ai) and Git (git-scm.com)
2. **Company computers**: **Always check with your IT department** before installing. This may violate company security policies
3. **Antivirus warnings**: You may see warnings during installation. Files from the official sites above are safe

---

## 3. Choosing Your Authentication Method

You need to log in with a Claude account to use Claude Code.

### Which One Should I Choose? (Flowchart)

```
Are you already subscribed to Claude Pro/Max ($20-$200/month)?
│
├─【Yes】→ Option 1: Use Claude Pro/Max Plan
│          (You can use Claude Code at no extra cost)
│
└─【No】→ Starting fresh?
          │
          ├─ Want fixed monthly billing → Sign up for Option 1
          │
          └─ Want pay-as-you-go → Option 2: Claude Console (API)
```

### Option 1: Claude Pro/Max Plan (Recommended)

**Pricing:**
- **Pro**: $20/month
- **Max 5x**: $100/month
- **Max 20x**: $200/month

**Features:**
- Use both Claude Desktop and Claude Code
- Fixed monthly fee - no surprises
- Simple browser-based login

### Option 2: Claude Console (API/Pay-as-you-go)

**Pricing:**
- Pay based on usage
- Requires payment method registration

**Features:**
- Pay only for what you use
- Good for business/enterprise use
- API key authentication

---

## 4. Method A: Install via Command Prompt (Recommended)

The most reliable method. Follow each step carefully.

### Step 1: Install Git for Windows

> **What's Git?**: A tool commonly used by programmers. Claude Code uses some features from Git internally. You won't need to use Git yourself, but it must be installed.

1. Open [Git for Windows official site](https://git-scm.com/downloads/win)
2. Click "**Click here to download**" or "**Download for Windows**"
3. Double-click the downloaded file (e.g., `Git-2.xx.x-64-bit.exe`)
4. When the installer starts, click "Next" through most screens

5. **IMPORTANT**: When you see "**Adjusting your PATH environment**":
   - Select the **second option**: "**Git from the command line and also from 3rd-party software**"
   - If you don't select this, Claude Code won't work properly

   ```
   ┌─────────────────────────────────────────────────────┐
   │ Adjusting your PATH environment                     │
   │                                                     │
   │ ○ Use Git from Git Bash only                       │
   │ ◉ Git from the command line and also from ...  ← Select this │
   │ ○ Use Git and optional Unix tools from the ...    │
   └─────────────────────────────────────────────────────┘
   ```

6. Continue with "Next" → "Install" → "Finish"

7. **Restart your computer** or close all open Command Prompt windows

### Step 2: Verify Git Installation

1. **Open Command Prompt**:
   - Press `Win + R` on your keyboard (Windows key + R)
   - Type "cmd" and press Enter
   - A black window will open

2. Type the following and press Enter:
   ```
   git --version
   ```

3. **Success**: You'll see something like `git version 2.xx.x`
4. **Failed**: If you see "'git' is not recognized", restart your computer and try again

### Step 3: Install Claude Code

1. In the same Command Prompt, type this command:

   ```cmd
   curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
   ```

   > **What this command does**:
   > - `curl`: Downloads a file from the internet
   > - `https://claude.ai/install.cmd`: Anthropic's official installer
   > - `&&`: Run the next command if the previous one succeeded
   > - Finally, delete the temporary file

2. Press Enter to run
3. Wait for installation to complete (may take a few minutes)

4. **Success check**: You should see "Installation complete" or similar message

### Step 4: Open a New Command Prompt

> **Why open a new one?**
> The "PATH environment variable" (settings that tell Windows where to find programs) set during installation won't take effect in already-open windows. Opening a new window applies the settings.

1. **Close** the current Command Prompt (click the X button)
2. Open a **new** Command Prompt (`Win + R` → "cmd" → Enter)

### Step 5: Launch Claude Code and Authenticate

1. In the new Command Prompt, type and press Enter:
   ```
   claude
   ```

2. You'll see authentication options:
   - **For Pro/Max plans**: Select "**Claude.ai (OAuth)**" or "**Claude App**"
   - **For API usage**: Select "**Claude Console**" or "**Anthropic API**"

3. A browser window will open automatically
4. Log in with your Claude account
5. When browser shows "Authentication complete", return to Command Prompt

6. **Success!** Claude Code is now ready to use

### If It Doesn't Work

If you see this error, proceed to [Step 6: Manual Environment Variable Setup](#step-6-manual-environment-variable-setup-if-needed):
- "'claude' is not recognized as an internal or external command..."

---

### Step 6: Manual Environment Variable Setup (If Needed)

> **What's PATH environment variable?**
> It's like an "address book" that Windows uses to find programs. By adding Claude Code's location here, you can run `claude` from anywhere.

If the `claude` command isn't recognized, follow these steps:

1. **Open Settings**: Press `Win + I`

2. **Navigate to Advanced System Settings**:
   - Windows 11: "System" → "About" → "Advanced system settings"
   - Windows 10: "System" → "About" → "Advanced system settings"

3. Click "**Environment Variables**"

4. Under **User variables** (top section), select "**Path**" and click "**Edit**"

5. Click "**New**" and add:
   ```
   %USERPROFILE%\.local\bin
   ```
   > **What's %USERPROFILE%?**: A shortcut for your user folder (e.g., `C:\Users\YourName`)

6. Click "**OK**" three times to close all dialogs

7. **Close Command Prompt and open a new one**

8. Run `claude --version` - if it shows a version number, you're done!

---

## 5. Method B: Install via PowerShell

An alternative using PowerShell instead of Command Prompt.

> **What's PowerShell?**: A newer version of Command Prompt with a blue background.

### Steps

1. **Open PowerShell**:
   - Press `Win + X` and select "Windows PowerShell"
   - Or search for "PowerShell" in the Start menu

2. Verify Git for Windows is installed:
   ```powershell
   git --version
   ```

3. Type the following and press Enter:
   ```powershell
   irm https://claude.ai/install.ps1 | iex
   ```

   > **What this command does**:
   > - `irm`: Invoke-RestMethod (fetch data from internet)
   > - `iex`: Invoke-Expression (run the fetched script)

4. After installation, **close PowerShell and open a new one**

5. Run `claude` to authenticate

### Notes

- If you see execution policy warnings, either allow temporarily or use Method A
- Corporate environments may block this due to security policies

---

## 6. Method C: Automated Installation Script

Use a batch file that automates all steps.

### Steps

1. Download [install-claude-code.bat](../scripts/claude-code-windows-installer/install-claude-code.bat)

2. Double-click the downloaded file

3. A black window will open and installation proceeds automatically:
   - If Git isn't installed → the download page will open
   - After installing Git, run the batch file again

4. After completion, **open a new Command Prompt** and run `claude`

### Notes

- This script automatically configures PATH environment variables
- Antivirus may show warnings, but files from this repository are safe

---

## 7. Installing Claude Desktop App (Optional)

Pro/Max subscribers can also use the desktop app.

### Installation Steps

1. Open [Claude official site](https://claude.com/download)
2. Click "Download for Windows"
3. Run the downloaded installer
4. After installation, log in with your Claude account

### Benefits of Claude Desktop

- Regular app interface (for those who don't like the black window)
- Chat history syncs to cloud
- Included in the same subscription as Claude Code

---

## 8. Troubleshooting

### "'claude' is not recognized..."

**Cause**: Claude Code's location isn't in the PATH environment variable.

**Solution**:
1. First, open a new Command Prompt and try again
2. If that doesn't work, follow [Step 6: Manual Environment Variable Setup](#step-6-manual-environment-variable-setup-if-needed)

**Direct run** (temporary fix):
```cmd
%USERPROFILE%\.local\bin\claude.exe
```

---

### "Git is not installed"

**Solution**:
1. Install [Git for Windows](https://git-scm.com/downloads/win)
2. Select "**Git from the command line and also from 3rd-party software**" during installation (important!)
3. **Restart your computer** and try again

---

### Selected Wrong Option During Git Installation

**Solution**:
1. Open "Control Panel" → "Uninstall a program"
2. Select "Git" and uninstall
3. Reinstall Git for Windows with the correct option

---

### Browser Doesn't Open (Can't Authenticate)

**Possible causes and solutions**:
1. **No default browser set**: Set a default browser in Settings
2. **Firewall blocking**: Temporarily disable and try again
3. **Manual authentication**: Copy the URL shown in Command Prompt and paste it in your browser

---

### Error About "ANTHROPIC_API_KEY"

**Cause**: You may have previously set up API authentication.

**Solution** (to switch to Pro/Max plan):
```cmd
claude /logout
claude
```
Then select "Claude.ai (OAuth)"

---

### Installer Download Failed

**Possible causes**:
- Internet connection issues
- Company proxy/firewall
- Antivirus blocking

**Solutions**:
1. Check your internet connection
2. For company PCs, consult IT department
3. Temporarily disable antivirus and try again

---

## 9. Uninstallation

Steps to remove Claude Code from your computer.

### Remove Claude Code

1. **Delete installation folder**:
   - Open this folder in Explorer:
     ```
     %USERPROFILE%\.local\bin
     ```
   - Delete `claude.exe` and related files

2. **Delete settings folder** (optional):
   ```
   %USERPROFILE%\.claude
   ```

3. **Remove from PATH environment variable**:
   - `Win + I` → System → About → Advanced system settings → Environment Variables
   - Remove `%USERPROFILE%\.local\bin` from user Path variable

### Restoring PATH

Just remove the path that was added during installation. Don't touch other entries.

---

## 10. FAQ

### Q: What's the difference between Claude Code and Claude Desktop?

A: **Claude Desktop** is a regular chat app, while **Claude Code** is a pro tool that can directly access files on your computer. You don't need to be a programmer - it's useful for file organization and document automation too.

---

### Q: Is there a cost?

A: You can use it through:
- **Claude Pro**: $20/month
- **Claude Max 5x**: $100/month
- **Claude Max 20x**: $200/month
- **Claude Console (API)**: Pay-as-you-go

---

### Q: Are there usage limits?

A: Pro/Max plans have usage limits every 5 hours:

| Plan | Approximate (per 5 hours) | What affects it? |
|------|--------------------------|------------------|
| Pro | 10-40 prompts | Message length, attachment size |
| Max 5x | 50-200 prompts | Same |
| Max 20x | 200-800 prompts | Same |

See [official documentation](https://support.claude.com/en/articles/11014257-about-claude-s-max-plan-usage) for details.

---

### Q: Can I use this on a company PC?

A: **Always check with your IT department first**. For enterprises, "Team" or "Enterprise" plans are available that meet security requirements.

---

### Q: Do I need Node.js or WSL?

A: **Neither is required**. The older installation method (via npm) required them, but the current native installer does not.

---

### Q: If installation fails, will it affect my computer?

A: Generally no. This guide only changes:
1. `%USERPROFILE%\.local\bin` folder (created)
2. PATH environment variable (one entry added)

These can easily be reversed (see [Uninstallation](#9-uninstallation)).

---

## 11. Glossary

| Term | Meaning |
|------|---------|
| **Command Prompt** | Text-based interface for controlling Windows. Black window with white text. Built into Windows. |
| **PowerShell** | Enhanced version of Command Prompt. Blue background. |
| **Terminal** | General term for Command Prompt, PowerShell, etc. The "black window" |
| **PATH environment variable** | A list of locations where Windows looks for programs. Like an "address book" |
| **Git** | Tool for programmers. Provides features that Claude Code uses internally. |
| **curl** | Command that downloads files from the internet. |
| **%USERPROFILE%** | Shortcut for your user folder (e.g., `C:\Users\YourName`). |
| **%LOCALAPPDATA%** | Shortcut for app data folder. |
| **OAuth** | Authentication via browser login. Safer because you don't enter passwords directly. |
| **API** | Interface for programs to communicate. Uses API keys for authentication. |

---

## Reference Links

- [Claude Code Official Documentation](https://code.claude.com/docs/en/setup)
- [Using Claude Code with Pro/Max Plan](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)
- [About Usage Limits](https://support.claude.com/en/articles/11014257-about-claude-s-max-plan-usage)
- [Git for Windows](https://git-scm.com/downloads/win)
- [Claude Download](https://claude.com/download)

---

*Last updated: December 2025*
