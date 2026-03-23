# Forbidden-to-Safe Mapping Table

Use this template to create a comprehensive mapping from forbidden (dangerous) patterns to their approved safe replacements. This table serves as a quick-reference for developers and reviewers.

---

## Template

| # | Anti-Pattern | Safe Replacement | Example Before | Example After | Tool Enforcement Option |
|---|-------------|-----------------|----------------|---------------|------------------------|
| 1 | [Forbidden pattern name] | [Approved safe pattern] | [Code snippet showing the dangerous way] | [Code snippet showing the safe way] | [lint/semgrep/regex rule ID or "manual review"] |

---

## Filled Example: Core Safe Defaults

| # | Anti-Pattern | Safe Replacement | Example Before | Example After | Tool Enforcement Option |
|---|-------------|-----------------|----------------|---------------|------------------------|
| 1 | Raw SQL string concatenation | Parameterized query / ORM | `query = f"SELECT * FROM users WHERE id = {uid}"` | `cursor.execute("SELECT * FROM users WHERE id = %s", [uid])` | Semgrep: `sbd-s01-sql-concatenation` |
| 2 | Opt-in authorization (unprotected routes) | Deny-by-default with `@require_permission` | `@app.route("/admin/export") def export(): ...` | `@app.route("/admin/export") @require_permission("admin.export") def export(): ...` | Semgrep: `sbd-s02-missing-auth-decorator` |
| 3 | Direct file path concatenation | FileService with path validation | `path = "/uploads/" + username + "/" + filename` | `content = file_service.read(bucket="uploads", key=filename)` | Semgrep: `sbd-s04-file-path-construction` |
| 4 | Success message before persistence | Post-commit/post-await success only | `showToast("Saved!"); await api.save(data);` | `const result = await api.save(data); showToast("Saved!");` | Semgrep: `sbd-s03-premature-success` |
| 5 | Naive datetime (no timezone) | UTC-aware datetime everywhere | `created_at = datetime.now()` | `created_at = datetime.now(timezone.utc)` | Lint: `sbd-l01-naive-datetime` |
| 6 | Positional row/column access | Named/keyed access | `name = row[1]; email = row[3]` | `name = row["name"]; email = row["email"]` | Lint: `sbd-l06-positional-access` (custom) |
| 7 | Bare except / catch-all swallowing | Specific exception with recovery | `try: save(x) except: pass` | `try: save(x) except IntegrityError as e: handle(e)` | Lint: `sbd-l04-bare-except` |
| 8 | Global state / service locator | Constructor dependency injection | `db = Database.connect(os.environ["DB_URL"])` | `class UserService: def __init__(self, db: Database): self.db = db` | Semgrep: `sbd-s05-global-state-access` |
| 9 | Non-idempotent write endpoint | Idempotency key + upsert | `POST /orders -> always creates new` | `POST /orders (Idempotency-Key: uuid) -> upsert` | Manual review + integration test |
| 10 | Hardcoded secrets in source | Environment variable / secrets manager | `API_KEY = "sk-abc123"` | `API_KEY = os.environ["API_KEY"]` | Regex: `sbd-r05-hardcoded-secret` + git-secrets |

---

## Category-Specific Mapping Tables

### Query Construction Patterns

| # | Anti-Pattern | Safe Replacement | Example Before | Example After | Tool Enforcement Option |
|---|-------------|-----------------|----------------|---------------|------------------------|
| Q1 | f-string SQL | Parameterized query | `f"WHERE name = '{name}'"` | `"WHERE name = %s", [name]` | Semgrep |
| Q2 | %-format SQL | Parameterized query | `"WHERE id = %d" % uid` | `"WHERE id = %s", [uid]` | Semgrep |
| Q3 | .format() SQL | Parameterized query | `"WHERE id = {}".format(uid)` | `"WHERE id = %s", [uid]` | Semgrep |
| Q4 | Dynamic column via concatenation | Allowlist lookup | `f"ORDER BY {col}"` | `ORDER_COLS = {"name", "date"}; assert col in ORDER_COLS` | Semgrep (taint) |
| Q5 | LIKE with unescaped wildcards | Escape wildcards before binding | `"LIKE '%{term}%'"` | `"LIKE %s", [f"%{escape_like(term)}%"]` | Manual review |

### Authorization Patterns

| # | Anti-Pattern | Safe Replacement | Example Before | Example After | Tool Enforcement Option |
|---|-------------|-----------------|----------------|---------------|------------------------|
| A1 | No auth check on endpoint | `@require_permission` decorator | Missing decorator | `@require_permission("resource.action")` | Semgrep |
| A2 | Role check inside handler body | Middleware/decorator-based check | `if not user.is_admin: return 403` | `@require_role("admin")` at handler level | Semgrep |
| A3 | Hardcoded role names in logic | Permission-based authorization | `if role == "admin"` | `if policy.can(user, "manage", resource)` | Lint (custom) |
| A4 | Object-level auth missing | Ownership/policy check per object | `Order.get(id)` (any user) | `Order.get(id, requester=current_user)` | Manual review |

### File Handling Patterns

| # | Anti-Pattern | Safe Replacement | Example Before | Example After | Tool Enforcement Option |
|---|-------------|-----------------|----------------|---------------|------------------------|
| F1 | String path concatenation | `FileService.resolve_safe_path()` | `"/uploads/" + name` | `file_service.resolve_safe_path(name)` | Semgrep |
| F2 | Trusting file extension for type | Magic bytes validation | `if ext == ".pdf"` | `if magic.from_buffer(data) == "application/pdf"` | Manual review |
| F3 | World-readable file permissions | Restrictive default permissions | `open(path, "w")` | `os.open(path, os.O_WRONLY, 0o640)` | Lint (custom) |
| F4 | No temp file cleanup | Context manager with cleanup | `tmp = open("/tmp/x", "w")` | `with tempfile.NamedTemporaryFile() as tmp:` | Lint |

---

## Usage Instructions

1. Start with the Core Safe Defaults table (covers the most common patterns)
2. Add category-specific tables as needed for your technology stack
3. For each entry, verify that the "Example After" code is copy-pasteable and correct
4. Link each "Tool Enforcement Option" to a rule definition in `references/static_rule_design_guide.md`
5. Review this table during onboarding for new team members
6. Update the table when new forbidden patterns are identified (Workflow 1) or safe alternatives evolve
7. Post this table in the team's developer documentation or wiki for easy access
