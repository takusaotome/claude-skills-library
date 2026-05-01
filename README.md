# Claude Skills Library

A collection of professional Claude Code skills for various domains and use cases.

## Overview

This repository contains custom skills designed to extend Claude's capabilities with specialized knowledge, workflows, and tools. Each skill is self-contained and follows best practices for skill development.

## Repository Structure

```
claude-skills-library/
├── skills/                 # 103 published skills (with SKILL.md) + 3 in-progress directories with only scripts/ — 106 dirs total
│   ├── data-scientist/
│   ├── project-manager/
│   ├── business-analyst/
│   └── ...
├── agents/                 # Agent definitions (18 agents)
│   ├── code-reviewer-bug-hunter.md
│   ├── document-reviewer-customer.md
│   └── ...
├── hooks/                  # Claude Code hook configurations
│   ├── current-datetime.json
│   └── notification-sound-macos.json
├── commands/               # Slash commands for Claude Code
│   └── clarify.md
├── skill-packages/         # Packaged .skill files for distribution
├── docs/                   # Additional documentation
└── README.md
```

## Hooks

Useful hook configurations for Claude Code. See [hooks/README.md](hooks/README.md) for details.

| Hook | Purpose |
|------|---------|
| `current-datetime.json` | Prevents Claude from confusing today's date |
| `notification-sound-macos.json` | Plays sound on notifications (macOS) |

## Commands

Slash commands for Claude Code workflows.

| Command | Purpose | Usage |
|---------|---------|-------|
| `/clarify` | Clarify plan ambiguities through structured Q&A | `/clarify [plan-file-path]` |

### `/clarify` - Plan Clarification

Resolves ambiguities in plan files through structured questioning using the AskUserQuestion tool.

**Features**:
- Detects vague language, missing specs, undefined constraints
- 2-4 questions per round with pros/cons options
- Records decisions with rationale and owner
- Updates plan file with decisions appendix
- Maximum 5 rounds (prevents infinite loops)

**Installation**: Copy `commands/clarify.md` to `~/.claude/commands/`

## Skill Catalog (103 Skills)

> Note: `skills/` contains 106 directories total — 103 published skills (with `SKILL.md`) listed below, plus 3 in-progress directories that only contain `scripts/` and are not yet ready for publication: `ai-bpo-proposal-generator`, `email-inbox-triager`, `email-triage-responder`.

### Business Strategy & Consulting (17 skills)

| Skill Name | Description | Key Features |
|------------|-------------|--------------|
| ai-adoption-consultant | AI/LLM活用提案、業界・部門別導入戦略 | 5 Industries, 5 Functions, ROI Analysis |
| business-analyst | BABOK準拠のビジネス分析、要件定義 | Stakeholder Analysis, BRD Templates |
| business-plan-creator | 事業計画書の体系的作成、収支シミュレーション | 5-Phase Workflow, Financial Modeling, Industry Templates |
| competitive-intelligence-analyst | 競合分析、バトルカード、Win/Loss分析 | Battlecards, Market Landscape |
| executive-briefing-writer | 経営層向け資料作成、So What分析 | Board Reports, Investor Briefings |
| m-and-a-advisor | M&Aアドバイザリー、DD、PMI計画 | Valuation, Due Diligence, PMI |
| pricing-strategist | 価格戦略、価格弾力性分析 | Value-Based Pricing, Price Testing |
| strategic-planner | 事業戦略立案、SWOT、シナリオ分析 | Strategy Canvas, Scenario Planning |
| design-thinking | デザイン思考プロセス支援 | 5-Phase Process, Empathy Maps |
| lean-six-sigma-consultant | リーンシックスシグマ、プロセス改善 | DMAIC, Value Stream Mapping |
| kpi-designer | KPI設計・パフォーマンス測定 | SMART KPIs, Dashboard Design |
| patent-analyst | 特許分析・IP戦略 | Prior Art Search, Patent Landscape |
| management-accounting-navigator | 管理会計ナビゲーター（12領域ルーティング） | COSO/IMA Framework, Domain Classification |
| ma-budget-actual-variance | 予算実績差異分析 | 有利/不利差異判定, Price/Quantity分解, CSV分析 |
| ma-cvp-break-even | CVP・損益分岐点分析 | Break-Even, Margin of Safety, Multi-Product |
| ma-standard-cost-variance | 標準原価差異分析 | Price/Quantity Variance, 材料費/労務費/間接費 |
| hearing-to-requirements-mapper | ヒアリングシート→要件定義書変換、ギャップ分析 | RTM, WBS Mapping, Ambiguity Detection, Bilingual |

### Project Management (7 skills)

| Skill Name | Description | Key Features |
|------------|-------------|--------------|
| action-status-updater | アクションアイテム状態管理、自然言語更新 | NL Parsing (JP/EN), Status Tracking, daily-comms-ops Integration |
| project-manager | PMBOK準拠PM、EVM分析、リスク管理 | 10 Knowledge Areas, EVM Metrics |
| project-plan-creator | プロジェクト計画書・WBS・ガント作成 | Charter, WBS, Gantt, RACI |
| project-completeness-scorer | プロジェクト完成度評価、重み付きスコアリング | 5 Dimensions, Gap Analysis, 4 Templates |
| project-artifact-linker | プロジェクト成果物のトレーサビリティ・クロスリファレンス | WBS↔Meeting↔Requirements Linking, Gap Detection |
| project-kickoff-bootstrapper | Claude用kickoff文脈・テンプレート導入、プロジェクト初期設定 | CLAUDE.md Scaffolding, 15 Templates, 3 Install Profiles |
| wbs-review-assistant | WBS・要件ドキュメント照合レビュー | Excel Annotation, Gap Analysis, Traceability Matrix |

### Software Development & IT (21 skills)

| Skill Name | Description | Key Features |
|------------|-------------|--------------|
| codex-reviewer | OpenAI Codexによるレビュー依頼 | GPT-5.1-Codex-Max Integration |
| critical-code-reviewer | 多角的コードレビュー | Multi-Persona Review |
| data-scientist | データ分析・ML・時系列予測 | Auto EDA, Model Comparison |
| data-visualization-expert | データ可視化、チャート設計 | 30+ Chart Types, Accessibility |
| design-implementation-reviewer | 設計・実装の整合性レビュー | Bug Hunting, Correctness Focus |
| duckdb-expert | DuckDBによる大規模データ分析 | SQL Optimization, File Formats |
| log-debugger | ログ分析・RCA・デバッグ | Log Patterns, Root Cause Analysis |
| multi-file-log-correlator | 複数ログファイルの相関分析・統合タイムライン | Cross-Source Correlation, Gap Detection |
| streamlit-expert | Streamlit Webアプリ開発支援 | OIDC Auth, Plotly/Altair, Caching |
| tdd-developer | TDD開発支援 | Red-Green-Refactor Cycle |
| it-system-roi-analyzer | IT投資ROI分析・TCO計算 | ROI, TCO, NPV, Payback |
| aws-cli-expert | AWS CLIコマンド生成 | EC2, S3, Lambda, IAM |
| render-cli-expert | Render CLIによるデプロイ管理 | Deploys, Logs, PostgreSQL |
| gogcli-expert | gogcli（Google Workspace CLI）操作支援 | 13 Services, OAuth2, Multi-Account |
| network-diagnostics | ネットワーク品質診断・ボトルネック特定 | Ping/Speed/HTTP/Traceroute, Cross-Platform |
| network-incident-analyzer | ネットワークログ分析・障害検出・原因分析 | Multi-Format Parsing, Anomaly Detection, Correlation |
| office-script-expert | Office Scripts（Excel Online）開発支援 | ExcelScript API, 13 Bug Patterns, lib/Testing |
| incident-rca-specialist | インシデントRCA・是正措置計画 | 5 Whys, Fishbone, FTA, 3D Prevention |
| timezone-aware-event-tracker | マルチタイムゾーンイベント追跡・相関分析 | DST Handling, Multi-TZ Timeline, Event Correlation |
| hidden-contract-investigator | 既存コードの暗黙契約抽出・再利用リスク可視化 | 6-Category Mismatch Taxonomy, Reuse Risk Classification |
| safe-by-default-architect | 危険パターン禁止・安全デフォルト設計標準 | Safe Pattern Catalog, Forbidden-to-Safe Mapping, Static Rules |

### Salesforce (4 skills)

| Skill Name | Description | Key Features |
|------------|-------------|--------------|
| salesforce-cli-expert | Salesforce CLIコマンド生成 | SOQL, Metadata, Security Audit |
| salesforce-expert | Salesforce開発・運用・トラブルシュート | Sharing, Apex, LWC, Architecture |
| salesforce-flow-expert | Flow実装・検証・デプロイ自動化 | Validation, Metadata Gen, Deploy |
| salesforce-report-creator | SF CLIでレポート作成・デプロイ | Report Types, REST/Metadata API |

### Media Processing Tools (5 skills)

| Skill Name | Description | Key Features |
|------------|-------------|--------------|
| ffmpeg-expert | FFmpegによる動画・音声処理 | Encoding, Filters, Streaming |
| imagemagick-expert | ImageMagickによる画像処理 | Convert, Resize, Effects |
| qr-code-generator | QRコード画像生成（URL/テキスト/vCard） | Customization, Batch Generation, Color Support |
| sox-expert | SoXによる音声処理 | Audio Effects, Format Conversion |
| yt-dlp-expert | yt-dlpによる動画ダウンロード | Download, Extract, Subtitles |

### Documentation & Communication (17 skills)

| Skill Name | Description | Key Features |
|------------|-------------|--------------|
| ai-text-humanizer | AI生成テキストのAI臭検出・人間化リライト | 6-Pattern Detection, 0-100 Scoring, 3 Humanization Techniques |
| bug-ticket-creator | バグチケット作成支援 | CLEAR Principles, Severity/Priority |
| critical-document-reviewer | ドキュメント批評レビュー | Multi-Persona Review |
| docling-converter | ドキュメント形式変換 | PDF, DOCX, Markdown |
| fujisoft-presentation-creator | FUJISOFT形式プレゼン作成 | MARP Templates, Corporate Style |
| markdown-to-pdf | Markdown→プロフェッショナルPDF | fpdf2, Playwright, Mermaid, Business Docs |
| video2minutes | 動画→文字起こし・議事録 | Transcription, Meeting Minutes |
| technical-spec-writer | 技術仕様書作成（画面/API/DB設計） | IEEE 830, Mermaid Diagrams, Traceability |
| operations-manual-creator | 操作マニュアル・SOP作成 | STEP Format, ANSI Z535, Troubleshooting |
| presentation-reviewer | プレゼン資料レビュー（聴衆視点） | 5 Evaluation Axes, Marp Compatibility |
| marp-layout-debugger | MARPレイアウト問題診断・自動修正 | Whitespace/Alignment/Bullet/Overflow/CSS Fix |
| codebase-onboarding-generator | CLAUDE.md自動生成（コードベース分析） | Project Detection, Command Extraction, Best Practices |
| meeting-asset-preparer | 会議資料準備（アジェンダ、決定ログ、アクション管理） | Bilingual (JA/EN), Context Integration, Decision Tracking |
| meeting-minutes-reviewer | 議事録レビュー・品質評価・フィードバック生成 | 5-Dimension Scoring, Action Item Validation, Consistency Check |
| meeting-minutes-writer | 議事録生成＋自己レビューループ（最大3反復） | 5 Mandatory Checks, Date Verification, Action-Item Coverage |
| internal-email-composer | 社内メール作成（見積依頼転送、タスク依頼、進捗報告） | JA/EN Bilingual, 6 Scenarios, Business Etiquette |
| iterative-design-assistant | デザイン反復履歴管理・文脈理解・一貫スタイリング | Design Decision Log, Contextual Reference Resolution, Token Management |

### QA & Testing (11 skills)

| Skill Name | Description | Key Features |
|------------|-------------|--------------|
| dual-axis-skill-reviewer | スキル品質レビュー（Auto+LLM二軸） | Deterministic Scoring, LLM Merge, Batch Review |
| migration-validation-explorer | データ移行検証・QAバックログ生成 | 4-Perspective Hypothesis, Priority Scoring |
| qa-bug-analyzer | バグデータ分析・品質トレンド | Quality Metrics, Trend Analysis |
| uat-testcase-generator | UATテストケース生成(Excel) | Excel Output, Traceability |
| helpdesk-responder | ヘルプデスク対応ドラフト作成 | KB-Based Responses, Confidence Scoring |
| cx-error-analyzer | CXエラーシナリオ分析・改善優先度付け | 6-Axis CX Scoring, Impact vs Effort Matrix |
| skill-idea-miner | セッションログからスキルアイデアを自動抽出・スコアリング | Session Log Mining, LLM Scoring, Backlog Management |
| skill-designer | アイデア仕様からスキル設計プロンプトを生成 | Design Prompt Generation, Repository Convention Compliance |
| completion-quality-gate-designer | 完了判定・品質ゲート・証跡・例外運用設計 | 7-Phase Gate Design, DoD Framework, Evidence Catalog |
| cross-module-consistency-auditor | 変更波及・横断整合性・コピペ展開監査 | Impact Map, Consistency Matrix, Copy Propagation Review |
| production-parity-test-designer | 本番同等テスト階層設計・盲点排除 | Test Tier Allocation, Smoke Suite, Adversarial Regression |

### Compliance & Governance (12 skills)

| Skill Name | Description | Key Features |
|------------|-------------|--------------|
| audit-control-designer | 統制設計書ドラフト自動生成 | 8 Control Templates, SoD Analysis, Assertion Mapping |
| audit-doc-checker | 監査ドキュメント品質レビュー（0-100スコア） | 12 Check Categories, Severity Scoring |
| bcp-planner | BCP（事業継続計画）策定支援 | Risk Assessment, Recovery Strategies |
| compliance-advisor | J-SOX/SOX、RCM、内部監査計画 | COSO Framework, Internal Audit |
| contract-reviewer | 契約書レビュー・リスク分析 | Risk Analysis, Clause Review |
| dama-dmbok | DMBOK準拠データ管理 | Data Governance, Quality |
| esg-reporter | ESG報告書作成支援 | GRI Standards, TCFD Alignment |
| internal-audit-assistant | 内部監査計画・実施支援 | Audit Planning, Sampling Methods |
| iso-implementation-guide | ISO規格実装ガイド | ISO 9001, 27001, 14001 |
| itil4-consultant | ITIL4コンサルティング | 34 Practices, Maturity Assessment |
| pci-dss-compliance-consultant | PCI DSS v4準拠支援 | Gap Analysis, SAQ Selection |
| financial-analyst | 財務分析・投資評価 | DCF, Comparable Analysis |

### Vendor Management (4 skills)

| Skill Name | Description | Key Features |
|------------|-------------|--------------|
| vendor-estimate-creator | 開発見積作成 | WBS, 4 Estimation Methods, ROI |
| vendor-estimate-reviewer | ベンダー見積レビュー・妥当性評価 | 12 Review Dimensions, 60+ Risk Factors |
| vendor-procurement-coordinator | RFQ送信〜見積受領〜クライアント見積作成の統合調整 | Email Automation, Response Tracking, Quote Comparison |
| vendor-rfq-creator | RFQ（見積依頼書）作成 | 150+ Checklist Items |

### HR Management (2 skills)

| Skill Name | Description | Key Features |
|------------|-------------|--------------|
| change-management-consultant | 組織変革マネジメント、チェンジ管理 | Kotter 8-Step, Stakeholder Engagement |
| talent-acquisition-specialist | JD作成、採用計画、面接評価 | JD Templates, Interview Evaluation |

### Operations & Supply Chain (3 skills)

| Skill Name | Description | Key Features |
|------------|-------------|--------------|
| supply-chain-consultant | サプライチェーン最適化、在庫管理 | Supply Chain Modeling, Optimization |
| production-schedule-optimizer | 製造施設の週次生産スケジュール最適化 | Greedy Bin-Packing, Staff Estimation, Shift Planning |
| shift-planner | 従業員別シフト自動編成、カバレッジ検証 | Greedy Assignment, Fairness Metrics, 30-min Coverage |

---

## Agent Catalog (15 Agents)

Agents are specialized sub-agents that can be spawned by Claude Code using the Task tool. They run autonomously and return results.

### Code Review Agents (4)

| Agent Name | Description |
|------------|-------------|
| code-reviewer-bug-hunter | Bug Hunter: 障害モード、エッジケース、並行性問題、影響範囲分析に特化 |
| code-reviewer-clean-code-expert | Clean Code: 命名、関数設計、可読性、SOLID原則に特化 |
| code-reviewer-tdd-expert | TDD Expert: テスト容易性、依存関係管理、リファクタリング安全性に特化 |
| code-reviewer-veteran-engineer | Veteran Engineer: 設計判断、アンチパターン、運用懸念、長期保守性に特化 |

### Document Review Agents (6)

| Agent Name | Description |
|------------|-------------|
| document-reviewer-customer | Customer Persona: 要件充足、理解容易性、期待値整合、ビジネス価値の観点 |
| document-reviewer-developer | Developer Persona: 技術的正確性、実装可能性、曖昧性、実務的懸念の観点 |
| document-reviewer-ops | Ops/SRE Persona: 監視、障害対応、運用負荷、保守性、キャパシティの観点 |
| document-reviewer-pm | PM Persona: リスク、一貫性、実現可能性、依存関係、プロジェクト影響の観点 |
| document-reviewer-qa | QA Persona: テスト可能性、受入基準明確性、エッジケース、異常系の観点 |
| document-reviewer-security | Security Persona: 認証・認可、データ保護、コンプライアンス、監査要件の観点 |

### Development & Analysis Agents (3)

| Agent Name | Description |
|------------|-------------|
| design-implementation-reviewer | コードが正しく動作するかの批評的レビュー（設計書との整合性ではなく実動作重視） |
| business-analyst | BABOK準拠のビジネス分析、要件抽出、ステークホルダー分析、プロセスマッピング |
| migration-validation-explorer | データ移行QA、隠れたリスク発見、検証仮説生成、QAバックログ作成 |

### Project & Vendor Management Agents (5)

| Agent Name | Description |
|------------|-------------|
| meeting-minutes-writer | 会議トランスクリプトから構造化された議事録を作成 |
| project-plan-creator | PMBOK準拠のプロジェクト計画書、WBS、ガントチャート、RACI作成 |
| vendor-estimate-creator | RFQから詳細な見積書（WBS、工数、コスト内訳、ROI分析）を作成 |
| vendor-estimate-reviewer | ベンダー見積の妥当性評価、リスク・ギャップ・レッドフラグの特定 |
| vendor-rfq-creator | 曖昧なクライアント要件から包括的なRFQ文書を作成 |

---

## Available Skills (Detailed)

### 📊 Data Scientist

**File:** `skill-packages/data-scientist.skill`

A comprehensive data science workflow skill for analyzing tabular and time series data.

**When to use:**
- Conducting exploratory data analysis (EDA)
- Building predictive models (classification, regression)
- Performing feature engineering and selection
- Time series analysis and forecasting
- Generating data-driven insights and reports

**Core Capabilities:**
- ✅ Automated EDA with quality assessment and visualizations
- ✅ Feature engineering strategies (10+ technique categories)
- ✅ Model comparison across multiple algorithms
- ✅ Time series analysis with stationarity tests and forecasting
- ✅ Professional visualization templates
- ✅ Statistical rigor and industry best practices

**Key Features:**

*Automated Scripts:*
- `auto_eda.py` - Comprehensive automated exploratory data analysis
- `model_comparison.py` - Train and compare 7-9 ML algorithms
- `timeseries_analysis.py` - Specialized time series analysis and forecasting

*Reference Guides:*
- `analysis_methodology.md` - 7-phase data science workflow
- `feature_engineering.md` - 10 categories of feature engineering techniques
- `evaluation_metrics.md` - Complete guide to model evaluation metrics
- `visualization_guide.md` - Data visualization patterns and best practices

*Templates:*
- `visualization_template.py` - Professional chart and graph functions
- `analysis_report_template.md` - Comprehensive analysis report structure

**Supported Problem Types:**
- Classification (binary and multi-class)
- Regression
- Time series forecasting
- Clustering analysis

**Example Use Cases:**
- "Analyze this sales data and find key drivers"
- "Build a model to predict customer churn"
- "Forecast next quarter's revenue based on historical data"
- "Compare different machine learning models for this classification problem"
- "Help me understand what features are most important"

**Domain-Specific Features:**
- Financial data analysis (technical indicators, ratios)
- E-commerce analytics (RFM, CLV, conversion metrics)
- Healthcare metrics (BMI, risk scores)

---

### 📋 Action Status Updater

**File:** `skill-packages/action-status-updater.skill`

A natural language action item tracking skill for managing status updates across communication channels.

**When to use:**
- Updating action item status via natural language (e.g., "Seanのメールには返信しておいた", "Delegated to Mike")
- Marking items as completed, delegated, deferred, or in-progress
- Tracking action items across email, Slack, meetings, and other channels
- Generating action item status reports
- Integrating with daily-comms-ops workflow

**Core Capabilities:**
- ✅ Natural language parsing for Japanese and English status updates
- ✅ Intent detection (completed, delegated, deferred, in-progress)
- ✅ Person and channel extraction from text
- ✅ Persistent YAML state with full history tracking
- ✅ Multiple export formats (daily-comms, slack, email)
- ✅ Fuzzy matching for description and person names

**Key Features:**

*Automated Scripts:*
- `action_status_updater.py` - CLI tool for action item management (init, add, update, report, export, list)
- `nl_parser.py` - Natural language parsing module for Japanese/English

*Reference Guides:*
- `status_patterns.md` - Comprehensive patterns for intent detection and target extraction
- `integration_guide.md` - Guide for daily-comms-ops workflow integration

**Supported Update Patterns:**
- Completed: 返信した, 完了, done, finished, sent
- Delegated: 〜に依頼, delegated to, assigned to
- Deferred: 延期, 来週, postponed, later
- In-Progress: 対応中, working on, in progress

**Example Use Cases:**
- "Seanのメールには返信しておいた" → Marks Sean's email action as completed
- "Delegated the report to Mike" → Marks report as delegated to Mike
- "Lu対応予定" → Marks item as delegated to Lu

---

### 📋 Project Manager

**File:** `skill-packages/project-manager.skill`

A comprehensive PMBOK®-aligned project management skill for professional project delivery.

**When to use:**
- Defining project requirements (ISO/IEC/IEEE 29148 compliant)
- Reviewing project plans against PMBOK best practices
- Generating progress reports with Earned Value Management (EVM)
- Conducting comprehensive risk assessments
- Estimating project costs using industry-standard methods
- Assessing project health and recommending corrective actions

**Core Capabilities:**
- ✅ Requirements engineering with traceability matrix
- ✅ Earned Value Management (SPI, CPI, EAC, ETC, VAC, TCPI)
- ✅ Three-phase risk management framework (14 categories, 9 risk types)
- ✅ Cost estimation (analogous, parametric, bottom-up, three-point)
- ✅ Project plan reviews across 10 PMBOK knowledge areas
- ✅ Stakeholder management and communication planning

**Key Features:**

*Automated Scripts:*
- `project_health_check.py` - Automated project health assessment with scoring

*Reference Guides:*
- `pmbok_knowledge_areas.md` - Comprehensive guide to all 10 PMBOK knowledge areas
- `risk_management_guide.md` - Three-phase risk management methodology

*Templates:*
- `requirements_definition_template.md` - ISO/IEC/IEEE 29148 compliant requirements documentation
- `progress_report_template.md` - EVM-based progress reporting with comprehensive metrics
- `risk_analysis_template.md` - Structured risk analysis with probability/impact assessment

**PMBOK Framework Coverage:**

*10 Knowledge Areas:*
1. Integration Management
2. Scope Management
3. Schedule Management
4. Cost Management
5. Quality Management
6. Resource Management
7. Communications Management
8. Risk Management
9. Procurement Management
10. Stakeholder Management

*5 Process Groups:*
1. Initiating
2. Planning
3. Executing
4. Monitoring & Controlling
5. Closing

**Example Use Cases:**
- "Create a requirements definition document for our CRM implementation"
- "Review this project plan and identify gaps and risks"
- "Generate a progress report with EVM analysis - our SPI is 0.85"
- "Conduct a comprehensive risk assessment for this legacy migration project"
- "Estimate project costs using bottom-up estimation"
- "Analyze our project health based on current metrics"

**Supported Methodologies:**
- Traditional (Waterfall) project management
- Agile project management with PMBOK
- Hybrid approaches

---

### 📊 Project Completeness Scorer

**File:** `skill-packages/project-completeness-scorer.skill`

A systematic project completeness evaluation skill that calculates weighted 0-100 scores across multiple dimensions.

**When to use:**
- Assessing project readiness for release or handoff
- Reviewing milestone deliverables against acceptance criteria
- Identifying gaps in code, documentation, or configuration
- Preparing for stakeholder reviews or gate approvals
- Scoring skill development projects within this repository

**Core Capabilities:**
- ✅ Multi-dimensional scoring (5 evaluation dimensions)
- ✅ Weighted scoring with customizable weights
- ✅ Gap identification with priority ranking
- ✅ Actionable next steps for each gap
- ✅ Project type templates (skill, webapp, library, document)

**Key Features:**

*Automated Scripts:*
- `score_project.py` - CLI tool for project evaluation with JSON/Markdown reports

*Reference Guides:*
- `scoring-methodology.md` - Detailed scoring rules and dimension definitions
- `project-templates.md` - Evaluation templates for different project types

**Evaluation Dimensions:**
- Functional Requirements (30%) - Core deliverables and features
- Quality Standards (20%) - Code quality, linting, formatting
- Test Coverage (25%) - Unit tests, integration tests
- Documentation (15%) - README, API docs, user guides
- Deployment Readiness (10%) - Config files, CI/CD, environment setup

**Project Templates:**
- `skill` - Claude Code skill projects
- `webapp` - Web applications (frontend/backend)
- `library` - Reusable libraries and packages
- `document` - Documentation-only projects
- `custom` - User-defined criteria from JSON file

**Example Use Cases:**
- "Score this skill project for completeness"
- "Evaluate our webapp before release"
- "Identify gaps in this library project"
- "Generate a completeness report for stakeholder review"

---

### 🔗 Project Artifact Linker

**File:** `skill-packages/project-artifact-linker.skill`

A comprehensive traceability and cross-referencing skill for project artifacts including WBS, meeting minutes, requirements, and decisions.

**When to use:**
- Tracing decisions back to the meetings where they were made
- Auditing project documentation for completeness and traceability
- Onboarding to a project and understanding decision history
- Preparing for project reviews with artifact linkage reports
- Extracting action items from meeting minutes and mapping to WBS tasks
- Generating compliance reports showing requirement-to-deliverable traceability
- Identifying orphaned artifacts (decisions without documentation, tasks without requirements)

**Core Capabilities:**
- Multi-document parsing (meetings, WBS, requirements, decisions)
- Automated link building with confidence scoring
- Bidirectional traceability matrix generation
- Gap detection for orphaned artifacts
- Overall health scoring for project traceability

**Key Features:**

*Automated Scripts:*
- `parse_artifacts.py` - Extract entities from project documents
- `link_artifacts.py` - Build cross-reference links between entities
- `generate_traceability_report.py` - Generate traceability matrix reports
- `analyze_coverage.py` - Identify gaps and orphaned artifacts

*Reference Guides:*
- `artifact_patterns.md` - Patterns for extracting entities from documents
- `link_heuristics.md` - Heuristics for establishing artifact links

**Link Types:**
- `action_item → wbs_task` - Action items mapped to implementing tasks
- `decision → requirement` - Decisions linked to requirements they address
- `meeting → wbs_task` - Meetings linked to tasks discussed
- `requirement → wbs_task` - Requirements traced to implementing tasks

**Example Use Cases:**
- "Parse all meeting minutes and link action items to WBS tasks"
- "Generate a traceability report for this project"
- "Find orphaned requirements without implementing tasks"
- "Show which decisions were made in which meetings"

---

### 🚀 Project Kickoff Bootstrapper

**File:** `skill-packages/project-kickoff-bootstrapper.skill`

新しいプロジェクトまたは既存リポジトリに Claude 用の kickoff 文脈（CLAUDE.md、docs/、.claude/rules/）を導入するスキル。リポジトリ証跡の自動検出とユーザー確認を組み合わせて、最小限の質問で最大限の文脈を整備する。

**When to use:**
- 新プロジェクト開始時に Claude の初期文脈を整備したい
- 既存リポジトリに後付けで CLAUDE.md と kickoff ドキュメント群を導入したい
- チーム間で完了判定やテスト方針の最低基準を揃えたい

**Key Features:**
- 8-phase bootstrap workflow (inspect → profile → question → resolve → create → extend → command → verify)
- 3 installation profiles (minimal, standard, full)
- 15 asset templates (CLAUDE.md, PROJECT_BRIEF, SKILL_ROUTING, QUALITY_GATES, TEST_STRATEGY, etc.)
- 6 reference guides (repository inspection, install profiles, question strategy, non-destructive update, consistency checklist, follow-on skill sequence)
- Non-destructive update policy for existing repositories
- Repository evidence inspection for auto-detection of stack, commands, and governance docs
- Follow-on skill recommendations (completion-quality-gate-designer, hidden-contract-investigator, etc.)

---

### 💼 Business Analyst

**File:** `skill-packages/business-analyst.skill`

A comprehensive BABOK®-aligned business analysis skill for professional requirements engineering and business process improvement.

**When to use:**
- Eliciting and documenting business requirements
- Conducting stakeholder analysis and engagement planning
- Analyzing and optimizing business processes
- Developing business cases with ROI/NPV analysis
- Performing gap analysis between current and future state
- Creating Business Requirements Documents (BRD)

**Core Capabilities:**
- ✅ Requirements elicitation with 6+ techniques (interviews, workshops, surveys, observation)
- ✅ Business process analysis with BPMN and value stream mapping
- ✅ Stakeholder analysis with Power/Interest matrix and RACI
- ✅ Business case development with financial analysis (ROI, NPV, IRR, Payback)
- ✅ Gap analysis with as-is/to-be process mapping
- ✅ Data quality assessment and profiling

**Key Features:**

*Automated Scripts:*
- `business_analysis.py` - Financial analysis, data profiling, and comparative analysis toolkit

*Reference Guides:*
- `babok_framework.md` - Complete BABOK® Guide v3 reference with 6 knowledge areas
- `process_data_analysis.md` - Process analysis and data assessment methodologies

*Templates:*
- `business_requirements_document_template.md` - ISO/IEC/IEEE 29148 compliant BRD
- `business_case_template.md` - Professional business case with financial analysis
- `stakeholder_analysis_template.md` - Comprehensive stakeholder management framework

**BABOK Framework Coverage:**

*6 Knowledge Areas:*
1. Business Analysis Planning & Monitoring
2. Elicitation & Collaboration
3. Requirements Life Cycle Management
4. Strategy Analysis
5. Requirements Analysis & Design Definition
6. Solution Evaluation

**Example Use Cases:**
- "Conduct stakeholder analysis for our digital transformation initiative"
- "Create a business case for automating our order processing system"
- "Document business requirements for the new customer portal"
- "Analyze our current sales process and identify optimization opportunities"
- "Perform gap analysis between current state and target operating model"
- "Profile this dataset to assess data quality for our analytics project"

**Supported Methodologies:**
- BABOK® Guide v3 standards
- Lean Six Sigma process improvement
- BPMN process modeling
- Value stream mapping
- MoSCoW prioritization

---

### 📊 Data Visualization Expert

**File:** `skill-packages/data-visualization-expert.skill`

A professional data visualization skill specialized in creating reader-friendly, accessible, and aesthetically pleasing charts and dashboards.

**When to use:**
- Creating any type of chart or graph
- Choosing the right visualization for your data
- Designing color schemes that work for everyone (including colorblind viewers)
- Creating executive dashboards or operational monitors
- Improving readability and aesthetic appeal of visualizations
- Preparing visualizations for presentations or reports
- Ensuring accessibility and WCAG compliance

**Core Capabilities:**
- ✅ Chart selection guidance (30+ chart types with decision trees)
- ✅ Colorblind-safe palettes (Okabe-Ito, Viridis, custom palettes)
- ✅ Professional dashboard design (Strategic, Operational, Analytical)
- ✅ Accessibility compliance (WCAG 2.1 standards)
- ✅ Story-driven visualization techniques
- ✅ Typography and layout principles
- ✅ Color theory and psychology

**Key Features:**

*Automated Scripts:*
- `create_visualization.py` - Command-line tool for creating professional charts (6 types: bar, line, scatter, heatmap, distribution, dashboard)

*Reference Guides:*
- `visualization_principles.md` - Design principles, color theory, typography, storytelling
- `chart_selection_guide.md` - Comprehensive guide to 30+ chart types with decision trees
- `dashboard_design.md` - Dashboard layout, KPI cards, interactivity patterns

*Templates & Assets:*
- `visualization_templates.py` - Ready-to-use Python templates (KPI cards, executive summaries, waterfall charts, etc.)
- `color_palettes.json` - 50+ professional color palettes (qualitative, sequential, diverging, business-specific, accessible)

**Visualization Workflows:**
1. Choosing the Right Chart Type
2. Applying Color Best Practices
3. Designing Professional Dashboards
4. Creating Story-Driven Visualizations
5. Ensuring Accessibility and Readability

**Example Use Cases:**
- "Create a bar chart comparing sales by region"
- "What's the best way to visualize this time series data?"
- "Design a dashboard showing our key metrics"
- "Choose colors that work for colorblind people"
- "Make this chart more readable for a presentation"
- "Create visualizations that tell a compelling story"

**Supported Chart Types:**
- Comparison: Bar, Lollipop, Bullet
- Distribution: Histogram, Box Plot, Violin Plot
- Relationship: Scatter, Line, Heatmap
- Composition: Stacked Bar, Tree Map, Waterfall
- Time Series: Line, Area, Sparkline
- Geographic: Choropleth, Symbol Map
- Hierarchy: Tree Map, Sunburst

**Accessibility Features:**
- Colorblind-safe palettes (red-green colorblindness)
- WCAG 2.1 contrast ratios (4.5:1 text, 3:1 graphics)
- Alternative text patterns
- Responsive design for mobile/tablet/desktop

---

### 🔍 Vendor Estimate Reviewer

**File:** `skill-packages/vendor-estimate-reviewer.skill`

A comprehensive skill for evaluating vendor estimates for software development projects, from the client's perspective. This skill helps you determine if a vendor's cost estimate, timeline, and approach are reasonable and whether the project is likely to succeed.

**When to use:**
- You've received a vendor estimate/quotation for software development
- You need to compare multiple vendor estimates
- You want to validate if an estimate is reasonable before contract signing
- You need to prepare negotiation points with a vendor
- You want to identify potential project risks early
- You need documentation for stakeholder approval

**Core Capabilities:**
- ✅ Scope completeness analysis (identify gaps and missing items)
- ✅ Cost reasonableness validation (compare against market standards)
- ✅ Risk identification (14+ critical red flags, 60+ risk factors)
- ✅ Project feasibility assessment (timeline, team composition)
- ✅ Contract terms review (payment terms, warranties, IP ownership)
- ✅ Automated analysis script (Excel, CSV, PDF parsing)
- ✅ Comprehensive Markdown reports with recommendations

**Key Features:**

**5 Integrated Workflows:**
1. Initial Review and Triage (quick red flag check)
2. Detailed Analysis and Assessment (12 dimensions)
3. Vendor Clarification Preparation (structured questions)
4. Final Review and Recommendation (go/no-go decision)
5. Decision Support and Follow-Up (stakeholder presentation)

**Industry Benchmarks:**
- Labor rate standards by role and region (North America, Europe, Asia Pacific)
- Phase distribution percentages (Requirements 10-15%, Design 15-20%, Development 40-50%, Testing 15-25%)
- Project size benchmarks by type (web app, mobile, e-commerce, ERP, API, data migration)
- Team composition standards (senior 20-30%, mid 40-50%, junior 20-30%)
- Contingency recommendations (10-20% typical, 15-25% high-risk)

**Automated Analysis Script:**
```bash
python scripts/analyze_estimate.py vendor_estimate.xlsx \
  --vendor "Acme Corp" \
  --project "CRM System" \
  --budget 500000 \
  --output review_report.md
```

**Critical Red Flags Detected:**
- Testing <10% of effort (critical quality risk)
- No contingency buffer (cost overrun risk)
- All resources at 100% allocation (unrealistic)
- Vague task descriptions
- Missing critical phases
- Rates 30%+ below market (hidden costs or low quality)
- Large upfront payment >30% (financial risk)
- >60% junior resources (quality risk)
- No change management process

**Risk Assessment:**
- 10 risk categories (scope, estimation, resources, technical, process, PM, contract, organizational, domain-specific)
- 60+ specific risk factors with probability, impact, and mitigation strategies
- Risk scoring framework (high/medium/low prioritization)
- Contingency recommendations based on risk profile

**Deliverables:**
- Executive summary (1-2 pages) with go/no-go recommendation
- Comprehensive review report (15-25 pages Markdown)
- Interactive checklist (10-section scoring with approval workflow)
- Clarification request document (structured vendor questions)
- Negotiation strategy memo (cost reduction and value-add opportunities)

**Supported Formats:**
- Excel (.xlsx, .xls)
- CSV
- PDF
- Structured text descriptions

**What You Get:**
- 3 comprehensive reference documents (350+ pages equivalent):
  - Review checklist (12 sections, 200+ items)
  - Cost estimation standards (11 sections with data tables)
  - Risk factors guide (60+ risks with mitigations)
- 1 Python analysis script (automated parsing and reporting)
- 2 Markdown templates (comprehensive report + interactive checklist)

**Use Cases:**
- Pre-contract vendor estimate evaluation
- Multi-vendor comparison and selection
- RFP/RFQ response analysis
- Contract negotiation preparation
- Project risk assessment
- Stakeholder approval documentation
- Budget validation and planning

**Best For:**
- Project managers evaluating vendor proposals
- Technical leads reviewing architecture and effort estimates
- Procurement teams comparing multiple bids
- Finance teams validating budgets
- Business analysts assessing scope completeness
- CTO/CTOs making vendor selection decisions

---

### 📝 Vendor RFQ Creator（ベンダー見積依頼書作成）

**File:** `skill-packages/vendor-rfq-creator.skill`

顧客の曖昧な要望を構造化し、ベンダーに対する明確な見積もり依頼書（RFQ）を作成するスキル。システム開発プロジェクトのRFQ作成に特化し、日本語をデフォルトとして英語にも対応。

A skill that transforms vague client requirements into comprehensive RFQ (Request for Quotation) documents for software development projects. Specializes in creating clear, complete RFQs that enable vendors to provide accurate estimates.

**When to use:**
- 顧客から曖昧または不完全な要件を受け取ったとき
- ベンダーに送付する正式なRFQを作成する必要があるとき
- 正確な見積もりに必要なすべての情報を確実に含めたいとき
- 組織全体でRFQ作成を標準化したいとき

**Core Capabilities:**
- ✅ 要件引き出し（5W1Hフレームワークを使用した体系的な質問）
- ✅ 要件の明確化と構造化（曖昧な要望を明確な仕様に変換）
- ✅ RFQ文書作成（マークダウン形式で専門的な見積依頼書を生成）
- ✅ 品質レビュー（完全性、明確性、一貫性の検証）
- ✅ 日本語・英語対応（日本語がデフォルト、英語にも対応可能）

**Key Features:**

**4つの統合ワークフロー**:
1. Requirements Elicitation（要件引き出し）: 構造化された質問を通じて顧客ニーズを抽出
2. Requirements Structuring（要件構造化）: 曖昧な要件を明確な仕様に変換
3. RFQ Document Creation（RFQ文書作成）: 専門的で包括的なRFQ文書を生成
4. Quality Review（品質レビュー）: ベンダーへの送付前に完全性を検証

**包括的なチェックリスト** (`rfq_checklist_ja.md` - 150+項目):
- プロジェクト概要（基本情報、スコープ、成果物）
- 機能要件（ユーザー要件、システム機能、統合要件）
- 非機能要件（性能、可用性、セキュリティ、拡張性、運用、UX）
- 技術要件（技術スタック、開発環境、標準、ライセンス）
- プロジェクト管理要件（スケジュール、予算、体制、品質、リスク、変更管理）
- 契約・法務要件（契約形態、IP、守秘義務、保証）
- 見積依頼特有の要件（見積書形式、評価基準、提出手続き）
- 品質チェック（明確性、完全性、実現可能性、検証可能性）

**RFQテンプレート** (`rfq_template_ja.md` - 400+行):
完全な9セクション構成の見積依頼書テンプレート:
1. プロジェクト概要
2. 要件詳細（機能・非機能・技術）
3. プロジェクト管理要件
4. 契約・法務要件
5. 見積依頼内容（標準化された見積書フォーマット付き）
6. 評価・選定基準
7. 提出要項
8. 注意事項
9. 問い合わせ先

**要件引き出し手法**:
- **5W1Hフレームワーク**: Who, What, Where, When, Why, How
- **MoSCoW優先順位付け**: Must have, Should have, Could have, Won't have
- **構造化された質問**: カテゴリー別、目的明確、選択肢付き
- **前提条件の文書化**: 合理的な前提、根拠、影響を記載

**見積書フォーマットの標準化**:
- WBS（作業分解構造）テンプレート
- 必須フェーズ: 要件定義、設計、実装、テスト、デプロイメント、PM、品質保証
- 必須カラム: タスク名、詳細、役割、工数（人日）、単価、小計
- コンティンジェンシー（10-20%）
- 前提条件・制約条件セクション

**品質チェック機能**:
- **明確性チェック**: 曖昧な表現の検出と修正提案
- **完全性チェック**: 必須項目の網羅確認
- **一貫性チェック**: 数値の整合性、用語の統一
- **実現可能性チェック**: 技術的実現可能性、予算・スケジュールの現実性

**プロジェクトタイプ別ガイダンス**:
- **Webアプリケーション**: レスポンシブデザイン、SSL/TLS、3秒応答、100同時接続
- **モバイルアプリ**: iOS/Android対応、オフライン動作、プッシュ通知、2秒応答
- **基幹システム**: 99.9%可用性、バックアップ、監査ログ、権限管理
- **データ基盤**: ETL、TB級処理、BI連携、バッチ・リアルタイム処理

**ベストプラクティス**:
1. ビジネス価値から始める（WHYを明確に）
2. 数値で具体的に表現（「多くのユーザー」→「初期1,000名、3年後10,000名」）
3. MoSCoWで優先順位付け
4. 文脈を提供（現状、課題、目指す姿）
5. 見積フォーマットを標準化
6. ベンダーの提案を促す
7. 現実的な期待値を設定
8. Q&Aプロセスを計画

**よくある落とし穴を回避**:
- ❌ 過去のRFQをカスタマイズせずにコピー
- ❌ 技術的に過度に規定
- ❌ スコープ境界が曖昧
- ❌ 非機能要件の欠落
- ❌ 非現実的な予算・スケジュール
- ❌ 評価基準の欠如

**Use Cases:**
- ベンダー選定プロセスの準備
- 複数ベンダーからの見積取得（相見積）
- RFP/RFQ作成の標準化
- プロジェクト予算承認のための文書化
- 要件の明確化とステークホルダー合意形成

**Best For:**
- プロジェクトマネージャー（ベンダー選定を担当）
- 調達・購買部門（システム開発の発注）
- ビジネスアナリスト（要件定義サポート）
- IT部門マネージャー（外部委託管理）
- プロダクトオーナー（開発ベンダーへの要件伝達）

**Output Format:**
- Markdown形式のRFQ文書（すぐにベンダーに送付可能）
- 構造化された見積書フォーマットテンプレート
- チェックリストベースの品質確認レポート

---

### 📋 Vendor Procurement Coordinator（ベンダー調達コーディネーター）

**File:** `skill-packages/vendor-procurement-coordinator.skill`

RFQ作成・送信から、ベンダー回答追跡、見積比較、クライアント向け見積作成までのエンドツーエンドのベンダー調達ワークフローを統合管理するスキル。`vendor-rfq-creator`と`vendor-estimate-creator`スキルをオーケストレーションし、メール自動化とステータス追跡を追加。

A skill that orchestrates the complete vendor procurement lifecycle from initial RFQ creation through vendor response tracking to final client-facing estimate generation. Integrates with existing vendor-rfq-creator and vendor-estimate-creator skills while adding email automation, response tracking, and procurement status management capabilities.

**When to use:**
- 単一プロジェクトで複数ベンダーへの見積依頼を管理するとき
- ベンダーの見積回答と期限を追跡するとき
- 受領したベンダー見積をクライアント向け見積に変換するとき
- RFQ配信をベンダーメールリストに自動化するとき
- エンドツーエンドの調達パイプラインを調整するとき

**Core Capabilities:**
- ✅ 調達プロジェクト初期化（ディレクトリ構造、設定ファイル作成）
- ✅ ベンダー管理（追加、編集、削除、CSVインポート）
- ✅ RFQメール送信（テンプレート、プレビュー/送信モード）
- ✅ 回答追跡（見積受領ログ、ステータス管理、リマインダー）
- ✅ 見積比較レポート（価格分析、納期比較、評価スコア）
- ✅ クライアント見積作成（マークアップ適用、統合）

**Key Features:**

**8ステップ統合ワークフロー**:
1. Initialize Procurement（調達プロジェクト初期化）
2. Create RFQ（RFQ文書作成 - vendor-rfq-creator連携）
3. Register Vendors（ベンダー登録）
4. Send RFQ（RFQ送信）
5. Track Responses（回答追跡）
6. Compare Quotes（見積比較）
7. Create Client Estimate（クライアント見積作成 - vendor-estimate-creator連携）
8. Generate Report（調達レポート生成）

**調達ステータス管理**:
- プロジェクトステータス: initialized → rfq_sent → quotes_received → evaluation → completed
- ベンダーステータス: pending → contacted → quote_received → selected/declined

**メールテンプレート**:
- RFQ送付メール（日本語/英語）
- リマインダーメール（1週間前/3日前）

**Bundled Resources:**
- `references/procurement_workflow_guide.md`: 調達プロセスガイド（6フェーズ）
- `references/vendor_evaluation_criteria.md`: ベンダー評価基準（6次元）
- `assets/email_templates/`: メールテンプレート集

**Use Cases:**
- 複数ベンダーからの相見積取得と管理
- 調達プロセスの標準化と監査証跡
- ベンダー選定の公平性と透明性確保
- クライアント向け見積作成の効率化

**Best For:**
- プロジェクトマネージャー（ベンダー選定担当）
- 調達・購買部門
- ITマネージャー
- システム開発ディレクター

**Output Format:**
- YAML形式の調達ステータス（procurement.yaml）
- Markdown形式のベンダー比較レポート
- Markdown形式のクライアント見積書

---

### 💰 Vendor Estimate Creator（ベンダー見積書作成）

**File:** `skill-packages/vendor-estimate-creator.skill`

RFQや要件を分析し、WBS作成、工数見積、コスト計算、ROI分析を行い、プロフェッショナルな見積書を生成するスキル。システム開発プロジェクトの見積作成に特化し、日本語をデフォルトとして英語にも対応。

A skill that transforms RFQs or project requirements into comprehensive cost estimates and quotations for software development projects. Specializes in creating accurate estimates with WBS, effort calculations, cost breakdowns, and ROI analysis to justify investments.

**When to use:**
- RFQや要件書を受け取り、見積書を作成する必要があるとき
- プロジェクトの工数とコストを高精度で算出したいとき
- 投資対効果（ROI）分析を提供し、投資を正当化したいとき
- 組織全体で見積作成を標準化したいとき
- クライアントのRFQに対してプロフェッショナルな見積書で応答するとき

**Core Capabilities:**
- ✅ RFQ分析と要件抽出（プロジェクト規模、複雑度、リスク評価）
- ✅ WBS作成とタスク特定（7フェーズ、タスク分解、完全性検証）
- ✅ 工数見積もり（4手法、標準工数適用、調整係数、検証）
- ✅ コスト計算と積み上げ（役割別単価、コスト集計、運用保守費算出）
- ✅ ROI分析とビジネスケース（As-Is/To-Be、ROI/NPV/IRR/回収期間、感度分析）
- ✅ 見積書生成（マークダウン形式、12セクション、品質チェック）

**Key Features:**

**6つの統合ワークフロー**:
1. RFQ Analysis and Understanding（RFQ分析と理解）: 要件抽出、規模測定、リスク評価
2. Work Breakdown and Task Identification（作業分解とタスク特定）: WBS作成、フェーズ定義、完全性検証
3. Effort Estimation（工数見積もり）: 手法選択、標準工数適用、調整係数、検証
4. Cost Calculation and Aggregation（コスト計算と積み上げ）: 役割別単価、コスト算出、集計
5. ROI Analysis and Business Case（ROI分析とビジネスケース）: 現状分析、期待効果、財務指標、感度分析
6. Estimate Document Generation（見積書生成）: テンプレート活用、全セクション記入、品質チェック

**見積手法ガイド** (`estimation_methodology.md`):
- 4つの見積手法（類推法、パラメトリック法、ボトムアップ法、三点見積もり）
- 見積精度とプロジェクトフェーズ
- プロジェクトタイプ別工数配分比率（Web、モバイル、基幹、API、データ基盤）
- 工数調整係数（複雑度、習熟度、技術リスク）
- コンティンジェンシー設定（5-40%、リスクレベル別）
- 人材リソース工数単価（役割別、経験年数別）
- 見積ベストプラクティスと注意事項

**工数見積基準ガイド** (`effort_estimation_standards.md`):
- 役割別生産性指標（LOC、FP）
- タスク別標準工数（要件定義、設計、実装、テスト、デプロイ、PM、QA）
- プロジェクトタイプ別標準工数（小規模、中規模、大規模）
- 調整係数の適用方法
- 工数見積の検証手法（生産性チェック、類似PJ比較、フェーズ比率チェック）

**ROI分析ガイド** (`roi_analysis_guide.md`):
- 主要財務指標（ROI、NPV、IRR、投資回収期間）の計算式と解釈
- ベネフィット分類（定量的：コスト削減、売上増加、生産性向上 / 定性的：顧客満足度、従業員満足度）
- ビジネスケース作成手順（As-Is分析、To-Be定義、投資額算出、キャッシュフロー分析、感度分析）
- ビジネスケース文書テンプレート
- ROI分析ベストプラクティス（保守的見積、定量化、複数シナリオ）

**見積書テンプレート** (`estimate_template_ja.md` - 400+行、12セクション):
完全な12セクション構成の見積書テンプレート:
1. エグゼクティブサマリー（プロジェクト概要、見積総額、ROI概要）
2. 前提条件（スコープ、技術前提、プロジェクト前提、納品物）
3. 見積詳細（フェーズ別見積、WBS詳細、役割別工数・単価）
4. プロジェクトスケジュール（マイルストーン、ガントチャート）
5. ROI分析（現状分析、期待効果、財務指標、感度分析）
6. チーム体制（体制図、主要メンバースキルセット）
7. リスクと対策（主要リスク、リスク軽減策）
8. 運用保守費用（保守内容、SLA）
9. 支払条件（開発費支払スケジュール、運用保守費支払）
10. 契約条件（知的財産権、守秘義務、瑕疵担保、変更管理）
11. その他（前提条件、除外事項、有効期限）
12. 承認（顧客・ベンダー署名欄）

**見積手法**:
- **類推法**: 過去の類似プロジェクトベース（精度±25〜50%、構想段階）
- **パラメトリック法**: 画面数・API数等のパラメータベース（精度±15〜30%、企画段階）
- **ボトムアップ法**: WBSベースの積み上げ（精度±5〜15%、要件定義後）
- **三点見積もり**: 楽観値・最頻値・悲観値による確率的見積（精度±10〜20%）

**工数配分比率**（Webアプリケーション標準）:
- 要件定義: 10-15%
- 設計: 15-20%
- 実装: 40-50%
- テスト: 20-25%
- デプロイ・運用準備: 5-10%
- プロジェクト管理: 10-15%
- 品質保証: 7-11%
- コンティンジェンシー: 10-25%

**役割別標準単価**（日本・2025年基準）:
- プロジェクトマネージャー: 100,000〜150,000円/人日
- アーキテクト: 90,000〜140,000円/人日
- シニアエンジニア: 80,000〜120,000円/人日
- ミドルエンジニア: 60,000〜90,000円/人日
- ジュニアエンジニア: 40,000〜65,000円/人日

**ROI財務指標**:
- **ROI**: (総利益 - 総投資額) / 総投資額 × 100
- **NPV**: 将来キャッシュフローの現在価値合計
- **IRR**: NPVをゼロにする割引率
- **投資回収期間**: 初期投資を回収するまでの期間

**ベストプラクティス**:
1. 複数手法で見積を検証（ボトムアップ、パラメトリック、類似PJ比較）
2. 保守的に見積もり（便益は控えめ、コストは余裕を持って）
3. 前提条件を明記（すべての前提を文書化）
4. リスクを早期特定（技術、要件、統合、チーム、PM）
5. ROI分析を提供（ROI、NPV、IRR、回収期間、感度分析）
6. PM・QA工数を必ず計上（PM 10-15%、QA 7-11%）

**よくある落とし穴を回避**:
- ❌ コンティンジェンシーを含めない
- ❌ プロジェクト管理工数を忘れる
- ❌ データ移行を見落とす
- ❌ 非機能要件（性能、セキュリティ）を軽視
- ❌ 統合テスト工数を過小評価
- ❌ ROI分析で楽観的すぎる便益見積もり

**Use Cases:**
- RFQ応答のための見積書作成
- 社内プロジェクトの予算承認申請
- 複数提案の中から最適案選定（ROI比較）
- 投資判断のための財務分析
- ベンダー選定プロセスでの自社見積提出

**Best For:**
- ベンダー営業（RFQ応答、提案書作成）
- プロジェクトマネージャー（プロジェクト計画、予算申請）
- アカウントマネージャー（顧客提案、価格交渉）
- 経営企画部門（投資判断、ROI分析）
- 財務部門（予算承認、投資対効果評価）

**Output Format:**
- Markdown形式の見積書（12セクション、WBS詳細、ROI分析含む）
- 標準化されたWBS構造（タスクID、役割、工数、単価、小計）
- 財務指標付きROI分析（ROI、NPV、IRR、回収期間、感度分析）

---

### 📋 Project Plan Creator（プロジェクト計画作成）

**File:** `skill-packages/project-plan-creator.skill`

システム開発・導入プロジェクトの包括的なプロジェクト計画を作成する専門スキル。Project Charter、WBS、Ganttチャート、RACI matrix、リスク分析等をMarkdown + Mermaidで文書化し、PMBOK準拠のプロジェクト管理成果物を生成。

A specialist skill for creating comprehensive project plans for system development or implementation projects. Generates PMBOK-aligned project management artifacts including Project Charters, WBS, Gantt Charts, RACI matrices, and Risk analysis using Markdown + Mermaid visualizations.

**When to use:**
- 新規プロジェクトを開始し、プロジェクト計画を作成する必要があるとき
- Project Charterでプロジェクトを正式に承認・権限付与したいとき
- WBS、スケジュール、リソース配分を含む包括的なプロジェクト計画が必要なとき
- Mermaidダイアグラム（Gantt、WBS、ワークフロー）でプロジェクト構造を可視化したいとき
- PMBOK準拠のプロジェクト文書が必要なとき
- knowledge/pm-knowledgeフォルダのPM知識を活用したいとき

**Core Capabilities:**
- ✅ プロジェクトチャーター作成（12セクション、PMBOK準拠、正式承認文書）
- ✅ スコープ定義と管理（In/Out定義、WBS、スコープ変更管理プロセス）
- ✅ スケジュール作成（Mermaid Ganttチャート、依存関係、クリティカルパス）
- ✅ リソース計画とRACI Matrix（体制図、役割定義、責任明確化）
- ✅ リスク管理計画（リスク識別、分析、対応計画、監視プロセス）
- ✅ コミュニケーション・品質計画（コミュニケーションマトリックス、品質基準、QAプロセス）
- ✅ 統合と文書生成（すべての計画成果物を包括的プロジェクト計画に統合）

**Key Features:**

**7つの統合ワークフロー**:
1. Project Charter Creation（プロジェクトチャーター作成）: インプット収集、目的定義、スコープ、成果物、予算、ステークホルダー、リスク、成功基準
2. Scope Definition and Management（スコープ定義と管理）: スコープステートメント、スコープ境界可視化、WBS作成、スコープベースライン、変更管理プロセス
3. Schedule Development with Gantt Charts（Ganttチャートでスケジュール作成）: アクティビティ定義、シーケンス、期間見積、Mermaid Gantt作成、クリティカルパス特定、スケジュール最適化
4. Resource Planning and RACI Matrix（リソース計画とRACI Matrix）: プロジェクト役割定義、RACI Matrix作成、コミュニケーションプロトコル、チーム構造可視化
5. Risk Management Planning（リスク管理計画）: リスク識別（5カテゴリ）、定性的分析、対応計画、監視プロセス確立
6. Communication and Quality Planning（コミュニケーション・品質計画）: ステークホルダー分析、コミュニケーションマトリックス、品質基準、QAプロセス、受け入れ基準
7. Integration and Document Generation（統合と文書生成）: テンプレート活用、全セクション記入、Mermaidダイアグラム生成、品質チェック、承認取得

**プロジェクトチャーターガイド** (`project_charter_guide.md`):
- PMBOK準拠のチャーター作成ガイド（12セクション）
- プロジェクト基本情報、エグゼクティブサマリー、背景と目的
- スコープ（In/Out）、主要成果物、マイルストーン
- 概算予算（開発、インフラ、間接費）
- 前提条件と制約、主要リスク
- ステークホルダー、成功基準、承認
- システム開発プロジェクトの実例
- ベストプラクティスとよくある落とし穴

**プロジェクト計画テンプレート** (`project_plan_template.md` - 400+行、12セクション):
Mermaidダイアグラム5つを含む完全なプロジェクト計画テンプレート:
1. プロジェクト基本情報（名称、コード、PM、期間、予算）
2. エグゼクティブサマリー（概要、目的、スコープ、成果物、期間、予算）
3. プロジェクトスコープ（スコープ記述、スコープ境界Mermaid図）
4. WBS（WBS階層Mermaid図、詳細WBS表）
5. プロジェクトスケジュール（Mermaid Ganttチャート、マイルストーン、クリティカルパス）
6. 成果物一覧（成果物、説明、納期、承認者、受け入れ基準）
7. チーム体制とRACI（体制図Mermaid、RACI Matrix）
8. リスク管理計画（リスク登録簿、対応計画、監視プロセスMermaid図）
9. コミュニケーション計画（コミュニケーションマトリックス、会議体、報告）
10. 品質管理計画（品質基準、QAプロセスMermaid図、レビュー体制）
11. 変更管理計画（変更管理プロセスMermaid図、CCB、影響評価）
12. 承認（PM、PO、Sponsor署名欄）

**Mermaid可視化**（5つのダイアグラム）:
- **Scope Boundary Diagram**: In Scope vs Out of Scope可視化（graph TB）
- **WBS Hierarchy**: 作業分解構成の階層図（graph TD）
- **Gantt Chart**: プロジェクトスケジュールとマイルストーン（gantt）
- **Risk Monitoring Process**: リスク監視プロセスフロー（graph LR）
- **Change Management Process**: 変更管理プロセスフロー（graph TD）

**PMBOK知識エリア統合**:
- Project Integration Management（統合管理）
- Project Scope Management（スコープ管理）
- Project Schedule Management（スケジュール管理）
- Project Cost Management（コスト管理）
- Project Quality Management（品質管理）
- Project Resource Management（リソース管理）
- Project Communications Management（コミュニケーション管理）
- Project Risk Management（リスク管理）
- Project Procurement Management（調達管理）
- Project Stakeholder Management（ステークホルダー管理）

**リスク管理フレームワーク**:
- **技術リスク**: 新技術習得、性能要件、外部API変更
- **要件リスク**: 要件変更頻発、ステークホルダー間認識相違、スコープクリープ
- **リソースリスク**: キーメンバー離脱、スキル不足、リソース競合
- **統合リスク**: 既存システム連携困難、データ移行複雑、第三者システム互換性
- **外部リスク**: ベンダー納期遅延、法規制変更、市場環境変化

**RACI Matrix定義**:
- **R (Responsible)**: 実行責任者（作業を実施する人）
- **A (Accountable)**: 説明責任者（最終意思決定者、各タスク1名のみ）
- **C (Consulted)**: 相談先（事前に意見を聞く人）
- **I (Informed)**: 報告先（結果を報告する人）

**スケジュール見積手法**:
- **PERT三点見積もり**: (楽観値 + 4×最頻値 + 悲観値) / 6
- **依存関係**: FS（Finish-to-Start）、SS（Start-to-Start）、FF（Finish-to-Finish）、SF（Start-to-Finish）
- **クリティカルパス**: 最長パスの特定と管理集中
- **スケジュール短縮**: Crashing（リソース追加）、Fast Tracking（並行実施）

**品質基準例**:
- **コード品質**: カバレッジ80%以上、複雑度10以下、コードレビュー、静的解析
- **テスト品質**: 単体テスト80%、統合テスト全API、システムテスト全機能、UAT全ビジネスシナリオ
- **ドキュメント品質**: 全設計書レビュー・承認、API仕様自動生成、運用マニュアルユーザーレビュー

**ベストプラクティス**:
1. チャーターから開始（プロジェクト正式承認、PM権限付与）
2. ビジュアル図を活用（MermaidでWBS、Gantt、プロセスフロー可視化）
3. RACIを早期定義（役割と責任の明確化、混乱回避）
4. プロアクティブなリスク管理（早期識別、継続監視）
5. すべてベースライン化（スコープ、スケジュール、コストのベースライン確立）
6. バージョン管理（文書バージョンと変更履歴維持）
7. ステークホルダーエンゲージメント（定期的コミュニケーション、期待値管理）
8. PMBOK準拠（一貫性とプロフェッショナリズム）

**よくある落とし穴を回避**:
- ❌ プロジェクトチャーター作成をスキップ
- ❌ 曖昧なスコープ定義（スコープクリープ発生）
- ❌ バッファなしの非現実的スケジュール
- ❌ RACI Matrixなし（役割混乱）
- ❌ 問題発生まで リスク管理を無視
- ❌ 変更管理プロセスの欠如
- ❌ ステークホルダーコミュニケーション不足
- ❌ 品質基準を事前に設定しない

**Use Cases:**
- 新規システム開発プロジェクト立ち上げ
- システム導入プロジェクトの計画策定
- 大規模リプレースプロジェクトの計画
- マルチベンダープロジェクトの統合計画
- PMO標準プロジェクト計画テンプレート作成
- プロジェクト提案書のプロジェクト計画セクション

**Best For:**
- プロジェクトマネージャー（プロジェクト計画作成、承認取得）
- PMO（標準テンプレート、プロセス確立）
- プロダクトオーナー（スコープ定義、優先順位）
- エンタープライズアーキテクト（技術計画、統合設計）
- ステアリングコミッティ（計画レビュー、承認）

**Output Format:**
- Markdown + Mermaid形式のプロジェクト計画（12セクション）
- 5つのMermaidダイアグラム（Scope、WBS、Gantt、Risk Process、Change Management）
- RACI Matrix（全タスク・成果物の責任明確化）
- リスク登録簿（リスク識別、分析、対応策）
- コミュニケーション・品質計画（マトリックス、基準、プロセス）

**Framework Alignment:**
- PMBOK® Guide 6th Edition準拠
- PMBOK® Guide 7th Edition principles対応
- ISO 21500プロジェクトマネジメント標準
- Prince2® compatible processes

---

### 📊 WBS Review Assistant（WBS照合レビュー支援）

**File:** `skill-packages/wbs-review-assistant.skill`

Work Breakdown Structure (WBS) Excelファイルをプロジェクト要件書、ヒアリングシート、過去の決定事項と照合し、ギャップ、不整合、決定事項からの逸脱を自動検出。Excelセルに直接レビューコメントを追加し、優先順位付けされたサマリーレポートを生成する専門スキル。

A specialist skill for reviewing and annotating Work Breakdown Structure (WBS) Excel files against project requirements, hearing sheets, and prior decisions. Automatically identifies gaps, inconsistencies, and deviations. Adds review comments directly to Excel cells and generates prioritized summary reports.

**When to use:**
- WBSを要件書と照合してレビューする必要があるとき
- WBS + 要件ドキュメントでギャップ分析が必要なとき
- ヒアリングシートの決定事項とWBSの整合性を確認したいとき
- ベースライン承認前にWBSの完全性を検証したいとき
- Excelにレビューコメントをアノテーションしたいとき
- キックオフ前にWBS課題の優先順位付けリストが必要なとき

**Core Capabilities:**
- ✅ 要件トレーサビリティ分析（要件IDとWBSタスクのマッピング）
- ✅ 構造検証（WBSコード階層、フェーズ構成、マイルストーン）
- ✅ コンテンツ品質チェック（工数見積、タスク記述、受入基準）
- ✅ ヒアリングシート決定事項クロスチェック（決定がWBSに反映されているか）
- ✅ Excel直接アノテーション（セルコメント + 条件付き書式で重要度可視化）
- ✅ 優先順位付けレポート生成（JSON、Markdown、アノテーション済Excel）

**Key Features:**

**5段階レビュープロセス**:
1. **Document Ingestion（ドキュメント取込）**: WBS Excel、要件書、ヒアリングノート解析
2. **Traceability Analysis（トレーサビリティ分析）**: 要件→WBSタスク、WBS→要件の双方向マッピング
3. **Structural Validation（構造検証）**: 階層整合性、WBSコード番号、フェーズ構成
4. **Content Quality Checks（コンテンツ品質チェック）**: 工数見積、タスク記述、品質ゲート
5. **Finding Prioritization（所見優先順位付け）**: 重要度 × 影響度で優先順位算出

**チェックリストカテゴリ（YAML設定）**:
- **Completeness（完全性）**: 全要件マッピング、成果物識別、受入基準、依存関係
- **Consistency（一貫性）**: WBSコード番号、工数見積、リソース割当、詳細レベル
- **Alignment（整合性）**: ヒアリングシート決定反映、スコープ境界遵守、技術選択整合
- **Quality（品質）**: テストフェーズ存在、ドキュメント作成タスク、レビューゲート
- **Estimation（見積品質）**: 積上計算正確性、妥当な工数範囲、バッファ/コンティンジェンシー

**重要度レベル定義**:
- **Critical（致命的）**: WBSベースライン不可（要件欠落、計算エラー）
- **Major（重大）**: プロジェクト成功に高リスク（テスト不足、詳細不足）
- **Minor（軽微）**: 改善機会（フォーマット、命名規則）

**3つの出力形式**:
1. **アノテーション済Excel** (`wbs_annotated_YYYYMMDD_HHMMSS.xlsx`):
   - 元のWBS構造保持（非破壊レビュー）
   - セルコメントに所見追加（Finding ID、重要度、推奨対応）
   - 条件付き書式（赤=Critical、オレンジ=Major、黄=Minor）
   - 新シート「Review Summary」（課題ダッシュボード、フィルタ機能）

2. **Markdownサマリーレポート** (`wbs_review_summary_YYYYMMDD_HHMMSS.md`):
   - エグゼクティブサマリー（重要度別課題数、準備度スコア）
   - 優先順位付け所見リスト（Top 10、推奨対応付き）
   - 要件カバレッジ分析（トレーサビリティマトリックス）
   - 欠落タスク候補（未マッピング要件から推奨）

3. **JSONギャップ分析** (`wbs_gaps_YYYYMMDD_HHMMSS.json`):
   - 機械可読な所見データ（CI/CD統合可能）
   - トレーサビリティマトリックス（要件→WBSタスク）
   - 各チェック基準の検証結果

**Readiness Score計算式**:
```
Base Score = 100
- Criticalごとに20点減点
- Majorごとに5点減点
- Minorごとに1点減点
Readiness Score = max(0, Base Score - 減点合計)

90-100: ベースライン承認可
70-89: 要修正だが使用可
50-69: 重大なギャップ、大幅な作り直し必要
<50: 不完全、レビュー不可
```

**よくあるWBS課題パターン（自動検出）**:
- ❌ **MISSING-REQ**: 要件書に記載があるがWBSタスクなし（Critical）
- ❌ **MISSING-MILESTONE**: フェーズ境界に承認マイルストーンなし（Major）
- ❌ **MISSING-TESTING**: 単体テスト、結合テスト、UAT不足（Critical）
- ❌ **INCONSISTENT-NUMBERING**: WBSコード階層スキップ（1.1→1.3）（Major）
- ❌ **MISSING-EFFORT**: リーフタスクに工数見積なし（Major）
- ❌ **ROLLUP-ERROR**: 親タスク合計 ≠ 子タスク合計（Critical）
- ❌ **HEARING-DECISION-MISSING**: ヒアリングシート決定事項がWBSに未反映（Critical）
- ❌ **OUT-OF-SCOPE-TASK**: 要件書に記載ない作業がWBSに存在（Major）
- ❌ **TECH-CHOICE-MISMATCH**: 要件書と異なる技術スタック（Major）
- ❌ **NO-ACCEPTANCE-CRITERIA**: マイルストーンに受入基準なし（Major）
- ❌ **MISSING-DOCUMENTATION**: 成果物にドキュメント作成タスクなし（Major）
- ❌ **NO-REVIEW-GATE**: 開発タスクに正式レビューなし（Major）
- ❌ **UNREALISTIC-ESTIMATE**: タスク工数が大きすぎる（>80h、分解が必要）（Major）
- ❌ **NO-CONTINGENCY**: コンティンジェンシーバッファなし（Minor）

**バイリンガルサポート**:
- 日本語WBS対応（タスク名、要件ID: 要件-001、機能-002）
- 日本語ヒアリングノート対応（決定、合意、承認マーカー）
- バイリンガルレポート生成（EN/JA並列表示オプション）

**Use Cases:**
- システム開発プロジェクトのWBS品質保証
- ベースライン承認前のWBS最終チェック
- ベンダー提出WBSの妥当性検証
- 要件変更後のWBS更新確認
- プロジェクトキックオフ前のWBS準備度評価
- PMO標準レビュープロセスの自動化

**Best For:**
- プロジェクトマネージャー（WBS品質保証、ベースライン前確認）
- PMO（標準レビュープロセス、品質ゲート）
- ビジネスアナリスト（要件トレーサビリティ確認）
- QAリード（テスト計画妥当性、受入基準確認）
- ステアリングコミッティ（WBS承認前のリスク評価）

**Framework Alignment:**
- PMBOK® Guide (WBS作成、スコープ管理、品質保証)
- ISO 21500 (Work Breakdown Structure standards)
- IEEE 830 (Requirements Traceability)

---

### 🐛 Bug Ticket Creator（不具合チケット作成）

**File:** `skill-packages/bug-ticket-creator.skill`

システムテスト中に発見した不具合を包括的なバグチケットに変換する対話型スキル。ユーザーと対話しながら再現手順、環境情報、重要度判定など必要な情報を収集し、プロフェッショナルなマークダウン形式の不具合報告書を生成。

An interactive skill that transforms bug discoveries during system testing into comprehensive bug tickets. Guides users through systematic questioning to collect reproduction steps, environment details, severity assessment, and generates professional Markdown bug reports.

**When to use:**
- テスト中に不具合を発見し、バグチケットを作成する必要があるとき
- 再現手順を体系的に整理したいとき
- 適切な重要度・優先度を判定したいとき
- 標準化されたプロフェッショナルなバグ報告フォーマットが必要なとき
- 開発チームが迅速に理解・修正できる高品質なバグチケットを作成したいとき

**Core Capabilities:**
- ✅ 対話型の情報収集（6つのワークフロー、体系的な質問）
- ✅ 初期発見（何が、どこで、いつ発生したか）
- ✅ 再現手順収集（CLEAR原則準拠、事前条件、ステップバイステップ、再現率）
- ✅ 期待値vs実際の動作（仕様との差異明確化）
- ✅ 環境情報収集（OS、ブラウザ、デバイス、解像度、ネットワーク等）
- ✅ 重要度・優先度判定（Severity: Critical/High/Medium/Low、Priority: P0/P1/P2/P3）
- ✅ バグチケット生成（マークダウンファイル出力、日本語/英語対応）

**Key Features:**

**6つの統合ワークフロー**:
1. Initial Bug Discovery（初期発見）: 何が起きたか、どこで起きたか、いつ起きたか、バグタイプ分類、初期重要度評価
2. Reproduction Steps Collection（再現手順収集）: 事前条件確立、ステップバイステップ収集、失敗ポイント特定、再現率確認
3. Expected vs Actual Behavior（期待vs実際）: 期待される動作明確化、実際の動作記録、ギャップ分析、証拠収集（スクリーンショット、ログ）
4. Environment Information Collection（環境情報収集）: 基本環境情報（OS、ブラウザ、デバイス）、追加詳細（解像度、ネットワーク、拡張機能）、環境依存性確認
5. Severity and Priority Assessment（重要度・優先度判定）: Severity判定（技術的影響）、Priority判定（ビジネス緊急性）、組み合わせ説明
6. Bug Ticket Generation（バグチケット生成）: 残情報収集、テンプレート選択、情報入力、レビュー、マークダウンファイル生成

**不具合分類ガイド** (`defect_classification_guide.md`):
- 7つの不具合タイプ分類:
  - 機能不具合（Functional Defect）: 機能欠如、機能誤動作、余分な機能
  - UI/UX不具合（UI/UX Defect）: 表示崩れ、デザイン不一致、操作性問題、アクセシビリティ問題
  - パフォーマンス不具合（Performance Defect）: 応答速度問題、リソース消費問題、スケーラビリティ問題
  - データ不具合（Data Defect）: データ損失、データ不整合、データ破損
  - セキュリティ不具合（Security Defect）: 認証・認可問題、データ漏洩、インジェクション、セッション管理問題
  - 統合・連携不具合（Integration Defect）: API連携エラー、データ連携エラー、認証連携エラー
  - 環境依存不具合（Environment-Specific Defect）: ブラウザ依存、OS依存、デバイス依存、環境設定依存
- 発生フェーズ分類（要件定義、設計、実装、テスト、デプロイ）
- 原因分類（仕様理解不足、設計ミス、コーディングエラー、環境問題、データ問題、第三者システム問題）
- 影響範囲分類（全体影響、機能影響、局所影響、視覚的影響）

**重要度・優先度判定ガイド** (`severity_priority_guide.md`):
- **重要度（Severity）** - 技術的影響（QAチームが判定）:
  - Critical: システム使用不可、データ損失、セキュリティリスク
  - High: 主要機能使用不可、回避策なし
  - Medium: 機能に問題あるが回避策あり
  - Low: 視覚的問題のみ、影響軽微
- **優先度（Priority）** - ビジネス緊急性（PO/PMが判定）:
  - P0（最優先）: 本番環境で発生中、即座対応（数時間以内）
  - P1（高優先）: 1-3営業日以内の対応が必要
  - P2（中優先）: 次回リリースで対応（1-2週間）
  - P3（低優先）: バックログ追加、時間がある時に対応
- 重要度×優先度マトリックス（判定ガイド）
- 判定フローチャート
- 実際の判定例5例（ログイン不可、管理画面レポート不具合、スマホ表示崩れ、ヘルプ誤字、管理者機能バグ）
- 特殊ケース判定（セキュリティ、パフォーマンス、UI/UX、環境依存、顧客影響）

**再現手順の書き方ガイド** (`reproduction_steps_guide.md`):
- **CLEAR原則**:
  - **C**omplete（完全）: すべての必要な情報
  - **L**ogical（論理的）: 論理的な順序
  - **E**xplicit（明示的）: 曖昧な表現なし
  - **A**ctionable（実行可能）: 誰でも同じ手順を実行可能
  - **R**eproducible（再現可能）: 何度でも同じ結果
- 再現手順の基本構成（事前条件、再現手順、期待結果、実際結果、環境情報）
- 事前条件の書き方（ログイン状態、データ状態、システム状態）
- 再現手順の書き方（番号付け、一つの手順に一つの操作、具体的記述、操作対象明示、入力値記載）
- 期待結果・実際結果の書き方（具体的、観測可能、仕様書参照）
- 環境情報の書き方（OS、ブラウザ、デバイス、解像度、ネットワーク、言語設定、タイムゾーン）
- スクリーンショット・動画・ログの添付ガイド
- 良い例と悪い例の比較（実例2例: ログイン失敗、スマホ表示崩れ）

**バグチケットテンプレート** (日本語・英語):
完全な12セクション構成:
1. ヘッダー（タイトル、作成日、報告者、ステータス、Severity、Priority）
2. 不具合概要（Summary）
3. 不具合分類（Classification）: タイプ、サブカテゴリ、影響範囲、発生フェーズ、影響ユーザー数
4. 事前条件（Preconditions）
5. 再現手順（Steps to Reproduce）: ステップバイステップ
6. 期待される結果（Expected Result）
7. 実際の結果（Actual Result）
8. 再現頻度（Reproduction Rate）
9. 環境情報（Environment）: OS、ブラウザ、デバイス、解像度等
10. 添付ファイル（Attachments）: スクリーンショット、動画、ログ
11. 追加情報（Additional Information）: エラーメッセージ全文、コンソールログ、ネットワークログ、サーバーログ
12. 関連情報（Related Information）: 関連チケット、仕様書、デザインモック、PR
13. 暫定回避策（Workaround）
14. 備考・コメント（Notes/Comments）
15. 影響分析（Impact Analysis）: ビジネス影響、セキュリティ影響、ユーザー影響
16. 対応方針推奨（Recommended Action）: 推奨優先度、推奨対応方法
17. 更新履歴（Update History）
18. チェックリスト（Quality Check）: 報告者確認、開発チーム確認

**対話の流れ（インタラクティブ質問）**:
```
1. 初期発見フェーズ:
   - 何が起きましたか？
   - どこで起きましたか？
   - 問題のタイプは？（7つの選択肢）
   - 影響の大きさは？

2. 再現手順フェーズ:
   - 事前条件は？（ログイン状態、データ、開始画面）
   - 操作を一つずつ教えてください
   - どの時点で問題が発生しましたか？
   - 毎回発生しますか？（再現率）

3. 期待vs実際フェーズ:
   - 本来どうあるべきですか？
   - 実際に何が起きましたか？
   - スクリーンショットはありますか？

4. 環境情報フェーズ:
   - OS、ブラウザ、デバイスは？
   - 追加の環境詳細は？
   - 他の環境でも発生しますか？

5. 重要度・優先度フェーズ:
   - システム全体が使えませんか？
   - データ損失はありますか？
   - 本番環境で発生していますか？
   - リリース予定日は近いですか？

6. チケット生成フェーズ:
   - チケットタイトルを考えてください
   - 回避策はありますか？
   - 添付ファイルは？
   - 日本語？英語？
```

**ベストプラクティス**:
1. 一度に一つの質問（ユーザーを圧倒しない）
2. 明確化と確認（曖昧な回答にフォローアップ質問）
3. 技術知識を仮定しない（用語説明、例示）
4. 体系的な収集（ワークフロー順守、ステップスキップしない）
5. プロフェッショナルな出力（整形されたMarkdown、テンプレート厳守）
6. 証拠を奨励（スクリーンショット、動画、ログ依頼）

**よくある落とし穴を回避**:
- ❌ 曖昧な説明を受け入れる（「エラーが出る」で終わらせない）
- ❌ 再現頻度をスキップ（毎回？何回中何回？を確認）
- ❌ 不完全な環境情報（「Chrome」だけでなくバージョンまで）
- ❌ 複数操作を一つにまとめる（ステップを分解）
- ❌ 証拠を求めない（スクリーンショット・ログを依頼）

**Use Cases:**
- システムテスト中の不具合発見
- 結合テスト、システムテスト、受け入れテストでのバグ報告
- 本番環境でのインシデント報告
- QAチームによる不具合文書化
- テスト担当者のバグ報告スキル向上
- チーム内でのバグ報告標準化

**Best For:**
- QAエンジニア（不具合発見・報告）
- テスター（テスト実行・バグチケット作成）
- 開発者（自己テスト時のバグ記録）
- プロジェクトマネージャー（バグ管理品質向上）
- ビジネスアナリスト（UAT時のバグ報告）

**Output Format:**
- Markdown形式の不具合チケット（.md file）
- ファイル名形式: BUG-[NUMBER]_[short-description]_[YYYY-MM-DD].md
- 完全な12セクション構成
- プロフェッショナルなフォーマット
- JIRAやRedmine、GitHub Issues等のチケット管理システムにそのまま利用可能

**Framework Alignment:**
- ISTQB（International Software Testing Qualifications Board）準拠のバグ報告
- IEEE 829テスト文書化標準
- ISO/IEC/IEEE 29119ソフトウェアテスト標準

**Bilingual Support:**
- 日本語（デフォルト）: 対話、テンプレート、ガイド全て日本語対応
- English: Full English template and workflow support

---

### 📧 Internal Email Composer

**File:** `skills/internal-email-composer/SKILL.md`

Generate professional internal email drafts for common coordination tasks in business environments. Creates culturally-appropriate bilingual (Japanese/English) emails with proper business tone.

**When to use:**
- Drafting internal emails to request vendor quote compilation
- Forwarding RFQ documents to internal stakeholders
- Delegating tasks to team members with clear instructions
- Sending status update emails for ongoing projects
- Composing follow-up emails for pending responses
- Creating escalation emails for delayed deliverables

**Core Capabilities:**
- ✅ 6 email scenarios (Vendor RFQ, Task Delegation, Status Update, Follow-up, Escalation, Info Request)
- ✅ Bilingual support (Japanese/English) with culturally-adapted content
- ✅ 3 urgency levels with appropriate subject prefixes
- ✅ Template engine with variable substitution
- ✅ Business etiquette compliance (敬語, keigo for Japanese)

**Key Components:**
- `scripts/compose_email.py` - Main email composition script with CLI interface
- `references/email-templates.md` - Template patterns for each email type
- `references/business-etiquette-guide.md` - Cultural considerations for JA/EN emails

**Output Formats:**
- Markdown email draft with subject, greeting, body, closing, signature
- JSON structure for programmatic integration

**Example Use Cases:**
- "Create a Japanese email to forward RFQ to procurement team"
- "Draft a task delegation email for Q4 budget review"
- "Compose a follow-up email for pending vendor quotes"
- "Generate an escalation email about delayed deliverables"

---

### 🎯 ITIL 4 Consultant

**File:** `itil4-consultant/`

Expert ITIL 4 consultant providing context-aware recommendations for IT service management improvement.

**When to use:**
- Implementing or improving ITIL 4 practices in your organization
- Assessing IT service management maturity
- Optimizing IT operations and service delivery
- Aligning IT services with business objectives
- Designing processes based on ITIL 4 best practices
- Integrating DevOps/Agile with ITIL 4 framework

**Core Capabilities:**
- ✅ Comprehensive ITIL 4 knowledge (34 practices across 3 categories)
- ✅ Context-aware consulting (department, scenario, industry-specific)
- ✅ Maturity assessment framework (5 levels)
- ✅ Tailored improvement roadmaps
- ✅ Integration with DevOps, Agile, and other frameworks
- ✅ Best practices from extensive knowledge base

**Knowledge Base:**
- ITIL 4 Foundation concepts (SVS, SVC, 4 Dimensions, 7 Guiding Principles)
- 14 General Management Practices (Architecture, Security, Risk, etc.)
- 17 Service Management Practices (Incident, Change, Release, etc.)
- 3 Technical Management Practices (Deployment, Infrastructure, Development)

**Core Workflows:**
1. **Context Analysis & Scoping** - Understand organizational context and needs
2. **Current State Assessment** - Maturity evaluation with gap analysis
3. **Recommendation Development** - Tailored, actionable recommendations
4. **Roadmap Creation** - Phased implementation plan
5. **Department/Scenario-Specific Consulting** - Context-aware guidance

**Scenario Support:**
- IT Operations (high incident volume, MTTR improvement)
- Development Teams (change failure reduction, DevOps integration)
- Security Teams (compliance, risk management)
- PMO (portfolio optimization, resource management)
- Infrastructure Teams (cloud migration, platform management)

**Deliverables:**
- Maturity Assessment Reports
- Gap Analysis with prioritization
- Implementation Roadmaps (phased approach)
- Practice-specific improvement plans with KPIs
- Integration strategies with DevOps/Agile

**Key Features:**
- **7 Guiding Principles** application to all recommendations
- **4 Dimensions** holistic consideration
- **Quick Wins → Medium-term → Strategic** phased approach
- **Value-focused** consulting (ITIL 4 core principle)
- **Best practices** from comprehensive knowledge base
- **Bilingual**: Japanese and English support

---

### ☁️ Salesforce Expert

**File:** `skill-packages/salesforce-expert.skill`

Expert guidance for Salesforce system development and operations management.

**When to use:**
- Configuring sharing settings, approval processes, validation rules
- Diagnosing access denied issues, approval process errors, missing relationships
- Designing system architecture, data models, object relationships
- Implementing Apex triggers, batch jobs, Lightning Web Components, REST APIs
- Resolving OWD settings, sharing rules, role hierarchy issues
- Addressing governor limit issues, slow queries, large data volume challenges

**Core Capabilities:**
- ✅ Sharing settings & access control troubleshooting
- ✅ Approval process configuration & debugging
- ✅ Custom development best practices (Apex, LWC)
- ✅ Architecture design & data modeling
- ✅ Governor limit optimization
- ✅ Integration patterns (REST API, Platform Events)

**Reference Guides:**
- `sharing_settings_guide.md` - OWD, sharing rules, role hierarchy, manual sharing patterns
- `approval_process_guide.md` - Single/multi-step approvals, submission methods, testing
- `custom_development_patterns.md` - Trigger handlers, batch apex, LWC, testing patterns
- `architecture_best_practices.md` - Data modeling, LDV design, integration, security

**Bug Analysis Workflow:**
1. **Gather Context** - Record type, user role, error message, reproduction steps
2. **Categorize Issue** - Access/permissions, data integrity, process automation, integration, UI/UX
3. **Diagnose Root Cause** - Systematic troubleshooting with debug queries
4. **Propose Solutions** - Quick fix, proper solution, long-term improvement
5. **Document Fix** - Root cause analysis, testing steps, deployment considerations

**Development Patterns:**
- Trigger Handler pattern with recursion prevention
- Service Layer pattern for reusable business logic
- Batch Apex (standard, iterable, stateful)
- Queueable Apex with chaining
- Lightning Web Components (wire, imperative, pub/sub)
- REST API design (inbound/outbound)

**Common Scenarios:**
- "User cannot access related Contact after Opportunity reassignment" → OWD/Sharing analysis
- "No applicable approval process found" → Entry criteria and active process validation
- "Contact shows 0 Opportunities despite linkage" → Relationship type analysis
- "Design REST API for external system integration" → REST resource pattern with proper HTTP methods
- "Optimize trigger for 200 records" → Bulkification and governor limit patterns

**Best Practices:**
- Security: Always use `with sharing`, check CRUD/FLS, principle of least privilege
- Performance: Bulkify code for 200 records, avoid SOQL in loops, batch DML operations
- Maintainability: Trigger → Handler → Service pattern, single responsibility
- Testing: Test Data Factory, bulk testing, mock callouts, 85%+ coverage

**Key Features:**
- **Systematic Troubleshooting** - Step-by-step diagnosis workflows
- **Enterprise Patterns** - Scalable, maintainable code patterns
- **Complete Code Examples** - Real-world Apex triggers, handlers, services, LWC
- **Architecture Guidance** - Data modeling, integration, security, testing
- **Bilingual**: Japanese and English support

---

### 🤖 AI Adoption Consultant

**File:** `skill-packages/ai-adoption-consultant.skill`

Expert AI/LLM adoption consultant with comprehensive use case knowledge across industries, departments, and scenarios.

**When to use:**
- Proposing AI/LLM adoption strategies for specific industries (Finance, Healthcare, Retail, Manufacturing, Education)
- Recommending AI solutions for department-specific needs (Sales, HR, Support, Finance, R&D)
- Creating AI implementation plans for different scenarios (Startup, Enterprise, Remote Work, CX, DX)
- Selecting appropriate AI agent types (RAG, Voice, Video Generation, Internal Business Support)
- Analyzing case studies and ROI for AI initiatives

**Core Capabilities:**
- ✅ Industry-specific AI adoption strategies (5 industries)
- ✅ Department-specific automation & efficiency improvements (5 functions)
- ✅ Scenario-based implementation approaches (5 scenarios)
- ✅ AI agent type recommendations (4 types: RAG, Voice, Video, Business Support)
- ✅ Detailed case studies (6 use cases: Sales Support, Customer Support, Knowledge Search, Project Planning, Competitive Analysis, Strategic Planning)

**Knowledge Base:**
- **Industries**: Finance, Healthcare, Retail, Manufacturing, Education
- **Functions**: Sales & Marketing, HR, Customer Support, Finance & Accounting, R&D
- **Scenarios**: Startup, Enterprise, Remote Work, Customer Experience, Digital Transformation
- **Agent Types**: RAG agents, Voice agents, Video generation, Internal business support
- **Case Studies**: 6 detailed implementation examples with architecture and ROI

**Consulting Workflow:**
1. **Hearing & Current State Assessment** - Understand industry, department, company size, specific challenges, existing systems, goals/KPIs, budget, technical skills
2. **Problem Analysis & Goal Setting** - Identify key issues, define success metrics, organize constraints, identify risks
3. **Knowledge Selection & Loading** - Load appropriate references (industry + function + scenario + agent type + case studies)
4. **AI Adoption Proposal Creation** - Executive summary, current analysis, AI utilization proposal (use cases, architecture, data flow), expected effects (quantitative & qualitative), implementation plan (3 phases), investment breakdown, risks & countermeasures, recommendations
5. **Follow-up & Q&A** - Technical details, alternative options, customization, additional case studies

**Proposal Components:**
- Executive Summary with ROI
- Current State Analysis
- AI Utilization Proposal (Technology, Use Cases, Architecture, Data Flow)
- Expected Effects (Cost reduction %, Efficiency improvement %, Quality metrics)
- 3-Phase Implementation Plan (Pilot → Full Deployment → Continuous Improvement)
- Investment Breakdown (Initial, Operational, TCO, ROI calculation)
- Risk Assessment & Mitigation
- Best Practices & Recommendations

**Example Proposals:**
- **Retail CX Enhancement**: Personalized recommendations, 24/7 chatbot support, review analysis, dynamic pricing → 20% conversion rate increase, 15% cart abandonment reduction, 30% satisfaction improvement
- **Startup Sales Efficiency**: AI lead generation/scoring, automated proposal creation, personalized sales emails, transcription/analysis → 50% prep time reduction, 25% deal closure rate increase, 2x monthly leads
- **Manufacturing Quality Control**: Image-based defect detection, sensor data anomaly detection, automated quality reports → 95%+ detection rate, 70% inspection time reduction, 30% quality cost reduction

**Key Principles:**
- Practice-oriented with specific implementation methods
- Quantified effects (ROI, cost reduction, efficiency improvement)
- Phased approach (Pilot → Deployment → Improvement)
- Risk management (technical, organizational, legal)
- Human-centric (AI augments human capabilities)

**Knowledge Resources** (27 files, 162KB):
- 5 industry guides
- 5 function guides
- 5 scenario guides
- 4 agent type guides
- 6 detailed case studies
- README with AI adoption trends and success factors

**Key Features:**
- **Comprehensive Knowledge** - 27 curated use case documents
- **Multi-dimensional Analysis** - Industry × Function × Scenario combinations
- **Quantified Benefits** - All proposals include ROI and cost reduction metrics
- **Practical Examples** - Real-world case studies with implementation details
- **Agent Type Expertise** - RAG, Voice, Video, Business Support recommendations
- **Bilingual**: Japanese and English support

---

### ☁️ Render CLI Expert

**File:** `skill-packages/render-cli-expert.skill`

Expert skill for managing Render cloud platform services via CLI. Supports deployments, log monitoring, SSH connections, PostgreSQL connections, and service management.

**When to use:**
- Deploying and managing Render services from the terminal
- Monitoring service logs in real-time
- Connecting to PostgreSQL databases via psql
- SSH remote connections to services
- Automating Render operations in CI/CD pipelines
- Listing workspaces and services

**Core Capabilities:**
- ✅ Service deployment with wait and confirmation options
- ✅ Real-time log monitoring and JSON output
- ✅ PostgreSQL database connections via psql
- ✅ SSH access to paid services
- ✅ CI/CD automation patterns (GitHub Actions, shell scripts)
- ✅ Workspace and service management

**Key Commands:**
| Command | Description |
|---------|-------------|
| `render login` | Interactive authentication |
| `render services` | List all services |
| `render deploys create` | Deploy a service |
| `render logs --tail` | Real-time log monitoring |
| `render psql` | Connect to PostgreSQL |
| `render ssh` | SSH into service |
| `render restart` | Restart a service |

**CI/CD Integration:**
```bash
# Environment variable authentication
export RENDER_API_KEY=rnd_xxx...

# Deploy with wait and auto-confirm
render deploys create srv-abc123 --wait --confirm
```

**Auto-Update Feature:**
- Automatic documentation check every month
- Manual update: `python3 scripts/render_cli_updater.py`
- Force update: `python3 scripts/render_cli_updater.py --force`

**Best Practices:**
- Use `RENDER_API_KEY` environment variable for CI/CD
- Use `--wait` flag to confirm deployment completion
- Use `-o json` for automation scripts
- Use `--confirm` to skip confirmation prompts

**Resources:**
- `scripts/render_cli_updater.py` - Auto-update checker script
- `references/cli_updates.md` - Latest update log
- `references/last_check.json` - Last check timestamp

---

### 🔍 Design Implementation Reviewer

**File:** `skill-packages/design-implementation-reviewer.skill`

A critical code review skill focused on whether code actually works correctly—not just whether it matches a design document.

**When to use:**
- Critical code review sessions
- Verifying implementation against requirements
- Finding bugs the design didn't anticipate
- Reviewing data pipelines and ETL processes

**Core Capabilities:**
- ✅ Three-layer review framework (Code Quality → Execution Flow → Goal Achievement)
- ✅ Concurrency, idempotency, and transaction boundary checks
- ✅ Resource management and timeout/retry logic verification
- ✅ API contract and backward compatibility analysis
- ✅ Design gap identification

**Key Features:**
- Always uses `ultrathink` mode for thorough analysis
- Security review is out of scope (use dedicated security skill)
- Structured output: Review Scope → Findings → Open Questions
- Test Plan required for Critical/High severity findings

---

### 🎬 Video2Minutes

**File:** `skill-packages/video2minutes.skill`

Automatically transcribes video files and generates structured meeting minutes.

**When to use:**
- Converting meeting recordings to text
- Creating meeting minutes from video content
- Extracting key points and action items from recorded discussions

**Core Capabilities:**
- ✅ Video transcription using Whisper
- ✅ Automatic meeting minutes generation
- ✅ Key points and action items extraction

---

### 🔍 Migration Validation Explorer

**File:** `skills/migration-validation-explorer/SKILL.md`

Exploratory data-migration validation and QA ideation workflow for CRM migrations. Surfaces hidden data quality risks and generates prioritized QA backlogs with automated testing.

**When to use:**
- Validating data migration projects (especially CRM migrations)
- Discovering hidden data quality risks
- Generating new validation angles from mapping specs
- Automated data profiling and hypothesis testing
- Exploring validation gaps in migration datasets

**Core Capabilities:**
- ✅ **4-Perspective Hypothesis Generation** (Domain, Tech, Edge Case, Statistical)
- ✅ **Priority Scoring** (Impact × Probability × Testability)
- ✅ **Automated Scripts** for profiling, testing, and lens combination
- ✅ Cross-pollination with operators (AND/XOR/SEQ/REQ)
- ✅ QA backlog generation with risk prioritization

**4-Perspective Framework:**

| Icon | Perspective | Focus Area |
|:----:|-------------|------------|
| 🏢 | Domain Expert | Business rules, compliance |
| 💻 | Tech Implementer | Code bugs, transforms |
| 🔍 | Edge Case Hunter | Boundaries, special cases |
| 📊 | Statistical Skeptic | Distributions, outliers |

**Automation Scripts:**
- `scripts/exploratory_profiler.py` - Data profiling with null rates, distributions
- `scripts/hypothesis_tester.py` - Reference integrity, value concentration tests
- `scripts/perspective_combiner.py` - Lens catalog and random combinations

**Workflow:**

| Step | Description |
|------|-------------|
| Step 0 | Preparation (Mission, Focus Catalog, Initial Profiling) |
| Step 1 | Random Focus Cycle x10 (4-perspective diverge → prioritize → verify) |
| Step 2 | Cross-Pollination x10 (Lens fusion with operators) |
| Step 3 | Converge into QA Backlog |

**Example Use Cases:**
- "Profile this migration dataset and find potential issues"
- "Generate hypotheses from 4 perspectives for Account data"
- "Test reference integrity between Contacts and Accounts"
- "Create a prioritized QA backlog for go-live"

---

### 📞 Helpdesk Responder

**File:** `skills/helpdesk-responder/SKILL.md`

Generic helpdesk first-response skill for creating KB-based response drafts. Adaptable to any industry or product support context.

**When to use:**
- Handling customer support tickets or inquiries
- Creating response drafts based on knowledge base articles
- Building a structured helpdesk workflow
- Training support staff on response patterns

**Core Capabilities:**
- ✅ Auto-detection patterns (error codes, keywords, symptoms)
- ✅ Confidence scoring for response selection (High/Medium/Low)
- ✅ Multi-language response templates (English/Japanese)
- ✅ KB index configuration with JSON schema
- ✅ Escalation workflow with handoff format

**Workflow:**

| Phase | Description |
|-------|-------------|
| Phase 1 | Inquiry Analysis (extract info, detect patterns, categorize) |
| Phase 2 | KB Search & Matching (confidence scoring, article prioritization) |
| Phase 3 | Response Draft Generation (template selection, variable substitution) |

**Confidence Thresholds:**
- High (>=80%): Provide solution directly
- Medium (50-79%): Request additional information
- Low (<50%): Escalate for investigation

**Key Components:**
- `references/kb_schema.json` - Complete JSON schema for KB index configuration
- `assets/response_templates.md` - Ready-to-use response templates (7 scenarios)

**Example Use Cases:**
- "Create a response draft for ticket #1234"
- "Handle this customer inquiry about error code 30001"
- "Generate a Japanese response for this support request"
- "Set up a KB-based helpdesk workflow for my product"

---

### 🎬 FFmpeg Expert

**File:** `skill-packages/ffmpeg-expert.skill`

A comprehensive FFmpeg CLI skill for multimedia processing - video/audio conversion, editing, and optimization.

**When to use:**
- Converting video formats (MP4, WebM, MKV, MOV, AVI)
- Transcoding codecs (H.264, H.265/HEVC, VP9, AV1, ProRes)
- Trimming, cutting, or merging videos
- Extracting or converting audio (MP3, AAC, FLAC, WAV)
- Creating GIFs from video
- Generating thumbnails
- Preparing for streaming (HLS/DASH)
- Using hardware acceleration (NVENC, QSV, VideoToolbox)
- Applying filters (blur, color correction, subtitles, watermarks)

**Key Components:**
- `references/quick_reference.md` - Copy-paste ready commands
- `references/codec_guide.md` - Codec selection guide (H.264, H.265, VP9, AV1)
- `references/filter_reference.md` - Filter syntax and examples
- `references/troubleshooting.md` - Common errors and solutions
- `scripts/ffprobe_analyzer.py` - Media analyzer with encoding recommendations

**Example Use Cases:**
- "Convert this video to MP4"
- "Extract audio from video"
- "Create a GIF from 1:00 to 1:10"
- "Compress with H.265"
- "Add a watermark"
- "Prepare for HLS streaming"

---

### 📊 Lean Six Sigma Consultant

**File:** `skill-packages/lean-six-sigma-consultant.skill`

Comprehensive Lean Six Sigma consulting skill supporting all belt levels (White Belt to Master Black Belt).

**When to use:**
- Leading or supporting process improvement projects
- DMAIC/DMADV methodology guidance
- Lean waste elimination (VSM, 8 Wastes/DOWNTIME, 5S)
- Statistical analysis (process capability Cp/Cpk, control charts, hypothesis testing)
- Root cause analysis (5 Whys, Fishbone)
- Six Sigma training and certification preparation

**Key Components:**
- `references/methodology/` - DMAIC, DMADV, Lean principles
- `references/tools-by-phase/` - Define, Measure, Analyze, Improve, Control
- `references/statistics/` - Control charts, hypothesis testing, process capability
- `references/lean-tools/` - 5S, VSM, Kaizen, 8 Wastes
- `scripts/sigma_calculator.py` - Calculate sigma level and DPMO
- `scripts/control_chart_analysis.py` - Control chart generation and analysis
- `scripts/process_capability.py` - Cp/Cpk calculation

**Example Use Cases:**
- "Guide me through a DMAIC project to reduce defects"
- "Calculate the Cpk for this process data"
- "Create a value stream map for our order fulfillment"
- "What control chart should I use for defect counts?"
- "Explain the 8 wastes in our service process"

---

### 🦆 DuckDB Expert

**File:** `skill-packages/duckdb-expert.skill`

Expert skill for large-scale data analysis using DuckDB - the embedded OLAP database.

**When to use:**
- Querying large CSV, Parquet, JSON files directly
- Analyzing datasets that don't fit in memory
- Building ETL pipelines with SQL
- Integrating with pandas/Polars
- Building file-based data warehouses
- Optimizing complex analytical queries

**Key Components:**
- `references/duckdb_functions_reference.md` - Function reference
- `references/file_formats_guide.md` - CSV, Parquet, JSON handling
- `references/performance_tuning_guide.md` - Query optimization
- `scripts/duckdb_analyzer.py` - Data analysis automation
- `scripts/etl_pipeline.py` - ETL pipeline utilities

**Example Use Cases:**
- "Analyze this 10GB Parquet file"
- "Query multiple CSV files with a wildcard pattern"
- "Optimize this slow analytical query"
- "Build an ETL pipeline for data transformation"

---

### 🔍 Critical Code Reviewer

**File:** `skill-packages/critical-code-reviewer.skill`

Self-contained multi-persona code review skill using four expert perspectives for thorough quality assessment. Agent prompts are embedded in the skill package — no external dependencies required.

**Reviewer Personas:**
| Persona | Focus | Key Question |
|---------|-------|--------------|
| **Veteran Engineer** (20年経験) | Design decisions, anti-patterns, maintainability | "Can this be maintained in 5 years?" |
| **TDD Expert** | Testability, dependency management, refactoring safety | "Can this be tested in isolation?" |
| **Clean Code Expert** | Naming, readability, SOLID principles | "Can this be understood at a glance?" |
| **Bug Hunter** | State transitions, exception paths, async race conditions | "How does this break in production?" |

**When to use:**
- Reviewing source code from multiple expert perspectives
- Finding design flaws, testability issues, and runtime bugs
- Assessing code quality and maintainability
- Python/JavaScript gets Tier 1 deep checks; IaC/Config files also supported

**Key Components:**
- `references/agents/*.md` - 4 embedded persona prompts (self-contained)
- `references/code_smell_patterns.md` - Code smells and anti-patterns
- `references/review_framework.md` - Critical analysis framework
- `references/severity_criteria.md` - Severity judgment criteria
- `references/file_type_classification.md` - File type auto-classification with content sniffing
- `references/scale_strategy.md` - Large codebase hotspot extraction strategy

---

### 📄 Critical Document Reviewer

**File:** `skill-packages/critical-document-reviewer.skill`

Self-contained multi-persona document review skill for rigorous validation of claims and evidence. Agent prompts are embedded in the skill package — no external dependencies required.

**Reviewer Personas (up to 6, selected by document type):**
| Persona | Focus |
|---------|-------|
| **Developer/Implementer** | Can I implement based on this? Technical accuracy? |
| **Project Manager** | Risks? Consistency? Feasibility? Dependencies? |
| **Customer/Stakeholder** | Does this meet requirements? Understandable? Business value? |
| **QA/Tester** | Can this be tested? Are acceptance criteria clear? |
| **Security/Compliance** | Authentication, data protection, regulatory compliance? |
| **Operations/SRE** | Monitoring, failure recovery, operational readiness? |

**When to use:**
- Reviewing design documents, analysis reports, or proposals
- Validating claims have proper evidence
- Detecting unsupported claims and logical gaps
- Finding missing traceability to requirements
- Security/operations review of technical documents

**Key Components:**
- `references/agents/*.md` - 6 embedded persona prompts (self-contained)
- `references/severity_criteria.md` - Document review severity criteria
- `references/red_flag_patterns.md` - Dangerous expression patterns (context-sensitive)
- `references/persona_selection_matrix.md` - Document type to persona mapping
- `references/scale_strategy.md` - Large document review strategy

---

### 🎨 Design Thinking

**File:** `skill-packages/design-thinking.skill`

Human-centered innovation and problem-solving skill based on Stanford d.school / IDEO methodology.

**5 Phases:**
```
EMPATHIZE → DEFINE → IDEATE → PROTOTYPE → TEST
   共感    →  定義  →  発想  →   試作   → 検証
```

**When to use:**
- New service/product planning
- Customer experience (CX/UX) improvement
- Problem redefinition ("What problem should we really solve?")
- Innovation creation and brainstorming facilitation

**Key Components:**
- `references/empathize_methods.md` - User research methods
- `references/define_methods.md` - Problem framing (HMW, POV)
- `references/ideate_methods.md` - Brainstorming techniques
- `references/prototype_methods.md` - Rapid prototyping
- `references/test_methods.md` - User testing methods
- Templates: Persona, Empathy Map, Journey Map, Ideation Canvas

---

### 📊 DAMA-DMBOK

**File:** `skill-packages/dama-dmbok.skill`

Data management skill based on DAMA-DMBOK (Data Management Body of Knowledge).

**11 Knowledge Areas:**
- Data Governance (central/governing)
- Data Quality, Data Architecture, Data Security
- Reference & Master Data Management (MDM)
- Data Integration, Metadata Management
- Data Modeling, DWH & BI, Data Storage
- Document & Content Management

**When to use:**
- Data strategy development
- Data governance framework implementation
- Data quality improvement
- Data catalog creation
- MDM implementation
- Data migration projects
- Data maturity assessment

**Key Components:**
- `references/data_governance.md` - Governance framework
- `references/data_quality.md` - Quality dimensions and improvement
- `references/metadata_management.md` - Metadata standards
- `references/master_data_management.md` - MDM patterns
- Templates: Governance Charter, Maturity Assessment, Data Catalog

---

### 🔧 TDD Developer

**File:** `skill-packages/tdd-developer.skill`

Test-Driven Development methodology skill for writing tests before implementation.

**TDD Cycle:**
```
RED → GREEN → REFACTOR
(Write failing test → Make it pass → Improve code)
```

**When to use:**
- User requests TDD or test-first development
- Building new features requiring high reliability
- Refactoring legacy code with test coverage
- Implementing complex business logic
- Learning TDD methodology

**Key Components:**
- `references/tdd_methodology.md` - TDD principles and workflow
- `references/test_patterns.md` - Common testing patterns

---

### 📈 QA Bug Analyzer

**File:** `skill-packages/qa-bug-analyzer.skill`

Bug ticket analysis skill for quality trends, hotspot detection, and improvement recommendations.

**When to use:**
- Analyzing bug ticket data (CSV, Excel, JSON, Markdown)
- Quality assessment for project reviews or release readiness
- Trend analysis over time
- Generating stakeholder reports
- Identifying improvement priorities

**Key Components:**
- `scripts/analyze_bugs.py` - Automated bug analysis
- `references/analysis_methodology.md` - Analysis approach
- `references/quality_metrics_guide.md` - Quality metrics
- `assets/report_template.md` - Report format

**Example Use Cases:**
- "Analyze bug trends from this CSV"
- "Generate a quality report for project management"
- "Which modules have the most bugs?"
- "What areas should we focus on for improvement?"

---

### 📑 UAT Testcase Generator

**File:** `skill-packages/uat-testcase-generator.skill`

Generates UAT (User Acceptance Testing) test cases in Excel format for Salesforce CRM projects.

**When to use:**
- Creating standardized UAT test cases for Salesforce projects
- Generating Excel files with summary and detailed test cases
- Documenting test scenarios, preconditions, steps, and expected results

---

### 🔄 Docling Converter

**File:** `skill-packages/docling-converter.skill`

Document conversion skill using the docling CLI - convert any document to Markdown and other formats.

**Supported Input:** PDF, DOCX, PPTX, HTML, Images, Excel
**Supported Output:** Markdown, JSON, YAML, HTML, Text

**When to use:**
- Converting documents to Markdown
- Extracting text from PDFs
- Processing scanned documents with OCR
- Converting office documents

**Example:**
```
/docling-converter document.pdf --to md --ocr-lang ja
```

---

### ☁️ AWS CLI Expert

**File:** `skill-packages/aws-cli-expert.skill`

AWS CLI expert skill for cloud infrastructure management and operations.

**Key Components:**
- `references/aws_cli_essentials.md` - Core CLI usage
- `references/iam_guide.md` - IAM and security
- `references/security_best_practices.md` - Security guidelines

---

### ☁️ gogcli Expert

**File:** `skill-packages/gogcli-expert.skill`

Expert skill for gogcli (steipete/gogcli), a Go-based CLI tool for managing 13 Google Workspace services from the terminal.

**When to use:**
- Managing Gmail (search, send, labels, filters, vacation)
- Calendar operations (events, conflicts, free/busy, recurring events)
- Drive file operations (list, upload, download, export, permissions)
- Sheets data reading/writing (A1 notation, append, formatting)
- Docs/Slides export (PDF, DOCX, PPTX via Drive export)
- Tasks management (create, complete, recurring)
- Workspace admin (Groups, Classroom, People, Contacts)
- Setting up OAuth2 / service account authentication
- Multi-account and multi-client configuration

**Core Capabilities:**
- 13 Google Workspace services: Gmail, Calendar, Drive, Sheets, Docs, Slides, Contacts, Tasks, Chat, Groups, Keep, Classroom, People
- OAuth2 + Service Account authentication with scope control
- Multi-account management with aliases and domain mapping
- `--json` / `--plain` output for pipeline integration
- Command sandboxing with `--enable-commands` for agent safety

**Key Components:**
- `references/quick_reference.md` - All 13 services command cheat sheet
- `references/communication_services.md` - Gmail/Calendar/Chat detailed guide
- `references/productivity_services.md` - Drive/Sheets/Docs/Slides/Tasks/Keep detailed guide
- `references/workspace_admin_services.md` - Groups/Classroom/People + service account guide
- `references/troubleshooting.md` - Comprehensive troubleshooting guide

---

### ☁️ Salesforce CLI Expert

**File:** `skill-packages/salesforce-cli-expert.skill`

Salesforce CLI (sf/sfdx) expert skill for Salesforce development and administration.

**When to use:**
- Authenticating to orgs
- Querying data with SOQL
- Retrieving metadata (profiles, permission sets, security settings)
- Deploying configuration changes
- Automating security audits

---

### 🤖 Codex Reviewer

**File:** `skill-packages/codex-reviewer.skill`

Uses OpenAI Codex CLI to review documents and code with GPT-5.1-Codex-Max model.

**When to use:**
- Code review requiring deep analysis
- Document review
- Design document review
- Test plan review

---

### 📊 Markdown to PDF

**File:** `skill-packages/markdown-to-pdf.skill`

Converts Markdown documents to professional PDF with two rendering modes: (1) fpdf2 mode for business documents with cover pages, themed styling, and styled tables, (2) Playwright mode for technical documentation with Mermaid diagram support.

**When to use:**
- Creating professional business PDFs (estimates, proposals, reports)
- Converting Markdown with cover pages and themed headers/footers
- Converting technical documentation with Mermaid diagrams
- Extracting Mermaid diagrams as images

**Key Components:**
- `scripts/markdown_to_fpdf.py` - Professional PDF (fpdf2, cover pages, themes, tables)
- `scripts/markdown_to_pdf.py` - Mermaid-aware PDF (Playwright/HTML/CSS)
- `scripts/themes.py` - Theme definitions and CJK font discovery
- `scripts/mermaid_to_image.py` - Mermaid to PNG/SVG

---

### 📋 Meeting Asset Preparer

**File:** `skills/meeting-asset-preparer/`

Prepares comprehensive meeting assets including agendas, reference materials, decision logs, and follow-up action items. Integrates with project context to pull relevant documents, estimates, and implementation differences. Supports bilingual (Japanese/English) output for cross-regional meetings.

**When to use:**
- Preparing assets for an upcoming project meeting or status review
- Creating bilingual meeting documentation for cross-regional teams
- Compiling reference materials from estimates, specs, and implementation docs
- Generating structured agendas with time allocations
- Setting up decision log and action item tracking templates

**Key Components:**
- `scripts/prepare_meeting.py` - Main CLI for meeting asset preparation (init, compile-refs, generate-agenda, create-decision-log, create-action-items, package)
- `references/meeting-best-practices.md` - Best practices for effective meeting preparation
- `assets/agenda_template.md` - Bilingual agenda template
- `assets/decision_log_template.md` - Bilingual decision log template
- `assets/action_items_template.md` - Bilingual action items template

**Key Features:**
- Bilingual support (Japanese/English) for cross-regional teams
- Context integration from project documents (estimates, specs, prior notes)
- Structured templates for agendas, decision logs, and action items
- Time allocation in agendas for focused meetings
- Meeting package generation with index document

---

### 📝 Meeting Minutes Reviewer

**File:** `skills/meeting-minutes-reviewer/`

Reviews meeting minutes documents for completeness, action item clarity, decision documentation, and consistency with source materials. Generates structured feedback with specific improvement suggestions and quality scores across 5 dimensions.

**When to use:**
- After drafting meeting minutes and before distribution
- When reviewing minutes created by others for quality assurance
- When validating that minutes accurately reflect source materials (hearing sheets, transcripts)
- When ensuring action items meet trackability standards
- When preparing minutes for formal project documentation or audit trails

**Key Components:**
- `scripts/review_minutes.py` - Main review script with 5-dimension quality analysis
- `references/review-criteria.md` - Detailed scoring criteria and quality standards
- `references/meeting-minutes-checklist.md` - Complete checklist for meeting minutes

**Key Features:**
- 5-dimension scoring: Completeness (25%), Action Items (25%), Decisions (20%), Consistency (15%), Clarity (15%)
- Action item validation: owner, deadline, description completeness
- Decision documentation check: context, rationale, alternatives
- Source material consistency verification (hearing sheets, agendas)
- Vague language detection and clarity analysis
- JSON and Markdown report output formats

---

### 📝 Meeting Minutes Writer

**File:** `skills/meeting-minutes-writer/`

Generates strategic-consultant-grade meeting minutes from transcripts or notes, then runs a self-review loop (max 3 iterations) that checks for internal contradictions, action-item omissions, speaker-name errors, and date/day-of-week mistakes before reporting completion.

**When to use:**
- Converting raw meeting transcripts or notes into structured minutes
- Producing executive-readable minutes (3-minute readability test)
- Any time minutes must include verified dates and complete action items
- When you need quality-gated output (zero findings or 3 iterations) before sharing

**Key Components:**
- `references/output_format.md` - Canonical minutes structure, inference rules, ambiguity markers
- `references/self_review_checklist.md` - 5 Mandatory Checks with severity model and iteration logic
- `assets/minutes_template_en.md` - Blank meeting minutes template (English)
- `assets/minutes_template_ja.md` - 議事録テンプレート（日本語）
- `assets/findings_report_template.md` - Per-iteration findings report layout (bilingual EN + JA)

**Key Features:**
- 2-phase workflow: ultrathink Generation → Self-Review Loop (max 3 iterations)
- 5 Mandatory Checks: Internal Contradictions, Consistency, Action-Item Omissions, Speaker-Name Errors, Date/Day-of-Week Errors
- MANDATORY date verification via `python3 -c "import datetime; ..."` (no memory-based dates)
- Severity model: HIGH (blocks completion) / MEDIUM / LOW
- Completion report surfaces remaining HIGH findings and `* To be confirmed` items
- Complements `meeting-minutes-reviewer` (review-only) and `video2minutes` (transcribe-then-write)

---

### 🎤 Fujisoft Presentation Creator

**File:** `skill-packages/fujisoft-presentation-creator.skill`

Creates professional presentations following FUJISOFT America's slide template standards.

**When to use:**
- Creating business presentations
- Proposal materials
- MARP-format Markdown presentations

---

### 📊 Office Script Expert

**File:** `skills/office-script-expert/`

Office Scripts（Excel Online / Microsoft 365）開発の専門スキル。プラットフォーム制約、ExcelScript APIパターン、テスト戦略、本番開発で発見された13のバグパターンをカバー。

**When to use:**
- Office Scripts（TypeScript）でExcel Onlineの自動化スクリプトを開発する
- ExcelScript APIのパターンや制約を確認する
- Office Scripts特有のバグパターンを回避する
- lib/抽出 + インライン化のアーキテクチャでテスト可能なコードを書く

**Key Features:**
- 6つの重要プラットフォーム制約（P1-P6）: import不可、外部ライブラリ不可、120秒タイムアウト等
- lib/抽出 + Vitestによるテスト戦略
- 13の実運用バグパターンと回避策
- ExcelScript API パターン集（シート読み書き、CSV解析、保護/解除、日付変換等）
- 実装前チェックリスト

**Reference Guides:**
- `excel_api_patterns.md` - ExcelScript API の9つの主要パターン
- `common_bug_patterns.md` - 13の実運用バグパターン
- `platform_limitations.md` - 6つの重要プラットフォーム制約
- `testing_strategy.md` - lib/抽出 + Vitest テスト戦略

**Assets:**
- `implementation_checklist.md` - デプロイ前の実装チェックリスト

---

### 🌐 Network Diagnostics

**File:** `skills/network-diagnostics/`

ネットワーク品質を総合的に診断し、ボトルネックの特定と根本原因の深堀りまで行うスキル。OS標準ツールのみ使用（外部依存なし）、macOSおよびLinux対応。

**When to use:**
- ネットワーク品質の総合診断
- 接続の遅延・速度低下の原因調査
- レイテンシ・帯域幅・ジッターの測定
- ネットワークヘルスレポートの生成

**Key Features:**
- 3-Phase ワークフロー: Collect → Analyze & Report → Deep-Dive
- 接続種別（Ethernet/Wi-Fi）対応の品質閾値判定
- 複数CDNによる速度テスト（Cloudflare, OVH, Hetzner）
- HTTP接続タイミング分解（DNS/TCP/TLS/TTFB）
- macOS/Linux クロスプラットフォーム対応（iproute2 + net-tools fallback）

**Scripts:**
- `network_diagnostics.py` - データ収集スクリプト（JSON出力、CLI対応）

**Reference Guides:**
- `network_quality_thresholds.md` - 品質閾値定義（接続種別×GOOD/WARNING/CRITICAL）
- `deep_dive_procedures.md` - 6カテゴリの深堀り調査手順

**Assets:**
- `network_report_template.md` - 日本語レポートテンプレート（罫線テーブル）

---

### 🌐 Network Incident Analyzer

**File:** `skills/network-incident-analyzer/`

Analyzes network device logs to identify connectivity issues, latency problems, and outages. Automatically correlates timestamps across timezones, detects anomaly patterns during specified time windows, and generates incident reports with root cause hypotheses.

**When to use:**
- Troubleshooting network connectivity issues using device logs
- Analyzing multiple log files from different network devices
- Investigating service outages with logs spanning multiple timezones
- Identifying patterns in network latency or packet loss
- Generating incident reports with root cause analysis

**Key Features:**
- Multi-format log parsing (Cisco IOS, JunOS, Palo Alto, F5, Syslog, JSON)
- Automatic timestamp normalization to UTC across timezones
- Anomaly detection (connection failure spikes, interface flapping, error rate spikes)
- Cross-device event correlation with configurable time windows
- Root cause hypothesis generation with confidence scoring
- JSON and Markdown report generation

**Scripts:**
- `analyze_network_logs.py` - Main analysis script with CLI interface

**Reference Guides:**
- `log-formats.md` - Supported log formats and parsing patterns
- `anomaly-patterns.md` - Anomaly detection patterns and thresholds

---

### 🔗 Multi-File Log Correlator

**File:** `skills/multi-file-log-correlator/`

Correlates events across multiple log files from different sources, systems, or time periods. Builds unified timelines, identifies causal relationships between events, and highlights anomalies that span multiple data sources. Supports timezone normalization and gap detection.

**When to use:**
- Investigating incidents involving multiple services (frontend, API, database, cache)
- Analyzing distributed system failures across microservices
- Building event timelines from logs with different timestamp formats
- Correlating infrastructure logs with application logs
- Detecting timing anomalies between system components
- Tracing request flows across multiple services

**Key Features:**
- Unified timeline construction from heterogeneous log sources
- Correlation ID tracking (request_id, trace_id, transaction_id, UUID)
- Temporal proximity correlation when explicit IDs are absent
- Timezone normalization (supports IANA timezone names)
- Gap detection with configurable thresholds
- Anomaly detection (timing anomalies, error bursts)
- JSON and Markdown report generation

**Scripts:**
- `correlate_logs.py` - Main correlation engine with CLI interface

**Reference Guides:**
- `correlation_methodology.md` - Correlation techniques and best practices
- `timestamp_formats.md` - Common log timestamp formats reference

---

### 🌊 Streamlit Expert

**File:** `skills/streamlit-expert/`

Streamlit Webアプリケーション開発の専門スキル。v1.42〜v1.52+の最新機能に対応。

**When to use:**
- Streamlitアプリの新規構築
- OIDC認証（Google, Microsoft, Okta, Auth0）の実装
- データ可視化ダッシュボードの作成
- パフォーマンス最適化（キャッシュ、セッション管理）

**Key Features:**
- 認証: `st.login()` / `st.logout()` / `st.user` によるネイティブOIDC
- 可視化: Plotly, Altair, ネイティブチャートの最適選択
- シークレット管理: `st.secrets` によるセキュアな資格情報管理
- パフォーマンス: キャッシュ戦略、大規模データセット処理
- モダン機能: カスタムテーマ、マルチページアプリ、Custom Components v2

---

### ✍️ AI Text Humanizer

**File:** `skills/ai-text-humanizer/`

AI（LLM）生成テキストの「AI臭」を検出・診断し、人間らしい文章にリライトするスキル。

**When to use:**
- AI生成テキストの品質チェック・改善
- 「AIっぽい」文章を人間らしくリライトしたいとき
- テキストがAI生成かどうかの簡易判定

**6つの検出パターン:**

| # | Pattern | Weight | Description |
|---|---------|--------|-------------|
| 1 | 視覚的マーカー残存 | 15% | `**太字**`、エムダッシュ、括弧過多、箇条書き過多 |
| 2 | 単調なリズム | 20% | 同一文末連続、接続詞過多、均一文長 |
| 3 | マニュアル的構成 | 20% | 長い前置き、構成宣言、ステップ表記、薄い結論 |
| 4 | 非コミット姿勢 | 15% | ヘッジ語、強制中立、断定回避、両論併記 |
| 5 | 抽象語の濫用 | 15% | 空疎な抽象語、根拠なき強評価、修飾語の空転 |
| 6 | 定型メタファー | 15% | 羅針盤、DNA、車の両輪、エンジン等の定型比喩 |

**3つの人間化技法:**
1. **バランスを崩す** — 立場を取る、強い断定を使う
2. **客観を崩す** — 主観・経験・判断を入れる
3. **論理を崩す** — 完璧な構造を壊す、自然な脱線を入れる

**Score Interpretation:**

| Score | Level | Action |
|-------|-------|--------|
| 0-25 | Natural | 修正不要 |
| 26-50 | Slightly AI | 軽微な修正で改善可能 |
| 51-75 | Clearly AI | リライト推奨 |
| 76-100 | Strongly AI | 全面リライト推奨 |

**Note:** 検出スクリプト (`detect_ai_patterns.py`) は日本語テキスト専用。英語テキストの場合はClaude自身が `references/` を参照して分析・リライトする。

### 🔍 Dual Axis Skill Reviewer

**File:** `skills/dual-axis-skill-reviewer/`

スキルの品質を二軸（Auto + LLM）で定量評価するレビュースキル。決定論的なコードベースチェック（構造、スクリプト、テスト、実行安全性）とLLMによる深層レビューを組み合わせ、再現性のあるスコアリングを提供する。

**When to use:**
- `skills/*/SKILL.md` の品質スコアリングが必要なとき
- マージゲートとしてスコア閾値（例: 90点以上）を設定したいとき
- 低スコアスキルの具体的改善項目を取得したいとき
- 別プロジェクトのスキルをクロスプロジェクトでレビューしたいとき

**Key Features:**
- Auto軸: メタデータ(20)、ワークフロー網羅(25)、実行安全性(25)、成果物(10)、テスト健全性(20)の5次元スコアリング
- LLM軸: スクリプトの正確性、リスク、保守性をJSON形式で評価
- 重み付き統合スコア（`--auto-weight` / `--llm-weight`で調整可能）
- `--all` オプションで全スキル一括レビュー＆サマリテーブル出力
- `--project-root` によるクロスプロジェクト対応
- knowledge_only スキルの自動判定（スクリプト不在でも不当減点を回避）
- 90点未満で改善項目を自動生成

---

### 📝 Business Plan Creator

**File:** `skills/business-plan-creator/`

事業計画書を体系的に作成するスキル。新規事業、既存事業拡大、スタートアップのピッチ資料、社内新規プロジェクト提案など、あらゆる事業計画のドキュメントを構造化して作成する。

**When to use:**
- 新規事業の事業計画書を作成したいとき
- 投資家向けピッチ資料や銀行融資申請書が必要なとき
- 社内稟議・新規事業提案書を作成したいとき
- 収支シミュレーションや市場分析を含む計画書が必要なとき

**Key Features:**
- 5フェーズワークフロー（ヒアリング → 分析 → 戦略設計 → 数値計画 → ドキュメント化）
- 7つの分析フレームワーク（TAM/SAM/SOM、PEST、5フォース、SWOT、BMC、リーンキャンバス、バリューチェーン）
- 財務モデリング（ユニットエコノミクス、3シナリオ分析、P/L・CF計画）
- 業種別テンプレート（SaaS、EC/D2C、コンサル、飲食、製造、AI、不動産）
- 標準構成（12セクション）と簡易構成（7セクション）の2パターン
- 日本語・英語の両言語対応

---

### 🔍 Audit Document Checker

**File:** `skills/audit-doc-checker/`

Review audit-related documents against 12 quality categories and produce a structured quality score (0-100) with severity-rated findings.

**When to use:**
- Reviewing control design documents before submission to external auditors
- Checking quality of bottleneck analyses or risk assessment reports
- Verifying consistency across audit documentation (terminology, currency, accounting standards)
- Pre-publication quality gate for audit-context documents

**Key Features:**
- 12 check categories (terminology, currency, accounting standards, control logic, assertions, SoD, materiality, etc.)
- Severity-based scoring (High -5, Medium -3, Low -1 per finding)
- Document-type weighting (control design, bottleneck analysis, requirements, process inventory)
- 4-tier quality assessment (90+ High Quality, 70-89 Improvement Recommended, 50-69 Revision Required, <50 Critical Risk)
- Integration with audit-control-designer for generate→review workflow

---

### 🏗️ Audit Control Designer

**File:** `skills/audit-control-designer/`

Generate audit-ready internal control design documents from As-Is business process inventories.

**When to use:**
- Building internal controls from As-Is process inventories
- Designing controls for new audit engagements (SOX, J-SOX, PCAOB)
- Preparing for initial audit readiness assessment
- Strengthening existing control frameworks

**Key Features:**
- 5 business process patterns (AP, Inventory, COGS, Returns, Price Management)
- 8 control templates (T-AP-01/02, T-INV-01/02, T-CO-01, T-VAL-01, T-CALC-01/02)
- 5 audit assertion mapping (C/A/V/CO/E) with coverage assessment
- 5 SoD pair analysis with compensating controls for small organizations
- 8 KPI definitions (K01-K08) with baseline/target guidelines
- Materiality framework (Overall, Performance, Clearly Trivial)
- Accounting standards reference (US GAAP / IFRS / J-GAAP differences)
- Short-term (M+1~M+4) and medium-term (M+6~M+18) roadmap generation
- Industry customization (F&B, Retail, Manufacturing, Services)

---

## Installation

### Installing a Skill

1. Download the desired `.skill` file from `skill-packages/`
2. For Claude Desktop: Settings → Capabilities → Upload the `.skill` file
3. For Claude Code CLI: Copy the skill folder to `~/.claude/skills/`
4. The skill will be available for use immediately

### Skill Structure

Each skill follows this standard structure:

```
skill-name/
├── SKILL.md              # Main skill documentation and workflow
├── scripts/              # Automated tools and utilities
├── references/           # Methodology guides and best practices
└── assets/               # Templates and boilerplate files
```

## Development

### Creating New Skills

This repository uses the `skill-creator` tool from Anthropic's agent-skills marketplace.

**Prerequisites:**
- Claude Code installed
- `example-skills:skill-creator` plugin available

**Steps to create a new skill:**

1. Initialize skill structure:
   ```bash
   python /path/to/skill-creator/scripts/init_skill.py <skill-name> --path ./
   ```

2. Develop skill contents:
   - Edit `SKILL.md` with workflow and instructions
   - Add executable scripts to `scripts/`
   - Add reference documentation to `references/`
   - Add templates to `assets/`

3. Package the skill:
   ```bash
   python /path/to/skill-creator/scripts/package_skill.py ./skill-name ./
   ```

### Skill Development Best Practices

**SKILL.md Guidelines:**
- Use imperative/infinitive form (verb-first instructions)
- Include clear "When to Use" section with specific scenarios
- Provide concrete examples and workflows
- Reference bundled resources appropriately

**Resource Organization:**
- `scripts/` - Executable code that can run without loading to context
- `references/` - Documentation loaded on-demand to inform decisions
- `assets/` - Files used in output (templates, boilerplate)

**Quality Standards:**
- Follow progressive disclosure (metadata → SKILL.md → resources)
- Document domain knowledge and procedural steps
- Provide decision trees for complex workflows
- Include troubleshooting sections

## Contributing

Contributions are welcome! To contribute a new skill:

1. Fork this repository
2. Create your skill following the structure above
3. Test thoroughly with various use cases
4. Submit a pull request with:
   - Skill `.skill` file
   - Update to this README
   - Example usage scenarios

## License

[Specify your license here]

## Contact

For questions or suggestions, please open an issue in this repository.

---

## Detailed Skill Descriptions

### Data Scientist Skill - Deep Dive

#### Analysis Workflow

The data-scientist skill follows a systematic 7-step approach:

1. **Problem Definition & Scoping**
   - Translate business problems into data science problems
   - Define success criteria and constraints

2. **Data Understanding (EDA)**
   - Automated quality assessment
   - Distribution and relationship analysis
   - Correlation exploration

3. **Data Preparation & Feature Engineering**
   - Mathematical transformations
   - Categorical encoding
   - Interaction features
   - Time-based features
   - Domain-specific features

4. **Model Selection & Training**
   - Automated model comparison
   - Hyperparameter tuning
   - Cross-validation

5. **Model Evaluation & Interpretation**
   - Multiple metrics assessment
   - Feature importance analysis
   - SHAP value interpretation
   - Residual analysis

6. **Time Series Analysis** (when applicable)
   - Stationarity testing
   - Seasonal decomposition
   - Forecasting with confidence intervals

7. **Insights & Recommendations**
   - Translate findings to business impact
   - Generate professional reports
   - Provide actionable recommendations

#### Quick Start Examples

**Example 1: Customer Churn Prediction**

```bash
# Step 1: Automated EDA
python scripts/auto_eda.py customer_data.csv --target churned --output eda_results/

# Step 2: Model Comparison
python scripts/model_comparison.py customer_data.csv churned --problem-type classification --output models/

# Step 3: Review results and generate insights
```

**Example 2: Sales Forecasting**

```bash
# Time series analysis and forecasting
python scripts/timeseries_analysis.py sales.csv revenue --date-col date --forecast-periods 30 --output forecast/
```

**Example 3: Regression Analysis**

```bash
# Step 1: EDA
python scripts/auto_eda.py housing_data.csv --target price --output eda/

# Step 2: Model comparison
python scripts/model_comparison.py housing_data.csv price --problem-type regression --output models/
```

#### Advanced Features

**Handling Imbalanced Data:**
- SMOTE oversampling
- Class weight adjustment
- Appropriate metric selection (PR-AUC, F1, MCC)

**Feature Engineering Techniques:**
- Mathematical: Log, Box-Cox, polynomial
- Encoding: One-hot, target, frequency
- Interactions: Ratios, products
- Time: Lags, rolling stats, cyclical encoding
- Aggregations: Group statistics, rankings

**Model Interpretation:**
- Global: Feature importance, SHAP summary plots
- Local: SHAP values, LIME, counterfactuals
- Visualization: Comprehensive chart templates

#### Best Practices Built-In

✓ Proper train/test splits to avoid data leakage
✓ Cross-validation for robust evaluation
✓ Multiple metrics for comprehensive assessment
✓ Feature importance and model interpretation
✓ Documentation for reproducibility
✓ Business context integration
✓ Deployment considerations

✗ Common pitfalls actively prevented:
- Using accuracy on imbalanced data
- Test data leakage
- Ignoring outliers
- Over-engineering features
- Correlation-causation confusion

---

### Project Manager Skill - Deep Dive

#### Core Workflows

The project-manager skill provides 5 comprehensive workflows aligned with PMBOK® standards:

1. **Requirements Definition Workflow**
   - Systematic requirements gathering across stakeholders
   - Functional and non-functional requirements documentation
   - MoSCoW prioritization (Must/Should/Could/Won't Have)
   - Requirements traceability matrix
   - Change control process establishment
   - ISO/IEC/IEEE 29148 compliant templates

2. **Project Plan Review Workflow**
   - 10 PMBOK knowledge area checklist
   - 5 stakeholder perspective reviews
   - Gap identification and risk flagging
   - Red flag detection (e.g., no contingency, inadequate testing)
   - Comprehensive review report generation

3. **Progress Reporting with EVM Workflow**
   - Earned Value Management calculations (SPI, CPI, SV, CV)
   - Forecast metrics (EAC, ETC, VAC, TCPI)
   - Recovery action recommendations
   - Trend analysis and variance reporting
   - Professional progress report generation

4. **Risk Management Workflow**
   - Information gathering across 14 categories
   - Risk identification across 9 risk types
   - Probability × Impact scoring
   - Four response strategies (Avoid, Mitigate, Transfer, Accept)
   - Detailed response planning with preventive/detective/contingent actions
   - Risk monitoring and escalation triggers

5. **Cost Estimation Workflow**
   - Four estimation methods (Analogous, Parametric, Bottom-Up, Three-Point)
   - Component-based cost breakdown
   - Validation against benchmarks and historical data
   - Confidence range presentation (P10, P50, P90)
   - Contingency and management reserve allocation

#### Quick Start Examples

**Example 1: Requirements Definition**

```
User: "I need to create a requirements document for our new CRM system"

Claude (using project-manager skill):
1. Gathers project context through structured questions
2. Uses requirements_definition_template.md as foundation
3. Guides through functional and non-functional requirements
4. Applies MoSCoW prioritization
5. Creates traceability matrix
6. Generates comprehensive ISO-compliant requirements document
```

**Example 2: EVM Progress Analysis**

```
User: "Our project has these metrics: BAC=¥50M, PV=¥30M, EV=¥25M, AC=¥28M"

Claude (using project-manager skill):
1. Calculates SPI = 0.83 (17% behind schedule) 🔴
2. Calculates CPI = 0.89 (11% over budget) 🔴
3. Forecasts EAC = ¥56.2M (¥6.2M overrun)
4. Calculates TCPI = 1.14 (needs 14% efficiency improvement)
5. Status: CRITICAL (both schedule and cost issues)
6. Recommends recovery actions:
   - Fast-track activities on critical path
   - Value engineering to reduce costs
   - Immediate escalation to sponsor
7. Generates comprehensive progress report
```

**Example 3: Risk Assessment**

```bash
# Automated project health check
python scripts/project_health_check.py project_metrics.json --output report/

# Input: metrics.json with schedule, cost, quality, risk data
# Output:
# - Overall health score (0-100)
# - Status: Healthy 🟢 / At Risk 🟡 / Critical 🔴
# - Issue identification and recommendations
```

**Example 4: Project Plan Review**

```
User: "Review our project plan for a legacy system migration"

Claude (using project-manager skill):
1. Reviews across 10 PMBOK knowledge areas
2. Identifies gaps:
   - ❌ No knowledge transfer plan (high risk - tribal knowledge)
   - ❌ Testing only 10% of schedule (should be 25-30%)
   - ❌ No rollback plan for cutover
   - ❌ Insufficient contingency (5% vs 20% recommended)
3. Reviews from 5 stakeholder perspectives
4. Provides red flag warnings
5. Generates detailed review report with recommendations
```

#### Advanced Features

**Earned Value Management (EVM):**
- Complete EVM metric suite: PV, EV, AC, BAC, SV, CV, SPI, CPI, EAC, ETC, VAC, TCPI
- Three EAC calculation methods for different scenarios
- Performance index trending
- Integration with Agile (story point-based EVM)

**Risk Management:**
- 14 information gathering categories (scope, stakeholders, team, vendors, schedule, budget, etc.)
- 9 risk categorization types (scope, schedule, cost, quality, resource, stakeholder, technology, vendor, external)
- Quantitative risk scoring (probability × impact)
- Risk heat map visualization
- Preventive, detective, and contingent response planning
- Risk monitoring dashboard with trend indicators

**Cost Estimation Methods:**
- **Analogous:** Quick estimates based on historical projects
- **Parametric:** Statistical relationships (e.g., cost per story point)
- **Bottom-Up:** Detailed work package estimation
- **Three-Point:** PERT estimation with optimistic/most likely/pessimistic scenarios

**Stakeholder Management:**
- Stakeholder register with interest/influence matrix
- Tailored communication plans
- Engagement strategies for different stakeholder types
- Escalation paths and decision-making frameworks

#### PMBOK Knowledge Area Coverage

**Integration Management:**
- Project charter creation
- Integrated project plan development
- Change control process
- Lessons learned capture

**Scope Management:**
- WBS development
- Scope definition (in-scope/out-of-scope)
- Acceptance criteria definition
- Scope change management

**Schedule Management:**
- Activity sequencing
- Critical path analysis
- Schedule buffer allocation
- SPI tracking and recovery actions

**Cost Management:**
- Cost estimation (multiple methods)
- Budget baseline creation
- CPI tracking and EAC forecasting
- Contingency management

**Quality Management:**
- Quality standards definition
- Testing strategy (20-30% of schedule)
- Defect tracking and metrics
- Quality audits and reviews

**Resource Management:**
- RACI matrix creation
- Resource allocation and leveling
- Skill gap analysis
- Team development planning

**Communications Management:**
- Communication plan with frequency/format
- Stakeholder-specific reporting
- Escalation procedures
- Status reporting (🟢🟡🔴 indicators)

**Risk Management:**
- Three-phase approach (Information → Analysis → Response)
- Risk register maintenance
- Mitigation strategy development
- Risk monitoring and control

**Procurement Management:**
- Contract type selection (Fixed-price, T&M, Cost-plus)
- Vendor evaluation and management
- SLA definition and monitoring
- Contract administration

**Stakeholder Management:**
- Stakeholder identification and analysis
- Engagement strategy development
- Expectation management
- Conflict resolution

#### Best Practices Built-In

✓ Requirements signed off before design
✓ 15-20% schedule contingency buffer
✓ 10-20% cost contingency reserve
✓ Testing allocated 20-30% of schedule
✓ Weekly SPI/CPI tracking
✓ Risk register updated weekly
✓ C-level executive sponsor required
✓ Change control process mandatory
✓ Documentation and traceability maintained

✗ Common pitfalls actively prevented:
- Starting development without signed-off requirements
- No contingency reserves (schedule or cost)
- Inadequate testing time (<20%)
- Fixed-price contracts with unclear scope
- Ignoring critical path dependencies
- Weak executive sponsorship
- Missing change control process
- Risk management as afterthought

#### Real-World Examples

**Example 1: Enterprise CRM Implementation (¥50M, 12 months)**
- 247 requirements documented with MoSCoW prioritization
- 27 risks identified and managed (3 critical, 8 high, 16 medium/low)
- Monthly EVM tracking (SPI, CPI)
- Delivered 92% of Must Have requirements
- Finished 5% under budget
- CSAT increased from 7.2 to 8.9

**Example 2: Legacy System Migration (¥95M, 20 months)**
- Comprehensive risk assessment (34 risks)
- Critical mitigation: Hired retired developers for tribal knowledge
- Zero-downtime cutover with blue-green deployment
- Delivered 2 months late but within revised budget
- System performance exceeded targets (250K TPS vs 200K target)
- Stakeholder satisfaction: 9.2/10

---

### Business Analyst Skill - Deep Dive

#### Core Workflows

The business-analyst skill provides 5 comprehensive workflows aligned with BABOK® Guide v3 standards:

1. **Requirements Elicitation Workflow**
   - Stakeholder identification and engagement planning
   - Elicitation technique selection (6+ techniques)
   - Structured requirements gathering sessions
   - MoSCoW prioritization (Must/Should/Could/Won't Have)
   - Requirements documentation and review
   - Requirements validation and sign-off

2. **Business Process Analysis Workflow**
   - As-is process documentation with BPMN
   - Process metrics collection (cycle time, efficiency, error rate, cost)
   - Value stream mapping and waste identification (TIMWOOD)
   - Root cause analysis (5 Whys, Fishbone diagrams)
   - To-be process design with improvement opportunities
   - Process optimization recommendations

3. **Stakeholder Analysis and Engagement Workflow**
   - Stakeholder register creation
   - Power/Interest matrix analysis (4 quadrants)
   - Engagement strategy development per quadrant
   - RACI matrix for decision-making clarity
   - Communication plan with frequency and format

4. **Business Case Development Workflow**
   - Problem/opportunity definition with quantified impact
   - Options analysis with weighted scoring
   - Financial analysis (ROI, NPV, IRR, Payback Period)
   - Benefit realization planning
   - Professional business case document generation

5. **Gap Analysis Workflow**
   - Current state assessment (processes, systems, capabilities)
   - Future state vision definition
   - Gap identification with priority scoring
   - Roadmap development for closing gaps
   - Change impact assessment

#### Quick Start Examples

**Example 1: Requirements Elicitation**

```
User: "I need to gather requirements for our new employee portal"

Claude (using business-analyst skill):
1. Identifies stakeholders: HR team, employees, IT, managers
2. Creates Power/Interest matrix for engagement planning
3. Recommends elicitation techniques:
   - Workshops with HR (high interest/influence)
   - Surveys for employees (high volume)
   - 1:1 interviews with IT (technical validation)
4. Guides through structured requirements gathering:
   - User stories with acceptance criteria
   - Non-functional requirements (performance, security)
   - Business rules documentation
5. Applies MoSCoW prioritization
6. Generates comprehensive BRD using template
```

**Example 2: Business Process Analysis**

```
User: "Analyze our current order processing workflow - it's taking too long and has errors"

Claude (using business-analyst skill):
1. Documents as-is process with BPMN notation
   - 8 steps, 45 minutes avg processing time
   - 3 manual handoffs, 2 system switches
   - 15% error rate requiring rework

2. Identifies waste using TIMWOOD framework:
   - Waiting: 20 minutes between handoffs
   - Over-processing: Duplicate data entry in 3 systems
   - Defects: 15% error rate (data entry mistakes)

3. Performs root cause analysis:
   - Primary cause: No integration between systems
   - Secondary: Manual validation prone to errors

4. Designs to-be process:
   - Automated data integration (reduce to 2 systems)
   - Real-time validation at point of entry
   - Elimination of manual handoffs
   - Target: 10 minutes, <2% error rate

5. Quantifies improvement:
   - Time savings: 78% reduction (35 min per order)
   - Cost savings: ¥15M annually
   - Customer satisfaction: Expected +25%

6. Generates comprehensive process analysis report
```

**Example 3: Business Case Development**

```bash
# Financial analysis with sensitivity
python scripts/business_analysis.py financial \
  --investment 10000000 \
  --annual-benefit 3500000 \
  --annual-cost 500000 \
  --years 5 \
  --discount-rate 0.10 \
  --sensitivity

# Output:
# Net Annual Benefit: ¥3,000,000
# Payback Period: 3.3 years
# ROI (5 years): 50%
# NPV (5 years, 10%): ¥1,372,867
# IRR: 15.2%
#
# Sensitivity Analysis:
# Best Case (benefit +20%, cost -10%):  NPV ¥4,127,340
# Likely Case (base):                   NPV ¥1,372,867
# Worst Case (benefit -20%, cost +10%): NPV -¥1,381,606
#
# Recommendation: APPROVE - Positive NPV in likely case, acceptable risk profile
```

**Example 4: Stakeholder Analysis**

```
User: "Create a stakeholder analysis for our CRM implementation"

Claude (using business-analyst skill):
1. Creates stakeholder register:
   - CEO (High Power, High Interest) → Manage Closely
   - Sales Team - 50 users (High Interest, Medium Power) → Keep Informed
   - IT Ops (Medium Interest, High Power) → Keep Satisfied
   - Finance Director (Medium Interest, High Power) → Keep Satisfied

2. Analyzes attitudes:
   - CEO: Champion (actively promotes)
   - Sales Team: Neutral (wait and see)
   - IT Ops: Skeptical (concerned about support burden)
   - Finance: Supporter (sees cost benefits)

3. Develops engagement strategies:
   - CEO: Monthly 1:1 briefings, involve in key decisions
   - Sales: Bi-weekly demos, involve in UAT, address "WIIFM"
   - IT: Early technical collaboration, address concerns
   - Finance: Monthly cost reports, ROI tracking

4. Creates RACI matrix for key activities
5. Generates communication plan with frequency/format
6. Produces comprehensive stakeholder analysis document
```

**Example 5: Data Quality Profiling**

```bash
# Profile dataset for quality assessment
python scripts/business_analysis.py profile customer_data.csv --output quality_report.json

# Output:
# Data Quality Assessment
# =======================
# Overall Score: 67/100 (Needs Improvement)
#
# Completeness: 75% (25% missing values in email, phone)
# Accuracy: 60% (40% invalid email formats detected)
# Consistency: 80% (name formatting inconsistent)
# Timeliness: 50% (50% of records >2 years old)
# Validity: 85% (15% values outside expected ranges)
# Uniqueness: 90% (10% duplicate records found)
#
# Recommendations:
# 1. HIGH: Implement email validation at entry point
# 2. HIGH: Create data cleanup process for missing values
# 3. MEDIUM: Standardize name formatting
# 4. MEDIUM: Archive/purge records >2 years old
```

#### Advanced Features

**BABOK® Knowledge Area Coverage:**

**1. Business Analysis Planning & Monitoring:**
- Stakeholder analysis with engagement strategies
- Requirements management approach definition
- Change control process establishment
- Performance metrics tracking

**2. Elicitation & Collaboration:**
- 6+ elicitation techniques (interviews, workshops, surveys, observation, document analysis, prototyping)
- Facilitation best practices
- Conflict resolution approaches
- Collaborative decision-making frameworks

**3. Requirements Life Cycle Management:**
- Requirements traceability (Business Need → Business Req → Functional Req → Test Case)
- Change management and version control
- Requirements approval and sign-off processes
- Requirements reuse and templates

**4. Strategy Analysis:**
- SWOT analysis
- Porter's Five Forces
- Value chain analysis
- Business model canvas
- Strategic roadmap development

**5. Requirements Analysis & Design Definition:**
- Requirements specification and modeling
- MoSCoW prioritization
- Gap analysis techniques
- Business rules definition
- Data flow and entity relationship modeling

**6. Solution Evaluation:**
- Benefits realization tracking
- Performance measurement (KPIs)
- Solution validation and acceptance criteria
- Post-implementation review

**Financial Analysis Capabilities:**

The `business_analysis.py` script provides comprehensive financial analysis:

```python
# Calculate ROI
roi = ((total_benefit - total_cost) / total_cost) × 100

# Calculate NPV (Net Present Value)
npv = Σ(cash_flow / (1 + discount_rate)^year)

# Calculate IRR (Internal Rate of Return)
# NPV = 0, solve for discount rate

# Calculate Payback Period
payback = investment / annual_net_benefit

# Perform Sensitivity Analysis
# Best: benefit +20%, cost -10%
# Likely: base case
# Worst: benefit -20%, cost +10%
```

**Process Analysis Techniques:**

**BPMN Notation:**
- Swimlane diagrams with roles and handoffs
- Process flow with decision points
- System integration points
- Exception handling flows

**Value Stream Mapping:**
- Value-added time vs. total lead time
- Process efficiency calculation
- Waste identification (TIMWOOD framework)
- Bottleneck analysis

**TIMWOOD Waste Framework:**
- **T**ransportation: Unnecessary movement of data/materials
- **I**nventory: Work-in-progress backlogs
- **M**otion: Unnecessary user actions
- **W**aiting: Idle time between steps
- **O**ver-production: Creating outputs before needed
- **O**ver-processing: Unnecessary complexity
- **D**efects: Errors requiring rework

**Root Cause Analysis:**
- **5 Whys:** Iterative questioning to find root cause
- **Fishbone (Ishikawa) Diagram:** 6M categories (Man, Machine, Method, Material, Measurement, Mother Nature)

**Data Quality Framework:**

6 Dimensions of Data Quality:
1. **Accuracy:** Correctness of data values
2. **Completeness:** No missing critical values
3. **Consistency:** Uniformity across datasets
4. **Timeliness:** Data currency and relevance
5. **Validity:** Values within expected ranges
6. **Uniqueness:** No unintended duplicates

#### Requirements Engineering Best Practices

**Effective Requirements Characteristics (SMART):**
- **S**pecific: Clear and unambiguous
- **M**easurable: Success criteria defined
- **A**chievable: Technically and organizationally feasible
- **R**elevant: Aligned with business objectives
- **T**ime-bound: Delivery expectations clear

**Requirements Format:**
```
FR-001: Automated Order Validation
Priority: Must Have
User Story: As a sales rep, I want the system to automatically validate
           customer credit limits so that I can process orders faster and
           avoid bad debt

Acceptance Criteria:
- Given an order with total > customer credit limit
- When the order is submitted
- Then the system displays credit limit warning within 2 seconds
- And requires manager approval before proceeding

Business Value: Reduce bad debt by 80% (from ¥5M to ¥1M annually)
Dependencies: BR-003 (Credit check API integration)
Source: VP Sales, CFO
```

**MoSCoW Prioritization:**
- **Must Have:** Critical for go-live, non-negotiable
- **Should Have:** Important but not critical, defer if needed
- **Could Have:** Desirable, include if capacity allows
- **Won't Have:** Out of scope for this release

**Requirements Traceability Matrix:**
```
| Business Need | Business Req | Functional Req | Design Element | Test Case | Status |
|---------------|-------------|----------------|----------------|-----------|--------|
| Reduce bad debt | BR-001 | FR-005, FR-006 | Credit API | TC-025 | Approved |
```

#### Stakeholder Management Best Practices

**Power/Interest Matrix:**
```
           High Interest
                │
                │
 Keep Informed  │   Manage Closely
  (Bi-weekly    │   (Weekly 1:1,
   updates)     │    Key decisions)
                │
Low ────────────┼──────────── High
Power           │            Power
                │
    Monitor     │   Keep Satisfied
  (Monthly      │   (Monthly reports,
   summaries)   │    Avoid surprises)
                │
           Low Interest
```

**RACI Matrix Example:**
```
| Activity | Executive | Business Owner | BA | Project Manager | Dev Team |
|----------|-----------|----------------|-----|-----------------|----------|
| Approve scope | A | C | I | R | I |
| Gather requirements | I | C | R | C | I |
| Review design | I | C | A | C | R |
| UAT | I | R | C | A | I |
| Go-live decision | A | R | C | C | I |
```

Legend: R=Responsible, A=Accountable, C=Consulted, I=Informed

**Communication Plan Considerations:**
- Executive Sponsor: Strategic alignment, ROI, decisions needed (Monthly)
- End Users: "What's in it for me?", training, support (Bi-weekly)
- IT Teams: Technical approach, integration, support model (Weekly)
- Finance: Cost tracking, benefit realization (Monthly)

#### Business Case Components

**Problem/Opportunity Statement:**
- Quantified current state impact
- Qualitative impacts (morale, reputation)
- Cost of inaction

**Options Analysis:**
```
| Option | Weighted Score | Investment | NPV (5yr) | Risk |
|--------|---------------|-----------|----------|------|
| Option 1: COTS | 85/100 | ¥10M | ¥5.2M | Medium |
| Option 2: Custom | 78/100 | ¥15M | ¥6.8M | High |
| Option 3: Hybrid | 92/100 | ¥12M | ¥7.1M | Low |
```

**Benefit Realization Plan:**
- Quantitative benefits with measurement approach
- Qualitative benefits
- Benefit timeline (quick wins vs. long-term)
- Baseline and target metrics

**Risk Assessment:**
- Probability × Impact scoring
- Mitigation strategies
- Contingency reserves

#### Best Practices Built-In

✓ Stakeholder identification early and comprehensive
✓ Requirements elicited from multiple perspectives
✓ MoSCoW prioritization for scope management
✓ Requirements traceability maintained
✓ Financial analysis with sensitivity testing
✓ Process analysis with quantified improvements
✓ Data quality assessment before analysis
✓ Documentation following BABOK standards
✓ Change management approach integrated

✗ Common pitfalls actively prevented:
- Starting solution design before understanding problem
- Missing key stakeholders (discovering late)
- Assuming requirements without validation
- No requirements prioritization (everything is critical)
- Business cases without financial rigor
- Process analysis without data/metrics
- Ignoring change management and adoption
- Poor requirements documentation and traceability

#### Real-World Examples

**Example 1: Order Processing Automation (¥8M investment)**
- Problem: 45 min/order, 15% error rate, ¥25M annual cost
- Solution: Automated workflow with system integration
- Results:
  - Processing time: 10 min (78% reduction)
  - Error rate: <2% (87% reduction)
  - Annual savings: ¥15M
  - Payback: 6.4 months
  - ROI: 187% (3 years)
  - Customer CSAT: 7.1 → 8.8

**Example 2: CRM Implementation (¥12M investment)**
- 127 requirements documented (MoSCoW: 45/52/30/0)
- 23 stakeholders identified, engagement strategies per quadrant
- Financial analysis: NPV ¥18.2M (5 years), IRR 24.1%
- Process improvements: Sales cycle reduced 30%
- Delivered 94% of Must Have + Should Have requirements
- User adoption: 89% within 60 days
- Benefit realization: 112% of projected (over-achieved)

**Example 3: Data Quality Initiative**
- Problem: 40% of customer data incomplete/inaccurate
- Data profiling revealed: Completeness 60%, Accuracy 55%
- Root causes: No validation at entry, multiple legacy systems
- Solution: Data quality rules, stewardship program, consolidation
- Results:
  - Data quality score: 60 → 92 (over 12 months)
  - Marketing campaign effectiveness: +45%
  - Duplicate account reduction: 85%
  - Annual savings: ¥3.2M

### 🏭 Production Schedule Optimizer

**File:** `skill-packages/production-schedule-optimizer.skill`

Optimizes weekly production schedules for manufacturing facilities (central kitchens, food factories, production lines).

**When to use:**
- Creating weekly production schedules for central kitchens or food factories
- Auto-calculating production frequency based on shelf life
- Optimizing room capacity and staff allocation
- Estimating staff requirements and designing shift plans
- Identifying bottlenecks and improving schedule balance

**Key Features:**
- Greedy Bin-Packing scheduling with deterministic sort/tie-break
- 4-CSV input system (products, demand, rooms, staff)
- Shelf-life based production frequency calculation
- Staff requirement estimation with buffer coefficient
- PSO-E/W alert system for validation and quality monitoring
- Markdown timetable output

**Scripts:**
- `generate_schedule.py` - Weekly schedule generation CLI
- `estimate_staff.py` - Staff requirement estimation CLI

### 📋 Shift Planner

Generates weekly employee shift schedules from roster and requirements using constraint-satisfaction greedy assignment.

**When to use:**
- Creating individual shift schedules from staff requirements
- Auto-assigning employees based on qualifications, availability, and labor constraints
- Verifying shift coverage at 30-minute granularity
- Analyzing fairness across employees (hours deviation, weekend distribution)
- Working with production-schedule-optimizer output for downstream shift planning

**Key Features:**
- Constraint-satisfaction greedy assignment (difficulty-first slot ordering)
- 3-CSV input system (roster, requirements, optional shift patterns)
- Hard constraints: max hours/days, qualifications, consecutive days, rest hours
- Soft constraints: avoid days, preferred patterns, weekend balance
- 30-minute coverage verification with break exclusion
- Fairness metrics: hours deviation, weekend distribution, avoid violations
- SFT-E/W alert system (8 error codes, 10 warning codes)
- Built-in 5 shift patterns (FULL_8H, EARLY_8H, LATE_8H, SHORT_6H, HALF_4H)
- 25 test cases

**Scripts:**
- `generate_shifts.py` - Shift generation CLI

---

### 🔍 Incident RCA Specialist

Systematically analyzes incidents to identify root causes and develop corrective action plans. Focuses on organizational process improvement, not log-level debugging (use log-debugger for that).

**When to use:**
- Conducting post-incident reviews
- Creating incident reports and RCA documentation
- Developing corrective action plans with SMART criteria
- Performing organizational root cause analysis (5 Whys, Fishbone, FTA)
- Building incident timelines with TTD/TTR/TTM/TTRe metrics

**Key Features:**
- 8 workflows: Information Gathering → Timeline → Impact Assessment → 5 Whys → Fishbone → FTA → Corrective Actions → Report
- 5 Whys with branching technique and human error decomposition (never stop at "operator error")
- Fault Tree Analysis with AND/OR gates, minimal cut sets, SPOF identification
- 3D Prevention Framework (Detect/Defend/Degrade)
- P0-P4 severity matrix with SLA violation evaluation
- Mermaid gantt-based timeline with TTD/TTR/TTM/TTRe calculation
- Bilingual report templates (Japanese/English)
- Corrective action tracker with SMART criteria validation

---

### 🔄 Iterative Design Assistant

**File:** `skill-packages/iterative-design-assistant.skill`

Tracks design iteration history for documents and presentations, understands context from previous change requests, and applies consistent styling decisions across multiple revision cycles.

**When to use:**
- User references a previous design decision ("前回も色で良いんだけど", "like last time")
- Multiple revision cycles on the same document/presentation
- Need to track which design elements were changed and why
- Applying consistent styling across related documents
- Reviewing design history to understand document evolution
- User asks to "undo" or "revert" to a previous design state

**Key Features:**
- Session-local design decision log with JSON schema
- 5 decision categories: color, typography, layout, content, style
- Contextual reference resolution (Japanese/English patterns)
- Design token extraction and management
- Bidirectional traceability (decisions ↔ elements)
- Markdown/JSON history report generation

**Scripts:**
- `design_log.py` - CLI for init, record, query, search, apply, history, token, resolve

**References:**
- `design-decision-methodology.md` - Best practices for tracking and applying design decisions

**Example Use Cases:**
- "Use the same blue as before" → Resolves to most recent color decision
- "前回と同じフォントで" → Applies previous typography decision
- "Generate a history of all design changes" → Markdown report with timeline

---

### 📝 Technical Spec Writer

Creates structured technical specifications bridging requirements and implementation. Generates screen designs, API specs, DB designs, sequence diagrams, and state transition diagrams with Mermaid.

**When to use:**
- Creating functional specifications from BRD/requirements
- Designing screen layouts with UI element and event tables
- Creating REST API design documents
- Designing database schemas with ER diagrams
- Generating sequence and state transition diagrams

**Key Features:**
- 7 workflows: Requirements Intake → Screen Design → API Design → DB Design → Sequence Diagram → State Transition → Document Assembly
- IEEE 830 / ISO 29148 compliant specifications
- ID numbering system (SCR-xxx, API-xxx, TBL-xxx, SEQ-xxx, STS-xxx)
- Mermaid diagram patterns (sequence, state, ER, flowchart)
- REST API design guide with error codes, pagination, authentication
- DB design guide with normalization, indexing, audit columns
- Traceability matrix (REQ → SCR/API/TBL mapping)
- Bilingual templates (Japanese/English)

---

### 📋 Operations Manual Creator

Creates structured operations manuals and SOPs using the STEP format (Specific/Target/Expected/Proceed) with ANSI Z535-inspired caution/warning classification.

**When to use:**
- Creating operations manuals for business systems
- Writing standard operating procedures (SOPs)
- Creating user guides with step-by-step instructions
- Building troubleshooting guides with escalation procedures

**Key Features:**
- 6 workflows: Scope Definition → Operations Inventory → Procedure Writing → Caution/Warning Notes → Troubleshooting → Assembly
- STEP format: Specific action, Target UI element, Expected result, Proceed confirmation
- ANSI Z535 classification: DANGER/WARNING/CAUTION/NOTE with placement rules
- Operation ID system (OP-xxx) with dependency mapping
- Symptom-Cause-Resolution troubleshooting tables
- L1/L2/L3 escalation procedure templates
- Screenshot placeholders and annotation guidance
- Bilingual templates (Japanese/English)

---

### 🎯 CX Error Analyzer

Analyzes error/exception scenarios from a customer experience perspective, scoring them on 6 axes and prioritizing improvements using an Impact vs Effort matrix.

**When to use:**
- Evaluating error scenarios from CX perspective
- Improving error message quality and recovery flows
- Prioritizing error UX improvements
- Creating CX-focused error analysis reports

**Key Features:**
- 5 workflows: Error Inventory → Multi-Axis Evaluation → CX Scoring → Priority Matrix → Report
- 6-axis evaluation: Impact Severity (25%), Frequency (20%), Recovery Ease (15%), Message Quality (15%), Emotional Impact (10%), Business Cost (15%)
- CX Score tiers: Critical (4.0-5.0) / Significant (3.0-3.9) / Moderate (2.0-2.9) / Minor (1.0-1.9)
- Impact vs Effort matrix with Quick Wins identification
- Error UX best practices (message design, recovery flows, emotional design)
- CX metrics reference (CES/CSAT correlation, support cost, churn risk)
- ROI calculation for error UX improvements
- Error classification taxonomy and user journey mapping

---

### 📊 Management Accounting Navigator

Routes management accounting inquiries to the appropriate analysis skill by auto-classifying user requests into 12 management accounting domains. COSO/IMA framework aligned.

**When to use:**
- Determining which management accounting analysis to perform
- Routing budget variance, CVP, cost accounting inquiries
- Navigating across management accounting domains

**Key Features:**
- 12-domain auto-classification with routing to specialized skills
- COSO/IMA management accounting framework alignment
- Bilingual domain classification templates (Japanese/English)
- Covers: Budget variance, CVP, standard costing, KPI design, ABC, make-or-buy

---

### 💰 MA: Budget-Actual Variance Analysis

Analyzes budget vs actual variances with automatic favorable/unfavorable classification by account type (revenue/expense), variance decomposition, and root cause hypothesis generation.

**When to use:**
- Monthly/quarterly budget vs actual comparison
- Variance decomposition (price variance, quantity variance)
- Management reporting with variance ranking

**Key Features:**
- Auto favorable/unfavorable determination by account type
- Price and quantity variance decomposition
- Significance ranking and root cause hypothesis
- CSV data upload support
- Bilingual report templates (Japanese/English)

---

### 📈 MA: CVP / Break-Even Analysis

Performs Cost-Volume-Profit analysis including break-even point calculation, contribution margin analysis, margin of safety evaluation, and target profit simulation. Supports multi-product analysis.

**When to use:**
- Calculating break-even point (sales amount/volume)
- New business or pricing change profitability simulation
- Fixed cost reduction / variable cost improvement impact analysis
- What-if scenario analysis

**Key Features:**
- Fixed/variable cost structure analysis
- Break-even point calculation (amount and volume)
- Contribution margin ratio and margin of safety
- Target profit required sales simulation
- Multi-product CVP analysis support
- Bilingual templates (Japanese/English)

---

### 🏭 MA: Standard Cost Variance Analysis

Analyzes variances between standard (planned) costs and actual costs, decomposing into price and quantity variances across material, labor, and overhead categories.

**When to use:**
- Manufacturing cost variance analysis
- Standard costing system operation and reporting
- Cost reduction activity effectiveness measurement

**Key Features:**
- Price and quantity variance decomposition
- Material, labor, and manufacturing overhead categorization
- Favorable/unfavorable auto-determination
- Responsible department identification
- Root cause hypothesis generation
- CSV data upload support
- Bilingual templates (Japanese/English)

---

### 🎯 Presentation Reviewer

Reviews presentation materials from the audience perspective, evaluating content clarity, visual design, logical flow, engagement factors, and Marp technical compatibility.

**When to use:**
- Reviewing draft presentations before delivery
- Getting objective feedback on slide quality
- Checking Marp template compatibility
- Improving presentation effectiveness

**Key Features:**
- 5 evaluation axes: Content clarity, visual design, logical flow, engagement, technical compatibility
- Audience perspective review methodology
- Actionable improvement recommendations

---

### 🔧 MARP Layout Debugger

**File:** `skills/marp-layout-debugger/`

Diagnoses and fixes common MARP slide layout issues including whitespace problems, box alignment, bullet formatting inconsistencies, and CSS rendering issues. Provides visual diff comparisons and automated fixes.

**When to use:**
- MARP slides have unexpected whitespace or spacing issues
- Box elements are misaligned or overlap incorrectly
- Bullet points have inconsistent indentation or formatting
- Content overflows slide boundaries
- CSS styles render differently than expected
- Need to validate MARP CSS against best practices

**Key Features:**
- 5 issue categories: Whitespace (WS), Alignment (AL), Bullets (BL), Overflow (OF), CSS (CS)
- 16 specific issue types with severity classification and auto-fix capability
- Automated fix application with safety-first approach (auto-fix vs manual review)
- Visual diff report generation showing before/after comparison
- Non-destructive analysis with backup support

---

### wbs-review-assistant v1.0 (2026-03-19)
- WBS Excel file review against requirements documents and hearing sheets
- Automatic gap detection with requirement traceability analysis
- Excel cell annotation with severity-based conditional formatting (Critical/Major/Minor)
- Structural validation: WBS code hierarchy, phase organization, milestone checks
- Content quality checks: effort estimates, task descriptions, acceptance criteria
- Hearing notes cross-check for decision alignment
- Three output formats: Annotated Excel, Markdown summary, JSON gap analysis
- Readiness score calculation (0-100) with Go/No-Go recommendation
- 14 common WBS issue patterns with auto-detection
- Bilingual support (Japanese/English WBS and requirements)
- Marp-specific technical checks
- Best practices checklist reference

---

### Skill Idea Miner

**File:** `skill-packages/skill-idea-miner.skill`

Mine Claude Code session logs for skill idea candidates, score them for novelty, feasibility, and work utility, and maintain a prioritized backlog for downstream skill generation.

**When to use:**
- Weekly automated pipeline run for skill idea generation
- Manual backlog refresh from recent coding sessions
- Dry-run to preview candidates without LLM scoring

**Key Features:**
- Session log extraction from `~/.claude/projects/` JSONL files
- LLM-based scoring (novelty, feasibility, work utility, composite)
- Backlog management with YAML persistence and dedup
- `mine_session_logs.py` - Extract candidates from session logs
- `score_ideas.py` - Score and merge candidates into backlog

---

### Skill Designer

**File:** `skill-packages/skill-designer.skill`

Design new Claude skills from structured idea specifications. Generates comprehensive Claude CLI prompts that create complete skill directories following repository conventions.

**When to use:**
- The skill auto-generation pipeline selects an idea from the backlog
- Bootstrapping a new business/professional skill from a JSON idea specification
- Quality review of generated skills requires awareness of the scoring rubric

**Key Features:**
- Design prompt generation from JSON idea specs
- Repository convention compliance (SKILL.md frontmatter, directory structure)
- Integration with dual-axis-skill-reviewer scoring rubric
- `build_design_prompt.py` - Generate design prompt from idea JSON

---

### Codebase Onboarding Generator

**File:** `skill-packages/codebase-onboarding-generator.skill`

Automatically analyze a codebase and generate comprehensive CLAUDE.md documentation for future Claude Code sessions. Identifies project type, common commands, build processes, test patterns, directory structure conventions, and architectural decisions.

**When to use:**
- Setting up Claude Code for a new project that lacks CLAUDE.md
- Generating initial project documentation for AI assistants
- Refreshing outdated CLAUDE.md files after significant project changes
- Creating standardized onboarding documentation for team codebases
- Analyzing unfamiliar codebases to understand structure and conventions

**Key Features:**
- Automatic project type detection (Python, Node.js, Rust, Go, Java, etc.)
- Command extraction from package.json, pyproject.toml, Makefile, Cargo.toml
- Framework detection (FastAPI, Django, React, Vue, Spring, etc.)
- Environment variable detection from .env files and source code
- Directory structure analysis with semantic descriptions
- `analyze_codebase.py` - Main analysis script with JSON and CLAUDE.md output

**Supported Project Types:**
- Python (pyproject.toml, setup.py, requirements.txt)
- Node.js (package.json with npm/yarn/pnpm/bun detection)
- Rust (Cargo.toml)
- Go (go.mod)
- Java (Maven pom.xml, Gradle build.gradle)
- Ruby (Gemfile)
- PHP (composer.json)
- .NET (*.csproj, *.sln)

---

### 🌍 Timezone-Aware Event Tracker

**File:** `skill-packages/timezone-aware-event-tracker.skill`

Track and correlate events across multiple timezones with automatic conversion. Maintains awareness of regional time differences (PST/CST/EST/JST and others), handles daylight saving time (DST) transitions, and generates time-normalized reports for distributed team incident analysis.

**When to use:**
- Analyzing incidents or logs from distributed systems spanning multiple timezones
- Correlating events from teams in different regions (US West, US East, Japan, etc.)
- Creating unified timelines from events recorded in different local times
- Investigating issues where timestamp confusion led to coordination failures
- Scheduling or reviewing cross-regional meetings and handoffs

**Key Features:**
- Automatic timezone detection from timestamp suffixes (PST, EST, JST, etc.)
- DST transition handling with ambiguity detection and warnings
- Event correlation within configurable time windows
- Multi-timezone timeline reports (Markdown and JSON)
- Pattern classification (cascading failure, rapid sequence, simultaneous)
- `timezone_event_tracker.py` - CLI for parse, correlate, report, and dst-check commands

**Supported Timestamp Formats:**
- ISO 8601 with offset (2024-03-15T10:30:00-07:00)
- Datetime with abbreviation (2024-03-15 10:30:00 PST)
- Common log format (15/Mar/2024:10:30:00 -0700)
- IANA timezone names (America/Los_Angeles, Asia/Tokyo)

---

### 📱 QR Code Generator

**File:** `skill-packages/qr-code-generator.skill`

Generate QR code images from arbitrary strings (URLs, text, contact information, etc.) using Python's qrcode library. Supports customization of size, margin (quiet zone), foreground/background colors, and error correction levels. Batch generation mode allows creating multiple QR codes from a CSV or JSON input file.

**When to use:**
- Generate a QR code from a URL, text, or data
- Create multiple QR codes in batch from a file
- Create QR codes with specific customization (size, colors, error correction)
- Encode contact information (vCard) as a QR code

**Key Features:**
- Single QR code generation with full customization
- Batch processing from CSV or JSON files
- vCard generation for contact information
- Configurable error correction levels (L, M, Q, H)
- Custom colors (named colors, hex, RGB)
- Automatic preview with Claude's image display
- `generate_qr.py` - CLI for single and batch QR code generation

**Parameters:**
- Box size (module pixel size): 5-20+ pixels
- Border (quiet zone): minimum 4 modules
- Error correction: L (7%), M (15%), Q (25%), H (30%)
- Fill/background colors: named, hex (#RRGGBB), or RGB format

---

### 🚪 Completion Quality Gate Designer

**File:** `skill-packages/completion-quality-gate-designer.skill`

Design quality gates, exit criteria, evidence requirements, and exception governance for each project phase. Separates "Implemented", "Verified", "Accepted", "Released", and "Exception-approved" states to prevent premature completion claims.

**When to use:**
- Defining Definition of Done per project phase
- Designing release readiness gates with evidence requirements
- Standardizing verification commands across CI, developers, and reports
- Establishing exception governance for incomplete items
- Reconciling test metrics between reports and dashboards

**Key Features:**
- 7-phase gate design workflow (scope → vocabulary → exit criteria → evidence → commands → exceptions → expression control)
- 5 templates: Quality Gate Matrix, Definition of Done, Exception Register, Release Readiness, Evidence Ownership Matrix
- Completion vocabulary separation framework (Implemented/Verified/Accepted/Released/Exception-approved)
- Metrics reconciliation guide with single source of truth principles

---

### 🔍 Hidden Contract Investigator

**File:** `skill-packages/hidden-contract-investigator.skill`

Extract implicit contracts from existing code, functions, and modules before reuse. Identifies mismatches between expected and actual behavior — return types, side effects, environment dependencies, and scope shadowing.

**When to use:**
- Reusing legacy functions in new features
- Investigating functions where names or comments don't match behavior
- Extracting return type, side effect, and exception contracts from code
- Assessing reuse risk before implementation
- Designing contract verification tests

**Key Features:**
- 6-step investigation workflow (target → surface contract → actual contract → mismatch classification → reuse judgment → verification design)
- 6-category mismatch taxonomy (Naming, Type, Scope, State, Environment, Hidden Side Effect)
- 5-level reuse risk classification (A: as-is through E: do not reuse)
- Contract test idea generation with pytest examples

---

### 🛡️ Safe By Default Architect

**File:** `skill-packages/safe-by-default-architect.skill`

Convert recurring dangerous implementation patterns into safe architectural defaults and enforceable standards. Defines forbidden patterns, approved replacements, common layers, static rule candidates, and exception governance.

**When to use:**
- Same dangerous code patterns keep recurring across controllers/pages
- Establishing deny-by-default authorization, ORM-only queries, service-layer I/O
- Creating static analysis rules (lint, semgrep) from defect patterns
- Documenting forbidden-to-safe pattern mappings with code examples
- Designing Architecture Decision Records for safety standards

**Key Features:**
- 6-step workflow (pattern aggregation → danger classification → safe standard definition → default decision → common layer design → operational deployment)
- 7-category safe pattern catalog (query, auth, file, persistence, datetime, dependency, idempotency)
- Forbidden-to-safe mapping with before/after code examples
- Static rule candidate templates with false positive assessment

---

### 🔗 Cross Module Consistency Auditor

**File:** `skill-packages/cross-module-consistency-auditor.skill`

Map change impact across all affected modules, flows, reports, and APIs. Audit consistency rules for aggregation totals, sign inversion, status transitions, and copy-paste propagation.

**When to use:**
- One specification change affects multiple screens, reports, or APIs
- Deploying the same logic to multiple flows (e.g., 6 POS transaction types)
- Verifying refund/void/correction flows maintain sign consistency
- Reviewing copy-paste implementations efficiently (canonical + diff strategy)
- Ensuring report totals match drill-down details

**Key Features:**
- 6-step workflow (change kernel → impact lens → impact map → consistency rules → copy propagation strategy → test checklist)
- 7-category consistency rule catalog (aggregation, status transitions, sign inversion, tax/rounding, visibility, naming, report alignment)
- Copy propagation review strategy with canonical-plus-diff approach
- Cross-module test checklist generation

---

### 🧪 Production Parity Test Designer

**File:** `skill-packages/production-parity-test-designer.skill`

Design test hierarchies that catch production-specific failures before deployment. Allocates failure modes to appropriate test tiers, eliminates proxy metrics, and creates adversarial regression backlogs.

**When to use:**
- PR CI is too light to catch production-specific failures
- SQLite/PostgreSQL or other DB dialect gaps exist
- UI shows success but database persistence is unverified
- Mocks hide runtime import errors or dependency gaps
- Defining what belongs in unit vs integration vs smoke vs E2E

**Key Features:**
- 7-step workflow (gap inventory → failure modes → tier allocation → proxy elimination → smoke suite → adversarial backlog → command map)
- Production gap catalog covering DB dialect, dependencies, env vars, timezone, OS, mock vs real, serialization
- Adversarial test patterns (injection, bypass, traversal, fake success, import mismatch, etc.)
- Standard command map separating local/CI/staging/release test commands

---

## Roadmap

Future skills planned for this library:

- [x] **Business Analyst** - Requirements analysis, process mapping, business case development (COMPLETED)
- [ ] **NLP Specialist** - Text analysis, sentiment, topic modeling
- [ ] **Computer Vision Analyst** - Image classification, object detection
- [ ] **Deep Learning Engineer** - Neural networks, transfer learning
- [ ] **AB Testing Statistician** - Experimental design, statistical testing
- [ ] **Business Intelligence Analyst** - Dashboard creation, KPI tracking
- [ ] **Data Engineer** - ETL pipelines, data quality monitoring
- [ ] **Salesforce Consultant** - CRM configuration, workflow automation, requirement gathering

## Version History

### meeting-minutes-writer v1.0 (2026-04-30)
- Generate meeting minutes from transcripts/notes with built-in self-review loop (max 3 iterations)
- 5 Mandatory Checks per iteration: Internal Contradictions, Consistency, Action-Item Omissions, Speaker-Name Errors, Date/Day-of-Week Errors
- MANDATORY date verification via `python3 -c "import datetime; ..."` — never memory-based
- Severity model (HIGH/MEDIUM/LOW); HIGH findings blocking completion
- Completion report surfaces remaining HIGH findings and `* To be confirmed` items after iteration 3
- Complements meeting-minutes-reviewer (review-only) and video2minutes (transcribe→write)
- Resources: output_format.md, self_review_checklist.md, minutes_template_en.md, minutes_template_ja.md, findings_report_template.md (bilingual)

### internal-email-composer v1.0 (2026-04-17)
- Compose professional internal emails for coordination tasks
- 6 supported scenarios: vendor RFQ, task delegation, status update, follow-up, escalation, info request
- Bilingual support (Japanese/English) with culturally-adapted content
- Business etiquette compliance (敬語/keigo for Japanese, professional tone for English)
- 3 urgency levels (normal, high, urgent) with appropriate subject prefixes
- CLI script `compose_email.py` with JSON and Markdown output formats
- Template engine with variable substitution for key points, deadlines, attachments
- Comprehensive reference guides for email templates and business etiquette

### iterative-design-assistant v1.0 (2026-03-29)
- Session-local design decision log with JSON schema (schema v1.0)
- 5 decision categories: color, typography, layout, content, style
- CLI commands: init, record, query, search, apply, history, token, resolve
- Contextual reference resolution for Japanese and English patterns
- Design token extraction and management with category namespacing
- Bidirectional traceability (decisions ↔ elements)
- Markdown and JSON history report generation

### vendor-procurement-coordinator v1.0 (2026-04-18)
- End-to-end vendor procurement workflow coordination
- Orchestrates vendor-rfq-creator and vendor-estimate-creator skills
- Project initialization with standard directory structure (rfq/, quotes/, estimates/, communications/)
- Vendor management (add, edit, remove, CSV import) with status tracking
- Quote response logging with amount, currency, delivery date, validity period
- Email template system (Japanese/English RFQ emails, reminder templates)
- Vendor comparison report generation with price scoring and analysis
- Procurement status tracking (project and vendor lifecycle states)
- Timeline event logging for complete audit trail
- Python CLI scripts: init_procurement.py, manage_vendors.py, track_responses.py, compare_quotes.py
- YAML-based procurement configuration (procurement.yaml)

### meeting-minutes-reviewer v1.0 (2026-03-26)
- Review meeting minutes for completeness, action item clarity, and decision documentation
- 5-dimension quality scoring: Completeness (25%), Action Items (25%), Decisions (20%), Consistency (15%), Clarity (15%)
- Action item validation: owner, deadline, description completeness checks
- Decision documentation validation: context, rationale, alternatives considered
- Source material consistency verification (hearing sheets, agendas)
- Vague language detection with specific suggestions
- JSON and Markdown report output formats
- CLI with `review_minutes.py` script

### action-status-updater v1.0 (2026-04-04)
- Natural language action item tracking for Japanese and English
- Intent detection (completed, delegated, deferred, in-progress) with regex patterns
- Person, channel, and keyword extraction from status updates
- Persistent YAML state with full history tracking
- CLI tool with init, add, update, report, export, and list commands
- Integration guide for daily-comms-ops workflow
- 52 tests covering NL parsing and state management

### project-artifact-linker v1.0 (2026-03-21)
- Cross-reference project artifacts (WBS, meeting minutes, requirements, decisions)
- Entity extraction from multiple document formats (Markdown, CSV, JSON)
- Automated link building with confidence scoring (owner match, keyword overlap, date proximity)
- Four link types: action_item→wbs_task, decision→requirement, meeting→wbs_task, requirement→wbs_task
- Bidirectional traceability matrix generation in Markdown/JSON
- Gap detection for orphaned artifacts (requirements without tasks, tasks without requirements)
- Overall health scoring with weighted component scores

### project-kickoff-bootstrapper v1.0 (2026-03-21)
- Claude kickoff context bootstrapper for new/existing repositories
- 3 install profiles (minimal, standard, full) with escalation rules
- 15 asset templates (CLAUDE.md, PROJECT_BRIEF, SKILL_ROUTING, QUALITY_GATES, TEST_STRATEGY, DECISION_LOG, HIDDEN_CONTRACT_REGISTER, CROSS_MODULE_CONSISTENCY_MATRIX, 3 rule templates, 1 command template, bootstrap input sheet, bootstrap summary)
- 6 reference guides (repository inspection, install profiles, question strategy, non-destructive update, cross-file consistency, follow-on skill sequence)
- Non-destructive update policy (create/refresh/augment modes)
- Repository evidence inspection for auto-detection of stack, commands, and risk areas

### completion-quality-gate-designer v1.0 (2026-03-21)
- 7-phase quality gate design workflow (scope, vocabulary, exit criteria, evidence, commands, exceptions, expression control)
- 5 templates: Quality Gate Matrix, Definition of Done, Exception Register, Release Readiness, Evidence Ownership Matrix
- Completion vocabulary separation (Implemented/Verified/Accepted/Released/Exception-approved)
- Metrics reconciliation guide with single source of truth principles

### hidden-contract-investigator v1.0 (2026-03-21)
- 6-step implicit contract extraction workflow
- 6-category mismatch taxonomy (Naming, Type, Scope, State, Environment, Hidden Side Effect)
- 5-level reuse risk classification (A through E)
- Contract test idea generation with pytest examples

### safe-by-default-architect v1.0 (2026-03-21)
- 6-step safe-by-default standard design workflow
- 7-category safe pattern catalog (query, auth, file, persistence, datetime, dependency, idempotency)
- Forbidden-to-safe mapping with before/after code examples
- Static rule candidate templates with false positive assessment

### cross-module-consistency-auditor v1.0 (2026-03-21)
- 6-step change impact and consistency audit workflow
- 7-category consistency rule catalog (aggregation, status, sign, tax, visibility, naming, report alignment)
- Copy propagation review strategy (canonical + diff approach)
- Cross-module test checklist generation

### production-parity-test-designer v1.0 (2026-03-21)
- 7-step production parity test design workflow
- Production gap catalog (DB dialect, dependencies, env vars, timezone, OS, mock vs real, serialization)
- Adversarial test patterns (injection, bypass, traversal, fake success, import mismatch)
- Standard command map separating local/CI/staging/release test tiers

### qr-code-generator v1.0 (2026-03-17)
- QR code image generation from text, URLs, or contact information
- Single and batch generation modes (CSV/JSON input)
- vCard format support for contact QR codes
- Customizable parameters: box size, border, colors, error correction
- Error correction levels: L (7%), M (15%), Q (25%), H (30%)
- Named colors, hex codes (#RRGGBB), and RGB format support
- Automatic batch summary report generation

### project-completeness-scorer v1.0 (2026-03-16)
- Systematic project completeness evaluation with weighted 0-100 scoring
- 5 evaluation dimensions: Functional Requirements, Quality Standards, Test Coverage, Documentation, Deployment Readiness
- Gap identification with severity classification (Critical/Major/Minor)
- Priority ranking based on impact-to-effort ratio
- 4 project templates: skill, webapp, library, document
- Custom template support via JSON files
- JSON and Markdown report generation
- CLI interface with `score_project.py`

### hearing-to-requirements-mapper v1.0 (2026-03-15)
- Transform client hearing sheets and meeting notes into structured requirements
- Requirements classification by type (BR/SR/FR/NFR/CON/ASM) and priority (MoSCoW)
- Automatic ambiguity detection (vague quantifiers, open lists, passive voice, temporal)
- Gap analysis against requirements completeness checklist
- WBS mapping with standard software project template
- Requirements traceability matrix (RTM) generation
- Bilingual (Japanese/English) input and output support
- Language auto-detection with mixed-language handling

### timezone-aware-event-tracker v1.0 (2026-03-11)
- Multi-timezone event tracking and correlation
- Automatic timezone detection from timestamp suffixes (PST, EST, JST, etc.)
- DST transition handling with ambiguity detection
- Event correlation within configurable time windows
- Multi-timezone timeline reports (Markdown/JSON)
- Pattern classification (cascading_failure, rapid_sequence, simultaneous)
- Comprehensive timezone conversion reference guide

### meeting-asset-preparer v1.0 (2026-03-10)
- Comprehensive meeting asset preparation for project meetings
- Bilingual (Japanese/English) output support for cross-regional teams
- Context integration from project documents (estimates, specs, prior notes)
- CLI with 6 commands: init, compile-refs, generate-agenda, create-decision-log, create-action-items, package
- Structured templates for agendas, decision logs, and action items
- Meeting package generation with index document
- YAML-based meeting configuration

### multi-file-log-correlator v1.0 (2026-03-09)
- Multi-file log correlation for distributed system analysis
- Unified timeline construction from heterogeneous log sources
- Correlation ID tracking (request_id, trace_id, transaction_id, UUID patterns)
- Temporal proximity correlation when explicit IDs are absent
- Timezone normalization with python-dateutil support
- Gap detection with configurable thresholds
- Anomaly detection (timing anomalies, error bursts)
- JSON and Markdown report generation
- Auto-detection of common timestamp formats (ISO 8601, Apache/Nginx, syslog, Java/Log4j)
- Differentiates from log-debugger (multi-source correlation vs single-file RCA)

### codebase-onboarding-generator v1.0 (2026-03-08)
- Automatic project type detection for 8+ languages (Python, Node.js, Rust, Go, Java, Ruby, PHP, .NET)
- Command extraction from package.json, pyproject.toml, Makefile, Cargo.toml, go.mod, pom.xml
- Framework detection (FastAPI, Django, Flask, React, Vue, Angular, Spring, Rails, etc.)
- Environment variable detection from .env files and source code patterns
- Directory structure analysis with semantic descriptions
- CLAUDE.md best practices reference guide
- `analyze_codebase.py` with JSON and CLAUDE.md output modes

### network-incident-analyzer v1.0 (2026-03-08)
- Network device log analysis for incident detection and root cause analysis
- Multi-format log parsing (Cisco IOS, JunOS, Palo Alto, F5, Syslog, JSON)
- Automatic timezone normalization to UTC
- Anomaly detection patterns:
  - Connection failure spikes (threshold-based with severity levels)
  - Interface flapping detection
  - Error rate spike detection
- Cross-device event correlation with configurable time windows
- Root cause hypothesis generation with confidence scoring
- JSON and Markdown report generation (incident summary, root cause analysis)
- CLI interface with flexible time window and config options

### skill-idea-miner v1.0 & skill-designer v1.0 (2026-03-07)
- **skill-idea-miner**: Mine Claude Code session logs for skill idea candidates
  - Session log extraction from `~/.claude/projects/` JSONL files
  - LLM-based scoring (novelty, feasibility, work utility)
  - Backlog management with YAML persistence and dedup
- **skill-designer**: Design new Claude skills from structured idea specifications
  - Design prompt generation from JSON idea specs
  - Repository convention compliance (SKILL.md frontmatter, directory structure)
  - Integration with dual-axis-skill-reviewer scoring rubric

### cx-error-analyzer v1.0 (2026-02-28)
- 6-axis CX evaluation (Impact/Frequency/Recovery/Message Quality/Emotional/Business Cost)
- Weighted CX scoring with 4 severity tiers
- Impact vs Effort priority matrix with Quick Wins identification
- Error UX best practices (message design, recovery flows, emotional design)
- CX metrics reference (CES/CSAT correlation, support cost calculation, churn risk)
- ROI calculation framework for error UX improvements
- Error classification taxonomy and user journey stage mapping

### operations-manual-creator v1.0 (2026-02-28)
- STEP format (Specific/Target/Expected/Proceed) for procedure writing
- ANSI Z535-inspired caution/warning classification (DANGER/WARNING/CAUTION/NOTE)
- Operation inventory with ID system (OP-xxx), frequency/role categorization
- Symptom-Cause-Resolution troubleshooting tables with decision trees
- L1/L2/L3 escalation procedure templates
- Bilingual manual templates (Japanese/English)

### technical-spec-writer v1.0 (2026-02-28)
- IEEE 830 / ISO 29148 compliant specification writing
- ID numbering system (SCR-xxx, API-xxx, TBL-xxx, SEQ-xxx, STS-xxx)
- Mermaid diagram patterns (sequenceDiagram, stateDiagram-v2, erDiagram, flowchart)
- REST API design guide (error codes, pagination, authentication, versioning)
- DB design guide (naming conventions, normalization, indexing, audit columns)
- Traceability matrix (REQ → SCR/API/TBL mapping)
- Bilingual functional spec templates (Japanese/English)

### incident-rca-specialist v1.0 (2026-02-28)
- 8-workflow incident RCA process (Information → Timeline → Impact → 5 Whys → Fishbone → FTA → Corrective Actions → Report)
- 5 Whys with branching technique and human error decomposition
- Fault Tree Analysis with AND/OR gates, minimal cut sets, SPOF identification
- 3D Prevention Framework (Detect/Defend/Degrade)
- P0-P4 severity matrix with SLA violation evaluation and business impact calculation
- Corrective action tracker with SMART criteria validation
- Mermaid gantt timeline with TTD/TTR/TTM/TTRe metrics
- Differentiated from log-debugger (organizational process focus vs log analysis)

### marp-layout-debugger v1.0 (2026-04-03)
- Diagnoses and fixes common MARP slide layout issues (whitespace, alignment, bullets, overflow, CSS)
- 5 issue categories with 16 specific issue types (WS001-WS004, AL001-AL004, BL001-BL004, OF001-OF004, CS001-CS004)
- Automated fix application with auto-fixable vs manual review classification
- Visual diff report generation with before/after comparison
- 3 Python scripts: analyze_marp_layout.py, fix_marp_layout.py, generate_diff_report.py

### presentation-reviewer v1.0 (2026-02-26)
- 5 evaluation axes: content clarity, visual design, logical flow, engagement, Marp compatibility
- Audience perspective review methodology
- Actionable improvement recommendations with best practices checklist

### management-accounting-navigator v1.0 (2026-02-24)
- 12-domain auto-classification for management accounting inquiries
- COSO/IMA management accounting framework alignment
- Routing to specialized MA skills (budget variance, CVP, standard cost)
- Bilingual domain classification templates

### ma-budget-actual-variance v1.0 (2026-02-24)
- Auto favorable/unfavorable determination by account type (revenue/expense)
- Price and quantity variance decomposition
- Significance ranking and root cause hypothesis generation
- CSV data upload support, bilingual report templates

### ma-cvp-break-even v1.0 (2026-02-24)
- Fixed/variable cost structure analysis and break-even point calculation
- Contribution margin ratio and margin of safety evaluation
- Target profit required sales simulation
- Multi-product CVP analysis support, bilingual templates

### ma-standard-cost-variance v1.0 (2026-02-24)
- Standard vs actual cost variance decomposition (price/quantity)
- Material, labor, and manufacturing overhead categorization
- Responsible department identification and root cause hypothesis
- CSV data upload support, bilingual report templates

### audit-doc-checker v1.0 (2026-02-26)
- 12-category audit document quality review with 0-100 scoring
- Severity-based deduction model (High -5, Medium -3, Low -1)
- Document-type weighting adjustments (control design, bottleneck analysis, requirements, process inventory)
- 4-tier quality assessment (High Quality / Improvement Recommended / Revision Required / Critical Risk)
- Generalized from Round1 F&B Inventory COGS audit engagement
- Integration with audit-control-designer for generate→review workflow

### audit-control-designer v1.0 (2026-02-26)
- 5 business process patterns (AP, Inventory, COGS, Returns/Credits, Price Management)
- 8 control pattern templates derived from real audit engagements (T-AP-01/02, T-INV-01/02, T-CO-01, T-VAL-01, T-CALC-01/02)
- 5 audit assertion mapping rules (C/A/V/CO/E) with coverage matrix
- 5 SoD pair patterns with compensating controls for small organizations
- 8 KPI catalog entries (K01-K08) with baseline/target guidelines
- Materiality framework (Overall, Performance, Clearly Trivial) with industry-specific guidelines
- Accounting standards reference (US GAAP/IFRS/J-GAAP differences affecting control design)
- Industry customization (F&B, Retail, Manufacturing, Services)
- Generalized from Round1 F&B Inventory COGS audit engagement

### shift-planner v1.0 (2026-02-21)
- Employee shift auto-assignment with constraint-satisfaction greedy algorithm
- 3-CSV input system (roster, requirements, optional shift patterns)
- Hard constraints: max hours/days, qualifications, consecutive days, min rest hours
- Soft constraints: avoid days, preferred patterns, weekend balance scoring
- 30-minute coverage verification with break exclusion
- Fairness metrics: hours deviation, weekend std_dev, avoid violations
- SFT-E001~E008 error alerts, SFT-W001~W010 warning alerts
- Built-in 5 shift patterns (FULL_8H/EARLY_8H/LATE_8H/SHORT_6H/HALF_4H)
- 25 test cases

### production-schedule-optimizer v1.0 (2026-02-21)
- Weekly production schedule optimization for manufacturing facilities
- Greedy Bin-Packing algorithm with deterministic sort/tie-break
- 4-CSV input system (products, demand, rooms, staff)
- Shelf-life based production frequency (min(ceil(7/shelf_life), 7))
- Staff requirement estimation with 1.1x buffer coefficient
- PSO-E001~E006 error alerts, PSO-W001~W006 warning alerts
- Lunch break skip (12:00-13:00) handling
- 14 test cases (11 scheduler + 3 staff estimation)

### dual-axis-skill-reviewer v1.0 (2026-02-20)
- Dual-axis skill quality review (Auto + LLM scoring)
- Auto axis: 5-dimension deterministic checks (metadata, workflow, execution safety, artifacts, test health)
- LLM axis: Deep content review with JSON schema merge
- Weighted final score with configurable auto/LLM weights
- Batch review (`--all`) with summary table output
- Cross-project review via `--project-root`
- knowledge_only skill auto-detection to avoid unfair penalties
- Improvement items auto-generated when score < 90

### markdown-to-pdf v2.0 (2026-02-19)
- Renamed from mermaid-to-pdf to markdown-to-pdf
- Added fpdf2-based professional PDF mode (markdown_to_fpdf.py)
- Cover page generation from YAML frontmatter
- Navy/Gray color themes with styled headers/footers
- Professional table rendering (data_table / info_table)
- Cross-platform CJK font discovery (macOS/Windows/Linux)
- Mermaid block fallback in fpdf2 mode

### network-diagnostics v1.0 (2026-02-18)
- Initial release
- ネットワーク品質の総合診断スキル（OS標準ツールのみ、外部依存なし）
- 3-Phase ワークフロー: Collect（自動データ収集）→ Analyze & Report（閾値判定+レポート）→ Deep-Dive（深堀り調査）
- データ収集: 接続情報、Ping（Gateway+8.8.8.8+1.1.1.1）、HTTP タイミング（DNS/TCP/TLS/TTFB）、速度テスト（3CDN）、Traceroute
- 接続種別対応閾値: Ethernet（厳格）/ Wi-Fi（緩和）で独立した GOOD/WARNING/CRITICAL 判定
- macOS / Linux クロスプラットフォーム対応（iproute2 優先、net-tools fallback）
- 6カテゴリの深堀り調査手順: 高レイテンシ、パケットロス、DNS遅延、低速DL、経路異常、高ジッター
- 45件のユニットテスト（unittest + mock、外部依存なし）

### office-script-expert v1.0 (2026-02-13)
- Initial release
- Office Scripts（Excel Online / Microsoft 365）開発支援スキル
- 6つの重要プラットフォーム制約（P1-P6）: import不可、外部ライブラリ不可、Map/Set反復問題、120秒タイムアウト等
- lib/抽出 + Vitestによるテスト戦略（Office Scripts自体はimport不可のためlib/で開発・テストしインライン化）
- 13の実運用バグパターン（common_bug_patterns.md）
- ExcelScript API パターン集9種（シート読み書き、CSV解析、保護/解除、日付変換、丸め関数等）
- 実装前チェックリスト（implementation_checklist.md）

### business-plan-creator v1.0 (2026-02-11)
- Initial release
- 事業計画書を体系的に作成するスキル（日本語・英語対応）
- 5フェーズワークフロー: ヒアリング → 分析 → 戦略設計 → 数値計画 → ドキュメント化
- 7分析フレームワーク: TAM/SAM/SOM、PEST、5フォース、SWOT、BMC、リーンキャンバス、バリューチェーン
- 財務モデリング: ユニットエコノミクス、3シナリオ分析、P/L・CF計画
- 業種別テンプレート: SaaS、EC/D2C、コンサル、飲食、製造、AI、不動産
- 標準構成（12セクション）と簡易構成（7セクション）の2パターン

### streamlit-expert v1.0 (2026-02-08)
- Initial release
- Streamlit v1.42〜v1.52+対応のWebアプリ開発支援スキル
- OIDC認証（st.login/st.logout/st.user）、シークレット管理、データ可視化、パフォーマンス最適化
- 対応プロバイダー: Google, Microsoft Entra ID, Okta, Auth0
- 可視化ライブラリ選択ガイド: Plotly, Altair, ネイティブチャート
- キャッシュ戦略、セッション状態管理、大規模データ処理のベストプラクティス

### ai-text-humanizer v1.0 (2026-02-08)
- Initial release
- AI生成テキスト（日本語）の「AI臭」を検出・スコアリング・リライトするスキル
- 6パターン検出: 視覚的マーカー残存、単調なリズム、マニュアル的構成、非コミット姿勢、抽象語の濫用、定型メタファー
- 0-100 AI臭スコア算出（正規表現ベース、`detect_ai_patterns.py`）
- 3つの人間化技法: バランスを崩す・客観を崩す・論理を崩す
- 3ワークフロー: AI臭診断、リライト実行、Before/After比較
- Markdown/JSON出力対応
- 英語テキストはClaude自身がreferences/を参照して分析・リライト

### gogcli-expert v1.0 (2026-01-29)
- Initial release
- Google Workspace CLI (gogcli / steipete/gogcli) expert skill
- 13 Google Workspace services: Gmail, Calendar, Drive, Sheets, Docs, Slides, Contacts, Tasks, Chat, Groups, Keep, Classroom, People
- Authentication: OAuth2, service account (domain-wide delegation), multi-account, multi-client
- 5 reference guides: quick reference, communication services, productivity services, workspace admin, troubleshooting
- 8 common automation patterns: daily digest, schedule check, team availability, batch download, CSV export, sandboxing, CI/CD, multi-account
- Security best practices: least-privilege auth, command sandboxing, credential management

### design-implementation-reviewer v1.0 (2025-12-26)
- Initial release
- Critical code review skill focused on correctness, not just design matching
- Three-layer review framework:
  - Layer 1: Code Quality (type safety, null handling, edge cases, logic, exceptions)
  - Layer 2: Execution Flow (function wiring, data flow, joins, concurrency, idempotency, transactions, resources, timeouts, API contracts)
  - Layer 3: Goal Achievement (expected results, real data validation, success rate, end-to-end trace, design gaps)
- Always uses `ultrathink` mode for thorough analysis
- Security review explicitly out of scope
- Structured output with Review Scope, Findings (with Test Plan for Critical/High), Open Questions

### video2minutes v1.0 (2025-12-25)
- Initial release
- Video transcription and meeting minutes generation
- Uses Whisper for transcription
- Automatic key points and action items extraction

### render-cli-expert v1.0 (2025-12-24)
- Initial release
- Render cloud platform CLI management skill
- Core capabilities:
  - Service deployment with `--wait` and `--confirm` options
  - Real-time log monitoring with `--tail` and JSON output
  - PostgreSQL database connections via `render psql`
  - SSH access to paid services (Web Services, Private Services, Background Workers)
  - CI/CD automation patterns (GitHub Actions, shell scripts)
  - Workspace and service management
- Installation methods: Homebrew (recommended), direct download, from source
- Authentication: Interactive login (`render login`) or API key (`RENDER_API_KEY`)
- Output formats: text (default), JSON, YAML
- Common patterns:
  - Quick deploy with wait: `render deploys create srv-xxx --wait --confirm`
  - Real-time log monitoring: `render logs srv-xxx --tail`
  - Database backup via psql
  - Service health check with JSON + jq
  - Bulk operations scripts
- Auto-update feature:
  - Monthly automatic documentation check
  - `scripts/render_cli_updater.py` for manual/forced updates
  - Update logs saved to `references/cli_updates.md`
- Best practices: API key for CI/CD, `--wait` flag, `-o json` for automation, `--confirm` for non-interactive

### migration-validation-explorer v2.0 (2025-12-28)
- Major update with automation and structured hypothesis generation
- **New: 4-Perspective Hypothesis Generation**
  - Domain Expert (business rules, compliance)
  - Tech Implementer (code bugs, transforms)
  - Edge Case Hunter (boundaries, special cases)
  - Statistical Skeptic (distributions, outliers)
- **New: Priority Scoring** (Impact × Probability × Testability)
- **New: Automation Scripts**
  - `exploratory_profiler.py` - Data profiling with null rates, distributions
  - `hypothesis_tester.py` - Reference integrity, value concentration tests
  - `perspective_combiner.py` - Lens catalog and random combinations
- **New: Cross-Pollination Operators** (AND, XOR, SEQ, REQ)
- **New: ID Normalization principle** (float `.0` suffix handling)
- Additional resources:
  - `references/hypothesis_generation_guide.md`
  - `assets/hypothesis_worksheet.md`

### migration-validation-explorer v1.0 (2025-12-28)
- Initial release
- Exploratory data-migration validation and QA ideation workflow
- Focus categories, Lens library, QA backlog generation

### helpdesk-responder v1.0 (2025-12-28)
- Initial release
- Generic helpdesk first-response skill based on round1-helpdesk-responder
- 3-phase workflow: Inquiry Analysis → KB Search & Matching → Response Draft Generation
- Core features:
  - Auto-detection patterns (error codes, device names, symptoms)
  - Confidence scoring system (High >=80%, Medium 50-79%, Low <50%)
  - Template-based response generation
  - Multi-language support (English/Japanese)
  - Escalation workflow with structured handoff format
- Resources:
  - `references/kb_schema.json` - Complete JSON schema for KB index configuration
  - `assets/response_templates.md` - 7 ready-to-use response templates
- Customizable for any industry or product support context
- Template variables for dynamic content substitution

### ai-adoption-consultant v1.0 (2025-11-09)
- Initial release
- Comprehensive AI/LLM adoption consulting skill with use case knowledge base
- 5 core capabilities: Industry-specific strategies, Department-specific automation, Scenario-based approaches, AI agent type recommendations, Detailed case studies
- 27 reference files (162KB total knowledge base):
  - 5 industry guides (Finance, Healthcare, Retail, Manufacturing, Education)
  - 5 function guides (Sales & Marketing, HR, Customer Support, Finance & Accounting, R&D)
  - 5 scenario guides (Startup, Enterprise, Remote Work, Customer Experience, Digital Transformation)
  - 4 agent type guides (RAG agents, Voice agents, Video generation, Internal business support)
  - 6 detailed case studies (Sales Support, Customer Support, Knowledge Search, Project Planning, Competitive Analysis, Strategic Planning)
  - README with AI adoption trends and success factors
- 5-step consulting workflow: Hearing & Assessment → Problem Analysis → Knowledge Selection → Proposal Creation → Follow-up & Q&A
- AI adoption proposal components:
  - Executive summary with ROI calculation
  - Current state analysis and priority identification
  - AI utilization proposal with use cases, architecture, data flow
  - Expected effects (quantitative: cost reduction %, efficiency %, quality metrics)
  - 3-phase implementation plan (Pilot → Full Deployment → Continuous Improvement)
  - Investment breakdown (initial, operational, TCO, ROI)
  - Risk assessment & mitigation (technical, organizational, legal risks)
  - Best practices and recommendations
- Example proposals:
  - Retail CX enhancement (20% conversion increase, 15% cart abandonment reduction, 30% satisfaction improvement)
  - Startup sales efficiency (50% prep time reduction, 25% deal closure increase, 2x leads)
  - Manufacturing quality control (95%+ detection rate, 70% inspection time reduction, 30% quality cost reduction)
- Key principles: Practice-oriented, Quantified effects, Phased approach, Risk management, Human-centric
- Multi-dimensional analysis framework: Industry × Function × Scenario combinations
- Agent type expertise: RAG, Voice, Video Generation, Business Support with architecture recommendations
- Bilingual support: Japanese and English

### salesforce-expert v1.0 (2025-11-09)
- Initial release
- Comprehensive Salesforce development and operations management guidance
- 4 core capabilities: Sharing Settings & Access Control, Approval Process Configuration, Custom Development Best Practices, Architecture Design & Data Modeling
- 4 reference guides (90KB total documentation):
  - `sharing_settings_guide.md` - OWD, sharing rules, role hierarchy, manual sharing, teams, troubleshooting
  - `approval_process_guide.md` - Approval patterns, submission methods, actions, testing, monitoring
  - `custom_development_patterns.md` - Trigger handlers, batch apex, queueable, LWC, testing, bulkification
  - `architecture_best_practices.md` - Data modeling, LDV design, governor limits, integration, security
- Bug analysis workflow: 5-step systematic approach (gather context, categorize, diagnose, propose solutions, document)
- Development patterns: Trigger Handler, Service Layer, Batch Apex, Queueable, LWC (wire/imperative/pub-sub), REST API
- Common scenarios covered:
  - Access denied issues (OWD, sharing rules, role hierarchy troubleshooting)
  - Approval process errors (entry criteria, active process validation, approver assignment)
  - Object relationship issues (Master-Detail vs Lookup, junction objects, Contact Roles)
  - Integration design (REST API inbound/outbound, Platform Events)
  - Governor limit optimization (SOQL, DML, heap size, CPU time)
- Enterprise patterns: Recursion prevention, service layer, test data factory, mock callouts
- Best practices: Security (with sharing, CRUD/FLS), Performance (bulkification), Maintainability (separation of concerns), Testing (85%+ coverage)
- Complete code examples: Real-world Apex triggers, handlers, services, batch jobs, LWC components, REST APIs
- Bilingual support: Japanese and English

### salesforce-flow-expert v1.0 (2025-01-09)
- Initial release: Phase 1 & 2 (validation, metadata generation, deployment automation)
- Comprehensive Salesforce Flow implementation guide from design through production deployment
- 4 core capabilities: Flow Design & Pattern Selection, Flow Metadata XML Generation, Pre-Deployment Validation, Deployment & Troubleshooting
- 4 Python automation scripts (~950 lines total):
  - `validate_flow.py` (550 lines) - Pre-deployment validation: reference errors, governor limits, metadata validation, naming conventions
  - `generate_flow_metadata.py` (210 lines) - Automated Flow-meta.xml generation with API version compatibility
  - `deploy_flow.py` (250 lines) - sf CLI deployment wrapper with error handling, pre-validation, rollback support
  - `extract_flow_elements.py` (180 lines) - Flow structure analysis and documentation generation
- 5 comprehensive reference guides (~2,450 lines total):
  - `variable_reference_patterns.md` (600 lines) - Top 10 reference errors catalog with fix patterns, prevention checklists
  - `flow_types_guide.md` (500 lines) - Screen Flow, Record-Triggered, Schedule-Triggered, Autolaunched patterns
  - `deployment_guide.md` (300 lines) - sf CLI command reference, error handling, rollback procedures
  - `metadata_xml_reference.md` (550 lines) - Complete XML structure, API version differences, element ordering
  - `governor_limits_optimization.md` (500 lines) - DML/SOQL optimization, bulkification patterns
- 7 templates: 4 Flow metadata templates (Screen, Record-Triggered, Schedule, Autolaunched), error reference table, package.xml, sfdx-project.json
- Validation capabilities: Detects 90%+ of errors before deployment
  - Priority 1: Variable/element reference validation (undeclared variables, invalid element references, type mismatches, collection vs single value errors)
  - Governor limit analysis (DML in loops, SOQL in loops, total SOQL/DML counts)
  - Metadata validation (API version, required fields, element ordering, XML structure)
  - Naming convention checks (camelCase variables, PascalCase elements)
- Error catalog: Top 10 most common Flow errors with frequency, root cause, fix pattern, prevention checklist
- Flow type support: All 4 types (Screen Flow, Record-Triggered Flow, Schedule-Triggered Flow, Autolaunched Flow)
- Deployment features: Pre-deployment validation, automated metadata generation, sf CLI integration, error parsing, rollback support
- Best practices: Bulkification (DML/SOQL outside loops), Before-Save optimization, recursion prevention, error handling
- Complete workflow: Design → Build → Validate → Deploy → Monitor (5-phase end-to-end process)
- Output formats: text, json, markdown for validation reports

**File:** `skill-packages/salesforce-flow-expert.skill`

### project-plan-creator v1.0 (2025-11-07)
- Initial release
- 7 core workflows: Project Charter Creation, Scope Definition and Management, Schedule Development, Resource Planning and RACI Matrix, Risk Management Planning, Communication and Quality Planning, Integration and Document Generation
- Comprehensive project charter guide (PMBOK-compliant, 12 sections)
- Complete project plan template (400+ lines, 12 sections) with 5 Mermaid diagrams
- Project charter creation:
  - Business case and benefits management
  - Project purpose and objectives definition
  - High-level scope (In/Out of Scope)
  - Key deliverables and milestones
  - Budget and resource estimation
  - Stakeholder identification
  - Risk assessment and success criteria
- Scope management features:
  - Detailed scope statement (product scope and project scope)
  - Scope boundary visualization (Mermaid graph)
  - WBS hierarchy with visual diagram (Mermaid graph)
  - Scope baseline establishment
  - Change control process (Mermaid flowchart)
- Schedule development:
  - Activity definition and sequencing (FS, SS, FF, SF dependencies)
  - PERT three-point estimation ((O + 4M + P) / 6)
  - Mermaid Gantt chart with milestones
  - Critical path identification
  - Schedule compression techniques (Crashing, Fast Tracking)
- Resource planning:
  - Project roles and team structure definition
  - RACI Matrix creation (Responsible, Accountable, Consulted, Informed)
  - Communication protocols and meeting schedules
  - Team structure visualization (Mermaid org chart)
- Risk management:
  - Risk identification (5 categories: technical, requirements, resources, integration, external)
  - Qualitative risk analysis (probability, impact, risk level)
  - Risk response strategies (Avoid, Mitigate, Transfer, Accept)
  - Risk monitoring process (Mermaid flowchart)
- Communication and quality planning:
  - Stakeholder communication needs analysis
  - Communication matrix (information, sender, receiver, frequency, method)
  - Quality standards (code, testing, documentation)
  - QA process workflow (Mermaid flowchart)
  - Acceptance criteria definition
- Mermaid visualizations (5 diagrams):
  - Scope Boundary Diagram (In/Out of Scope)
  - WBS Hierarchy (project decomposition)
  - Gantt Chart (schedule with milestones)
  - Risk Monitoring Process (continuous improvement loop)
  - Change Management Process (CCB approval workflow)
- PMBOK knowledge areas integration:
  - Integration, Scope, Schedule, Cost, Quality, Resource, Communications, Risk, Procurement, Stakeholder Management
- Framework alignment: PMBOK® Guide 6th/7th editions, ISO 21500, Prince2® compatible
- Best practices: Charter-first approach, visual diagrams, early RACI definition, proactive risk management, baseline establishment, version control, stakeholder engagement
- Bilingual support: Japanese (default), English
- Output format: Markdown + Mermaid diagrams for professional project plans
- Integration with knowledge/pm-knowledge folder for PMBOK standards

### vendor-estimate-creator v1.0 (2025-01-07)
- Initial release
- 6 core workflows: RFQ Analysis, Work Breakdown, Effort Estimation, Cost Calculation, ROI Analysis, Estimate Document Generation
- Comprehensive Japanese estimate template (400+ lines, 12 sections)
- 3 reference guides:
  - Estimation methodology (4 methods: analogous, parametric, bottom-up, three-point)
  - Effort estimation standards (role-based productivity, task-level standards, project type benchmarks)
  - ROI analysis guide (ROI, NPV, IRR, payback period calculations with examples)
- Estimation methodology features:
  - Accuracy by phase (±50% → ±5% as project progresses)
  - Project type-specific effort distribution (Web, Mobile, Enterprise, API, Data)
  - Adjustment factors (complexity, team proficiency, technical risk)
  - Contingency recommendations (5-40% based on risk level)
- Effort estimation standards:
  - Role-based productivity (LOC, Function Points)
  - Task-level standard effort (requirements, design, implementation, testing, deployment)
  - Project size benchmarks (small, medium, large by project type)
  - Validation methods (productivity check, similar project comparison, phase ratio check)
- ROI analysis capabilities:
  - Financial metrics (ROI, NPV, IRR, payback period)
  - Benefit classification (quantitative and qualitative)
  - Business case creation (As-Is analysis, To-Be definition, cash flow analysis, sensitivity analysis)
  - Scenario analysis (best, standard, pessimistic cases)
- Estimate template sections: Executive Summary, Assumptions, Detailed Estimate (WBS), Schedule, ROI Analysis, Team Structure, Risks, O&M Costs, Payment Terms, Contract Terms
- Best practices: Multiple estimation methods, conservative estimates, documented assumptions, early risk identification, ROI justification
- Bilingual support: Japanese (default), English
- Output format: Professional Markdown estimate documents

### vendor-rfq-creator v1.0 (2025-01-07)
- Initial release
- 4 core workflows: Requirements Elicitation, Requirements Structuring, RFQ Document Creation, Quality Review
- Comprehensive Japanese RFQ template (400+ lines, 9 sections) in Markdown format
- Complete checklist (150+ items across 9 sections):
  - プロジェクト概要、機能要件、非機能要件、技術要件、PM要件、契約要件、見積依頼要件、品質チェック
- Requirements elicitation framework:
  - 5W1H questioning methodology (Who, What, Where, When, Why, How)
  - MoSCoW prioritization (Must/Should/Could/Won't have)
  - Structured clarification questions with templates
  - Assumption documentation with rationale
- Standardized estimate submission format:
  - WBS template with required phases (要件定義、設計、実装、テスト、デプロイメント、PM、品質保証)
  - Required columns (タスク名、詳細、役割、工数、単価、小計)
  - Contingency recommendations (10-20%)
- Quality assurance features:
  - Completeness check (必須項目の網羅確認)
  - Clarity check (曖昧な表現の検出と修正提案)
  - Consistency check (数値整合性、用語統一)
  - Feasibility check (実現可能性評価)
- Project type-specific guidance (Web, Mobile, Enterprise, Data Infrastructure)
- Best practices and common pitfalls documented
- Examples: E-Commerce, Mobile SFA, Data Migration
- Bilingual support: Japanese (default), English
- Output format: Professional Markdown RFQ documents

### vendor-estimate-reviewer v1.0 (2025-01-07)
- Initial release
- 5 integrated workflows: Initial Review & Triage, Detailed Analysis & Assessment, Vendor Clarification Preparation, Final Review & Recommendation, Decision Support & Follow-Up
- Comprehensive evaluation across 12 dimensions (scope, WBS, effort, cost, resources, timeline, QA, risk, contract, vendor capability, comparison, red flags)
- 3 reference documents (350+ pages equivalent):
  - Review checklist (12 sections, 200+ checklist items)
  - Cost estimation standards (labor rates, effort distribution, project benchmarks by type)
  - Risk factors guide (60+ risks with probability, impact, and mitigation strategies)
- Automated analysis script (Excel, CSV, PDF parsing with pandas/openpyxl/PyPDF2)
- 2 Markdown templates (comprehensive report 15+ sections, interactive checklist with scoring)
- Industry benchmarks (North America, Europe, Asia Pacific labor rates by role and seniority)
- 14 critical red flags detection
- Risk scoring framework (high/medium/low prioritization)
- Go/no-go decision framework with weighted scoring
- Support for multi-vendor comparison
- Negotiation strategy guidance (cost reduction and value-add opportunities)

### data-visualization-expert v1.0 (2025-01-07)
- Initial release
- 5 core workflows: Chart Selection, Color Best Practices, Dashboard Design, Story-Driven Visualization, Accessibility
- Comprehensive reference guides (30+ chart types, color theory, dashboard design)
- Command-line visualization tool (6 chart types: bar, line, scatter, heatmap, distribution, dashboard)
- Professional templates (KPI cards, executive summaries, waterfall charts, correlation heatmaps)
- 50+ color palettes (qualitative, sequential, diverging, business-specific, colorblind-safe)
- WCAG 2.1 accessibility compliance
- Support for colorblind-safe visualizations (Okabe-Ito, Viridis palettes)

### business-analyst v1.0 (2025-01-07)
- Initial release
- BABOK® Guide v3 alignment
- 5 core workflows: Requirements Elicitation, Business Process Analysis, Stakeholder Analysis, Business Case Development, Gap Analysis
- Comprehensive templates (ISO/IEC/IEEE 29148 compliant BRD, Business Case, Stakeholder Analysis)
- Automated business analysis toolkit with financial calculations
- Coverage of all 6 BABOK knowledge areas
- Support for MoSCoW prioritization, BPMN process modeling, value stream mapping
- Data quality profiling and assessment capabilities

### project-manager v1.0 (2025-01-07)
- Initial release
- PMBOK® 6th/7th Edition alignment
- 5 core workflows: Requirements Definition, Project Plan Review, Progress Reporting with EVM, Risk Management, Cost Estimation
- Comprehensive templates (ISO/IEC/IEEE 29148 compliant)
- Automated project health check script
- Coverage of all 10 PMBOK knowledge areas and 5 process groups
- Support for traditional, agile, and hybrid methodologies

### data-scientist v1.0 (2025-01-07)
- Initial release
- Auto EDA, model comparison, time series analysis
- Comprehensive reference guides
- Professional templates
- Support for classification, regression, time series

---

*This library is designed to enhance Claude Code's capabilities with professional-grade workflows and best practices across data science, project management, business analysis, data visualization, and vendor estimate evaluation domains.*
