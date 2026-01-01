# SOC 2 to PCI DSS Control Mapping

Mapping between SOC 2 Trust Services Criteria and PCI DSS 4.0.1 requirements for combined audit efficiency.

## Overview

### Frameworks Compared

| Aspect | SOC 2 | PCI DSS |
|--------|-------|---------|
| **Issuing Body** | AICPA | PCI Security Standards Council |
| **Focus** | Service organization controls | Payment card data security |
| **Mandatory** | Voluntary (market-driven) | Required for card processing |
| **Scope** | Customer data broadly | Cardholder data specifically |
| **Assessment** | CPA firm | QSA (Qualified Security Assessor) |
| **Report Type** | SOC 2 Type I/II | ROC (Report on Compliance) |

### Combined Audit Benefits

- **~60% control overlap** between frameworks
- **20-30% time savings** on combined audits
- **Reduced audit fatigue** for personnel
- **Consistent evidence collection**
- **Single source of truth** for overlapping controls

---

## SOC 2 Trust Services Criteria Overview

### Five Categories

| Category | Code | Description |
|----------|------|-------------|
| Security | CC | Controls against unauthorized access |
| Availability | A | System availability for operation |
| Processing Integrity | PI | Complete, valid, accurate processing |
| Confidentiality | C | Protection of confidential information |
| Privacy | P | Collection, use, retention of personal information |

**Note**: Security (CC) is required for all SOC 2 audits. Others are optional based on scope.

---

## Detailed Control Mapping

### CC1: Control Environment

| SOC 2 Criteria | PCI DSS Mapping | Overlap Level |
|----------------|-----------------|---------------|
| CC1.1 - Commitment to integrity | 12.1.1 - Security policy | Partial |
| CC1.2 - Board oversight | 12.4.1 - Executive responsibility | High |
| CC1.3 - Management structure | 12.1.3 - Security roles | High |
| CC1.4 - Competence | 12.6.2 - Training | High |
| CC1.5 - Accountability | 12.1.4 - Responsibility assignment | High |

### CC2: Communication and Information

| SOC 2 Criteria | PCI DSS Mapping | Overlap Level |
|----------------|-----------------|---------------|
| CC2.1 - Information quality | 10.2.2 - Log details | Partial |
| CC2.2 - Internal communication | 12.6 - Security awareness | High |
| CC2.3 - External communication | 12.8.2 - Vendor agreements | Partial |

### CC3: Risk Assessment

| SOC 2 Criteria | PCI DSS Mapping | Overlap Level |
|----------------|-----------------|---------------|
| CC3.1 - Risk objectives | 12.3.1 - Targeted risk analysis | High |
| CC3.2 - Risk identification | 12.3.2 - Risk analysis approach | High |
| CC3.3 - Fraud consideration | 12.10.1 - Incident response | Partial |
| CC3.4 - Change identification | 6.5.1 - Change control | High |

### CC4: Monitoring Activities

| SOC 2 Criteria | PCI DSS Mapping | Overlap Level |
|----------------|-----------------|---------------|
| CC4.1 - Ongoing monitoring | 10.4.1 - Daily log review | High |
| CC4.2 - Deficiency communication | 12.10.6 - IRP lessons learned | Partial |

### CC5: Control Activities

| SOC 2 Criteria | PCI DSS Mapping | Overlap Level |
|----------------|-----------------|---------------|
| CC5.1 - Control selection | 12.1.1 - Security policy | Partial |
| CC5.2 - Technology controls | 1, 2 - Network/configuration | High |
| CC5.3 - Policy deployment | 12.1, 12.2 - Policies | High |

### CC6: Logical and Physical Access

| SOC 2 Criteria | PCI DSS Mapping | Overlap Level |
|----------------|-----------------|---------------|
| CC6.1 - Access control | 7.1, 7.2 - Access restriction | **Full** |
| CC6.2 - Registration/authorization | 8.2.4 - User lifecycle | **Full** |
| CC6.3 - Access removal | 8.2.5 - Terminated users | **Full** |
| CC6.4 - Access restrictions | 7.2.4 - Least privilege | **Full** |
| CC6.5 - Physical access | 9.1, 9.2 - Physical security | **Full** |
| CC6.6 - Transmission protection | 4.2.1 - Strong cryptography | **Full** |
| CC6.7 - Disposal | 9.4.6, 9.4.7 - Media destruction | **Full** |
| CC6.8 - Malware protection | 5 - Malware protection | **Full** |

### CC7: System Operations

| SOC 2 Criteria | PCI DSS Mapping | Overlap Level |
|----------------|-----------------|---------------|
| CC7.1 - Detect anomalies | 11.5.1 - IDS/IPS | High |
| CC7.2 - Monitor components | 10 - Logging | **Full** |
| CC7.3 - Evaluate events | 10.4 - Log review | **Full** |
| CC7.4 - Incident response | 12.10 - IRP | **Full** |
| CC7.5 - Incident recovery | 12.10 - IRP | High |

### CC8: Change Management

| SOC 2 Criteria | PCI DSS Mapping | Overlap Level |
|----------------|-----------------|---------------|
| CC8.1 - Change management | 6.5 - Change control | **Full** |

### CC9: Risk Mitigation

| SOC 2 Criteria | PCI DSS Mapping | Overlap Level |
|----------------|-----------------|---------------|
| CC9.1 - Risk mitigation | Multiple requirements | Partial |
| CC9.2 - Vendor management | 12.8 - Service providers | High |

---

## Mapping by PCI DSS Requirement

### Requirement 1: Network Security Controls

| PCI DSS | SOC 2 Criteria | Notes |
|---------|----------------|-------|
| 1.1 - NSC processes | CC5.2 | Technology controls |
| 1.2 - NSC configuration | CC5.2, CC6.1 | Access, technology |
| 1.3 - CDE restrictions | CC6.1 | Logical access |
| 1.4 - Wireless | CC5.2 | Network security |
| 1.5 - Mobile | CC5.2 | Endpoint security |

### Requirement 2: Secure Configurations

| PCI DSS | SOC 2 Criteria | Notes |
|---------|----------------|-------|
| 2.1 - Config standards | CC5.2 | Technology controls |
| 2.2 - System hardening | CC5.2, CC6.8 | Security controls |
| 2.3 - Wireless config | CC5.2 | Network security |

### Requirement 3: Stored Account Data

| PCI DSS | SOC 2 Criteria | Notes |
|---------|----------------|-------|
| 3.1 - Data retention | CC6.7, C1.2 | Disposal, confidentiality |
| 3.2 - SAD not stored | C1.1 | Confidentiality |
| 3.3-3.4 - PAN protection | C1.1 | Confidentiality |
| 3.5-3.7 - Key management | C1.1 | Cryptography |

### Requirement 4: Transmission Encryption

| PCI DSS | SOC 2 Criteria | Notes |
|---------|----------------|-------|
| 4.1-4.2 - Encryption | CC6.6 | Transmission protection |

### Requirement 5: Malware Protection

| PCI DSS | SOC 2 Criteria | Notes |
|---------|----------------|-------|
| 5.1-5.4 - Anti-malware | CC6.8 | Malware protection |

### Requirement 6: Secure Development

| PCI DSS | SOC 2 Criteria | Notes |
|---------|----------------|-------|
| 6.1-6.2 - Secure SDLC | CC8.1, PI1.3 | Change, processing |
| 6.3 - Vulnerability mgmt | CC7.1 | Anomaly detection |
| 6.4 - Web app security | CC5.2 | Technology controls |
| 6.5 - Change management | CC8.1 | **Full overlap** |

### Requirement 7: Access Control

| PCI DSS | SOC 2 Criteria | Notes |
|---------|----------------|-------|
| 7.1-7.3 - Access restriction | CC6.1, CC6.4 | **Full overlap** |

### Requirement 8: Authentication

| PCI DSS | SOC 2 Criteria | Notes |
|---------|----------------|-------|
| 8.1-8.6 - User ID/auth | CC6.1-CC6.4 | **Full overlap** |

### Requirement 9: Physical Security

| PCI DSS | SOC 2 Criteria | Notes |
|---------|----------------|-------|
| 9.1-9.5 - Physical access | CC6.5 | **Full overlap** |

### Requirement 10: Logging and Monitoring

| PCI DSS | SOC 2 Criteria | Notes |
|---------|----------------|-------|
| 10.1-10.7 - Logging | CC7.2, CC7.3 | **Full overlap** |

### Requirement 11: Security Testing

| PCI DSS | SOC 2 Criteria | Notes |
|---------|----------------|-------|
| 11.1-11.2 - Wireless scans | CC7.1 | Detection |
| 11.3 - Vulnerability scans | CC7.1 | Detection |
| 11.4 - Penetration testing | CC4.1 | Monitoring |
| 11.5-11.6 - IDS/FIM | CC7.1, CC7.2 | Detection, monitoring |

### Requirement 12: Policies and Programs

| PCI DSS | SOC 2 Criteria | Notes |
|---------|----------------|-------|
| 12.1 - Security policy | CC1.1, CC5.1 | Control environment |
| 12.3 - Risk assessment | CC3.1, CC3.2 | **Full overlap** |
| 12.5 - Scope documentation | CC3.1 | Risk objectives |
| 12.6 - Security awareness | CC1.4, CC2.2 | **Full overlap** |
| 12.7 - Personnel screening | CC1.4 | Competence |
| 12.8 - Vendor management | CC9.2 | **Full overlap** |
| 12.10 - Incident response | CC7.4, CC7.5 | **Full overlap** |

---

## Overlap Summary

### High Overlap Areas (~60%)

These controls can use shared evidence:

| Area | SOC 2 | PCI DSS | Shared Evidence |
|------|-------|---------|-----------------|
| Access Control | CC6.1-6.4 | 7, 8 | Access matrix, user provisioning |
| Physical Security | CC6.5 | 9 | Badge logs, visitor logs |
| Logging | CC7.2-7.3 | 10 | SIEM reports, log samples |
| Change Management | CC8.1 | 6.5 | Change tickets, CAB records |
| Incident Response | CC7.4-7.5 | 12.10 | IRP, incident records |
| Vendor Management | CC9.2 | 12.8 | Vendor list, contracts |
| Security Training | CC1.4, CC2.2 | 12.6 | Training records |
| Risk Assessment | CC3.1-3.2 | 12.3 | Risk assessment docs |

### Limited Overlap Areas

| Area | Notes |
|------|-------|
| Network Security | PCI DSS more specific on segmentation |
| Encryption/Key Mgmt | PCI DSS more prescriptive |
| Vulnerability Scanning | PCI DSS quarterly requirement |
| Penetration Testing | PCI DSS annual requirement |
| Anti-Malware | PCI DSS more detailed |

### No Overlap

| PCI DSS Specific | SOC 2 Specific |
|------------------|----------------|
| PAN masking/truncation | Availability criteria |
| ASV scanning | Processing integrity |
| Quarterly wireless scans | Privacy criteria |
| POI device security | Service organization context |
| SAQ types | Type I vs Type II timing |

---

## Combined Audit Strategy

### Planning Phase

1. **Map common controls**
   - Identify overlapping requirements
   - Create unified control matrix
   - Assign single evidence requirements

2. **Coordinate timing**
   - Align audit periods
   - Schedule interviews once
   - Single evidence collection cycle

3. **Unified documentation**
   - Common policy structure
   - Shared procedures
   - Combined evidence repository

### Evidence Collection Strategy

```
Evidence Collection Structure:

Shared_Evidence/
├── Access_Control/          # CC6.1-6.4, PCI 7-8
├── Physical_Security/       # CC6.5, PCI 9
├── Logging_Monitoring/      # CC7.2-7.3, PCI 10
├── Change_Management/       # CC8.1, PCI 6.5
├── Incident_Response/       # CC7.4-7.5, PCI 12.10
├── Vendor_Management/       # CC9.2, PCI 12.8
├── Training/                # CC1.4, PCI 12.6
└── Risk_Assessment/         # CC3.1-3.2, PCI 12.3

PCI_Specific/
├── Network_Segmentation/    # PCI 1
├── Encryption/              # PCI 3, 4
├── Vulnerability_Scans/     # PCI 11.3
├── Penetration_Tests/       # PCI 11.4
└── POI_Security/            # PCI 9.5

SOC2_Specific/
├── Availability/            # A criteria
├── Processing_Integrity/    # PI criteria
└── Privacy/                 # P criteria (if in scope)
```

### Interview Consolidation

| Topic | SOC 2 Criteria | PCI DSS | Single Interview |
|-------|----------------|---------|------------------|
| Access Management | CC6.1-6.4 | 7, 8 | IAM Team |
| Physical Security | CC6.5 | 9 | Facilities |
| Logging/Monitoring | CC7.2-7.3 | 10 | SOC/Security |
| Change Management | CC8.1 | 6.5 | Change Manager |
| Incident Response | CC7.4-7.5 | 12.10 | Incident Manager |
| Vendor Management | CC9.2 | 12.8 | Procurement |
| Training | CC1.4, CC2.2 | 12.6 | HR/Training |

---

## Implementation Recommendations

### For Organizations with SOC 2

If you already have SOC 2:

1. **Leverage existing controls** for ~60% of PCI DSS
2. **Gap analysis** on PCI-specific requirements:
   - Network segmentation
   - PAN handling
   - Quarterly scanning
   - POI security
3. **Enhance** logging for PCI requirements
4. **Add** PCI-specific policies

### For Organizations with PCI DSS

If you already have PCI DSS:

1. **Map to SOC 2 TSC** for common controls
2. **Add** SOC 2 specific criteria if needed:
   - Availability
   - Processing Integrity
   - Privacy
3. **Enhance** documentation for AICPA format
4. **Engage** CPA firm for SOC 2 audit

### Combined Approach

For new compliance programs:

1. **Design controls** to satisfy both frameworks
2. **Single policy framework** with mapped requirements
3. **Unified evidence collection**
4. **Coordinate audit timing**
5. **Train staff** on both frameworks

---

## Resources

### SOC 2 Resources
- AICPA SOC 2 Guide
- Trust Services Criteria (2017)
- SOC for Cybersecurity

### PCI DSS Resources
- PCI DSS v4.0.1 Documentation
- SAQ Templates
- Prioritized Approach

### Mapping Resources
- Cloud Security Alliance CCM
- NIST Cybersecurity Framework
- ISO 27001 mappings
