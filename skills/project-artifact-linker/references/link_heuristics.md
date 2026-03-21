# Link Heuristics

This document defines heuristics for establishing cross-reference links between project artifacts.

## Link Types

### 1. Action Item → WBS Task (`implements`)

An action item from a meeting implements or contributes to a WBS task.

**Matching Criteria:**

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Owner Match | 0.35 | Same person assigned to both |
| Keyword Overlap | 0.30 | Significant term overlap (>60% Jaccard) |
| Date Proximity | 0.20 | Action due date near task dates |
| Explicit Reference | 0.15 | Direct ID mention |

**Confidence Thresholds:**
- High (≥0.85): Owner match + keyword overlap
- Medium (0.60-0.84): Any two criteria met
- Low (0.40-0.59): Single criterion with strong signal
- Below 0.40: Do not create link

### 2. Decision → Requirement (`addresses`)

A decision addresses or clarifies a requirement.

**Matching Criteria:**

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Keyword Exact Match | 0.40 | Key technical terms match exactly |
| Domain Alignment | 0.25 | Same functional area (security, performance, etc.) |
| Temporal Proximity | 0.20 | Decision made after requirement created |
| Explicit Reference | 0.15 | Direct requirement ID mention |

**Domain Categories:**
- Security: authentication, authorization, encryption, access control
- Performance: latency, throughput, response time, scalability
- Usability: UI, UX, accessibility, user experience
- Integration: API, interface, connector, import/export
- Data: database, storage, migration, backup

### 3. Meeting → WBS Task (`discusses`)

A meeting discusses progress or issues related to a WBS task.

**Matching Criteria:**

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Task Owner Present | 0.30 | Task owner attended meeting |
| Task Mentioned | 0.35 | Task ID or name mentioned in minutes |
| Topic Alignment | 0.20 | Discussion topics align with task scope |
| Date Relevance | 0.15 | Meeting during task execution period |

### 4. Requirement → WBS Task (`implemented_by`)

A requirement is implemented by a WBS task.

**Matching Criteria:**

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Explicit Traceability | 0.45 | Direct reference in either document |
| Functional Alignment | 0.30 | Same functional module or feature |
| Owner Overlap | 0.15 | Same team or individual responsible |
| Timeline Fit | 0.10 | Task timeline supports requirement delivery |

## Keyword Extraction

### Technical Term Extraction

1. **Tokenization**: Split on whitespace and punctuation
2. **Stopword Removal**: Remove common English stopwords
3. **Domain Filtering**: Prioritize technical/domain terms
4. **N-gram Extraction**: Include bigrams for compound terms

### Domain-Specific Dictionaries

```yaml
security:
  - authentication
  - authorization
  - encryption
  - OAuth
  - SAML
  - JWT
  - access control
  - password
  - MFA
  - SSO

performance:
  - latency
  - throughput
  - response time
  - scalability
  - caching
  - load balancing
  - optimization
  - benchmark

data:
  - database
  - schema
  - migration
  - ETL
  - backup
  - restore
  - replication
  - indexing
```

## Similarity Calculations

### Jaccard Similarity

```python
def jaccard_similarity(set_a: set, set_b: set) -> float:
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0
```

### TF-IDF Weighted Similarity

```python
def tfidf_similarity(doc_a: str, doc_b: str, corpus: list) -> float:
    # Vectorize documents
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([doc_a, doc_b] + corpus)

    # Calculate cosine similarity
    return cosine_similarity(vectors[0], vectors[1])[0][0]
```

### Owner Match Scoring

```python
def owner_match_score(owner_a: str, owner_b: str) -> float:
    # Exact match
    if normalize_name(owner_a) == normalize_name(owner_b):
        return 1.0

    # Partial match (first name only, nickname)
    if partial_name_match(owner_a, owner_b):
        return 0.7

    # Team match
    if same_team(owner_a, owner_b):
        return 0.3

    return 0.0
```

## Temporal Proximity

### Date Distance Scoring

```python
def date_proximity_score(date_a: date, date_b: date, max_days: int = 30) -> float:
    delta = abs((date_a - date_b).days)
    if delta == 0:
        return 1.0
    if delta > max_days:
        return 0.0
    return 1.0 - (delta / max_days)
```

### Timeline Overlap

```python
def timeline_overlap_score(
    start_a: date, end_a: date,
    start_b: date, end_b: date
) -> float:
    # Calculate overlap period
    overlap_start = max(start_a, start_b)
    overlap_end = min(end_a, end_b)

    if overlap_start > overlap_end:
        return 0.0  # No overlap

    overlap_days = (overlap_end - overlap_start).days + 1
    total_days = (max(end_a, end_b) - min(start_a, start_b)).days + 1

    return overlap_days / total_days
```

## Conflict Resolution

When multiple potential links exist:

1. **Highest Confidence Wins**: Select link with highest confidence score
2. **Explicit Over Implicit**: Prefer links with explicit ID references
3. **Recent Over Historical**: When equal confidence, prefer more recent source
4. **Human Review Flag**: Mark ambiguous cases for manual verification

## Link Validation Rules

### Mandatory Checks

1. **Self-Reference Prevention**: Source and target must be different artifacts
2. **Type Compatibility**: Link types must connect compatible artifact types
3. **Temporal Consistency**: Effect cannot precede cause (decision → requirement)
4. **Existence Validation**: Both source and target must exist in artifact set

### Warning Checks

1. **Low Confidence Alert**: Flag links with confidence < 0.60
2. **Orphan Detection**: Warn on artifacts with no incoming or outgoing links
3. **Circular Reference**: Detect and warn on circular link chains
4. **Duplicate Detection**: Identify redundant links between same artifacts

## Confidence Calibration

### Confidence Score Interpretation

| Score Range | Interpretation | Recommended Action |
|-------------|----------------|-------------------|
| 0.90-1.00 | Very High | Auto-accept |
| 0.75-0.89 | High | Accept with spot-check |
| 0.60-0.74 | Medium | Review recommended |
| 0.40-0.59 | Low | Manual verification required |
| 0.00-0.39 | Very Low | Do not create link |

### Calibration Factors

Adjust confidence based on:
- **Corpus Size**: Larger corpora may have more false positives
- **Domain Specificity**: More specific domains have higher base confidence
- **Historical Accuracy**: Adjust based on past link accuracy feedback
