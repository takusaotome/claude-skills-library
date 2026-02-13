"""Skill catalog - loads and provides metadata for all available skills."""

import logging
from pathlib import Path

import yaml

from config.settings import SKILL_CATEGORIES_PATH, SKILLS_LIBRARY_PATH

logger = logging.getLogger(__name__)


def load_skill_categories() -> dict:
    """Load skill categories from YAML configuration."""
    logger.debug("Loading skill categories from %s", SKILL_CATEGORIES_PATH)
    with open(SKILL_CATEGORIES_PATH, "r") as f:
        return yaml.safe_load(f)


def get_all_skills() -> list[dict]:
    """Return flat list of all skills with their category and description."""
    categories = load_skill_categories()
    skills = []
    for category_name, category_data in categories.get("categories", {}).items():
        for skill in category_data.get("skills", []):
            skills.append(
                {
                    "name": skill["name"],
                    "description": skill["description"],
                    "category": category_name,
                }
            )
    return skills


def get_skill_catalog_text() -> str:
    """Generate a formatted text catalog of all skills for the system prompt."""
    categories = load_skill_categories()
    lines = []
    for category_name, category_data in categories.get("categories", {}).items():
        lines.append(f"\n### {category_name}")
        for skill in category_data.get("skills", []):
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
