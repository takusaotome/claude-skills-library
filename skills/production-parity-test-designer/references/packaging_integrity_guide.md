# Packaging Integrity Guide

A comprehensive guide to verifying that built artifacts (packages, containers, installers) faithfully reproduce the development and test environment in production. This guide covers runtime dependency verification, container build validation, import smoke testing, lockfile alignment, and install method parity.

## Why Packaging Integrity Matters

The gap between "tests pass" and "production works" often lives in the packaging and deployment pipeline. Common failures include:

- All tests pass against source code, but the built package is missing a module
- Docker image builds successfully, but the container crashes on start due to a missing native library
- `pip install mypackage` succeeds, but `import mypackage.submodule` fails because a data file was not included
- CI uses `npm install` but production uses `npm ci` with a stale lockfile
- Development uses Python 3.11 but the production container has Python 3.9

These failures are invisible to unit, integration, and E2E tests because those tests run against the source tree, not the built artifact.

## Runtime Dependency Verification

### Python Packages

#### Requirements File Completeness

Every module imported in source code must appear in the dependency specification.

**Verification method**:
```bash
# Find all imports in source code
grep -rn "^import \|^from " src/ --include="*.py" | \
  awk '{print $2}' | sort -u > /tmp/source_imports.txt

# Compare against requirements.txt / pyproject.toml
# Flag any import not covered by a declared dependency
```

**Common gaps**:
- Development-only packages used in production code (e.g., `pytest` fixtures imported at runtime)
- Transitive dependencies relied upon directly (works when parent package is installed, breaks if parent changes)
- Standard library modules that moved between Python versions (`asyncio`, `tomllib`)
- Platform-specific packages (`pywin32`, `readline` vs `gnureadline`)

#### Native Extension Verification

Some Python packages require system-level libraries to be installed.

| Package | Required System Library | Install Command (Debian/Ubuntu) |
|---------|------------------------|--------------------------------|
| `psycopg2` | `libpq-dev` | `apt-get install libpq-dev` |
| `Pillow` | `libjpeg-dev`, `zlib1g-dev` | `apt-get install libjpeg-dev zlib1g-dev` |
| `cryptography` | `libssl-dev`, `libffi-dev` | `apt-get install libssl-dev libffi-dev` |
| `lxml` | `libxml2-dev`, `libxslt1-dev` | `apt-get install libxml2-dev libxslt1-dev` |
| `mysqlclient` | `libmysqlclient-dev` | `apt-get install libmysqlclient-dev` |
| `cv2` (OpenCV) | `libgl1-mesa-glx` | `apt-get install libgl1-mesa-glx` |

**Verification method**:
```bash
# In a clean container, install packages and verify imports
pip install -r requirements.txt
python -c "import psycopg2; import PIL; import cv2; print('All imports OK')"
```

### Node.js Packages

#### lockfile Integrity

```bash
# Verify lockfile is up-to-date with package.json
npm ci  # Fails if lockfile doesn't match package.json (GOOD)
# Never use `npm install` in CI/production -- it modifies lockfile
```

**Common gaps**:
- `package-lock.json` committed but stale (last `npm install` not committed)
- `yarn.lock` and `package-lock.json` both present (which is authoritative?)
- `optionalDependencies` that install on macOS but skip on Linux
- `peerDependencies` not installed in production (npm 7+ auto-installs, older versions do not)

#### Native Module Build

```bash
# Verify native modules build in production environment
npm rebuild  # Recompiles native addons for current platform
node -e "require('sharp'); require('bcrypt'); console.log('Native modules OK')"
```

### General Dependency Principles

1. **Lockfile is the source of truth**: Never allow package installation to resolve versions at install time in CI or production
2. **Exact version pinning**: Use `==` (Python) or exact versions in lockfile (Node.js)
3. **Reproducible installs**: `pip install -r requirements.txt` and `npm ci` must produce identical results every time
4. **No implicit dependencies**: If you import it, you must declare it

## Container Build Validation

### Dockerfile Best Practices for Testability

```dockerfile
# Multi-stage build: test stage validates before production stage
FROM python:3.11-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Test stage: run import smoke and health check
FROM base AS test
COPY . .
RUN python -c "from myapp import main; print('Import smoke: OK')"
RUN python -m pytest tests/smoke/ -v --timeout=60

# Production stage: only if test stage passes
FROM base AS production
COPY . .
EXPOSE 8000
CMD ["gunicorn", "myapp:app", "--bind", "0.0.0.0:8000"]
```

### Container Validation Checklist

| Check | Command | What It Catches |
|-------|---------|----------------|
| Image builds | `docker build -t myapp .` | Syntax errors, missing files, build failures |
| Container starts | `docker run --rm myapp echo "OK"` | Missing entrypoint, broken CMD |
| Health check passes | `curl http://localhost:8000/health` | Missing dependencies, config errors |
| Import smoke | `docker run --rm myapp python -c "import myapp"` | Missing packages in image |
| CLI smoke | `docker run --rm myapp myapp --version` | Broken entry points |
| Correct user | `docker run --rm myapp whoami` | Running as root when shouldn't |
| Timezone | `docker run --rm myapp date +%Z` | Wrong TZ in container |
| Locale | `docker run --rm myapp locale` | Missing locale data |

### Layer Size Analysis

Large or unexpected layers may indicate packaging problems:
```bash
docker history myapp:latest --human --format "{{.Size}}\t{{.CreatedBy}}"
```

Look for:
- Layers that include test fixtures, documentation, or `.git` directory
- Duplicate installations (pip install in two separate layers)
- Development dependencies in production image
- Uncompressed assets that should be minified

## Import Smoke Testing

### The Import Smoke Test

The simplest and most effective packaging test: verify that every production module can be imported in the built environment.

**Python example**:
```python
"""Import smoke test: run in clean environment or built container."""
import importlib
import sys

PRODUCTION_MODULES = [
    "myapp",
    "myapp.api",
    "myapp.models",
    "myapp.services.payment",
    "myapp.services.notification",
    "myapp.utils.datetime_helpers",
    "myapp.utils.file_processing",
]

def test_import_smoke():
    failures = []
    for module_name in PRODUCTION_MODULES:
        try:
            importlib.import_module(module_name)
        except ImportError as e:
            failures.append(f"{module_name}: {e}")

    if failures:
        print("IMPORT SMOKE FAILED:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"All {len(PRODUCTION_MODULES)} modules imported successfully")
```

**Node.js example**:
```javascript
// import_smoke.js: run in clean environment or built container
const modules = [
  './src/app',
  './src/routes',
  './src/models',
  './src/services/payment',
  './src/utils/helpers',
];

const failures = [];
for (const mod of modules) {
  try {
    require(mod);
  } catch (e) {
    failures.push(`${mod}: ${e.message}`);
  }
}

if (failures.length > 0) {
  console.error('IMPORT SMOKE FAILED:');
  failures.forEach(f => console.error(`  - ${f}`));
  process.exit(1);
} else {
  console.log(`All ${modules.length} modules imported successfully`);
}
```

### When Import Smoke Catches Real Bugs

| Scenario | What Happened | Import Smoke Would Catch |
|----------|---------------|-------------------------|
| Missing native lib | `Pillow` installed but `libjpeg` missing in container | `from PIL import Image` -> `ImportError` |
| Wrong Python version | Code uses `match` statement (3.10+) but image has 3.9 | `import myapp` -> `SyntaxError` |
| Missing data file | Model file not included in package | `import myapp.ml` -> `FileNotFoundError` in init |
| Circular import | New import added creating cycle | `import myapp.service` -> `ImportError` |
| Missing `__init__.py` | Subpackage directory missing init file | `import myapp.subpackage` -> `ModuleNotFoundError` |

## Lockfile Alignment

### What Lockfile Alignment Means

The lockfile in your repository must produce the exact same dependency tree in development, CI, and production.

### Verification Steps

1. **Lockfile is committed**: Verify lockfile exists in version control
2. **Lockfile is current**: `pip freeze > /tmp/actual.txt && diff requirements.txt /tmp/actual.txt` (should be identical)
3. **CI uses locked install**: CI runs `pip install -r requirements.txt` (not `pip install .` which resolves from setup.py)
4. **Production uses locked install**: Dockerfile runs same install command as CI
5. **No floating versions**: No `>=`, `~=`, `^` in production requirements (use exact `==`)

### Cross-Platform Lockfile Issues

| Issue | Description | Mitigation |
|-------|-------------|------------|
| Platform markers | `pywin32; sys_platform == 'win32'` only on Windows | Use environment markers correctly |
| Wheel availability | Some packages have wheels for macOS but not Linux | Test install on Linux container |
| Build tool versions | `setuptools`, `wheel` version differences | Pin build tools in CI |
| Hash verification | `--require-hashes` fails with platform-specific wheels | Use per-platform hash files or disable hashes |

## Install Method Parity

### The Install Method Must Match

If development uses one install method and production uses another, dependency behavior may differ.

| Development | CI | Production | Risk |
|-------------|----|-----------|----- |
| `pip install -e .` | `pip install .` | `pip install .` | Editable install may mask missing `MANIFEST.in` entries |
| `npm install` | `npm ci` | `npm ci` | `npm install` updates lockfile; `npm ci` uses it strictly |
| `bundle install` | `bundle install --frozen` | `bundle install --frozen` | Non-frozen install may resolve different versions |
| `go build ./...` | `go build ./...` | `go build ./...` | Usually consistent, but `GOPATH` vs module mode matters |

### Verifying Install Method Parity

1. **Document the install command** for each environment (dev, CI, staging, production)
2. **Compare the commands**: Are they identical?
3. **Test with production method locally**: Can you install using the production command and run the app?
4. **Verify in CI**: CI install command matches production install command

## Packaging Integrity Test Suite

### Minimum viable packaging tests (run before every release):

1. **Build artifact**: Build the package/image without errors
2. **Import smoke**: All production modules import successfully in built artifact
3. **CLI smoke**: Entry points execute with `--help` or `--version`
4. **Health check**: Application starts and responds to health endpoint
5. **Dependency audit**: No known vulnerabilities in installed dependencies
6. **Size check**: Built artifact size is within expected bounds (catch accidental inclusion of test data)

### Extended packaging tests (run nightly or before major releases):

1. **Multi-platform build**: Build and test on all target platforms
2. **Upgrade test**: Install new version over previous version; verify migration
3. **Rollback test**: Downgrade from new version to previous version; verify clean rollback
4. **Clean install test**: Install in completely fresh environment (no cached packages)
5. **Dependency conflict test**: Verify no version conflicts in dependency tree
6. **License audit**: Verify all dependencies comply with license policy

## Integration with CI/CD Pipeline

### Recommended Pipeline Stage Order

```
1. Lint + Type Check          (< 1 min)
2. Unit Tests                 (< 1 min)
3. Integration Tests          (< 5 min)
4. Smoke Tests                (< 5 min)
5. Build Artifact             (< 3 min)
6. Import Smoke (on artifact) (< 1 min)
7. Container Health Check     (< 1 min)
8. Deploy to Staging          (automated)
9. E2E Tests (on staging)     (< 15 min)
10. Release Packaging Verify  (before production deploy)
```

Steps 5-7 are the packaging integrity tests. They run after source-level tests pass but before any deployment.
