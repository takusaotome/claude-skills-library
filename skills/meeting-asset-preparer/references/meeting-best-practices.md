# Meeting Best Practices Reference Guide

## Overview

This guide provides best practices for preparing and conducting effective meetings. It covers agenda design, facilitation techniques, decision-making frameworks, and follow-up processes.

## Pre-Meeting Preparation

### 1. Define Clear Objectives

Every meeting should have:
- **Primary objective**: The main goal to accomplish
- **Secondary objectives**: Additional items to address if time permits
- **Success criteria**: How to measure if the meeting was successful

### 2. Attendee Selection

Consider the **RACI model** when selecting attendees:
- **Responsible (R)**: People who do the work
- **Accountable (A)**: Decision makers who must be present
- **Consulted (C)**: Subject matter experts who provide input
- **Informed (I)**: Stakeholders who receive updates (may not need to attend)

**Guideline**: Keep meetings to 7 or fewer participants for effective decision-making.

### 3. Time Allocation Framework

| Meeting Type | Recommended Duration | Time Buffer |
|--------------|---------------------|-------------|
| Status Update | 15-30 minutes | 5 minutes |
| Planning Session | 60-90 minutes | 10 minutes |
| Decision Meeting | 30-60 minutes | 10 minutes |
| Workshop | 2-4 hours | 15 minutes per hour |

**Rule**: Allocate 10% buffer time for transitions and unexpected discussions.

### 4. Reference Material Preparation

Gather and organize:
- **Context documents**: Background information attendees need
- **Decision support materials**: Data, estimates, comparisons
- **Prior meeting notes**: Relevant decisions and action items from previous meetings
- **Visual aids**: Diagrams, charts, mockups

**Best Practice**: Distribute materials 24-48 hours before the meeting.

## Agenda Design

### Structure Template

1. **Opening (5%)**: Welcome, objectives review
2. **Context Setting (10%)**: Background and current state
3. **Main Discussion (60%)**: Core topics
4. **Decision Making (15%)**: Capture decisions
5. **Action Items (10%)**: Assign tasks and owners

### Time Boxing

For each agenda item, specify:
- **Topic**: What will be discussed
- **Duration**: How much time allocated
- **Presenter/Facilitator**: Who leads the discussion
- **Expected Output**: Decision, information, or action

### Priority Ordering

Sequence agenda items by:
1. **Most important first**: Ensure critical items get addressed
2. **Energy matching**: Put complex topics when energy is high
3. **Dependency order**: Prerequisites before dependent topics
4. **Attendee availability**: If key people must leave early, address their items first

## Bilingual Meeting Considerations

### Language Strategy

| Scenario | Primary Language | Secondary Language |
|----------|-----------------|-------------------|
| Japanese-majority attendees | Japanese | English subtitles/notes |
| English-majority attendees | English | Japanese translation available |
| 50/50 split | Bilingual (both) | Equal representation |
| Executive-level | English | Japanese summary |

### Bilingual Document Format

For bilingual documents, use side-by-side or row-by-row format:

```markdown
| English | 日本語 |
|---------|--------|
| Topic 1 | 議題1 |
```

Or inline format:
```markdown
# Meeting Agenda / 会議アジェンダ
## Topic 1 / 議題1
```

### Cultural Considerations

- **Japan**: Allow silence for reflection; avoid putting individuals on the spot
- **US/Europe**: More direct discussion style; encourage open debate
- **Best Practice**: Explicitly invite input from quieter attendees

## Decision-Making Frameworks

### RAPID Model

- **Recommend (R)**: Proposes a decision
- **Agree (A)**: Must concur for implementation
- **Perform (P)**: Executes the decision
- **Input (I)**: Provides information
- **Decide (D)**: Has final authority

### Decision Log Requirements

For each decision, record:
1. **Decision statement**: Clear, specific, actionable
2. **Rationale**: Why this decision was made
3. **Alternatives considered**: Other options evaluated
4. **Owner**: Who is accountable for implementation
5. **Date**: When the decision was made
6. **Review date**: When to revisit if needed

## Action Item Best Practices

### SMART Criteria

Each action item should be:
- **Specific**: Clear task description
- **Measurable**: How to verify completion
- **Assignable**: Single owner
- **Realistic**: Achievable in timeframe
- **Time-bound**: Specific due date

### Status Tracking

Use consistent status values:
- **Open**: Not started
- **In Progress**: Work underway
- **Blocked**: Waiting on dependency
- **Completed**: Done and verified
- **Cancelled**: No longer needed

### Follow-Up Cadence

| Priority | Follow-Up Frequency |
|----------|-------------------|
| Critical | Daily |
| High | 2-3 times per week |
| Medium | Weekly |
| Low | Bi-weekly |

## Post-Meeting Process

### Within 24 Hours

1. Distribute meeting notes to all attendees and informed stakeholders
2. Update decision log with new decisions
3. Create action items in tracking system
4. Send calendar invites for follow-up meetings

### Within 1 Week

1. Check status of high-priority action items
2. Address any blockers identified
3. Confirm understanding with remote/async attendees

## Reference Material Organization

### Directory Structure

```
meeting_package/
├── index.md              # Meeting overview and links
├── agenda.md             # Meeting agenda
├── decision_log.md       # Decisions made
├── action_items.md       # Tasks assigned
└── references/           # Supporting documents
    ├── estimates/        # Cost/effort estimates
    ├── specs/            # Technical specifications
    └── prior_meetings/   # Previous meeting notes
```

### Naming Convention

Use consistent naming:
```
YYYY-MM-DD_meeting-type_topic.md
```

Example:
```
2026-03-15_sprint-review_q1-sprint-3.md
```

## Meeting Type Templates

### Status Update Meeting

- Duration: 15-30 minutes
- Frequency: Weekly or bi-weekly
- Structure: Round-robin updates + blockers + next steps

### Decision Meeting

- Duration: 30-60 minutes
- Frequency: As needed
- Structure: Context + options + discussion + decision + action items

### Planning Session

- Duration: 60-90 minutes
- Frequency: Per project phase
- Structure: Review + planning + assignment + risks + timeline

### Retrospective

- Duration: 45-60 minutes
- Frequency: Per sprint/milestone
- Structure: What went well + What to improve + Action items

## Metrics and Improvement

### Meeting Effectiveness Indicators

- **Decision rate**: Decisions made vs. decisions needed
- **Action completion rate**: Actions completed by due date
- **Attendee satisfaction**: Post-meeting feedback scores
- **Time efficiency**: Meeting finished on time

### Continuous Improvement

After each meeting, consider:
1. Did we achieve our objectives?
2. Was the time allocation appropriate?
3. Were the right people present?
4. What should we change for next time?
