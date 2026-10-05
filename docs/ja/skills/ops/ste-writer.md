---
layout: default
title: "STE Writer"
grand_parent: 日本語
parent: 運用・ドキュメント
nav_order: 18
lang_peer: /en/skills/ops/ste-writer/
permalink: /ja/skills/ops/ste-writer/
---

# STE Writer
{: .no_toc }

英文を ASD-STE100 Simplified Technical English の主要ルールに沿って、新しく書く、または書き換えるスキル。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>
<span class="badge badge-workflow">執筆・書き換え</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/ste-writer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/ste-writer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

ASD-STE100 Simplified Technical English、略して STE は、英語が少ししか分からない読み手でも、指示を誤読せずに実行できるようにするための書き方です。1語に1つの意味、1文に1つの内容、凝った言い回しをしない、が基本です。文章は平板になりますが、どの文も意味が1つに決まり、機械翻訳にもかけやすくなります。

使い方は2つあります。

- **書き換え**：既存の英文を渡すと、STE に書き換えます。
- **新規執筆**：事実、メモ、箇条書き、トピック、コードを渡すと、最初から STE で書きます。

{: .callout .warning }
このスキルは主要ルールを記憶に基づいて適用します。公式の ASD-STE100 仕様書や承認語辞書は同梱していません。そのため出力は「STE準拠」「認証済み」ではなく、「ASD-STE100 の主要ルールに沿って記述」と表現します。正式な準拠が必要な場合は、公式辞書やチェックツールで確認してください。仕様書や語彙リストを渡せば、スキル内のメモよりそちらを優先します。

---

## 2. 使う場面

- 英語が母語でない読み手向けの手順書、マニュアル、SOP、ランブック、リリースノート
- 機械翻訳にかける予定の英文
- 冗長、受け身が多い、意味が複数に取れる既存の英文ドキュメント
- 「STE」「simple technical English」「ASD-STE100」「80% STE」などの依頼

日本語の文書には [japanese-clear-writing]({{ '/ja/skills/ops/japanese-clear-writing/' | relative_url }}) を使ってください。

---

## 3. 前提条件

ありません。スクリプトや APIキーは不要で、指示だけで動くスキルです。

---

## 4. クイックスタート

既存の英文を書き換える例です。

```
docs/install.md を STE で書き換えて。
```

メモから新しい手順書を書く例です。

```
次のメモから STE の手順書を書いて。バッジプリンターのリセット手順。
ボタンを押し続けてランプを待つ。約1分かかる。最初に電源を抜く。
```

ゆるめのモードを使う例です。

```
このリリースノートを 80% STE で書き換えて。技術用語はそのまま残して。
```

説明は依頼と同じ言語で返します。文書そのものは常に英語です。

---

## 5. 厳しさの段階

| モード | 内容 |
|:-------|:-----|
| **full**（既定） | 14の主要ルールをすべて適用する |
| **soft** | ルール1〜6を適用し、作者の技術用語と自然なリズムを残す。25語程度までの文を一部許す。「80%」「軽めに」「トーンを残して」と頼まれたときに使う |

どちらのモードを使ったかは、出力に必ず書きます。

---

## 6. 主要ルール

1. 1文に1つの指示。手順の文は20語以内、説明の文は25語以内
2. 動作は命令形で書く。例：「Remove the cover.」
3. 能動態を使う
4. 時制は単純現在、単純過去、未来だけを使う
5. 1つの意味には1つの語。言い換えで変化をつけない
6. 簡単でよく使われる語を選ぶ。「utilize」ではなく「use」
7. 冠詞などの短い語を省かない。電報文にしない
8. 名詞を続けるのは3つまで
9. 句動詞や慣用句は、意味がはっきりした1語の動詞に置き換える
10. 短縮形と、指す先が曖昧な代名詞を避ける
11. 段落は1トピック、6文以内
12. 警告と注意は、対象の手順の前に置く。人への危険は「WARNING」、機器やデータへの危険は「CAUTION」
13. 必須は「must」、能力は「can」、許可は「may」
14. 数字は算用数字で書き、単位を添える

書き換えの例です。

| 書き換え前 | 書き換え後 |
|:-----------|:-----------|
| Before the unit is powered on, it should be ensured that all of the connectors have been properly seated, otherwise damage could occur. | CAUTION: Make sure that all connectors are fully connected before you start the unit. If a connector is loose, the unit can be damaged. |

---

## 7. 出力

次の順で出します。

1. **文書**：使う場所に合った形式で出します。ファイルを書き換える場合は、元のファイルの隣に新しいファイルを作り、元は上書きしません。
2. **変更点または用語**：書き換えでは、主な変更の種類を3〜6個、前後の例付きで示します。新規執筆では、選んだ用語の一覧を示します。後の文書でも同じ用語を使えるようにするためです。
3. **作者への質問**：`[CHECK: ...]` の箇所ごとに1つ出します。トルク値、時間、コマンドなど足りない値は、推測せずにこの印を付けます。
4. **モードの明記**：使ったモードと、公式認証ではない旨を1行で書きます。

---

## 8. リソース

- `SKILL.md`：ルール、語の置き換え表、手順、出力形式、例
