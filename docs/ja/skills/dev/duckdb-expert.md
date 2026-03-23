---
layout: default
title: "DuckDB Expert"
grand_parent: 日本語
parent: ソフトウェア開発
nav_order: 17
lang_peer: /en/skills/dev/duckdb-expert/
permalink: /ja/skills/dev/duckdb-expert/
---

# DuckDB Expert
{: .no_toc }

DuckDBを使用した大規模データ分析の専門スキル。DuckDBのアーキテクチャ、SQL構文、パフォーマンス最適化、各種ファイル形式（CSV、Parquet、JSON等）の効率的な読み込み・書き出しを熟知。メモリ効率の良い分析、複雑なクエリの最適化、データパイプライン構築を支援。Use when analyzing large datasets, querying CSV/Parquet/JSON files directly, building data pipelines, or optimizing analytical queries with DuckDB.
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/duckdb-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/duckdb-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

DuckDBは、OLAP（オンライン分析処理）に最適化された組み込み型の列指向データベースです。このスキルは、DuckDBを使用した効率的なデータ分析、大規模データセットの処理、パフォーマンス最適化を支援します。

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- **Python 3.8+** with `duckdb` package installed
- Optional: `pandas`, `polars`, `pyarrow` for DataFrame integration

```bash
# Install DuckDB (required)
pip install duckdb

# Optional: Install DataFrame libraries
pip install pandas polars pyarrow
```

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

```bash
1. Connect to DuckDB (in-memory or persistent)
2. Load/query data files directly (CSV, Parquet, JSON)
3. Transform and analyze using SQL
4. Export results (DataFrame, file, or database)
```

<!-- TODO: 翻訳 -->

---

## 4. 仕組み

<!-- TODO: 翻訳 -->

---

## 5. 使用例

<!-- TODO: 翻訳 -->

---

## 6. 出力の読み方

<!-- TODO: 翻訳 -->

---

## 7. Tips & ベストプラクティス

<!-- TODO: 翻訳 -->

---

## 8. 他スキルとの連携

<!-- TODO: 翻訳 -->

---

## 9. トラブルシューティング

<!-- TODO: 翻訳 -->

---

## 10. リファレンス

**References:**

- `skills/duckdb-expert/references/duckdb_functions_reference.md`
- `skills/duckdb-expert/references/file_formats_guide.md`
- `skills/duckdb-expert/references/performance_tuning_guide.md`

**Scripts:**

- `skills/duckdb-expert/scripts/duckdb_analyzer.py`
- `skills/duckdb-expert/scripts/etl_pipeline.py`
