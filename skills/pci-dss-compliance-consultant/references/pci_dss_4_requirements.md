# PCI DSS 4.0.1 Requirements Guide

Comprehensive reference for all 12 PCI DSS requirements with implementation guidance.

## Requirement Structure

Each requirement follows this hierarchy:
- **Requirement** (1-12): Principal security objective
- **Sub-requirement** (X.Y): Specific control area
- **Defined approach** (X.Y.Z): Detailed requirement
- **Customized approach objective**: Alternative compliance path

## Requirement 1: Install and Maintain Network Security Controls

**Objective**: Protect cardholder data by controlling network traffic and connections.

### Key Sub-requirements

| Req | Description | Evidence Required |
|-----|-------------|-------------------|
| 1.1.1 | Formal processes for NSC management | Documented procedures |
| 1.2.1 | NSC rules restrict CDE traffic | Configuration files, rule bases |
| 1.2.5 | Services, protocols, ports documented | Network diagrams, inventory |
| 1.2.8 | Anti-spoofing measures | NSC configurations |
| 1.3.1 | Inbound traffic restricted to CDE | Firewall rules |
| 1.3.2 | Outbound traffic from CDE limited | Firewall rules |
| 1.4.1 | NSCs between wireless and CDE | Network diagrams |
| 1.4.2 | Deny-by-default for wireless | Configuration evidence |
| 1.5.1 | Security controls on mobile devices | MDM policies |

### March 2025 Mandatory Items
- **1.2.8**: Anti-spoofing controls (becomes mandatory)

### Implementation Examples

```
# Example firewall rule structure
# Inbound to CDE - deny all except:
ALLOW TCP 443 from authorized IPs to web servers
ALLOW TCP 22 from bastion to CDE (management)
DENY ALL to CDE (default)

# Outbound from CDE - deny all except:
ALLOW TCP 443 to payment processor
ALLOW TCP 53 to internal DNS
DENY ALL from CDE (default)
```

---

## Requirement 2: Apply Secure Configurations

**Objective**: Ensure system components are configured securely by removing defaults and hardening.

### Key Sub-requirements

| Req | Description | Evidence Required |
|-----|-------------|-------------------|
| 2.1.1 | Configuration standards documented | Hardening standards |
| 2.2.1 | Configuration standards for all components | CIS benchmarks, vendor guides |
| 2.2.2 | Vendor default accounts changed/disabled | Account inventory |
| 2.2.4 | Only necessary services enabled | Service inventory |
| 2.2.5 | Insecure services secured | Configuration evidence |
| 2.2.6 | System security parameters configured | Parameter settings |
| 2.2.7 | Non-console admin access encrypted | Access method documentation |
| 2.3.1 | Wireless defaults changed | Wireless configuration |

### Implementation Checklist

- [ ] Default passwords changed on all systems
- [ ] Unnecessary services disabled
- [ ] CIS benchmarks applied
- [ ] Administrative access encrypted (SSH, TLS)
- [ ] Wireless encryption (WPA3 or WPA2-Enterprise)
- [ ] SNMP community strings changed

---

## Requirement 3: Protect Stored Account Data

**Objective**: Minimize data storage and protect any data that must be stored.

### Key Sub-requirements

| Req | Description | Evidence Required |
|-----|-------------|-------------------|
| 3.1.1 | Data retention policies | Policy documents |
| 3.2.1 | SAD not stored post-authorization | Database schemas, code review |
| 3.3.1 | PAN masked when displayed | Application screenshots |
| 3.3.2 | PAN masked in logs | Log samples |
| 3.4.1 | PAN unreadable when stored | Encryption evidence |
| 3.5.1 | Cryptographic keys protected | Key management procedures |
| 3.6.1 | Key management procedures | Documentation |
| 3.7.1 | Key rotation procedures | Rotation evidence |

### March 2025 Mandatory Items
- **3.3.3**: SAD cannot be stored in logs
- **3.4.2**: Technical controls prevent PAN copy/relocation
- **3.5.1.1**: Hashes use keyed cryptographic hashes
- **3.5.1.2**: Disk-level encryption only for removable media

### Data Storage Rules

| Data Element | Storage Allowed | Protection Required |
|--------------|-----------------|---------------------|
| PAN | Yes | Render unreadable |
| Cardholder Name | Yes | Best practice to protect |
| Expiration Date | Yes | Best practice to protect |
| Service Code | Yes | Best practice to protect |
| Full Track Data | **NO** | N/A |
| CVV/CVC | **NO** | N/A |
| PIN/PIN Block | **NO** | N/A |

### Acceptable PAN Protection Methods
1. One-way hashes (keyed cryptographic hash)
2. Truncation (first 6 + last 4 max)
3. Index tokens/pads
4. Strong cryptography with key management

---

## Requirement 4: Protect Cardholder Data During Transmission

**Objective**: Encrypt CHD over open, public networks.

### Key Sub-requirements

| Req | Description | Evidence Required |
|-----|-------------|-------------------|
| 4.1.1 | Processes for secure transmission | Policy documents |
| 4.2.1 | Strong cryptography for transmission | TLS configuration |
| 4.2.1.1 | Trusted certificates used | Certificate inventory |
| 4.2.1.2 | Certificate validity verified | Configuration evidence |
| 4.2.2 | PAN secured in end-user messaging | Secure messaging solution |

### Minimum Cryptography Standards

| Protocol | Minimum Version | Notes |
|----------|-----------------|-------|
| TLS | 1.2 | TLS 1.3 recommended |
| SSH | 2.0 | Required |
| IPSec | Current | For VPNs |

### March 2025 Mandatory Items
- **4.2.1**: Security certificates valid and not expired
- **4.2.1.1**: Inventory of trusted keys and certificates

---

## Requirement 5: Protect Systems from Malicious Software

**Objective**: Protect systems from malware using anti-malware solutions.

### Key Sub-requirements

| Req | Description | Evidence Required |
|-----|-------------|-------------------|
| 5.1.1 | Processes for malware protection | Policy documents |
| 5.2.1 | Anti-malware deployed | Deployment evidence |
| 5.2.2 | Anti-malware on commonly affected systems | Installation records |
| 5.2.3 | Systems not at risk have evaluation | Risk assessment |
| 5.3.1 | Anti-malware kept current | Update logs |
| 5.3.2 | Periodic scans performed | Scan logs |
| 5.3.3 | Removable media scanned | Configuration evidence |
| 5.3.4 | Audit logging enabled | Log samples |
| 5.3.5 | Anti-malware cannot be disabled by users | Configuration evidence |
| 5.4.1 | Anti-phishing mechanisms | Email security configuration |

### March 2025 Mandatory Items
- **5.2.3.1**: Risk evaluation for systems not commonly affected
- **5.3.2.1**: Targeted risk analysis for scan frequency
- **5.3.3**: Anti-malware on removable media
- **5.4.1**: Anti-phishing protection for personnel

---

## Requirement 6: Develop and Maintain Secure Systems and Software

**Objective**: Ensure security in software development and maintain secure systems.

### Key Sub-requirements

| Req | Description | Evidence Required |
|-----|-------------|-------------------|
| 6.1.1 | Processes for secure development | SDLC documentation |
| 6.2.1 | Bespoke software developed securely | Secure coding standards |
| 6.2.2 | Security training for developers | Training records |
| 6.2.3 | Code reviewed prior to production | Code review records |
| 6.2.4 | Vulnerabilities addressed before release | Remediation evidence |
| 6.3.1 | Security vulnerabilities identified | Vulnerability sources |
| 6.3.2 | Software inventory maintained | Component inventory |
| 6.3.3 | Critical patches within one month | Patch records |
| 6.4.1 | Public web apps protected | WAF deployment |
| 6.4.2 | Technical solution for web apps | WAF configuration |
| 6.4.3 | Payment page scripts managed | Script inventory |
| 6.5.1 | Change control processes | Change records |
| 6.5.2 | Significant changes documented | Change documentation |
| 6.5.3 | Pre-production testing | Test records |
| 6.5.4 | Roles and functions separated | Access matrix |
| 6.5.5 | Live PANs not in test environments | Environment controls |
| 6.5.6 | Test data removed before production | Verification evidence |

### March 2025 Mandatory Items
- **6.3.2**: Software inventory with version information
- **6.4.2**: WAF required for public-facing web apps
- **6.4.3**: Payment page scripts authorized and integrity verified

### OWASP Top 10 Coverage Required
1. Injection
2. Broken Authentication
3. Sensitive Data Exposure
4. XML External Entities (XXE)
5. Broken Access Control
6. Security Misconfiguration
7. Cross-Site Scripting (XSS)
8. Insecure Deserialization
9. Known Vulnerabilities
10. Insufficient Logging

---

## Requirement 7: Restrict Access to System Components and Cardholder Data

**Objective**: Limit access to cardholder data to only those with business need.

### Key Sub-requirements

| Req | Description | Evidence Required |
|-----|-------------|-------------------|
| 7.1.1 | Processes for access control | Policy documents |
| 7.2.1 | Access control system defined | Access control documentation |
| 7.2.2 | Access based on job function | Role definitions |
| 7.2.3 | Default deny for all | Configuration evidence |
| 7.2.4 | Access limited to least privileges | Access matrix |
| 7.2.5 | Access based on need-to-know | Access approvals |
| 7.2.5.1 | Access reviews performed | Review records |
| 7.2.6 | Application/system accounts managed | Account inventory |
| 7.3.1 | Access control system configured | System configuration |
| 7.3.2 | Access control system denies by default | Configuration evidence |
| 7.3.3 | Access control system reviewed | Review logs |

### Access Control Implementation

```
Role-Based Access Control (RBAC) Example:

Role: Payment Processor Operator
- Access: Payment processing application
- PAN Access: Masked view only
- Database: No direct access
- Network: CDE segment only

Role: Database Administrator
- Access: Database management tools
- PAN Access: Encrypted fields only
- Database: Read/Write (no PAN decryption)
- Network: CDE segment only
```

---

## Requirement 8: Identify Users and Authenticate Access

**Objective**: Ensure proper user identification and authentication to system components.

### Key Sub-requirements

| Req | Description | Evidence Required |
|-----|-------------|-------------------|
| 8.1.1 | Processes for identification/authentication | Policy documents |
| 8.2.1 | Unique IDs for all users | Account inventory |
| 8.2.2 | Group/shared IDs not used | Account review |
| 8.2.3 | Service accounts managed | Service account inventory |
| 8.2.4 | User lifecycle management | User administration records |
| 8.2.5 | Terminated users removed promptly | Termination records |
| 8.2.6 | Inactive accounts disabled | Account status report |
| 8.2.7 | Third-party access managed | Third-party agreements |
| 8.2.8 | Usage policies for third-party | Policy documents |
| 8.3.1 | Strong authentication for users | Authentication configuration |
| 8.3.2 | Strong authentication for non-console | Configuration evidence |
| 8.3.4 | Invalid authentication attempts limited | Lockout configuration |
| 8.3.5 | Passwords/passphrases meet requirements | Password policy |
| 8.3.6 | Minimum 12 characters for passwords | Policy configuration |
| 8.3.7 | Passwords cannot equal previous 4 | Configuration evidence |
| 8.3.8 | Authentication policies documented | Policy documents |
| 8.3.9 | Passwords changed at least every 90 days | Password history |
| 8.3.10 | MFA for CDE access | MFA configuration |
| 8.3.10.1 | MFA factors are independent | MFA architecture |
| 8.3.11 | Physical token or biometric required | MFA implementation |
| 8.4.1 | MFA for non-console admin access | Configuration evidence |
| 8.4.2 | MFA for all CDE access | MFA deployment |
| 8.4.3 | MFA for remote network access | VPN configuration |
| 8.5.1 | MFA implemented correctly | Technical review |
| 8.6.1 | System/app accounts managed | Account procedures |
| 8.6.2 | Passwords for system accounts managed | Password storage |
| 8.6.3 | Service account passwords protected | Access controls |

### March 2025 Mandatory Items
- **8.3.6**: Minimum 12-character passwords
- **8.4.2**: MFA for ALL access into CDE
- **8.5.1**: MFA systems properly configured
- **8.6.1**: Interactive login for service accounts managed
- **8.6.2**: Passwords for app/system accounts managed
- **8.6.3**: Service account passwords not hard-coded

### Password/Authentication Requirements

| Parameter | Requirement |
|-----------|-------------|
| Minimum Length | 12 characters (March 2025) |
| Complexity | Numeric AND alphabetic |
| History | Cannot reuse last 4 |
| Maximum Age | 90 days (if no dynamic analysis) |
| Lockout | After not more than 10 attempts |
| Lockout Duration | 30 minutes minimum |
| Idle Timeout | 15 minutes for sessions |

---

## Requirement 9: Restrict Physical Access to Cardholder Data

**Objective**: Physical security controls to protect CDE and cardholder data.

### Key Sub-requirements

| Req | Description | Evidence Required |
|-----|-------------|-------------------|
| 9.1.1 | Physical security processes defined | Policy documents |
| 9.2.1 | Physical access controls for CDE | Access control configuration |
| 9.2.2 | Physical access restricted | Physical security measures |
| 9.2.3 | Physical access to network jacks | Physical controls |
| 9.2.4 | Physical access to wireless APs | Physical controls |
| 9.3.1 | Procedures for distinguishing personnel | Badge procedures |
| 9.3.2 | Procedures for visitor management | Visitor logs |
| 9.3.3 | Visitor badges expire | Badge procedures |
| 9.3.4 | Visitor log maintained | Visitor logs |
| 9.4.1 | Media physically secured | Physical controls |
| 9.4.2 | Media classification | Classification labels |
| 9.4.3 | Secure media transport | Transport procedures |
| 9.4.4 | Management approval for media moves | Approval records |
| 9.4.5 | Inventory of electronic media | Media inventory |
| 9.4.6 | Media destroyed when unneeded | Destruction records |
| 9.4.7 | Electronic media destroyed | Destruction certificates |
| 9.5.1 | POI devices protected | Device inventory |
| 9.5.1.1 | POI device list maintained | Device list |
| 9.5.1.2 | POI devices inspected | Inspection records |
| 9.5.1.3 | Training on POI tampering | Training records |

### March 2025 Mandatory Items
- **9.5.1.2.1**: POI device inspection frequency based on risk analysis

---

## Requirement 10: Log and Monitor All Access

**Objective**: Track and monitor all access to network resources and cardholder data.

### Key Sub-requirements

| Req | Description | Evidence Required |
|-----|-------------|-------------------|
| 10.1.1 | Logging processes defined | Policy documents |
| 10.2.1 | Audit logs enabled | Logging configuration |
| 10.2.1.1 | User access logged | Log samples |
| 10.2.1.2 | Actions by admins logged | Log samples |
| 10.2.1.3 | Access to audit logs logged | Log samples |
| 10.2.1.4 | Invalid access attempts logged | Log samples |
| 10.2.1.5 | Changes to credentials logged | Log samples |
| 10.2.1.6 | Initialization of logs logged | Log samples |
| 10.2.1.7 | Security function changes logged | Log samples |
| 10.2.2 | Audit logs include details | Log format review |
| 10.3.1 | Log read access restricted | Access controls |
| 10.3.2 | Log files protected from modification | File permissions |
| 10.3.3 | Log files backed up promptly | Backup procedures |
| 10.3.4 | File integrity monitoring on logs | FIM configuration |
| 10.4.1 | Logs reviewed daily | Review records |
| 10.4.1.1 | Automated mechanisms for review | SIEM configuration |
| 10.4.2 | All other logs reviewed periodically | Review procedures |
| 10.4.2.1 | Periodic review frequency defined | Policy documents |
| 10.4.3 | Exceptions followed up | Exception records |
| 10.5.1 | Audit log retention 12 months | Retention policy |
| 10.6.1 | Time synchronization | NTP configuration |
| 10.6.2 | Time data protected | Time source security |
| 10.6.3 | Time servers from trusted sources | Time architecture |
| 10.7.1 | Security alert response processes | Incident procedures |
| 10.7.2 | Failures detected and responded to | Alert configuration |
| 10.7.3 | Failures responded to promptly | Response records |

### March 2025 Mandatory Items
- **10.4.1.1**: Automated audit log review mechanisms
- **10.4.2.1**: Targeted risk analysis for review frequency
- **10.7.2**: Critical security control failures detected and alerted
- **10.7.3**: Critical security control failures responded to promptly

### Required Log Events

| Event Category | Details Required |
|----------------|------------------|
| User Access | User ID, timestamp, success/fail, resource |
| Admin Actions | User ID, action, timestamp, affected system |
| Log Access | User ID, timestamp, action |
| Auth Failures | Attempted user ID, timestamp, source |
| Security Changes | User ID, change details, before/after |

---

## Requirement 11: Test Security of Systems and Networks Regularly

**Objective**: Regular testing to ensure security controls remain effective.

### Key Sub-requirements

| Req | Description | Evidence Required |
|-----|-------------|-------------------|
| 11.1.1 | Testing processes defined | Policy documents |
| 11.2.1 | Authorized wireless APs detected | Wireless scan reports |
| 11.2.2 | Wireless scan inventory maintained | AP inventory |
| 11.3.1 | Internal vulnerability scans quarterly | Scan reports |
| 11.3.1.1 | Internal scans authenticated | Scanner configuration |
| 11.3.1.2 | Internal scans managed | Scan procedures |
| 11.3.1.3 | Internal vulnerabilities addressed | Remediation records |
| 11.3.2 | External vulnerability scans quarterly | ASV reports |
| 11.3.2.1 | External vulnerabilities addressed | Remediation evidence |
| 11.4.1 | Penetration testing performed | Pentest reports |
| 11.4.2 | Internal penetration testing | Pentest reports |
| 11.4.3 | External penetration testing | Pentest reports |
| 11.4.4 | Segmentation testing | Segmentation test reports |
| 11.4.5 | Penetration testing methodology | Methodology documentation |
| 11.4.6 | Pentest findings addressed | Remediation evidence |
| 11.4.7 | Service provider pentest 6 months | Service provider reports |
| 11.5.1 | Intrusion detection deployed | IDS/IPS configuration |
| 11.5.1.1 | IDS/IPS techniques current | Update logs |
| 11.5.2 | Change detection mechanisms | Change detection config |
| 11.6.1 | Payment page tampering detection | Monitoring configuration |

### March 2025 Mandatory Items
- **11.3.1.1**: Authenticated internal vulnerability scans
- **11.3.1.2**: Internal scans via qualified resource
- **11.4.7**: Service provider pentest every 6 months
- **11.5.1.1**: IDS/IPS keeps up with current threats
- **11.6.1**: Payment page change/tamper detection

### Testing Schedule

| Test Type | Frequency | Notes |
|-----------|-----------|-------|
| Internal Vulnerability Scan | Quarterly + after changes | Authenticated (March 2025) |
| External Vulnerability Scan | Quarterly + after changes | ASV required |
| Internal Penetration Test | Annual + after changes | Qualified tester |
| External Penetration Test | Annual + after changes | Qualified tester |
| Segmentation Test | Annual (bi-annual for SPs) | If segmentation used |
| Wireless Scan | Quarterly | Detect rogue APs |

---

## Requirement 12: Support Information Security with Policies and Programs

**Objective**: Maintain policies supporting security of cardholder data.

### Key Sub-requirements

| Req | Description | Evidence Required |
|-----|-------------|-------------------|
| 12.1.1 | Information security policy | Policy documents |
| 12.1.2 | Policy reviewed annually | Review records |
| 12.1.3 | Security roles defined | Role documentation |
| 12.1.4 | Executive responsibility assigned | Assignment documentation |
| 12.2.1 | Acceptable use policies | Policy documents |
| 12.3.1 | Targeted risk assessments | Risk assessment records |
| 12.3.2 | Targeted risk analysis performed | Analysis documentation |
| 12.3.3 | Cryptographic cipher suites reviewed | Review documentation |
| 12.3.4 | Hardware/software review | Review procedures |
| 12.4.1 | Executive PCI DSS responsibility (SP) | Assignment documentation |
| 12.4.2 | Additional requirements for SP | Compliance documentation |
| 12.5.1 | PCI DSS scope documented | Scope documentation |
| 12.5.2 | PCI DSS scope confirmed annually | Scope review records |
| 12.5.2.1 | Scope documented upon change | Change records |
| 12.5.3 | Scope review includes all elements | Comprehensive scope doc |
| 12.6.1 | Security awareness program | Training program |
| 12.6.2 | Security awareness training | Training records |
| 12.6.3 | Personnel acknowledge policies | Acknowledgment records |
| 12.6.3.1 | Training includes threat awareness | Training content |
| 12.6.3.2 | Training includes acceptable use | Training content |
| 12.7.1 | Personnel screening | Background check records |
| 12.8.1 | Service providers documented | SP list |
| 12.8.2 | Written agreements with SPs | Contracts/agreements |
| 12.8.3 | SP engagement process | Engagement procedures |
| 12.8.4 | SP PCI DSS compliance monitoring | Monitoring records |
| 12.8.5 | SP responsibilities documented | RACI matrix |
| 12.9.1 | SP acknowledge requirements | Written acknowledgments |
| 12.9.2 | SP support customer compliance | Support documentation |
| 12.10.1 | Incident response plan | IRP document |
| 12.10.2 | IRP reviewed annually | Review records |
| 12.10.3 | Specific personnel for IR | Contact list |
| 12.10.4 | IR training | Training records |
| 12.10.4.1 | IR training frequency | Training schedule |
| 12.10.5 | IR monitoring systems | Alert configuration |
| 12.10.6 | IRP evolved from lessons learned | IRP updates |
| 12.10.7 | IR procedures for unexpected PANs | Procedure documentation |

### March 2025 Mandatory Items
- **12.3.1**: Targeted risk analysis performed
- **12.3.2**: Targeted risk analysis approach documented
- **12.5.2.1**: Scope documented upon significant change
- **12.6.2**: Training upon hire and annually
- **12.6.3.1**: Training includes emerging threats
- **12.6.3.2**: Training includes acceptable use requirements

### Required Policies

1. Information Security Policy
2. Acceptable Use Policy
3. Access Control Policy
4. Password Policy
5. Remote Access Policy
6. Network Security Policy
7. Encryption Policy
8. Data Retention Policy
9. Incident Response Plan
10. Vendor Management Policy
11. Change Management Policy
12. Physical Security Policy

---

## Customized Approach

PCI DSS 4.0 introduces the "Customized Approach" as an alternative to defined requirements:

### When to Use Customized Approach
- Innovative technologies not covered by defined approach
- Existing controls that meet intent differently
- Business constraints preventing standard implementation

### Requirements for Customized Approach
1. Document the customized control
2. Perform targeted risk analysis
3. Demonstrate control meets security objective
4. Independent assessor validates effectiveness

### Not Allowed for Customized Approach
- Compensating controls (use existing compensating control process)
- Reducing scope of requirements
- Avoiding fundamental security objectives
