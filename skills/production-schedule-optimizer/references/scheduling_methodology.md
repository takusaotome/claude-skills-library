# Scheduling Methodology Guide

## Table of Contents
- [Greedy Bin-Packing Algorithm](#greedy-bin-packing-algorithm)
- [Deterministic Sort & Tie-Break](#deterministic-sort--tie-break)
- [Constraint Modeling Patterns](#constraint-modeling-patterns)
- [Improvement Techniques](#improvement-techniques)
- [Quality Metrics](#quality-metrics)

---

## Greedy Bin-Packing Algorithm

### Overview

The scheduling engine uses a **Greedy Bin-Packing** approach with the **Largest-First Decreasing (LFD)** heuristic. This is a well-known approximation algorithm for the bin-packing problem.

### Why Bin-Packing?

Production scheduling can be modeled as a multi-dimensional bin-packing problem:
- **Items** = Production tasks (with duration and staff requirements)
- **Bins** = Room-day slots (with capacity limits)
- **Dimensions** = Time (duration) and staff (headcount)

### Largest-First Decreasing Heuristic

1. Sort all tasks by size (staff-hours) in descending order
2. For each task, find the bin (room-day) with the most remaining capacity
3. Place the task in that bin if constraints are satisfied
4. If no bin can accommodate the task, mark it as unassigned

### Why LFD Works for Production Scheduling

- Large tasks are hardest to place and have the fewest viable slots
- Placing them first avoids fragmentation of available capacity
- Smaller tasks can fill gaps more flexibly
- Empirically achieves within 10-15% of optimal for typical production workloads

### Approximation Guarantee

LFD guarantees a solution no worse than `(11/9) * OPT + 6/9` bins for the classic 1D bin-packing problem. In practice, for production scheduling with multiple constraints, performance is typically within 5-15% of optimal.

### Algorithm Pseudocode

```
function schedule(tasks, rooms, staff):
    sort tasks by (-staff_hours, shelf_life, product_code)

    capacity = initialize_room_day_capacity(rooms, staff)
    schedule = empty
    unassigned = empty

    for task in tasks:
        assigned_days = compute_day_distribution(task)
        for day in assigned_days:
            candidate_rooms = filter_allowed_rooms(task, day)
            candidate_rooms.sort(by=-remaining_capacity, then room_code)

            placed = false
            for room in candidate_rooms:
                if can_fit(task, room, day, capacity):
                    place(task, room, day, capacity, schedule)
                    placed = true
                    break

            if not placed:
                unassigned.append((task, day))

    return schedule, unassigned
```

---

## Deterministic Sort & Tie-Break

### Motivation

Deterministic scheduling is essential for:
- **Reproducibility**: Same inputs always produce the same schedule
- **Auditability**: Stakeholders can verify why a specific assignment was made
- **Testing**: Unit tests can assert exact output

### Task Sort Specification

Tasks are sorted using a composite key with three levels:

| Priority | Key | Direction | Type |
|----------|-----|-----------|------|
| 1 | total_staff_hours | Descending | float |
| 2 | shelf_life_days | Ascending | int |
| 3 | product_code | Ascending | string |

**Rationale for each key:**
1. **total_staff_hours DESC**: Largest tasks first (LFD heuristic core principle)
2. **shelf_life_days ASC**: Shorter shelf life = higher priority (FEFO principle); these products have less scheduling flexibility
3. **product_code ASC**: Lexicographic tie-break ensures determinism when first two keys are equal

### Room Selection Tie-Break

When multiple rooms can accommodate a task, selection follows:

| Priority | Key | Direction |
|----------|-----|-----------|
| 1 | remaining_capacity | Descending |
| 2 | room_code | Ascending |

### Day Distribution Determinism

Day assignment uses evenly-spaced index selection:
```
step = len(available_days) / production_count
assigned_days = [available_days[int(i * step)] for i in range(production_count)]
```

This distributes production days as evenly as possible across the available days.

### Edge Cases

- **Equal staff-hours and shelf-life**: product_code ensures stable sort
- **All rooms at equal capacity**: room_code ensures consistent selection
- **production_count > 7**: Clamped to 7 (daily production)

---

## Constraint Modeling Patterns

### Time Window Constraints

Each room-day combination defines an available time window:
```
window_start = shift_start_hour * 60  (e.g., 8 * 60 = 480 min)
window_end = window_start + (shift_hours * 60)  (e.g., 480 + 480 = 960 min)
available_minutes = window_end - window_start
```

Tasks must fit entirely within this window. No task is allowed to span across the window boundary.

### Capacity Constraints

Two capacity dimensions are checked simultaneously:

1. **Time capacity**: Sum of task durations must not exceed available minutes
2. **Staff capacity**: Concurrent task staff requirements must not exceed room max_staff

```
time_check: sum(durations) <= available_minutes
staff_check: max(concurrent_staff_at_any_t) <= max_staff
```

### Priority Constraints

Task priority is implicitly encoded in the sort order:
- Higher staff-hours = higher priority (placed first, gets best slots)
- Shorter shelf life = higher priority (less flexibility in scheduling)

Explicit priority overrides can be added via an optional `priority` column in products.csv.

### Precedence Constraints (Future Extension)

Not currently implemented, but the architecture supports:
- Task A must complete before Task B starts (same room)
- Cleaning time between product changeovers
- Temperature stabilization periods

These would be modeled as additional edges in a dependency graph, resolved via topological sort before bin-packing.

---

## Improvement Techniques

### Local Search: Swap

After initial placement, try swapping two tasks between different room-day slots:

```
for each pair (task_A in slot_X, task_B in slot_Y):
    if swap improves balance_score and both fit:
        perform swap
        update capacity tracking
```

**When to use**: Balance score < 0.7 (significant load imbalance)

### Compaction: Shift Earlier

Move tasks to earlier time slots within their assigned room-day:

```
for each room-day:
    sort tasks by start_time
    next_available = window_start
    for task in tasks:
        task.start_time = next_available
        next_available = task.start_time + task.duration
```

**When to use**: After swaps or manual adjustments that may have created gaps

### Reassignment: Move to Alternate Room

For overloaded rooms, try moving tasks to alternate rooms:

```
for each overloaded room-day:
    for each task in room-day (smallest first):
        for each alternate room in task.allowed_rooms:
            if alternate room has capacity:
                move task
                break
```

**When to use**: Room utilization > 90% and alternate rooms < 70%

### When NOT to Optimize Further

Stop optimization when:
1. All quality metrics are within target ranges
2. Balance score >= 0.8
3. Schedule completeness = 100%
4. No PSO-W004 (unassigned tasks) alerts
5. Improvement iterations exceed 100 with < 1% improvement

Over-optimization can reduce schedule readability and make it harder for floor managers to understand the rationale behind assignments.

---

## Quality Metrics

### Room Utilization Rate

```
utilization = used_hours / available_hours
```

| Range | Assessment | Action |
|-------|-----------|--------|
| 90-100% | Over-utilized | Risk of delays; consider redistributing |
| 70-85% | Optimal | Target range; good balance of efficiency and flexibility |
| 50-70% | Under-utilized | Consider consolidating or adding tasks |
| < 50% | Significantly under-utilized | Review room necessity |

### Staff Efficiency

```
efficiency = required_staff_hours / assigned_staff_hours
```

Measures how much of the assigned staff time is productively used. Target: 80-90%.

### Schedule Completeness

```
completeness = assigned_demand / total_demand
```

Should always be 100%. Any value below indicates unassigned tasks (PSO-W004).

### Balance Score

```
balance = 1 - std_dev(utilizations) / mean(utilizations)
```

Measures how evenly the workload is distributed. Target: >= 0.8. A score of 1.0 means perfectly balanced; a score below 0.5 indicates severe imbalance.

### Composite Quality Score

For overall schedule assessment:
```
quality = 0.3 * completeness + 0.3 * mean_utilization + 0.2 * efficiency + 0.2 * balance
```

Target: >= 0.8 (on a 0-1 scale).
