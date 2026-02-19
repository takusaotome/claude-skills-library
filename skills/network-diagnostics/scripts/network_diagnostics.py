#!/usr/bin/env python3
"""
Network Diagnostics - Comprehensive network quality assessment tool.

Collects connection info, latency, download speed, HTTP timing, and
traceroute data using only OS-standard tools (no external dependencies).

Usage:
    python3 network_diagnostics.py                          # All tests → stdout JSON
    python3 network_diagnostics.py -o results.json          # File output
    python3 network_diagnostics.py -t 10.0.0.50,MyServer    # Custom target
    python3 network_diagnostics.py --skip-traceroute        # Skip traceroute
    python3 network_diagnostics.py --skip-speed             # Skip speed test
    python3 network_diagnostics.py --ping-count 20          # Custom ping count

Requires: Python 3.7+, ping, curl
Optional: traceroute (skipped with warning if missing)
"""

import argparse
import json
import platform
import re
import shutil
import socket
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple


# =============================================================================
# Utility Functions
# =============================================================================

def hex_netmask_to_cidr(hex_mask: str) -> Optional[int]:
    """Convert hex netmask (e.g., 0xffffff00) to CIDR prefix length."""
    try:
        mask_int = int(hex_mask, 16)
        return bin(mask_int).count('1')
    except (ValueError, TypeError):
        return None


def dotted_netmask_to_cidr(mask: str) -> Optional[int]:
    """Convert dotted-decimal netmask (e.g., 255.255.255.0) to CIDR prefix length."""
    try:
        parts = mask.split('.')
        if len(parts) != 4:
            return None
        binary = ''.join(format(int(p), '08b') for p in parts)
        return binary.count('1')
    except (ValueError, TypeError):
        return None


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class ConnectionInfo:
    """Network connection information."""
    interface: str
    type: str  # Ethernet, Wi-Fi, Unknown
    ip: str
    cidr: Optional[int]
    gateway: str
    dns: List[str]
    isp: Optional[str]
    mac: Optional[str]
    mtu: Optional[int]

    def to_dict(self) -> Dict:
        return {
            'interface': self.interface,
            'type': self.type,
            'ip': self.ip,
            'cidr': self.cidr,
            'gateway': self.gateway,
            'dns': self.dns,
            'isp': self.isp,
            'mac': self.mac,
            'mtu': self.mtu,
        }


@dataclass
class PingResult:
    """Ping test result."""
    target: str
    target_name: str
    avg_ms: Optional[float]
    min_ms: Optional[float]
    max_ms: Optional[float]
    stddev_ms: Optional[float]
    packet_loss_pct: float
    count: int

    def to_dict(self) -> Dict:
        return {
            'target': self.target,
            'target_name': self.target_name,
            'avg_ms': self.avg_ms,
            'min_ms': self.min_ms,
            'max_ms': self.max_ms,
            'stddev_ms': self.stddev_ms,
            'packet_loss_pct': self.packet_loss_pct,
            'count': self.count,
        }


@dataclass
class HttpTiming:
    """HTTP connection timing breakdown."""
    url: str
    dns_ms: float
    tcp_ms: float
    tls_ms: float
    ttfb_ms: float
    total_ms: float
    http_code: int
    size_bytes: int

    def to_dict(self) -> Dict:
        return {
            'url': self.url,
            'dns_ms': round(self.dns_ms, 3),
            'tcp_ms': round(self.tcp_ms, 3),
            'tls_ms': round(self.tls_ms, 3),
            'ttfb_ms': round(self.ttfb_ms, 3),
            'total_ms': round(self.total_ms, 3),
            'http_code': self.http_code,
            'size_bytes': self.size_bytes,
        }


@dataclass
class DownloadSpeed:
    """Download speed test result."""
    url: str
    label: str
    speed_mbps: float
    size_bytes: int
    duration_sec: float

    def to_dict(self) -> Dict:
        return {
            'url': self.url,
            'label': self.label,
            'speed_mbps': round(self.speed_mbps, 2),
            'size_bytes': self.size_bytes,
            'duration_sec': round(self.duration_sec, 3),
        }


@dataclass
class TracerouteHop:
    """Single traceroute hop."""
    hop_number: int
    hostname: Optional[str]
    ip: Optional[str]
    rtt_ms: Optional[float]
    is_timeout: bool

    def to_dict(self) -> Dict:
        return {
            'hop_number': self.hop_number,
            'hostname': self.hostname,
            'ip': self.ip,
            'rtt_ms': self.rtt_ms,
            'is_timeout': self.is_timeout,
        }


@dataclass
class TracerouteResult:
    """Traceroute result."""
    target: str
    target_name: str
    hops: List[TracerouteHop]
    total_hops: int

    def to_dict(self) -> Dict:
        return {
            'target': self.target,
            'target_name': self.target_name,
            'hops': [h.to_dict() for h in self.hops],
            'total_hops': self.total_hops,
        }


@dataclass
class DiagnosticsResult:
    """Complete diagnostics result."""
    timestamp: str
    platform: str
    connection: Optional[ConnectionInfo]
    ping: List[PingResult]
    http: List[HttpTiming]
    download: List[DownloadSpeed]
    traceroute: List[TracerouteResult]
    errors: List[str]
    skipped_tests: List[str]

    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp,
            'platform': self.platform,
            'connection': self.connection.to_dict() if self.connection else None,
            'ping': [p.to_dict() for p in self.ping],
            'http': [h.to_dict() for h in self.http],
            'download': [d.to_dict() for d in self.download],
            'traceroute': [t.to_dict() for t in self.traceroute],
            'errors': self.errors,
            'skipped_tests': self.skipped_tests,
        }


# =============================================================================
# Platform Detection
# =============================================================================

class PlatformDetector:
    """Detect OS platform and check command availability."""

    def system(self) -> str:
        return platform.system()

    def check_command(self, cmd: str) -> bool:
        return shutil.which(cmd) is not None


# =============================================================================
# Connection Info Collector
# =============================================================================

class ConnectionCollector:
    """Collect network connection information."""

    TIMEOUT = 10  # seconds

    def __init__(self, detector: PlatformDetector):
        self._detector = detector
        self._errors: List[str] = []

    def collect(self) -> Optional[ConnectionInfo]:
        """Collect connection info for the active interface."""
        try:
            system = self._detector.system()
            if system == 'Darwin':
                return self._collect_macos()
            elif system == 'Linux':
                return self._collect_linux()
            else:
                self._errors.append(f"Unsupported platform: {system}")
                return None
        except Exception as e:
            self._errors.append(f"Connection info collection failed: {e}")
            return None

    # --- macOS ---

    def _collect_macos(self) -> Optional[ConnectionInfo]:
        # Get default interface
        route_out = self._run_cmd(['route', 'get', 'default'])
        if not route_out:
            return None
        iface = self._parse_macos_default_interface(route_out)
        if not iface:
            self._errors.append("Could not determine default interface")
            return None

        # Get IP, mask, MAC, MTU from ifconfig
        ifconfig_out = self._run_cmd(['ifconfig', iface])
        if not ifconfig_out:
            return None
        ip, cidr, mac, mtu = self._parse_macos_ifconfig(ifconfig_out, iface)

        # Get gateway
        netstat_out = self._run_cmd(['netstat', '-rn'])
        gateway = self._parse_macos_gateway(netstat_out) if netstat_out else ''

        # Get DNS
        scutil_out = self._run_cmd(['scutil', '--dns'])
        dns = self._parse_scutil_dns(scutil_out) if scutil_out else []

        # Get interface type
        nsetup_out = self._run_cmd(['networksetup', '-listallhardwareports'])
        itype = self._parse_networksetup_type(nsetup_out, iface) if nsetup_out else 'Unknown'

        # Try ISP via reverse DNS of first DNS server
        isp = self._try_isp_lookup(dns)

        return ConnectionInfo(
            interface=iface, type=itype, ip=ip or '',
            cidr=cidr, gateway=gateway or '', dns=dns,
            isp=isp, mac=mac, mtu=mtu,
        )

    def _parse_macos_default_interface(self, output: str) -> Optional[str]:
        m = re.search(r'interface:\s*(\S+)', output)
        return m.group(1) if m else None

    def _parse_macos_ifconfig(self, output: str, iface: str) -> Tuple[Optional[str], Optional[int], Optional[str], Optional[int]]:
        ip = cidr = mac = mtu = None

        m = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)\s+netmask\s+(0x[0-9a-fA-F]+)', output)
        if m:
            ip = m.group(1)
            cidr = hex_netmask_to_cidr(m.group(2))

        m = re.search(r'ether\s+([0-9a-fA-F:]+)', output)
        if m:
            mac = m.group(1)

        m = re.search(r'mtu\s+(\d+)', output)
        if m:
            mtu = int(m.group(1))

        return ip, cidr, mac, mtu

    def _parse_macos_gateway(self, output: str) -> Optional[str]:
        for line in output.strip().split('\n'):
            parts = line.split()
            if len(parts) >= 2 and parts[0] == 'default':
                return parts[1]
        return None

    def _parse_scutil_dns(self, output: str) -> List[str]:
        dns_servers = []
        in_resolver1 = False
        for line in output.strip().split('\n'):
            if 'resolver #1' in line:
                in_resolver1 = True
            elif re.match(r'^resolver\s+#\d+', line):
                in_resolver1 = False
            if in_resolver1:
                m = re.match(r'\s*nameserver\[\d+\]\s*:\s*(\S+)', line)
                if m:
                    dns_servers.append(m.group(1))
        return dns_servers

    def _parse_networksetup_type(self, output: str, target_iface: str) -> str:
        lines = output.strip().split('\n')
        current_port = None
        for line in lines:
            m = re.match(r'Hardware Port:\s*(.+)', line)
            if m:
                current_port = m.group(1).strip()
            m = re.match(r'Device:\s*(\S+)', line)
            if m and m.group(1) == target_iface:
                if current_port:
                    # Normalize known types
                    port_lower = current_port.lower()
                    if 'wi-fi' in port_lower or 'wifi' in port_lower or 'airport' in port_lower:
                        return 'Wi-Fi'
                    elif any(kw in port_lower for kw in ('ethernet', 'thunderbolt', 'lan', 'usb')):
                        return 'Ethernet'
                    return current_port
        return 'Unknown'

    # --- Linux ---

    def _collect_linux(self) -> Optional[ConnectionInfo]:
        has_ip = self._detector.check_command('ip')
        has_ifconfig = self._detector.check_command('ifconfig')

        if has_ip:
            return self._collect_linux_iproute2()
        elif has_ifconfig:
            return self._collect_linux_nettools()
        else:
            self._errors.append("Neither 'ip' nor 'ifconfig' found on Linux")
            return None

    def _collect_linux_iproute2(self) -> Optional[ConnectionInfo]:
        # Get default route
        route_out = self._run_cmd(['ip', 'route', 'show', 'default'])
        if not route_out:
            return None
        gateway, iface = self._parse_linux_ip_route(route_out)
        if not iface:
            self._errors.append("Could not determine default interface from ip route")
            return None

        # Get IP info
        addr_out = self._run_cmd(['ip', 'addr', 'show', iface])
        if not addr_out:
            return None
        ip, cidr, mac, mtu = self._parse_linux_ip_addr(addr_out, iface)

        # DNS
        dns = self._read_resolv_conf()

        # Interface type
        itype = self._detect_linux_interface_type(iface)

        isp = self._try_isp_lookup(dns)

        return ConnectionInfo(
            interface=iface, type=itype, ip=ip or '',
            cidr=cidr, gateway=gateway or '', dns=dns,
            isp=isp, mac=mac, mtu=mtu,
        )

    def _collect_linux_nettools(self) -> Optional[ConnectionInfo]:
        # Get default route
        route_out = self._run_cmd(['route', '-n'])
        if not route_out:
            return None
        gateway, iface = self._parse_linux_route_n(route_out)
        if not iface:
            self._errors.append("Could not determine default interface from route -n")
            return None

        ifconfig_out = self._run_cmd(['ifconfig', iface])
        if not ifconfig_out:
            return None
        ip, cidr, mac, mtu = self._parse_linux_ifconfig(ifconfig_out, iface)

        dns = self._read_resolv_conf()
        itype = self._detect_linux_interface_type(iface)
        isp = self._try_isp_lookup(dns)

        return ConnectionInfo(
            interface=iface, type=itype, ip=ip or '',
            cidr=cidr, gateway=gateway or '', dns=dns,
            isp=isp, mac=mac, mtu=mtu,
        )

    def _parse_linux_ip_addr(self, output: str, iface: str) -> Tuple[Optional[str], Optional[int], Optional[str], Optional[int]]:
        ip = cidr = mac = mtu = None

        m = re.search(r'mtu\s+(\d+)', output)
        if m:
            mtu = int(m.group(1))

        m = re.search(r'link/ether\s+([0-9a-fA-F:]+)', output)
        if m:
            mac = m.group(1)

        m = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)/(\d+)', output)
        if m:
            ip = m.group(1)
            cidr = int(m.group(2))

        return ip, cidr, mac, mtu

    def _parse_linux_ifconfig(self, output: str, iface: str) -> Tuple[Optional[str], Optional[int], Optional[str], Optional[int]]:
        ip = cidr = mac = mtu = None

        m = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)', output)
        if m:
            ip = m.group(1)

        m = re.search(r'netmask\s+(\d+\.\d+\.\d+\.\d+)', output)
        if m:
            cidr = dotted_netmask_to_cidr(m.group(1))

        m = re.search(r'ether\s+([0-9a-fA-F:]+)', output)
        if m:
            mac = m.group(1)

        m = re.search(r'mtu\s+(\d+)', output)
        if m:
            mtu = int(m.group(1))

        return ip, cidr, mac, mtu

    def _parse_linux_ip_route(self, output: str) -> Tuple[Optional[str], Optional[str]]:
        m = re.search(r'default\s+via\s+(\S+)\s+dev\s+(\S+)', output)
        if m:
            return m.group(1), m.group(2)
        return None, None

    def _parse_linux_route_n(self, output: str) -> Tuple[Optional[str], Optional[str]]:
        for line in output.strip().split('\n'):
            parts = line.split()
            if len(parts) >= 8 and parts[0] == '0.0.0.0':
                return parts[1], parts[7]
        return None, None

    def _parse_resolv_conf(self, content: str) -> List[str]:
        dns_servers = []
        for line in content.strip().split('\n'):
            line = line.strip()
            if line.startswith('#'):
                continue
            m = re.match(r'nameserver\s+(\S+)', line)
            if m:
                dns_servers.append(m.group(1))
        return dns_servers

    def _read_resolv_conf(self) -> List[str]:
        try:
            with open('/etc/resolv.conf', 'r') as f:
                return self._parse_resolv_conf(f.read())
        except (IOError, OSError):
            return []

    def _detect_linux_interface_type(self, iface: str) -> str:
        try:
            wireless_path = f'/sys/class/net/{iface}/wireless'
            import os
            if os.path.exists(wireless_path):
                return 'Wi-Fi'
            type_path = f'/sys/class/net/{iface}/type'
            if os.path.exists(type_path):
                with open(type_path) as f:
                    if f.read().strip() == '1':
                        return 'Ethernet'
        except (IOError, OSError):
            pass
        return 'Unknown'

    def _try_isp_lookup(self, dns: List[str]) -> Optional[str]:
        """Try reverse DNS lookup on first DNS server to guess ISP."""
        if not dns:
            return None
        try:
            hostname, _, _ = socket.gethostbyaddr(dns[0])
            return hostname
        except (socket.herror, socket.gaierror, OSError):
            return None

    def _run_cmd(self, cmd: List[str]) -> Optional[str]:
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=self.TIMEOUT
            )
            return result.stdout
        except subprocess.TimeoutExpired:
            self._errors.append(f"Timeout running: {' '.join(cmd)}")
            return None
        except (OSError, subprocess.SubprocessError) as e:
            self._errors.append(f"Error running {' '.join(cmd)}: {e}")
            return None


# =============================================================================
# Ping Tester
# =============================================================================

class PingTester:
    """Execute ping tests against multiple targets."""

    DEFAULT_TARGETS = [
        ('gateway', 'Gateway'),
        ('8.8.8.8', 'Google DNS'),
        ('1.1.1.1', 'Cloudflare DNS'),
    ]

    def __init__(self, gateway: Optional[str] = None, custom_targets: Optional[List[Tuple[str, str]]] = None,
                 count: int = 10):
        self._gateway = gateway
        self._custom_targets = custom_targets or []
        self._count = count
        self._errors: List[str] = []

    def run(self) -> List[PingResult]:
        results = []
        targets = []

        # Build target list
        for host, name in self.DEFAULT_TARGETS:
            if host == 'gateway':
                if self._gateway:
                    targets.append((self._gateway, name))
            else:
                targets.append((host, name))

        targets.extend(self._custom_targets)

        for host, name in targets:
            result = self._run_ping(host, name, self._count)
            if result:
                results.append(result)

        return results

    def _run_ping(self, target: str, name: str, count: int) -> Optional[PingResult]:
        timeout = count * 2 + 10
        try:
            result = subprocess.run(
                ['ping', '-c', str(count), target],
                capture_output=True, text=True, timeout=timeout
            )
            output = result.stdout + result.stderr
            return self._parse_ping_output(output, target, name, count)
        except subprocess.TimeoutExpired:
            self._errors.append(f"Ping timeout for {name} ({target})")
            return None
        except (OSError, subprocess.SubprocessError) as e:
            self._errors.append(f"Ping error for {name} ({target}): {e}")
            return None

    def _parse_ping_output(self, output: str, target: str, name: str, count: int) -> Optional[PingResult]:
        # Parse packet loss
        loss_match = re.search(r'(\d+(?:\.\d+)?)%\s*packet\s*loss', output)
        packet_loss = float(loss_match.group(1)) if loss_match else 0.0

        # Parse RTT stats
        # macOS: round-trip min/avg/max/stddev = 3.987/4.389/5.012/0.365 ms
        # Linux: rtt min/avg/max/mdev = 3.980/4.386/5.010/0.365 ms
        rtt_match = re.search(
            r'(?:round-trip|rtt)\s+min/avg/max/(?:std|m)dev\s*=\s*'
            r'([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)\s*ms',
            output
        )

        if rtt_match:
            return PingResult(
                target=target, target_name=name,
                min_ms=float(rtt_match.group(1)),
                avg_ms=float(rtt_match.group(2)),
                max_ms=float(rtt_match.group(3)),
                stddev_ms=float(rtt_match.group(4)),
                packet_loss_pct=packet_loss,
                count=count,
            )
        else:
            # 100% packet loss - no RTT stats
            return PingResult(
                target=target, target_name=name,
                avg_ms=None, min_ms=None, max_ms=None, stddev_ms=None,
                packet_loss_pct=packet_loss,
                count=count,
            )


# =============================================================================
# HTTP Timing Tester
# =============================================================================

class HttpTimingTester:
    """Measure HTTP connection timing using curl."""

    TIMEOUT = 15  # seconds
    DEFAULT_URLS = [
        'https://www.google.com',
        'https://www.cloudflare.com',
    ]

    CURL_FORMAT = (
        '     time_namelookup:  %{time_namelookup}\\n'
        '        time_connect:  %{time_connect}\\n'
        '     time_appconnect:  %{time_appconnect}\\n'
        '    time_pretransfer:  %{time_pretransfer}\\n'
        '       time_redirect:  %{time_redirect}\\n'
        '  time_starttransfer:  %{time_starttransfer}\\n'
        '                     ----------\\n'
        '          time_total:  %{time_total}\\n'
        '      http_code: %{http_code}\\n'
        '   size_download: %{size_download}\\n'
    )

    def __init__(self, urls: Optional[List[str]] = None):
        self._urls = urls or self.DEFAULT_URLS
        self._errors: List[str] = []

    def run(self) -> List[HttpTiming]:
        results = []
        for url in self._urls:
            result = self._run_http_timing(url)
            if result:
                results.append(result)
        return results

    def _run_http_timing(self, url: str) -> Optional[HttpTiming]:
        try:
            result = subprocess.run(
                ['curl', '-s', '-o', '/dev/null', '-w', self.CURL_FORMAT, url],
                capture_output=True, text=True, timeout=self.TIMEOUT
            )
            return self._parse_curl_output(result.stdout, url)
        except subprocess.TimeoutExpired:
            self._errors.append(f"HTTP timing timeout for {url}")
            return None
        except (OSError, subprocess.SubprocessError) as e:
            self._errors.append(f"HTTP timing error for {url}: {e}")
            return None

    def _parse_curl_output(self, output: str, url: str) -> Optional[HttpTiming]:
        values = {}
        for line in output.strip().split('\n'):
            line = line.strip()
            if line.startswith('-') or not line:
                continue
            m = re.match(r'(\w+):\s+([\d.]+)', line)
            if m:
                values[m.group(1)] = m.group(2)

        try:
            dns = float(values.get('time_namelookup', 0))
            connect = float(values.get('time_connect', 0))
            appconnect = float(values.get('time_appconnect', 0))
            starttransfer = float(values.get('time_starttransfer', 0))
            total = float(values.get('time_total', 0))
            http_code = int(values.get('http_code', 0))
            size = int(float(values.get('size_download', 0)))

            return HttpTiming(
                url=url,
                dns_ms=dns * 1000,
                tcp_ms=(connect - dns) * 1000,
                tls_ms=(appconnect - connect) * 1000,
                ttfb_ms=starttransfer * 1000,
                total_ms=total * 1000,
                http_code=http_code,
                size_bytes=size,
            )
        except (ValueError, KeyError) as e:
            self._errors.append(f"Failed to parse curl output for {url}: {e}")
            return None


# =============================================================================
# Speed Tester
# =============================================================================

class SpeedTester:
    """Measure download speed using curl against multiple CDN endpoints."""

    TEST_URLS = [
        ("https://speed.cloudflare.com/__down?bytes=10000000", "Cloudflare (Anycast)"),
        ("https://proof.ovh.net/files/10Mb.dat", "OVH (US/EU)"),
        ("https://ash-speed.hetzner.com/10MB.bin", "Hetzner (US-East)"),
    ]
    TIMEOUT = 30  # seconds per test

    def __init__(self):
        self._errors: List[str] = []

    def run(self) -> List[DownloadSpeed]:
        results = []
        for url, label in self.TEST_URLS:
            result = self._run_speed_test(url, label, self.TIMEOUT)
            if result:
                results.append(result)
        return results

    def _run_speed_test(self, url: str, label: str, timeout: int) -> Optional[DownloadSpeed]:
        try:
            start = datetime.now()
            result = subprocess.run(
                ['curl', '-s', '-o', '/dev/null', '-w',
                 '%{size_download} %{time_total} %{speed_download}', url],
                capture_output=True, text=True, timeout=timeout
            )
            duration = (datetime.now() - start).total_seconds()
            return self._parse_speed_output(result.stdout, url, label, duration)
        except subprocess.TimeoutExpired:
            self._errors.append(f"Speed test timeout for {label} ({url})")
            return None
        except (OSError, subprocess.SubprocessError) as e:
            self._errors.append(f"Speed test error for {label}: {e}")
            return None

    def _parse_speed_output(self, output: str, url: str, label: str,
                            duration: float) -> Optional[DownloadSpeed]:
        try:
            parts = output.strip().split()
            if len(parts) >= 3:
                size_bytes = int(float(parts[0]))
                time_total = float(parts[1])
                speed_bytes_sec = float(parts[2])
                speed_mbps = (speed_bytes_sec * 8) / 1_000_000
                return DownloadSpeed(
                    url=url, label=label,
                    speed_mbps=speed_mbps,
                    size_bytes=size_bytes,
                    duration_sec=time_total,
                )
        except (ValueError, IndexError) as e:
            self._errors.append(f"Failed to parse speed output for {label}: {e}")
        return None


# =============================================================================
# Traceroute Tester
# =============================================================================

class TracerouteTester:
    """Execute traceroute and parse output."""

    TIMEOUT = 60  # seconds

    DEFAULT_TARGETS = [
        ('8.8.8.8', 'Google DNS'),
    ]

    def __init__(self, custom_targets: Optional[List[Tuple[str, str]]] = None):
        self._custom_targets = custom_targets or []
        self._errors: List[str] = []

    def run(self) -> List[TracerouteResult]:
        results = []
        targets = list(self.DEFAULT_TARGETS) + self._custom_targets
        for host, name in targets:
            result = self._run_traceroute(host, name)
            if result:
                results.append(result)
        return results

    def _run_traceroute(self, target: str, name: str) -> Optional[TracerouteResult]:
        try:
            result = subprocess.run(
                ['traceroute', target],
                capture_output=True, text=True, timeout=self.TIMEOUT
            )
            return self._parse_traceroute_output(result.stdout, target, name)
        except subprocess.TimeoutExpired:
            self._errors.append(f"Traceroute timeout for {name} ({target})")
            return None
        except (OSError, subprocess.SubprocessError) as e:
            self._errors.append(f"Traceroute error for {name} ({target}): {e}")
            return None

    def _parse_traceroute_output(self, output: str, target: str, name: str) -> Optional[TracerouteResult]:
        hops = []
        for line in output.strip().split('\n'):
            line = line.strip()
            # Skip header line
            if line.startswith('traceroute'):
                continue

            # Match hop number at start
            m = re.match(r'\s*(\d+)\s+(.+)', line)
            if not m:
                continue

            hop_num = int(m.group(1))
            rest = m.group(2).strip()

            # Check for timeout (* * *)
            if re.match(r'^\*\s+\*\s+\*$', rest):
                hops.append(TracerouteHop(
                    hop_number=hop_num, hostname=None, ip=None,
                    rtt_ms=None, is_timeout=True,
                ))
                continue

            # Parse hostname/IP and RTT
            # Format: hostname (ip)  rtt1 ms  rtt2 ms  rtt3 ms
            # or: ip (ip)  rtt1 ms  rtt2 ms  rtt3 ms
            hop_match = re.match(
                r'(\S+)\s+\((\d+\.\d+\.\d+\.\d+)\)\s+([\d.]+)\s*ms',
                rest
            )
            if hop_match:
                hostname = hop_match.group(1)
                ip = hop_match.group(2)
                rtt = float(hop_match.group(3))
                hops.append(TracerouteHop(
                    hop_number=hop_num, hostname=hostname, ip=ip,
                    rtt_ms=rtt, is_timeout=False,
                ))
            else:
                # Try IP-only format
                ip_match = re.match(r'(\d+\.\d+\.\d+\.\d+)\s+([\d.]+)\s*ms', rest)
                if ip_match:
                    hops.append(TracerouteHop(
                        hop_number=hop_num, hostname=None, ip=ip_match.group(1),
                        rtt_ms=float(ip_match.group(2)), is_timeout=False,
                    ))

        return TracerouteResult(
            target=target, target_name=name,
            hops=hops, total_hops=len(hops),
        )


# =============================================================================
# Main Orchestrator
# =============================================================================

class NetworkDiagnostics:
    """Orchestrate all network diagnostic tests."""

    def __init__(self, skip_traceroute: bool = False, skip_speed: bool = False,
                 ping_count: int = 10, custom_targets: Optional[List[Tuple[str, str]]] = None):
        self._skip_traceroute = skip_traceroute
        self._skip_speed = skip_speed
        self._ping_count = ping_count
        self._custom_targets = custom_targets or []
        self._detector = PlatformDetector()
        self._errors: List[str] = []
        self._skipped_tests: List[str] = []

    def run(self) -> DiagnosticsResult:
        # Check required commands
        if not self._detector.check_command('ping'):
            self._errors.append("Required command 'ping' not found")
        if not self._detector.check_command('curl'):
            self._errors.append("Required command 'curl' not found")

        # Check optional commands
        if not self._skip_traceroute and not self._detector.check_command('traceroute'):
            self._skipped_tests.append("traceroute: command not found (install with: apt install traceroute / brew install traceroute)")
            self._skip_traceroute = True

        # Collect connection info
        conn_collector = ConnectionCollector(self._detector)
        connection = conn_collector.collect()
        self._errors.extend(conn_collector._errors)

        gateway = connection.gateway if connection else None

        # Ping tests
        ping_tester = PingTester(
            gateway=gateway, custom_targets=self._custom_targets,
            count=self._ping_count,
        )
        ping_results = ping_tester.run()
        self._errors.extend(ping_tester._errors)

        # HTTP timing
        http_tester = HttpTimingTester()
        http_results = http_tester.run()
        self._errors.extend(http_tester._errors)

        # Speed tests
        if self._skip_speed:
            self._skipped_tests.append("speed: skipped by user request")
            download_results = []
        else:
            speed_tester = SpeedTester()
            download_results = speed_tester.run()
            self._errors.extend(speed_tester._errors)

        # Traceroute
        if self._skip_traceroute:
            traceroute_results = []
        else:
            trace_tester = TracerouteTester(custom_targets=self._custom_targets)
            traceroute_results = trace_tester.run()
            self._errors.extend(trace_tester._errors)

        return DiagnosticsResult(
            timestamp=datetime.now(timezone.utc).isoformat(),
            platform=f"{self._detector.system()} {platform.release()}",
            connection=connection,
            ping=ping_results,
            http=http_results,
            download=download_results,
            traceroute=traceroute_results,
            errors=self._errors,
            skipped_tests=self._skipped_tests,
        )


# =============================================================================
# CLI Interface
# =============================================================================

def parse_target(target_str: str) -> Tuple[str, str]:
    """Parse target string in format 'host,label'."""
    parts = target_str.split(',', 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return parts[0].strip(), parts[0].strip()


def main():
    parser = argparse.ArgumentParser(
        description='Network Diagnostics - Comprehensive network quality assessment'
    )
    parser.add_argument('-o', '--output', help='Output file path (default: stdout)')
    parser.add_argument('-t', '--target', action='append', default=[],
                        help='Custom target in format host,label (repeatable)')
    parser.add_argument('--skip-traceroute', action='store_true',
                        help='Skip traceroute tests')
    parser.add_argument('--skip-speed', action='store_true',
                        help='Skip download speed tests')
    parser.add_argument('--ping-count', type=int, default=10,
                        help='Number of ping packets (default: 10)')

    args = parser.parse_args()

    custom_targets = [parse_target(t) for t in args.target]

    diag = NetworkDiagnostics(
        skip_traceroute=args.skip_traceroute,
        skip_speed=args.skip_speed,
        ping_count=args.ping_count,
        custom_targets=custom_targets,
    )

    print("Running network diagnostics...", file=sys.stderr)
    result = diag.run()
    output = json.dumps(result.to_dict(), indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
