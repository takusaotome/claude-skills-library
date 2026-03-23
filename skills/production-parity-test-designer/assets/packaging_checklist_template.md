# Packaging and Dependency Integrity Checklist

Verify that the built artifact (package, container image, installer) faithfully reproduces the development and test environment. Complete this checklist before every release.

## Instructions

1. Fill in one row per dependency file or build artifact
2. Verify each column by running the specified check
3. Mark Pass/Fail/N-A for each check
4. Any Fail blocks the release until resolved

## Dependency File Inventory

| # | Dependency File | Install Command | Location in Artifact | Verified? |
|---|----------------|----------------|---------------------|:---------:|
| 1 | `requirements.txt` | `pip install -r requirements.txt` | `/app/requirements.txt` | Pass |
| 2 | `package.json` + `package-lock.json` | `npm ci` | `/app/package.json` | Pass |
| 3 | `Gemfile` + `Gemfile.lock` | `bundle install --frozen` | `/app/Gemfile` | N/A |
| 4 | `go.mod` + `go.sum` | `go mod download` | `/app/go.mod` | N/A |
| 5 | | | | |

## Install Path Verification

| # | Component | Expected Install Path | Verification Command | Result |
|---|-----------|----------------------|---------------------|--------|
| 1 | Python packages | `/usr/local/lib/python3.11/site-packages/` | `pip show mypackage` | Pass |
| 2 | Node modules | `/app/node_modules/` | `ls node_modules/.package-lock.json` | Pass |
| 3 | System libraries | `/usr/lib/x86_64-linux-gnu/` | `ldconfig -p \| grep libpq` | Pass |
| 4 | Binary tools | `/usr/local/bin/` | `which gunicorn` | Pass |
| 5 | | | | |

## Import Smoke Verification

| # | Module | Import Command | Expected Result | Actual Result | Status |
|---|--------|---------------|-----------------|---------------|--------|
| 1 | `myapp` | `python -c "import myapp"` | Exit code 0 | Exit code 0 | Pass |
| 2 | `myapp.api` | `python -c "from myapp import api"` | Exit code 0 | Exit code 0 | Pass |
| 3 | `myapp.models` | `python -c "from myapp import models"` | Exit code 0 | Exit code 0 | Pass |
| 4 | `psycopg2` | `python -c "import psycopg2"` | Exit code 0 | Exit code 0 | Pass |
| 5 | `PIL` | `python -c "from PIL import Image"` | Exit code 0 | ImportError: libjpeg | Fail |
| 6 | | | | | |

## Runtime Command Verification

| # | Command | Purpose | Expected Output | Actual Output | Status |
|---|---------|---------|-----------------|---------------|--------|
| 1 | `myapp --version` | CLI entry point works | Version string printed | `myapp 1.2.3` | Pass |
| 2 | `gunicorn myapp:app --check-config` | WSGI server can load app | Config OK | Config OK | Pass |
| 3 | `celery -A myapp.tasks inspect ping` | Task worker can connect | Pong response | Pong response | Pass |
| 4 | `python -m myapp.migrate --check` | Migrations are current | No pending migrations | No pending migrations | Pass |
| 5 | | | | | |

## Container Image Parity

| # | Check | Development | Production Image | Match? | Notes |
|---|-------|-------------|-----------------|:------:|-------|
| 1 | Python version | 3.11.7 | 3.11.7 | Yes | Pin in Dockerfile `FROM python:3.11.7-slim` |
| 2 | OS base | macOS 14.2 | Debian 12 (bookworm) | Expected | Different OS is expected; test on Linux CI |
| 3 | PostgreSQL client | 15.4 | 15.4 | Yes | Installed via `apt-get` in Dockerfile |
| 4 | Timezone | Local (JST) | UTC | Expected | Verify `TZ=UTC` in container env |
| 5 | Locale | `en_US.UTF-8` | `C.UTF-8` | No | Add `ENV LANG=en_US.UTF-8` to Dockerfile |
| 6 | System libraries | Homebrew-managed | apt-managed | Expected | Verify all required libs in Dockerfile |
| 7 | Container user | `$(whoami)` | `appuser` (non-root) | Expected | Verify `USER appuser` in Dockerfile |
| 8 | | | | | |

## Environment Secrets Dependency

| # | Environment Variable | Required At | Default If Missing | Verified In CI? | Notes |
|---|---------------------|-------------|-------------------|:---------------:|-------|
| 1 | `DATABASE_URL` | Runtime | None (app crashes) | Yes | CI uses test DB URL |
| 2 | `SECRET_KEY` | Runtime | None (app crashes) | Yes | CI uses dummy key |
| 3 | `API_KEY` | Runtime | Falls back to demo mode | No | Add startup validation |
| 4 | `SENTRY_DSN` | Runtime | No error reporting | N/A | Optional in CI |
| 5 | `AWS_ACCESS_KEY_ID` | Runtime (if using S3) | None (S3 calls fail) | No | Use localstack in CI |
| 6 | | | | | |

## Lockfile Alignment Check

| # | Check | Command | Expected | Actual | Status |
|---|-------|---------|----------|--------|--------|
| 1 | Lockfile exists in repo | `git ls-files requirements.txt` | Listed | Listed | Pass |
| 2 | Lockfile is current | `pip freeze \| diff - requirements.txt` | No diff | No diff | Pass |
| 3 | CI uses locked install | Check CI config for `pip install -r` | Uses locked | Uses locked | Pass |
| 4 | No floating versions | `grep -E "[><=~^]" requirements.txt` | No matches | No matches | Pass |
| 5 | Dockerfile uses same install | Check Dockerfile `RUN pip install` | Matches CI | Matches CI | Pass |
| 6 | | | | | |

## Pre-Release Sign-Off

| Check Category | All Passed? | Reviewer | Date |
|---------------|:-----------:|---------|------|
| Dependency Files | | | |
| Install Paths | | | |
| Import Smoke | | | |
| Runtime Commands | | | |
| Image Parity | | | |
| Env Secrets | | | |
| Lockfile Alignment | | | |

**Release Approved**: [ ] Yes / [ ] No -- Requires remediation

**Blocking Issues** (if any):

| Issue | Severity | Remediation Plan | ETA |
|-------|----------|-----------------|-----|
| | | | |
