# PCI DSS Evidence Collection Guide

Detailed guide for collecting and organizing evidence for each PCI DSS requirement.

## Evidence Collection Principles

### Golden Rules

1. **Date stamps matter**: Evidence should be dated within the assessment period
2. **Screenshots beat descriptions**: Visual evidence is preferred
3. **Show, don't tell**: Demonstrate controls are active, not just configured
4. **Consistency is key**: Evidence should align across documents
5. **Samples suffice**: Representative samples acceptable per QSA guidance

### Evidence Types

| Type | Description | Examples |
|------|-------------|----------|
| Configuration | System/application settings | Firewall rules, server configs |
| Process | Documented procedures | Change management tickets |
| Logs | System-generated records | Audit logs, scan reports |
| Documentation | Policies and standards | Security policy, standards |
| Interview | Verbal confirmation | Not standalone evidence |
| Observation | Direct visual verification | Data center walkthrough |

---

## Requirement 1: Network Security Controls

### 1.1 Processes and Procedures

| Evidence | Description | Source |
|----------|-------------|--------|
| NSC management procedures | Documented process for managing firewalls | Policy repository |
| Change control records | Sample firewall change tickets | ITSM system |
| Configuration standards | NSC configuration baseline | Standards library |

### 1.2 Network Security Control Configuration

| Evidence | Description | Source |
|----------|-------------|--------|
| Firewall rule base export | Full rule set with comments | Firewall management |
| Rule review records | Documentation of rule reviews | Security team |
| Business justification | Justification for each rule | Change tickets |
| Network diagram | Current network topology | Architecture |
| Data flow diagram | CHD flows through network | Architecture |

**Sample Evidence Format**:
```
Rule Review Record - [Date]
Rule ID: FW-001
Source: 10.0.0.0/8
Destination: Payment Gateway
Port: 443
Protocol: TCP
Justification: Required for payment processing
Last Reviewed: [Date]
Reviewed By: [Name]
```

### 1.3 Inbound/Outbound Restrictions

| Evidence | Description | Source |
|----------|-------------|--------|
| Inbound rules to CDE | Filtered rule export | Firewall |
| Outbound rules from CDE | Filtered rule export | Firewall |
| Default deny configuration | Screenshot of default rule | Firewall |
| DMZ architecture | DMZ configuration documentation | Network team |

### 1.4-1.5 Wireless and Mobile

| Evidence | Description | Source |
|----------|-------------|--------|
| Wireless network diagram | Showing isolation from CDE | Network team |
| Wireless configuration | AP settings, encryption | Wireless controller |
| Mobile device policy | MDM/MAM configuration | MDM solution |

---

## Requirement 2: Secure Configurations

### 2.1-2.2 Configuration Standards

| Evidence | Description | Source |
|----------|-------------|--------|
| Hardening standards | CIS benchmark or equivalent | Standards library |
| Configuration compliance report | Scan showing compliance | Vulnerability scanner |
| Default account inventory | List of changed defaults | Security team |
| Service inventory | Enabled services per system | Configuration management |

**Sample Evidence - Configuration Compliance**:
```
Server: PAYSVR01
Benchmark: CIS Windows Server 2019 L1
Compliance Score: 98%
Non-Compliant Items: 2 (documented exceptions)
Scan Date: [Date]
```

### 2.3 Wireless Security

| Evidence | Description | Source |
|----------|-------------|--------|
| Wireless encryption config | WPA2/WPA3 settings | Wireless controller |
| Default credential changes | Evidence of SSID/password changes | Network team |

---

## Requirement 3: Protect Stored Account Data

### 3.1 Data Retention

| Evidence | Description | Source |
|----------|-------------|--------|
| Data retention policy | Policy document | Compliance |
| Retention schedule | Table of data types and periods | Compliance |
| Purge evidence | Logs showing data deletion | Database/application |

### 3.2 Sensitive Authentication Data

| Evidence | Description | Source |
|----------|-------------|--------|
| Database schema | Showing no SAD storage | DBA |
| Application code review | Verification no SAD logged | Development |
| Log samples | Showing no SAD in logs | Log management |

### 3.3-3.4 PAN Protection

| Evidence | Description | Source |
|----------|-------------|--------|
| PAN masking screenshots | UI showing masked PAN | Application |
| Encryption configuration | Encryption settings | Database/storage |
| Encryption algorithm | AES-256 or equivalent | Security team |
| Tokenization evidence | Token vault configuration | Tokenization vendor |

**Sample Evidence - PAN Masking**:
```
Application: Customer Portal
Screen: Account Summary
PAN Display: ****-****-****-1234
Date Captured: [Date]
```

### 3.5-3.7 Key Management

| Evidence | Description | Source |
|----------|-------------|--------|
| Key management procedures | Documented process | Security team |
| Key inventory | List of cryptographic keys | Key management system |
| Key rotation records | Evidence of key changes | Key management |
| Split knowledge evidence | Dual control procedures | Security team |
| Key custodian list | Personnel with key access | Security team |

---

## Requirement 4: Transmission Encryption

### 4.1-4.2 Strong Cryptography

| Evidence | Description | Source |
|----------|-------------|--------|
| TLS configuration | Server cipher suites | Web servers |
| SSL scan results | External TLS scan | SSL Labs or equivalent |
| Certificate inventory | All certificates with expiry | Certificate management |
| Protocol scan | Showing TLS 1.2+ only | Security scanner |

**Sample Evidence - TLS Configuration**:
```
Server: www.example.com
Protocol: TLS 1.2, TLS 1.3
Cipher Suites:
- TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
- TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
SSL Labs Grade: A
Scan Date: [Date]
```

---

## Requirement 5: Malware Protection

### 5.1-5.3 Anti-Malware Deployment

| Evidence | Description | Source |
|----------|-------------|--------|
| AV deployment report | Installed systems list | AV console |
| Definition status | Current definitions | AV console |
| Scan schedule | Periodic scan configuration | AV console |
| Tamper protection | Cannot be disabled | AV console |

**Sample Evidence Format**:
```
Antivirus Status Report - [Date]
Total CDE Systems: 50
AV Installed: 50 (100%)
Current Definitions: 48 (96%)
Last Full Scan: [Date]
Real-Time Protection: Enabled
```

### 5.4 Anti-Phishing

| Evidence | Description | Source |
|----------|-------------|--------|
| Email security config | Anti-phishing settings | Email gateway |
| Phishing simulation results | Test campaign results | Security awareness |

---

## Requirement 6: Secure Development

### 6.1-6.2 Secure SDLC

| Evidence | Description | Source |
|----------|-------------|--------|
| SDLC documentation | Secure development process | Development |
| Secure coding standards | Developer guidelines | Development |
| Training records | Developer security training | Training system |
| Code review records | Sample code reviews | Version control |

### 6.3 Vulnerability Management

| Evidence | Description | Source |
|----------|-------------|--------|
| Vulnerability sources | How vulnerabilities tracked | Security team |
| Software inventory | Components with versions | CMDB |
| Patch records | Critical patch timeline | Patch management |

### 6.4 Web Application Protection

| Evidence | Description | Source |
|----------|-------------|--------|
| WAF configuration | Rule sets, learning mode | WAF console |
| WAF logs | Sample blocked attacks | WAF logs |
| Payment page scripts | Script inventory | Development |

### 6.5 Change Management

| Evidence | Description | Source |
|----------|-------------|--------|
| Change policy | Change control process | ITSM |
| Change tickets | Sample changes with approval | ITSM system |
| Test records | Pre-production testing | QA team |
| Separation of duties | Developer access vs. production | Access management |

---

## Requirement 7: Access Control

### 7.1-7.3 Need-to-Know Access

| Evidence | Description | Source |
|----------|-------------|--------|
| Access control policy | Documented policy | Compliance |
| Role definitions | Roles and permissions | IAM system |
| Access matrix | Who has access to what | Security team |
| Access review records | Periodic access reviews | IAM system |
| Default deny evidence | Configuration showing deny-by-default | Systems |

**Sample Evidence - Access Matrix**:
```
| Role | Application | CDE Access | PAN Access |
|------|------------|------------|------------|
| Payment Operator | Payment App | Yes | Masked |
| DBA | Database | Yes | Encrypted |
| Help Desk | Support Portal | No | No |
```

---

## Requirement 8: Authentication

### 8.1-8.3 User Identification

| Evidence | Description | Source |
|----------|-------------|--------|
| Account inventory | All user accounts | IAM system |
| No shared accounts | Evidence of unique IDs | IAM system |
| Service account list | Non-interactive accounts | IAM system |
| Password policy config | Technical enforcement | IAM/AD |
| MFA configuration | Multi-factor settings | MFA system |

**Sample Evidence - Password Policy**:
```
Password Policy Configuration - Active Directory
Minimum Length: 12 characters
Complexity: Enabled (upper, lower, number, special)
History: 4 passwords remembered
Maximum Age: 90 days
Lockout Threshold: 10 attempts
Lockout Duration: 30 minutes
```

### 8.4-8.5 MFA Implementation

| Evidence | Description | Source |
|----------|-------------|--------|
| MFA architecture | How MFA is implemented | Security team |
| MFA enrollment | Users with MFA enabled | MFA system |
| Independence proof | Factors are separate | Technical documentation |

---

## Requirement 9: Physical Security

### 9.1-9.4 Physical Access Controls

| Evidence | Description | Source |
|----------|-------------|--------|
| Physical access policy | Documented procedures | Facilities |
| Badge access reports | CDE access logs | Badge system |
| Visitor logs | Sample visitor records | Reception |
| Camera coverage | CCTV placement diagram | Security |
| Media inventory | Electronic media list | IT Operations |
| Media destruction records | Destruction certificates | IT Operations |

### 9.5 POI Device Security

| Evidence | Description | Source |
|----------|-------------|--------|
| POI device inventory | All terminals with serials | IT Operations |
| Inspection records | Tamper inspection logs | Store operations |
| Training records | Staff tamper awareness | Training |

**Sample Evidence - POI Inventory**:
```
| Device ID | Make/Model | Serial | Location | Last Inspected |
|-----------|------------|--------|----------|----------------|
| POS-001 | Ingenico iSC250 | 12345 | Store 1 | [Date] |
| POS-002 | Verifone VX520 | 67890 | Store 2 | [Date] |
```

---

## Requirement 10: Logging and Monitoring

### 10.1-10.3 Audit Logs

| Evidence | Description | Source |
|----------|-------------|--------|
| Logging configuration | Log settings per system | System configs |
| Log format samples | Sample logs showing fields | Log management |
| Log access controls | Who can access logs | Access management |
| Log integrity | FIM on log files | FIM solution |

**Required Log Fields**:
```
Sample Log Entry:
Timestamp: 2024-01-15T14:23:45.123Z
User ID: jsmith
Event Type: Login Success
Source IP: 192.168.1.100
Destination: PAYSVR01
Result: Success
```

### 10.4-10.5 Log Review and Retention

| Evidence | Description | Source |
|----------|-------------|--------|
| Log review procedures | How logs are reviewed | Security team |
| SIEM dashboard | Automated review evidence | SIEM |
| Alert samples | Security alert examples | SIEM |
| Retention configuration | 12 month retention | Log management |

### 10.6-10.7 Time Synchronization and Alerting

| Evidence | Description | Source |
|----------|-------------|--------|
| NTP configuration | Time sync settings | System configs |
| Time source architecture | NTP hierarchy | Network team |
| Alert configuration | What triggers alerts | SIEM |
| Alert response records | How alerts handled | Incident management |

---

## Requirement 11: Security Testing

### 11.1-11.2 Wireless Detection

| Evidence | Description | Source |
|----------|-------------|--------|
| Wireless scan reports | Quarterly scan results | Security team |
| Rogue AP procedures | How rogues are handled | Security team |
| AP inventory | Authorized wireless APs | Network team |

### 11.3 Vulnerability Scanning

| Evidence | Description | Source |
|----------|-------------|--------|
| Internal scan reports | Quarterly internal scans | Security team |
| ASV scan reports | Quarterly external scans | ASV |
| Remediation evidence | How vulnerabilities fixed | Vulnerability management |

**Sample Evidence - Scan Summary**:
```
Internal Vulnerability Scan - Q4 2024
Scan Date: [Date]
Systems Scanned: 50
Critical: 0
High: 2 (remediated)
Medium: 15
Low: 45
Authenticated: Yes
```

### 11.4 Penetration Testing

| Evidence | Description | Source |
|----------|-------------|--------|
| Penetration test report | Full test results | Testing vendor |
| Scope documentation | What was tested | Testing vendor |
| Remediation evidence | How findings addressed | Security team |
| Segmentation test | If segmentation used | Testing vendor |

### 11.5-11.6 IDS/IPS and Change Detection

| Evidence | Description | Source |
|----------|-------------|--------|
| IDS/IPS configuration | System settings | Network security |
| Alert samples | Sample detections | IDS/IPS |
| FIM configuration | Change detection settings | FIM solution |
| Change alerts | Sample change detections | FIM solution |

---

## Requirement 12: Policies and Programs

### 12.1-12.5 Security Policies

| Evidence | Description | Source |
|----------|-------------|--------|
| Information security policy | Master policy | Compliance |
| Policy review records | Annual review evidence | Compliance |
| Responsibility assignment | CISO/security team roles | HR/Compliance |
| Scope documentation | PCI DSS scope definition | Compliance |

### 12.6 Security Awareness

| Evidence | Description | Source |
|----------|-------------|--------|
| Training program | Awareness program description | Training |
| Completion records | Who completed training | LMS |
| Acknowledgment forms | Policy acknowledgments | HR |

### 12.8 Vendor Management

| Evidence | Description | Source |
|----------|-------------|--------|
| Vendor inventory | Service providers list | Procurement |
| Vendor agreements | Contracts with security terms | Legal |
| Vendor AOCs | Third-party compliance docs | Vendor files |
| Monitoring records | Vendor compliance reviews | Compliance |

### 12.10 Incident Response

| Evidence | Description | Source |
|----------|-------------|--------|
| Incident response plan | IRP document | Security team |
| IRP test records | Annual test/exercise | Security team |
| Contact list | IR team contacts | Security team |
| Incident logs | Sample incident records | Incident management |

---

## Evidence Collection Tips

### Do's

- Collect evidence throughout the year, not just before audit
- Use consistent naming conventions
- Include date stamps on all evidence
- Cross-reference evidence to requirements
- Keep evidence organized by requirement

### Don'ts

- Don't fabricate or backdate evidence
- Don't provide more than asked
- Don't include sensitive data unnecessarily
- Don't assume QSA will accept verbal confirmations
- Don't wait until last minute to collect evidence

### Sample Naming Convention

```
[Req#]-[SubReq]-[Description]-[Date].[ext]

Examples:
01.2-Firewall-RuleExport-2024-01-15.xlsx
08.3-MFA-Configuration-2024-01-15.png
11.3-ASV-ScanReport-Q4-2024.pdf
```
