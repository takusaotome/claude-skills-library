---
title: Mermaid Test
theme: navy
cover: false
---

# Architecture

```mermaid
graph TD
    A[Client] --> B[Server]
    B --> C[Database]
```

## Sequence

```mermaid
sequenceDiagram
    User->>Server: Request
    Server->>DB: Query
    DB-->>Server: Result
    Server-->>User: Response
```
