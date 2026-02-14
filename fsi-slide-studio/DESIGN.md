# FSI Slide Studio - 設計書

## Context

FUJISOFT America 社内の誰もが、チャットで話しかけるだけでプロフェッショナルなプレゼンテーションを自動生成できる Web アプリ。既存の `fujisoft-presentation-creator` スキルのテンプレートと品質基準を活用し、63 ドメイン専門スキルの知識を動的にロードしてスライド内容の質を高める。

## アーキテクチャ概要

```
┌─────────────────────────────────────────────┐
│  Streamlit Frontend (Chat UI)               │
│  - st.chat_input / st.chat_message          │
│  - IME composition fix (JS injection)       │
│  - Streaming: token-level deltas            │
│  - Slide preview (HTML iframe)              │
│  - PDF / Markdown download                  │
│  - Tool activity display                    │
└──────────────┬──────────────────────────────┘
               │ User message
               ▼
┌─────────────────────────────────────────────┐
│  AsyncBridge (Persistent Event Loop)        │
│  - Survives Streamlit reruns                │
│  - run_until_complete on main thread        │
└──────────────┬──────────────────────────────┘
               │ Coroutine dispatch
               ▼
┌─────────────────────────────────────────────┐
│  Claude Agent SDK (Python)                  │
│  - ClaudeSDKClient (multi-turn session)     │
│  - System prompt: presentation expert       │
│  - CLAUDE.md: 品質ルール・行動指示         │
│  - Custom MCP tools (7 tools):              │
│    - list_skills: 利用可能スキル一覧        │
│    - load_skill: スキル知識の動的ロード     │
│    - convert_to_pdf: MARP→PDF 変換          │
│    - convert_to_html: MARP→HTML 変換        │
│    - render_mermaid: Mermaid→PNG 変換       │
│    - review_structure: 構成レビュー         │
│    - review_design: デザインレビュー        │
└──────────────┬──────────────────────────────┘
               │ Reads on-demand
               ▼
┌─────────────────────────────────────────────┐
│  Skill Library (knowledge base)             │
│  - 63 skills (44 curated + 19 auto-discovered) │
│  - 13 categories                            │
│  - fujisoft-presentation-creator template   │
│  - presentation_best_practices_checklist.md │
└─────────────────────────────────────────────┘
```

## 技術スタック

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend | Streamlit | >= 1.42 | Chat UI, file download, preview |
| Agent | claude-agent-sdk (Python) | latest | Multi-turn AI conversation |
| Template | MARP (marp-cli) | 4.2.x | Markdown → PDF/HTML 変換 |
| Diagrams | mermaid-cli (mmdc) | 11.x | Mermaid → PNG 変換 |
| Language | Python | >= 3.11 | Backend logic |
| Model | Claude Sonnet 4.5 | latest | コスト効率とスピードのバランス |

## プロジェクト構造

```
fsi-slide-studio/
├── app.py                    # Streamlit メインアプリ (IME fix, AsyncBridge, streaming)
├── CLAUDE.md                 # エージェント行動ルール (品質ルール, 進捗報告, フィードバック案内)
├── agent/
│   ├── __init__.py
│   ├── async_bridge.py       # 永続イベントループ (Streamlit↔SDK ブリッジ)
│   ├── client.py             # Claude Agent SDK クライアント管理 (streaming 対応)
│   ├── system_prompt.py      # システムプロンプト構築 (4フェーズワークフロー)
│   ├── tools.py              # カスタム MCP ツール定義 (7ツール)
│   └── tool_activity.py      # ツール実行ログのフォーマット (完了ラベル, キャプション生成)
├── skills/
│   ├── __init__.py
│   ├── router.py             # スキルルーティング
│   └── catalog.py            # スキルカタログ (YAML 読込, コンテンツ読込, 3000-byte truncation)
├── converter/
│   ├── __init__.py
│   └── marp.py               # MARP CLI ラッパー (PDF + HTML + Mermaid PNG)
├── config/
│   ├── settings.py           # アプリ設定 (OUTPUT_DIR/LOG_DIR 自動作成, setup_logging)
│   └── skill_categories.yaml # スキルカテゴリマッピング (13カテゴリ, 44 curated skills)
├── tests/                    # ユニットテスト
│   ├── conftest.py           # SDK モック注入 + 共通 fixtures
│   ├── unit/                 # ユニットテスト (118 テスト)
│   └── fixtures/             # テスト用データ
├── output/                   # 生成物の一時保存 (PDF, HTML, Markdown, PNG)
├── logs/                     # アプリケーションログ
├── Dockerfile
├── render.yaml
├── requirements.txt
├── pyproject.toml            # pytest 設定
├── .env.example
└── DESIGN.md                 # この設計書
```

---

## スキルローディングアーキテクチャ

FSI Slide Studio は Claude Code の組み込み `.claude/skills/` メカニズムではなく、**独自の MCP ツールベースのシステム**でスキルを読み込む。**YAML カテゴリ定義 + ファイルシステム自動検出**のハイブリッド方式で、新しいスキルを `skills/` に追加するだけで自動的にカタログに載る。

```
config/skill_categories.yaml   ← カテゴリ・スキル名・説明・キーワードを定義（curated）
         │
         ▼
skills/catalog.py              ← YAML + 自動検出を統合し、以下の関数を提供:
├── get_all_skills()           │  1. YAML 定義スキル → カテゴリ付きでリスト化
│                              │  2. ディスクスキャン → YAML 未登録スキルを "Other" に追加
│                              │  3. SKILL.md フロントマターから description を自動抽出
├── get_skill_catalog_text()   │  全スキルのカテゴリ別カタログテキスト
├── load_skill_content()       │  SKILL.md + references/*.md を結合して返却
│                              │  (各 reference は 3000 bytes で truncation)
└── list_skill_names()         │  ディスク上に存在するスキル名一覧
         │
         │ load_skill_content() は以下のパスからスキルを読み込む:
         ▼
SKILLS_LIBRARY_PATH            ← シブリングリポジトリの skills/ ディレクトリ
  (default: ../claude-skills-library/skills/)
         │
         ├── financial-analyst/SKILL.md        ← YAML 登録済み (Finance)
         ├── financial-analyst/references/*.md
         ├── aws-cli-expert/SKILL.md           ← 自動検出 (Other)
         └── ...
```

### 読み込みフロー

1. `system_prompt.py` がビルド時に `get_skill_catalog_text()` を呼び出し、全スキルの名前・説明をシステムプロンプトに埋め込む
2. エージェントが `list_skills` MCP ツールで動的にカタログを取得（YAML + 自動検出の全スキル）
3. トピックに応じて `load_skill` MCP ツールで特定スキルの知識（SKILL.md + references）をオンデマンドで読み込む
4. 読み込んだ知識がスライド内容の質を高める

### スキル追加手順

1. `skills/` ディレクトリに新しいスキルフォルダを作成（`SKILL.md` 必須）
2. **それだけで完了** — 自動検出により "Other" カテゴリに追加される
3. （任意）`skill_categories.yaml` にエントリを追加してカテゴリを指定

### スキルカタログ（13カテゴリ, 63スキル）

| カテゴリ | スキル数 | 方式 | 例 |
|---------|---------|------|-----|
| Strategy | 5 | YAML | ai-adoption-consultant, strategic-planner, design-thinking |
| Finance | 4 | YAML | financial-analyst, m-and-a-advisor, pricing-strategist |
| Operations | 7 | YAML | business-analyst, project-manager, lean-six-sigma-consultant, kpi-designer |
| Compliance | 8 | YAML | compliance-advisor, contract-reviewer, bcp-planner, pci-dss |
| IT | 4 | YAML | itil4-consultant, dama-dmbok, helpdesk-responder, office-script-expert |
| Salesforce | 2 | YAML | salesforce-expert, salesforce-flow-expert |
| Presentation | 2 | YAML | fujisoft-presentation-creator, critical-document-reviewer |
| Analytics | 2 | YAML | data-scientist, data-visualization-expert |
| Content | 2 | YAML | executive-briefing-writer, ai-text-humanizer |
| HR | 1 | YAML | talent-acquisition-specialist |
| Vendor | 3 | YAML | vendor-rfq-creator, vendor-estimate-creator, vendor-estimate-reviewer |
| QA | 4 | YAML | bug-ticket-creator, qa-bug-analyzer, uat-testcase-generator |
| Other | 19 | **自動検出** | aws-cli-expert, duckdb-expert, ffmpeg-expert, streamlit-expert 等 |

---

## ワークフロー設計（4 フェーズ）

### 全体フロー図

```
User ──→ Phase 1: ヒアリング ──→ Phase 2: スキルロード + 構成提案（内部レビュー込み）
                 ↑ 質問ループ                   │
                 └─────────┘                   ▼
                                          User 承認
                                               │
                                               ▼
                                        Phase 3: スライド生成
                                               │
                                               ▼
                                        Phase 4: デザインレビュー（自動）
                                               │
                                               ▼
                                        自動修正 → PDF + Markdown 出力
                                               │
                                               ▼
                                        フィードバック案内
```

### Phase 1: ヒアリング（深掘り質問）

**目的**: ユーザーの要望を正確に理解し、高品質なプレゼン生成に必要な情報を収集する。

**動作**:
1. ユーザーの初回メッセージを受け取る
2. **スライド構成を提案せず**、3〜5つの的確な質問を返す
3. 回答を受けて追加質問、を繰り返す
4. 十分な情報が集まったら次フェーズへ

**質問カテゴリ**:

| カテゴリ | 質問例 |
|---------|--------|
| 目的・ゴール | このプレゼンで何を決定・承認してもらいたい？ |
| 聴衆 | 誰が聞く？技術レベルは？何を事前に知っている？ |
| キーメッセージ | 聴衆が持ち帰るべき 2〜3 のポイントは？ |
| 背景・文脈 | 何がきっかけ？前回の提案を踏まえている？ |
| データ・根拠 | 具体的な数値やケーススタディはある？ |
| 制約 | プレゼン時間は？避けるべきトピックは？ |
| トーン | フォーマル／ビジョナリー？保守的／挑戦的？ |
| 成功基準 | どうなったら「成功」？ |

**終了条件**: エージェントが「十分な情報が集まった」と判断した時点で Phase 2 へ進む旨をユーザーに伝える。

---

### Phase 2: スキルロード + 構成提案（内部レビュー込み）

**目的**: ドメインスキルの知識をロードし、構成を提案、内部でレビュー済みのものをユーザーに提示する。

**動作**:
1. `load_skill` ツールで関連スキルの専門知識を取得（使用スキルをユーザーに報告）
2. 内部で構成案をドラフト
3. `review_structure` ツールで構成をレビュー（ユーザーには見せない）
4. レビューフィードバックを反映して構成を修正
5. **レビュー済みの最終構成のみをユーザーに提示**
6. **ユーザーの承認を 1 回だけ待つ**（修正要望があれば対応）

**設計判断**: 以前は構成提案→レビュー→修正版提示で 2 回確認が必要だったが、ユーザー負担軽減のため 1 回に統合。

---

### Phase 3: スライド生成

**目的**: レビュー済みの構成に基づき、MARP Markdown を生成する。

**動作**:
1. FUJISOFT テンプレート CSS を frontmatter に含めて生成
2. 各スライドにページクラス（cover / content / thankyou）を適用
3. 全コンテンツページにフッターを配置
4. 視覚デザイン要素（info-box, metric-grid, step-card 等）を適切に活用
5. 必要に応じて Mermaid ダイアグラムを `render_mermaid` で事前レンダリングし、`![](filename.png)` で埋め込む

---

### Phase 4: デザインレビュー（自動）

**目的**: 生成されたスライドを、スライドデザイン専門家の視点でレビューし、プロフェッショナル品質を保証する。

**実装**: `review_design` MCP ツール

**レビュー観点**:

| 観点 | チェック内容 |
|------|------------|
| 視覚デザイン | フォント・色彩・余白・ビジュアルヒエラルキー |
| CSS 品質 | box-shadow 不使用、border 代替、テンプレート準拠 |
| コンテンツ密度 | **高さ見積り制**: 各スライドの推定高さを計算し、520px 超過は分割必須 |
| はみ出し防止 | バレット最大 5 項目、テーブル最大 4 行、組み合わせルール適用 |
| フッタークリアランス | 底部 100px 確保 |
| 10 秒スキャンルール | 各スライドの要点が 10 秒で把握可能か |
| デザイン要素の活用 | info-box / metric-box / step-card 等の適切な使用 |
| ブランド一貫性 | カラーパレット・フォントがテンプレートに準拠 |
| 可読性 | 見出し 36pt+、本文 24pt+、コントラスト比 4.5:1 以上 |

**動作**:
1. 生成された MARP Markdown を `review_design` ツールに渡す
2. ツール内部で独立した `query()` を実行（デザインレビュアー用システムプロンプト）
3. スライドごとの品質スコア + 推定高さ + オーバーフローリスク + 改善指示を返却
4. エージェントがフィードバックを反映して Markdown を修正
5. 修正完了後、`convert_to_pdf` で PDF を生成（同時に `.md` ソースも保存）
6. ユーザーにダウンロードリンクを提供
7. フィードバック案内を表示（CLAUDE.md で義務化）

---

## Mermaid ダイアグラム対応

スライドに Mermaid ダイアグラム（Gantt チャート、フローチャート、シーケンス図、パイチャート等）を埋め込める。

### フロー

```
Mermaid コード → render_mermaid ツール → mmdc CLI → PNG ファイル → MARP に ![](file.png) で埋め込み
```

### 実装

- `converter/marp.py` の `render_mermaid_to_png()` が `mmdc` CLI を呼び出し
- 出力: `OUTPUT_DIR/{filename}.png`（1200x600px, 透明背景）
- 一時ファイルに `.mmd` を書き込み → `mmdc -i input.mmd -o output.png -w 1200 -H 600 -b transparent`

### 利用シーン

- Gantt チャート: プロジェクトタイムライン、実装スケジュール
- フローチャート: プロセスフロー、意思決定ツリー
- シーケンス図: システム間の連携フロー
- パイチャート: 予算配分、リソース割り当て

---

## MCP ツール一覧（7 ツール）

| ツール名 | 目的 | 入力 | 出力 |
|---------|------|------|------|
| `list_skills` | スキルカタログ参照 | なし | スキル一覧テキスト |
| `load_skill` | スキル知識の動的ロード | skill_name: str | スキル内容テキスト |
| `convert_to_pdf` | MARP → PDF 変換 | markdown_content, filename | PDF ファイルパス |
| `convert_to_html` | MARP → HTML 変換 | markdown_content, filename | HTML ファイルパス |
| `render_mermaid` | Mermaid → PNG 変換 | mermaid_code, filename | PNG ファイルパス |
| `review_structure` | 構成レビュー | structure, context | レビュー結果 |
| `review_design` | デザインレビュー | marp_markdown | レビュー結果 + スコア |

### review_structure ツール詳細

```python
@tool("review_structure", "...", {
    "structure": str,    # 提案されたスライド構成（アウトライン）
    "context": str       # ヒアリングで得た背景情報（目的・聴衆・メッセージ）
})
async def review_structure(args):
    # 独立した query() で構成レビュアーを実行
    # システムプロンプト: STRUCTURE_REVIEWER_PROMPT
    # 返却: { strengths, improvements, critical_issues, revised_structure }
```

### review_design ツール詳細

```python
@tool("review_design", "...", {
    "marp_markdown": str  # 生成された完全な MARP Markdown
})
async def review_design(args):
    # 独立した query() でデザインレビュアーを実行
    # checklist: presentation_best_practices_checklist.md を動的ロード
    # システムプロンプト: DESIGN_REVIEWER_PROMPT（高さ見積り + オーバーフローリスク判定）
    # 返却: { per_slide_scores, estimated_height, overflow_risk, critical_issues, overall_score }
```

### render_mermaid ツール詳細

```python
@tool("render_mermaid", "...", {
    "mermaid_code": str,  # Mermaid 記法のダイアグラムコード
    "filename": str       # 出力ファイル名（拡張子なし、デフォルト: "diagram"）
})
async def render_mermaid(args):
    # converter/marp.py の render_mermaid_to_png() を呼び出し
    # mmdc CLI で PNG にレンダリング
    # 返却: { filename, embed_instruction }
```

---

## エージェント行動ルール（CLAUDE.md）

`fsi-slide-studio/CLAUDE.md` にエージェントの行動ルールを集約し、SDK の `add_dirs` 経由で自動読み込みされる。

| ルール | 内容 |
|--------|------|
| 進捗報告 | 各フェーズ遷移時にユーザーへテキストで報告 |
| スキル使用報告 | `load_skill` 使用時にスキル名と理由を報告 |
| フィードバック案内 | PDF 納品後に修正オプションを案内 |
| バレット上限 | 1 スライド最大 5 項目（サブバレット最大 3 項目） |
| テーブル上限 | 最大 4 行×5 列、セル最大 30 文字 |
| 高さバジェット | 520px 超過は分割必須、450px 超過は要検討 |
| 組み合わせルール | テーブル+バレット、メトリクス+リスト等の制限 |

---

## チャットフロー例

```
User: 「来月の取締役会で使う、AI導入の提案プレゼンを作りたい」

─── Phase 1: ヒアリング ───

Agent: 「AI導入の提案ですね。いくつか確認させてください。
  1. この提案で最終的に何を承認してもらいたいですか？（予算承認？PoC開始？）
  2. 取締役会メンバーの技術リテラシーはどの程度ですか？
  3. 想定しているAI活用領域は具体的にありますか？
  4. プレゼン時間はどのくらいですか？」

User: 「年間$500KのAI予算承認が目的。技術にはあまり詳しくない。
  カスタマーサポートの自動化を考えている。持ち時間は20分。」

Agent: 「ありがとうございます。もう少し深掘りさせてください。
  1. 現在のカスタマーサポートの課題は？（応答時間、コスト、品質）
  2. 競合他社のAI導入状況は把握していますか？
  3. $500Kの内訳イメージはありますか？（ツール費、人件費、外注費）」

User: 「応答時間が平均24時間で遅い。競合は2社がチャットボット導入済み。
  内訳はまだこれから。」

─── Phase 2: スキルロード + 構成提案（内部レビュー済み） ───

Agent: 「十分な情報が集まりました。関連スキルを読み込んで構成案を作成します...」
Agent: [load_skill: ai-adoption-consultant] 「AI導入コンサルタントスキルを読み込みました」
Agent: [load_skill: financial-analyst] 「ROI分析のためにファイナンシャルアナリストスキルを読み込みました」
Agent: [review_structure: 構成案を内部レビュー（ユーザーには見せない）]

Agent: 「レビュー済みの構成です：
  1. 表紙
  2. エグゼクティブサマリー（$500K投資で応答時間90%短縮）
  3. 現状課題（応答時間・コスト・競合比較）
  4. AI活用提案（カスタマーサポート自動化）
  5. 導入ロードマップ（3フェーズ）
  6. ROI分析（投資回収シミュレーション）
  7. リスクと対策
  8. Next Steps
  9. Thank You
  この構成でよろしいですか？」

User: 「いいね。セキュリティの懸念も入れてほしい」

Agent: [load_skill: compliance-advisor] 「コンプライアンスアドバイザースキルを読み込みました」
Agent: 「承知しました。7番の後にセキュリティ・データプライバシーのスライドを追加します。」

─── Phase 3 & 4: 生成 + デザインレビュー ───

Agent: 「構成が確定しました。MARPスライドを生成します...」
Agent: [render_mermaid: 導入ロードマップの Gantt チャートをレンダリング]
Agent: [MARP Markdown 生成]
Agent: 「スライド生成完了。デザイン品質レビューを実行中...」
Agent: [review_design: デザインレビュー実行]
Agent: [レビューフィードバックを反映して修正]
Agent: [convert_to_pdf: PDF 生成]

Agent: 「PDF生成完了！品質レビュー結果のサマリーです:
  - 全スライド 80 点以上達成
  - オーバーフローリスクなし

  変更したい箇所はありますか？
  - コンテンツ: スライドの追加・削除・修正
  - デザイン: レイアウト・色・ビジュアル要素の変更
  - はみ出し修正: コンテンツが収まらないスライドの調整
  - トーン: よりフォーマル/カジュアル/テクニカルに」
```

---

## 主要な設計判断

| 判断事項 | 選択 | 理由 |
|---------|------|------|
| Agent SDK vs API 直接利用 | Agent SDK | Multi-turn、ツール統合、セッション管理が組み込み済み |
| スキルの読み込み方式 | On-demand (MCP ツール経由) + 自動検出 | 全スキルをプロンプトに含めるとトークン爆発。YAML カテゴリ定義 + ファイルシステム自動検出のハイブリッド方式。新スキル追加は `skills/` にフォルダを置くだけ |
| レビューの実装方式 | 独立した query() 呼び出し | 自己レビューよりも客観性が高い。別のシステムプロンプトで異なる視点を確保 |
| レビュー基準 | presentation_best_practices_checklist.md | 170+ 項目の実績あるチェックリスト |
| ヒアリングフェーズ | 必須（スキップ不可） | 初手の品質を大幅に向上させる最重要フェーズ |
| 構成確認回数 | 1 回（内部レビュー後に提示） | ユーザー負担軽減。内部でレビュー→修正→提示 |
| エージェント行動ルール | CLAUDE.md に集約 | コード変更なしでルール調整可能。`add_dirs` 経由で自動読み込み |
| はみ出し防止 | 高さバジェット制（520px） | DESIGN_REVIEWER_PROMPT + CLAUDE.md の両方でルールを適用 |
| モデル | Claude Sonnet 4.5 | コスト効率とスピード |
| PDF 変換 | marp-cli (subprocess) | 安定性・互換性実証済み |
| Mermaid 変換 | mmdc (subprocess) | mermaid-cli 公式。1200x600px, 透明背景 |
| Markdown ソース保存 | PDF 変換成功時に `.md` もリネーム保存 | ユーザーが後で編集・再利用可能 |
| デプロイ | Render (Docker) | Node.js + Chromium + Python を同梱 |
| AsyncBridge パターン | 永続イベントループ | SDK が内部で保持する anyio タスクグループがループに紐づくため、ループ使い捨ては不可。macOS の子プロセスウォッチャーもメインスレッド必須 |
| IME 入力対応 | document capture phase + justComposed timer | Safari は compositionend → keydown の順で発火（Chrome と逆）。`e.data` 空チェックで Safari の空 composition cycle を区別 |
| ストリーミング表示 | StreamEvent (token-level delta) + AssistantMessage fallback | UX 向上のためトークン単位で表示。StreamEvent 未対応時はブロック単位にフォールバック |
| デフォルト言語 | 日本語 (JP) | FUJISOFT America 社内ユーザーの主要言語 |

---

## 実装済みの変更

| ファイル | 実装済みの変更 |
|---------|--------------|
| `app.py` | IME composition fix (Safari 対応: document capture + justComposed timer + e.data チェック), AsyncBridge 統合, ストリーミング表示 (token-level delta + block-level fallback), ツール実行状況表示, カスタム CSS (チャット見出しサイズ縮小), PDF/Markdown ダウンロード, プレビューデフォルト展開, デフォルト言語 JP |
| `CLAUDE.md` | **新規ファイル**: 進捗報告、スキル使用報告、フィードバック案内、強化品質ルール（高さバジェット、組み合わせルール） |
| `agent/system_prompt.py` | 4フェーズワークフロー (Phase 2+3 統合), レビューツール使用指示, スライド品質ルール, Mermaid ダイアグラムガイド |
| `agent/tools.py` | `review_structure`, `review_design`, `convert_to_html`, `render_mermaid` ツール追加, `_load_checklist()` ヘルパー, DESIGN_REVIEWER_PROMPT に高さ見積り + オーバーフローリスク判定 |
| `agent/client.py` | `send_message_streaming()` async generator, StreamEvent 対応, 7ツール許可リスト, `add_dirs=[PROJECT_ROOT]` (CLAUDE.md 自動読込) |
| `agent/tool_activity.py` | **新規ファイル**: ツール完了ラベル定義, キャプション生成 (7ツール対応) |
| `agent/async_bridge.py` | **新規ファイル**: 永続イベントループ, `run()` / `shutdown()` / `is_alive`, Streamlit rerun 耐性 |
| `skills/catalog.py` | リファレンスファイル 3000-byte truncation, 自動検出機能（YAML 未登録スキルをディスクスキャンで "Other" に自動追加, SKILL.md フロントマターから description 抽出）, 合計 63 スキル利用可能 |
| `config/skill_categories.yaml` | 13カテゴリ, 44 curated スキル（Salesforce・Presentation カテゴリ追加） |
| `converter/marp.py` | `convert_marp_to_html()`, `render_mermaid_to_png()` 関数追加, PDF 変換成功時に `.md` ソース保存 |
| `config/settings.py` | `OUTPUT_DIR` / `LOG_DIR` の `mkdir(exist_ok=True)` 自動作成, `setup_logging()`, デフォルト言語 JP |
