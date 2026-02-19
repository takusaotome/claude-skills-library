# Network Quality Thresholds

Phase 2 (ANALYZE & REPORT) where Claude evaluates collected metrics against these thresholds.

## Connection Type Detection

Thresholds vary by connection type. Use `connection.type` from diagnostics result:
- **Ethernet** - Wired connection (stricter thresholds)
- **Wi-Fi** - Wireless connection (relaxed thresholds)
- **Unknown** - Use Wi-Fi thresholds as conservative default

---

## Ethernet Thresholds

| Category | Metric | GOOD | WARNING | CRITICAL |
|----------|--------|------|---------|----------|
| Latency | Avg Ping | < 20ms | 20-100ms | > 100ms |
| Latency | Jitter (stddev) | < 5ms | 5-20ms | > 20ms |
| Latency | Packet Loss | 0% | 0.1-1% | > 1% |
| Speed | Download | > 50 Mbps | 10-50 Mbps | < 10 Mbps |

## Wi-Fi Thresholds

| Category | Metric | GOOD | WARNING | CRITICAL |
|----------|--------|------|---------|----------|
| Latency | Avg Ping | < 30ms | 30-150ms | > 150ms |
| Latency | Jitter (stddev) | < 10ms | 10-30ms | > 30ms |
| Latency | Packet Loss | < 0.5% | 0.5-2% | > 2% |
| Speed | Download | > 30 Mbps | 5-30 Mbps | < 5 Mbps |

## Common Thresholds (Connection-Type Independent)

| Category | Metric | GOOD | WARNING | CRITICAL |
|----------|--------|------|---------|----------|
| HTTP | DNS Resolution | < 50ms | 50-200ms | > 200ms |
| HTTP | TCP Connect | < 50ms | 50-200ms | > 200ms |
| HTTP | TLS Handshake | < 100ms | 100-500ms | > 500ms |
| HTTP | TTFB | < 200ms | 200-600ms | > 600ms |
| Route | Hop Count | < 15 | 15-25 | > 25 |

---

## Overall Rating Algorithm

1. Evaluate each metric against the appropriate thresholds
2. Determine per-metric rating: GOOD / WARNING / CRITICAL
3. Compute overall rating:
   - **CRITICAL** - If ANY metric is CRITICAL
   - **WARNING** - If any metric is WARNING (and none CRITICAL)
   - **GOOD** - All metrics are GOOD

## Notes

- **ISP field** is informational only (not evaluated) - may be `null` if lookup fails
- **Packet loss evaluation** uses the ping to external targets (8.8.8.8, 1.1.1.1), not gateway
- **Speed evaluation** uses the median of all successful download tests
- **Gateway ping** indicates local network health; compare with external to isolate issues
- **Multiple speed servers** reduce CDN-specific bias; use median for evaluation
