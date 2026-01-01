# PCI DSS Gap Analysis Template

Framework for conducting gap analysis against PCI DSS 4.0.1 requirements.

## Gap Analysis Overview

### Purpose
Identify discrepancies between current security posture and PCI DSS 4.0.1 requirements to create a remediation roadmap.

### Scope Definition

Before conducting gap analysis, clearly define:

| Element | Description |
|---------|-------------|
| **CDE Boundary** | Systems storing, processing, or transmitting CHD |
| **Connected Systems** | Systems connected to CDE |
| **Security-Impacting** | Systems that could impact CDE security |
| **Out of Scope** | Systems with no connectivity to CDE |

---

## Scoping Worksheet

### Cardholder Data Flows

Document all CHD flows through your environment:

| Flow ID | Entry Point | Systems Touched | Storage Location | Exit Point | Data Elements |
|---------|-------------|-----------------|------------------|------------|---------------|
| F001 | | | | | |
| F002 | | | | | |
| F003 | | | | | |

### System Inventory

| System Name | Function | In CDE? | Connected? | Stores CHD? | Owner |
|-------------|----------|---------|------------|-------------|-------|
| | | | | | |
| | | | | | |
| | | | | | |

### Network Segmentation Assessment

| Segment | Purpose | CDE Connection | Controls |
|---------|---------|----------------|----------|
| | | | |
| | | | |

---

## Gap Analysis Template

### Requirement 1: Network Security Controls

| Sub-Req | Description | Current State | Gap Identified | Severity | Remediation |
|---------|-------------|---------------|----------------|----------|-------------|
| 1.1.1 | NSC roles defined | | | | |
| 1.2.1 | NSC rules restrict CDE | | | | |
| 1.2.5 | Services/ports documented | | | | |
| 1.2.8 | Anti-spoofing measures | | | | |
| 1.3.1 | Inbound traffic restricted | | | | |
| 1.3.2 | Outbound traffic restricted | | | | |
| 1.4.1 | NSC between wireless and CDE | | | | |
| 1.5.1 | Mobile device security | | | | |

**Current State Options**: Compliant | Partial | Non-Compliant | N/A
**Severity**: Critical | High | Medium | Low

---

### Requirement 2: Secure Configurations

| Sub-Req | Description | Current State | Gap Identified | Severity | Remediation |
|---------|-------------|---------------|----------------|----------|-------------|
| 2.1.1 | Config standards defined | | | | |
| 2.2.1 | Config standards applied | | | | |
| 2.2.2 | Vendor defaults changed | | | | |
| 2.2.4 | Only necessary services | | | | |
| 2.2.5 | Insecure services secured | | | | |
| 2.2.6 | Security parameters set | | | | |
| 2.2.7 | Admin access encrypted | | | | |
| 2.3.1 | Wireless defaults changed | | | | |

---

### Requirement 3: Protect Stored Account Data

| Sub-Req | Description | Current State | Gap Identified | Severity | Remediation |
|---------|-------------|---------------|----------------|----------|-------------|
| 3.1.1 | Data retention policy | | | | |
| 3.2.1 | SAD not stored | | | | |
| 3.3.1 | PAN masked in display | | | | |
| 3.3.2 | PAN masked in logs | | | | |
| 3.4.1 | PAN unreadable | | | | |
| 3.5.1 | Keys protected | | | | |
| 3.6.1 | Key management procedures | | | | |
| 3.7.1 | Key rotation | | | | |

**March 2025**:
| 3.3.3 | SAD not in logs | | | | |
| 3.4.2 | Technical DLP for PAN | | | | |
| 3.5.1.1 | Keyed hashes | | | | |
| 3.5.1.2 | Disk encryption limits | | | | |

---

### Requirement 4: Protect CHD in Transit

| Sub-Req | Description | Current State | Gap Identified | Severity | Remediation |
|---------|-------------|---------------|----------------|----------|-------------|
| 4.1.1 | Secure transmission process | | | | |
| 4.2.1 | Strong cryptography | | | | |
| 4.2.1.1 | Trusted certificates | | | | |
| 4.2.1.2 | Certificate validation | | | | |
| 4.2.2 | PAN in messaging secured | | | | |

---

### Requirement 5: Malware Protection

| Sub-Req | Description | Current State | Gap Identified | Severity | Remediation |
|---------|-------------|---------------|----------------|----------|-------------|
| 5.1.1 | Malware protection process | | | | |
| 5.2.1 | Anti-malware deployed | | | | |
| 5.2.2 | Commonly affected systems | | | | |
| 5.2.3 | Risk evaluation for others | | | | |
| 5.3.1 | Anti-malware current | | | | |
| 5.3.2 | Periodic scans | | | | |
| 5.3.4 | Audit logging | | | | |
| 5.3.5 | Cannot be disabled | | | | |

**March 2025**:
| 5.3.3 | Removable media scans | | | | |
| 5.4.1 | Anti-phishing | | | | |

---

### Requirement 6: Secure Development

| Sub-Req | Description | Current State | Gap Identified | Severity | Remediation |
|---------|-------------|---------------|----------------|----------|-------------|
| 6.1.1 | Secure development process | | | | |
| 6.2.1 | Bespoke software secure | | | | |
| 6.2.2 | Developer training | | | | |
| 6.2.3 | Code review | | | | |
| 6.2.4 | Vulnerabilities addressed | | | | |
| 6.3.1 | Vulnerability identification | | | | |
| 6.3.3 | Critical patches | | | | |
| 6.4.1 | Web app protection | | | | |
| 6.5.1 | Change control | | | | |
| 6.5.5 | No live PAN in test | | | | |

**March 2025**:
| 6.3.2 | Software inventory | | | | |
| 6.4.2 | WAF required | | | | |
| 6.4.3 | Payment page scripts | | | | |

---

### Requirement 7: Restrict Access

| Sub-Req | Description | Current State | Gap Identified | Severity | Remediation |
|---------|-------------|---------------|----------------|----------|-------------|
| 7.1.1 | Access control process | | | | |
| 7.2.1 | Access system defined | | | | |
| 7.2.2 | Access by job function | | | | |
| 7.2.3 | Default deny | | | | |
| 7.2.4 | Least privileges | | | | |
| 7.2.5 | Need-to-know | | | | |
| 7.2.5.1 | Access reviews | | | | |
| 7.2.6 | App/system accounts | | | | |

---

### Requirement 8: Identify and Authenticate

| Sub-Req | Description | Current State | Gap Identified | Severity | Remediation |
|---------|-------------|---------------|----------------|----------|-------------|
| 8.1.1 | ID/auth process | | | | |
| 8.2.1 | Unique IDs | | | | |
| 8.2.2 | No shared accounts | | | | |
| 8.2.3 | Service accounts | | | | |
| 8.2.4 | User lifecycle | | | | |
| 8.2.5 | Terminated users | | | | |
| 8.2.6 | Inactive accounts | | | | |
| 8.3.4 | Lockout | | | | |
| 8.3.5 | Password requirements | | | | |
| 8.3.7 | Password history | | | | |
| 8.3.9 | Password age | | | | |
| 8.3.10 | MFA for CDE | | | | |
| 8.4.1 | MFA for admin | | | | |
| 8.4.3 | MFA for remote | | | | |

**March 2025**:
| 8.3.6 | 12-char passwords | | | | |
| 8.4.2 | MFA all CDE access | | | | |
| 8.5.1 | MFA properly implemented | | | | |
| 8.6.1 | Service account login | | | | |
| 8.6.2 | Service account passwords | | | | |
| 8.6.3 | No hard-coded passwords | | | | |

---

### Requirement 9: Physical Security

| Sub-Req | Description | Current State | Gap Identified | Severity | Remediation |
|---------|-------------|---------------|----------------|----------|-------------|
| 9.1.1 | Physical security process | | | | |
| 9.2.1 | Physical access controls | | | | |
| 9.2.3 | Network jack access | | | | |
| 9.2.4 | Wireless AP access | | | | |
| 9.3.1 | Personnel identification | | | | |
| 9.3.2 | Visitor management | | | | |
| 9.3.4 | Visitor log | | | | |
| 9.4.1 | Media secured | | | | |
| 9.4.5 | Media inventory | | | | |
| 9.4.6 | Media destroyed | | | | |
| 9.5.1 | POI protected | | | | |
| 9.5.1.1 | POI list | | | | |
| 9.5.1.2 | POI inspection | | | | |

---

### Requirement 10: Logging and Monitoring

| Sub-Req | Description | Current State | Gap Identified | Severity | Remediation |
|---------|-------------|---------------|----------------|----------|-------------|
| 10.1.1 | Logging process | | | | |
| 10.2.1 | Audit logs enabled | | | | |
| 10.2.2 | Logs include details | | | | |
| 10.3.1 | Log read access | | | | |
| 10.3.2 | Logs protected | | | | |
| 10.3.3 | Logs backed up | | | | |
| 10.3.4 | FIM on logs | | | | |
| 10.4.1 | Daily log review | | | | |
| 10.4.3 | Exceptions followed up | | | | |
| 10.5.1 | 12-month retention | | | | |
| 10.6.1 | Time sync | | | | |
| 10.7.1 | Alert response | | | | |

**March 2025**:
| 10.4.1.1 | Automated log review | | | | |
| 10.4.2.1 | Review frequency analysis | | | | |
| 10.7.2 | Security control failures | | | | |
| 10.7.3 | Failure response | | | | |

---

### Requirement 11: Security Testing

| Sub-Req | Description | Current State | Gap Identified | Severity | Remediation |
|---------|-------------|---------------|----------------|----------|-------------|
| 11.1.1 | Testing process | | | | |
| 11.2.1 | Wireless AP detection | | | | |
| 11.3.1 | Internal vuln scans | | | | |
| 11.3.2 | External ASV scans | | | | |
| 11.4.1 | Penetration testing | | | | |
| 11.4.4 | Segmentation testing | | | | |
| 11.5.1 | IDS/IPS | | | | |
| 11.5.2 | Change detection | | | | |

**March 2025**:
| 11.3.1.1 | Authenticated scans | | | | |
| 11.3.1.2 | Qualified scanner | | | | |
| 11.4.7 | SP pentest 6 months | | | | |
| 11.5.1.1 | IDS/IPS current | | | | |
| 11.6.1 | Payment page tampering | | | | |

---

### Requirement 12: Policies and Programs

| Sub-Req | Description | Current State | Gap Identified | Severity | Remediation |
|---------|-------------|---------------|----------------|----------|-------------|
| 12.1.1 | Security policy | | | | |
| 12.1.2 | Annual policy review | | | | |
| 12.1.3 | Roles defined | | | | |
| 12.1.4 | Executive responsibility | | | | |
| 12.2.1 | Acceptable use policy | | | | |
| 12.5.1 | Scope documented | | | | |
| 12.5.2 | Scope confirmed annually | | | | |
| 12.6.1 | Awareness program | | | | |
| 12.6.2 | Training | | | | |
| 12.6.3 | Acknowledgments | | | | |
| 12.7.1 | Personnel screening | | | | |
| 12.8.1 | SP documented | | | | |
| 12.8.2 | SP agreements | | | | |
| 12.8.4 | SP monitoring | | | | |
| 12.10.1 | IRP | | | | |
| 12.10.2 | IRP reviewed | | | | |
| 12.10.4 | IR training | | | | |

**March 2025**:
| 12.3.1 | Targeted risk analysis | | | | |
| 12.3.2 | Risk analysis approach | | | | |
| 12.5.2.1 | Scope on change | | | | |
| 12.6.2 | Training annually | | | | |
| 12.6.3.1 | Threat awareness | | | | |
| 12.6.3.2 | Acceptable use training | | | | |

---

## Gap Summary

### By Severity

| Severity | Count | Requirements Affected |
|----------|-------|----------------------|
| Critical | | |
| High | | |
| Medium | | |
| Low | | |

### By Requirement

| Requirement | Compliant | Partial | Non-Compliant | N/A |
|-------------|-----------|---------|---------------|-----|
| 1. Network Security | | | | |
| 2. Secure Config | | | | |
| 3. Stored Data | | | | |
| 4. Transmission | | | | |
| 5. Malware | | | | |
| 6. Development | | | | |
| 7. Access Control | | | | |
| 8. Authentication | | | | |
| 9. Physical | | | | |
| 10. Logging | | | | |
| 11. Testing | | | | |
| 12. Policies | | | | |

### March 2025 Readiness

| Status | Count |
|--------|-------|
| Ready Now | |
| In Progress | |
| Not Started | |
| At Risk | |

---

## Remediation Priority Matrix

| Priority | Criteria | Target Timeline |
|----------|----------|-----------------|
| **P1 - Critical** | Current requirement, high risk | Immediate |
| **P2 - High** | March 2025 requirement, complex | 60-90 days |
| **P3 - Medium** | Current requirement, moderate risk | 90-180 days |
| **P4 - Low** | Best practice improvement | Next cycle |

---

## Next Steps

1. [ ] Validate scope boundaries with stakeholders
2. [ ] Complete gap analysis for all requirements
3. [ ] Calculate compliance percentage
4. [ ] Prioritize gaps by severity and deadline
5. [ ] Create remediation plan with owners
6. [ ] Schedule follow-up assessments
7. [ ] Report to executive leadership
