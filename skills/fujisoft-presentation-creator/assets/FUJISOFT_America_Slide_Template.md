---
marp: true
theme: default
paginate: false
class: lead
style: |
  @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Bahnschrift:wght@400;600;700&display=swap');
  
  :root {
    --cover-gradient: linear-gradient(135deg, #4a90a4 0%, #2b5797 25%, #1e3a8a 75%, #1a237e 100%);
    --cover-secondary: rgba(255,255,255,0.9);
    --cover-accent: rgba(255,255,255,0.7);
    --title-font: 'Bahnschrift', 'Arial Black', sans-serif;
    --body-font: 'Lato', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --light-font: 'Lato', 'Segoe UI Light', sans-serif;
    --brand-primary: #1a237e;
    --brand-secondary: #3949ab;
    --brand-accent: #5c6bc0;
    --success-color: #4caf50;
    --warning-color: #ff9800;
    --info-color: #2196f3;
    --error-color: #f44336;
    --info-bg: #e3f2fd;
    --success-bg: #e8f5e9;
    --warning-bg: #fff3e0;
    --error-bg: #fce4ec;
    --neutral-bg: #f5f5f5;
  }
  
  /* Cover Page Class */
  section.cover {
    background: var(--cover-gradient) !important;
    color: white;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-family: var(--title-font);
    position: relative;
    padding: 80px 60px;
  }
  
  section.cover::before,
  section.cover::after {
    display: block !important;
  }
  
  section.cover h1 {
    font-size: 1.7rem;
    font-weight: 300;
    margin-bottom: 0.5em;
    letter-spacing: 2px;
    line-height: 1.2;
    text-transform: uppercase;
    color: var(--cover-secondary) !important;
    text-shadow: none;
    max-width: 90%;
    word-wrap: break-word;
    hyphens: auto;
    overflow-wrap: break-word;
  }
  
  section.cover h1 span {
    color: var(--cover-secondary) !important;
  }
  
  section.cover h2 {
    font-size: 1.1rem;
    font-weight: 300;
    opacity: 0.85;
    font-family: var(--light-font);
    letter-spacing: 2px;
    margin-bottom: 2.5em;
    color: var(--cover-accent);
    line-height: 1.3;
  }
  
  section.cover .company-info {
    position: absolute;
    bottom: 100px;
    left: 50%;
    transform: translateX(-50%);
    font-family: var(--body-font);
    font-size: 1.1rem;
    font-weight: 400;
    color: var(--cover-secondary);
    letter-spacing: 1px;
  }
  
  section.cover .confidential {
    position: absolute;
    bottom: 60px;
    left: 50%;
    transform: translateX(-50%);
    font-family: var(--light-font);
    font-size: 0.85rem;
    font-weight: 300;
    color: var(--cover-accent);
    letter-spacing: 2px;
    text-transform: uppercase;
  }
  
  /* Content Page Class */
  section.content {
    background: white !important;
    color: #212121;
    font-family: var(--body-font);
    font-size: 19px;
    padding: 70px 60px 80px 60px;
    line-height: 1.5;
    letter-spacing: 0.3px;
    position: relative;
    overflow: hidden;
  }
  
  .content-main {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    padding-bottom: 1em;
    min-height: calc(100vh - 150px);
  }
  
  /* Two-column layout for content pages */
  .two-column {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    margin-top: 1em;
  }
  
  .column {
    padding: 0;
  }
  
  .column h3 {
    margin-top: 0;
  }
  
  /* Enhanced spacing for pages with fewer content */
  .content-main > * {
    margin-bottom: 1.5em;
  }
  
  .content-main > *:last-child {
    margin-bottom: 0;
  }
  
  /* Fixed Header for Content Pages */
  section.content > h2:first-of-type {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 50px;
    background: white;
    color: var(--brand-primary) !important;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    font-family: var(--title-font);
    font-size: 1.3rem;
    font-weight: 600;
    letter-spacing: 1px;
    margin: 0;
    padding-left: 50px;
    z-index: 5;
    text-align: left;
    border-bottom: 4px solid #8c9eff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  section.content h1 {
    font-size: 2.1rem;
    font-weight: 600;
    color: var(--brand-primary);
    margin-bottom: 0.7em;
    font-family: var(--title-font);
    line-height: 1.3;
    overflow-wrap: break-word;
    word-wrap: break-word;
  }
  
  section.content h2 {
    font-size: 1.6rem;
    font-weight: 500;
    color: var(--brand-secondary);
    margin-bottom: 0.6em;
    margin-top: 1em;
    font-family: var(--title-font);
    line-height: 1.3;
    overflow-wrap: break-word;
  }
  
  section.content h3 {
    font-size: 1.3rem;
    font-weight: 500;
    color: var(--brand-primary);
    margin-bottom: 0.5em;
    margin-top: 0.8em;
    line-height: 1.3;
    overflow-wrap: break-word;
  }
  
  section.content p {
    margin-bottom: 0.8em;
    line-height: 1.6;
  }
  
  section.content ul, section.content ol {
    padding-left: 1.5em;
    margin-bottom: 1em;
  }
  
  section.content li {
    margin-bottom: 0.4em;
  }
  
  section.content table {
    width: auto;
    border-collapse: collapse;
    margin: 1.2em 0;
    font-size: 0.9em;
    table-layout: auto;
    box-shadow: none;
    border: none;
    border-radius: 6px;
    overflow: hidden;
  }
  
  section.content th {
    background: linear-gradient(135deg, var(--brand-primary), var(--brand-secondary));
    color: white;
    padding: 0.8em 1em;
    text-align: left;
    font-weight: 600;
    font-size: 0.95em;
    overflow-wrap: break-word;
    line-height: 1.3;
    border: none;
    position: relative;
  }
  
  section.content td {
    padding: 0.7em 1em;
    border: none;
    border-bottom: 1px solid #e0e0e0;
    overflow-wrap: break-word;
    word-break: break-word;
    line-height: 1.4;
    font-size: 0.9em;
    vertical-align: top;
  }
  
  section.content tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  
  section.content tr:last-child td {
    border-bottom: none;
  }
  
  /* Common Footer Background and Styles for pages with footers */
  section.content::after,
  section.thankyou::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 50px;
    background: var(--cover-gradient);
    display: block !important;
  }
  
  /* Common Footer Styles for all pages with footers */
  section.content .footer-left,
  section.thankyou .footer-left {
    position: absolute;
    bottom: 12px;
    left: 30px;
    color: rgba(255,255,255,0.7);
    font-family: var(--body-font);
    font-size: 1rem;
    font-weight: 400;
    z-index: 10;
  }
  
  section.content .footer-center,
  section.thankyou .footer-center {
    position: absolute;
    bottom: 12px;
    left: 50%;
    transform: translateX(-50%);
    color: rgba(255,255,255,0.7);
    font-family: var(--body-font);
    font-size: 1rem;
    font-weight: 400;
    z-index: 10;
  }
  
  section.content .footer-right,
  section.thankyou .footer-right {
    position: absolute;
    bottom: 12px;
    right: 30px;
    color: rgba(255,255,255,0.8);
    font-family: var(--light-font);
    font-size: 0.85rem;
    font-weight: 300;
    letter-spacing: 1px;
    text-transform: uppercase;
    z-index: 10;
  }
  
  /* Thank You Page Class */
  section.thankyou {
    background: white !important;
    color: #212121;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-family: var(--title-font);
    position: relative;
    padding: 40px 60px 80px 60px;
  }
  
  section.thankyou::before {
    display: block !important;
  }
  
  section.thankyou h1 {
    font-size: 3.2rem;
    font-weight: 300;
    color: #212121;
    margin-bottom: 0.4em;
    letter-spacing: 2px;
  }
  
  section.thankyou .blue-line {
    width: 150px;
    height: 3px;
    background: #1a237e;
    margin: 0 auto 1.5em auto;
  }
  
  section.thankyou .company-logo {
    font-family: var(--body-font);
    font-size: 1.6rem;
    font-weight: 600;
    color: #1a237e;
    margin-bottom: 1em;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
  }
  
  section.thankyou .address {
    font-family: var(--light-font);
    font-size: 1.1rem;
    color: #666;
    line-height: 1.5;
    margin-bottom: 1.5em;
  }
  
  section.thankyou .contact-info {
    display: flex;
    justify-content: center;
    gap: 40px;
    align-items: center;
    margin-bottom: 1.8em;
    flex-wrap: wrap;
  }
  
  section.thankyou .contact-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: var(--body-font);
    font-size: 1rem;
    color: #3949ab;
  }
  
  section.thankyou .contact-item .icon {
    font-size: 1.1rem;
    color: #1a237e;
  }
  
  /* Visual Design Elements */
  .info-box {
    background: var(--info-bg);
    border-left: 4px solid var(--brand-accent);
    padding: 1em;
    margin: 1em 0;
    border-radius: 0 6px 6px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }
  
  .success-box {
    background: var(--success-bg);
    border-left: 4px solid var(--success-color);
    padding: 1em;
    margin: 1em 0;
    border-radius: 0 6px 6px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }
  
  .warning-box {
    background: var(--warning-bg);
    border-left: 4px solid var(--warning-color);
    padding: 1em;
    margin: 1em 0;
    border-radius: 0 6px 6px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }
  
  .error-box {
    background: var(--error-bg);
    border-left: 4px solid var(--error-color);
    padding: 1em;
    margin: 1em 0;
    border-radius: 0 6px 6px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }
  
  .metric-card {
    background: var(--neutral-bg);
    padding: 1.2em;
    border-radius: 8px;
    text-align: center;
    margin: 0.5em;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
  }
  
  .metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  }
  
  .metric-value {
    font-size: 1.8em;
    font-weight: bold;
    margin: 0.2em 0;
    color: var(--brand-primary);
  }
  
  .step-card {
    background: white;
    text-align: center;
    border-radius: 8px;
    overflow: hidden;
    margin: 0.5em;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  }
  
  .step-number {
    background: var(--brand-primary);
    color: white;
    padding: 0.8em 1em;
    font-weight: bold;
    font-size: 1.1em;
    margin: 0;
    display: block;
  }
  
  .step-card:nth-child(1) .step-number {
    background: #2b5797;
  }
  
  .step-card:nth-child(2) .step-number {
    background: #4caf50;
  }
  
  .step-card:nth-child(3) .step-number {
    background: #ff9800;
  }
  
  .step-content {
    padding: 1.5em 1.2em;
    background: #e3f2fd;
    min-height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  
  .step-card:nth-child(1) .step-content {
    background: #e3f2fd;
  }
  
  .step-card:nth-child(2) .step-content {
    background: #e8f5e9;
  }
  
  .step-card:nth-child(3) .step-content {
    background: #fff3e0;
  }
  
  .step-icon {
    font-size: 1.8em;
    margin-bottom: 0.3em;
  }
  
  .highlight {
    background: linear-gradient(transparent 60%, #ffeb3b 60%);
    padding: 0 0.2em;
    font-weight: bold;
  }
  
  .badge {
    background: var(--brand-accent);
    color: white;
    padding: 0.3em 0.8em;
    border-radius: 15px;
    font-size: 0.85em;
    font-weight: 600;
    margin: 0.2em;
    display: inline-block;
  }
  
  .success-badge {
    background: var(--success-color);
    color: white;
    padding: 0.3em 0.8em;
    border-radius: 15px;
    font-size: 0.85em;
    font-weight: 600;
    margin: 0.2em;
    display: inline-block;
  }
  
  .warning-badge {
    background: var(--warning-color);
    color: white;
    padding: 0.3em 0.8em;
    border-radius: 15px;
    font-size: 0.85em;
    font-weight: 600;
    margin: 0.2em;
    display: inline-block;
  }
  
  .timeline-item {
    display: flex;
    align-items: center;
    margin: 1em 0;
    padding: 0.8em;
    border-radius: 8px;
    background: rgba(26, 35, 126, 0.05);
  }
  
  .timeline-badge {
    background: var(--brand-primary);
    color: white;
    padding: 0.5em 1em;
    border-radius: 20px;
    min-width: 100px;
    text-align: center;
    font-weight: bold;
    margin-right: 1em;
    flex-shrink: 0;
  }
  
  .icon-text {
    display: flex;
    align-items: flex-start;
    margin: 0.8em 0;
  }
  
  .icon-text .icon {
    font-size: 1.5em;
    margin-right: 0.5em;
    flex-shrink: 0;
    margin-top: 0.1em;
  }
  
  .grid-2 {
    display: flex;
    gap: 1.5em;
    margin: 1em 0;
  }
  
  .grid-2 > * {
    flex: 1;
  }
  
  .grid-3 {
    display: flex;
    gap: 1em;
    margin: 1em 0;
    justify-content: space-between;
  }
  
  .grid-3 > * {
    flex: 1;
    max-width: calc(33.333% - 0.67em);
  }
  
  .grid-4 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 1em;
    margin: 1em 0;
  }
  
  @media (max-width: 768px) {
    .grid-2, .grid-3, .grid-4 {
      grid-template-columns: 1fr;
    }
  }
  
  /* ROI and Summary Styles */
  .roi-box {
    background: var(--success-bg);
    padding: 1.5em;
    border-radius: 8px;
    margin: 1em 0;
    text-align: center;
    border: 2px solid var(--success-color);
  }
  
  .roi-highlight {
    font-size: 1.3em;
    color: var(--warning-color);
    font-weight: bold;
  }
  
  .summary-box {
    background: linear-gradient(135deg, var(--brand-primary), var(--brand-secondary));
    color: white;
    padding: 1.5em;
    border-radius: 8px;
    text-align: center;
    margin: 1em 0;
  }
  
  .summary-title {
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 0.3em;
  }
  
  .metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1em;
    margin: 1.5em 0;
  }
  
  .metric-box {
    background: white;
    border-radius: 8px;
    padding: 1.2em;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    border: 2px solid #e0e0e0;
  }
  
  .metric-box.metric-green {
    background: #e8f5e9;
    border: 2px solid #4caf50;
    border-left: 6px solid #4caf50;
  }
  
  .metric-box.metric-blue {
    background: #e3f2fd;
    border: 2px solid #2196f3;
    border-left: 6px solid #2196f3;
  }
  
  .metric-box.metric-orange {
    background: #fff3e0;
    border: 2px solid #ff9800;
    border-left: 6px solid #ff9800;
  }
  
  .metric-box.metric-red {
    background: #fce4ec;
    border: 2px solid #f44336;
    border-left: 6px solid #f44336;
  }
  
  .metric-icon {
    font-size: 1.5em;
    margin-bottom: 0.3em;
  }
  
  .metric-label {
    font-size: 0.9em;
    font-weight: bold;
    margin-bottom: 0.3em;
  }
  
  .metric-box.metric-green .metric-label {
    color: #4caf50;
  }
  
  .metric-box.metric-blue .metric-label {
    color: #2196f3;
  }
  
  .metric-box.metric-orange .metric-label {
    color: #ff9800;
  }
  
  .metric-box.metric-red .metric-label {
    color: #f44336;
  }
  
  .metric-number {
    font-size: 1.8em;
    font-weight: bold;
    color: #333;
    margin: 0.2em 0;
  }
  
  .metric-description {
    font-size: 0.85em;
    color: #666;
    margin-top: 0.2em;
    line-height: 1.3;
  }
  
  /* Gantt Chart Styles */
  .gantt-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 0.85em;
  }
  
  .gantt-table th {
    background: var(--brand-primary);
    color: white;
    padding: 0.6em;
    text-align: left;
    font-weight: 600;
    border: 1px solid var(--brand-primary);
  }
  
  .gantt-table td {
    padding: 0.5em;
    border: 1px solid #ddd;
    vertical-align: middle;
  }
  
  .gantt-table tr:nth-child(even) {
    background: #f9f9f9;
  }
  
  .gantt-bar {
    background: var(--brand-primary) !important;
    color: var(--brand-primary) !important;
    text-align: center;
    padding: 0.4em 0.2em;
    border-radius: 3px;
    min-height: 1.2em;
    font-family: monospace;
    font-weight: bold;
  }
  
  .milestone-list {
    background: var(--info-bg);
    padding: 1em;
    border-radius: 8px;
    margin: 1em 0;
  }
  
  .milestone-item {
    display: flex;
    align-items: center;
    margin: 0.5em 0;
    padding: 0.5em;
    background: white;
    border-radius: 4px;
  }
  
  .milestone-date {
    font-weight: bold;
    color: var(--brand-primary);
    margin-right: 1em;
    min-width: 80px;
  }
  
  .milestone-complete {
    color: var(--success-color);
    margin-left: auto;
  }
  
  /* Large Step Cards */
  .step-large {
    background: white;
    padding: 2em 1.5em;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    position: relative;
    border-top: 4px solid var(--brand-primary);
  }
  
  .step-large-number {
    background: var(--brand-primary);
    color: white;
    font-size: 1.3em;
    font-weight: bold;
    padding: 0.8em 1em;
    margin: 0;
    display: block;
  }
  
  .step-large.step-blue .step-large-number {
    background: #2b5797;
  }
  
  .step-large.step-green .step-large-number {
    background: #4caf50;
  }
  
  .step-large.step-orange .step-large-number {
    background: #ff9800;
  }
  
  .step-large-content {
    padding: 1.5em 1.2em;
    min-height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  
  .step-large.step-blue .step-large-content {
    background: #e3f2fd;
  }
  
  .step-large.step-green .step-large-content {
    background: #e8f5e9;
  }
  
  .step-large.step-orange .step-large-content {
    background: #fff3e0;
  }
  
  .step-large-icon {
    font-size: 2em;
    margin-bottom: 0.5em;
  }
  
  .step-large-title {
    font-size: 1em;
    font-weight: 400;
    color: #333;
    line-height: 1.4;
  }
  
  .step-large-description {
    color: #666;
    line-height: 1.4;
  }
  
  /* Color-coded Step Cards */
  .step-blue { background: var(--info-bg) !important; }
  .step-green { background: var(--success-bg) !important; }
  .step-orange { background: var(--warning-bg) !important; }
---

<!-- _class: cover -->

# <span style="color: rgba(255,255,255,0.9);">PROJECT TITLE</span>
## システム開発・技術提案

<div class="company-info">FUJISOFT America, Inc.</div>
<div class="confidential">CONFIDENTIAL</div>

---

<!-- _class: content -->

## プロジェクト概要

### 目標
- **効率化**: 業務プロセス最適化
- **デジタル変革**: システム統合・自動化
- **ユーザビリティ**: 直感的なUI/UX設計
- **スケーラビリティ**: 将来拡張への対応

### 技術ソリューション
- **基幹システム**: 統合プラットフォーム構築
- **BI・分析**: データ可視化・経営ダッシュボード
- **API連携**: 外部システム統合
- **クラウド基盤**: 高可用性インフラ構築

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">2</div>
<div class="footer-right">CONFIDENTIAL</div>

---

<!-- _class: content -->

## 開発フェーズ概要

| フェーズ | 期間 | 主要成果物 | 責任者 |
|---------|------|------------|--------|
| **要件定義** | Phase 1 | 業務要件・システム要件定義 | プロジェクトチーム |
| **基本設計** | Phase 2 | アーキテクチャ・統合設計 | 技術チーム |
| **詳細設計** | Phase 3 | 詳細仕様・実装設計 | 開発チーム |
| **開発・テスト** | Phase 4 | システム開発・品質保証 | 開発・QAチーム |

### 重要ポイント
- **お客様責任**: 業務要件・承認・ユーザートレーニング
- **FUJISOFT責任**: システム設計・開発・技術サポート
- **合同作業**: 要件レビュー・受入テスト・本番移行

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">3</div>
<div class="footer-right">CONFIDENTIAL</div>

---


<!-- _class: content -->

## テンプレート使用ガイド

### 基本的な構造
このテンプレートは3つの主要なクラスを使用します：
- **cover**（カバーページ）
- **content**（内容ページ）
- **thankyou**（終了ページ）

### カバーページ（class: cover）
表紙として使用します。以下の構造で記述：

```markdown
<!-- _class: cover -->
# <span style="color: rgba(255,255,255,0.9);">プロジェクトタイトル</span>
## サブタイトル
<div class="company-info">FUJISOFT America, Inc.</div>
<div class="confidential">CONFIDENTIAL</div>
```

### 📝 フォントサイズガイドライン

<div class="grid-2">
<div class="info-box">
**標準サイズ（推奨）**
- 見出し（h1）: 36-48pt
- サブ見出し（h2）: 28-36pt  
- 本文テキスト: 24-28pt
- 注釈・キャプション: 20-22pt
</div>
<div class="success-box">
**カスタムサイズ**
```html
<div style="font-size: 2em;">大見出し</div>
<div style="font-size: 1.2em;">強調テキスト</div>
<div style="font-size: 0.9em;">小さな注釈</div>
```
</div>
</div>

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">4</div>
<div class="footer-right">CONFIDENTIAL</div>

---

<!-- _class: content -->

## 内容ページ（class: content）

### 通常のスライド内容に使用
```markdown
<!-- _class: content -->
## ページタイトル
### セクション見出し
- 箇条書き項目
- 項目2

| 項目 | 内容 | 備考 |
|------|------|------|
| 例1  | 内容1 | 備考1 |

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">ページ番号</div>
<div class="footer-right">CONFIDENTIAL</div>
```

### 重要なポイント
- 最初の ## がページタイトルとして自動的にヘッダーに表示
- フッター3要素（left/center/right）を各ページに追加
- center にはページ番号を記述

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">5</div>
<div class="footer-right">CONFIDENTIAL</div>

---

<!-- _class: content -->

## 終了ページ・注意点・カスタマイズ

### 終了ページ（class: thankyou content）
```markdown
<!-- _class: thankyou content -->
# Thank You
<div class="blue-line"></div>
<div class="company-logo">FUJISOFT America, Inc.</div>
<div class="address">住所情報</div>
<div class="contact-info">
  <div class="contact-item">
    <span class="icon">📞</span>電話番号
  </div>
</div>
```

### 重要な注意点
- 各スライドは `---` で区切る
- クラス指定は `<!-- _class: クラス名 -->` で行う
- フッター要素は各ページで必須

### カスタマイズ
- タイトルや内容は自由に変更可能
- 連絡先情報は実際の情報に変更してください

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">6</div>
<div class="footer-right">CONFIDENTIAL</div>

---

<!-- _class: content -->

## 📊 視覚的デザイン要素サンプル

### 情報ボックス（色別）

<div class="info-box">
<strong>情報ボックス（青）</strong><br>
重要な情報や説明を目立たせたい時に使用します
</div>

<div class="success-box">
<strong>成功・完了ボックス（緑）</strong><br>
成果や達成事項、ポジティブな情報に使用します
</div>

<div class="warning-box">
<strong>注意・警告ボックス（オレンジ）</strong><br>
注意事項やリスク、重要な警告に使用します
</div>

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">7</div>
<div class="footer-right">CONFIDENTIAL</div>

---

<!-- _class: content -->

## 📈 メトリック表示とバッジ

### 数値指標の効果的な表示

<div class="grid-2">
<div class="metric-card">
<strong style="color: #4caf50;">✅ 効率向上</strong><br>
<div class="metric-value">35%</div>
処理時間の短縮を実現
</div>
<div class="metric-card">
<strong style="color: #2196f3;">📊 精度向上</strong><br>
<div class="metric-value">99.8%</div>
システム精度を達成
</div>
</div>

### バッジとハイライト

<div class="success-badge">達成済み</div>
<div class="badge">進行中</div>
<div class="warning-badge">要注意</div>

重要な <span class="highlight">キーワードの強調</span> も効果的です。

### 📏 コンテンツ密度ガイドライン

<div class="warning-box">
**推奨制限（品質確保のため）**
- **テーブル**: 最大5行まで（ヘッダー除く）
- **箇条書き**: 最大8項目まで
- **フッタークリアランス**: 底部100px確保必須
- **1スライド1メッセージ**: 複数トピックは分割推奨
</div>

<div class="info-box">
**💡 密度が高い場合の対処法**
- 内容を複数スライドに分割
- 重要度に応じた優先順位付け
- サマリーページの活用
</div>

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">8</div>
<div class="footer-right">CONFIDENTIAL</div>

---

<!-- _class: content -->

## 🚀 3ステッププロセス

### わかりやすいステップ表示

<div class="grid-3">
<div class="step-card">
<div class="step-number">STEP 1</div>
<div class="step-content">
<div class="step-icon">📋</div>
ドライバーのスマホで<br>配送完了を記録
</div>
</div>
<div class="step-card">  
<div class="step-number">STEP 2</div>
<div class="step-content">
<div class="step-icon">📸</div>
写真・署名・位置情報を<br>自動で保存
</div>
</div>
<div class="step-card">
<div class="step-number">STEP 3</div>
<div class="step-content">
<div class="step-icon">📊</div>
管理画面で配送状況を<br>リアルタイム確認
</div>
</div>
</div>

### タイムライン表示

<div class="timeline-item">
<div class="timeline-badge">1ヶ月目</div>
<div>
<strong>準備フェーズ</strong><br>
要件確認・環境構築・基準設定
</div>
</div>

<div class="timeline-item">
<div class="timeline-badge">2ヶ月目</div>
<div>
<strong>実装フェーズ</strong><br>
システム開発・テスト・結果分析
</div>
</div>

</div>

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">9</div>
<div class="footer-right">CONFIDENTIAL</div>

---

<!-- _class: content -->

## ✅ アイコンとテキストの組み合わせ

### 効果的な項目表示

<div class="icon-text">
<div class="icon" style="color: #4caf50;">✓</div>
<div>
<strong>特定製品に偏らない公平な選定</strong><br>
自社製品の押し売りではなく、最適なシステムを提案
</div>
</div>

<div class="icon-text">
<div class="icon" style="color: #4caf50;">✓</div>
<div>
<strong>現場第一主義</strong><br>
理論ではなく、実際に現場で使いやすい仕組みを構築
</div>
</div>

<div class="icon-text">
<div class="icon" style="color: #4caf50;">✓</div>
<div>
<strong>スピーディーな導入</strong><br>
短期間でテスト運用開始、効率的な本番稼働
</div>
</div>

### リスクと対策の対比

<div class="grid-2">
<div>
<strong style="color: #ff9800;">⚠️ 想定リスク</strong>
<ul style="list-style: none; padding: 0;">
<li style="margin: 0.5em 0;">❗ データ移行の失敗</li>
<li style="margin: 0.5em 0;">❗ システム間連携の遅延</li>
<li style="margin: 0.5em 0;">❗ ユーザー研修不足</li>
</ul>
</div>
<div>
<strong style="color: #4caf50;">✅ 対策・解決法</strong>
<ul style="list-style: none; padding: 0;">
<li style="margin: 0.5em 0;">✅ 段階的移行とバックアップ</li>
<li style="margin: 0.5em 0;">✅ 複数の連携方式を準備</li>
<li style="margin: 0.5em 0;">✅ 体系的な研修プログラム</li>
</ul>
</div>
</div>

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">10</div>
<div class="footer-right">CONFIDENTIAL</div>

---

<!-- _class: content -->

## 📈 期待できる効果

### 想定している数値改善（目標値）

<div class="metric-grid">
<div class="metric-box metric-green">
<div class="metric-icon" style="color: #4caf50;">✅</div>
<div class="metric-label">配送証明の取得率（目標）</div>
<div class="metric-number">99%以上</div>
<div class="metric-description">ほぼ全ての配送で証明取得を目指します</div>
</div>
<div class="metric-box metric-blue">
<div class="metric-icon" style="color: #2196f3;">✅</div>
<div class="metric-label">荷物受け入れ時間（目標）</div>
<div class="metric-number">8分以内</div>
<div class="metric-description">システム化で最大35%短縮を目標とします</div>
</div>
<div class="metric-box metric-orange">
<div class="metric-icon" style="color: #ff9800;">✅</div>
<div class="metric-label">誤配送率（目標）</div>
<div class="metric-number">0.3%以下</div>
<div class="metric-description">一般的な率から60%削減を目標とします</div>
</div>
<div class="metric-box metric-red">
<div class="metric-icon" style="color: #f44336;">✅</div>
<div class="metric-label">問題追跡時間（目標）</div>
<div class="metric-number">20分以内</div>
<div class="metric-description">トラブル発生時の迅速な原因特定を目指します</div>
</div>
</div>

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">11</div>
<div class="footer-right">CONFIDENTIAL</div>

---

<!-- _class: content -->

## 💰 投資対効果

### わかりやすい費用対効果

<div class="roi-box">
<strong style="font-size: 1.3em;">投資額：$46,000（3ヶ月間のコンサルティング費用）</strong>
</div>

<p style="font-size: 0.8em; color: #666; margin: 0.3em 0;">※ 以下は想定している効果です。実際の効果は店舗数・配送件数・運用方法によって異なります</p>

<div class="grid-2">
<div class="info-box">
<strong>人件費削減効果（想定）</strong><br>
3施設・1日60件の配送で<br>
<span class="highlight">月額 $2,200削減</span>
</div>
<div class="success-box">
<strong>誤配送防止効果（想定）</strong><br>
再配達コストの削減で<br>
<span class="highlight">月額 $4,200削減</span>
</div>
</div>

<div class="summary-box" style="margin-top: 1em; margin-bottom: 120px;">
<div style="font-size: 1.1em;">合計で月額 $6,000〜$8,000 のコスト削減（想定）<span class="roi-highlight">→ 8ヶ月で投資回収</span></div>
</div>

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">12</div>
<div class="footer-right">CONFIDENTIAL</div>

---

<!-- _class: content -->

## 🎯 まとめ

<div class="summary-box">
<div class="summary-title">💰 投資対効果</div>
<div>3ヶ月・$46,000の投資で月額$6,000〜$8,000のコスト削減（想定）</div>
<div style="font-size: 0.9em; margin-top: 0.3em; opacity: 0.9;">→ 8ヶ月で投資回収完了</div>
</div>

### 実現する成果

<div class="grid-3">
<div class="success-box" style="padding: 1em; text-align: center;">
<div style="font-size: 1.2em; margin-bottom: 0.3em;">📍</div>
<div style="font-weight: bold;">配送証明取得率</div>
<div style="font-size: 1.8em; font-weight: bold; margin: 0.2em 0;">99%以上</div>
</div>
<div class="info-box" style="padding: 1em; text-align: center;">
<div style="font-size: 1.2em; margin-bottom: 0.3em;">⚡</div>
<div style="font-weight: bold;">荷物受け入れ</div>
<div style="font-size: 1.8em; font-weight: bold; margin: 0.2em 0;">8分以内</div>
</div>
<div class="warning-box" style="padding: 1em; text-align: center;">
<div style="font-size: 1.2em; margin-bottom: 0.3em;">📉</div>
<div style="font-weight: bold;">誤配送削減</div>
<div style="font-size: 1.8em; font-weight: bold; margin: 0.2em 0;">60%減</div>
</div>
</div>

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">13</div>
<div class="footer-right">CONFIDENTIAL</div>

---

<!-- _class: content -->

## 📅 主要マイルストーン・スケジュール

### フェーズ別マイルストーン


| フェーズ | 期間 | 7月 | 8月 | 9月 | 10月 | 11月 | 12月 | 主要成果物 |
|----------|------|-----|-----|-----|------|------|------|-----------|
| **要件定義** | 4週 | ████ |  |  |  |  |  | 要件仕様書 |
| **開発** | 13週 | ██ | ████ | ████ | █ |  |  | 8部門CRM機能 |
| **統合テスト** | 4週 |  |  |  | ██ | ██ |  | 品質保証完了 |
| **受入テスト** | 1週 |  |  |  |  | █ |  | ユーザー承認 |
| **本番導入** | 2週 |  |  |  |  | █ | █ | 本番稼働開始 |


### 重要マイルストーン

<div class="milestone-list" style="margin-bottom: 160px;">
<div class="milestone-item">
<span class="milestone-date">7/31</span>
<span>要件定義完了</span>
<span class="milestone-complete">✓</span>
</div>
<div class="milestone-item">
<span class="milestone-date">10/31</span>
<span>Development完了</span>
</div>
</div>


<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">14</div>
<div class="footer-right">CONFIDENTIAL</div>

---

<!-- _class: content -->

## Two-Columnレイアウト使用例

<div class="two-column">
<div class="column">

### 左カラム
**プロジェクト要件**
- システム統合
- データ移行

**技術スタック**
- Frontend: React/Vue.js
- Backend: Node.js/Python

</div>
<div class="column">

### 右カラム
**実装スケジュール**
- Phase 1: 要件定義（2週間）
- Phase 2: 設計開発（8週間）

**チーム構成**
- プロジェクトマネージャー: 1名
- フロントエンド開発者: 2名

</div>
</div>

### Two-Columnレイアウトの使用方法

```markdown
<div class="two-column">
<div class="column">
左側の内容
</div>
<div class="column">
右側の内容
</div>
</div>
```

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">15</div>
<div class="footer-right">CONFIDENTIAL</div>

---

<!-- _class: content -->

## 🔍 視覚レビューツール

### 自動品質チェック機能

このテンプレートには**自動視覚レビューツール**が付属しています：

<div class="grid-2">
<div class="info-box">
**📋 検出項目**
- フッター重複（底部100pxエリア）
- コンテンツオーバーフロー
- レイアウト崩れの自動検出
- 品質スコア算出（100点満点）
</div>
<div class="success-box">
**🚀 使用方法**
```bash
# HTMLに変換
marp slides.md -o slides.html
# 視覚レビュー実行
cd scripts && node visual-review.js ../slides.html
```
</div>
</div>

### レビューレポート

- **HTMLレポート**: `review-output/review-report.html`
- **スクリーンショット**: 各スライドの視覚確認用画像
- **JSON詳細データ**: 自動化・CI/CD統合用

<div class="warning-box">
**⚠️ 推奨タイミング**: 最終確認前に必ず実行して品質を確保してください
</div>

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">17</div>
<div class="footer-right">CONFIDENTIAL</div>

---

<!-- _class: thankyou content -->

# Thank You

<div class="blue-line"></div>

<div class="company-logo">FUJISOFT America, Inc.</div>

<div class="address">
1710 S. Amphlett Blvd<br>
Suite 215<br>
San Mateo, CA 94402
</div>

<div class="contact-info">
  <div class="contact-item">
    <span class="icon">📞</span>
    650-235-9422
  </div>
  <div class="contact-item">
    <span class="icon">✉️</span>
    inquiry@your-company.com
  </div>
</div>

<div class="footer-left">FUJISOFT America, Inc.</div>
<div class="footer-center">16</div>
<div class="footer-right">CONFIDENTIAL</div>

