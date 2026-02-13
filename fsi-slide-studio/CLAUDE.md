# FSI Slide Studio — Project Rules

## Progress Reporting (MANDATORY)

Always keep the user informed of your progress. At each phase transition, provide a brief status update:

- Phase 1→2: "十分な情報が集まりました。関連スキルを読み込んで構成案を作成します..."
- Phase 2→3 (after user approves structure): "構成が確定しました。MARPスライドを生成します..."
- Phase 3→4: "スライド生成完了。デザイン品質レビューを実行中..."
- Phase 4→done: "PDF生成完了！品質レビュー結果のサマリーです..."

During slide generation (Phase 3), provide intermediate updates:
- "表紙とエグゼクティブサマリーを生成中..."
- "メインコンテンツのスライドを作成中..."
- "まとめとサンキューページを仕上げ中..."

## Skill Usage Reporting (MANDATORY)

When you load a domain skill, ALWAYS tell the user which skill you loaded and why.
Example: "I'm loading the **financial-analyst** skill to include ROI analysis frameworks and industry benchmarks."

## Feedback Prompt (MANDATORY)

After delivering the PDF, ALWAYS explicitly offer refinements:

"Would you like to make any changes?
- Content: Add, remove, or modify slides
- Design: Change layout, colors, or visual elements
- Overflow fix: Adjust slides where content doesn't fit
- Tone: Make it more formal/casual/technical

Just describe what you'd like to change and I'll update the presentation."

When the user requests changes:
1. Regenerate only the affected slides (not the entire presentation)
2. Run review_design again on the updated markdown
3. Convert to PDF again
4. Ask if further changes are needed

## Enhanced Quality Rules (override system prompt defaults)

### Bullet Point Limits
- Maximum **5** bullet points per slide (not 8)
- Each bullet: maximum 2 lines (~80 chars EN / ~40 chars JP per line)
- Sub-bullets: maximum 2 levels deep, maximum 3 sub-items

### Table Limits
- Maximum **4** rows (excluding header), maximum 5 columns
- Cell text: maximum 30 characters per cell
- If more data is needed, SPLIT across multiple slides

### Content Height Budget (CRITICAL for overflow prevention)
- MARP viewport: 1280x720px
- Available content area after header/footer/padding: ~520px height
- Approximate element heights:
  - H2 title: 50px, H3 heading: 40px
  - Each bullet: 35px, each table row: 40px, table header: 45px
  - Info-box: 80px, metric-box row: 120px
- Before finalizing each slide, mentally add up element heights
- If total > 450px → consider splitting
- **If total > 520px → MUST split. This is non-negotiable.**

### Combination Rules (prevents the most common overflow)
- Table + bullets on same slide: maximum 2 short bullets above/below the table
- Metric-grid on a slide: NO additional bullet lists on that slide
- Info-box + other visual elements: maximum 1 info-box per slide
- **When in doubt, ALWAYS split into more slides. Extra slides are better than overflow.**
