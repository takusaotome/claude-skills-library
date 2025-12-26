---
name: zoho-mcp-helper
description: Efficient Zoho MCP data access using subagent pattern. Use this skill when fetching data from Zoho Desk (tickets, threads) or Zoho Projects (projects, tasks, issues) to minimize context consumption. Instead of using MCP tools directly (which return large responses), this skill uses a subagent to fetch and filter data, returning only essential fields.
---

# Zoho MCP Helper - Efficient Data Access

## Problem Statement

When using ZohoMCP tools directly, API responses contain many fields and consume significant context. For example:
- `ZohoDesk_listOfTickets` returns 50+ fields per ticket
- `ZohoProjects_getAllProjects` returns full project objects with nested data

This quickly fills the context window.

## Solution: Subagent Pattern

This skill uses a **subagent** to:
1. Execute MCP calls
2. Filter responses to extract only essential fields
3. Return compact data to the main agent

**Context reduction: 70-90%**

---

# Part 1: Zoho Desk

## Configuration

| Key | Value |
|-----|-------|
| Org ID | 748513201 (FUJISOFT America, Inc.) |

### Department IDs

| Department | ID | Key |
|------------|-----|-----|
| FUJISOFT America | 596958000000006907 | fujisoft |
| Zen Trading | 596958000000481045 | zen-trading |
| Round1 | 596958000000485037 | round1 |
| Salad Cosmo | 596958000000997080 | salad-cosmo |
| Applova | 596958000001547290 | applova |
| Furukawa Sangyo | 596958000002581045 | furukawa |
| JENY | 596958000002586045 | jeny |
| Daido | 596958000007902032 | daido |

## Desk Usage Patterns

### List Tickets (Compact)

```
Task(subagent_type="general-purpose", prompt="""
Fetch Zoho Desk tickets for [DEPARTMENT]:
1. Call mcp__ZohoMCP__ZohoDesk_listOfTickets with:
   - query_params.orgId: "748513201"
   - query_params.departmentId: "[DEPT_ID]"
   - query_params.limit: "[NUMBER]"
2. Extract ONLY: id, ticketNumber, subject (60 chars), status, priority, email, createdTime
3. Return as markdown table: | # | Ticket# | Subject | Status | Priority | From | Created |
""")
```

### Get Ticket Details

```
Task(subagent_type="general-purpose", prompt="""
Get Zoho Desk ticket [TICKET_ID]:
1. Call mcp__ZohoMCP__ZohoDesk_getTicket with:
   - path_variables.ticketId: "[TICKET_ID]"
   - query_params.orgId: "748513201"
   - query_params.include: ["contacts", "assignee"]
2. Call mcp__ZohoMCP__ZohoDesk_getThreads for conversation
3. Return formatted summary with: ticket details, contact info, thread summary (200 chars each)
""")
```

### Draft Reply with CC

```
Task(subagent_type="general-purpose", prompt="""
Create draft reply for ticket [TICKET_ID]:
1. First get threads to find CC addresses
2. Call mcp__ZohoMCP__ZohoDesk_draftsReply with:
   - channel: "EMAIL"
   - fromEmailAddress: "support@fujisoftamerica.zohodesk.com"
   - to: "[RECIPIENT]"
   - cc: "[CC_ADDRESSES]"
   - contentType: "html"
   - content: "[EMAIL_CONTENT]"
3. Return confirmation with draft ID
""")
```

---

# Part 2: Zoho Projects

## Configuration

| Key | Value |
|-----|-------|
| Portal ID | 748512806 (FUJISOFT America, Inc.) |
| Portal Name | fujisoftamerica2 |

### Project Groups

| Group | Key Projects |
|-------|--------------|
| FSAI | Reframe, GenAI Hub, Bookkeeping, HR, Financials, Sales, Admin |
| Round1 | Spo-cha gate application renewal |
| Salad Cosmo | Pallet Special Instruction |
| Redac | Kintone maintenance |

## Projects Usage Patterns

### List Projects (Compact)

```
Task(subagent_type="general-purpose", prompt="""
Fetch Zoho Projects list:
1. Call mcp__ZohoMCP__ZohoProjects_getAllProjects with:
   - path_variables.portal_id: "748512806"
   - query_params.per_page: 20
2. Extract ONLY: id, key, name, status.name, owner.name, project_group.name, percent_complete, tasks.open_count
3. Return as markdown table: | # | Key | Project Name | Status | Owner | Group | Progress | Open Tasks |
""")
```

### Get Project Details

```
Task(subagent_type="general-purpose", prompt="""
Get Zoho Project details for [PROJECT_ID]:
1. Call mcp__ZohoMCP__ZohoProjects_getProjectDetails with:
   - path_variables.portal_id: "748512806"
   - path_variables.project_id: "[PROJECT_ID]"
2. Extract: name, description (200 chars), status, owner, start_date, end_date, percent_complete, tasks count, milestones count
3. Return formatted project summary
""")
```

### List Tasks in Project

```
Task(subagent_type="general-purpose", prompt="""
Fetch tasks for project [PROJECT_ID]:
1. Call mcp__ZohoMCP__ZohoProjects_getTasksByProject with:
   - path_variables.portal_id: "748512806"
   - path_variables.project_id: "[PROJECT_ID]"
   - query_params.per_page: 50
2. Extract ONLY: id, name (60 chars), status.name, priority, owners[0].name, start_date, end_date, percent_complete
3. Return as markdown table: | # | Task Name | Status | Priority | Owner | Start | End | Progress |
""")
```

### Get Task Details

```
Task(subagent_type="general-purpose", prompt="""
Get task details for [TASK_ID] in project [PROJECT_ID]:
1. Call mcp__ZohoMCP__ZohoProjects_getTaskDetails with:
   - path_variables.portal_id: "748512806"
   - path_variables.project_id: "[PROJECT_ID]"
   - path_variables.task_id: "[TASK_ID]"
2. Return: name, description, status, priority, owners, dates, subtasks, dependencies
""")
```

### List Issues/Bugs in Project

```
Task(subagent_type="general-purpose", prompt="""
Fetch issues for project [PROJECT_ID]:
1. Call mcp__ZohoMCP__ZohoProjects_getProjectIssues with:
   - path_variables.portal_id: "748512806"
   - path_variables.project_id: "[PROJECT_ID]"
   - query_params.page: 1
   - query_params.per_page: 50
2. Extract: id, name, status.name, severity.name, assignee.name, due_date
3. Return as markdown table
""")
```

### Create Task

```
Task(subagent_type="general-purpose", prompt="""
Create task in project [PROJECT_ID]:
1. First get task lists: mcp__ZohoMCP__ZohoProjects_getAllProjectTaskLists
2. Call mcp__ZohoMCP__ZohoProjects_createTask with:
   - path_variables.portal_id: "748512806"
   - path_variables.project_id: "[PROJECT_ID]"
   - body.name: "[TASK_NAME]"
   - body.tasklist.id: "[TASKLIST_ID]"
   - body.description: "[DESCRIPTION]"
   - body.start_date: "[YYYY-MM-DD]"
   - body.end_date: "[YYYY-MM-DD]"
   - body.priority: "high/medium/low"
3. Return created task ID and confirmation
""")
```

### List Phases/Milestones

```
Task(subagent_type="general-purpose", prompt="""
Fetch phases for project [PROJECT_ID]:
1. Call mcp__ZohoMCP__ZohoProjects_getProjectPhases with:
   - path_variables.portal_id: "748512806"
   - path_variables.project_id: "[PROJECT_ID]"
2. Extract: id, name, status, start_date, end_date, owner
3. Return as markdown table
""")
```

---

# Compact Output Formats

## Ticket List Format (Desk)
```
| # | Ticket# | Subject | Status | Priority | From | Created |
|---|---------|---------|--------|----------|------|---------|
| 1 | 12345 | Issue with... | Open | High | user@example.com | 2025-12-20 |
```

## Project List Format (Projects)
```
| # | Key | Project Name | Status | Owner | Group | Progress | Open Tasks |
|---|-----|--------------|--------|-------|-------|----------|------------|
| 1 | 186 | Spo-cha gate... | D - Need Analysis | Takuei | Round1 | 1% | 85 |
```

## Task List Format (Projects)
```
| # | Task Name | Status | Priority | Owner | Start | End | Progress |
|---|-----------|--------|----------|-------|-------|-----|----------|
| 1 | Design UI | Open | High | Takuei | 2025-12-01 | 2025-12-15 | 50% |
```

---

# Quick Reference

## Zoho Desk MCP Tools

| Operation | Tool | Key Params |
|-----------|------|------------|
| List tickets | ZohoDesk_listOfTickets | orgId, departmentId, status, limit |
| Get ticket | ZohoDesk_getTicket | ticketId, include |
| Get threads | ZohoDesk_getThreads | ticketId, limit |
| Draft reply | ZohoDesk_draftsReply | ticketId, channel, content, to, cc |
| Create ticket | ZohoDesk_createTicket | subject, contactId, departmentId |
| Update ticket | ZohoDesk_updateTicket | ticketId, status, priority |

## Zoho Projects MCP Tools

| Operation | Tool | Key Params |
|-----------|------|------------|
| List portals | ZohoProjects_getAllPortals | - |
| List projects | ZohoProjects_getAllProjects | portal_id, per_page |
| Get project | ZohoProjects_getProjectDetails | portal_id, project_id |
| List tasks | ZohoProjects_getTasksByProject | portal_id, project_id |
| Get task | ZohoProjects_getTaskDetails | portal_id, project_id, task_id |
| Create task | ZohoProjects_createTask | portal_id, project_id, name, tasklist |
| Update task | ZohoProjects_updateTask | portal_id, project_id, task_id |
| List issues | ZohoProjects_getProjectIssues | portal_id, project_id |
| Create issue | ZohoProjects_createProjectIssue | portal_id, project_id, name |
| List phases | ZohoProjects_getProjectPhases | portal_id, project_id |
| List task lists | ZohoProjects_getAllProjectTaskLists | portal_id, project_id |

---

# Best Practices

1. **Always use subagent** for Zoho queries to minimize context
2. **Specify field limits** - truncate text fields to reasonable lengths
3. **Use table format** for lists - more scannable, fewer tokens
4. **Filter at source** - only request needed include/fields
5. **Batch requests** - combine related queries in one subagent call

---

# Python Helper Script

```bash
# Location
~/.claude/skills/zoho-mcp-helper/scripts/zoho_mcp_client.py

# Desk Commands
python3 zoho_mcp_client.py desk list-departments
python3 zoho_mcp_client.py desk list-tickets salad-cosmo --limit 20
python3 zoho_mcp_client.py desk get-ticket 596958000001234567

# Projects Commands
python3 zoho_mcp_client.py projects list-projects
python3 zoho_mcp_client.py projects list-tasks 1790933000006815495
python3 zoho_mcp_client.py projects get-task 1790933000006815495 1234567
```

---

# Error Handling

If subagent returns error:

**For Desk:**
1. Check department ID is correct
2. Verify ticket ID exists
3. Confirm org ID is 748513201

**For Projects:**
1. Verify portal ID is 748512806
2. Check project ID exists
3. Confirm task/issue ID is valid
