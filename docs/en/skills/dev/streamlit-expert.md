---
layout: default
title: "Streamlit Expert"
grand_parent: English
parent: Software Development
nav_order: 31
lang_peer: /ja/skills/dev/streamlit-expert/
permalink: /en/skills/dev/streamlit-expert/
---

# Streamlit Expert
{: .no_toc }

Streamlit Web application development expert skill. Provides guidance on OIDC authentication (st.login/st.logout/st.user), secrets management, data visualization with Plotly/Altair, performance optimization with caching, and modern Streamlit features (v1.42-1.52+). Use this skill when building Streamlit apps, implementing user authentication, creating data dashboards, or optimizing app performance. Triggers include "streamlit app", "st.login", "data dashboard", "streamlit authentication", "streamlit visualization".
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/streamlit-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/streamlit-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Streamlit Web application development expert skill supporting the latest features from v1.42 to v1.52+ (2025-2026). Provides comprehensive guidance on:

- **Authentication**: Native OIDC authentication with `st.login()`, `st.logout()`, `st.user`
- **Data Visualization**: Optimal library selection (Plotly, Altair, native charts) and performance tuning
- **Secrets Management**: Secure credential handling with `st.secrets`
- **Performance Optimization**: Caching strategies, large dataset handling, session state management
- **Modern Features**: Custom themes, layout containers, multipage apps, Custom Components v2

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

```bash
User Request
├── "Add authentication" → Authentication Workflow
├── "Create dashboard/visualization" → Visualization Workflow
├── "App is slow/optimize" → Performance Optimization Workflow
├── "New Streamlit app" → Project Setup Workflow
└── "Deploy app" → Deployment Workflow
```

---

## 4. How It Works

```
User Request
├── "Add authentication" → Authentication Workflow
├── "Create dashboard/visualization" → Visualization Workflow
├── "App is slow/optimize" → Performance Optimization Workflow
├── "New Streamlit app" → Project Setup Workflow
└── "Deploy app" → Deployment Workflow
```

---

## 5. Usage Examples

- Building new Streamlit applications from scratch
- Implementing user authentication with OIDC providers (Google, Microsoft, Okta, Auth0)
- Creating data visualization dashboards
- Optimizing Streamlit app performance
- Managing secrets and credentials securely
- Implementing modern Streamlit features (v1.42+)

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 4 guide file(s).
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/streamlit-expert/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: visualization_best_practices.md, release_notes_summary.md, authentication_guide.md.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/dev/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- Confirm the expected Python version and required packages are installed in the active environment.

---

## 10. Reference

**References:**

- `skills/streamlit-expert/references/authentication_guide.md`
- `skills/streamlit-expert/references/performance_optimization.md`
- `skills/streamlit-expert/references/release_notes_summary.md`
- `skills/streamlit-expert/references/visualization_best_practices.md`
