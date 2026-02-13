"""Skill catalog - loads and provides metadata for all available skills.

Combines a curated YAML category file with auto-discovery of any skill
that exists on disk.  Skills defined in the YAML keep their category;
skills found on disk but absent from the YAML are placed in "Other".
"""

import logging
import re
from pathlib import Path

import yaml

from config.settings import SKILL_CATEGORIES_PATH, SKILLS_LIBRARY_PATH

logger = logging.getLogger(__name__)


def _parse_frontmatter_description(skill_md_path: Path) -> str:
    """Extract the 'description' field from SKILL.md YAML frontmatter."""
    try:
        text = skill_md_path.read_text(errors="replace")
        match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if match:
            fm = yaml.safe_load(match.group(1))
            if isinstance(fm, dict):
                desc = fm.get("description", "")
                if isinstance(desc, str):
                    # Take only the first sentence/line for brevity
                    first_line = desc.strip().split("\n")[0].strip()
                    return first_line[:200] if first_line else ""
    except Exception as e:
        logger.debug("Failed to parse frontmatter of %s: %s", skill_md_path, e)
    return ""


def load_skill_categories() -> dict:
    """Load skill categories from YAML configuration."""
    logger.debug("Loading skill categories from %s", SKILL_CATEGORIES_PATH)
    with open(SKILL_CATEGORIES_PATH, "r") as f:
        return yaml.safe_load(f)


def get_all_skills() -> list[dict]:
    """Return flat list of ALL skills with their category and description.

    1. Load curated skills from skill_categories.yaml (with assigned categories).
    2. Scan SKILLS_LIBRARY_PATH for any additional skills not in the YAML.
    3. Auto-discovered skills are placed in the "Other" category with their
       description extracted from SKILL.md frontmatter.
    """
    categories = load_skill_categories()
    skills = []
    known_names: set[str] = set()

    # 1. Curated skills from YAML
    for category_name, category_data in categories.get("categories", {}).items():
        for skill in category_data.get("skills", []):
            skills.append(
                {
                    "name": skill["name"],
                    "description": skill["description"],
                    "category": category_name,
                }
            )
            known_names.add(skill["name"])

    # 2. Auto-discover skills on disk that are not in the YAML
    if SKILLS_LIBRARY_PATH.is_dir():
        for skill_dir in sorted(SKILLS_LIBRARY_PATH.iterdir()):
            skill_md = skill_dir / "SKILL.md"
            if skill_dir.is_dir() and skill_md.exists() and skill_dir.name not in known_names:
                desc = _parse_frontmatter_description(skill_md)
                skills.append(
                    {
                        "name": skill_dir.name,
                        "description": desc or f"(Auto-discovered skill: {skill_dir.name})",
                        "category": "Other",
                    }
                )
                logger.info("Auto-discovered skill: %s", skill_dir.name)

    return skills


def get_skill_catalog_text() -> str:
    """Generate a formatted text catalog of all skills for the system prompt."""
    all_skills = get_all_skills()
    by_category: dict[str, list[dict]] = {}
    for s in all_skills:
        by_category.setdefault(s["category"], []).append(s)

    lines = []
    for category_name, cat_skills in by_category.items():
        lines.append(f"\n### {category_name}")
        for skill in cat_skills:
            lines.append(f"- **{skill['name']}**: {skill['description']}")
    return "\n".join(lines)


def load_skill_content(skill_name: str) -> str:
    """Load the full content of a skill (SKILL.md + key reference files).

    Args:
        skill_name: Name of the skill directory.

    Returns:
        Combined content of the skill's SKILL.md and reference files.
    """
    skill_dir = SKILLS_LIBRARY_PATH / skill_name
    if not skill_dir.is_dir():
        logger.warning("Skill '%s' not found at %s", skill_name, skill_dir)
        return f"Error: Skill '{skill_name}' not found."

    parts = []

    # Load SKILL.md
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text()
        logger.info("Loaded skill '%s' SKILL.md (%d bytes)", skill_name, len(content))
        parts.append(f"# Skill: {skill_name}\n\n{content}")

    # Load key reference files
    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        for ref_file in sorted(refs_dir.glob("*.md")):
            content = ref_file.read_text()
            # Limit each reference file to 3000 chars to avoid token explosion
            if len(content) > 3000:
                content = content[:3000] + "\n\n... (truncated)"
            parts.append(f"\n## Reference: {ref_file.name}\n\n{content}")

    return "\n\n---\n\n".join(parts) if parts else f"Skill '{skill_name}' has no content."


def list_skill_names() -> list[str]:
    """Return list of all skill directory names that exist on disk."""
    if not SKILLS_LIBRARY_PATH.is_dir():
        return []
    return sorted(
        d.name
        for d in SKILLS_LIBRARY_PATH.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    )
