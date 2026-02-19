---
name: network-diagnostics
description: |
  ネットワーク品質を総合的に診断し、ボトルネックの特定と根本原因の深堀りまで行うスキル。
  接続情報、レイテンシ、ダウンロード速度、HTTP接続タイミング、経路解析を自動実行し、
  品質閾値に基づく総合評価を日本語レポートとして出力する。
  外部依存なし（OS標準ツールのみ使用）、macOSおよびLinux対応。

  Use when diagnosing network quality, troubleshooting slow connections,
  identifying network bottlenecks, measuring latency/bandwidth/jitter,
  or generating network health reports.

  「ネットワーク診断」「network diagnostics」「ネットワークが遅い」
  「latency check」「bandwidth test」「traceroute analysis」
---

# Network Diagnostics

Comprehensive network quality assessment using OS-standard tools only.
3-Phase workflow: Collect → Analyze & Report → Deep-Dive (on issues).

## 3-Phase Workflow

### Phase 1: COLLECT (Data Collection)

Run the diagnostics script to collect all network metrics as JSON:

```bash
python3 scripts/network_diagnostics.py -o /tmp/network_diag.json
```

**CLI Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `-o FILE` | Output file (default: stdout) | stdout |
| `-t host,label` | Add custom target (repeatable) | - |
| `--skip-traceroute` | Skip traceroute | false |
| `--skip-speed` | Skip download speed tests | false |
| `--ping-count N` | Ping packet count | 10 |

**Collected Data:**

1. **Connection Info** - Interface, type (Ethernet/Wi-Fi), IP, gateway, DNS, ISP, MAC, MTU
2. **Ping Tests** - Gateway + 8.8.8.8 + 1.1.1.1 (+ custom targets) → avg/min/max/jitter/loss
3. **HTTP Timing** - DNS resolution, TCP connect, TLS handshake, TTFB, total
4. **Download Speed** - Cloudflare + OVH + Hetzner CDN endpoints → Mbps
5. **Traceroute** - Hop-by-hop route analysis with RTT and timeout detection

### Phase 2: ANALYZE & REPORT

1. Read the JSON output from Phase 1
2. Load `references/network_quality_thresholds.md` for threshold definitions
3. Evaluate each metric against thresholds (connection-type aware: Ethernet vs Wi-Fi)
4. Generate report using `assets/network_report_template.md` format

**Threshold Summary:**

| Metric | Ethernet GOOD | Wi-Fi GOOD |
|--------|---------------|------------|
| Avg Ping | < 20ms | < 30ms |
| Jitter | < 5ms | < 10ms |
| Packet Loss | 0% | < 0.5% |
| Download | > 50 Mbps | > 30 Mbps |
| DNS | < 50ms | < 50ms |
| TLS | < 100ms | < 100ms |
| TTFB | < 200ms | < 200ms |

**Overall Rating:** CRITICAL if any CRITICAL → WARNING if any WARNING → GOOD

### Phase 3: DEEP-DIVE (Issues Only)

Triggered when Phase 2 detects WARNING or CRITICAL issues.

1. Load `references/deep_dive_procedures.md`
2. Identify problem category (high latency, packet loss, DNS delay, low speed, route anomaly, high jitter)
3. Run additional diagnostic commands from the procedures
4. Compare results with root cause indicators
5. Report findings with specific remediation steps

**Problem Categories:**
- High latency → Gateway vs external comparison, buffer bloat detection, MTU test
- Packet loss → Extended ping, traceroute loss point identification
- DNS delay → Resolver comparison (current vs 8.8.8.8 vs 1.1.1.1)
- Low speed → Multi-server test, duplex/MTU check
- Route anomaly → Multi-destination traceroute, ASN identification
- High jitter → Wired vs wireless comparison, channel congestion check

## Requirements

- **Python**: 3.7+ (standard library only)
- **Required commands**: `ping`, `curl`
- **Optional commands**: `traceroute` (skipped with warning if missing)
- **Platforms**: macOS, Linux (auto-detects and adapts commands)

## Resources

### scripts/
- `network_diagnostics.py` - Main data collection script (JSON output)

### references/
- `network_quality_thresholds.md` - Quality thresholds by connection type (GOOD/WARNING/CRITICAL)
- `deep_dive_procedures.md` - Deep-dive investigation procedures by problem category

### assets/
- `network_report_template.md` - Japanese report template with box-drawing tables

### tests/
- `test_network_diagnostics.py` - Unit tests for all parsers (unittest + mock)
