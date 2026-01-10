---
name: esg-reporter
description: |
  ESG(環境・社会・ガバナンス)レポート作成支援スキル。GRI、SASB、TCFD、CDP等の国際基準に準拠した
  サステナビリティレポート作成、マテリアリティ分析、KPI設定、データ収集・開示をサポート。
  Use when creating sustainability reports, conducting materiality assessments, setting ESG targets,
  or preparing disclosures aligned with GRI, SASB, TCFD, CDP, or CSRD standards.
  Triggers: "ESG report", "sustainability report", "TCFD", "GRI", "SASB", "CDP", "materiality assessment", "carbon footprint".
---

# ESG Reporter（ESGレポート作成支援）

## Overview

This skill provides professional ESG (Environmental, Social, Governance) reporting and sustainability disclosure support. Helps organizations create comprehensive sustainability reports aligned with international standards including GRI, SASB, TCFD, CDP, and emerging EU CSRD (Corporate Sustainability Reporting Directive).

**Primary language**: Japanese (default), English supported
**Standards Supported**: GRI, SASB, TCFD, CDP, CSRD/ESRS, ISSB (IFRS S1/S2)
**Output format**: Sustainability reports, materiality matrices, ESG KPI dashboards, TCFD disclosures, CDP responses

Use this skill when:
- Creating annual sustainability or ESG reports
- Conducting materiality assessments
- Setting science-based targets (SBTi)
- Preparing climate-related financial disclosures (TCFD)
- Responding to CDP (Carbon Disclosure Project) questionnaires
- Complying with EU CSRD requirements
- Benchmarking ESG performance against peers
- Engaging with ESG rating agencies (MSCI, Sustainalytics, CDP)

---

## Core Framework: ESG Reporting Standards

### Major ESG Reporting Frameworks

**1. GRI (Global Reporting Initiative)** - Global standard for sustainability reporting
- **Focus**: Broad sustainability impacts (environmental, social, governance)
- **Structure**: Universal Standards + Topic-specific Standards (33 topics)
- **Materiality**: Impact materiality (organization's impact on economy, environment, people)
- **Users**: All stakeholders (investors, employees, communities, NGOs)

**2. SASB (Sustainability Accounting Standards Board)** - Financially material ESG information
- **Focus**: Financially material ESG topics by industry (77 industry-specific standards)
- **Structure**: 26 General Issue Categories across 5 Dimensions
- **Materiality**: Financial materiality (ESG factors affecting company value)
- **Users**: Investors and financial community

**3. TCFD (Task Force on Climate-related Financial Disclosures)** - Climate risk disclosure
- **Focus**: Climate-related risks and opportunities
- **Structure**: 4 Pillars (Governance, Strategy, Risk Management, Metrics & Targets), 11 Recommendations
- **Materiality**: Climate-related financial risks
- **Users**: Investors, lenders, insurance underwriters

**4. CDP (Carbon Disclosure Project)** - Environmental data disclosure platform
- **Focus**: Climate change, water security, forests
- **Structure**: Detailed questionnaires with scoring methodology (A to D-)
- **Materiality**: Environmental impacts and dependencies
- **Users**: Investors (representing $130+ trillion in assets)

**5. CSRD/ESRS (EU Corporate Sustainability Reporting Directive / European Sustainability Reporting Standards)**
- **Focus**: Mandatory sustainability reporting for EU companies
- **Structure**: 12 ESRS standards (2 cross-cutting, 5 environmental, 4 social, 1 governance)
- **Materiality**: Double materiality (impact + financial materiality)
- **Users**: Mandatory for large EU companies (50,000+ companies by 2028)

**6. ISSB (International Sustainability Standards Board) - IFRS S1 & S2**
- **Focus**: Global baseline for sustainability disclosure (successor to TCFD)
- **Structure**: S1 (General sustainability disclosures), S2 (Climate-related disclosures)
- **Materiality**: Financial materiality
- **Users**: Investors (designed for capital markets)

### Framework Comparison Table

```markdown
| Framework | Scope | Materiality | Mandatory? | Primary Users |
|-----------|-------|-------------|------------|---------------|
| GRI | Broad sustainability (E, S, G) | Impact | Voluntary | All stakeholders |
| SASB | Financial ESG (industry-specific) | Financial | Voluntary (US) | Investors |
| TCFD | Climate risk | Financial | Increasingly mandatory | Investors, regulators |
| CDP | Environmental (Climate, Water, Forests) | Environmental | Voluntary | Investors, supply chain |
| CSRD/ESRS | Comprehensive sustainability | Double (Impact + Financial) | Mandatory (EU) | All stakeholders, regulators |
| ISSB (IFRS S1/S2) | General + Climate | Financial | Emerging mandatory | Investors |
```

**Recommendation**:
- **Integrated Approach**: Report using multiple frameworks (e.g., GRI for comprehensive report, TCFD for climate, SASB for investors)
- **Prioritization**: Start with GRI (baseline), add TCFD (climate focus), then SASB (investor focus)
- **EU Companies**: CSRD compliance is mandatory; use ESRS standards
- **Global Companies**: Monitor ISSB adoption in your jurisdictions

---

## Core Workflows

### Workflow 1: Materiality Assessment

**Purpose**: Identify and prioritize ESG topics most relevant to the organization and its stakeholders.

#### Step 1: Understand Materiality Concepts

**Single Materiality (Traditional)**: What ESG issues affect the company's financial performance?
- Used by: SASB, traditional financial reporting

**Double Materiality (Comprehensive)**:
1. **Impact Materiality**: How does the company impact the environment and society?
2. **Financial Materiality**: How do ESG issues affect the company's financial value?
- Used by: CSRD/ESRS, increasingly GRI

**Dynamic Materiality**: Materiality changes over time as risks emerge
- Example: Climate change was not material 20 years ago, now it's critical for most industries

#### Step 2: Identify Potential ESG Topics

**Comprehensive ESG Topic List** (categorized by E, S, G):

**Environmental (E)**:
- Climate change and GHG emissions (Scope 1, 2, 3)
- Energy management and renewable energy transition
- Water and wastewater management
- Waste management and circular economy
- Biodiversity and ecosystem impacts
- Air quality and pollution
- Resource efficiency (materials, packaging)

**Social (S)**:
- Employee health and safety
- Labor practices and working conditions
- Diversity, equity, and inclusion (DEI)
- Employee engagement and development
- Human rights in operations and supply chain
- Community relations and impact
- Product safety and quality
- Customer privacy and data security
- Responsible marketing and labeling

**Governance (G)**:
- Board composition and diversity
- Executive compensation linked to ESG
- Business ethics and anti-corruption
- Transparency and reporting
- Stakeholder engagement
- Supply chain management
- Risk management and oversight
- Tax strategy and transparency
- Political contributions and lobbying

#### Step 3: Stakeholder Engagement

**Identify Key Stakeholders**:
```markdown
| Stakeholder Group | Engagement Method | Key ESG Concerns |
|-------------------|-------------------|------------------|
| Investors/Shareholders | Annual meetings, investor calls, surveys | Climate risk, governance, financial materiality |
| Employees | Internal surveys, town halls, union consultations | Health & safety, DEI, labor rights, development |
| Customers | Customer surveys, feedback channels | Product safety, privacy, responsible marketing |
| Suppliers | Supplier assessments, audits | Supply chain ethics, human rights, environment |
| Communities | Community meetings, local partnerships | Environmental impact, jobs, social investment |
| Regulators | Compliance reporting, consultations | Legal compliance, transparency, risk management |
| NGOs/Civil Society | Partnerships, stakeholder forums | Environmental impact, human rights, transparency |
```

**Engagement Activities**:
- **Surveys**: Online questionnaires to prioritize ESG topics (typically 15-20 topics, rank by importance)
- **Interviews**: 1-on-1 discussions with key stakeholders (executives, large investors, community leaders)
- **Workshops**: Facilitated sessions with internal teams to identify impacts
- **Benchmarking**: Analyze peers' materiality assessments and ESG reports

#### Step 4: Materiality Matrix Construction

**Assess Each Topic on Two Dimensions**:

**Dimension 1: Stakeholder Concern (Importance to Stakeholders)**
- Score 1-5 based on stakeholder survey results and engagement feedback
- Weight different stakeholder groups based on strategic importance

**Dimension 2: Business Impact (Importance to Company)**
- **Financial Impact**: Potential financial risk/opportunity (revenue, cost, reputation)
- **Operational Impact**: Effect on operations, supply chain, regulatory compliance
- **Strategic Impact**: Alignment with business strategy and long-term value creation
- Score 1-5 based on internal assessment

**Materiality Matrix Example**:
```
         High Stakeholder Concern
                  │
    Material      │     High Priority
    (Report)      │     (Report + Action)
                  │
  ────────────────┼────────────────
                  │
    Monitor       │     Material
    (Internal)    │     (Report)
                  │
         Low Business Impact → High Business Impact
```

**Sample Materiality Matrix Results**:
```markdown
| ESG Topic | Stakeholder Concern | Business Impact | Materiality Level | Action |
|-----------|---------------------|-----------------|-------------------|--------|
| Climate change & GHG emissions | 5 | 5 | **High Priority** | Report + Set targets |
| Employee health & safety | 5 | 4 | **High Priority** | Report + Improve |
| Data privacy & security | 4 | 5 | **Material** | Report + Invest |
| Diversity, equity & inclusion | 4 | 3 | **Material** | Report + Programs |
| Water management | 3 | 4 | **Material** | Report |
| Board diversity | 3 | 2 | **Monitor** | Internal tracking |
| Community investment | 2 | 2 | **Monitor** | Continue programs |

**Material Topics** (will be disclosed in ESG report): Climate change, Employee health & safety, Data privacy, DEI, Water management
**High Priority Topics** (require strategic action + disclosure): Climate change, Employee health & safety
```

#### Step 5: Materiality Assessment Report

**Deliverable: Materiality Assessment Summary**:
```markdown
# Materiality Assessment 2025

## Executive Summary
Following a comprehensive materiality assessment process, we have identified 12 material ESG topics that are most significant to our business and stakeholders. These topics will form the foundation of our ESG strategy and reporting.

## Assessment Process
- **Period**: January - March 2025
- **Stakeholders Engaged**: 2,500+ respondents across 7 stakeholder groups
- **Methodology**: Double materiality assessment (impact + financial)
- **Framework Alignment**: GRI 3 (Material Topics), CSRD/ESRS

## Material Topics Identified

### High Priority (Report + Strategic Action Required)
1. **Climate Change & GHG Emissions** (Score: 5.0, 4.8)
   - Why material: Regulatory risk (carbon pricing), physical risks, stakeholder pressure
   - Current performance: 15% reduction since 2020, target: Net Zero by 2040
   - Actions: Science-based targets, renewable energy transition, Scope 3 engagement

2. **Employee Health & Safety** (Score: 4.9, 4.5)
   - Why material: Workforce wellbeing, regulatory compliance, operational continuity
   - Current performance: LTIR (Lost Time Injury Rate) 1.2 (industry avg: 1.8)
   - Actions: Zero-harm culture, enhanced training, AI-powered safety monitoring

[Continue for all material topics...]

## Materiality Matrix
[Insert visualization]

## Benchmarking
Our material topics align with 85% of peer companies in our industry, with stronger focus on climate and DEI compared to peers.

## Next Steps
1. Develop KPIs and targets for each material topic
2. Integrate material topics into ESG report structure
3. Annual review of materiality (next assessment: Q1 2026)

---

**Approved By**: ESG Steering Committee
**Date**: March 31, 2025
```

---

### Workflow 2: ESG Data Collection & Management

**Purpose**: Establish systematic data collection processes to measure ESG performance.

#### Step 1: Define ESG Metrics by Material Topic

**Metric Categories**:
- **Quantitative Metrics**: Numerical data (GHG emissions in tCO2e, water consumption in m³, injury rate)
- **Qualitative Metrics**: Descriptions and narratives (governance policies, stakeholder engagement approach)
- **Leading Indicators**: Forward-looking metrics (training hours, % renewable energy capacity)
- **Lagging Indicators**: Historical performance (total emissions, injury incidents)

**Example Metric Framework (Climate Change)**:
```markdown
## Material Topic: Climate Change & GHG Emissions

### Metrics (aligned with GRI 305, SASB, TCFD)

**GHG Emissions (Quantitative)**:
- **Scope 1 (Direct emissions)**: Emissions from owned/controlled sources
  - Metric: Total Scope 1 emissions (tCO2e)
  - Data source: Fuel consumption records (natural gas, diesel, fleet vehicles)
  - Calculation: Fuel consumption × Emission factor (IPCC guidelines)
  - Reporting frequency: Monthly, aggregated annually

- **Scope 2 (Indirect energy emissions)**: Emissions from purchased electricity, steam, heating, cooling
  - Metric: Total Scope 2 emissions (tCO2e), reported in both location-based and market-based methods
  - Data source: Utility bills, renewable energy certificates (RECs)
  - Calculation: kWh consumed × Grid emission factor (IEA, EPA)
  - Reporting frequency: Monthly, aggregated annually

- **Scope 3 (Value chain emissions)**: Upstream and downstream emissions (15 categories)
  - Metric: Total Scope 3 emissions (tCO2e) by category
  - Data source: Supplier data, spend-based estimates, industry averages
  - Calculation: Activity data × Emission factor (GHG Protocol Scope 3 Database)
  - Reporting frequency: Annually (most challenging to collect)

**Energy Consumption (Quantitative)**:
- Total energy consumption (MWh)
- % renewable energy (purchased or self-generated)
- Energy intensity (MWh per $ revenue or per production unit)

**Climate Targets (Qualitative + Quantitative)**:
- Science-based target status (committed/validated/achieved)
- Target: Reduce Scope 1+2 by 50% by 2030 (vs. 2020 baseline)
- Target: Net Zero across value chain by 2040

**Climate Risk Assessment (Qualitative)**:
- Physical risks identified (floods, hurricanes, drought)
- Transition risks identified (carbon pricing, regulation, technology shifts)
- Financial impact estimates ($ at risk over 10-year horizon)
```

#### Step 2: Data Collection Infrastructure

**Data Collection Methods**:

**1. Automated Data Collection** (Preferred):
- **ERP Integration**: Pull energy, water, waste data from ERP systems automatically
- **IoT Sensors**: Real-time monitoring of energy consumption, emissions
- **Smart Meters**: Electricity, gas, water meters with automated reporting
- **ESG Software Platforms**: Centralized ESG data management (Workiva, Sphera, Enablon, Benchmark Gensuite)

**2. Manual Data Collection** (Supplement when automation unavailable):
- **Spreadsheet Templates**: Standardized templates for sites to submit data
- **Surveys**: Employee surveys (engagement, DEI), supplier surveys (Scope 3)
- **Document Review**: Board meeting minutes (governance), policies, incident reports

**Data Quality Assurance**:
- **Validation Rules**: Automated checks (e.g., emissions cannot be negative, year-over-year change >50% triggers review)
- **Reconciliation**: Cross-check with financial data (spend on electricity should correlate with kWh consumed)
- **Third-Party Verification**: External assurance for key metrics (GHG inventory, water data)
- **Internal Audit**: Annual internal audit of ESG data collection processes

#### Step 3: ESG Data Governance

**Roles and Responsibilities**:
```markdown
| Role | Responsibility |
|------|----------------|
| **Chief Sustainability Officer (CSO)** | Overall ESG strategy and reporting accountability |
| **ESG Data Manager** | Centralized data collection, validation, reporting |
| **Site ESG Coordinators** | Data collection at each facility (energy, water, waste, safety) |
| **Procurement Team** | Supplier ESG data (Scope 3, supply chain ethics) |
| **HR Department** | Employee data (DEI, training, health & safety, engagement) |
| **IT Department** | Data infrastructure, ESG software platform management |
| **Finance Department** | Financial ESG metrics (ESG-linked financing, green investments) |
| **Internal Audit** | Annual ESG data quality audit |
| **External Auditor** | Third-party assurance of ESG report |
```

**Data Management Calendar**:
```markdown
| Month | Activity |
|-------|----------|
| **Jan** | Data collection launch for previous year (final data) |
| **Feb** | Data validation and quality checks |
| **Mar** | ESG report drafting, materiality review |
| **Apr** | Internal review and approvals |
| **May** | External assurance engagement |
| **Jun** | Publish annual ESG report |
| **Ongoing** | Quarterly KPI tracking, monthly metrics for internal dashboards |
```

---

### Workflow 3: TCFD Climate Disclosure

**Purpose**: Disclose climate-related risks and opportunities aligned with TCFD recommendations.

#### TCFD Structure: 4 Pillars, 11 Recommendations

**Pillar 1: Governance** (2 recommendations):
- a) Board's oversight of climate-related risks and opportunities
- b) Management's role in assessing and managing climate-related risks and opportunities

**Pillar 2: Strategy** (3 recommendations):
- a) Climate-related risks and opportunities identified over short, medium, and long term
- b) Impact of climate risks and opportunities on business, strategy, and financial planning
- c) Resilience of strategy under different climate scenarios (including 2°C or lower scenario)

**Pillar 3: Risk Management** (3 recommendations):
- a) Processes for identifying and assessing climate-related risks
- b) Processes for managing climate-related risks
- c) Integration of climate risk into overall risk management

**Pillar 4: Metrics and Targets** (3 recommendations):
- a) Metrics used to assess climate-related risks and opportunities
- b) Scope 1, 2, and (if appropriate) Scope 3 GHG emissions and related risks
- c) Targets used to manage climate-related risks and opportunities, and performance against targets

#### TCFD Disclosure Template

**Governance Disclosure Example**:
```markdown
## Governance

### Board Oversight
The Board of Directors oversees climate-related risks and opportunities through the Sustainability Committee, which meets quarterly. The Committee reviews:
- Climate risk assessments and scenario analysis results
- Progress toward emissions reduction targets
- Climate-related investments and capital allocation
- Emerging climate regulations and policy developments

In 2024, the Sustainability Committee:
- Approved Science-Based Target (SBTi) commitment for Net Zero by 2040
- Reviewed climate scenario analysis results (including 1.5°C pathway)
- Approved $50M investment in renewable energy infrastructure

### Management's Role
The Chief Sustainability Officer (CSO) reports to the CEO and is responsible for:
- Developing and implementing climate strategy
- Conducting annual climate risk assessments
- Monitoring climate-related metrics and targets
- Integrating climate considerations into business planning

The Climate Steering Committee (chaired by CSO, includes CFO, COO, CRO) meets monthly to:
- Assess climate risks and opportunities
- Prioritize climate mitigation and adaptation actions
- Review quarterly emissions performance
- Coordinate cross-functional climate initiatives
```

**Strategy Disclosure Example** (Most Complex Section):
```markdown
## Strategy

### Climate-Related Risks and Opportunities

**Short-term (0-3 years)**:

**Transition Risks**:
- **Policy & Legal**: Carbon pricing implementation in key markets (EU ETS, potential US carbon tax)
  - Impact: Estimated $5-10M additional annual cost if carbon price reaches $50/tCO2e
  - Response: Reduce Scope 1+2 emissions by 25% by 2026, invest in energy efficiency

**Physical Risks**:
- **Acute**: Increased frequency of hurricanes affecting Gulf Coast manufacturing facility
  - Impact: Potential 2-week disruption, $8M revenue loss per event
  - Response: Enhanced business continuity planning, facility hardening, insurance coverage

**Opportunities**:
- **Products & Services**: Growing customer demand for low-carbon products
  - Impact: Potential $20M new revenue from "Green Product Line" by 2026
  - Response: Accelerate R&D for sustainable alternatives, launch marketing campaign

**Medium-term (3-10 years)**:

[Continue for medium and long-term...]

### Scenario Analysis

We conducted climate scenario analysis to test the resilience of our strategy under different climate futures:

**Scenarios Analyzed**:
1. **IEA Net Zero by 2050 (1.5°C pathway)**: Aggressive decarbonization, high carbon prices, rapid clean tech adoption
2. **IEA Stated Policies (STEPS) (2.7°C pathway)**: Current policies continue, moderate carbon pricing
3. **High Physical Risk (3-4°C pathway)**: Limited mitigation, severe physical impacts

**Key Assumptions**:
| Parameter | Net Zero 2050 | Stated Policies | High Physical Risk |
|-----------|---------------|-----------------|---------------------|
| Carbon price (2030) | $150/tCO2e | $50/tCO2e | $25/tCO2e |
| Renewable energy cost | -60% by 2030 | -40% by 2030 | -30% by 2030 |
| Frequency of extreme weather | +20% | +40% | +100% |
| Customer low-carbon preference | 70% by 2030 | 40% by 2030 | 20% by 2030 |

**Financial Impact by Scenario (NPV over 10 years)**:
- **Net Zero 2050**: -$50M (High transition costs, but long-term revenue growth from green products)
- **Stated Policies**: -$30M (Moderate transition costs, moderate physical risks)
- **High Physical Risk**: -$120M (Severe physical disruptions, lower carbon product demand)

**Resilience Assessment**:
Our strategy is resilient across scenarios because:
1. Committed to emissions reduction regardless of policy (SBTi target)
2. Diversified operations across multiple geographies (reduces single-point physical risk)
3. Investing in low-carbon product innovation (captures opportunity in Net Zero scenario)
4. Physical risk mitigation (site hardening, business continuity) protects against high physical risk

However, we have identified vulnerabilities:
- Heavy reliance on natural gas (Scope 1 emissions) exposes us to carbon pricing risk in Net Zero scenario
- Gulf Coast facility highly exposed to hurricanes in High Physical Risk scenario

**Strategic Adaptations**:
- Accelerate transition from natural gas to renewable electricity (electrification of processes)
- Evaluate relocation or redundancy for Gulf Coast facility
```

**Risk Management Disclosure Example**:
```markdown
## Risk Management

### Process for Identifying Climate Risks

We identify climate risks through:
1. **Annual Climate Risk Assessment**: Cross-functional workshop with 30+ participants from operations, finance, strategy, EHS
   - Physical risks: Review climate projections (IPCC, local meteorological data) for each facility location
   - Transition risks: Monitor policy developments (carbon pricing, renewable mandates), technology trends, market shifts

2. **External Data Sources**:
   - Climate models: IPCC scenarios, regional climate projections
   - Policy tracking: IEA, World Bank, local government consultations
   - Stakeholder input: Investor surveys, customer feedback

3. **Risk Prioritization**:
   - Likelihood (1-5 scale based on climate science/policy probability)
   - Impact (1-5 scale based on financial, operational, reputational consequences)
   - Time horizon (short/medium/long term)

### Process for Managing Climate Risks

Prioritized climate risks are assigned to functional owners who develop mitigation plans:
- **Transition Risks**: CSO leads mitigation strategy (emissions reduction, renewable energy procurement)
- **Physical Risks**: COO leads adaptation strategy (facility resilience, supply chain diversification)

Mitigation plans are integrated into:
- Annual budget and capital allocation process
- Strategic planning (3-5 year horizon)
- Enterprise risk management (ERM) system

### Integration into Overall Risk Management

Climate risks are integrated into our Enterprise Risk Management (ERM) framework:
- **Risk Register**: Climate risks are part of the enterprise-wide risk register, reviewed quarterly by Risk Committee
- **Risk Appetite**: Board has defined risk tolerance for climate risks (e.g., no single-site physical risk >$10M exposure)
- **Risk Reporting**: Climate risks reported to Board alongside financial, operational, cyber, and strategic risks
```

**Metrics and Targets Disclosure Example**:
```markdown
## Metrics and Targets

### GHG Emissions

| Scope | 2022 | 2023 | 2024 | 2024 Target | % Change (vs. 2020) |
|-------|------|------|------|-------------|---------------------|
| Scope 1 | 125,000 | 118,000 | 112,000 | 115,000 | -15% ✓ |
| Scope 2 (location-based) | 85,000 | 78,000 | 70,000 | 75,000 | -22% ✓ |
| Scope 2 (market-based) | 85,000 | 65,000 | 45,000 | 60,000 | -47% ✓ |
| Scope 3 (Category 1: Purchased Goods) | 450,000 | 440,000 | 430,000 | - | -4% |
| **Total Scope 1+2 (market-based)** | **210,000** | **183,000** | **157,000** | **175,000** | **-25% ✓** |
| **Total (all scopes)** | **660,000** | **623,000** | **587,000** | - | **-11%** |

**Emissions Intensity**:
- Per $ revenue: 125 tCO2e/million USD (2024) vs. 145 tCO2e/million USD (2020) → -14%
- Per production unit: 0.85 tCO2e/unit (2024) vs. 1.05 tCO2e/unit (2020) → -19%

### Climate Targets

**Science-Based Targets (SBTi-validated)**:
- **Near-term (2030)**: Reduce Scope 1+2 GHG emissions by 50% vs. 2020 baseline
  - Progress: -25% achieved as of 2024 → ON TRACK
- **Long-term (2040)**: Achieve Net Zero emissions across value chain (Scope 1+2+3)
  - Progress: Scope 3 accounting complete, supplier engagement launched

**Renewable Energy Target**:
- **Target**: 100% renewable electricity by 2030
- **Progress**: 35% renewable (2024) vs. 10% (2020)

### Other Climate Metrics

**Energy Consumption**:
- Total energy: 850,000 MWh (2024) vs. 920,000 MWh (2020) → -8%
- Renewable energy: 300,000 MWh (35% of total)

**Climate-Related Investments**:
- Capital investment in emissions reduction projects: $50M (2024)
- % of capex allocated to low-carbon projects: 25%

**Climate Risk Exposure**:
- Number of facilities in high physical risk zones (floods, hurricanes): 3 out of 12 (25%)
- Financial exposure to carbon pricing: $8M annually at $50/tCO2e
```

---

### Workflow 4: GRI-Based ESG Report Creation

**Purpose**: Create comprehensive annual sustainability report following GRI Standards.

#### GRI Universal Standards Structure

**GRI 1: Foundation** (Principles and concepts)
**GRI 2: General Disclosures** (Organizational profile, activities, governance, stakeholder engagement)
**GRI 3: Material Topics** (Process to determine material topics, list of material topics)

**GRI Topic-Specific Standards** (33 standards across E, S, G):
- Environmental: GRI 301-308 (Materials, Energy, Water, Biodiversity, Emissions, Waste, Supplier Environmental Assessment)
- Social: GRI 401-416 (Employment, Labor Relations, OHS, Training, Diversity, Non-Discrimination, Freedom of Association, Child/Forced Labor, Security Practices, Rights of Indigenous Peoples, Human Rights Assessment, Local Communities, Supplier Social Assessment, Public Policy, Customer Health & Safety, Marketing & Labeling, Customer Privacy)
- Economic/Governance: GRI 201-207 (Economic Performance, Market Presence, Indirect Economic Impacts, Procurement Practices, Anti-Corruption, Anti-Competitive Behavior, Tax)

#### ESG Report Structure Template

```markdown
# Sustainability Report 2024

## Table of Contents

1. CEO Message
2. About This Report
3. Company Profile
4. Sustainability Strategy
5. Materiality Assessment
6. Environmental Performance
7. Social Performance
8. Governance
9. GRI Content Index
10. Assurance Statement

---

## 1. CEO Message (1 page)

[Narrative from CEO highlighting key achievements, challenges, commitments]

Key Points to Include:
- Strategic importance of sustainability
- 2024 highlights (e.g., "Achieved 25% emissions reduction, launched DEI program")
- Challenges faced (e.g., "Supply chain disruptions from climate events")
- Future commitments (e.g., "Committing to Science-Based Targets")

---

## 2. About This Report (GRI 2-1 to 2-5)

**Reporting Period**: January 1 - December 31, 2024
**Reporting Cycle**: Annual (previous report published June 2024)
**Reporting Standards**: GRI Standards 2021, TCFD Recommendations, SASB [Industry] Standard
**Reporting Boundary**: [Company Name] and all consolidated subsidiaries (See Note X for list of entities)
**Restatements**: 2023 Scope 2 emissions restated due to improved data quality (-5% adjustment)
**External Assurance**: Limited assurance provided by [Auditor] (see Assurance Statement)
**Contact**: sustainability@company.com

---

## 3. Company Profile (GRI 2-1 to 2-6)

**Company Name**: [Full legal name]
**Headquarters**: [Location]
**Nature of Ownership**: Publicly traded (NASDAQ: ABC)
**Operations**: [Brief description of business activities, products, markets]
**Scale**:
- Revenue: $2.5B (2024)
- Employees: 8,500 (2024)
- Locations: 35 facilities across 12 countries

[Include organizational chart, geographic footprint map]

---

## 4. Sustainability Strategy (GRI 2-12, 2-13, 2-22 to 2-24)

### Our Sustainability Vision
"To be the most sustainable company in our industry by 2030, delivering value to shareholders while minimizing environmental impact and creating positive social outcomes."

### Sustainability Governance
- **Board Oversight**: Sustainability Committee (4 independent directors, meets quarterly)
- **Management Accountability**: Chief Sustainability Officer (CSO) reports to CEO
- **Policy Statement**: [Link to Sustainability Policy, approved by Board in January 2024]

### Strategic Priorities (Aligned with Material Topics)
1. **Climate Action**: Achieve Net Zero by 2040 (SBTi-validated targets)
2. **Circular Economy**: Zero waste to landfill by 2030
3. **Workforce Wellbeing**: Zero harm culture, industry-leading safety
4. **Diversity & Inclusion**: 40% women in leadership by 2027
5. **Responsible Supply Chain**: 100% suppliers screened for ESG by 2026

### Stakeholder Engagement (GRI 2-29)
[Table showing stakeholder groups, engagement methods, frequency, key concerns]

---

## 5. Materiality Assessment (GRI 3-1, 3-2, 3-3)

### Process (GRI 3-1)
[Describe materiality assessment process - see Workflow 1]

### Material Topics List (GRI 3-2)
1. Climate change & GHG emissions → GRI 305 (Emissions), TCFD
2. Employee health & safety → GRI 403 (Occupational Health & Safety)
3. Data privacy & security → GRI 418 (Customer Privacy)
4. Diversity, equity & inclusion → GRI 405 (Diversity), 406 (Non-Discrimination)
5. Water management → GRI 303 (Water)
6. Waste and circular economy → GRI 306 (Waste)
7. Supply chain labor practices → GRI 414 (Supplier Social Assessment)
8. Product safety & quality → GRI 416 (Customer Health & Safety)
9. Business ethics & anti-corruption → GRI 205 (Anti-Corruption)
10. Responsible tax practices → GRI 207 (Tax)

### Materiality Matrix
[Insert visual]

---

## 6. Environmental Performance

### 6.1 Climate Change & GHG Emissions (GRI 305)

**Material Topic**: Climate change & GHG emissions (identified as highest priority in materiality assessment)

**Why This is Material**:
- **Impact**: Our operations emit 660,000 tCO2e annually, contributing to climate change
- **Financial**: Exposed to carbon pricing risk ($8M annually at $50/tCO2e)
- **Stakeholder Concern**: Investors, customers, regulators prioritize emissions reduction

**Our Approach** (GRI 3-3: Management of Material Topic):
- Committed to Science-Based Targets: 50% reduction by 2030, Net Zero by 2040
- Three-pillar strategy: Energy efficiency, renewable energy, Scope 3 engagement
- Annual capital budget allocation: $50M for low-carbon projects
- Governance: Climate Steering Committee (CSO, CFO, COO) oversees implementation

**Performance** (GRI 305-1, 305-2, 305-3):

[Insert emissions data table - see TCFD example]

**Progress Against Target**:
- 2030 Target: 50% reduction (Scope 1+2 vs. 2020) → **Current: -25% → ON TRACK**
- 2040 Target: Net Zero (all scopes) → Roadmap developed, execution underway

**Key Initiatives in 2024**:
1. Installed 5 MW solar panels at 3 facilities (generates 8,000 MWh/year)
2. Replaced 15% of natural gas boilers with electric heat pumps
3. Purchased 150,000 MWh of renewable energy certificates (RECs)
4. Launched supplier engagement program: Top 20 suppliers (covering 60% of Scope 3) committed to SBTs

**[Repeat this structure for each material topic]**

### 6.2 Water Management (GRI 303)
[Content following same structure as above]

### 6.3 Waste and Circular Economy (GRI 306)
[Content...]

---

## 7. Social Performance

### 7.1 Employee Health & Safety (GRI 403)
[Content...]

### 7.2 Diversity, Equity & Inclusion (GRI 405, 406)
[Content...]

### 7.3 Supply Chain Labor Practices (GRI 414)
[Content...]

---

## 8. Governance

### 8.1 Business Ethics & Anti-Corruption (GRI 205)
[Content...]

### 8.2 Responsible Tax Practices (GRI 207)
[Content...]

---

## 9. GRI Content Index

| GRI Standard | Disclosure | Location in Report | Omission |
|--------------|------------|--------------------|----------|
| GRI 2-1 | Organizational details | Section 3, p. 5 | - |
| GRI 2-6 | Activities, value chain, relationships | Section 3, p. 6-7 | - |
| GRI 305-1 | Direct (Scope 1) GHG emissions | Section 6.1, p. 22 | - |
| GRI 305-3 | Other indirect (Scope 3) GHG emissions | Section 6.1, p. 24 | Categories 9-15 omitted (not material) |
| ... | ... | ... | ... |

---

## 10. Independent Assurance Statement

[Third-party assurance report from auditor confirming data accuracy]

---

**Publication Date**: June 15, 2025
**Next Report**: June 2026
**Feedback**: sustainability@company.com
```

---

### Workflow 5: CDP Climate Change Response

**Purpose**: Respond to CDP Climate Change questionnaire to achieve high score (A/A-).

#### CDP Structure and Scoring

**CDP Climate Change Questionnaire Sections**:
1. **Introduction** (Company info, reporting year)
2. **Management** (Governance, business implications of climate change)
3. **Risks and Opportunities** (Climate risks and opportunities)
4. **Business Strategy** (Strategic planning, scenario analysis)
5. **Targets and Performance** (Emissions targets and progress)
6. **Emissions Methodology** (Scope 1, 2, 3 accounting)
7. **Emissions Data** (Actual emissions numbers)
8. **Energy** (Energy consumption, renewable energy)
9. **Additional Metrics** (Other climate metrics)
10. **Verification** (Third-party assurance)
11. **Carbon Pricing** (Internal carbon price, carbon credits)
12. **Engagement** (Value chain engagement, public policy)

**CDP Scoring Levels**:
- **A / A-**: Leadership (Implementing current best practices, leading industry)
- **B / B-**: Management (Taking coordinated action on climate issues)
- **C / C-**: Awareness (Knowledge of climate impacts, beginning to act)
- **D / D-**: Disclosure (Disclosing information, limited evidence of action)
- **F**: Failure (Did not respond or provided insufficient information)

**Score Distribution (2023 Global Data)**:
- A: 2% of companies
- B: 23%
- C: 38%
- D: 29%
- F: 8%

#### Key Success Factors for High CDP Score

**1. Comprehensive Disclosure** (Complete all relevant questions):
- Don't skip questions; "Not applicable" is better than blank
- Provide narrative explanations, not just data
- Attach supporting documents (policies, reports, targets)

**2. Board-Level Governance**:
- Demonstrate board oversight (Sustainability Committee)
- Show executive accountability (CSO with climate mandate)
- Link executive compensation to climate metrics

**3. Ambitious Science-Based Targets**:
- Targets aligned with SBTi (1.5°C pathway preferred for A score)
- Short-term AND long-term targets (2030 + 2050)
- Scope 3 targets (increasingly required for A score)

**4. Complete Scope 3 Accounting**:
- Report all 15 Scope 3 categories (or justify exclusions)
- Use primary supplier data, not just spend-based estimates
- Engage suppliers to reduce Scope 3 emissions

**5. Scenario Analysis**:
- Conduct climate scenario analysis (TCFD requirement)
- Use IEA or IPCC scenarios (including 2°C or lower)
- Show financial quantification of risks/opportunities

**6. Third-Party Assurance**:
- External verification of Scope 1+2 emissions (minimum)
- Ideally, assurance for Scope 3 as well

**7. Value Chain Engagement**:
- Supplier engagement (% of suppliers with SBTs)
- Customer engagement (low-carbon products)
- Industry collaboration (trade associations, initiatives)

#### CDP Response Strategy

**Question Prioritization** (focus effort on high-scoring questions):
- **High Weight Questions** (Leadership level required for A):
  - C1.1a: Board oversight of climate (demonstrate climate expertise on board)
  - C2.4a: Transition risks (financial quantification required)
  - C4.1/C4.2: Scenario analysis (detailed scenarios, financial impacts)
  - C4.5: Net Zero target (SBTi-validated target)
  - C6.5: Scope 3 emissions (all categories reported)
  - C11.3: Value chain engagement (supplier SBT commitments)

**Common Mistakes to Avoid**:
- ❌ Incomplete Scope 3 reporting (loses significant points)
- ❌ No financial quantification of risks (narrative only)
- ❌ No scenario analysis (or superficial analysis)
- ❌ Targets not science-based (e.g., intensity-only targets without absolute reduction)
- ❌ No third-party assurance
- ❌ No evidence of board engagement (climate relegated to middle management)

**CDP Response Workflow**:
```markdown
## CDP Response Timeline (Annual)

**July**: CDP opens for responses
**July-August**: Data collection (emissions, energy, targets, risks, financials)
**September**: First draft (assign questions to functional experts)
**October**: Internal review and Q&A refinement
**November**: External review (consultant review recommended for first submission)
**December**: Final submission (deadline varies, typically late December to early January)
**January-March**: CDP scoring and feedback
**March**: CDP score release (public A-list announced in spring)
```

---

## Best Practices

### 1. Start with Materiality

Don't report on everything; focus on material topics:
- Conduct materiality assessment every 2-3 years
- Align reporting with material topics (depth > breadth)
- Explain why certain topics are not material (if questioned)

### 2. Set Science-Based Targets

Credible climate action requires science-based targets:
- Submit targets to SBTi for validation (demonstrates rigor)
- Align with 1.5°C pathway (increasingly expected)
- Include Scope 3 (mandatory for many industries)

### 3. Integrate ESG into Core Business

ESG should not be a separate reporting exercise:
- Link ESG KPIs to executive compensation (10-20% of variable pay)
- Integrate ESG into capital allocation (ESG-linked financing, green bonds)
- Embed sustainability into product development and operations

### 4. External Assurance Enhances Credibility

Third-party assurance builds trust:
- Start with limited assurance (less expensive, faster)
- Focus on material quantitative metrics (GHG emissions, water, safety)
- Reasonable assurance for key metrics (higher level of rigor)

### 5. Communicate Progress Transparently

Transparency builds trust, even when targets are missed:
- Report progress against targets honestly (don't cherry-pick)
- Explain underperformance and corrective actions
- Update stakeholders regularly (quarterly ESG updates, not just annual report)

---

## Common Pitfalls

### ❌ Greenwashing (Overstating Achievements)

Making misleading environmental claims.
**Solution**: Be specific, provide evidence, get third-party assurance.

### ❌ Boilerplate Reporting (Generic Narratives)

Report reads like every other company's report.
**Solution**: Be specific to your company, use real examples, show year-over-year progress.

### ❌ Data Quality Issues

Inaccurate or incomplete ESG data.
**Solution**: Invest in ESG data management systems, establish data governance, conduct internal audits.

### ❌ Ignoring Scope 3 Emissions

Focusing only on Scope 1+2, ignoring 80%+ of footprint.
**Solution**: Account for all 15 Scope 3 categories, engage suppliers, set Scope 3 targets.

### ❌ Lack of Ambition

Setting weak targets (e.g., intensity targets only, no absolute reduction).
**Solution**: Set science-based absolute reduction targets, align with 1.5°C pathway.

### ❌ No Governance Accountability

ESG delegated to mid-level managers, no board oversight.
**Solution**: Establish board-level Sustainability Committee, link executive pay to ESG.

---

このスキルの目的は、組織が国際的なESG基準に準拠したサステナビリティレポートを作成し、ステークホルダーの信頼を獲得し、持続可能な経営を推進することです。マテリアリティ分析、データ収集、TCFD開示、GRIレポート、CDP対応を通じて、透明性の高いESG情報開示を実現してください。
