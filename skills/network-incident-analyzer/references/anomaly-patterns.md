# Anomaly Detection Patterns Reference

This document describes the anomaly detection patterns, thresholds, and correlation logic used by the network-incident-analyzer.

## Pattern Categories

### 1. Connection Failure Patterns

#### Connection Failure Spike
- **Trigger**: >50 connection failures within 1-minute window
- **Baseline**: Rolling 5-minute average of connection failures
- **Severity Levels**:
  - Warning: 2x baseline
  - Error: 3x baseline
  - Critical: 5x baseline

#### Timeout Cluster
- **Pattern**: Multiple timeout events from same source/destination pair
- **Trigger**: >10 timeouts to same destination within 2 minutes
- **Correlation**: Group by destination IP or hostname

#### Connection Refused Burst
- **Pattern**: Rapid connection refused responses
- **Trigger**: >20 refused connections within 30 seconds
- **Typical Cause**: Service down, firewall blocking, port not listening

### 2. Interface State Patterns

#### Interface Flapping
- **Pattern**: Interface alternating between up/down states
- **Trigger**: >3 state changes within 5 minutes
- **Severity**: Critical (network instability)

#### Multi-Interface Failure
- **Pattern**: Multiple interfaces going down in sequence
- **Trigger**: >2 interfaces down within 1-minute window
- **Correlation**: Group by device or connected segment

#### Protocol Flapping
- **Pattern**: Line protocol up/down without physical link change
- **Trigger**: Protocol state changes without corresponding link state
- **Typical Cause**: Duplex mismatch, keepalive failure, encapsulation issue

### 3. Routing Protocol Patterns

#### BGP Session Loss
- **Pattern**: BGP neighbor state transition to Idle/Active
- **Severity**: Critical for eBGP, High for iBGP
- **Correlation**: Track all BGP events within 2-minute window

#### OSPF Adjacency Failure
- **Pattern**: OSPF neighbor transitioning out of Full state
- **Trigger**: Adjacency change from Full to any lower state
- **Impact Assessment**: Calculate affected routes

#### Routing Convergence Burst
- **Pattern**: High volume of route updates/withdrawals
- **Trigger**: >100 routing events within 30 seconds
- **Typical Cause**: Major topology change, route oscillation

### 4. Latency Patterns

#### Latency Spike
- **Baseline**: Rolling 10-minute average latency
- **Trigger**: Current latency >2 standard deviations from baseline
- **Measurement Sources**: ICMP echo, TCP handshake time, application response

#### Jitter Anomaly
- **Pattern**: High variance in round-trip times
- **Trigger**: Jitter >20% of average latency
- **Impact**: Affects real-time applications (VoIP, video)

#### Progressive Latency Increase
- **Pattern**: Steadily increasing latency over time
- **Trigger**: >50% increase over 10-minute window
- **Typical Cause**: Queue buildup, congestion, memory leak

### 5. Error Rate Patterns

#### Error Rate Spike
- **Baseline**: Rolling 5-minute average error rate
- **Trigger**: >3x baseline error rate
- **Error Types**: CRC, frame, collision, input, output errors

#### Packet Loss Burst
- **Pattern**: Sudden increase in dropped packets
- **Trigger**: >1% packet loss over 1-minute window
- **Correlation**: Match with interface utilization data

#### Buffer Overflow
- **Pattern**: Input/output queue drops
- **Trigger**: Queue drops >0.1% of traffic
- **Typical Cause**: Traffic bursts, undersized buffers

### 6. Security Patterns

#### Authentication Failure Cluster
- **Pattern**: Multiple auth failures from same source
- **Trigger**: >5 failures within 5 minutes
- **Escalation**: Alert if failures span multiple devices

#### ACL Deny Spike
- **Pattern**: Rapid increase in ACL deny matches
- **Trigger**: >100 denies within 1 minute
- **Correlation**: Group by source IP, destination, port

#### Port Scan Detection
- **Pattern**: Single source accessing many ports
- **Trigger**: >20 different ports accessed within 30 seconds
- **Classification**: Horizontal (multiple hosts) vs Vertical (multiple ports)

---

## Correlation Logic

### Temporal Correlation

Events are correlated when they occur within a configurable time window:

| Correlation Type | Default Window | Rationale |
|------------------|----------------|-----------|
| Same Device | 5 seconds | Local events highly related |
| Adjacent Devices | 30 seconds | Allow for propagation delay |
| Network-Wide | 60 seconds | Capture cascade effects |

### Causal Correlation

Events are analyzed for cause-effect relationships:

```
Cause Event                    Effect Events
-----------                    -------------
BGP Session Down        -->    Connection Failures (30s window)
Interface Down          -->    Protocol Down, Routing Changes
Firewall Rule Change    -->    Traffic Pattern Change
```

### Correlation Confidence Scoring

Confidence calculated based on:
- Temporal proximity (closer = higher confidence)
- Causal relationship match (known patterns = higher confidence)
- Device topology (directly connected = higher confidence)
- Event frequency (rare events = higher confidence when matched)

```
confidence = (temporal_score × 0.4) + (causal_score × 0.3) +
             (topology_score × 0.2) + (rarity_score × 0.1)
```

---

## Root Cause Hypothesis Generation

### Hypothesis Templates

| Pattern Combination | Hypothesis | Confidence Modifier |
|---------------------|------------|---------------------|
| BGP Down + Connection Failures | BGP session failure caused connectivity loss | +0.3 if BGP preceded failures |
| Interface Down + Multiple Timeouts | Physical link failure disrupted traffic | +0.2 per affected downstream device |
| Error Spike + Latency Increase | Network congestion or hardware degradation | +0.15 if errors precede latency |
| Auth Failures + ACL Denies | Security incident or misconfiguration | +0.25 if single source |

### Evidence Scoring

Each hypothesis accumulates evidence:
- Direct evidence: Event explicitly supports hypothesis (+0.2)
- Indirect evidence: Event consistent with hypothesis (+0.1)
- Contradicting evidence: Event suggests alternative cause (-0.15)

### Ranking Algorithm

1. Calculate raw confidence for each hypothesis
2. Adjust based on evidence count
3. Apply temporal weight (earlier root cause = higher rank)
4. Normalize scores to 0-1 range

---

## Threshold Configuration

### Default Configuration (JSON)

```json
{
  "connection_failure": {
    "spike_threshold": 50,
    "window_seconds": 60,
    "severity_multipliers": {
      "warning": 2,
      "error": 3,
      "critical": 5
    }
  },
  "interface_flapping": {
    "state_change_threshold": 3,
    "window_seconds": 300
  },
  "latency": {
    "std_dev_threshold": 2,
    "baseline_window_seconds": 600
  },
  "error_rate": {
    "baseline_multiplier": 3,
    "baseline_window_seconds": 300
  },
  "correlation": {
    "same_device_window_seconds": 5,
    "adjacent_device_window_seconds": 30,
    "network_wide_window_seconds": 60
  },
  "security": {
    "auth_failure_threshold": 5,
    "auth_failure_window_seconds": 300,
    "acl_deny_threshold": 100,
    "acl_deny_window_seconds": 60
  }
}
```

### Tuning Recommendations

| Environment | Adjustment |
|-------------|------------|
| High-volume data center | Increase thresholds by 2-3x |
| Small branch office | Decrease thresholds by 50% |
| Real-time sensitive | Lower latency std_dev to 1.5 |
| Security-focused | Lower auth failure threshold to 3 |

---

## Severity Classification

### Impact-Based Severity

| Severity | Impact Description | Response Time |
|----------|-------------------|---------------|
| Critical | Service outage affecting multiple systems | Immediate |
| High | Single service or significant degradation | <15 minutes |
| Medium | Intermittent issues or minor degradation | <1 hour |
| Low | Cosmetic or non-impacting anomalies | Next business day |

### Automatic Escalation

Events automatically escalate severity when:
- Multiple critical events correlate within 5 minutes
- Same anomaly pattern repeats >3 times
- Anomaly duration exceeds 15 minutes without resolution

---

## Output Event Schema

### Anomaly Event Structure

```json
{
  "anomaly_id": "ANO-2024031512345",
  "type": "connection_failure_spike",
  "severity": "critical",
  "start_time": "2024-03-15T10:23:45Z",
  "end_time": "2024-03-15T10:45:12Z",
  "duration_seconds": 1287,
  "affected_devices": ["router-01", "fw-edge-01"],
  "event_count": 234,
  "baseline_value": 12,
  "peak_value": 78,
  "threshold_exceeded": 50,
  "raw_events": ["..."],
  "correlation_clusters": ["CLU-001", "CLU-002"]
}
```

### Correlation Cluster Structure

```json
{
  "cluster_id": "CLU-001",
  "confidence": 0.92,
  "root_cause_device": "core-router-01",
  "cascade_sequence": [
    {"device": "core-router-01", "event": "BGP peer down", "delta_ms": 0},
    {"device": "fw-edge-01", "event": "route withdrawal", "delta_ms": 1523},
    {"device": "switch-access-01", "event": "ARP timeout", "delta_ms": 3012}
  ],
  "total_affected_events": 45,
  "hypothesis": "BGP session failure triggered routing reconvergence"
}
```
