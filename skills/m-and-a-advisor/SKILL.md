---
name: m-and-a-advisor
description: |
  M&Aアドバイザリー支援スキル。デューデリジェンス（DD）実施、企業価値評価（バリュエーション）、
  シナジー分析、PMI（Post Merger Integration）計画策定を包括的に支援。
  Use when conducting M&A due diligence (Financial, Legal, IT, HR), company valuation
  (DCF, Comparable Companies, Precedent Transactions), synergy analysis, or post-merger
  integration planning.
  Triggers: "M&A", "デューデリジェンス", "DD", "バリュエーション", "企業価値評価", "DCF",
  "comparable", "類似企業", "先行取引", "PMI", "統合計画", "シナジー分析", "買収", "合併"
---

# M&A Advisor

## Overview

M&Aアドバイザリー業務を包括的に支援するスキル。デューデリジェンス（DD）の実施から企業価値評価、シナジー分析、PMI計画策定まで、M&Aプロセス全体をカバー。

**主要機能:**
1. **デューデリジェンス（DD）** - 財務/法務/IT/HR の4領域 + 業種別DD
2. **バリュエーション** - DCF/類似企業比較/先行取引分析の3手法
3. **シナジー分析** - コスト/収益シナジーの定量化
4. **PMI計画** - 統合計画の策定と実行支援

## When to Use This Skill

| シナリオ | 対応ワークフロー |
|---------|-----------------|
| 買収対象企業の調査・評価 | DD実施ワークフロー |
| 企業価値算定・株価算定 | バリュエーションワークフロー |
| 買収効果の定量化 | シナジー分析ワークフロー |
| 買収後の統合計画 | PMI計画ワークフロー |

---

## Workflow 1: デューデリジェンス（DD）実施

### Step 1.1: DDスコープ定義

**対象領域の特定:**
```
□ 財務DD (Financial Due Diligence)
□ 法務DD (Legal Due Diligence)
□ IT DD (IT/Technology Due Diligence)
□ 人事DD (HR Due Diligence)
□ 業種別DD (Industry-Specific DD)
```

**業種別DD選択:**
- IT・ソフトウェア業 → `references/dd-industry/it_software_dd.md`
- 製造業 → `references/dd-industry/manufacturing_dd.md`
- 金融・保険業 → `references/dd-industry/financial_services_dd.md`
- 小売・消費財 → `references/dd-industry/retail_consumer_dd.md`

### Step 1.2: 各領域のDD実施

**財務DD** (`references/dd-checklists/financial_dd_checklist.md`):
1. 財務諸表分析（過去3-5年）
2. 収益性・成長性分析
3. 運転資本・キャッシュフロー分析
4. 税務リスク評価
5. オフバランス項目確認
6. 会計方針の検証

**法務DD** (`references/dd-checklists/legal_dd_checklist.md`):
1. 会社組織・株主構成
2. 契約関係（重要契約、COC条項）
3. 知的財産権
4. 訴訟・紛争リスク
5. 許認可・コンプライアンス

**IT DD** (`references/dd-checklists/it_dd_checklist.md`):
1. システム資産棚卸
2. インフラ評価
3. セキュリティ評価
4. 統合難易度評価
5. 技術負債評価

**人事DD** (`references/dd-checklists/hr_dd_checklist.md`):
1. 組織構造・人員分析
2. 報酬・福利厚生制度
3. キーパーソンリスク
4. 退職給付債務

### Step 1.3: リスク評価・レポート作成

**リスク評価マトリックス:**
| リスクレベル | 基準 | アクション |
|-------------|------|-----------|
| 🔴 高 | ディールブレイカー or 重大な価格調整要因 | 即時対応・交渉必須 |
| 🟡 中 | 対応可能だが要モニタリング | 契約条件で対応 |
| 🟢 低 | 許容範囲内 | 通常モニタリング |

**出力:** `assets/dd_report_template_ja.md` または `assets/dd_report_template_en.md`

---

## Workflow 2: バリュエーション（企業価値評価）

### Step 2.1: 評価手法の選択

**3つの主要アプローチ:**

| 手法 | 適用場面 | 参照ファイル |
|-----|---------|-------------|
| DCF法 | 将来CFが予測可能な事業会社 | `references/valuation/dcf_methodology.md` |
| 類似企業比較法 | 上場類似企業が存在する場合 | `references/valuation/comparable_analysis.md` |
| 先行取引分析法 | 類似M&A取引が存在する場合 | `references/valuation/precedent_transactions.md` |

### Step 2.2: DCF法による評価

**基本フレームワーク:**
1. **事業計画の検証** - 過去実績との整合性確認
2. **FCF（フリーキャッシュフロー）予測** - 5-10年の予測期間
3. **WACC計算** - 加重平均資本コスト
4. **継続価値（Terminal Value）算定** - 永久成長率モデル or Exit Multiple
5. **感度分析** - WACC/成長率の変動による価値レンジ

**WACC計算式:**
```
WACC = E/(D+E) × Re + D/(D+E) × Rd × (1-T)

Re = Rf + β × (Rm - Rf) + サイズプレミアム + 国別リスクプレミアム
```

**Pythonスクリプト活用:** `scripts/valuation_calculator.py`

### Step 2.3: 類似企業比較法

**主要マルチプル:**
- EV/EBITDA - 最も一般的、業種間比較に有効
- EV/Sales - 赤字企業、成長企業向け
- P/E - 成熟企業、安定収益企業向け
- PBR - 金融機関、資産集約型事業向け

**調整要因:**
- 流動性ディスカウント（非上場企業: 15-30%）
- コントロールプレミアム（支配権取得: 20-40%）
- サイズディスカウント（小規模企業調整）

### Step 2.4: 先行取引分析法

**取引選定基準:**
- 業種・事業モデルの類似性
- 取引規模の類似性
- 取引時期（直近3-5年が望ましい）
- 地域・市場環境の類似性

**分析ポイント:**
- 公表マルチプルからのシナジー除去
- コントロールプレミアムの分離
- 市場環境の調整

### Step 2.5: 評価結論（フットボールチャート）

**出力:** `assets/valuation_summary_template_ja.md` または `assets/valuation_summary_template_en.md`

```
評価手法別株式価値レンジ
                    [--------|--------]  DCF法
              [--------|--------]        類似企業比較法
                  [--------|--------]    先行取引分析法
              |----|----|----|----|----|
              80   90  100  110  120 (億円)
                        ↑
                    推定株式価値
```

---

## Workflow 3: シナジー分析

### Step 3.1: シナジー類型の特定

**参照:** `references/synergy_analysis_guide.md`

| シナジー類型 | 内容 | 実現難易度 | 実現期間 |
|-------------|------|----------|---------|
| コストシナジー | 重複コスト削減、規模の経済 | 中 | 1-3年 |
| 収益シナジー | クロスセル、新市場アクセス | 高 | 2-5年 |
| 財務シナジー | 資金調達コスト低減、税効果 | 低 | 即時-1年 |

### Step 3.2: シナジーの定量化

**コストシナジー項目例:**
- 本社機能統合（経理、人事、IT）
- 調達コスト削減（スケールメリット）
- 拠点統合・不動産コスト削減
- システム統合・IT費用削減

**収益シナジー項目例:**
- 顧客基盤へのクロスセル
- 販売チャネルの相互活用
- 新製品開発の加速
- 地理的市場拡大

### Step 3.3: 実現確度評価

**評価マトリックス:**
| 確度 | 基準 | NPV計算への反映 |
|-----|------|----------------|
| 高（80%+） | 実績あり、定量化済み | 100%計上 |
| 中（50-80%） | 計画策定済み、実行可能 | 70%計上 |
| 低（30-50%） | コンセプト段階 | 40%計上 |
| 要検証（30%未満） | 仮説段階 | 計上せず |

### Step 3.4: シナジーモデル作成

**出力:** `assets/synergy_model_template_ja.md` または `assets/synergy_model_template_en.md`

---

## Workflow 4: PMI（Post Merger Integration）計画

### Step 4.1: PMIフレームワーク

**参照:** `references/pmi_framework.md`

**3つのフェーズ:**
```
[Day 1準備] → [100日計画] → [長期統合]
  (D-90~D0)    (D+1~D+100)   (D+100~)
```

### Step 4.2: Day 1準備（クロージング前）

**必須タスク:**
- 統合推進体制（IMO: Integration Management Office）設置
- Day 1 コミュニケーション計画
- 法的・規制対応（独禁法承認等）
- 重要顧客・取引先への連絡計画
- 従業員リテンション施策

### Step 4.3: 100日計画

**機能別統合計画:**

| 機能領域 | 主要タスク | 優先度 |
|---------|----------|-------|
| 経営・ガバナンス | 意思決定プロセス統一、取締役会構成 | 最優先 |
| 財務・経理 | 会計システム統合、報告体制 | 高 |
| 人事 | 報酬制度調整、組織再編 | 高 |
| IT | システム統合計画、インフラ整理 | 中 |
| 営業・マーケ | ブランド戦略、販売体制 | 中 |
| オペレーション | サプライチェーン、製造拠点 | 後続 |

### Step 4.4: KPI設定・モニタリング

**統合成功指標:**
- シナジー実現率（計画対比）
- 従業員離職率（特にキーパーソン）
- 顧客維持率
- 統合コスト（計画対比）
- 事業業績（売上・利益）

### Step 4.5: PMI計画書作成

**出力:** `assets/pmi_plan_template_ja.md` または `assets/pmi_plan_template_en.md`

---

## Resources

### references/

**DDチェックリスト（汎用）:**
- `dd-checklists/financial_dd_checklist.md` - 財務DD項目
- `dd-checklists/legal_dd_checklist.md` - 法務DD項目
- `dd-checklists/it_dd_checklist.md` - IT DD項目
- `dd-checklists/hr_dd_checklist.md` - 人事DD項目

**業種別DDチェックリスト:**
- `dd-industry/it_software_dd.md` - IT・ソフトウェア業
- `dd-industry/manufacturing_dd.md` - 製造業
- `dd-industry/financial_services_dd.md` - 金融・保険業
- `dd-industry/retail_consumer_dd.md` - 小売・消費財

**バリュエーション手法:**
- `valuation/dcf_methodology.md` - DCF法詳細
- `valuation/comparable_analysis.md` - 類似企業比較法
- `valuation/precedent_transactions.md` - 先行取引分析法

**その他ガイド:**
- `synergy_analysis_guide.md` - シナジー分析ガイド
- `pmi_framework.md` - PMI計画フレームワーク

### assets/

**テンプレート（日本語）:**
- `dd_report_template_ja.md` - DDレポートテンプレート
- `valuation_summary_template_ja.md` - バリュエーションサマリー
- `synergy_model_template_ja.md` - シナジーモデルテンプレート
- `pmi_plan_template_ja.md` - PMI計画テンプレート

**テンプレート（English）:**
- `dd_report_template_en.md` - DD Report Template
- `valuation_summary_template_en.md` - Valuation Summary Template
- `synergy_model_template_en.md` - Synergy Model Template
- `pmi_plan_template_en.md` - PMI Plan Template

### scripts/

- `valuation_calculator.py` - DCF計算、WACC計算、感度分析ツール
