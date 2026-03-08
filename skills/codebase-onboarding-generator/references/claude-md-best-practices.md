# CLAUDE.md Best Practices

This guide defines best practices for creating effective CLAUDE.md files that maximize Claude Code's ability to assist with a codebase.

## Purpose of CLAUDE.md

CLAUDE.md serves as the primary context document for Claude Code when working with a project. It should provide:

1. **Quick orientation** -- What the project does and how it's organized
2. **Actionable commands** -- Copy-pasteable commands for common tasks
3. **Conventions** -- Coding standards and patterns used in the project
4. **Gotchas** -- Non-obvious behaviors or project-specific quirks

## Essential Sections

### 1. Project Overview (Required)

Provide a 2-3 sentence description of what the project does. Include:
- Primary purpose and functionality
- Target users or use case
- Key technologies or frameworks

**Example:**
```markdown
## Project Overview

This is a FastAPI-based REST API for managing user authentication and authorization.
It provides JWT-based authentication, role-based access control, and integrates with
PostgreSQL for persistence.
```

### 2. Common Commands (Required)

List the most frequently used commands. Always use full paths and explicit flags.

**Essential command categories:**
- Install dependencies
- Run development server
- Run tests (with coverage if available)
- Build/compile
- Lint and format
- Database migrations (if applicable)

**Example:**
```markdown
## Common Commands

### Setup
```bash
# Install dependencies
pip install -e ".[dev]"

# Initialize database
python scripts/init_db.py
```

### Development
```bash
# Run development server
uvicorn app.main:app --reload --port 8000

# Run tests with coverage
pytest tests/ -v --cov=app --cov-report=term-missing
```

### Code Quality
```bash
# Format code
black . && isort .

# Run linter
ruff check . --fix
```
```

### 3. Directory Structure (Recommended)

Provide an annotated directory tree showing key directories and their purposes.

**Example:**
```markdown
## Directory Structure

```
project/
├── app/                  # Application source code
│   ├── api/              # API route handlers
│   ├── core/             # Configuration and security
│   ├── models/           # SQLAlchemy models
│   └── services/         # Business logic
├── tests/                # Test files (mirrors app/ structure)
├── scripts/              # Utility scripts
├── migrations/           # Alembic database migrations
└── docs/                 # Documentation
```
```

### 4. Architecture & Patterns (Recommended)

Document the architectural patterns and design decisions:
- Framework architecture (MVC, Clean Architecture, etc.)
- API conventions (REST, GraphQL)
- Data layer patterns (Repository, Active Record)
- Error handling approach
- Logging conventions

**Example:**
```markdown
## Architecture

### API Design
- RESTful endpoints following resource-based naming
- JSON responses with consistent error format: `{"error": {"code": "...", "message": "..."}}`
- All endpoints under `/api/v1/` prefix

### Data Layer
- Repository pattern: `app/repositories/` contains data access logic
- Models: SQLAlchemy ORM models in `app/models/`
- Migrations: Alembic migrations in `migrations/`
```

### 5. Coding Conventions (Recommended)

Document naming conventions and style guidelines:
- File naming (snake_case, kebab-case, PascalCase)
- Function/method naming
- Class naming
- Variable naming
- Documentation style (docstrings, comments)

**Example:**
```markdown
## Coding Conventions

### Naming
- Files: `snake_case.py`
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

### Documentation
- Google-style docstrings for all public functions
- Type hints required for function signatures
- README.md required for each package directory
```

### 6. Testing (Recommended)

Document the testing approach:
- Test framework and plugins
- Test file organization
- Fixture locations
- How to run specific tests

**Example:**
```markdown
## Testing

### Framework
- pytest with pytest-asyncio for async tests
- Fixtures in `tests/conftest.py` and per-directory `conftest.py`
- Factory Boy for test data generation

### Running Tests
```bash
# All tests
pytest tests/ -v

# Specific module
pytest tests/api/test_users.py -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```
```

### 7. Environment Variables (When Applicable)

List required environment variables without exposing actual values.

**Example:**
```markdown
## Environment Variables

Required environment variables (set in `.env` or export):

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://user:pass@localhost/db |
| JWT_SECRET | Secret key for JWT signing | (generate with `openssl rand -hex 32`) |
| DEBUG | Enable debug mode | true/false |
```

## Anti-Patterns to Avoid

### 1. Hardcoded Absolute Paths

**Bad:**
```markdown
Run tests: `/Users/john/projects/myapp/run_tests.sh`
```

**Good:**
```markdown
Run tests: `pytest tests/ -v`
```

### 2. Secrets or Credentials

**Never include:**
- API keys
- Passwords
- Connection strings with credentials
- Private keys

### 3. Outdated Information

Keep CLAUDE.md synchronized with actual project state. Outdated commands cause confusion.

### 4. Excessive Detail

CLAUDE.md should be concise. Link to detailed documentation rather than duplicating it.

**Bad:**
```markdown
## API Documentation
[500 lines of API endpoint details]
```

**Good:**
```markdown
## API Documentation
See `docs/api.md` for complete API reference.
```

### 5. Vague Instructions

**Bad:**
```markdown
Run the appropriate test command for your environment.
```

**Good:**
```markdown
```bash
pytest tests/ -v --cov=app
```
```

## Section Priority

When generating CLAUDE.md, prioritize sections based on usefulness:

| Priority | Section | Why |
|----------|---------|-----|
| 1 | Common Commands | Most frequently referenced |
| 2 | Directory Structure | Essential for navigation |
| 3 | Architecture | Prevents design mistakes |
| 4 | Coding Conventions | Ensures consistent code |
| 5 | Testing | Enables confident changes |
| 6 | Environment Variables | Required for setup |
| 7 | Project Overview | Context setting |

## Language and Tone

- Use imperative mood: "Run tests" not "You should run tests"
- Be concise: One sentence per concept
- Use code blocks liberally
- Prefer examples over explanations
- Use tables for structured information

## Maintenance

CLAUDE.md should be updated when:
- Build process changes
- New major dependencies added
- Architecture evolves
- Directory structure changes significantly
- New team conventions established

## Template

A minimal CLAUDE.md template:

```markdown
# CLAUDE.md

## Project Overview

[2-3 sentences describing the project]

## Common Commands

```bash
# Install dependencies
[command]

# Run development server
[command]

# Run tests
[command]

# Lint/format
[command]
```

## Directory Structure

```
project/
├── src/          # [description]
├── tests/        # [description]
└── [other dirs]
```

## Architecture

[Key architectural decisions and patterns]

## Coding Conventions

[Naming conventions, style guidelines]

## Testing

[Test framework, how to run tests, fixture locations]
```
