"""Skill router - maps topics to relevant skills based on keyword matching."""

import yaml

from config.settings import SKILL_CATEGORIES_PATH


def load_categories() -> dict:
    """Load category configuration."""
    with open(SKILL_CATEGORIES_PATH, "r") as f:
        return yaml.safe_load(f)


def suggest_skills(user_message: str) -> list[dict]:
    """Suggest relevant skills based on keyword matching against user message.

    This is a lightweight helper. The Agent itself makes the final decision
    on which skills to load via the load_skill tool.

    Args:
        user_message: The user's request text.

    Returns:
        List of matching skill dicts with name, description, and category.
    """
    categories = load_categories()
    message_lower = user_message.lower()
    matched = []
    seen = set()

    for category_name, category_data in categories.get("categories", {}).items():
        keywords = [kw.lower() for kw in category_data.get("keywords", [])]
        if any(kw in message_lower for kw in keywords):
            for skill in category_data.get("skills", []):
                if skill["name"] not in seen:
                    matched.append(
                        {
                            "name": skill["name"],
                            "description": skill["description"],
                            "category": category_name,
                        }
                    )
                    seen.add(skill["name"])

    return matched
