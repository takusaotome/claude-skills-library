# FSI Slide Studio - 設計書

## Context

FUJISOFT America 社内の誰もが、チャットで話しかけるだけでプロフェッショナルなプレゼンテーションを自動生成できる Web アプリ。既存の `fujisoft-presentation-creator` スキルのテンプレートと品質基準を活用し、30+ ドメイン専門スキルの知識を動的にロードしてスライド内容の質を高める。

## アーキテクチャ概要

```
┌─────────────────────────────────────────────┐
│  Streamlit Frontend (Chat UI)               │
│  - st.chat_input / st.chat_message          │
│  - IME composition fix (JS injection)       │
│  - Streaming: token-level deltas            │
│  - Slide preview (HTML iframe)              │
│  - PDF download button                      │
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
│  - Custom MCP tools:                        │
│    - list_skills: 利用可能スキル一覧        │
│    - load_skill: スキル知識の動的ロード     │
│    - convert_to_pdf: MARP→PDF 変換          │
│    - convert_to_html: MARP→HTML 変換        │
│    - review_structure: 構成レビュー         │
│    - review_design: デザインレビュー        │
└──────────────┬──────────────────────────────┘
               │ Reads on-demand
               ▼
┌─────────────────────────────────────────────┐
│  Skill Library (knowledge base)             │
│  - 30+ domain skills (SKILL.md + refs)      │
│  - fujisoft-presentation-creator template   │
│  - presentation_best_practices_checklist.md │
│  - Categorized: Strategy/Finance/Ops/...    │
└─────────────────────────────────────────────┘
```

## 技術スタック

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend | Streamlit | >= 1.42 | Chat UI, file download, preview |
| Agent | claude-agent-sdk (Python) | latest | Multi-turn AI conversation |
| Template | MARP (marp-cli) | 4.2.x | Markdown → PDF/HTML 変換 |
| Language | Python | >= 3.11 | Backend logic |
| Model | Claude Sonnet 4.5 | latest | コスト効率とスピードのバランス |

## プロジェクト構造

```
fsi-slide-studio/
├── app.py                    # Streamlit メインアプリ (IME fix, AsyncBridge, streaming)
├── agent/
│   ├── __init__.py
│   ├── async_bridge.py       # 永続イベントループ (Streamlit↔SDK ブリッジ)
│   ├── client.py             # Claude Agent SDK クライアント管理 (streaming 対応)
│   ├── system_prompt.py      # システムプロンプト構築 (5フェーズワークフロー)
│   └── tools.py              # カスタム MCP ツール定義 (6ツール)
├── skills/
│   ├── __init__.py
│   ├── router.py             # スキルルーティング
│   └── catalog.py            # スキルカタログ (3000-byte truncation)
├── converter/
│   ├── __init__.py
│   └── marp.py               # MARP CLI ラッパー (PDF + HTML 変換)
├── config/
│   ├── settings.py           # アプリ設定 (OUTPUT_DIR/LOG_DIR 自動作成, setup_logging)
│   └── skill_categories.yaml # スキルカテゴリマッピング
├── tests/                    # ユニットテスト
│   ├── conftest.py           # SDK モック注入 + 共通 fixtures
│   ├── unit/                 # ユニットテスト (76 テスト)
│   └── fixtures/             # テスト用データ
├── output/                   # 生成物の一時保存
├── logs/                     # アプリケーションログ
├── Dockerfile
├── render.yaml
├── requirements.txt
├── pyproject.toml            # pytest 設定
├── .env.example
└── DESIGN.md                 # この設計書
```

---

## ワークフロー設計（5 フェーズ）

### 全体フロー図

```
User ──→ Phase 1: ヒアリング ──→ Phase 2: 構成提案 ──→ Phase 3: 構成レビュー
                 ↑ 質問ループ          │                    │
                 └─────────┘          ▼                    ▼ フィードバック
                                  User 承認 ←──── 修正指示 ──┘
                                      │
                                      ▼
                               Phase 4: スライド生成 ──→ Phase 5: デザインレビュー
                                                             │
                                                             ▼ フィードバック
                                                        自動修正 → PDF 出力
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

### Phase 2: 構成提案 + スキルロード

**目的**: トピックに関連するドメインスキルの知識をロードし、スライド構成を提案する。

**動作**:
1. `load_skill` ツールで関連スキルの専門知識を取得
2. Guy Kawasaki 10-20-30 ルールに基づく構成を提案
3. 各スライドのタイトル + 主要ポイントを提示
4. **ユーザーの承認を待つ**（修正要望があれば対応）

---

### Phase 3: 構成レビュー（自動）

**目的**: 提案した構成を、プレゼンテーション専門家の視点で客観的にレビューし、品質を担保する。

**実装**: `review_structure` MCP ツール

**レビュー観点**:

| 観点 | チェック内容 |
|------|------------|
| ストーリーフロー | 導入→課題→解決策→効果→行動促進の論理展開 |
| 聴衆適合性 | Phase 1 で特定した聴衆のレベル・関心に合っているか |
| メッセージ整合性 | キーメッセージが構成全体で一貫しているか |
| 情報密度 | 各スライドが 1 メッセージ原則を守っているか |
| 抜け漏れ | 聴衆が当然期待する内容が欠けていないか |
| スライド枚数 | 発表時間に対して適切か |

**動作**:
1. エージェントが構成案を `review_structure` ツールに渡す
2. ツール内部で独立した `query()` を実行（レビュアー用システムプロンプト）
3. レビュー結果（Good / Improvement / Critical）を返却
4. エージェントがフィードバックを反映して構成を修正
5. 修正後の構成をユーザーに提示

**レビュアーのシステムプロンプト要件**:
- `presentation_best_practices_checklist.md` の「事前準備・設計段階」「構成・ストーリー設計」セクションを基準にする
- Phase 1 のヒアリング結果（目的・聴衆・キーメッセージ）を考慮する
- 具体的な改善提案を出す（「足りない」ではなく「〇〇を追加すべき」）

---

### Phase 4: スライド生成

**目的**: レビュー済みの構成に基づき、MARP Markdown を生成する。

**動作**:
1. FUJISOFT テンプレート CSS を frontmatter に含めて生成
2. 各スライドにページクラス（cover / content / thankyou）を適用
3. 全コンテンツページにフッターを配置
4. 視覚デザイン要素（info-box, metric-grid, step-card 等）を適切に活用

---

### Phase 5: デザインレビュー（自動）

**目的**: 生成されたスライドを、スライドデザイン専門家の視点でレビューし、プロフェッショナル品質を保証する。

**実装**: `review_design` MCP ツール

**レビュー観点**:

| 観点 | チェック内容 |
|------|------------|
| 視覚デザイン | フォント・色彩・余白・ビジュアルヒエラルキー |
| CSS 品質 | box-shadow 不使用、border 代替、テンプレート準拠 |
| コンテンツ密度 | テーブル 5 行以下、リスト 8 項目以下 |
| フッタークリアランス | 底部 100px 確保 |
| 10 秒スキャンルール | 各スライドの要点が 10 秒で把握可能か |
| デザイン要素の活用 | info-box / metric-box / step-card 等の適切な使用 |
| ブランド一貫性 | カラーパレット・フォントがテンプレートに準拠 |
| 可読性 | 見出し 36pt+、本文 24pt+、コントラスト比 4.5:1 以上 |

**動作**:
1. 生成された MARP Markdown を `review_design` ツールに渡す
2. ツール内部で独立した `query()` を実行（デザインレビュアー用システムプロンプト）
3. スライドごとの品質スコア + 具体的改善指示を返却
4. エージェントがフィードバックを反映して Markdown を修正
5. 修正完了後、`convert_to_pdf` で PDF を生成
6. ユーザーにダウンロードリンクを提供

**レビュアーのシステムプロンプト要件**:
- `presentation_best_practices_checklist.md` 全セクションを基準にする
- FUJISOFT テンプレートの CSS クラス一覧を把握した上で評価する
- 各スライドに 0〜100 のスコアをつけ、80 未満のスライドは修正必須とする
- 修正指示は具体的な CSS クラス名やマークダウン記法で出す

---

## MCP ツール一覧（6 ツール）

| ツール名 | 目的 | 入力 | 出力 |
|---------|------|------|------|
| `list_skills` | スキルカタログ参照 | なし | スキル一覧テキスト |
| `load_skill` | スキル知識の動的ロード | skill_name: str | スキル内容テキスト |
| `convert_to_pdf` | MARP → PDF 変換 | markdown_content, filename | PDF ファイルパス |
| `convert_to_html` | MARP → HTML 変換 | markdown_content, filename | HTML ファイルパス |
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
    # システムプロンプト: presentation_best_practices_checklist.md の構成セクション
    # 返却: { strengths, improvements, critical_issues }
```

### review_design ツール詳細

```python
@tool("review_design", "...", {
    "marp_markdown": str  # 生成された完全な MARP Markdown
})
async def review_design(args):
    # 独立した query() で デザインレビュアーを実行
    # システムプロンプト: presentation_best_practices_checklist.md 全体 + テンプレート仕様
    # 返却: { per_slide_scores, critical_issues, improvements, overall_score }
```

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

Agent: 「十分に理解できました。構成を提案します。」

─── Phase 2 & 3: 構成提案 + レビュー ───

Agent: [load_skill: ai-adoption-consultant, financial-analyst]
Agent: [review_structure: 構成案を内部レビュー]
Agent: 「レビューを反映した構成です：
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

Agent: [load_skill: compliance-advisor]
Agent: 「承知しました。7番の後にセキュリティ・データプライバシーのスライドを追加します。」

─── Phase 4 & 5: 生成 + デザインレビュー ───

Agent: [MARP Markdown 生成]
Agent: [review_design: デザインレビュー実行]
Agent: [レビューフィードバックを反映して修正]
Agent: [convert_to_pdf: PDF 生成]
Agent: 「プレゼンテーションが完成しました。PDFをダウンロードできます。
  デザインレビューの結果、全スライド80点以上を達成しています。」
```

---

## 主要な設計判断

| 判断事項 | 選択 | 理由 |
|---------|------|------|
| Agent SDK vs API 直接利用 | Agent SDK | Multi-turn、ツール統合、セッション管理が組み込み済み |
| スキルの読み込み方式 | On-demand (MCP ツール経由) | 全スキルをプロンプトに含めるとトークン爆発 |
| レビューの実装方式 | 独立した query() 呼び出し | 自己レビューよりも客観性が高い。別のシステムプロンプトで異なる視点を確保 |
| レビュー基準 | presentation_best_practices_checklist.md | 170+ 項目の実績あるチェックリスト |
| ヒアリングフェーズ | 必須（スキップ不可） | 初手の品質を大幅に向上させる最重要フェーズ |
| モデル | Claude Sonnet 4.5 | コスト効率とスピード |
| PDF 変換 | marp-cli (subprocess) | 安定性・互換性実証済み |
| デプロイ | Render (Docker) | Node.js + Chromium + Python を同梱 |
| AsyncBridge パターン | 永続イベントループ (`new_event_loop` + `run_until_complete`) | SDK が内部で保持する anyio タスクグループがループに紐づくため、ループ使い捨ては不可。macOS の子プロセスウォッチャーもメインスレッド必須 |
| IME 入力対応 | JavaScript injection (`compositionstart`/`end`) | Streamlit の `chat_input` は IME 変換中の Enter でも送信してしまうため、JS レイヤーで抑制 |
| ストリーミング表示 | StreamEvent (token-level delta) + AssistantMessage fallback | UX 向上のためトークン単位で表示。StreamEvent 未対応時はブロック単位にフォールバック |
| レビュー実装場所 | MCP ツール内の独立 `query()` | エージェントのコンテキストを汚染せず、別のシステムプロンプトで客観的レビューを実現 |

---

## 実装済みの変更

| ファイル | 実装済みの変更 |
|---------|--------------|
| `app.py` | IME composition fix (JS injection), AsyncBridge 統合, ストリーミング表示 (token-level delta + block-level fallback), ツール実行状況表示 |
| `agent/system_prompt.py` | 5フェーズワークフロー, レビューツール使用指示, スライド品質ルール |
| `agent/tools.py` | `review_structure`, `review_design` ツール追加, `convert_to_html` ツール追加, `_load_checklist()` ヘルパー |
| `agent/client.py` | `send_message_streaming()` async generator 追加, StreamEvent 対応, 6ツール許可リスト |
| `agent/async_bridge.py` | **新規ファイル**: 永続イベントループ, `run()` / `shutdown()` / `is_alive`, Streamlit rerun 耐性 |
| `skills/catalog.py` | リファレンスファイル 3000-byte truncation 追加 |
| `converter/marp.py` | `convert_marp_to_html()` 関数追加 |
| `config/settings.py` | `OUTPUT_DIR` / `LOG_DIR` の `mkdir(exist_ok=True)` 自動作成, `setup_logging()` 関数追加 |
