# Common Log Timestamp Formats Reference

## Overview

This document provides a reference for common log timestamp formats across different systems and applications. Use this to configure the multi-file-log-correlator for your specific log sources.

## Format Specification

Timestamp formats use Python's `strftime` directives:

| Directive | Meaning | Example |
|-----------|---------|---------|
| `%Y` | 4-digit year | 2025 |
| `%m` | Month (zero-padded) | 01-12 |
| `%d` | Day (zero-padded) | 01-31 |
| `%H` | Hour (24-hour, zero-padded) | 00-23 |
| `%I` | Hour (12-hour, zero-padded) | 01-12 |
| `%M` | Minute (zero-padded) | 00-59 |
| `%S` | Second (zero-padded) | 00-59 |
| `%f` | Microsecond | 000000-999999 |
| `%z` | UTC offset | +0000, -0500 |
| `%Z` | Timezone name | UTC, EST, JST |
| `%p` | AM/PM | AM, PM |
| `%b` | Month abbreviation | Jan, Feb |
| `%B` | Month full name | January |
| `%a` | Day abbreviation | Mon, Tue |

## Common Log Formats

### ISO 8601 Formats

**Standard ISO 8601:**
```
2025-01-15T10:30:45Z
2025-01-15T10:30:45+00:00
2025-01-15T10:30:45.123456Z
```
Format: `%Y-%m-%dT%H:%M:%S%z` or `%Y-%m-%dT%H:%M:%S.%fZ`

**ISO 8601 with space separator:**
```
2025-01-15 10:30:45
```
Format: `%Y-%m-%d %H:%M:%S`

### Syslog Format (RFC 3164)

**Traditional syslog:**
```
Jan 15 10:30:45
```
Format: `%b %d %H:%M:%S`
Note: No year - must be inferred from context.

**With hostname:**
```
Jan 15 10:30:45 server01 app[1234]: message
```
Format: `%b %d %H:%M:%S` (extract timestamp portion first)

### Syslog Format (RFC 5424)

**High-precision syslog:**
```
2025-01-15T10:30:45.123456+00:00
```
Format: `%Y-%m-%dT%H:%M:%S.%f%z`

### Web Server Formats

**Apache/Nginx Common Log Format:**
```
192.168.1.1 - - [15/Jan/2025:10:30:45 +0000] "GET /api HTTP/1.1"
```
Format: `%d/%b/%Y:%H:%M:%S %z`

**Apache Error Log:**
```
[Wed Jan 15 10:30:45.123456 2025] [error] message
```
Format: `%a %b %d %H:%M:%S.%f %Y`

### Database Formats

**MySQL:**
```
2025-01-15 10:30:45
```
Format: `%Y-%m-%d %H:%M:%S`

**PostgreSQL:**
```
2025-01-15 10:30:45.123 UTC
2025-01-15 10:30:45.123456+00
```
Format: `%Y-%m-%d %H:%M:%S.%f %Z` or `%Y-%m-%d %H:%M:%S.%f%z`

**MongoDB:**
```
2025-01-15T10:30:45.123+0000
```
Format: `%Y-%m-%dT%H:%M:%S.%f%z`

### Application Frameworks

**Java/Log4j:**
```
2025-01-15 10:30:45,123
```
Format: `%Y-%m-%d %H:%M:%S,%f` (note: comma before milliseconds)

**Python logging:**
```
2025-01-15 10:30:45,123
```
Format: `%Y-%m-%d %H:%M:%S,%f`

**Node.js/Bunyan:**
```
{"time":"2025-01-15T10:30:45.123Z"}
```
Format: `%Y-%m-%dT%H:%M:%S.%fZ` (in JSON)

**Ruby/Rails:**
```
2025-01-15T10:30:45.123456Z
```
Format: `%Y-%m-%dT%H:%M:%S.%fZ`

### Cloud Provider Formats

**AWS CloudWatch:**
```
2025-01-15T10:30:45.123Z
```
Format: `%Y-%m-%dT%H:%M:%S.%fZ`

**AWS CloudTrail:**
```
2025-01-15T10:30:45Z
```
Format: `%Y-%m-%dT%H:%M:%SZ`

**Azure:**
```
2025-01-15T10:30:45.1234567Z
```
Format: `%Y-%m-%dT%H:%M:%S.%fZ` (7 decimal places)

**GCP:**
```
2025-01-15T10:30:45.123456789Z
```
Format: `%Y-%m-%dT%H:%M:%S.%fZ` (nanoseconds truncated to microseconds)

### Container/Orchestration

**Docker:**
```
2025-01-15T10:30:45.123456789Z
```
Format: `%Y-%m-%dT%H:%M:%S.%fZ`

**Kubernetes:**
```
2025-01-15T10:30:45.123456789Z
```
Format: `%Y-%m-%dT%H:%M:%S.%fZ`

### Message Queues

**Kafka:**
```
1705318245123
```
Format: Unix epoch milliseconds (numeric)

**RabbitMQ:**
```
2025-01-15 10:30:45.123
```
Format: `%Y-%m-%d %H:%M:%S.%f`

## Timezone Reference

### Common Timezone Abbreviations

| Abbreviation | UTC Offset | Name |
|--------------|------------|------|
| UTC | +00:00 | Coordinated Universal Time |
| GMT | +00:00 | Greenwich Mean Time |
| EST | -05:00 | Eastern Standard Time |
| EDT | -04:00 | Eastern Daylight Time |
| CST | -06:00 | Central Standard Time |
| CDT | -05:00 | Central Daylight Time |
| MST | -07:00 | Mountain Standard Time |
| MDT | -06:00 | Mountain Daylight Time |
| PST | -08:00 | Pacific Standard Time |
| PDT | -07:00 | Pacific Daylight Time |
| JST | +09:00 | Japan Standard Time |
| CET | +01:00 | Central European Time |
| CEST | +02:00 | Central European Summer Time |

### IANA Timezone Names (Preferred)

```
America/New_York
America/Chicago
America/Denver
America/Los_Angeles
Europe/London
Europe/Paris
Europe/Berlin
Asia/Tokyo
Asia/Shanghai
Australia/Sydney
```

## Auto-Detection Patterns

The correlator attempts to auto-detect timestamp formats using these patterns:

```python
AUTO_DETECT_PATTERNS = [
    # ISO 8601 variants
    (r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z', '%Y-%m-%dT%H:%M:%S.%fZ'),
    (r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', '%Y-%m-%dT%H:%M:%SZ'),
    (r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}', '%Y-%m-%dT%H:%M:%S%z'),
    (r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', '%Y-%m-%d %H:%M:%S'),

    # Apache/Nginx
    (r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4}', '%d/%b/%Y:%H:%M:%S %z'),

    # Syslog
    (r'\w{3} \d{1,2} \d{2}:\d{2}:\d{2}', '%b %d %H:%M:%S'),

    # Unix epoch (milliseconds)
    (r'^\d{13}$', 'epoch_ms'),

    # Unix epoch (seconds)
    (r'^\d{10}$', 'epoch_s'),
]
```

## Configuration Examples

### Multi-Source Configuration

```yaml
sources:
  - name: nginx
    file: nginx/access.log
    timezone: America/New_York
    format: "%d/%b/%Y:%H:%M:%S %z"

  - name: app
    file: app/application.log
    timezone: UTC
    format: "%Y-%m-%d %H:%M:%S,%f"

  - name: database
    file: postgres/postgresql.log
    timezone: America/New_York
    format: "%Y-%m-%d %H:%M:%S.%f %Z"

  - name: redis
    file: redis/redis.log
    timezone: UTC
    format: "%d %b %H:%M:%S.%f"
    # Note: Redis doesn't include year

output:
  timezone: UTC
```

## Troubleshooting

### Common Issues

**1. Year not in timestamp:**
- Syslog and some formats omit year
- Infer from file modification time or log rotation pattern
- Specify explicitly: `--assume-year 2025`

**2. Ambiguous month/day order:**
- `01/02/2025` - January 2 or February 1?
- Specify format explicitly or check surrounding entries

**3. Timezone abbreviation ambiguity:**
- `CST` = Central Standard Time (US) or China Standard Time?
- Use IANA names when possible

**4. Milliseconds vs microseconds:**
- `%f` expects 6 digits (microseconds)
- For 3-digit milliseconds, pad with zeros or use custom parsing
