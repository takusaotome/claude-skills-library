---
layout: default
title: "DuckDB Expert"
grand_parent: English
parent: Software Development
nav_order: 17
lang_peer: /ja/skills/dev/duckdb-expert/
permalink: /en/skills/dev/duckdb-expert/
---

# DuckDB Expert
{: .no_toc }

DuckDBを使用した大規模データ分析の専門スキル。DuckDBのアーキテクチャ、SQL構文、パフォーマンス最適化、各種ファイル形式（CSV、Parquet、JSON等）の効率的な読み込み・書き出しを熟知。メモリ効率の良い分析、複雑なクエリの最適化、データパイプライン構築を支援。Use when analyzing large datasets, querying CSV/Parquet/JSON files directly, building data pipelines, or optimizing analytical queries with DuckDB.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/duckdb-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/duckdb-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

DuckDBは、OLAP（オンライン分析処理）に最適化された組み込み型の列指向データベースです。このスキルは、DuckDBを使用した効率的なデータ分析、大規模データセットの処理、パフォーマンス最適化を支援します。

---

## 2. Prerequisites

- **Python 3.8+** with `duckdb` package installed
- Optional: `pandas`, `polars`, `pyarrow` for DataFrame integration

```bash
# Install DuckDB (required)
pip install duckdb

# Optional: Install DataFrame libraries
pip install pandas polars pyarrow
```

---

## 3. Quick Start

```bash
1. Connect to DuckDB (in-memory or persistent)
2. Load/query data files directly (CSV, Parquet, JSON)
3. Transform and analyze using SQL
4. Export results (DataFrame, file, or database)
```

---

## 4. How It Works

<!-- TODO: Describe the internal pipeline/algorithm -->

---

## 5. Usage Examples

<!-- TODO: Add 4-6 real-world usage scenarios -->

---

## 6. Understanding the Output

<!-- TODO: Describe output file format and field definitions -->

---

## 7. Tips & Best Practices

<!-- TODO: Add expert advice for getting the most value -->

---

## 8. Combining with Other Skills

<!-- TODO: Add multi-skill workflow table -->

---

## 9. Troubleshooting

<!-- TODO: Add common errors and fixes -->

---

## 10. Reference

**References:**

- `skills/duckdb-expert/references/duckdb_functions_reference.md`
- `skills/duckdb-expert/references/file_formats_guide.md`
- `skills/duckdb-expert/references/performance_tuning_guide.md`

**Scripts:**

- `skills/duckdb-expert/scripts/duckdb_analyzer.py`
- `skills/duckdb-expert/scripts/etl_pipeline.py`
