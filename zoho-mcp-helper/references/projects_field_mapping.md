# Zoho Projects Field Mapping Reference

## Configuration

| Key | Value |
|-----|-------|
| Portal ID | 748512806 |
| Portal Name | fujisoftamerica2 |
| Organization | FUJISOFT America, Inc. |

---

## Projects List (ZohoProjects_getAllProjects)

### Full Response Fields (avoid)
```
id, key, name, description, status, owner, project_group,
start_date, end_date, created_time, modified_time,
percent_complete, is_public_project, is_rollup_project,
budget_info, layout, sub_module_settings, tags,
tasks (open_count, closed_count, total),
milestones (open_count, closed_count, total),
issues (open_count, closed_count, total),
... many more nested objects
```

### Compact Fields (use these)
| Field | Type | Notes |
|-------|------|-------|
| id | string | Project ID |
| key | string | Short project key (e.g., "186") |
| name | string | Truncate to 60 chars |
| status.name | string | e.g., "D - Need Analysis" |
| owner.name | string | Project owner name |
| project_group.name | string | e.g., "Round1" |
| percent_complete | number | 0-100 |
| tasks.open_count | number | Open task count |

### Output Format
```
| # | Key | Project Name | Status | Owner | Group | Progress | Open Tasks |
|---|-----|--------------|--------|-------|-------|----------|------------|
| 1 | 186 | Spo-cha gate... | D - Need Analysis | Takuei | Round1 | 1% | 85 |
```

---

## Project Details (ZohoProjects_getProjectDetails)

### Compact Fields
| Field | Type | Notes |
|-------|------|-------|
| id | string | Project ID |
| key | string | Short key |
| name | string | Full name |
| description | string | Truncate to 200 chars |
| status.name | string | Current status |
| owner.name | string | Owner name |
| start_date | string | YYYY-MM-DD |
| end_date | string | YYYY-MM-DD |
| percent_complete | number | Progress percentage |
| tasks | object | {open_count, closed_count, total} |
| milestones | object | {open_count, closed_count, total} |
| issues | object | {open_count, closed_count, total} |

---

## Tasks (ZohoProjects_getTasksByProject)

### Full Response Fields (avoid)
```
id, key, name, description, status, priority, owners,
start_date, end_date, created_time, modified_time,
percent_complete, duration, billing_type, budget_info,
tasklist, parental_info, recurrence, reminder, tags, teams,
attachments, integrations, subtasks, dependencies,
... extensive nested objects
```

### Compact Fields (use these)
| Field | Type | Notes |
|-------|------|-------|
| id | string | Task ID |
| name | string | Truncate to 60 chars |
| status.name | string | e.g., "Open", "In Progress", "Closed" |
| priority | string | "High", "Medium", "Low", "None" |
| owners[0].name | string | First owner name |
| start_date | string | YYYY-MM-DD |
| end_date | string | YYYY-MM-DD |
| percent_complete | number | 0-100 |

### Output Format
```
| # | Task Name | Status | Priority | Owner | Start | End | Progress |
|---|-----------|--------|----------|-------|-------|-----|----------|
| 1 | Design UI | Open | High | Takuei | 2025-12-01 | 2025-12-15 | 50% |
```

---

## Task Details (ZohoProjects_getTaskDetails)

### Compact Fields
| Field | Type | Notes |
|-------|------|-------|
| id | string | Task ID |
| name | string | Full name |
| description | string | Full description |
| status.name | string | Current status |
| priority | string | Priority level |
| owners | array | All owners |
| start_date | string | YYYY-MM-DD |
| end_date | string | YYYY-MM-DD |
| percent_complete | number | Progress |
| subtasks | array | Child tasks if any |
| dependencies | array | Task dependencies |
| tasklist.name | string | Parent tasklist |

---

## Issues/Bugs (ZohoProjects_getProjectIssues)

### Full Response Fields (avoid)
```
id, key, name, description, status, severity, classification,
module, assignee, reporter, affected_milestone, release_milestone,
due_date, created_time, modified_time, is_it_reproducible,
followers, tags, associated_teams, attachments, sprints,
... extensive nested objects
```

### Compact Fields (use these)
| Field | Type | Notes |
|-------|------|-------|
| id | string | Issue ID |
| name | string | Truncate to 60 chars |
| status.name | string | e.g., "Open", "In Progress", "Closed" |
| severity.name | string | e.g., "Critical", "Major", "Minor" |
| assignee.name | string | Assigned user |
| due_date | string | YYYY-MM-DD |

### Output Format
```
| # | Issue Name | Status | Severity | Assignee | Due Date |
|---|------------|--------|----------|----------|----------|
| 1 | Login bug | Open | Major | Takuei | 2025-12-20 |
```

---

## Phases/Milestones (ZohoProjects_getProjectPhases)

### Compact Fields
| Field | Type | Notes |
|-------|------|-------|
| id | string | Phase ID |
| name | string | Phase name |
| status | string | Status |
| start_date | string | YYYY-MM-DD |
| end_date | string | YYYY-MM-DD |
| owner.name | string | Owner name |

### Output Format
```
| # | Phase Name | Status | Start | End | Owner |
|---|------------|--------|-------|-----|-------|
| 1 | Phase 1 | Active | 2025-12-01 | 2025-12-31 | Takuei |
```

---

## Task Lists (ZohoProjects_getAllProjectTaskLists)

### Compact Fields
| Field | Type | Notes |
|-------|------|-------|
| id | string | Tasklist ID |
| name | string | Tasklist name |
| status | string | "active" or "completed" |
| milestone.name | string | Associated milestone |
| task_count | number | Number of tasks |

---

## Context Reduction Examples

### Before (Full API Response)
```json
{
  "id": "1790933000006815495",
  "key": "186",
  "name": "Round1 USA :: Spo-cha gate application renewal",
  "description": "Full description with many paragraphs...",
  "status": {
    "id": "1790933000000028029",
    "name": "D - Need Analysis",
    "type": "open",
    "color": "#00b0f0"
  },
  "owner": {
    "id": "748512806",
    "name": "Takuei Isaotome",
    "email": "saotome@fsi-america.com",
    "zpuid": "789621823",
    "profile_photo_url": "..."
  },
  "project_group": { ... },
  "budget_info": { ... },
  "tasks": { ... },
  "milestones": { ... },
  ... // 50+ more fields
}
```
**Tokens: ~2000+**

### After (Compact Format)
```
| # | Key | Project Name | Status | Owner | Group | Progress | Open Tasks |
|---|-----|--------------|--------|-------|-------|----------|------------|
| 1 | 186 | Round1 USA :: Spo-cha gate... | D - Need Analysis | Takuei Isaotome | Round1 | 1% | 85 |
```
**Tokens: ~100**

**Reduction: ~95%**

---

## MCP Tool Reference

| Operation | MCP Tool | Required Path Variables | Query Params |
|-----------|----------|------------------------|--------------|
| List projects | ZohoProjects_getAllProjects | portal_id | per_page |
| Get project | ZohoProjects_getProjectDetails | portal_id, project_id | - |
| List tasks | ZohoProjects_getTasksByProject | portal_id, project_id | per_page |
| Get task | ZohoProjects_getTaskDetails | portal_id, project_id, task_id | - |
| Create task | ZohoProjects_createTask | portal_id, project_id | - |
| Update task | ZohoProjects_updateTask | portal_id, project_id, task_id | - |
| List issues | ZohoProjects_getProjectIssues | portal_id, project_id | page, per_page |
| Create issue | ZohoProjects_createProjectIssue | portal_id, project_id | - |
| List phases | ZohoProjects_getProjectPhases | portal_id, project_id | - |
| List tasklists | ZohoProjects_getAllProjectTaskLists | portal_id, project_id | - |
