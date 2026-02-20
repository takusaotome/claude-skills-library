# PM Knowledge Base Catalog and Usage Guide

## Overview

This skill includes a comprehensive PM knowledge base in the `references/` directory (544KB, 11 files) covering PMBOK standards, Software/SaaS best practices, IT industry guidance, and specialized PM methodologies.

---

## Knowledge Base Resources

### 1. Software & SaaS PM Best Practices Q&A (156KB)

**File**: `20250703-Software & SaaS 業界のPMベストプラクティスQ&A-ppxYLyVn.md`

**32 comprehensive Q&A scenarios** covering:
- **DevOps/CI/CD** (Q1-7, 19, 26-27): DevOps adoption, MVP strategy, silo elimination, CI/CD prioritization, automated testing, DevSecOps, canary releases
- **Backlog Management** (Q8-14): Refinement frequency, backlog bloat prevention, visualization, cross-team sharing, collaborative change management
- **Remote Development** (Q15-18): Communication rules, outcome-based accountability, digital-optimized Agile practices, async workflows
- **Requirements & Change** (Q20-21): Scope creep handling, technical debt repayment strategies
- **Stakeholder Communication** (Q22-25): Feedback cycles, sprint reviews, lightweight documentation, wiki maintenance
- **Team Collaboration** (Q23-24, 29-32): Bottleneck removal, inter-team dependencies, velocity stability, QA integration, tool selection

**Use when**: Cloud migration projects, SaaS product development, DevOps transformation, remote team management, Agile/Scrum adoption

### 2. IT PM Resources for US IT Industry (66KB)

**File**: `20250703-IT Project Management Resources for the US IT Industry-tcccN2I2.md`

US IT industry-specific PM resources, regulatory considerations, and industry best practices.

**Use when**: Projects for US-based clients, compliance with US IT standards, understanding US market PM practices

### 3. PMI Companion Standards for IT (48KB)

**File**: `20250703-PMIコンパニオン標準と拡張ガイド（IT業界向け）-bwKcIXZS.md`

PMI companion standards and extension guides tailored for IT industry projects.

**Use when**: Need to align project plans with PMI IT-specific standards, software development project planning

### 4. Project Scheduling and Risk Management Deep Dive (36KB)

**File**: `20250703-プロジェクトスケジューリングとリスク管理に関する詳細調査-TmSqtqVJ.md`

Detailed methodologies for:
- Critical path method (CPM)
- Schedule network analysis
- Risk identification and quantification
- Risk response strategies
- Monte Carlo simulation

**Use when**: Complex schedule development, high-risk projects, need for quantitative risk analysis

### 5. PMBOK Edition Comparison (6th/7th/8th) (35KB)

**File**: `20250703-PMBOK®ガイド第6版・第7版・第8版の構造・概念の比較調査-5Szb5Q8O.md`

Structural and conceptual comparison across PMBOK editions, helping understand evolution of PM standards.

**Use when**: Transitioning between PMBOK versions, understanding modern vs. traditional PM approaches

### 6. Framework Mapping: PMBOK vs. PRINCE2, ITIL 4, ISO 21502 (108KB)

**File**: `20250703-PMBOK第6版・第7版とPRINCE2・ITIL 4・ISO 21502のマッピング比較-iUp9j_kf.md`

Cross-framework mapping showing alignment and differences between:
- PMBOK 6th/7th Edition
- PRINCE2
- ITIL 4
- ISO 21502

**Use when**: Working in multi-framework environments, need to bridge PMBOK with ITIL/PRINCE2, international project standards compliance

### 7. PMBOK-GPT Knowledge Base Design (21KB)

**File**: `20250703-PMBOK-GPT Knowledge Base Design-PXgrdjZb.md`

Knowledge base architecture patterns for PM tools and AI-assisted project management systems.

**Use when**: Designing PM knowledge management systems, structuring project documentation repositories

### 8. PMP/PgMP Exam Outlines and Learning Roadmap (17KB)

**File**: `20250703-PMPPgMP等の試験アウトラインと学習ロードマップ  -oTfpatOa.md`

PMP (Project Management Professional) and PgMP (Program Management Professional) certification guidance.

**Use when**: Team capability development, PM training programs, certification preparation

### 9. AI, Hybrid Work, and ESG Impacts on PM (16KB)

**File**: `20250703-Impacts of AI, Hybrid Work, and ESG on Project Management-oTIu7R8E.md`

Modern PM trends and adaptations:
- AI integration in project management
- Hybrid work model considerations
- ESG (Environmental, Social, Governance) factors in project planning

**Use when**: Contemporary projects involving AI tools, distributed teams, sustainability requirements

### 10. Project Charter Guide (33KB)

**File**: `project_charter_guide.md`

Comprehensive guide for creating PMBOK-compliant project charters with 12 sections covering all charter components.

**Use when**: Creating or reviewing project charters, need detailed charter section templates

---

## Progressive Disclosure Pattern

**Level 1 - SKILL.md**: Core workflows and common scenarios (always loaded)
**Level 2 - References**: Detailed methodologies loaded on-demand when specific expertise needed
**Level 3 - Generated Output**: Customized artifacts incorporating knowledge base insights

---

## Usage Examples

### Example 1: Cloud Migration Project

**Scenario**: Planning AWS cloud migration for enterprise application

**Knowledge base usage**:
1. Start with **Software & SaaS Q&A** (#1) -> Q1-7 for DevOps adoption strategy
2. Reference **IT PM Resources** (#2) for US regulatory considerations (if applicable)
3. Use **Scheduling & Risk Management** (#4) for migration risk quantification
4. Apply **Framework Mapping** (#6) if client requires ITIL 4 alignment

**Workflow**:
- Create Project Charter with DevOps principles (Q1: small-scale pilot approach)
- Build WBS incorporating CI/CD pipeline setup (Q6: prioritize automation goals)
- Develop risk register for cloud migration risks (Reference #4)
- Create RACI matrix with cross-functional DevOps team structure (Q3: eliminate silos)

### Example 2: SaaS Product Development

**Scenario**: New SaaS product MVP launch

**Knowledge base usage**:
1. **Software & SaaS Q&A** (#1) -> Q2 (MVP strategy), Q8-14 (backlog management)
2. **AI/Hybrid Work/ESG** (#9) for modern development practices
3. **PMI IT Standards** (#3) for software development lifecycle alignment

**Workflow**:
- Project Charter emphasizing iterative MVP releases (Q2)
- Scope management with backlog refinement schedule (Q8: frequent reviews)
- Sprint planning with remote team considerations (Q15-18)
- Quality management integrating continuous testing (Q32: QA in development cycle)

---

## PMBOK Knowledge Area Coverage

All 10 PMBOK knowledge areas are supported through references:

| Knowledge Area | Primary Resources |
|----------------|-------------------|
| Integration | Framework Mapping (#6), PMBOK Comparison (#5) |
| Scope | Software & SaaS Q&A (#1: Q8-14 backlog management) |
| Schedule | Scheduling & Risk Deep Dive (#4) |
| Cost | IT PM Resources (#2), Exam Guides (#8) |
| Quality | Software & SaaS Q&A (#1: Q19, Q32) |
| Resource | Software & SaaS Q&A (#1: Q15-18 remote teams, Q23 productivity) |
| Communications | Software & SaaS Q&A (#1: Q22, Q16) |
| Risk | Scheduling & Risk Deep Dive (#4), Software & SaaS Q&A (#1: Q28) |
| Procurement | PMI Companion Standards (#3) |
| Stakeholder | Software & SaaS Q&A (#1: Q22, Q25) |

---

## When to Load Specific References

**During Charter Creation**: Load #1 (Q&A) for team structure and #6 (Framework Mapping) for organizational standards alignment

**During Scope Planning**: Load #1 (Q8-14) for backlog management best practices

**During Schedule Development**: Load #4 (Scheduling & Risk) for detailed network analysis and CPM

**During Risk Planning**: Load #4 (Scheduling & Risk) for quantitative methods and #1 (Q28) for Agile risk management

**For IT/Software Projects**: Always load #1 (Software & SaaS Q&A) as primary reference

**For Multi-Framework Environments**: Load #6 (Framework Mapping) to bridge PMBOK with PRINCE2/ITIL/ISO
