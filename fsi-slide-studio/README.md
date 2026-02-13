# FSI Slide Studio

A Streamlit chat application that generates professional FUJISOFT America-branded presentations using the Claude Agent SDK and 30+ domain expert skills.

## Features

- Chat-based presentation generation with a 5-phase workflow (hearing, structure proposal, structure review, slide generation, design review)
- Dynamic skill loading from 30+ domain expert skills (Strategy, Finance, Operations, Compliance, IT, Analytics, and more)
- MARP Markdown to PDF/HTML conversion with FUJISOFT America corporate template
- Automated structure review and design review via independent AI reviewers
- Token-level streaming display for real-time response rendering
- IME composition fix for Japanese/Chinese input
- Bilingual support (English / Japanese)

## Architecture

```
Streamlit (Chat UI + IME fix + Streaming)
    |
AsyncBridge (Persistent event loop)
    |
Claude Agent SDK (Multi-turn + 6 MCP tools)
    |
Skill Library (30+ domain skills + MARP template)
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js (for marp-cli)
- Anthropic API key

### Installation

```bash
cd fsi-slide-studio
pip install -r requirements.txt
npm install -g @marp-team/marp-cli
```

### Environment Setup

```bash
cp .env.example .env
# Edit .env and set your ANTHROPIC_API_KEY
```

### Run

```bash
streamlit run app.py
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | (required) | Anthropic API key |
| `CLAUDE_MODEL` | `claude-sonnet-4-5-20250929` | Claude model to use |
| `LOG_LEVEL` | `INFO` | Logging level |
| `SKILLS_LIBRARY_PATH` | `../skills` | Path to the skills library directory |

## Docker Deployment

```bash
docker build -t fsi-slide-studio .
docker run -p 8501:8501 --env-file .env fsi-slide-studio
```

## Render Deployment

The included `render.yaml` provides configuration for deploying on Render with Docker runtime. Set the `ANTHROPIC_API_KEY` environment variable in the Render dashboard.

## Project Structure

```
fsi-slide-studio/
├── app.py                    # Streamlit main app (IME fix, AsyncBridge, streaming)
├── agent/
│   ├── __init__.py
│   ├── async_bridge.py       # Persistent event loop bridge
│   ├── client.py             # Claude Agent SDK client management
│   ├── system_prompt.py      # System prompt builder
│   └── tools.py              # Custom MCP tools (6 tools)
├── skills/
│   ├── __init__.py
│   ├── router.py             # Skill routing (keyword matching)
│   └── catalog.py            # Skill catalog (YAML loader + content loader)
├── converter/
│   ├── __init__.py
│   └── marp.py               # MARP CLI wrapper (PDF + HTML)
├── config/
│   ├── settings.py           # App settings
│   └── skill_categories.yaml # Skill category mappings
├── tests/                    # Unit tests (76 tests)
├── output/                   # Generated files
├── logs/                     # Application logs
├── Dockerfile
├── render.yaml
├── requirements.txt
├── pyproject.toml
└── DESIGN.md                 # Detailed design document
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `list_skills` | List all available domain expert skills with descriptions and categories |
| `load_skill` | Load specialized domain knowledge from a skill's SKILL.md and references |
| `convert_to_pdf` | Convert MARP Markdown content to a PDF file |
| `convert_to_html` | Convert MARP Markdown content to an HTML file for preview |
| `review_structure` | Review a proposed slide structure before generation |
| `review_design` | Review generated MARP Markdown slides for design quality |

## Testing

```bash
# Run all tests
python3.11 -m pytest tests/ -v

# With coverage report
python3.11 -m pytest tests/ --cov=. --cov-report=term-missing
```

## Design Document

See [DESIGN.md](DESIGN.md) for detailed architecture, workflow design, and design decisions.
