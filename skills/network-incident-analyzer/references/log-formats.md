# Network Log Format Reference

This document describes the log formats supported by the network-incident-analyzer and their parsing patterns.

## Cisco IOS/NX-OS Format

### Standard Format
```
*Mar 15 10:23:45.123: %LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to down
```

### Components
- `*` -- Timestamp prefix marker
- `Mar 15 10:23:45.123` -- Timestamp (MMM DD HH:MM:SS.mmm)
- `%LINK-3-UPDOWN` -- Facility-Severity-Mnemonic
- Message text follows the colon

### Severity Levels
| Level | Name | Description |
|-------|------|-------------|
| 0 | Emergency | System unusable |
| 1 | Alert | Immediate action needed |
| 2 | Critical | Critical conditions |
| 3 | Error | Error conditions |
| 4 | Warning | Warning conditions |
| 5 | Notice | Normal but significant |
| 6 | Info | Informational |
| 7 | Debug | Debug messages |

### Regex Pattern
```python
CISCO_IOS_PATTERN = r'^\*?(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}(?:\.\d+)?):?\s*%(\w+)-(\d)-(\w+):\s*(.+)$'
```

### Key Event Types
- `%LINK-3-UPDOWN` -- Interface state change
- `%LINEPROTO-5-UPDOWN` -- Line protocol state change
- `%BGP-3-NOTIFICATION` -- BGP session notification
- `%OSPF-4-ADJCHG` -- OSPF adjacency change
- `%SYS-5-RESTART` -- System restart
- `%SEC-6-IPACCESSLOGP` -- ACL match logging

---

## Juniper JunOS Format

### Standard Format
```
Mar 15 10:23:45 router-name rpd[1234]: BGP_NEIGHBOR_STATE_CHANGED: Peer 10.0.0.1 state changed from Established to Idle
```

### Components
- `Mar 15 10:23:45` -- Timestamp (MMM DD HH:MM:SS)
- `router-name` -- Hostname
- `rpd[1234]` -- Process name and PID
- Message text follows the colon

### Regex Pattern
```python
JUNOS_PATTERN = r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\w+)\[(\d+)\]:\s*(.+)$'
```

### Key Event Types
- `BGP_NEIGHBOR_STATE_CHANGED` -- BGP session state transition
- `OSPF_NEIGHBOR_DOWN` -- OSPF neighbor loss
- `RPD_ISIS_ADJDOWN` -- IS-IS adjacency down
- `SNMPD_AUTH_FAILURE` -- SNMP authentication failure
- `UI_AUTH_EVENT` -- User authentication event
- `CHASSISD_FPC_OFFLINE` -- Line card offline

---

## Palo Alto Firewall Format

### CSV Format
```
Mar 15 10:23:45,INFO,TRAFFIC,end,2024/03/15 10:23:45,10.0.0.1,192.168.1.1,0.0.0.0,0.0.0.0,Allow_All,user@domain,,web-browsing,vsys1,trust,untrust,ethernet1/1,ethernet1/2,Log_Forwarding,2024/03/15 10:23:45,12345,1,54321,443,0,0,0x100000,tcp,allow,1234,567,890,15,2024/03/15 10:23:30,45,any,0,9876543,0x8000000000000000,10.0.0.0-10.255.255.255,US,0,5,10,aged-out,12,34,0,0,,PA-5220,from-policy,,,0,,0,,N/A,0,0,0,0,0,0
```

### Components
- Timestamp in two formats (syslog prefix and field)
- Comma-separated values following PAN-OS log format
- Key fields: type, subtype, source IP, destination IP, action, application

### Regex Pattern
```python
PALO_ALTO_PATTERN = r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}),(\w+),(\w+),(\w+),'
```

### Log Types
| Type | Description |
|------|-------------|
| TRAFFIC | Traffic flow logs |
| THREAT | Threat/IPS logs |
| SYSTEM | System events |
| CONFIG | Configuration changes |
| HIPMATCH | HIP profile matches |
| GLOBALPROTECT | VPN events |

---

## F5 BIG-IP Format

### Standard Format
```
Mar 15 10:23:45 bigip-ltm01 info tmm[1234]: Rule /Common/redirect_rule <HTTP_REQUEST>: Client 10.0.0.1 redirected to https://example.com
```

### Components
- `Mar 15 10:23:45` -- Timestamp
- `bigip-ltm01` -- Hostname
- `info` -- Log level
- `tmm[1234]` -- Process and PID
- Message with optional iRule context

### Regex Pattern
```python
F5_PATTERN = r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\w+)\s+(\w+)\[(\d+)\]:\s*(.+)$'
```

### Key Processes
| Process | Description |
|---------|-------------|
| tmm | Traffic Management Module |
| mcpd | Master Control Program Daemon |
| httpd | Management GUI |
| sod | Statistics collection |
| gtmd | Global Traffic Manager |

### Important Events
- Pool member state changes (up/down)
- Virtual server status changes
- SSL handshake failures
- iRule execution errors
- Connection limit exceeded

---

## Generic Syslog Format (RFC 5424)

### Standard Format
```
<134>1 2024-03-15T10:23:45.123Z hostname appname 1234 MSGID - Message content here
```

### Legacy BSD Format (RFC 3164)
```
<134>Mar 15 10:23:45 hostname process[1234]: Message content here
```

### Priority Calculation
- Priority = (Facility × 8) + Severity
- Example: `<134>` = Facility 16 (local0) × 8 + Severity 6 (info) = 134

### Regex Patterns
```python
# RFC 5424
SYSLOG_5424_PATTERN = r'^<(\d+)>1\s+(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)\s+(\S+)\s+(\S+)\s+(\d+|-)\s+(\S+)\s+(-|\[.+\])\s*(.*)$'

# RFC 3164
SYSLOG_3164_PATTERN = r'^<(\d+)>(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\S+?)(?:\[(\d+)\])?:\s*(.+)$'
```

### Facility Codes
| Code | Facility |
|------|----------|
| 0 | kern |
| 1 | user |
| 2 | mail |
| 3 | daemon |
| 4 | auth |
| 5 | syslog |
| 6 | lpr |
| 7 | news |
| 16-23 | local0-local7 |

---

## JSON Structured Logs

### Standard Schema
```json
{
  "timestamp": "2024-03-15T10:23:45.123Z",
  "level": "error",
  "device": "core-router-01",
  "source_ip": "10.0.0.1",
  "destination_ip": "192.168.1.1",
  "event_type": "connection_failed",
  "message": "TCP connection timeout after 30s",
  "metadata": {
    "port": 443,
    "protocol": "tcp",
    "interface": "eth0"
  }
}
```

### Required Fields
| Field | Type | Description |
|-------|------|-------------|
| timestamp | ISO 8601 string | Event timestamp |
| level | string | Log level (debug, info, warn, error, critical) |
| message | string | Human-readable message |

### Optional Fields
| Field | Type | Description |
|-------|------|-------------|
| device | string | Device hostname or identifier |
| source_ip | string | Source IP address |
| destination_ip | string | Destination IP address |
| event_type | string | Categorized event type |
| metadata | object | Additional structured data |

---

## Timestamp Parsing

### Supported Formats
| Format | Example | Pattern |
|--------|---------|---------|
| ISO 8601 | 2024-03-15T10:23:45.123Z | `%Y-%m-%dT%H:%M:%S.%fZ` |
| ISO 8601 (no ms) | 2024-03-15T10:23:45Z | `%Y-%m-%dT%H:%M:%SZ` |
| Syslog | Mar 15 10:23:45 | `%b %d %H:%M:%S` |
| Syslog (ms) | Mar 15 10:23:45.123 | `%b %d %H:%M:%S.%f` |
| Cisco | *Mar 15 10:23:45.123 | `*%b %d %H:%M:%S.%f` |
| PAN-OS | 2024/03/15 10:23:45 | `%Y/%m/%d %H:%M:%S` |

### Year Inference
When logs lack year information (e.g., syslog format), the analyzer:
1. Uses the current year by default
2. If the resulting date is in the future, uses the previous year
3. Respects `--year` flag if provided explicitly

### Timezone Handling
1. Timestamps without timezone info assumed to be in the device's configured timezone
2. Use `--device-timezone` to specify per-file timezone overrides
3. All timestamps normalized to UTC for correlation
4. Output reports show both UTC and local time for clarity
