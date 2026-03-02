---
layout: default
title: English
nav_order: 1
has_children: true
lang_peer: /ja/
permalink: /en/
---

<div class="hero">
  <div class="hero-tagline">Claude Skills Library</div>
  <p class="hero-mantra">78 professional skills to extend Claude Code across every domain</p>
</div>

## What is Claude Skills Library?

Claude Skills Library is an open-source collection of **78 ready-to-use skills** that extend [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with specialized knowledge, workflows, and automation scripts. Each skill is a self-contained package you can install in seconds -- no configuration required.

Skills cover everything from code review and data science to compliance advisory, financial analysis, and project management. Whether you are a solo developer or part of an enterprise team, there is a skill to accelerate your work.

---

## Skill Categories

<div class="category-cards">

  <a href="{{ '/en/skill-catalog/#software-development--it' | relative_url }}" class="category-card" style="text-decoration:none;color:inherit;">
    <h3>Software Development & IT</h3>
    <p>16 skills -- Code review, TDD, data science, cloud CLI, debugging, and more.</p>
  </a>

  <a href="{{ '/en/skill-catalog/#project--business' | relative_url }}" class="category-card" style="text-decoration:none;color:inherit;">
    <h3>Project & Business</h3>
    <p>18 skills -- Strategy, M&A, pricing, project planning, management accounting.</p>
  </a>

  <a href="{{ '/en/skill-catalog/#operations--documentation' | relative_url }}" class="category-card" style="text-decoration:none;color:inherit;">
    <h3>Operations & Documentation</h3>
    <p>10 skills -- Technical writing, presentations, PDF conversion, meeting minutes.</p>
  </a>

  <a href="{{ '/en/skill-catalog/#compliance-finance--governance' | relative_url }}" class="category-card" style="text-decoration:none;color:inherit;">
    <h3>Compliance, Finance & Governance</h3>
    <p>12 skills -- SOX, ISO, PCI DSS, ESG, audit, financial analysis.</p>
  </a>

  <a href="{{ '/en/skill-catalog/#qa-testing--vendor-management' | relative_url }}" class="category-card" style="text-decoration:none;color:inherit;">
    <h3>QA, Testing & Vendor Management</h3>
    <p>9 skills -- UAT, migration QA, vendor estimates, helpdesk, CX analysis.</p>
  </a>

</div>

---

## Get Started in 3 Steps

<div class="steps">

  <div class="step">
    <div class="step-number">1</div>
    <h4>Install Claude Code</h4>
    <p>Set up the Claude Code CLI on your machine.</p>
  </div>

  <div class="step">
    <div class="step-number">2</div>
    <h4>Copy a Skill</h4>
    <p><code>cp -r ./skills/skill-name ~/.claude/skills/</code></p>
  </div>

  <div class="step">
    <div class="step-number">3</div>
    <h4>Use It</h4>
    <p>Claude automatically detects installed skills and applies them when relevant.</p>
  </div>

</div>

[Getting Started Guide]({{ '/en/getting-started/' | relative_url }}){: .btn .btn-primary }

---

## Featured Skills

| Skill | Category | Highlights |
|:------|:---------|:-----------|
| [critical-code-reviewer]({{ '/en/skills/dev/critical-code-reviewer/' | relative_url }}) | Dev | 4-persona parallel code review |
| [data-scientist]({{ '/en/skills/dev/data-scientist/' | relative_url }}) | Dev | Auto EDA, ML model comparison, time-series |
| [project-plan-creator]({{ '/en/skills/management/project-plan-creator/' | relative_url }}) | PM | PMBOK charter, WBS, Gantt, RACI |
| [financial-analyst]({{ '/en/skills/finance/financial-analyst/' | relative_url }}) | Finance | DCF, NPV/IRR, comparable analysis |
| [markdown-to-pdf]({{ '/en/skills/ops/markdown-to-pdf/' | relative_url }}) | Ops | Professional PDF with Mermaid diagrams |

[Browse All 78 Skills]({{ '/en/skill-catalog/' | relative_url }}){: .btn }
