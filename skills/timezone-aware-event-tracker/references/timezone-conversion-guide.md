# Timezone Conversion Guide

This reference document provides comprehensive guidance on timezone handling, conversion best practices, and common pitfalls for distributed system event tracking.

## Common Timezone Abbreviations and IANA Names

### United States

| Abbreviation | IANA Name | UTC Offset (Standard) | UTC Offset (DST) |
|--------------|-----------|----------------------|------------------|
| PST/PDT | America/Los_Angeles | UTC-8 | UTC-7 |
| MST/MDT | America/Denver | UTC-7 | UTC-6 |
| CST/CDT | America/Chicago | UTC-6 | UTC-5 |
| EST/EDT | America/New_York | UTC-5 | UTC-4 |

### Asia-Pacific

| Abbreviation | IANA Name | UTC Offset | DST |
|--------------|-----------|------------|-----|
| JST | Asia/Tokyo | UTC+9 | No DST |
| KST | Asia/Seoul | UTC+9 | No DST |
| CST (China) | Asia/Shanghai | UTC+8 | No DST |
| SGT | Asia/Singapore | UTC+8 | No DST |
| IST | Asia/Kolkata | UTC+5:30 | No DST |
| AEST/AEDT | Australia/Sydney | UTC+10 | UTC+11 |

### Europe

| Abbreviation | IANA Name | UTC Offset (Standard) | UTC Offset (DST) |
|--------------|-----------|----------------------|------------------|
| GMT/BST | Europe/London | UTC+0 | UTC+1 |
| CET/CEST | Europe/Paris | UTC+1 | UTC+2 |
| EET/EEST | Europe/Helsinki | UTC+2 | UTC+3 |

## Daylight Saving Time (DST) Rules

### United States (2007-present)

- **Spring Forward**: Second Sunday of March at 2:00 AM local time
- **Fall Back**: First Sunday of November at 2:00 AM local time

```
2024 DST Transitions (US):
- March 10, 2024: 2:00 AM → 3:00 AM (clocks spring forward)
- November 3, 2024: 2:00 AM → 1:00 AM (clocks fall back)
```

### Europe (EU)

- **Spring Forward**: Last Sunday of March at 1:00 AM UTC
- **Fall Back**: Last Sunday of October at 1:00 AM UTC

```
2024 DST Transitions (EU):
- March 31, 2024: 1:00 AM UTC → 2:00 AM UTC
- October 27, 2024: 1:00 AM UTC → 0:00 AM UTC
```

### Regions Without DST

- Japan (JST)
- China (CST)
- India (IST)
- Singapore (SGT)
- Arizona, USA (except Navajo Nation)
- Hawaii, USA

## Conversion Formulas

### PST ↔ UTC

```
Standard Time (Nov - Mar):
  UTC = PST + 8 hours
  PST = UTC - 8 hours

Daylight Time (Mar - Nov):
  UTC = PDT + 7 hours
  PDT = UTC - 7 hours
```

### EST ↔ UTC

```
Standard Time (Nov - Mar):
  UTC = EST + 5 hours
  EST = UTC - 5 hours

Daylight Time (Mar - Nov):
  UTC = EDT + 4 hours
  EDT = UTC - 4 hours
```

### JST ↔ UTC

```
Year-round (no DST):
  UTC = JST - 9 hours
  JST = UTC + 9 hours
```

### Cross-Region Examples

```
PST to EST: EST = PST + 3 hours (always, DST shifts together)
PST to JST: JST = PST + 17 hours (standard) / + 16 hours (PDT)
EST to JST: JST = EST + 14 hours (standard) / + 13 hours (EDT)
```

## Ambiguous Time Handling

### Spring Forward Gap

During spring DST transition, some local times do not exist:

```
US Example (March 10, 2024):
- 1:59:59 AM PST exists
- 2:00:00 AM PST does not exist (skipped to 3:00 AM PDT)
- 3:00:00 AM PDT exists

Strategy: If an event claims to occur at 2:30 AM on DST spring date:
1. Flag as "non-existent time"
2. Assume it means 3:30 AM PDT (post-transition)
3. Log warning for human review
```

### Fall Back Overlap

During fall DST transition, some local times occur twice:

```
US Example (November 3, 2024):
- 1:30 AM PDT exists (first occurrence)
- 1:30 AM PST exists (second occurrence, 1 hour later)

Strategy: If an event occurs at 1:30 AM on DST fall date:
1. Flag as "ambiguous time"
2. Check for offset suffix (-07:00 vs -08:00) if available
3. Use event context (before/after) to infer correct instance
4. Default to first occurrence (PDT) if no context available
```

## Timestamp Formats and Parsing

### ISO 8601 (Recommended)

```
With offset:     2024-03-15T10:30:00-07:00
With Z (UTC):    2024-03-15T17:30:00Z
With timezone:   2024-03-15T10:30:00 America/Los_Angeles
```

### Common Log Formats

```
Apache:          15/Mar/2024:10:30:00 -0700
Syslog:          Mar 15 10:30:00
ISO basic:       20240315T103000-0700
US format:       03/15/2024 10:30:00 AM PST
```

### Parsing Priority

When parsing timestamps, follow this priority:

1. **Explicit offset** (-07:00, +09:00): Use directly
2. **IANA timezone** (America/Los_Angeles): Convert using timezone rules
3. **Abbreviation with date** (PST on March 15): Check if DST applies
4. **Abbreviation only** (PST): Assume standard time, flag as potentially ambiguous
5. **No timezone info**: Require source timezone specification

## Best Practices for Event Tracking

### 1. Store in UTC

Always convert and store events in UTC internally:

```python
# Good
stored_timestamp = "2024-03-15T17:30:00Z"

# Avoid
stored_timestamp = "2024-03-15T10:30:00 PST"
```

### 2. Preserve Original Timestamp

Keep the original timestamp for debugging:

```python
event = {
    "normalized_timestamp": "2024-03-15T17:30:00Z",
    "original_timestamp": "2024-03-15 10:30:00 PST",
    "source_timezone": "America/Los_Angeles"
}
```

### 3. Use IANA Timezone Names

```python
# Good
timezone = "America/Los_Angeles"

# Avoid (ambiguous)
timezone = "PST"  # Could be Pacific, Philippines, or Pakistan
```

### 4. Handle DST Transitions Explicitly

```python
# Check if timestamp falls in DST transition period
if is_dst_transition_period(timestamp, timezone):
    event["dst_warning"] = True
    event["dst_status"] = "ambiguous"
```

### 5. Log Timezone Assumptions

When making assumptions about timezone, log them:

```python
if not timestamp_has_timezone(raw_timestamp):
    assumed_tz = get_default_timezone(source_system)
    log.warning(f"No timezone in timestamp, assuming {assumed_tz}")
```

## Common Pitfalls

### 1. Confusing CST

"CST" can mean:
- Central Standard Time (US): UTC-6
- China Standard Time: UTC+8
- Cuba Standard Time: UTC-5

**Solution**: Always use IANA names or require explicit offset.

### 2. Ignoring DST in Calculations

```python
# Wrong: Assumes fixed offset
tokyo_time = utc_time + timedelta(hours=9)  # Correct for JST
la_time = utc_time - timedelta(hours=8)     # Wrong during PDT!

# Correct: Use timezone library
la_tz = ZoneInfo("America/Los_Angeles")
la_time = utc_time.astimezone(la_tz)
```

### 3. Server Time vs Event Time

Distinguish between:
- **Server time**: When the server recorded the event
- **Event time**: When the event actually occurred

```python
event = {
    "event_time": "2024-03-15T10:30:00-07:00",      # When it happened
    "server_time": "2024-03-15T10:30:05-05:00",    # When server logged it
    "event_timezone": "America/Los_Angeles",
    "server_timezone": "America/New_York"
}
```

### 4. Midnight Boundary Issues

Events near midnight may appear to be on different dates in different timezones:

```
23:30 PST on March 14 = 07:30 UTC on March 15 = 16:30 JST on March 15
```

**Solution**: When grouping events by date, specify the reference timezone.

## Python Code Examples

### Using zoneinfo (Python 3.9+)

```python
from datetime import datetime
from zoneinfo import ZoneInfo

# Parse UTC timestamp
utc_time = datetime.fromisoformat("2024-03-15T17:30:00+00:00")

# Convert to different timezones
la_time = utc_time.astimezone(ZoneInfo("America/Los_Angeles"))
tokyo_time = utc_time.astimezone(ZoneInfo("Asia/Tokyo"))

print(f"UTC: {utc_time}")
print(f"Los Angeles: {la_time}")  # Handles DST automatically
print(f"Tokyo: {tokyo_time}")
```

### Detecting DST Status

```python
from datetime import datetime
from zoneinfo import ZoneInfo

def get_dst_status(dt: datetime, tz: ZoneInfo) -> str:
    """Determine if a datetime is in DST, standard time, or transition."""
    if dt.dst():
        return "daylight_time"
    else:
        return "standard_time"

def is_dst_transition_date(date, tz_name: str) -> bool:
    """Check if a date has a DST transition."""
    tz = ZoneInfo(tz_name)
    # Check midnight to midnight for offset changes
    start = datetime(date.year, date.month, date.day, 0, 0, tzinfo=tz)
    end = datetime(date.year, date.month, date.day, 23, 59, tzinfo=tz)
    return start.utcoffset() != end.utcoffset()
```

### Parsing Ambiguous Timestamps

```python
from datetime import datetime
from zoneinfo import ZoneInfo
import re

def parse_timestamp_with_tz(raw: str, default_tz: str = "UTC") -> dict:
    """Parse timestamp and extract timezone info."""
    # Try ISO format with offset
    iso_pattern = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})([+-]\d{2}:\d{2}|Z)"
    match = re.match(iso_pattern, raw)
    if match:
        return {
            "datetime": datetime.fromisoformat(raw),
            "source": "iso_offset",
            "ambiguous": False
        }

    # Try with timezone abbreviation
    tz_abbrev_pattern = r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(PST|PDT|EST|EDT|JST|UTC)"
    match = re.match(tz_abbrev_pattern, raw)
    if match:
        dt_str, tz_abbrev = match.groups()
        # Map abbreviation to IANA (simplified)
        tz_map = {
            "PST": "America/Los_Angeles",
            "PDT": "America/Los_Angeles",
            "EST": "America/New_York",
            "EDT": "America/New_York",
            "JST": "Asia/Tokyo",
            "UTC": "UTC"
        }
        return {
            "datetime_str": dt_str,
            "tz_name": tz_map.get(tz_abbrev, default_tz),
            "source": "abbreviation",
            "ambiguous": tz_abbrev in ["PST", "EST"]  # Could be DST
        }

    # No timezone info
    return {
        "datetime_str": raw,
        "tz_name": default_tz,
        "source": "assumed",
        "ambiguous": True
    }
```
