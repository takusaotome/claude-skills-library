"""Custom MCP tools for the presentation agent."""

from typing import Any

from claude_agent_sdk import tool, create_sdk_mcp_server, query, ClaudeAgentOptions

from skills.catalog import get_all_skills, load_skill_content
from converter.marp import convert_marp_to_pdf, convert_marp_to_html
from config.settings import SKILLS_LIBRARY_PATH


def _load_checklist() -> str:
    """Load the presentation best practices checklist."""
    path = (
        SKILLS_LIBRARY_PATH
        / "fujisoft-presentation-creator"
        / "references"
        / "presentation_best_practices_checklist.md"
    )
    if path.exists():
        return path.read_text()
    return "(Checklist not found)"


# --- Skill tools ---


@tool(
    "list_skills",
    "List all available domain expert skills with their descriptions and categories. "
    "Use this to discover which skills can provide specialized knowledge for the presentation topic.",
    {},
)
async def list_skills(args: dict[str, Any]) -> dict[str, Any]:
    skills = get_all_skills()
    lines = []
    current_category = None
    for s in sorted(skills, key=lambda x: x["category"]):
        if s["category"] != current_category:
            current_category = s["category"]
            lines.append(f"\n## {current_category}")
        lines.append(f"- **{s['name']}**: {s['description']}")
    text = "\n".join(lines)
    return {"content": [{"type": "text", "text": text}]}


@tool(
    "load_skill",
    "Load specialized domain knowledge from a skill. "
    "This reads the skill's SKILL.md and reference documents to provide expert knowledge "
    "that should inform the presentation content. Use this before generating slides "
    "when the topic requires domain expertise (e.g., financial analysis, compliance, strategy).",
    {"skill_name": str},
)
async def load_skill(args: dict[str, Any]) -> dict[str, Any]:
    skill_name = args.get("skill_name", "")
    content = load_skill_content(skill_name)
    return {"content": [{"type": "text", "text": content}]}


# --- Conversion tools ---


@tool(
    "convert_to_pdf",
    "Convert MARP Markdown content to a PDF file. "
    "Pass the complete MARP Markdown (including CSS frontmatter) and a filename. "
    "Returns the path to the generated PDF.",
    {"markdown_content": str, "filename": str},
)
async def convert_to_pdf(args: dict[str, Any]) -> dict[str, Any]:
    markdown_content = args.get("markdown_content", "")
    filename = args.get("filename", "presentation")
    try:
        pdf_path = convert_marp_to_pdf(markdown_content, filename)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"PDF generated successfully: {pdf_path}",
                }
            ]
        }
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"PDF conversion failed: {e}"}],
            "is_error": True,
        }


@tool(
    "convert_to_html",
    "Convert MARP Markdown content to an HTML file for preview. "
    "Pass the complete MARP Markdown and a filename. Returns the path to the generated HTML.",
    {"markdown_content": str, "filename": str},
)
async def convert_to_html(args: dict[str, Any]) -> dict[str, Any]:
    markdown_content = args.get("markdown_content", "")
    filename = args.get("filename", "presentation")
    try:
        html_path = convert_marp_to_html(markdown_content, filename)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"HTML generated successfully: {html_path}",
                }
            ]
        }
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"HTML conversion failed: {e}"}],
            "is_error": True,
        }


# --- Review tools ---

STRUCTURE_REVIEWER_PROMPT = """You are a Presentation Structure Reviewer.
Your job is to critically review a proposed slide structure BEFORE it gets turned into actual slides.

## Review Criteria (from the Presentation Best Practices Checklist)

### Story & Logic Flow
- Is the structure logical? (Introduction → Problem → Solution → Impact → Call to Action)
- Does each slide focus on ONE key message?
- Is there an Executive Summary that conveys the conclusion in 60 seconds?
- Are sections clearly delineated with navigation cues?

### Audience Alignment
- Does the content depth match the audience's knowledge level?
- Are technical terms appropriate for the audience?
- Does the structure address what the audience cares about most?

### Message Consistency
- Are the 2-3 key messages woven throughout the structure?
- Is there a clear "so what?" for each slide?
- Does the flow build a compelling argument?

### Completeness
- Are there any obvious gaps the audience would expect to see?
- Is there a clear call to action / next steps?
- Are risks and mitigation addressed (if applicable)?

### Slide Count & Timing
- Is the number of slides appropriate for the time slot?
- Guy Kawasaki 10-20-30 rule: ~10 slides for 20 minutes

## Output Format

Respond with a structured review:

### Strengths
- (what's good about this structure)

### Improvements Needed
- (specific, actionable suggestions - say WHAT to change and WHERE)

### Critical Issues
- (anything that must be fixed before proceeding, or "None")

### Revised Structure Suggestion
- (if improvements are needed, suggest the revised outline)
"""

DESIGN_REVIEWER_PROMPT = """You are a Presentation Design Reviewer for FUJISOFT America.
Your job is to review generated MARP Markdown slides for visual quality and design best practices.

## FUJISOFT Template CSS Classes Available
- Page classes: cover, content, thankyou
- Info boxes: .info-box, .success-box, .warning-box, .error-box
- Metrics: .metric-grid, .metric-box (.metric-green, .metric-blue, .metric-orange, .metric-red)
- Step cards: .step-card, .step-number, .step-content
- Timeline: .timeline-item, .timeline-badge
- Badges: .badge, .success-badge, .warning-badge
- Grid layouts: .grid-2, .grid-3, .grid-4
- Two-column: .two-column > .column
- ROI display: .roi-box, .summary-box

## Review Criteria

### Visual Design
- Font sizes readable (headings 36-60pt, body 24-30pt)
- Visual hierarchy clear (important elements are prominent)
- Consistent use of brand colors (#1a237e primary, #3949ab secondary)
- Effective use of whitespace

### CSS Quality (CRITICAL)
- NO box-shadow anywhere (causes gray rectangles in PDF) - use border instead
- Template CSS classes used correctly
- No inline styles that conflict with template

### Content Density
- Tables: max 5 rows (excluding header)
- Bullet lists: max 8 items per slide
- One message per slide

### Footer & Layout
- Footer clearance: at least 100px from last content element to footer
- Footer present on every content/thankyou page with correct 3 elements
- Page numbers sequential and correct

### 10-Second Scan Rule
- Can each slide's key point be understood in 10 seconds?
- Are key numbers and takeaways visually prominent?

### Design Element Usage
- Are info-boxes, metric-grids, step-cards used where appropriate?
- Would plain bullet lists benefit from visual treatment?
- Are grids and columns used to organize related information?

## Output Format

For EACH slide, provide:
- **Slide N: [Title]** — Score: X/100
- Issues found (if any)
- Specific fix instructions (use exact CSS class names or markdown syntax)

Then provide:
### Overall Score: X/100
### Critical Issues (must fix before PDF generation)
### Recommended Improvements (nice to have)
"""


@tool(
    "review_structure",
    "Review a proposed slide structure before generating slides. "
    "Pass the structure outline and the context from the hearing phase "
    "(purpose, audience, key messages). Returns expert feedback with "
    "strengths, improvements needed, and critical issues. "
    "Use this AFTER proposing a structure and BEFORE generating MARP markdown.",
    {"structure": str, "context": str},
)
async def review_structure(args: dict[str, Any]) -> dict[str, Any]:
    structure = args.get("structure", "")
    context = args.get("context", "")

    review_prompt = (
        f"## Presentation Context\n\n{context}\n\n"
        f"## Proposed Slide Structure\n\n{structure}\n\n"
        "Review this structure thoroughly and provide your assessment."
    )

    try:
        response_parts = []
        async for message in query(
            prompt=review_prompt,
            options=ClaudeAgentOptions(
                system_prompt=STRUCTURE_REVIEWER_PROMPT,
                allowed_tools=[],
                max_turns=1,
            ),
        ):
            if hasattr(message, "content"):
                for block in message.content:
                    if hasattr(block, "text"):
                        response_parts.append(block.text)

        review_text = "\n".join(response_parts) if response_parts else "No review generated."
        return {"content": [{"type": "text", "text": review_text}]}
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"Structure review failed: {e}"}],
            "is_error": True,
        }


@tool(
    "review_design",
    "Review generated MARP Markdown slides for visual design quality. "
    "Pass the complete MARP Markdown content. Returns per-slide scores, "
    "critical issues, and specific improvement instructions. "
    "Use this AFTER generating slides and BEFORE converting to PDF. "
    "Fix any critical issues before calling convert_to_pdf.",
    {"marp_markdown": str},
)
async def review_design(args: dict[str, Any]) -> dict[str, Any]:
    marp_markdown = args.get("marp_markdown", "")
    checklist = _load_checklist()

    review_prompt = (
        f"## Best Practices Checklist\n\n{checklist}\n\n"
        f"## MARP Markdown to Review\n\n```markdown\n{marp_markdown}\n```\n\n"
        "Review every slide in detail and provide your assessment."
    )

    try:
        response_parts = []
        async for message in query(
            prompt=review_prompt,
            options=ClaudeAgentOptions(
                system_prompt=DESIGN_REVIEWER_PROMPT,
                allowed_tools=[],
                max_turns=1,
            ),
        ):
            if hasattr(message, "content"):
                for block in message.content:
                    if hasattr(block, "text"):
                        response_parts.append(block.text)

        review_text = "\n".join(response_parts) if response_parts else "No review generated."
        return {"content": [{"type": "text", "text": review_text}]}
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"Design review failed: {e}"}],
            "is_error": True,
        }


def create_presentation_tools_server():
    """Create the MCP server with all presentation tools."""
    return create_sdk_mcp_server(
        name="presentation-tools",
        version="2.0.0",
        tools=[
            list_skills,
            load_skill,
            convert_to_pdf,
            convert_to_html,
            review_structure,
            review_design,
        ],
    )
