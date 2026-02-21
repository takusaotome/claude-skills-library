# Weekly Production Schedule

**Week**: {{ week_start }} - {{ week_end }}
**Generated**: {{ generated_at }}
**Buffer Coefficient**: {{ buffer_coefficient }}

---

## Summary

| Metric | Value |
|--------|-------|
| Total products | {{ total_products }} |
| Total production runs | {{ total_runs }} |
| Rooms used | {{ rooms_used }} |
| Schedule completeness | {{ completeness }}% |
| Balance score | {{ balance_score }} |

---

## Schedule by Day

### {{ day_name }} ({{ date }})

| Time | Room | Product | Qty | Staff | Duration | Lot |
|------|------|---------|-----|-------|----------|-----|
| {{ start_time }}-{{ end_time }} | {{ room_code }} | {{ product_name }} | {{ qty }} | {{ required_staff }} | {{ duration }}min | {{ lot_count }} |

---

## Staff Requirements

### Summary by Room and Day

| Room | MON | TUE | WED | THU | FRI | SAT | SUN |
|------|-----|-----|-----|-----|-----|-----|-----|
| {{ room_code }} | {{ recommended_staff }} | {{ recommended_staff }} | {{ recommended_staff }} | {{ recommended_staff }} | {{ recommended_staff }} | {{ recommended_staff }} | {{ recommended_staff }} |

### Gap Analysis

| Room | Day | Current | Peak | Min | Recommended | Gap | Status |
|------|-----|---------|------|-----|-------------|-----|--------|
| {{ room_code }} | {{ day }} | {{ current_staff }} | {{ peak_staff }} | {{ min_staff }} | {{ recommended_staff }} | {{ gap }} | {{ status }} |

---

## Room Utilization

| Room | MON | TUE | WED | THU | FRI | SAT | SUN | Avg |
|------|-----|-----|-----|-----|-----|-----|-----|-----|
| {{ room_code }} | {{ util_mon }}% | {{ util_tue }}% | {{ util_wed }}% | {{ util_thu }}% | {{ util_fri }}% | {{ util_sat }}% | {{ util_sun }}% | {{ util_avg }}% |

---

## Alerts

### Errors (PSO-E)

| Code | Product/Room | Message |
|------|-------------|---------|
| {{ error_code }} | {{ target }} | {{ error_message }} |

### Warnings (PSO-W)

| Code | Product/Room | Message |
|------|-------------|---------|
| {{ warning_code }} | {{ target }} | {{ warning_message }} |

---

## Quality Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Room Utilization (avg) | {{ avg_utilization }}% | 70-85% | {{ util_status }} |
| Staff Efficiency | {{ staff_efficiency }}% | 80-90% | {{ eff_status }} |
| Schedule Completeness | {{ completeness }}% | 100% | {{ comp_status }} |
| Balance Score | {{ balance_score }} | >= 0.8 | {{ bal_status }} |

---

## Improvement Suggestions

{{ #if has_suggestions }}
| Priority | Type | Description | Expected Impact |
|----------|------|-------------|-----------------|
| {{ priority }} | {{ suggestion_type }} | {{ suggestion_description }} | {{ expected_impact }} |
{{ /if }}

{{ #if no_suggestions }}
All quality metrics are within target ranges. No improvements needed.
{{ /if }}

---

## Unassigned Tasks

{{ #if has_unassigned }}
| Product | Required Room | Reason | Suggested Action |
|---------|---------------|--------|-----------------|
| {{ product_name }} | {{ room_codes }} | {{ reason }} | {{ action }} |
{{ /if }}

{{ #if no_unassigned }}
All tasks successfully assigned. Schedule completeness: 100%.
{{ /if }}
