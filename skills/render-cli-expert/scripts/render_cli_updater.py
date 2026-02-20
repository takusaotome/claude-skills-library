#!/usr/bin/env python3
"""
Render CLI Documentation Auto-Updater

This script checks the official Render CLI documentation for updates.
If the last check was more than 30 days ago, it fetches the latest
information and saves it to references/cli_updates.md.

Usage:
    python3 render_cli_updater.py           # Check and update if needed
    python3 render_cli_updater.py --force   # Force update regardless of time
    python3 render_cli_updater.py --check   # Only check, don't update
    python3 render_cli_updater.py --status  # Show last check status
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional

# Configuration
SKILL_DIR = Path(__file__).parent.parent
REFERENCES_DIR = SKILL_DIR / "references"
LAST_CHECK_FILE = REFERENCES_DIR / "last_check.json"
UPDATES_FILE = REFERENCES_DIR / "cli_updates.md"
UPDATE_INTERVAL_DAYS = 30

# Official documentation URLs
RENDER_CLI_DOCS_URL = "https://render.com/docs/cli"
RENDER_CHANGELOG_URL = "https://render.com/changelog"
GITHUB_RELEASES_URL = "https://api.github.com/repos/render-oss/cli/releases/latest"


class SimpleHTMLTextExtractor(HTMLParser):
    """Simple HTML parser to extract text content."""

    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_tags = {"script", "style", "nav", "footer", "header"}
        self.current_skip = False
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.current_skip = True
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip_depth -= 1
            if self.skip_depth == 0:
                self.current_skip = False

    def handle_data(self, data):
        if not self.current_skip:
            text = data.strip()
            if text:
                self.text_parts.append(text)

    def get_text(self) -> str:
        return "\n".join(self.text_parts)


def load_last_check() -> Optional[dict]:
    """Load the last check information from JSON file."""
    if not LAST_CHECK_FILE.exists():
        return None

    try:
        with open(LAST_CHECK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load last check file: {e}")
        return None


def save_last_check(data: dict) -> None:
    """Save the last check information to JSON file."""
    REFERENCES_DIR.mkdir(parents=True, exist_ok=True)

    with open(LAST_CHECK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def needs_update(last_check: Optional[dict]) -> bool:
    """Check if an update is needed based on the last check date."""
    if last_check is None:
        return True

    last_check_date_str = last_check.get("last_check_date")
    if not last_check_date_str:
        return True

    try:
        last_check_date = datetime.fromisoformat(last_check_date_str)
        days_since_check = (datetime.now() - last_check_date).days
        return days_since_check >= UPDATE_INTERVAL_DAYS
    except ValueError:
        return True


def fetch_url(url: str, timeout: int = 30) -> Optional[str]:
    """Fetch content from a URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching {url}: {e}")
        return None


def extract_text_from_html(html: str) -> str:
    """Extract text content from HTML."""
    parser = SimpleHTMLTextExtractor()
    parser.feed(html)
    return parser.get_text()


def fetch_github_release() -> Optional[dict]:
    """Fetch the latest release information from GitHub."""
    try:
        headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "Render-CLI-Updater/1.0"}
        request = urllib.request.Request(GITHUB_RELEASES_URL, headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except Exception as e:
        print(f"Error fetching GitHub release: {e}")
        return None


def generate_update_report(docs_content: str, release_info: Optional[dict]) -> str:
    """Generate the update report markdown."""
    now = datetime.now()

    report = f"""# Render CLI Updates

Last updated: {now.strftime("%Y-%m-%d %H:%M:%S")}

## Latest Release Information

"""

    if release_info:
        report += f"""- **Version**: {release_info.get("tag_name", "Unknown")}
- **Published**: {release_info.get("published_at", "Unknown")[:10] if release_info.get("published_at") else "Unknown"}
- **Release URL**: {release_info.get("html_url", GITHUB_RELEASES_URL)}

### Release Notes

{release_info.get("body", "No release notes available.")}

"""
    else:
        report += "Could not fetch latest release information from GitHub.\n\n"

    report += f"""## Official Documentation Summary

Source: {RENDER_CLI_DOCS_URL}

### Key Points from Documentation

"""

    # Extract key sections from docs content
    lines = docs_content.split("\n")
    key_sections = []
    current_section = []

    for line in lines:
        if line.strip():
            current_section.append(line.strip())
            if len(current_section) > 5:
                key_sections.append(" ".join(current_section))
                current_section = []

    if current_section:
        key_sections.append(" ".join(current_section))

    # Add relevant excerpts (first 2000 chars of meaningful content)
    content_excerpt = "\n".join(key_sections)[:2000]
    report += f"{content_excerpt}\n\n"

    report += f"""## Update Check Configuration

- **Check Interval**: {UPDATE_INTERVAL_DAYS} days
- **Documentation URL**: {RENDER_CLI_DOCS_URL}
- **GitHub Releases**: https://github.com/render-oss/cli/releases

## How to Force Update

```bash
python3 ~/.claude/skills/render-cli-expert/scripts/render_cli_updater.py --force
```

## Links

- [Official CLI Documentation]({RENDER_CLI_DOCS_URL})
- [Render Changelog]({RENDER_CHANGELOG_URL})
- [GitHub Releases](https://github.com/render-oss/cli/releases)
"""

    return report


def perform_update(force: bool = False) -> bool:
    """Perform the documentation update check and update if needed."""
    last_check = load_last_check()

    if not force and not needs_update(last_check):
        days_since = 0
        if last_check and last_check.get("last_check_date"):
            try:
                last_date = datetime.fromisoformat(last_check["last_check_date"])
                days_since = (datetime.now() - last_date).days
            except ValueError:
                pass

        print(f"Last check was {days_since} days ago. No update needed.")
        print(f"Next update will be checked after {UPDATE_INTERVAL_DAYS - days_since} days.")
        print("Use --force to update now.")
        return True

    print("Fetching latest Render CLI documentation...")

    # Fetch documentation
    docs_html = fetch_url(RENDER_CLI_DOCS_URL)
    if not docs_html:
        print("Failed to fetch documentation. Keeping existing data.")
        return False

    docs_content = extract_text_from_html(docs_html)

    # Fetch GitHub release
    print("Fetching latest GitHub release information...")
    release_info = fetch_github_release()

    # Generate report
    print("Generating update report...")
    report = generate_update_report(docs_content, release_info)

    # Save report
    REFERENCES_DIR.mkdir(parents=True, exist_ok=True)
    with open(UPDATES_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    # Update last check file
    check_data = {
        "last_check_date": datetime.now().isoformat(),
        "docs_url": RENDER_CLI_DOCS_URL,
        "latest_version": release_info.get("tag_name") if release_info else None,
        "update_interval_days": UPDATE_INTERVAL_DAYS,
    }
    save_last_check(check_data)

    print("Update completed successfully!")
    print(f"Report saved to: {UPDATES_FILE}")
    if release_info:
        print(f"Latest version: {release_info.get('tag_name', 'Unknown')}")

    return True


def show_status() -> None:
    """Show the current update status."""
    last_check = load_last_check()

    print("=== Render CLI Updater Status ===\n")

    if last_check is None:
        print("No previous check found. Run without --status to perform initial check.")
        return

    last_date_str = last_check.get("last_check_date", "Unknown")
    try:
        last_date = datetime.fromisoformat(last_date_str)
        days_since = (datetime.now() - last_date).days
        next_update_in = max(0, UPDATE_INTERVAL_DAYS - days_since)

        print(f"Last check: {last_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Days since last check: {days_since}")
        print(f"Update interval: {UPDATE_INTERVAL_DAYS} days")
        print(f"Next update in: {next_update_in} days")
        print(f"Update needed: {'Yes' if needs_update(last_check) else 'No'}")
    except ValueError:
        print(f"Last check date: {last_date_str} (invalid format)")

    print(f"\nLatest known version: {last_check.get('latest_version', 'Unknown')}")
    print(f"Documentation URL: {last_check.get('docs_url', RENDER_CLI_DOCS_URL)}")

    if UPDATES_FILE.exists():
        print(f"\nUpdate report: {UPDATES_FILE}")
    else:
        print("\nNo update report found.")


def main():
    parser = argparse.ArgumentParser(
        description="Render CLI Documentation Auto-Updater",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 render_cli_updater.py           # Check and update if needed
  python3 render_cli_updater.py --force   # Force update
  python3 render_cli_updater.py --status  # Show status
  python3 render_cli_updater.py --check   # Check only, no update
        """,
    )

    parser.add_argument("--force", "-f", action="store_true", help="Force update regardless of time since last check")

    parser.add_argument(
        "--check", "-c", action="store_true", help="Only check if update is needed, do not perform update"
    )

    parser.add_argument("--status", "-s", action="store_true", help="Show current status and last check information")

    args = parser.parse_args()

    if args.status:
        show_status()
        return 0

    if args.check:
        last_check = load_last_check()
        if needs_update(last_check):
            print("Update is needed.")
            return 1
        else:
            print("No update needed.")
            return 0

    success = perform_update(force=args.force)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
