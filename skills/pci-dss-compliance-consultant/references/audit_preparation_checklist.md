# PCI DSS Audit Preparation Checklist

Comprehensive checklist for preparing for QSA on-site assessment.

## Pre-Audit Timeline

### 12 Weeks Before Audit

- [ ] Confirm audit dates with QSA
- [ ] Complete internal gap analysis
- [ ] Identify key stakeholders for each requirement
- [ ] Begin remediation of critical gaps
- [ ] Review previous ROC findings (if applicable)

### 8 Weeks Before Audit

- [ ] Begin evidence collection
- [ ] Conduct internal vulnerability scans
- [ ] Schedule ASV external scans
- [ ] Review and update policies and procedures
- [ ] Prepare network diagrams

### 4 Weeks Before Audit

- [ ] Complete evidence organization
- [ ] Conduct internal readiness review
- [ ] Identify interview subjects by topic
- [ ] Schedule penetration testing (if annual test due)
- [ ] Verify all technical controls are functioning

### 2 Weeks Before Audit

- [ ] Final documentation review
- [ ] Conduct tabletop audit simulation
- [ ] Prepare executive summary of compliance status
- [ ] Confirm logistics (meeting rooms, access badges)
- [ ] Brief interview subjects on expectations

### 1 Week Before Audit

- [ ] Final evidence verification
- [ ] Prepare evidence binders/folders
- [ ] Confirm system access for QSA
- [ ] Prepare project contact list
- [ ] Send welcome packet to QSA

---

## Documentation Requirements

### Required Policies

| Policy | Owner | Last Review | Status |
|--------|-------|-------------|--------|
| Information Security Policy | CISO | | [ ] Ready |
| Acceptable Use Policy | IT Director | | [ ] Ready |
| Access Control Policy | Security Team | | [ ] Ready |
| Password/Authentication Policy | Security Team | | [ ] Ready |
| Remote Access Policy | IT Director | | [ ] Ready |
| Network Security Policy | Network Team | | [ ] Ready |
| Encryption/Key Management Policy | Security Team | | [ ] Ready |
| Data Retention/Disposal Policy | Compliance | | [ ] Ready |
| Incident Response Plan | Security Team | | [ ] Ready |
| Vendor Management Policy | Procurement | | [ ] Ready |
| Change Management Policy | IT Director | | [ ] Ready |
| Physical Security Policy | Facilities | | [ ] Ready |
| Wireless Security Policy | Network Team | | [ ] Ready |
| Media Handling Policy | IT Operations | | [ ] Ready |

### Required Procedures

| Procedure | Owner | Status |
|-----------|-------|--------|
| User Provisioning/De-provisioning | IT Operations | [ ] Ready |
| Firewall Rule Change Process | Network Team | [ ] Ready |
| Patch Management Process | IT Operations | [ ] Ready |
| Vulnerability Management Process | Security Team | [ ] Ready |
| Log Review Process | Security Team | [ ] Ready |
| Incident Response Procedures | Security Team | [ ] Ready |
| Backup and Recovery Procedures | IT Operations | [ ] Ready |
| Key Management Procedures | Security Team | [ ] Ready |
| Visitor Management Procedures | Facilities | [ ] Ready |
| Media Destruction Procedures | IT Operations | [ ] Ready |

### Network Documentation

| Document | Owner | Status |
|----------|-------|--------|
| Network Diagram (current) | Network Team | [ ] Ready |
| Data Flow Diagram | Architecture | [ ] Ready |
| Asset Inventory | IT Operations | [ ] Ready |
| CDE Scope Documentation | Compliance | [ ] Ready |
| Firewall Rule Documentation | Network Team | [ ] Ready |
| VLAN Configuration | Network Team | [ ] Ready |
| Wireless AP Inventory | Network Team | [ ] Ready |

---

## Evidence Organization

### Folder Structure (Recommended)

```
PCI_DSS_Audit_Evidence/
├── 01_Network_Security_Controls/
│   ├── Firewall_Configurations/
│   ├── Network_Diagrams/
│   ├── Rule_Review_Records/
│   └── Segmentation_Testing/
├── 02_Secure_Configurations/
│   ├── Hardening_Standards/
│   ├── Configuration_Baselines/
│   └── Default_Account_Changes/
├── 03_Stored_Data_Protection/
│   ├── Encryption_Evidence/
│   ├── Key_Management/
│   ├── Data_Retention/
│   └── Masking_Screenshots/
├── 04_Transmission_Encryption/
│   ├── TLS_Configurations/
│   ├── Certificate_Inventory/
│   └── Protocol_Scans/
├── 05_Malware_Protection/
│   ├── Antivirus_Deployment/
│   ├── Update_Logs/
│   └── Scan_Results/
├── 06_Secure_Development/
│   ├── SDLC_Documentation/
│   ├── Code_Reviews/
│   ├── Vulnerability_Management/
│   └── WAF_Configuration/
├── 07_Access_Control/
│   ├── Access_Matrix/
│   ├── Role_Definitions/
│   └── Access_Reviews/
├── 08_Authentication/
│   ├── Password_Policy/
│   ├── MFA_Configuration/
│   └── Account_Inventory/
├── 09_Physical_Security/
│   ├── Badge_Access_Reports/
│   ├── Visitor_Logs/
│   ├── CCTV_Evidence/
│   └── POI_Inventory/
├── 10_Logging_Monitoring/
│   ├── Log_Configurations/
│   ├── SIEM_Reports/
│   ├── Log_Review_Records/
│   └── Alert_Samples/
├── 11_Security_Testing/
│   ├── Vulnerability_Scans/
│   ├── Penetration_Tests/
│   ├── Wireless_Scans/
│   └── Segmentation_Tests/
├── 12_Policies_Programs/
│   ├── Policies/
│   ├── Training_Records/
│   ├── Risk_Assessments/
│   └── Vendor_Management/
└── Supporting_Documents/
    ├── Previous_ROC/
    ├── ASV_Reports/
    └── Third_Party_AOCs/
```

---

## Interview Preparation

### Interview Subject Matrix

| Topic | Primary SME | Backup | QSA Requirements |
|-------|-------------|--------|------------------|
| Executive Responsibility | CISO/CIO | CEO | Req 12.1, 12.4 |
| Network Architecture | Network Architect | Network Engineer | Req 1 |
| Firewall Management | Firewall Admin | Network Team | Req 1.2, 1.3 |
| System Hardening | System Admin | IT Operations | Req 2 |
| Encryption/Key Management | Security Engineer | CISO | Req 3, 4 |
| Anti-Malware | Security Operations | System Admin | Req 5 |
| Software Development | Development Lead | QA Lead | Req 6 |
| Access Control | Identity Management | HR | Req 7, 8 |
| Physical Security | Facilities Manager | Security Guard Supervisor | Req 9 |
| Logging/Monitoring | SOC Analyst | Security Engineer | Req 10 |
| Vulnerability Management | Security Engineer | IT Operations | Req 11 |
| Incident Response | Incident Manager | SOC Lead | Req 12.10 |
| Security Awareness | Training Coordinator | HR | Req 12.6 |
| Vendor Management | Procurement | Legal | Req 12.8 |

### Interview Best Practices

**Before the Interview:**
- Review relevant requirements
- Prepare specific evidence locations
- Know your processes, not just documentation

**During the Interview:**
- Answer only what is asked
- Refer to documentation when needed
- Say "I don't know, but I can find out" if uncertain
- Take notes on follow-up items

**Common Interview Questions:**
1. "Walk me through how a user gets access to CDE systems"
2. "What happens when a firewall rule change is needed?"
3. "How do you handle a suspected security incident?"
4. "Show me your most recent vulnerability scan and how you addressed findings"
5. "How do you ensure patches are applied within required timeframes?"

---

## Technical Verification Checklist

### Network Controls (Requirement 1)

- [ ] Firewall configurations reviewed within last 6 months
- [ ] NSC rules documented with business justification
- [ ] Deny-by-default rules in place
- [ ] Segmentation testing completed (if applicable)
- [ ] Wireless networks isolated from CDE

### System Configuration (Requirement 2)

- [ ] All vendor default passwords changed
- [ ] CIS benchmarks or equivalent applied
- [ ] Only necessary services running
- [ ] SNMP community strings changed
- [ ] Administrative access encrypted

### Data Protection (Requirements 3, 4)

- [ ] PAN storage locations identified
- [ ] Encryption verified for stored PAN
- [ ] Key management procedures documented
- [ ] TLS 1.2+ for all transmissions
- [ ] Certificate validity verified

### Anti-Malware (Requirement 5)

- [ ] Anti-malware on all applicable systems
- [ ] Definitions current (within 1 day)
- [ ] Real-time scanning enabled
- [ ] Periodic scans configured
- [ ] Cannot be disabled by users

### Access Controls (Requirements 7, 8)

- [ ] Unique IDs for all users
- [ ] Access based on need-to-know
- [ ] MFA for CDE access and remote access
- [ ] Password policy enforced (12 chars, complexity)
- [ ] Inactive accounts disabled
- [ ] Terminated user accounts removed

### Logging (Requirement 10)

- [ ] Audit logging enabled on all CDE systems
- [ ] Logs include required details
- [ ] Log retention meets 12 months online, 12 months total
- [ ] Logs reviewed daily
- [ ] FIM on log files

### Testing (Requirement 11)

- [ ] Internal vulnerability scans quarterly (authenticated)
- [ ] External ASV scans quarterly (passing)
- [ ] Penetration testing annual
- [ ] Wireless scans quarterly
- [ ] IDS/IPS functioning

---

## Common Audit Findings to Avoid

### High-Risk Areas

| Finding | Prevention |
|---------|------------|
| Incomplete scope documentation | Document all systems and data flows |
| Missing or outdated policies | Annual policy review with signatures |
| Inadequate evidence of log review | Automated alerting plus documented review |
| Password policy gaps | Technical enforcement, not just policy |
| Incomplete vulnerability remediation | Track and verify all remediations |
| Missing third-party AOCs | Maintain vendor compliance calendar |
| Untested incident response | Annual tabletop exercise minimum |
| Segmentation failures | Regular penetration testing of boundaries |

### Quick Wins Before Audit

1. Update all network diagrams
2. Complete user access review
3. Verify all default passwords changed
4. Run and review vulnerability scans
5. Test incident response procedures
6. Collect all third-party compliance documentation
7. Verify security awareness training completion
8. Review firewall rule justifications

---

## QSA Interaction Guidelines

### What QSAs Will Do

- Review documentation
- Interview personnel
- Observe processes
- Inspect configurations
- Sample evidence
- Test controls

### QSA Access Requirements

| Access Type | Preparation |
|-------------|-------------|
| Physical | Badge access to CDE, data centers |
| Network | View-only access to firewalls, servers |
| Systems | Screenshots or live demos |
| Documentation | Organized evidence folders |
| Personnel | Interview schedule with SMEs |

### Handling Findings

1. **During audit**: Clarify, don't argue
2. **After identification**: Understand the gap
3. **Response**: Provide additional evidence or accept finding
4. **Remediation**: Document timeline and actions
5. **Follow-up**: Provide evidence of remediation

---

## Post-Audit Activities

### If Full Compliance (ROC)
- [ ] Review ROC for accuracy
- [ ] Sign Attestation of Compliance (AOC)
- [ ] Submit to acquiring bank/payment brand
- [ ] Plan for next year's assessment
- [ ] Address any observations (not findings)

### If Gaps Identified
- [ ] Create remediation plan with timelines
- [ ] Prioritize by risk and deadline
- [ ] Assign owners to each finding
- [ ] Schedule follow-up validation with QSA
- [ ] Document lessons learned
