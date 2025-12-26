# Render CLI Updates

Last updated: 2025-12-24 06:03:52

## Latest Release Information

- **Version**: v2.6.1
- **Published**: 2025-12-09
- **Release URL**: https://github.com/render-oss/cli/releases/tag/v2.6.1

### Release Notes

[d924074](https://github.com/render-oss/cli/commit/d924074944a62c1ffc75e40238dcd041cf323003) - Bug fix for log viewer infinite scroll.

**Full Changelog**: https://github.com/render-oss/cli/compare/v2.6.0...v2.6.1

## Official Documentation Summary

Source: https://render.com/docs/cli

### Key Points from Documentation

The Render CLI – Render Docs Use the Render CLI to manage your Render services and datastores directly from your terminal: Among many other capabilities, the CLI supports: Triggering service deploys, restarts, and one-off jobs Opening a psql session to your database Viewing and filtering live service logs
The CLI also supports non-interactive use in scripts and CI/CD. Please submit bugs and feature requests on the CLI's public GitHub repository .
Setup 1. Install Homebrew Linux/MacOS Direct download Build from source
Run the following commands: Run the following command: Open the CLI's GitHub releases page . Download the executable that corresponds to your system's architecture.
If you use an architecture besides those provided, you can build from source instead. We recommend building from source only if no other installation method works for your system. Install the Go programming language if you haven't already. Clone and build the CLI project with the following commands: After installation completes, open a new terminal tab and run
render with no arguments to confirm. 2. Log in The Render CLI uses a CLI token to authenticate with the Render platform. Generate a token with the following steps:
Run the following command: Your browser opens a confirmation page in the Render Dashboard. Click Generate token . The CLI saves the generated token to its
local configuration file . When you see the success message in your browser, close the tab and return to your terminal. The CLI prompts you to set your active workspace. You can switch workspaces at any time with render workspace set
. You're ready to go! Common commands This is not an exhaustive list of commands. Run render
with no arguments for a list of all available commands. Run render help <command> for details about a specific command. Command Description
login Opens your browser to authorize the Render CLI for your account. Authorizing generates a CLI token that's saved locally. If the CLI already has a valid CLI t

## Update Check Configuration

- **Check Interval**: 30 days
- **Documentation URL**: https://render.com/docs/cli
- **GitHub Releases**: https://github.com/render-oss/cli/releases

## How to Force Update

```bash
python3 ~/.claude/skills/render-cli-expert/scripts/render_cli_updater.py --force
```

## Links

- [Official CLI Documentation](https://render.com/docs/cli)
- [Render Changelog](https://render.com/changelog)
- [GitHub Releases](https://github.com/render-oss/cli/releases)
