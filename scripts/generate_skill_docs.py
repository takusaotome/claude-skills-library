#!/usr/bin/env python3
"""Generate Jekyll documentation pages from SKILL.md files.

Reads each skill's SKILL.md (YAML frontmatter + body) to produce EN and JA
pages under docs/{en,ja}/skills/{category}/.

Usage:
    python3 scripts/generate_skill_docs.py --mode full         # all missing skills
    python3 scripts/generate_skill_docs.py --skill tdd-developer
    python3 scripts/generate_skill_docs.py --overwrite          # regenerate all
    python3 scripts/generate_skill_docs.py --add-buttons        # add buttons to hand-written pages
    python3 scripts/generate_skill_docs.py --validate           # validate docs pages
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_DIR = PROJECT_ROOT / "skills"
DEFAULT_DOCS_DIR = PROJECT_ROOT / "docs"

GITHUB_REPO_URL = "https://github.com/takusaotome/claude-skills-library"

# Category slug -> (EN parent title, JA parent title)
CATEGORY_PARENTS = {
    "dev": ("Software Development", "ソフトウェア開発"),
    "management": ("Project & Business", "プロジェクト・経営"),
    "ops": ("Operations & Docs", "運用・ドキュメント"),
    "finance": ("Finance & Analysis", "財務・分析"),
    "meta": ("Meta & Quality", "メタ・品質"),
}

# Existing hand-written guides; skip by default (--overwrite to regenerate).
HAND_WRITTEN = frozenset(
    {
        "business-analyst",
        "completion-quality-gate-designer",
        "critical-code-reviewer",
        "cross-module-consistency-auditor",
        "data-scientist",
        "dual-axis-skill-reviewer",
        "financial-analyst",
        "hidden-contract-investigator",
        "incident-rca-specialist",
        "markdown-to-pdf",
        "operations-manual-creator",
        "production-parity-test-designer",
        "project-plan-creator",
        "safe-by-default-architect",
        "strategic-planner",
        "tdd-developer",
        "vendor-estimate-creator",
    }
)

# Max existing nav_order per category (for appending new pages after).
MAX_NAV_ORDER = {
    "dev": 11,
    "management": 4,
    "ops": 3,
    "finance": 1,
    "meta": 12,
}

# Primary category for every skill.  Determines where the docs page lives.
PRIMARY_CATEGORY: dict[str, str] = {
    # === dev (Software Development & IT) ===
    "aws-cli-expert": "dev",
    "codex-reviewer": "dev",
    "critical-code-reviewer": "dev",
    "critical-document-reviewer": "dev",
    "data-scientist": "dev",
    "design-implementation-reviewer": "dev",
    "docling-converter": "dev",
    "duckdb-expert": "dev",
    "ffmpeg-expert": "dev",
    "gogcli-expert": "dev",
    "hidden-contract-investigator": "dev",
    "imagemagick-expert": "dev",
    "log-debugger": "dev",
    "network-diagnostics": "dev",
    "office-script-expert": "dev",
    "render-cli-expert": "dev",
    "safe-by-default-architect": "dev",
    "salesforce-cli-expert": "dev",
    "salesforce-expert": "dev",
    "salesforce-flow-expert": "dev",
    "salesforce-report-creator": "dev",
    "sox-expert": "dev",
    "streamlit-expert": "dev",
    "tdd-developer": "dev",
    "video2minutes": "dev",
    "qr-code-generator": "dev",
    "yt-dlp-expert": "dev",
    # === management (Project & Business) ===
    "ai-adoption-consultant": "management",
    "bug-ticket-creator": "management",
    "business-analyst": "management",
    "business-plan-creator": "management",
    "change-management-consultant": "management",
    "competitive-intelligence-analyst": "management",
    "contract-reviewer": "management",
    "design-thinking": "management",
    "executive-briefing-writer": "management",
    "hearing-to-requirements-mapper": "management",
    "helpdesk-responder": "management",
    "kpi-designer": "management",
    "m-and-a-advisor": "management",
    "patent-analyst": "management",
    "pricing-strategist": "management",
    "project-artifact-linker": "management",
    "project-manager": "management",
    "project-plan-creator": "management",
    "qa-bug-analyzer": "management",
    "strategic-planner": "management",
    "supply-chain-consultant": "management",
    "talent-acquisition-specialist": "management",
    "technical-spec-writer": "management",
    "uat-testcase-generator": "management",
    "vendor-estimate-creator": "management",
    "vendor-estimate-reviewer": "management",
    "vendor-rfq-creator": "management",
    "wbs-review-assistant": "management",
    # === ops (Operations & Documentation) ===
    "ai-text-humanizer": "ops",
    "bcp-planner": "ops",
    "cx-error-analyzer": "ops",
    "data-visualization-expert": "ops",
    "fujisoft-presentation-creator": "ops",
    "incident-rca-specialist": "ops",
    "markdown-to-pdf": "ops",
    "migration-validation-explorer": "ops",
    "operations-manual-creator": "ops",
    "presentation-reviewer": "ops",
    "production-schedule-optimizer": "ops",
    "shift-planner": "ops",
    # === finance (Compliance, Finance & Governance) ===
    "audit-control-designer": "finance",
    "audit-doc-checker": "finance",
    "compliance-advisor": "finance",
    "dama-dmbok": "finance",
    "esg-reporter": "finance",
    "financial-analyst": "finance",
    "internal-audit-assistant": "finance",
    "iso-implementation-guide": "finance",
    "it-system-roi-analyzer": "finance",
    "lean-six-sigma-consultant": "finance",
    "ma-budget-actual-variance": "finance",
    "ma-cvp-break-even": "finance",
    "ma-standard-cost-variance": "finance",
    "management-accounting-navigator": "finance",
    "pci-dss-compliance-consultant": "finance",
    # === meta (Meta, Quality & Specialized) ===
    "codebase-onboarding-generator": "meta",
    "completion-quality-gate-designer": "meta",
    "cross-module-consistency-auditor": "meta",
    "dual-axis-skill-reviewer": "meta",
    "itil4-consultant": "meta",
    "meeting-asset-preparer": "meta",
    "multi-file-log-correlator": "meta",
    "network-incident-analyzer": "meta",
    "production-parity-test-designer": "meta",
    "project-completeness-scorer": "meta",
    "project-kickoff-bootstrapper": "meta",
    "skill-designer": "meta",
    "skill-idea-miner": "meta",
    "timezone-aware-event-tracker": "meta",
}

# ---------------------------------------------------------------------------
# SKILL.md parser
# ---------------------------------------------------------------------------


def parse_skill_md(path: Path) -> dict:
    """Parse SKILL.md into {frontmatter: dict, body: str, sections: dict}."""
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {"frontmatter": {}, "body": text, "sections": {}}

    import yaml

    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        # Fallback: extract name and description manually when YAML
        # has unquoted colons in values.
        fm = {}
        for line in parts[1].strip().splitlines():
            if line.startswith("name:"):
                fm["name"] = line.split(":", 1)[1].strip()
            elif line.startswith("description:"):
                fm["description"] = line.split(":", 1)[1].strip()
    body = parts[2].strip()
    sections = _split_sections(body)
    return {"frontmatter": fm, "body": body, "sections": sections}


def _split_sections(body: str) -> dict[str, str]:
    """Split markdown body into {heading_lower: content} by ## headings."""
    sections: dict[str, str] = {}
    current_key = ""
    lines: list[str] = []

    for line in body.splitlines():
        if line.startswith("## "):
            if current_key:
                sections[current_key] = "\n".join(lines).strip()
            current_key = line.lstrip("# ").strip().lower()
            lines = []
        else:
            lines.append(line)

    if current_key:
        sections[current_key] = "\n".join(lines).strip()

    return sections


# ---------------------------------------------------------------------------
# Badge generation (simplified -- all skills are No API Required)
# ---------------------------------------------------------------------------


def api_badges() -> str:
    """Return EN badge span."""
    return '<span class="badge badge-free">No API Required</span>'


def api_badges_ja() -> str:
    """Return JA badge span."""
    return '<span class="badge badge-free">API不要</span>'


# ---------------------------------------------------------------------------
# Button generation
# ---------------------------------------------------------------------------


def _generate_buttons(skill_name: str, skill_packages_dir: Path | None, lang: str) -> str:
    """Return markdown download/source buttons for a skill page.

    Args:
        skill_name: The skill slug (e.g., "tdd-developer").
        skill_packages_dir: Path to the skill-packages directory, or None.
            Download button is shown only when the .skill file exists.
        lang: "en" or "ja".

    Returns:
        Markdown string with Source button always present, plus Download
        button when .skill package exists.
    """
    buttons = []
    has_package = skill_packages_dir is not None and (skill_packages_dir / f"{skill_name}.skill").exists()

    if has_package:
        dl_url = f"{GITHUB_REPO_URL}/raw/main/skill-packages/{skill_name}.skill"
        if lang == "ja":
            buttons.append(
                f"[スキルパッケージをダウンロード (.skill)]({dl_url})"
                "{: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }"
            )
        else:
            buttons.append(
                f"[Download Skill Package (.skill)]({dl_url}){{: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }}"
            )

    src_url = f"{GITHUB_REPO_URL}/tree/main/skills/{skill_name}"
    if lang == "ja":
        buttons.append(f"[GitHubでソースを見る]({src_url}){{: .btn .fs-5 .mb-4 .mb-md-0 }}")
    else:
        buttons.append(f"[View Source on GitHub]({src_url}){{: .btn .fs-5 .mb-4 .mb-md-0 }}")

    return "\n".join(buttons)


# ---------------------------------------------------------------------------
# Page generation
# ---------------------------------------------------------------------------


def generate_en_page(
    skill_name: str,
    skill_data: dict,
    nav_order: int,
    resources: dict,
    category: str,
    skill_packages_dir: Path | None = None,
) -> str:
    """Generate a 6-section EN documentation page."""
    fm = skill_data["frontmatter"]
    sections = skill_data["sections"]
    title = _title_case(skill_name)
    description = fm.get("description", "")
    badges = api_badges()
    buttons = _generate_buttons(skill_name, skill_packages_dir, "en")
    parent_en = CATEGORY_PARENTS[category][0]

    # Build sections
    overview = _extract_section(sections, ["overview", title.lower()])
    if not overview:
        overview = skill_data["body"].split("\n\n")[0] if skill_data["body"] else description

    prerequisites = _extract_section(sections, ["prerequisites", "pre-requisites"])
    workflow = _extract_section(sections, ["workflow", "running the script", "how to run"])
    when_to_use = _extract_section(sections, ["when to use", "when to use this skill"])

    quick_start = _extract_quick_start(workflow, None)

    # Resources
    refs_list = _format_file_list(resources.get("references", []), f"skills/{skill_name}/references/")
    scripts_list = _format_file_list(resources.get("scripts", []), f"skills/{skill_name}/scripts/")

    page = f"""---
layout: default
title: "{title}"
grand_parent: English
parent: {parent_en}
nav_order: {nav_order}
lang_peer: /ja/skills/{category}/{skill_name}/
permalink: /en/skills/{category}/{skill_name}/
---

# {title}
{{: .no_toc }}

{description}
{{: .fs-6 .fw-300 }}

{badges}

"""
    if buttons:
        page += f"{buttons}\n\n"

    page += f"""<details open markdown="block">
  <summary>Table of Contents</summary>
  {{: .text-delta }}
- TOC
{{:toc}}
</details>

---

## 1. Overview

{overview}

"""
    if when_to_use:
        page += f"""---

## 2. When to Use

{when_to_use}

"""

    page += f"""---

## {"3" if when_to_use else "2"}. Prerequisites

"""
    if prerequisites:
        page += f"{prerequisites}\n\n"
    else:
        page += "- **API Key:** None required\n- **Python 3.9+** recommended\n\n"

    page += f"""---

## {"4" if when_to_use else "3"}. Quick Start

{quick_start}

---

## {"5" if when_to_use else "4"}. Workflow

"""
    if workflow:
        page += f"{workflow}\n\n"
    else:
        page += "See the skill's SKILL.md for the complete workflow.\n\n"

    page += f"""---

## {"6" if when_to_use else "5"}. Resources

"""
    if refs_list:
        page += f"**References:**\n\n{refs_list}\n\n"
    if scripts_list:
        page += f"**Scripts:**\n\n{scripts_list}\n\n"
    if not refs_list and not scripts_list:
        page += "This skill uses built-in Claude capabilities without external scripts or references.\n\n"

    return page.rstrip() + "\n"


def generate_ja_page(
    skill_name: str,
    skill_data: dict,
    nav_order: int,
    resources: dict,
    category: str,
    skill_packages_dir: Path | None = None,
) -> str:
    """Generate a compact JA documentation page."""
    return _generate_ja_doc_page(
        skill_name=skill_name,
        skill_data=skill_data,
        nav_order=nav_order,
        resources=resources,
        category=category,
        skill_packages_dir=skill_packages_dir,
        extended=False,
    )


def generate_en_full_page(
    skill_name: str,
    skill_data: dict,
    nav_order: int,
    resources: dict,
    category: str,
    skill_packages_dir: Path | None = None,
) -> str:
    """Generate a 10-section EN documentation page without TODO placeholders."""
    fm = skill_data["frontmatter"]
    sections = skill_data["sections"]
    title = _title_case(skill_name)
    description = fm.get("description", "")
    badges = api_badges()
    buttons = _generate_buttons(skill_name, skill_packages_dir, "en")
    parent_en = CATEGORY_PARENTS[category][0]

    overview = _extract_section(sections, ["overview", title.lower()])
    if not overview:
        overview = skill_data["body"].split("\n\n")[0] if skill_data["body"] else description

    prerequisites = _extract_section(sections, ["prerequisites", "pre-requisites"])
    if not prerequisites:
        prerequisites = "- **API Key:** None required\n- **Python 3.9+** recommended"

    workflow = _extract_section(sections, ["workflow", "running the script", "how to run"])
    when_to_use = _extract_section(sections, ["when to use", "when to use this skill"])
    outputs = _extract_section(
        sections,
        ["output", "outputs", "deliverables", "artifacts", "output format", "this skill generates"],
    )
    related = _extract_section(sections, ["combining with other skills", "related skills", "multi-skill"])
    quick_start = _extract_quick_start(workflow, None)

    workflow_summary = _excerpt_markdown(
        workflow or "Follow the skill's SKILL.md workflow step by step, starting from a small validated input.",
        max_lines=24,
        ellipsis_note="See the skill's SKILL.md for the full end-to-end workflow.",
    )
    usage_examples = _build_usage_examples_en(when_to_use, title)
    output_text = _build_outputs_en(outputs, resources)
    tips_text = _build_tips_en(skill_name, resources)
    related_text = _build_related_en(related, category)
    troubleshooting_text = _build_troubleshooting_en(resources, prerequisites)
    resources_text = _build_resources_text_en(skill_name, resources)

    page = f"""---
layout: default
title: "{title}"
grand_parent: English
parent: {parent_en}
nav_order: {nav_order}
lang_peer: /ja/skills/{category}/{skill_name}/
permalink: /en/skills/{category}/{skill_name}/
---

# {title}
{{: .no_toc }}

{description}
{{: .fs-6 .fw-300 }}

{badges}

"""
    if buttons:
        page += f"{buttons}\n\n"

    page += f"""<details open markdown="block">
  <summary>Table of Contents</summary>
  {{: .text-delta }}
- TOC
{{:toc}}
</details>

---

## 1. Overview

{overview}

---

## 2. Prerequisites

{prerequisites}

---

## 3. Quick Start

{quick_start}

---

## 4. How It Works

{workflow_summary}

---

## 5. Usage Examples

{usage_examples}

---

## 6. Understanding the Output

{output_text}

---

## 7. Tips & Best Practices

{tips_text}

---

## 8. Combining with Other Skills

{related_text}

---

## 9. Troubleshooting

{troubleshooting_text}

---

## 10. Reference

{resources_text}"""

    return page.rstrip() + "\n"


def generate_ja_full_page(
    skill_name: str,
    skill_data: dict,
    nav_order: int,
    resources: dict,
    category: str,
    skill_packages_dir: Path | None = None,
) -> str:
    """Generate a 10-section JA documentation page without untranslated placeholders."""
    return _generate_ja_doc_page(
        skill_name=skill_name,
        skill_data=skill_data,
        nav_order=nav_order,
        resources=resources,
        category=category,
        skill_packages_dir=skill_packages_dir,
        extended=True,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _title_case(slug: str) -> str:
    """Convert slug to title case, preserving known acronyms."""
    acronyms = {
        "aws": "AWS",
        "cli": "CLI",
        "rca": "RCA",
        "tdd": "TDD",
        "qa": "QA",
        "uat": "UAT",
        "rfq": "RFQ",
        "kpi": "KPI",
        "roi": "ROI",
        "esg": "ESG",
        "iso": "ISO",
        "pdf": "PDF",
        "qr": "QR",
        "m": "M",
        "a": "A",
        "bcp": "BCP",
        "cx": "CX",
        "it": "IT",
        "duckdb": "DuckDB",
        "ffmpeg": "FFmpeg",
        "sox": "SoX",
        "pci": "PCI",
        "dss": "DSS",
        "itil4": "ITIL4",
        "ma": "MA",
        "cvp": "CVP",
        "mcp": "MCP",
        "sql": "SQL",
        "ai": "AI",
        "wbs": "WBS",
    }
    words = slug.split("-")
    return " ".join(acronyms.get(w, w.capitalize()) for w in words)


def _extract_section(sections: dict, keys: list[str]) -> str:
    """Find a section by trying multiple heading keys."""
    for key in keys:
        for sec_key, content in sections.items():
            if key in sec_key:
                return content
    return ""


def _extract_quick_start(workflow: str, cli_example: str | None) -> str:
    """Extract a quick start section from workflow or CLI example."""
    if cli_example:
        return f"```bash\n{cli_example}\n```"
    if workflow:
        # Extract the first code block from workflow
        code_match = re.search(r"```(?:bash)?\n(.*?)```", workflow, re.DOTALL)
        if code_match:
            return f"```bash\n{code_match.group(1).strip()}\n```"
        # Extract the first step
        lines = workflow.strip().splitlines()
        quick = []
        for line in lines[:10]:
            quick.append(line)
            if line.strip() == "" and len(quick) > 3:
                break
        return "\n".join(quick).strip()
    return "Invoke this skill by describing your analysis needs to Claude."


def _excerpt_markdown(text: str, max_lines: int, ellipsis_note: str | None = None) -> str:
    """Return the first N markdown lines, optionally appending a note."""
    clean_lines: list[str] = []
    for line in text.strip().splitlines():
        if line.strip() == "---":
            break
        clean_lines.append(line)
    if len(clean_lines) <= max_lines:
        return "\n".join(clean_lines).strip()
    excerpt = "\n".join(clean_lines[:max_lines]).rstrip()
    if ellipsis_note:
        excerpt += f"\n\n{ellipsis_note}"
    return excerpt


def _extract_bullet_lines(text: str, max_items: int = 6) -> list[str]:
    """Extract bullet or numbered list items from markdown text."""
    items: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^[-*]\s+", stripped):
            items.append(re.sub(r"^[-*]\s+", "", stripped))
        elif re.match(r"^\d+\.\s+", stripped):
            items.append(re.sub(r"^\d+\.\s+", "", stripped))
        if len(items) >= max_items:
            break
    return items


def _build_usage_examples_en(when_to_use: str, title: str) -> str:
    """Build a practical usage examples section."""
    items = _extract_bullet_lines(when_to_use, max_items=6)
    if items:
        return "\n".join(f"- {item}" for item in items)
    return "\n".join(
        [
            f"- Use **{title}** when you need a structured workflow rather than an ad-hoc answer.",
            "- Start with a small representative input before applying the workflow to production data or assets.",
            "- Review the helper scripts and reference guides to tailor the output format to your project.",
        ]
    )


def _build_outputs_en(outputs: str, resources: dict) -> str:
    """Describe expected outputs using explicit sections or resource inventory."""
    if outputs:
        return _excerpt_markdown(
            outputs, max_lines=18, ellipsis_note="The full output details are documented in SKILL.md."
        )

    refs = len(resources.get("references", []))
    scripts = len(resources.get("scripts", []))
    lines = [
        "- A structured response or artifact aligned to the skill's workflow.",
        f"- Reference support from {refs} guide file(s)."
        if refs
        else "- Guidance derived directly from the skill instructions.",
    ]
    if scripts:
        lines.append(f"- Script-assisted execution using {scripts} helper command(s) where applicable.")
    lines.append("- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.")
    return "\n".join(lines)


def _build_tips_en(skill_name: str, resources: dict) -> str:
    """Generate best-practice guidance for auto-generated pages."""
    refs = resources.get("references", [])
    scripts = resources.get("scripts", [])
    lines = [
        "- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.",
        f"- Keep `skills/{skill_name}/SKILL.md` open while working; it remains the authoritative source for the full procedure.",
    ]
    if refs:
        lines.append(
            f"- Review the most relevant reference files first instead of scanning every guide: {', '.join(refs[:3])}."
        )
    if scripts:
        lines.append(
            f"- Run helper scripts on test data before using them on final assets or production-bound inputs: {', '.join(scripts[:3])}."
        )
    lines.append(
        "- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly."
    )
    return "\n".join(lines)


def _build_related_en(related: str, category: str) -> str:
    """Generate related-skills guidance."""
    if related:
        return _excerpt_markdown(
            related, max_lines=16, ellipsis_note="Refer to the category index for additional related skills."
        )

    category_url = f"{{{{ '/en/skills/{category}/' | relative_url }}}}"
    return "\n".join(
        [
            "- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.",
            f"- Browse the broader category for neighboring workflows: [category index]({category_url}).",
            "- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.",
        ]
    )


def _build_troubleshooting_en(resources: dict, prerequisites: str) -> str:
    """Generate generic troubleshooting guidance."""
    lines = [
        "- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.",
        "- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.",
        "- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.",
    ]
    if "Python" in prerequisites:
        lines.append(
            "- Confirm the expected Python version and required packages are installed in the active environment."
        )
    if resources.get("scripts"):
        lines.append(
            "- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths."
        )
    return "\n".join(lines)


def _build_resources_text_en(skill_name: str, resources: dict) -> str:
    """Render reference and script lists for EN pages."""
    refs_list = _format_file_list(resources.get("references", []), f"skills/{skill_name}/references/")
    scripts_list = _format_file_list(resources.get("scripts", []), f"skills/{skill_name}/scripts/")
    chunks = []
    if refs_list:
        chunks.append(f"**References:**\n\n{refs_list}")
    if scripts_list:
        chunks.append(f"**Scripts:**\n\n{scripts_list}")
    if not chunks:
        chunks.append("This skill uses built-in Claude capabilities without external scripts or references.")
    return "\n\n".join(chunks)


def _localize_prerequisites_ja(prerequisites: str) -> str:
    """Convert common prerequisite lines into Japanese."""
    if not prerequisites.strip():
        return "- APIキーは不要です\n- Python 3.9 以上を推奨します"

    packages: list[str] = []
    package_match = re.search(r"(Required packages|Dependencies)\s*:\s*(.+)", prerequisites, re.IGNORECASE)
    if package_match:
        raw = package_match.group(2).replace("`", "")
        packages = [p.strip() for p in re.split(r",\s*", raw) if p.strip()]

    lines = [
        "- APIキーは不要です",
        "- Python 3.9 以上を推奨します",
    ]
    if packages:
        lines.append(f"- 主な依存パッケージ: {', '.join(packages)}")
    elif any(dep in prerequisites for dep in ("openpyxl", "pandas", "pyyaml")):
        deps = [dep for dep in ("openpyxl", "pandas", "pyyaml") if dep in prerequisites]
        lines.append(f"- 主な依存パッケージ: {', '.join(deps)}")
    lines.append("- 詳細な実行条件は英語版ガイドまたは `SKILL.md` を参照してください。")
    return "\n".join(lines)


def _build_ja_blurb(title: str, skill_name: str) -> str:
    """Build a Japanese lead sentence for generated pages."""
    return (
        f"{title} に関する日本語ガイドです。`skills/{skill_name}/SKILL.md` をもとに、"
        "利用開始手順、参照ファイル、補助スクリプトへの入口を日本語で整理しています。"
    )


def _build_overview_ja(title: str, skill_name: str, resources: dict) -> str:
    """Build a Japanese overview without embedding untranslated English sections."""
    refs = len(resources.get("references", []))
    scripts = len(resources.get("scripts", []))
    lines = [
        f"このページは **{title}** スキルの日本語サマリーです。",
        f"- スキル本体: `skills/{skill_name}/SKILL.md`",
        f"- 参照ガイド: {refs} 件" if refs else "- 参照ガイド: なし",
        f"- 補助スクリプト: {scripts} 件" if scripts else "- 補助スクリプト: なし",
        "- 詳細な背景説明や判断基準は英語版ガイドを参照してください。",
    ]
    return "\n".join(lines)


def _build_usage_examples_ja(title: str, resources: dict) -> str:
    """Build a practical Japanese usage section."""
    lines = [
        f"- **{title}** に沿って作業の進め方を整理したいとき",
        "- まず最小の入力やサンプルデータで手順を確認したいとき",
    ]
    if resources.get("scripts"):
        lines.append("- 補助スクリプトを使って定型処理や検証を実行したいとき")
    if resources.get("references"):
        lines.append("- 参照ガイドを見ながら出力の粒度や観点を揃えたいとき")
    lines.append("- 詳細な実装判断や例外ケースは英語版ガイドも併用したいとき")
    return "\n".join(lines)


def _build_workflow_ja(skill_name: str, resources: dict) -> str:
    """Build a generic Japanese workflow summary."""
    lines = [
        f"1. `skills/{skill_name}/SKILL.md` を開き、対象タスクと期待する成果物を確認します。",
        "2. クイックスタートのコマンドや最小サンプルで、手順が通ることを先に確認します。",
    ]
    if resources.get("references"):
        lines.append("3. 必要な観点に応じて `references/` 配下のガイドを確認し、判断基準を揃えます。")
    if resources.get("scripts"):
        lines.append("4. 補助スクリプトがある場合は小さな入力で実行し、出力形式を確認してから本番データへ広げます。")
    else:
        lines.append("4. スキルの手順に沿って対話またはドキュメント作成を進めます。")
    lines.append("5. 仕上げ時に、出力内容と前提条件が依頼内容に合っているか見直します。")
    return "\n".join(lines)


def _build_outputs_ja(resources: dict) -> str:
    """Describe expected outputs in Japanese."""
    refs = len(resources.get("references", []))
    scripts = len(resources.get("scripts", []))
    lines = [
        "- スキルの手順に沿った構造化された回答、分析結果、または文書ドラフト",
        f"- 参照ガイド {refs} 件を根拠にした判断材料" if refs else "- スキル定義に基づく判断材料",
    ]
    if scripts:
        lines.append(f"- 補助スクリプト {scripts} 件による補助出力や検証結果")
    lines.append("- 後続レビューや別スキル連携に回せる中間成果物")
    return "\n".join(lines)


def _build_tips_ja(skill_name: str, resources: dict) -> str:
    """Generate Japanese best-practice guidance."""
    lines = [
        "- まずは小さな入力で試し、期待する出力形式になっていることを確認してから対象範囲を広げてください。",
        f"- 詳細な手順や判断基準は `skills/{skill_name}/SKILL.md` を基準にしてください。",
    ]
    if resources.get("references"):
        lines.append("- 参照ガイドは必要なものから順に読むと、過剰に読み散らかさずに進められます。")
    if resources.get("scripts"):
        lines.append("- 補助スクリプトは本番データの前にサンプル入力で実行し、引数と出力先を確認してください。")
    lines.append("- 出力前に、前提条件・入力範囲・未確定事項を明示すると後戻りが減ります。")
    return "\n".join(lines)


def _build_related_ja(category: str) -> str:
    """Generate Japanese related-skills guidance."""
    category_url = f"{{{{ '/ja/skills/{category}/' | relative_url }}}}"
    en_url = f"{{{{ '/en/skills/{category}/' | relative_url }}}}"
    return "\n".join(
        [
            "- 同じカテゴリのスキルと組み合わせると、計画・実装・レビューまでの流れをつなぎやすくなります。",
            f"- 日本語のカテゴリ一覧: [カテゴリページ]({category_url})",
            f"- 詳細な関連ワークフローを探す場合は英語版カテゴリ一覧も参照してください: [English category]({en_url})",
        ]
    )


def _build_troubleshooting_ja(prerequisites: str, resources: dict) -> str:
    """Generate Japanese troubleshooting guidance."""
    lines = [
        "- まず前提条件を確認し、必要なランタイムやパッケージが揃っているかを見直してください。",
        "- 補助スクリプトを使う場合は、最小入力で一度実行してから本番データへ広げてください。",
        "- 期待する出力にならない場合は、参照ガイドにある入力形式や観点の前提を確認してください。",
    ]
    if "Python" in prerequisites:
        lines.append("- Python のバージョン差分が原因になることがあるため、推奨バージョンを確認してください。")
    if resources.get("scripts"):
        lines.append("- 引数や出力先の指定漏れが多いため、コマンド例をそのまま起点に調整すると安全です。")
    return "\n".join(lines)


def _build_resources_text_ja(skill_name: str, resources: dict) -> str:
    """Render reference and script lists for JA pages."""
    refs_list = _format_file_list(resources.get("references", []), f"skills/{skill_name}/references/")
    scripts_list = _format_file_list(resources.get("scripts", []), f"skills/{skill_name}/scripts/")
    chunks = []
    if refs_list:
        chunks.append(f"**参照ガイド:**\n\n{refs_list}")
    if scripts_list:
        chunks.append(f"**補助スクリプト:**\n\n{scripts_list}")
    if not chunks:
        chunks.append("このスキルは外部スクリプトや追加の参照ファイルを使わず、Claude の標準機能を中心に利用します。")
    return "\n\n".join(chunks)


def _generate_ja_doc_page(
    skill_name: str,
    skill_data: dict,
    nav_order: int,
    resources: dict,
    category: str,
    skill_packages_dir: Path | None,
    extended: bool,
) -> str:
    """Generate a Japanese summary page."""
    title = _title_case(skill_name)
    badges = api_badges_ja()
    buttons = _generate_buttons(skill_name, skill_packages_dir, "ja")
    parent_ja = CATEGORY_PARENTS[category][1]
    workflow = _extract_section(skill_data["sections"], ["workflow", "running the script", "how to run"])
    quick_start = _extract_quick_start(workflow, None)
    prerequisites = _extract_section(skill_data["sections"], ["prerequisites", "pre-requisites"])
    localized_prereqs = _localize_prerequisites_ja(prerequisites)
    blurb = _build_ja_blurb(title, skill_name)
    overview = _build_overview_ja(title, skill_name, resources)
    usage_examples = _build_usage_examples_ja(title, resources)
    workflow_text = _build_workflow_ja(skill_name, resources)
    outputs_text = _build_outputs_ja(resources)
    tips_text = _build_tips_ja(skill_name, resources)
    related_text = _build_related_ja(category)
    troubleshooting_text = _build_troubleshooting_ja(prerequisites, resources)
    resources_text = _build_resources_text_ja(skill_name, resources)
    english_link = f"{{{{ '/en/skills/{category}/{skill_name}/' | relative_url }}}}"

    page = f"""---
layout: default
title: "{title}"
grand_parent: 日本語
parent: {parent_ja}
nav_order: {nav_order}
lang_peer: /en/skills/{category}/{skill_name}/
permalink: /ja/skills/{category}/{skill_name}/
---

# {title}
{{: .no_toc }}

{blurb}
{{: .fs-6 .fw-300 }}

{badges}

"""
    if buttons:
        page += f"{buttons}\n\n"

    page += f"""<details open markdown="block">
  <summary>目次</summary>
  {{: .text-delta }}
- TOC
{{:toc}}
</details>

---

## 1. 概要

{overview}

---

## 2. 前提条件

{localized_prereqs}

---

## 3. クイックスタート

{quick_start}

"""
    if not extended:
        page += f"""---

## 4. 進め方

{workflow_text}

---

## 5. リソース

{resources_text}

---

## 6. 英語版ガイド

- 詳細な背景説明、判断基準、実装例は [English version]({english_link}) を参照してください。
"""
        return page.rstrip() + "\n"

    page += f"""---

## 4. 進め方

{workflow_text}

---

## 5. 使用例

{usage_examples}

---

## 6. 出力の読み方

{outputs_text}

---

## 7. ベストプラクティス

{tips_text}

---

## 8. 他スキルとの連携

{related_text}

---

## 9. トラブルシューティング

{troubleshooting_text}

---

## 10. リファレンス

{resources_text}

---

## English Version

- 詳細な解説、背景説明、個別の運用判断は [English version]({english_link}) を参照してください。
"""

    return page.rstrip() + "\n"


def _format_file_list(files: list[str], prefix: str) -> str:
    """Format a list of files as markdown."""
    if not files:
        return ""
    return "\n".join(f"- `{prefix}{f}`" for f in sorted(files))


def _list_skill_resources(skill_dir: Path) -> dict:
    """List references and scripts files for a skill."""
    result: dict[str, list[str]] = {"references": [], "scripts": []}

    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        result["references"] = [f.name for f in refs_dir.iterdir() if f.is_file() and not f.name.startswith(".")]

    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        result["scripts"] = [
            f.name
            for f in scripts_dir.iterdir()
            if f.is_file() and f.suffix == ".py" and not f.name.startswith("test_")
        ]

    return result


def _slugify(name: str) -> str:
    """Convert a display name to a directory slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _get_category(skill_name: str) -> str:
    """Get the primary category for a skill.  Defaults to 'meta'."""
    return PRIMARY_CATEGORY.get(skill_name, "meta")


# ---------------------------------------------------------------------------
# Index page update
# ---------------------------------------------------------------------------

# Regex to match a skill name in a table row (linked or plain text).
_INDEX_SKILL_RE = re.compile(
    r"^\|"  # row starts with |
    r"\s*"
    r"(?:\[([^\]]+)\]\([^)]+\))"  # linked: [name](url)
    r"|"
    r"(?:([^|[]+?))"  # or plain text name
)

_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def update_index_pages(
    skills_dir: Path,
    docs_dir: Path,
) -> None:
    """Add links to category index tables and skill catalog rows."""
    table_paths = []
    for lang in ("en", "ja"):
        table_paths.append(docs_dir / lang / "skill-catalog.md")
        for cat_slug in CATEGORY_PARENTS:
            table_paths.append(docs_dir / lang / "skills" / cat_slug / "index.md")

    for table_path in table_paths:
        if not table_path.exists():
            continue

        text = table_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        changed = False
        lang = "ja" if "/ja/" in str(table_path) else "en"

        for i, line in enumerate(lines):
            if not line.startswith("|"):
                continue
            cols = [c.strip() for c in line.split("|")]
            if len(cols) < 4:
                continue
            name_col = cols[1]
            if not name_col or name_col.startswith("---") or name_col in ("Skill", "スキル", "Badge"):
                continue
            if "[" in name_col:
                continue

            slug = _slugify(name_col)
            if not slug:
                continue

            cat_slug = _get_category(slug)
            page_path = docs_dir / lang / "skills" / cat_slug / f"{slug}.md"
            if not page_path.exists():
                continue

            link = f"{{{{ '/{lang}/skills/{cat_slug}/{slug}/' | relative_url }}}}"
            linked_name = f"[{name_col}]({link})"
            new_line = line.replace(f"| {name_col} |", f"| {linked_name} |", 1)
            if new_line != line:
                lines[i] = new_line
                changed = True

        if changed:
            table_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(f"  Updated index: {table_path}")


# ---------------------------------------------------------------------------
# --add-buttons mode
# ---------------------------------------------------------------------------


def add_buttons_to_hand_written(
    docs_dir: Path,
    skill_packages_dir: Path | None,
) -> None:
    """Add download/GitHub buttons to existing hand-written pages."""
    for skill_name in sorted(HAND_WRITTEN):
        category = _get_category(skill_name)
        for lang in ("en", "ja"):
            page_path = docs_dir / lang / "skills" / category / f"{skill_name}.md"
            if not page_path.exists():
                continue

            text = page_path.read_text(encoding="utf-8")

            # Skip if buttons already exist
            if lang == "ja" and "スキルパッケージをダウンロード" in text:
                continue
            if lang == "en" and "Download Skill Package" in text:
                continue
            if "View Source on GitHub" in text or "GitHubでソースを見る" in text:
                continue

            buttons = _generate_buttons(skill_name, skill_packages_dir, lang)
            if not buttons:
                continue

            # Find the badge line (line containing <span class="badge)
            lines = text.splitlines()
            insert_idx = None
            for idx, line in enumerate(lines):
                if '<span class="badge' in line:
                    insert_idx = idx + 1
                    break

            if insert_idx is None:
                print(f"  Skipped (no badge line): {page_path}")
                continue

            # Insert buttons after badge line
            lines.insert(insert_idx, "")
            lines.insert(insert_idx + 1, buttons)
            page_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(f"  Added buttons: {page_path}")


# ---------------------------------------------------------------------------
# --validate mode
# ---------------------------------------------------------------------------


def validate_docs(
    docs_dir: Path,
    skills_dir: Path,
    skill_packages_dir: Path | None,
) -> int:
    """Validate docs pages.  Returns number of errors."""
    errors = 0

    for lang in ("en", "ja"):
        for cat_slug in CATEGORY_PARENTS:
            cat_dir = docs_dir / lang / "skills" / cat_slug
            if not cat_dir.is_dir():
                continue

            for md_file in sorted(cat_dir.iterdir()):
                if md_file.name == "index.md" or not md_file.suffix == ".md":
                    continue

                skill_name = md_file.stem
                text = md_file.read_text(encoding="utf-8")

                # Parse frontmatter
                parts = text.split("---", 2)
                if len(parts) < 3:
                    print(f"  ERROR: No frontmatter: {md_file}")
                    errors += 1
                    continue

                fm_text = parts[1]

                # Check lang_peer points to existing file
                peer_match = re.search(r"lang_peer:\s*(/\w+/skills/\w+/[\w-]+/)", fm_text)
                if peer_match:
                    peer_url = peer_match.group(1)
                    # Convert permalink to file path
                    # e.g., /en/skills/dev/tdd-developer/ -> docs/en/skills/dev/tdd-developer.md
                    peer_parts = peer_url.strip("/").split("/")
                    if len(peer_parts) >= 4:
                        peer_path = docs_dir / peer_parts[0] / "skills" / peer_parts[2] / f"{peer_parts[3]}.md"
                        if not peer_path.exists():
                            print(f"  ERROR: lang_peer target missing: {md_file} -> {peer_path}")
                            errors += 1

                # Check permalink matches file path
                perm_match = re.search(r"permalink:\s*(/[\w/-]+/)", fm_text)
                if perm_match:
                    perm_url = perm_match.group(1)
                    expected = f"/{lang}/skills/{cat_slug}/{skill_name}/"
                    if perm_url != expected:
                        print(f"  ERROR: permalink mismatch: {md_file} has {perm_url}, expected {expected}")
                        errors += 1

                # Check skill directory exists
                skill_dir = skills_dir / skill_name
                if not skill_dir.is_dir():
                    print(f"  ERROR: skill dir missing: {skill_dir}")
                    errors += 1

                has_pkg_button = "Download Skill Package" in text or "スキルパッケージをダウンロード" in text
                has_src_button = "View Source on GitHub" in text or "GitHubでソースを見る" in text

                if not has_src_button:
                    print(f"  ERROR: missing GitHub source button: {md_file}")
                    errors += 1

                if "<!-- TODO:" in text:
                    print(f"  ERROR: unfinished TODO marker remains: {md_file}")
                    errors += 1

                if "This page has not yet been translated into Japanese" in text:
                    print(f"  ERROR: untranslated JA note remains: {md_file}")
                    errors += 1

                if skill_packages_dir:
                    skill_file = skill_packages_dir / f"{skill_name}.skill"
                    if has_pkg_button and not skill_file.exists():
                        print(f"  ERROR: download button but no .skill file: {skill_file}")
                        errors += 1
                    if skill_file.exists() and not has_pkg_button:
                        print(f"  ERROR: missing package download button: {md_file}")
                        errors += 1

    skill_names = sorted(p.name for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    for skill_name in skill_names:
        category = _get_category(skill_name)

        for lang in ("en", "ja"):
            page_path = docs_dir / lang / "skills" / category / f"{skill_name}.md"
            if not page_path.exists():
                print(f"  ERROR: missing docs page: {page_path}")
                errors += 1

        if skill_packages_dir:
            skill_file = skill_packages_dir / f"{skill_name}.skill"
            if not skill_file.exists():
                print(f"  ERROR: missing .skill package: {skill_file}")
                errors += 1

    if errors == 0:
        print("  Validation passed: no errors found.")
    else:
        print(f"  Validation found {errors} error(s).")
    return errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate skill documentation pages")
    parser.add_argument("--skills-dir", type=Path, default=DEFAULT_SKILLS_DIR)
    parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    parser.add_argument("--skill", type=str, help="Generate for a single skill")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing pages")
    parser.add_argument(
        "--skill-packages-dir",
        type=Path,
        default=PROJECT_ROOT / "skill-packages",
        help="Path to skill-packages directory for download buttons",
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "full"],
        default="auto",
        help="Generation mode: 'auto' (6-section) or 'full' (10-section skeleton)",
    )
    parser.add_argument(
        "--add-buttons",
        action="store_true",
        help="Add download/source buttons to existing hand-written pages",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate docs pages for consistency",
    )
    args = parser.parse_args(argv)

    # Resolve skill-packages-dir (None if it doesn't exist)
    skill_packages_dir = args.skill_packages_dir if args.skill_packages_dir.is_dir() else None

    # --validate mode
    if args.validate:
        errors = validate_docs(args.docs_dir, args.skills_dir, skill_packages_dir)
        return 1 if errors > 0 else 0

    # --add-buttons mode
    if args.add_buttons:
        add_buttons_to_hand_written(args.docs_dir, skill_packages_dir)
        return 0

    # Discover skills
    skill_dirs = sorted(args.skills_dir.iterdir())
    if args.skill:
        skill_dirs = [args.skills_dir / args.skill]

    # Track per-category nav_order counters (start after existing max)
    nav_counters: dict[str, int] = {cat: mx for cat, mx in MAX_NAV_ORDER.items()}

    # Discover which skills to generate
    new_skills: list[str] = []
    for d in skill_dirs:
        if not d.is_dir() or not (d / "SKILL.md").exists():
            continue
        name = d.name
        if name in HAND_WRITTEN and not args.overwrite:
            continue
        new_skills.append(name)
    new_skills.sort()

    # Assign nav_orders per category
    nav_orders: dict[str, int] = {}
    for name in new_skills:
        cat = _get_category(name)
        nav_counters[cat] = nav_counters.get(cat, 0) + 1
        nav_orders[name] = nav_counters[cat]

    generated_en = 0
    generated_ja = 0
    skipped = 0

    for d in skill_dirs:
        if not d.is_dir() or not (d / "SKILL.md").exists():
            continue

        name = d.name

        if name in HAND_WRITTEN and not args.overwrite:
            skipped += 1
            continue

        category = _get_category(name)
        en_dir = args.docs_dir / "en" / "skills" / category
        ja_dir = args.docs_dir / "ja" / "skills" / category
        en_dir.mkdir(parents=True, exist_ok=True)
        ja_dir.mkdir(parents=True, exist_ok=True)

        en_path = en_dir / f"{name}.md"
        ja_path = ja_dir / f"{name}.md"

        if en_path.exists() and not args.overwrite:
            skipped += 1
            continue

        skill_data = parse_skill_md(d / "SKILL.md")
        nav_order = nav_orders.get(name, nav_counters.get(category, 99) + 1)
        resources = _list_skill_resources(d)

        if args.mode == "full":
            en_content = generate_en_full_page(
                name,
                skill_data,
                nav_order,
                resources,
                category,
                skill_packages_dir=skill_packages_dir,
            )
            ja_content = generate_ja_full_page(
                name,
                skill_data,
                nav_order,
                resources,
                category,
                skill_packages_dir=skill_packages_dir,
            )
        else:
            en_content = generate_en_page(
                name,
                skill_data,
                nav_order,
                resources,
                category,
                skill_packages_dir=skill_packages_dir,
            )
            ja_content = generate_ja_page(
                name,
                skill_data,
                nav_order,
                resources,
                category,
                skill_packages_dir=skill_packages_dir,
            )

        en_path.write_text(en_content, encoding="utf-8")
        generated_en += 1

        ja_path.write_text(ja_content, encoding="utf-8")
        generated_ja += 1

        print(f"  Generated: {name} -> {category}/ (EN + JA, mode={args.mode})")

    print(f"\nDone: {generated_en} EN + {generated_ja} JA generated, {skipped} skipped")

    # Update index pages with links to newly generated pages
    update_index_pages(args.skills_dir, args.docs_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
