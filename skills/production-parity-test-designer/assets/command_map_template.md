# Standard Test Command Map

Define named test commands for each execution context. Every developer, CI pipeline, and release process should use these exact commands to ensure consistency.

## Instructions

1. Define one command per execution context (local, PR CI, nightly, staging, release)
2. Specify which test tiers are included in each command
3. Map commands to environments (local workstation, CI runner, staging server, etc.)
4. Assign an owner responsible for maintaining each command
5. Include the exact command syntax -- no ambiguity

## Command Map

| # | Command Name | Command Syntax | Scope / Description | Test Tiers Included | Environment | Runtime Budget | Owner |
|---|-------------|---------------|--------------------|--------------------|-------------|---------------|-------|
| 1 | `test:local` | `pytest tests/ -m "unit or integration" --timeout=120 -q` | Developer runs during coding for fast feedback | Unit + Integration (core) | Local workstation with Docker Compose (PostgreSQL) | 2 min | All developers |
| 2 | `test:smoke` | `pytest tests/ -m smoke --timeout=180 -v` | PR-required smoke suite gating every merge | Smoke (DB dialect + import + persistence + timezone + serialization) | CI runner with PostgreSQL 15 service container | 3 min | CI/DevOps team |
| 3 | `test:pr` | `make lint && pytest tests/ -m "unit or smoke" --timeout=300 -v` | Full PR CI pipeline (lint + unit + smoke) | Lint + Type Check + Unit + Smoke | CI runner with PostgreSQL 15 service container | 5 min | CI/DevOps team |
| 4 | `test:nightly` | `pytest tests/ -m "not slow_e2e" --timeout=1800 -v --tb=long` | Comprehensive nightly parity suite | Unit + Integration (full) + Smoke + Adversarial Regression | CI runner with PostgreSQL 15 + Redis + full service stack | 30 min | QA team |
| 5 | `test:e2e` | `pytest tests/e2e/ --timeout=900 -v --base-url=$STAGING_URL` | End-to-end tests against staging environment | E2E (UI + API + persistence verification) | Staging environment (deployed application) | 15 min | QA team |
| 6 | `test:packaging` | `docker build -t myapp:test . && docker run --rm myapp:test python -c "from myapp import main" && docker run --rm myapp:test myapp --version` | Build artifact verification before release | Packaging (build + import smoke + CLI smoke + health check) | CI runner with Docker | 3 min | DevOps team |
| 7 | `test:release` | `make test:pr && make test:packaging && make test:e2e` | Full release verification pipeline | All tiers combined | CI + Staging | 25 min | Release manager |

## Execution Context Matrix

Mark which commands run in each context:

| Command | Local Dev | PR CI | Nightly CI | Pre-Staging | Pre-Release |
|---------|:---------:|:-----:|:----------:|:-----------:|:-----------:|
| `test:local` | Yes | -- | -- | -- | -- |
| `test:smoke` | Optional | Yes | Yes | Yes | Yes |
| `test:pr` | Optional | Yes | Yes | Yes | Yes |
| `test:nightly` | -- | -- | Yes | -- | Yes |
| `test:e2e` | -- | -- | Optional | Yes | Yes |
| `test:packaging` | -- | -- | Optional | -- | Yes |
| `test:release` | -- | -- | -- | -- | Yes |

## Marker Definitions

Define pytest markers (or equivalent test framework tags) for each tier:

```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
markers = [
    "unit: Pure logic tests, no I/O (fast, deterministic)",
    "integration: Tests requiring real external services (DB, cache)",
    "smoke: Minimum production parity checks for PR CI",
    "e2e: Full end-to-end workflow tests",
    "packaging: Build and install verification tests",
    "adversarial: Regression tests from past defects and attack patterns",
    "slow_e2e: E2E tests too slow for nightly (staging only)",
    "nightly: Tests that run on nightly schedule only",
]
```

## CI Pipeline Integration

### GitHub Actions Example

```yaml
name: Test Pipeline
on:
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 2 * * *'  # Nightly at 2 AM UTC

jobs:
  pr-tests:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_PASSWORD: test_pass
        ports: ['5432:5432']
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: make test:pr

  nightly-tests:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_PASSWORD: test_pass
        ports: ['5432:5432']
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: make test:nightly
```

### Makefile Integration

```makefile
.PHONY: test test:local test:smoke test:pr test:nightly test:e2e test:packaging test:release

test: test:local

test\:local:
	pytest tests/ -m "unit or integration" --timeout=120 -q

test\:smoke:
	pytest tests/ -m smoke --timeout=180 -v

test\:pr: lint
	pytest tests/ -m "unit or smoke" --timeout=300 -v

test\:nightly:
	pytest tests/ -m "not slow_e2e" --timeout=1800 -v --tb=long

test\:e2e:
	pytest tests/e2e/ --timeout=900 -v --base-url=$(STAGING_URL)

test\:packaging:
	docker build -t myapp:test .
	docker run --rm myapp:test python -c "from myapp import main"
	docker run --rm myapp:test myapp --version

test\:release: test:pr test:packaging test:e2e

lint:
	ruff check src/ tests/
	mypy src/ --strict
```

## Runtime Monitoring

Track actual vs budgeted runtime to detect drift:

| Command | Budgeted | Last Actual | Trend | Action Needed? |
|---------|----------|-------------|-------|:--------------:|
| `test:local` | 2 min | | | |
| `test:smoke` | 3 min | | | |
| `test:pr` | 5 min | | | |
| `test:nightly` | 30 min | | | |
| `test:e2e` | 15 min | | | |
| `test:packaging` | 3 min | | | |
| `test:release` | 25 min | | | |

**Action triggers**:
- If actual exceeds budget by 20%, investigate and optimize
- If actual exceeds budget by 50%, demote slow tests to a lower-frequency tier
- If actual is consistently under 50% of budget, consider promoting more tests to this tier

## Ownership and Maintenance

| Command | Primary Owner | Backup Owner | Last Reviewed | Next Review |
|---------|--------------|-------------|---------------|-------------|
| `test:local` | | | | |
| `test:smoke` | | | | |
| `test:pr` | | | | |
| `test:nightly` | | | | |
| `test:e2e` | | | | |
| `test:packaging` | | | | |
| `test:release` | | | | |

Review cadence: Monthly or after any production incident that a test should have caught.
