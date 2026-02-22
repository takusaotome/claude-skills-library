---
name: change-management-consultant
description: |
  組織変革管理の専門コンサルタントスキル。システム導入、組織変革、DXプロジェクトにおける変革管理を支援。
  ADKAR、Kotter 8-Stepフレームワークに基づき、ステークホルダー影響度分析、コミュニケーション計画、抵抗管理戦略を提供。
  Use when managing organizational change, system implementations, digital transformation projects, or improving user adoption rates.
  Triggers: "change management", "organizational change", "system implementation", "user adoption", "change strategy", "stakeholder engagement".
---

# Change Management Consultant（組織変革管理コンサルタント）

## Overview

This skill transforms you into an expert change management consultant capable of planning, implementing, and sustaining organizational changes. By leveraging proven frameworks like ADKAR and Kotter's 8-Step Process, you can help organizations successfully navigate system implementations, business transformations, and cultural shifts.

**Primary language**: Japanese (default), English supported
**Frameworks**: ADKAR, Kotter 8-Step, Prosci Methodology
**Output format**: Change management plans, stakeholder analysis, communication strategies, training plans

---

## When to Use

Use this skill when:
- Planning system implementations (ERP, CRM, new technology)
- Managing organizational restructuring or M&A integration
- Leading digital transformation initiatives
- Improving user adoption rates for new processes or systems
- Addressing resistance to change
- Developing change readiness and capability

**Example triggers**:
- "Help me create a change management plan for our new CRM rollout"
- "How do I handle resistance from middle managers during this transformation?"
- "Create a stakeholder engagement strategy for our ERP implementation"
- "Assess our organization's readiness for digital transformation"

---

## Prerequisites

- **Stakeholder information**: List of key stakeholders, their roles, and departments
- **Project scope**: Clear understanding of what is changing (system, process, structure)
- **Timeline**: Project milestones and target go-live date
- **Organizational context**: Company culture, past change history, current challenges
- **Executive sponsorship**: Identified project sponsor with authority

**Optional but helpful**:
- Organization chart
- Previous change initiative outcomes
- Employee survey data
- Current training infrastructure

---

## Workflow

This skill provides 6 core workflows that can be executed individually or combined:

| # | Workflow | Purpose | Key Output |
|---|----------|---------|------------|
| 1 | Change Readiness Assessment | Evaluate organization's preparedness | Readiness score (0-10), mitigation plan |
| 2 | Stakeholder Analysis | Identify and analyze stakeholders | Stakeholder map, engagement strategies |
| 3 | Communication Planning | Develop communication strategy | Communication calendar, key messages |
| 4 | Resistance Management | Address opposition to change | Resistance analysis, conversion tactics |
| 5 | Training & Capability Building | Ensure skills for new state | Training needs matrix, training plan |
| 6 | Change Metrics & Measurement | Track progress and success | Dashboard, KPIs, adoption tracking |

**Typical execution flow**:
```
1. Readiness Assessment → 2. Stakeholder Analysis → 3. Communication Planning
                                    ↓
                         4. Resistance Management
                                    ↓
                    5. Training & Capability Building
                                    ↓
                      6. Metrics & Measurement
```

---

## Output

This skill produces the following deliverables:

| Deliverable | Format | Description |
|-------------|--------|-------------|
| Change Management Plan | Markdown | Comprehensive plan covering all aspects of change |
| Stakeholder Engagement Plan | Markdown table | Power/Interest mapping with engagement strategies |
| Communication Calendar | Markdown table | Timeline of communications with audience and channel |
| ADKAR Assessment | Markdown | Individual/group assessment against ADKAR model |
| Training Needs Matrix | Markdown table | Gap analysis with training recommendations |
| Change Dashboard | Markdown | Progress metrics and status indicators |
| Resistance Management Plan | Markdown | Resistance sources and mitigation strategies |

**Example command execution**:

```bash
# Generate ADKAR assessment for a stakeholder group
python3 skills/change-management-consultant/scripts/adkar_assessment.py \
  --stakeholder "Sales Team" \
  --awareness 8 --desire 4 --knowledge 2 --ability 0 --reinforcement 0

# Calculate change readiness score
python3 skills/change-management-consultant/scripts/readiness_calculator.py \
  --leadership 8 --culture 6 --capacity 5 --history 7 --resources 9
# Or use short flags: -l 8 -c 6 -a 5 -y 7 -r 9

# Generate stakeholder analysis from CSV
python3 skills/change-management-consultant/scripts/stakeholder_analyzer.py \
  --input stakeholders.csv --output stakeholder_analysis.md
```

---

## Resources

### References (loaded on-demand)
- `references/adkar_framework.md` - Detailed ADKAR model guidance
- `references/kotter_8_step.md` - Kotter's 8-Step Process reference
- `references/resistance_patterns.md` - Common resistance patterns and responses

### Scripts (executable automation)
- `scripts/adkar_assessment.py` - ADKAR scoring and gap analysis
- `scripts/readiness_calculator.py` - Change readiness score calculation
- `scripts/stakeholder_analyzer.py` - Stakeholder analysis from CSV input

### Assets (templates for output)
- `assets/change_plan_template.md` - Change management plan template
- `assets/communication_calendar_template.md` - Communication calendar template

---

## Core Frameworks

### 1. ADKAR Model（Prosci）

ADKAR is an individual change model that represents the five outcomes an individual needs to achieve for change to be successful.

```
A - Awareness（認識）: 変革の必要性の理解
D - Desire（意欲）: 変革への参加意欲
K - Knowledge（知識）: 変革の方法に関する知識
A - Ability（能力）: 変革を実行する能力
R - Reinforcement（強化）: 変革の定着化
```

**Application**:
For each individual or group affected by change, assess their current state against each ADKAR element and develop targeted interventions.

**Example Assessment**:
```
Current State:
- Awareness: 8/10 (understand why change is needed)
- Desire: 4/10 (skeptical about benefits)
- Knowledge: 2/10 (don't know how to use new system)
- Ability: 0/10 (haven't tried yet)
- Reinforcement: 0/10 (change not implemented)

Action: Focus on building Desire through benefits communication and addressing concerns.
```

### 2. Kotter's 8-Step Process

John Kotter's 8-step process for leading change, focused on organizational transformation.

```
1. 危機感を高める (Create Urgency)
2. 変革推進チームを作る (Build Guiding Coalition)
3. ビジョンと戦略を生み出す (Form Strategic Vision)
4. 変革のビジョンを周知徹底する (Enlist Volunteer Army)
5. 従業員の自発を促す (Enable Action by Removing Barriers)
6. 短期的成果を実現する (Generate Short-Term Wins)
7. 成果を生かして更なる変革を進める (Sustain Acceleration)
8. 新しい方法を企業文化に定着させる (Institute Change)
```

**Application**:
Use this sequential process for organization-wide transformations. Each step builds on the previous one.

### 3. Lewin's Change Model

Simple three-stage model: Unfreeze → Change → Refreeze

**Unfreeze**:
- Create awareness of the need for change
- Challenge the status quo
- Prepare for change

**Change**:
- Implement new processes, systems, behaviors
- Provide training and support
- Communicate frequently

**Refreeze**:
- Reinforce new behaviors
- Celebrate successes
- Update policies and procedures

---

## Core Workflows

### Workflow 1: Change Readiness Assessment

**Purpose**: Evaluate the organization's preparedness for change.

#### Step 1: Assess Organizational Factors

Evaluate the following dimensions:

**1. Leadership Commitment**
- Visible sponsorship from executives?
- Resources allocated?
- Leaders communicate importance?

**2. Past Change History**
- Previous change success rate?
- Lessons learned applied?
- Change fatigue present?

**3. Organizational Culture**
- Innovation vs. risk-averse?
- Open communication?
- Trust levels?

**4. Current State**
- Workload and capacity?
- Other competing initiatives?
- Stability of operations?

#### Step 2: Calculate Readiness Score

```
Readiness Score = Σ (Factor Weight × Factor Score) / 100

Example:
- Leadership Commitment (30%): 8/10
- Culture (25%): 6/10
- Capacity (20%): 5/10
- Past History (15%): 7/10
- Resources (10%): 9/10

Readiness Score = (30×8 + 25×6 + 20×5 + 15×7 + 10×9) / 100 = 6.8/10
```

**Interpretation**:
- 8-10: High readiness, proceed with confidence
- 6-7.9: Moderate readiness, address gaps before proceeding
- <6: Low readiness, significant preparation needed

#### Step 3: Develop Mitigation Plan

For low-scoring factors, develop targeted interventions:
- Low leadership commitment → Executive briefing, business case reinforcement
- Low capacity → Phased approach, additional resources
- Change fatigue → Quick wins, celebrate successes, reduce scope

---

### Workflow 2: Stakeholder Analysis and Engagement

**Purpose**: Identify, analyze, and engage stakeholders to build support.

#### Step 1: Identify Stakeholders

**Stakeholder Categories**:
- **Sponsors**: Executive leadership, project sponsors
- **Change Agents**: Managers, team leads, influencers
- **Target Groups**: End users affected by change
- **Support Functions**: IT, HR, Training, Communications

#### Step 2: Analyze Stakeholders

Use the **Power-Interest Matrix**:

```
        High Power
         │
  Keep   │  Manage
Satisfied│  Closely
         │
  ───────┼───────
         │
Monitor  │  Keep
         │ Informed
         │
       Low Interest
```

And **Impact-Influence Matrix**:

```
       High Impact
         │
 Partner │ Engage
 Closely │Proactively
         │
  ───────┼───────
         │
 Monitor │  Inform
         │
       Low Influence
```

#### Step 3: Assess Individual Attitudes

**Stakeholder Attitude Spectrum**:
```
Champion → Supporter → Neutral → Skeptic → Resistor
   (5)        (4)        (3)       (2)       (1)
```

**Example Stakeholder Map**:
```
| Stakeholder | Power | Interest | Impact | Attitude | Strategy |
|-------------|-------|----------|--------|----------|----------|
| CEO         | High  | Medium   | High   | 4        | Keep Satisfied, Regular Updates |
| CIO         | High  | High     | High   | 5        | Manage Closely, Partnership |
| Dept Manager| Medium| High     | High   | 2        | Convert Skeptic, Address Concerns |
| End Users   | Low   | High     | Medium | 3        | Keep Informed, Training |
```

#### Step 4: Develop Engagement Strategy

For each stakeholder group:

**Champions (5)**:
- Leverage as change agents
- Ask to advocate and influence others
- Involve in planning and decision-making

**Supporters (4)**:
- Keep engaged and informed
- Provide recognition
- Ask for feedback

**Neutral (3)**:
- Educate on benefits
- Provide information
- Move towards support

**Skeptics (2)**:
- Listen to concerns
- Address objections with data
- Provide early involvement
- Show quick wins

**Resistors (1)**:
- Understand root causes of resistance
- One-on-one engagement
- May need to isolate if unchangeable
- Focus on "what's in it for me" (WIIFM)

---

### Workflow 3: Communication Planning

**Purpose**: Develop a comprehensive communication strategy to support change.

#### Step 1: Define Communication Objectives

**Awareness**: Make stakeholders aware of the change
**Understanding**: Explain why the change is necessary
**Buy-in**: Build support and address concerns
**Action**: Guide stakeholders on what to do
**Reinforcement**: Sustain new behaviors

#### Step 2: Segment Audiences

**Audience Segmentation Criteria**:
- Level in organization (Executive, Manager, Staff)
- Department/Function
- Impact level (High, Medium, Low)
- Role in change (Sponsor, Change Agent, Target)

#### Step 3: Select Communication Channels

**Channel Selection Matrix**:

| Channel | Richness | Reach | Feedback | Best For |
|---------|----------|-------|----------|----------|
| Town Hall | High | High | Medium | Launch, Major Milestones |
| Email | Low | High | Low | Updates, Instructions |
| Video Message | Medium | High | Low | Executive Messages |
| Department Meeting | High | Medium | High | Detailed Discussion |
| One-on-One | Very High | Low | Very High | Resistance, Concerns |
| Intranet | Low | High | Low | Reference, FAQs |
| Newsletter | Low | High | Low | Regular Updates |
| Workshops | High | Medium | High | Training, Engagement |

#### Step 4: Create Communication Calendar

**Example Communication Plan**:

```markdown
| Date | Audience | Message | Channel | Owner |
|------|----------|---------|---------|-------|
| Week 1 | All Staff | Change Announcement | Email + Town Hall | CEO |
| Week 2 | Managers | Detailed Impact | Workshop | Change Team |
| Week 3 | End Users | "What's Changing for You" | Department Meetings | Managers |
| Week 4 | All Staff | FAQs and Support | Intranet + Email | Communications |
| Ongoing | All Staff | Weekly Progress Updates | Newsletter | Change Team |
```

#### Step 5: Key Message Development

**Message Framework**:

**Awareness Messages**:
- What is changing?
- When is it happening?
- Who is affected?

**Understanding Messages**:
- Why are we changing?
- What are the benefits?
- What happens if we don't change?

**Buy-in Messages**:
- What's in it for me? (WIIFM)
- How will this make my job easier?
- Success stories and testimonials

**Action Messages**:
- What do I need to do?
- Where can I get training?
- Who can I ask for help?

**Reinforcement Messages**:
- Celebrate successes
- Share progress metrics
- Recognize change champions

---

### Workflow 4: Resistance Management

**Purpose**: Identify, understand, and address resistance to change.

#### Step 1: Identify Sources of Resistance

**Common Resistance Sources**:

1. **Loss of Control**
   - Symptom: "I wasn't consulted"
   - Response: Increase participation, seek input

2. **Uncertainty**
   - Symptom: "What will happen to me?"
   - Response: Provide clear information, reduce ambiguity

3. **Loss of Face**
   - Symptom: "This means I was doing it wrong"
   - Response: Honor the past, "evolving" not "fixing"

4. **Competence Concerns**
   - Symptom: "I don't know how to do this"
   - Response: Training, support, practice time

5. **More Work**
   - Symptom: "I'm already busy"
   - Response: Acknowledge workload, provide resources, show efficiency gains

6. **Past Resentments**
   - Symptom: "Last time this failed"
   - Response: Acknowledge past, show what's different

#### Step 2: Assess Resistance Level

**Resistance Intensity Scale**:
```
1 - Passive Resistance: Silent, not participating
2 - Verbal Resistance: Complaints, skepticism
3 - Active Resistance: Arguing, refusing to participate
4 - Aggressive Resistance: Sabotage, undermining
```

#### Step 3: Apply Resistance Management Strategies

**For Passive Resistance**:
- One-on-one conversations
- Ask open-ended questions
- Listen actively
- Provide safe space to express concerns

**For Verbal Resistance**:
- Acknowledge concerns as valid
- Provide data and evidence
- Address specific objections
- Involve in solution design

**For Active Resistance**:
- Set clear expectations
- Consequences for non-participation
- Offer coaching and support
- Consider role changes if necessary

**For Aggressive Resistance**:
- Immediate intervention by leadership
- Formal performance management
- Isolation from change-critical roles
- Last resort: organizational separation

#### Step 4: Convert Resistors

**Conversion Tactics**:

1. **Listen First**: Understand root causes
2. **Empathize**: "I understand why you feel that way"
3. **Educate**: Provide factual information
4. **Involve**: Give them a role in the change
5. **Pilot**: Let them try it on small scale
6. **Peer Influence**: Connect with supporters
7. **Quick Wins**: Show early successes
8. **WIIFM**: Focus on personal benefits

---

### Workflow 5: Training and Capability Building

**Purpose**: Ensure stakeholders have the knowledge and skills to succeed in the new state.

#### Step 1: Conduct Training Needs Analysis

**Assessment Questions**:
- What new skills are required?
- What is the current skill level?
- What is the skill gap?
- How many people need training?
- What is the urgency?

**Training Needs Matrix**:

```
| Role | Current State | Future State | Gap | Training Need |
|------|---------------|--------------|-----|---------------|
| Manager | Excel-based reports | BI Dashboard | High | 2-day workshop |
| Analyst | Manual data entry | Automated ETL | Medium | 1-day training |
| Executive | Email reports | Real-time dashboard | Low | 1-hour orientation |
```

#### Step 2: Design Training Program

**70-20-10 Learning Model**:
- **70% On-the-job**: Hands-on practice, job shadowing
- **20% Coaching**: Mentoring, peer learning
- **10% Formal Training**: Classroom, e-learning

**Training Delivery Methods**:
- **Instructor-Led Training (ILT)**: Classroom, workshop
- **E-Learning**: Online courses, videos
- **Job Aids**: Quick reference guides, cheat sheets
- **Hands-on Labs**: Practice environments
- **Train-the-Trainer**: Build internal capability

#### Step 3: Develop Training Materials

**Essential Training Assets**:

1. **Training Manual**: Step-by-step procedures
2. **Quick Reference Guide**: 1-2 page cheat sheet
3. **Video Tutorials**: Screen recordings for common tasks
4. **FAQ Document**: Answers to common questions
5. **Practice Exercises**: Hands-on activities
6. **Assessment**: Quiz or practical test

#### Step 4: Execute Training

**Training Rollout Best Practices**:

**Before Training**:
- Send pre-work materials
- Confirm attendance
- Prepare training environment

**During Training**:
- Start with "why" (benefits)
- Hands-on practice
- Allow questions
- Real-world examples

**After Training**:
- Provide job aids
- Follow-up support
- Refresher sessions
- Measure effectiveness

#### Step 5: Provide Ongoing Support

**Support Mechanisms**:
- **Help Desk**: Dedicated support team
- **Champions Network**: Peer supporters
- **Office Hours**: Drop-in Q&A sessions
- **Knowledge Base**: Self-service documentation
- **Feedback Loop**: Continuous improvement

---

### Workflow 6: Change Metrics and Measurement

**Purpose**: Track progress and measure change success.

#### Key Change Metrics

**Leading Indicators** (predict future success):
- Stakeholder engagement scores
- Training completion rates
- Communication effectiveness
- Resistance levels
- Change readiness scores

**Lagging Indicators** (measure actual outcomes):
- User adoption rates
- Performance metrics (productivity, quality)
- Business results (cost savings, revenue)
- Employee satisfaction
- Customer satisfaction

#### Measurement Framework

**Adoption Curve Tracking**:

```
Adoption %
   │
100│                    ........
   │                 ...
 75│              ...
   │           ...
 50│        ...
   │     ...
 25│   ..
   │ ..
  0│.
   └────────────────────────────> Time
    Launch  +1mo  +2mo  +3mo  +6mo
```

**Target**: 80% adoption within 3 months

**Usage Metrics**:
- Login frequency
- Feature utilization
- Process compliance
- Error rates

#### Reporting

**Dashboard Example**:

```markdown
## Change Management Dashboard

### Overall Status: 🟡 On Track with Risks

### Key Metrics:
- Training Completion: 85% ✅
- User Adoption: 65% 🟡 (Target: 75%)
- Stakeholder Support: 72% ✅
- Resistance Index: 18% 🟡 (Target: <15%)

### Progress This Week:
- ✅ Completed Department A rollout
- ✅ Resolved top 5 user issues
- 🟡 Department B resistance higher than expected

### Next Week Focus:
- Targeted resistance management in Dept B
- Refresher training for early adopters
- Executive steering committee review
```

---

## Deliverable Templates

### 1. Change Management Plan

```markdown
# Change Management Plan: [Project Name]

## Executive Summary
[One-page overview of change scope, impact, and strategy]

## Change Overview
- **What is Changing**: [Description]
- **Why**: [Business drivers, benefits]
- **Who is Affected**: [Stakeholder groups and impact levels]
- **When**: [Timeline and phases]

## Change Readiness Assessment
- Overall Readiness Score: X.X/10
- Key Risks: [Top 3-5 risks]
- Mitigation Strategies: [Actions to improve readiness]

## Stakeholder Analysis
[Stakeholder map with engagement strategies]

## Communication Plan
[Detailed communication calendar and key messages]

## Training Plan
[Training needs, approach, and schedule]

## Resistance Management Strategy
[Anticipated resistance and response plans]

## Success Metrics
[KPIs and targets]

## Governance
- **Steering Committee**: [Members and meeting frequency]
- **Change Network**: [Change agents and champions]
- **Decision Authority**: [Escalation path]

## Budget
[Estimated costs for training, communication, resources]

## Timeline
[Gantt chart or phase diagram]
```

### 2. Stakeholder Engagement Plan

```markdown
# Stakeholder Engagement Plan

| Stakeholder Group | Power | Interest | Attitude | Engagement Strategy | Owner | Frequency |
|-------------------|-------|----------|----------|---------------------|-------|-----------|
| Executive Team | High | Medium | Supporter | Monthly steering committee | Change Lead | Monthly |
| Department Managers | Medium | High | Mixed | Weekly check-ins, workshops | Change Agents | Weekly |
| End Users | Low | High | Neutral | Training, office hours, newsletters | Trainers | Ongoing |
| IT Support | Medium | High | Champion | Partnership, co-design | IT Lead | As needed |
```

### 3. Communication Calendar

```markdown
# Communication Calendar: [Project Name]

| Week | Date | Audience | Message Theme | Channel | Owner | Status |
|------|------|----------|---------------|---------|-------|--------|
| -2 | [Date] | Executives | Pre-launch briefing | Executive meeting | Sponsor | ✅ |
| 0 | [Date] | All Staff | Change announcement | Town Hall + Email | CEO | ✅ |
| 1 | [Date] | Managers | Manager toolkit | Workshop | Change Team | 🔄 |
| 2 | [Date] | End Users | What's changing for me | Dept meetings | Managers | Pending |
| 3 | [Date] | All Staff | Training schedule | Email + Intranet | Training Team | Pending |
| Ongoing | Weekly | All Staff | Progress updates | Newsletter | Comms Team | Ongoing |
```

---

## Best Practices

### 1. Start Early
Begin change management at project initiation, not just before go-live.

### 2. Secure Executive Sponsorship
Visible, active sponsorship is the #1 success factor.

### 3. Focus on WIIFM
People support change when they understand "What's In It For Me."

### 4. Build a Change Network
Identify and empower change agents across the organization.

### 5. Communicate, Communicate, Communicate
Over-communication is better than under-communication.

### 6. Address Resistance Directly
Don't ignore resistors—engage them early and often.

### 7. Celebrate Quick Wins
Show early successes to build momentum.

### 8. Provide Adequate Training
Insufficient training is a top cause of change failure.

### 9. Measure and Adjust
Track metrics and be willing to pivot based on feedback.

### 10. Sustain the Change
Reinforcement is key—don't declare victory too early.

---

## Common Pitfalls

### ❌ Starting Change Management Too Late
- **Problem**: Change activities begin weeks before go-live
- **Solution**: Integrate change management from day one

### ❌ Underestimating Resistance
- **Problem**: "Our people will love this change"
- **Solution**: Assume resistance and plan accordingly

### ❌ Insufficient Training
- **Problem**: One-hour training for complex system
- **Solution**: Adequate time, hands-on practice, ongoing support

### ❌ Poor Communication
- **Problem**: One-time announcement, then silence
- **Solution**: Frequent, multi-channel, two-way communication

### ❌ Ignoring Middle Management
- **Problem**: Focus only on executives and end users
- **Solution**: Engage and equip managers as change agents

### ❌ No Metrics
- **Problem**: Can't measure progress or success
- **Solution**: Define KPIs upfront and track consistently

---

## Integration with ITIL 4

Change Management Consultant skill complements ITIL 4 practices:

### Organizational Change Management ↔ ITIL 4 Practices

**Relationship Management**:
- Stakeholder engagement aligns with relationship management
- Communication plans support service relationship management

**Service Level Management**:
- Training ensures teams can meet new SLAs
- Change readiness affects service delivery

**Knowledge Management**:
- Training materials feed into knowledge base
- Change FAQs become organizational knowledge

**Continual Improvement**:
- Change metrics inform improvement opportunities
- Lessons learned drive future change effectiveness

### DevOps and Agile

**Change Enablement**:
- Organizational change management supports technical change
- User adoption for new CI/CD practices

**Agile Transformation**:
- ADKAR for adopting agile mindset
- Training for scrum/kanban practices

---

## Tools and Resources

### Stakeholder Management
- Stakeholder maps (Excel, PowerPoint)
- Prosci ADKAR tools
- Survey tools (SurveyMonkey, Qualtrics)

### Communication
- Email campaigns (Mailchimp, SendGrid)
- Intranet (SharePoint, Confluence)
- Video (Loom, Camtasia)

### Training
- LMS (Moodle, TalentLMS, Cornerstone)
- E-learning authoring (Articulate, Adobe Captivate)
- Screen recording (Loom, Camtasia)

### Project Management
- Change tracking (Jira, Asana, Monday.com)
- Collaboration (Miro, Mural, Microsoft Teams)

---

このスキルの目的は、組織変革を成功に導き、新しいシステム、プロセス、文化を定着させることです。ADKAR、Kotter、その他のフレームワークを活用し、ステークホルダーを巻き込み、抵抗を管理し、継続的な改善を実現してください。
