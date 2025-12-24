#!/usr/bin/env python3
"""
Zoho MCP Client - Efficient data fetching with filtering for Desk and Projects

This script generates MCP call instructions with filtering specifications
to minimize context consumption in Claude Code.

Usage:
    python3 zoho_mcp_client.py desk <command> [options]
    python3 zoho_mcp_client.py projects <command> [options]

Desk Commands:
    desk list-departments    List all departments
    desk list-tickets        List tickets (compact format)
    desk get-ticket          Get single ticket details
    desk get-threads         Get ticket threads (summary format)

Projects Commands:
    projects list-projects   List all projects
    projects get-project     Get project details
    projects list-tasks      List tasks in project
    projects get-task        Get task details
    projects list-issues     List issues in project
"""

import json
import sys
import argparse
from typing import Optional, Dict, Any


# ============================================================================
# ZOHO DESK CONFIGURATION
# ============================================================================

DESK_ORG_ID = "748513201"  # FUJISOFT America, Inc.

DEPARTMENTS = {
    "fujisoft": "596958000000006907",
    "zen-trading": "596958000000481045",
    "round1": "596958000000485037",
    "salad-cosmo": "596958000000997080",
    "applova": "596958000001547290",
    "furukawa": "596958000002581045",
    "jeny": "596958000002586045",
    "daido": "596958000007902032",
}


# ============================================================================
# ZOHO PROJECTS CONFIGURATION
# ============================================================================

PROJECTS_PORTAL_ID = "748512806"  # FUJISOFT America, Inc.
PROJECTS_PORTAL_NAME = "fujisoftamerica2"

PROJECT_GROUPS = {
    "fsai": "FSAI internal projects",
    "round1": "Round1 client projects",
    "salad-cosmo": "Salad Cosmo client projects",
    "redac": "Redac client projects",
}


# ============================================================================
# ZOHO DESK COMMANDS
# ============================================================================

def desk_list_departments() -> str:
    """List available departments"""
    return json.dumps({
        "service": "Zoho Desk",
        "departments": DEPARTMENTS,
        "org_id": DESK_ORG_ID,
        "note": "Use department key (e.g., 'salad-cosmo') for queries"
    }, indent=2)


def desk_list_tickets(department: str, status: Optional[str] = None, limit: int = 20) -> str:
    """Generate compact ticket list output"""
    dept_id = DEPARTMENTS.get(department.lower())
    if not dept_id:
        return json.dumps({
            "error": f"Unknown department: {department}",
            "available": list(DEPARTMENTS.keys())
        }, indent=2)

    query_params = {
        "orgId": DESK_ORG_ID,
        "departmentId": dept_id,
        "limit": str(limit),
    }
    if status:
        query_params["status"] = status

    return json.dumps({
        "service": "Zoho Desk",
        "action": "list_tickets",
        "mcp_tool": "mcp__ZohoMCP__ZohoDesk_listOfTickets",
        "params": {"query_params": query_params},
        "filter_fields": ["id", "ticketNumber", "subject (60 chars)", "status", "priority", "email", "createdTime"],
        "output_format": "| # | Ticket# | Subject | Status | Priority | From | Created |",
        "instructions": "Execute MCP call, extract only filter_fields, return as markdown table"
    }, indent=2)


def desk_get_ticket(ticket_id: str) -> str:
    """Generate single ticket query"""
    return json.dumps({
        "service": "Zoho Desk",
        "action": "get_ticket",
        "mcp_tool": "mcp__ZohoMCP__ZohoDesk_getTicket",
        "params": {
            "path_variables": {"ticketId": ticket_id},
            "query_params": {"orgId": DESK_ORG_ID, "include": ["contacts", "assignee"]}
        },
        "filter_fields": ["id", "ticketNumber", "subject", "description (500 chars)", "status", "priority", "email", "assignee.firstName", "createdTime", "dueDate"],
        "output_format": "formatted_summary",
        "instructions": "Execute MCP call, also call getThreads, return formatted ticket summary with thread history"
    }, indent=2)


def desk_get_threads(ticket_id: str, limit: int = 10) -> str:
    """Generate thread query with summary format"""
    return json.dumps({
        "service": "Zoho Desk",
        "action": "get_threads",
        "mcp_tool": "mcp__ZohoMCP__ZohoDesk_getThreads",
        "params": {
            "path_variables": {"ticketId": ticket_id},
            "query_params": {"orgId": DESK_ORG_ID, "limit": str(limit)}
        },
        "filter_fields": ["id", "direction", "from.email", "sendDateTime", "content (200 chars, strip HTML)"],
        "output_format": "thread_summary",
        "instructions": "For each thread: [date] direction from email - content_summary"
    }, indent=2)


# ============================================================================
# ZOHO PROJECTS COMMANDS
# ============================================================================

def projects_list_projects(limit: int = 20) -> str:
    """Generate projects list query"""
    return json.dumps({
        "service": "Zoho Projects",
        "action": "list_projects",
        "mcp_tool": "mcp__ZohoMCP__ZohoProjects_getAllProjects",
        "params": {
            "path_variables": {"portal_id": PROJECTS_PORTAL_ID},
            "query_params": {"per_page": limit}
        },
        "filter_fields": ["id", "key", "name (60 chars)", "status.name", "owner.name", "project_group.name", "percent_complete", "tasks.open_count"],
        "output_format": "| # | Key | Project Name | Status | Owner | Group | Progress | Open Tasks |",
        "instructions": "Execute MCP call, extract only filter_fields, return as markdown table"
    }, indent=2)


def projects_get_project(project_id: str) -> str:
    """Generate project details query"""
    return json.dumps({
        "service": "Zoho Projects",
        "action": "get_project",
        "mcp_tool": "mcp__ZohoMCP__ZohoProjects_getProjectDetails",
        "params": {
            "path_variables": {
                "portal_id": PROJECTS_PORTAL_ID,
                "project_id": project_id
            }
        },
        "filter_fields": ["id", "key", "name", "description (200 chars)", "status.name", "owner.name", "start_date", "end_date", "percent_complete", "tasks", "milestones"],
        "output_format": "formatted_summary",
        "instructions": "Return formatted project summary with key metrics"
    }, indent=2)


def projects_list_tasks(project_id: str, limit: int = 50) -> str:
    """Generate tasks list query"""
    return json.dumps({
        "service": "Zoho Projects",
        "action": "list_tasks",
        "mcp_tool": "mcp__ZohoMCP__ZohoProjects_getTasksByProject",
        "params": {
            "path_variables": {
                "portal_id": PROJECTS_PORTAL_ID,
                "project_id": project_id
            },
            "query_params": {"per_page": limit}
        },
        "filter_fields": ["id", "name (60 chars)", "status.name", "priority", "owners[0].name", "start_date", "end_date", "percent_complete"],
        "output_format": "| # | Task Name | Status | Priority | Owner | Start | End | Progress |",
        "instructions": "Execute MCP call, extract only filter_fields, return as markdown table"
    }, indent=2)


def projects_get_task(project_id: str, task_id: str) -> str:
    """Generate task details query"""
    return json.dumps({
        "service": "Zoho Projects",
        "action": "get_task",
        "mcp_tool": "mcp__ZohoMCP__ZohoProjects_getTaskDetails",
        "params": {
            "path_variables": {
                "portal_id": PROJECTS_PORTAL_ID,
                "project_id": project_id,
                "task_id": task_id
            }
        },
        "filter_fields": ["id", "name", "description", "status.name", "priority", "owners", "start_date", "end_date", "percent_complete", "subtasks", "dependencies"],
        "output_format": "formatted_summary",
        "instructions": "Return formatted task summary with all relevant details"
    }, indent=2)


def projects_list_issues(project_id: str, limit: int = 50) -> str:
    """Generate issues list query"""
    return json.dumps({
        "service": "Zoho Projects",
        "action": "list_issues",
        "mcp_tool": "mcp__ZohoMCP__ZohoProjects_getProjectIssues",
        "params": {
            "path_variables": {
                "portal_id": PROJECTS_PORTAL_ID,
                "project_id": project_id
            },
            "query_params": {"page": 1, "per_page": limit}
        },
        "filter_fields": ["id", "name (60 chars)", "status.name", "severity.name", "assignee.name", "due_date"],
        "output_format": "| # | Issue Name | Status | Severity | Assignee | Due Date |",
        "instructions": "Execute MCP call, extract only filter_fields, return as markdown table"
    }, indent=2)


def projects_list_phases(project_id: str) -> str:
    """Generate phases/milestones list query"""
    return json.dumps({
        "service": "Zoho Projects",
        "action": "list_phases",
        "mcp_tool": "mcp__ZohoMCP__ZohoProjects_getProjectPhases",
        "params": {
            "path_variables": {
                "portal_id": PROJECTS_PORTAL_ID,
                "project_id": project_id
            }
        },
        "filter_fields": ["id", "name", "status", "start_date", "end_date", "owner.name"],
        "output_format": "| # | Phase Name | Status | Start | End | Owner |",
        "instructions": "Execute MCP call, extract only filter_fields, return as markdown table"
    }, indent=2)


def projects_info() -> str:
    """Show Zoho Projects configuration"""
    return json.dumps({
        "service": "Zoho Projects",
        "portal_id": PROJECTS_PORTAL_ID,
        "portal_name": PROJECTS_PORTAL_NAME,
        "project_groups": PROJECT_GROUPS,
        "note": "Use project_id from list-projects for other commands"
    }, indent=2)


# ============================================================================
# MAIN CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Zoho MCP Client - Efficient data fetching for Desk and Projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 zoho_mcp_client.py desk list-departments
  python3 zoho_mcp_client.py desk list-tickets salad-cosmo --limit 20
  python3 zoho_mcp_client.py desk get-ticket 596958000001234567

  python3 zoho_mcp_client.py projects info
  python3 zoho_mcp_client.py projects list-projects
  python3 zoho_mcp_client.py projects list-tasks 1790933000006815495
        """
    )

    subparsers = parser.add_subparsers(dest="service", help="Zoho service")

    # ---- DESK subcommands ----
    desk_parser = subparsers.add_parser("desk", help="Zoho Desk commands")
    desk_subparsers = desk_parser.add_subparsers(dest="command")

    # desk list-departments
    desk_subparsers.add_parser("list-departments", help="List available departments")

    # desk list-tickets
    list_tickets = desk_subparsers.add_parser("list-tickets", help="List tickets in compact format")
    list_tickets.add_argument("department", help="Department key (e.g., salad-cosmo, round1)")
    list_tickets.add_argument("--status", help="Filter by status (Open, Closed, etc.)")
    list_tickets.add_argument("--limit", type=int, default=20, help="Maximum number of tickets")

    # desk get-ticket
    get_ticket = desk_subparsers.add_parser("get-ticket", help="Get single ticket details")
    get_ticket.add_argument("ticket_id", help="Ticket ID")

    # desk get-threads
    get_threads = desk_subparsers.add_parser("get-threads", help="Get ticket threads")
    get_threads.add_argument("ticket_id", help="Ticket ID")
    get_threads.add_argument("--limit", type=int, default=10, help="Maximum number of threads")

    # ---- PROJECTS subcommands ----
    projects_parser = subparsers.add_parser("projects", help="Zoho Projects commands")
    projects_subparsers = projects_parser.add_subparsers(dest="command")

    # projects info
    projects_subparsers.add_parser("info", help="Show Projects configuration")

    # projects list-projects
    list_projects = projects_subparsers.add_parser("list-projects", help="List all projects")
    list_projects.add_argument("--limit", type=int, default=20, help="Maximum number of projects")

    # projects get-project
    get_project = projects_subparsers.add_parser("get-project", help="Get project details")
    get_project.add_argument("project_id", help="Project ID")

    # projects list-tasks
    list_tasks = projects_subparsers.add_parser("list-tasks", help="List tasks in project")
    list_tasks.add_argument("project_id", help="Project ID")
    list_tasks.add_argument("--limit", type=int, default=50, help="Maximum number of tasks")

    # projects get-task
    get_task = projects_subparsers.add_parser("get-task", help="Get task details")
    get_task.add_argument("project_id", help="Project ID")
    get_task.add_argument("task_id", help="Task ID")

    # projects list-issues
    list_issues = projects_subparsers.add_parser("list-issues", help="List issues in project")
    list_issues.add_argument("project_id", help="Project ID")
    list_issues.add_argument("--limit", type=int, default=50, help="Maximum number of issues")

    # projects list-phases
    list_phases = projects_subparsers.add_parser("list-phases", help="List phases/milestones")
    list_phases.add_argument("project_id", help="Project ID")

    args = parser.parse_args()

    # Handle commands
    if args.service == "desk":
        if args.command == "list-departments":
            print(desk_list_departments())
        elif args.command == "list-tickets":
            print(desk_list_tickets(args.department, args.status, args.limit))
        elif args.command == "get-ticket":
            print(desk_get_ticket(args.ticket_id))
        elif args.command == "get-threads":
            print(desk_get_threads(args.ticket_id, args.limit))
        else:
            desk_parser.print_help()

    elif args.service == "projects":
        if args.command == "info":
            print(projects_info())
        elif args.command == "list-projects":
            print(projects_list_projects(args.limit))
        elif args.command == "get-project":
            print(projects_get_project(args.project_id))
        elif args.command == "list-tasks":
            print(projects_list_tasks(args.project_id, args.limit))
        elif args.command == "get-task":
            print(projects_get_task(args.project_id, args.task_id))
        elif args.command == "list-issues":
            print(projects_list_issues(args.project_id, args.limit))
        elif args.command == "list-phases":
            print(projects_list_phases(args.project_id))
        else:
            projects_parser.print_help()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
