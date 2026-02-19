# Deep-Dive Investigation Procedures

Phase 3 (DEEP-DIVE) reference. Load this when Phase 2 detects WARNING or CRITICAL issues.
For each problem category: symptoms, additional test commands, common root causes, and remediation.

---

## 1. High Latency

### Symptoms
- Avg ping > threshold (Ethernet: 20ms / Wi-Fi: 30ms)
- Gateway ping normal but external ping high → upstream issue
- Gateway ping also high → local network issue

### Additional Tests

```bash
# Extended ping with timestamps (50 packets)
ping -c 50 8.8.8.8

# Buffer bloat detection: ping under load
# Terminal 1: Start download
curl -o /dev/null https://speed.cloudflare.com/__down?bytes=100000000 &
# Terminal 2: Measure ping during download
ping -c 20 8.8.8.8
# Compare latency under load vs idle

# MTU path discovery
ping -D -s 1472 -c 3 8.8.8.8   # macOS
ping -M do -s 1472 -c 3 8.8.8.8 # Linux
# If fails, reduce size by 10 until success

# Gateway vs external comparison
ping -c 10 <gateway_ip>
ping -c 10 8.8.8.8
```

### Common Root Causes

| Root Cause | Indicator | Remediation |
|------------|-----------|-------------|
| Buffer bloat | Latency spikes during download | Enable SQM/QoS on router |
| Wi-Fi congestion | High jitter, intermittent spikes | Change channel, use 5GHz |
| ISP congestion | High external ping, low gateway ping | Contact ISP, consider VPN |
| MTU mismatch | Fragmentation, packet loss at specific sizes | Set MTU to discovered value |
| VPN overhead | High latency with VPN on, normal without | Expected; try different VPN server |

---

## 2. Packet Loss

### Symptoms
- Packet loss > 0% on external targets
- May be intermittent (run extended tests)

### Additional Tests

```bash
# Extended ping (100 packets) for statistical significance
ping -c 100 8.8.8.8

# Compare targets to isolate loss point
ping -c 50 <gateway_ip>
ping -c 50 8.8.8.8
ping -c 50 1.1.1.1

# Traceroute with loss detection
# Run traceroute multiple times to identify consistent loss points
traceroute -q 5 8.8.8.8
```

### Common Root Causes

| Root Cause | Indicator | Remediation |
|------------|-----------|-------------|
| Wi-Fi interference | Loss at gateway, low RSSI | Move closer to AP, change channel |
| Cable fault | Loss at gateway on wired | Replace cable, check connectors |
| ISP issue | Loss at specific hop in traceroute | Contact ISP with traceroute data |
| Network congestion | Loss increases during peak hours | QoS, bandwidth upgrade |
| Firewall/rate limit | Consistent loss at exact percentage | Check firewall ICMP rules |

---

## 3. DNS Delay

### Symptoms
- DNS resolution time > 50ms
- Affects all HTTP timing measurements

### Additional Tests

```bash
# Compare DNS resolvers
# Current DNS
curl -s -o /dev/null -w "DNS: %{time_namelookup}s\n" https://www.example.com

# Google DNS
curl -s -o /dev/null -w "DNS: %{time_namelookup}s\n" --dns-servers 8.8.8.8 https://www.example.com

# Cloudflare DNS
curl -s -o /dev/null -w "DNS: %{time_namelookup}s\n" --dns-servers 1.1.1.1 https://www.example.com

# Direct DNS query timing
dig @192.168.1.1 www.google.com     # Current resolver
dig @8.8.8.8 www.google.com          # Google
dig @1.1.1.1 www.google.com          # Cloudflare

# DNS cache check (query twice, second should be faster)
dig www.example.com
dig www.example.com
```

### Common Root Causes

| Root Cause | Indicator | Remediation |
|------------|-----------|-------------|
| Slow resolver | All DNS queries slow via current DNS | Switch to 8.8.8.8 or 1.1.1.1 |
| DNS over router | Router DNS forwarding adds latency | Configure direct DNS on device |
| DNS pollution | Inconsistent results between resolvers | Use DoH/DoT (DNS over HTTPS/TLS) |
| No local cache | Every query is slow (no speedup on repeat) | Install local DNS cache (dnsmasq) |

---

## 4. Low Download Speed

### Symptoms
- Download speed below threshold
- May vary significantly between test servers

### Additional Tests

```bash
# Test multiple servers to rule out server-side throttling
curl -o /dev/null -w "Speed: %{speed_download} bytes/sec\n" \
  https://speed.cloudflare.com/__down?bytes=50000000

# Test with different file sizes
curl -o /dev/null -w "Speed: %{speed_download} bytes/sec\n" \
  https://speed.cloudflare.com/__down?bytes=1000000    # 1MB
curl -o /dev/null -w "Speed: %{speed_download} bytes/sec\n" \
  https://speed.cloudflare.com/__down?bytes=50000000   # 50MB

# Check interface speed/duplex (Linux)
ethtool eth0 | grep -i speed
ethtool eth0 | grep -i duplex

# Check interface speed (macOS)
networksetup -getMedia en0

# MTU check
ping -D -s 1472 -c 3 8.8.8.8      # macOS
ping -M do -s 1472 -c 3 8.8.8.8   # Linux
```

### Common Root Causes

| Root Cause | Indicator | Remediation |
|------------|-----------|-------------|
| ISP throttling | Speed matches plan limit | Upgrade plan or contact ISP |
| Wi-Fi limitation | Low speed on Wi-Fi, fast on Ethernet | Use 5GHz, move closer to AP |
| Half-duplex | Speed ~50% of expected, high under load | Fix duplex negotiation |
| MTU issues | Speed drops with large transfers | Adjust MTU (typically 1500) |
| Background traffic | Speed varies, other devices using bandwidth | Check for bandwidth-heavy applications |
| Cable quality | Low speed on Ethernet, inconsistent | Replace with Cat6/Cat6a cable |

---

## 5. Route Anomalies

### Symptoms
- High hop count (> 15)
- Timeout hops in traceroute
- Unexpected routing paths

### Additional Tests

```bash
# Multiple destination traceroutes for comparison
traceroute 8.8.8.8
traceroute 1.1.1.1
traceroute www.cloudflare.com

# ASN identification (if whois available)
whois -h whois.radb.net <suspicious_ip>

# Reverse DNS for hop identification
dig -x <hop_ip>

# TCP traceroute (bypasses ICMP filtering)
# macOS
sudo traceroute -T -p 443 8.8.8.8
# Linux
sudo traceroute -T -p 443 8.8.8.8
```

### Common Root Causes

| Root Cause | Indicator | Remediation |
|------------|-----------|-------------|
| Sub-optimal routing | Unnecessary geographic detours | Contact ISP, use VPN |
| ICMP filtering | Single timeout hop, no latency impact | Normal; many routers drop ICMP |
| Asymmetric routing | Different paths forward vs return | Usually ISP-level; difficult to fix |
| Routing loop | Same IPs appearing multiple times | Contact ISP immediately |
| Congested peering | High latency at ISP boundary hops | Try different ISP or VPN |

---

## 6. High Jitter

### Symptoms
- Stddev (jitter) above threshold
- Latency varies significantly between packets
- Affects real-time applications (VoIP, video calls)

### Additional Tests

```bash
# Extended ping to capture jitter pattern
ping -c 100 8.8.8.8

# Compare wired vs wireless (if possible)
# Connect via Ethernet and test
ping -c 50 8.8.8.8

# Wi-Fi channel scan (macOS)
/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s

# Wi-Fi diagnostics (macOS)
# Option+Click Wi-Fi icon for detailed info (RSSI, noise, channel)
```

### Common Root Causes

| Root Cause | Indicator | Remediation |
|------------|-----------|-------------|
| Wi-Fi interference | High jitter on Wi-Fi, stable on Ethernet | Change channel, use 5GHz band |
| Channel congestion | Many SSIDs on same channel | Use Wi-Fi analyzer, pick least congested |
| Microwave/Bluetooth | Periodic spikes on 2.4GHz | Move AP, use 5GHz |
| QoS misconfiguration | Jitter during mixed traffic | Configure proper QoS/WMM |
| Weak signal | High jitter + low RSSI | Move closer to AP, add extender |

---

## Investigation Workflow

1. **Identify the problem category** from Phase 2 results
2. **Load this document** for the relevant category
3. **Run additional tests** from the commands listed
4. **Compare results** with the root cause indicators
5. **Report findings** with specific remediation steps
6. **Re-run diagnostics** after applying fixes to verify improvement
