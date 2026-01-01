---
name: pci-dss-compliance-consultant
description: PCI DSS 4.0.1 compliance audit support skill. Provides expert guidance for Cardholder Data Environment (CDE) scoping, gap analysis, audit preparation, SAQ completion support, and remediation planning. Includes SOC 2 mapping for combined audit efficiency. Use when preparing for PCI DSS audits, conducting gap analysis, creating remediation plans, or answering SAQ questionnaires for payment card compliance.
---

# PCI DSS Compliance Consultant

Expert guidance for PCI DSS 4.0.1 compliance and audit preparation.

## Overview

This skill provides comprehensive support for organizations preparing for PCI DSS (Payment Card Industry Data Security Standard) compliance assessments. It covers all 12 requirements of PCI DSS 4.0.1 and includes integration with SOC 2 for organizations pursuing combined audits.

### Key Dates

| Milestone | Date | Impact |
|-----------|------|--------|
| PCI DSS 3.2.1 Retirement | April 1, 2024 | v4.0 mandatory |
| v4.0.1 Release | June 2024 | Minor clarifications |
| Future-Dated Requirements | March 31, 2025 | 51 requirements become mandatory |

### Compliance Levels (Annual Transaction Volume)

| Level | Visa/Mastercard | Assessment Type |
|-------|-----------------|-----------------|
| Level 1 | 6M+ transactions | On-site QSA assessment |
| Level 2 | 1M - 6M transactions | SAQ + quarterly scans |
| Level 3 | 20K - 1M e-commerce | SAQ + quarterly scans |
| Level 4 | < 20K e-commerce | SAQ + quarterly scans |

## When to Use This Skill

Use this skill when you need to:

- **Prepare for QSA audits** - Get comprehensive checklists and evidence requirements
- **Conduct gap analysis** - Compare current security posture against PCI DSS 4.0.1 requirements
- **Understand specific requirements** - Get detailed explanations of any of the 281 sub-requirements
- **Select appropriate SAQ type** - Determine which Self-Assessment Questionnaire applies
- **Create remediation plans** - Develop prioritized action plans for compliance gaps
- **Map to SOC 2** - Identify overlapping controls for combined audit efficiency
- **Prepare evidence packages** - Know what documentation QSAs expect to see

## Workflows

### 1. Scoping and Gap Analysis

**Purpose**: Define CDE boundaries and identify compliance gaps

**Process**:
1. Identify all systems that store, process, or transmit cardholder data
2. Map data flows and identify connected systems
3. Review current security controls against each PCI DSS requirement
4. Document gaps with severity and remediation priority
5. Generate gap analysis report

**Reference**: Load `references/gap_analysis_template.md` for structured analysis

**Key Questions**:
- Where does cardholder data enter your environment?
- How does it flow through systems?
- Where is it stored (even temporarily)?
- Who/what has access to it?
- How is it transmitted externally?

### 2. Requirement Guidance

**Purpose**: Provide detailed explanations of PCI DSS requirements

**Process**:
1. Identify the specific requirement(s) in question
2. Load `references/pci_dss_4_requirements.md`
3. Explain the requirement's intent and testing procedures
4. Provide implementation examples
5. Highlight March 2025 mandatory items if applicable

**The 12 Requirements**:

| # | Requirement | Key Focus |
|---|-------------|-----------|
| 1 | Install and maintain network security controls | Firewalls, NSCs, segmentation |
| 2 | Apply secure configurations | Vendor defaults, hardening |
| 3 | Protect stored account data | Encryption, masking, retention |
| 4 | Protect CHD during transmission | TLS 1.2+, strong cryptography |
| 5 | Protect from malicious software | Anti-malware, detection |
| 6 | Develop secure systems and software | SDLC, vulnerability management |
| 7 | Restrict access to CHD | Need-to-know, least privilege |
| 8 | Identify and authenticate users | MFA, password policies |
| 9 | Restrict physical access | Physical security controls |
| 10 | Log and monitor access | Audit trails, monitoring |
| 11 | Test security regularly | Penetration testing, scans |
| 12 | Support with policies and programs | Security policies, awareness |

### 3. Audit Preparation

**Purpose**: Prepare organization for QSA on-site assessment

**Process**:
1. Load `references/audit_preparation_checklist.md`
2. Review documentation requirements
3. Prepare interview subjects by topic
4. Organize evidence packages
5. Conduct pre-audit readiness review

**Reference**: Load `references/evidence_collection_guide.md` for evidence specifics

**Timeline** (Recommended):
- 12 weeks out: Complete gap analysis
- 8 weeks out: Begin evidence collection
- 4 weeks out: Internal readiness review
- 2 weeks out: Final documentation check
- 1 week out: Prepare interview subjects

### 4. SAQ Completion Support

**Purpose**: Guide through Self-Assessment Questionnaire completion

**Process**:
1. Determine appropriate SAQ type using `references/saq_selection_guide.md`
2. Review each question in context
3. Provide guidance on compliant vs. non-compliant answers
4. Identify evidence needed for each "Yes" response
5. Document compensating controls if applicable

**SAQ Types**:

| SAQ | Applies To | Questions |
|-----|-----------|-----------|
| A | Card-not-present, fully outsourced | ~22 |
| A-EP | E-commerce with partial outsourcing | ~191 |
| B | Imprint machines or standalone terminals | ~41 |
| B-IP | IP-connected terminals, no e-commerce | ~82 |
| C | Payment applications, no storage | ~160 |
| C-VT | Virtual terminal only, no storage | ~79 |
| D | All others (merchants & service providers) | ~329 |
| P2PE | Validated P2PE solution | ~33 |

### 5. Remediation Planning

**Purpose**: Create prioritized remediation plans for identified gaps

**Process**:
1. Review gap analysis findings
2. Categorize by March 2025 deadline vs. current requirements
3. Assess remediation complexity and resource needs
4. Create prioritized remediation roadmap
5. Generate remediation plan document

**Template**: Use `assets/remediation_plan_template.md`

**Priority Framework**:
- **Critical**: Current requirements with high risk
- **High**: March 2025 requirements, complex implementation
- **Medium**: Current requirements, moderate effort
- **Low**: Best practice improvements

### 6. SOC 2 Integration

**Purpose**: Leverage SOC 2 controls for PCI DSS compliance

**Process**:
1. Load `references/soc2_pci_mapping.md`
2. Identify overlapping Trust Services Criteria
3. Map existing SOC 2 evidence to PCI DSS requirements
4. Identify gaps requiring additional controls
5. Plan combined audit strategy

**Overlap Areas** (~60% control overlap):
- Access control and authentication
- Network security and monitoring
- Change management
- Incident response
- Vendor management
- Security awareness training

## Quick Reference: March 2025 Mandatory Requirements

These requirements transition from best practice to mandatory on March 31, 2025:

### High-Impact Items

| Req | Description | Action Needed |
|-----|-------------|---------------|
| 3.4.2 | Technical controls to prevent copy/relocation of PAN | Implement DLP |
| 5.3.3 | Anti-malware for removable media | Deploy controls |
| 5.4.1 | Detect and protect against phishing | Implement email security |
| 6.4.2 | Web application firewall for public apps | Deploy WAF |
| 8.3.6 | Minimum password length 12 characters | Update policies |
| 8.4.2 | MFA for all access to CDE | Implement MFA |
| 10.4.1.1 | Automated audit log review | Implement SIEM |
| 11.3.1.1 | Internal vulnerability scans authenticated | Update scanning |
| 11.6.1 | Change/tamper detection for payment pages | Implement monitoring |
| 12.3.1 | Targeted risk analysis for requirements | Document analysis |

## Output Templates

### Compliance Report
Use `assets/compliance_report_template.md` for:
- Executive summary
- Scope description
- Requirement-by-requirement status
- Gap summary
- Recommendations

### Remediation Plan
Use `assets/remediation_plan_template.md` for:
- Gap identification
- Remediation actions
- Resource requirements
- Timeline
- Success criteria

## Glossary

| Term | Definition |
|------|------------|
| **CDE** | Cardholder Data Environment - systems that store, process, or transmit cardholder data |
| **CHD** | Cardholder Data - PAN plus cardholder name, expiration, service code |
| **PAN** | Primary Account Number - the 15-19 digit card number |
| **QSA** | Qualified Security Assessor - PCI-certified auditor |
| **ROC** | Report on Compliance - formal QSA assessment report |
| **SAQ** | Self-Assessment Questionnaire - self-evaluation form |
| **AOC** | Attestation of Compliance - formal compliance declaration |
| **ASV** | Approved Scanning Vendor - PCI-certified vulnerability scanner |
| **NSC** | Network Security Controls - firewalls and equivalent |
| **SAD** | Sensitive Authentication Data - CVV, PIN, track data |

## Important Notes

- PCI DSS compliance is a continuous process, not a one-time achievement
- Compensating controls may be acceptable when requirements cannot be met directly
- Documentation is critical - if it's not documented, it didn't happen
- Scope reduction through segmentation can significantly reduce compliance burden
- Always work with a QSA for complex compliance questions
- This skill provides guidance; final compliance determination is made by QSA/acquirer

## Resources

**Official Sources**:
- [PCI Security Standards Council](https://www.pcisecuritystandards.org/)
- [PCI DSS v4.0.1 Document Library](https://www.pcisecuritystandards.org/document_library/)

**Reference Files**:
- `references/pci_dss_4_requirements.md` - Detailed 12 requirements guide
- `references/audit_preparation_checklist.md` - Pre-audit checklist
- `references/evidence_collection_guide.md` - Evidence requirements
- `references/saq_selection_guide.md` - SAQ type selection
- `references/gap_analysis_template.md` - Gap analysis framework
- `references/soc2_pci_mapping.md` - SOC 2 control mapping
