# Mermaid Diagram Patterns

This reference provides comprehensive Mermaid syntax patterns for technical specification documents. Each section includes syntax rules, practical examples, best practices, and common mistakes to avoid.

## 1. Sequence Diagram (sequenceDiagram)

### Basic Syntax

```
sequenceDiagram
    participant A as Actor
    participant F as Frontend
    participant B as Backend
    participant D as Database

    A->>F: Action description
    F->>B: Request description
    B->>D: Query description
    D-->>B: Result description
    B-->>F: Response description
    F-->>A: Display result
```

### Arrow Types

| Arrow | Meaning | Usage |
|-------|---------|-------|
| `->>` | Solid line with arrowhead | Synchronous request |
| `-->>` | Dashed line with arrowhead | Response / return |
| `-x` | Solid line with cross | Failed / rejected message |
| `--x` | Dashed line with cross | Failed response |
| `-)` | Solid line with open arrow | Asynchronous message |
| `--)` | Dashed line with open arrow | Asynchronous response |

### Conditional Branches (alt/opt/loop)

```
sequenceDiagram
    participant U as User
    participant S as Server
    participant DB as Database

    U->>S: POST /api/v1/login
    S->>DB: SELECT user WHERE email = ?

    alt User found and password matches
        DB-->>S: User record
        S->>S: Generate JWT token
        S-->>U: 200 OK { token: "..." }
    else User not found
        DB-->>S: Empty result
        S-->>U: 401 Unauthorized { error: "Invalid credentials" }
    else Password mismatch
        DB-->>S: User record
        S->>S: Increment failed_attempts
        S-->>U: 401 Unauthorized { error: "Invalid credentials" }
    end
```

### Optional Block (opt)

```
sequenceDiagram
    participant U as User
    participant S as Server
    participant C as Cache

    U->>S: GET /api/v1/products/123
    opt Cache hit
        S->>C: GET product:123
        C-->>S: Cached data
        S-->>U: 200 OK (from cache)
    end
    S->>DB: SELECT * FROM products WHERE id = 123
    DB-->>S: Product record
    S-->>U: 200 OK
```

### Loop Block

```
sequenceDiagram
    participant Scheduler as Batch Scheduler
    participant Worker as Worker Process
    participant DB as Database

    Scheduler->>DB: SELECT pending jobs (LIMIT 100)
    DB-->>Scheduler: Job list

    loop For each job in batch
        Scheduler->>Worker: Process job
        Worker->>DB: UPDATE job SET status = 'processing'
        Worker->>Worker: Execute job logic
        Worker->>DB: UPDATE job SET status = 'completed'
        Worker-->>Scheduler: Job result
    end
```

### Parallel Execution (par)

```
sequenceDiagram
    participant U as User
    participant API as API Gateway
    participant UserSvc as User Service
    participant OrderSvc as Order Service
    participant NotifSvc as Notification Service

    U->>API: GET /api/v1/dashboard

    par Fetch user profile
        API->>UserSvc: GET /users/123
        UserSvc-->>API: User profile
    and Fetch recent orders
        API->>OrderSvc: GET /orders?user=123&limit=5
        OrderSvc-->>API: Order list
    and Fetch notifications
        API->>NotifSvc: GET /notifications?user=123&unread=true
        NotifSvc-->>API: Notification list
    end

    API-->>U: 200 OK { profile, orders, notifications }
```

### Notes and Activation

```
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend

    Note over U,F: User initiates the flow
    U->>F: Click "Submit Order"
    activate F
    F->>F: Validate form fields
    Note right of F: Client-side validation
    F->>B: POST /api/v1/orders
    activate B
    B->>B: Business rule validation
    B-->>F: 201 Created
    deactivate B
    F-->>U: Display confirmation
    deactivate F
```

### Best Practices

1. **Limit participants to 6 or fewer** — More than 6 makes diagrams hard to read
2. **Use aliases** — `participant DB as Database` is more readable than long names
3. **Group related messages** — Use `rect` blocks to highlight transaction boundaries
4. **Show error paths** — Always include `alt` blocks for error handling
5. **Keep descriptions concise** — Use "Validate input" not "Validate the user input data fields"

### Common Mistakes

- Missing `end` keyword after `alt`, `opt`, `loop`, or `par` blocks
- Using `->` (single arrow) instead of `->>` (double arrow) — single arrow has no arrowhead
- Forgetting to close `activate`/`deactivate` pairs
- Placing participant declarations after the first message

## 2. State Diagram (stateDiagram-v2)

### Basic Syntax

```
stateDiagram-v2
    [*] --> Draft
    Draft --> PendingReview: Submit
    PendingReview --> Approved: Approve
    PendingReview --> Draft: Reject (with comments)
    Approved --> Published: Publish
    Published --> Archived: Archive
    Archived --> [*]
```

### States with Description

```
stateDiagram-v2
    state "Draft (editing)" as Draft
    state "Pending Review" as PendingReview
    state "Approved" as Approved

    [*] --> Draft
    Draft --> PendingReview: Submit for review
    PendingReview --> Approved: Reviewer approves
    PendingReview --> Draft: Reviewer rejects
```

### Composite States (Nested)

```
stateDiagram-v2
    [*] --> Active

    state Active {
        [*] --> Normal
        Normal --> Warning: Usage > 80%
        Warning --> Critical: Usage > 95%
        Critical --> Warning: Usage drops below 95%
        Warning --> Normal: Usage drops below 80%
    }

    Active --> Suspended: Payment overdue
    Suspended --> Active: Payment received
    Suspended --> Terminated: 90 days elapsed
    Terminated --> [*]
```

### Fork and Join (Concurrent States)

```
stateDiagram-v2
    state fork_state <<fork>>
    state join_state <<join>>

    [*] --> OrderReceived
    OrderReceived --> fork_state

    fork_state --> PaymentProcessing
    fork_state --> InventoryCheck

    PaymentProcessing --> PaymentCompleted
    InventoryCheck --> StockConfirmed

    PaymentCompleted --> join_state
    StockConfirmed --> join_state

    join_state --> Shipping
    Shipping --> Delivered
    Delivered --> [*]
```

### Choice (Decision Point)

```
stateDiagram-v2
    state check_amount <<choice>>

    [*] --> ReviewRequest
    ReviewRequest --> check_amount

    check_amount --> AutoApproved: Amount < 10,000
    check_amount --> ManagerReview: 10,000 <= Amount < 100,000
    check_amount --> DirectorReview: Amount >= 100,000

    AutoApproved --> Completed
    ManagerReview --> Completed: Approved
    ManagerReview --> Rejected: Denied
    DirectorReview --> Completed: Approved
    DirectorReview --> Rejected: Denied

    Completed --> [*]
    Rejected --> [*]
```

### Best Practices

1. **Always include `[*]` start and end** — Makes the lifecycle boundary clear
2. **Use descriptive transition labels** — Include the event/trigger that causes the transition
3. **Limit to 8-10 states** — Use composite states for complex lifecycles
4. **Show all terminal states** — Every state without outgoing transitions must connect to `[*]`
5. **Use `<<choice>>` for business rules** — Makes decision logic explicit

### Common Mistakes

- Forgetting the `v2` suffix: use `stateDiagram-v2`, not `stateDiagram`
- Missing transition label (arrow without event description)
- Orphaned states with no incoming or outgoing transitions
- Using special characters in state names without quoting (use `state "Name with spaces" as alias`)

## 3. ER Diagram (erDiagram)

### Basic Syntax

```
erDiagram
    USER {
        bigint id PK
        varchar email UK
        varchar name
        varchar password_hash
        timestamp created_at
        timestamp updated_at
    }

    ORDER {
        bigint id PK
        bigint user_id FK
        decimal total_amount
        varchar status
        timestamp ordered_at
        timestamp created_at
        timestamp updated_at
    }

    USER ||--o{ ORDER : places
```

### Relationship Cardinality

| Notation | Meaning |
|----------|---------|
| `\|\|--\|\|` | One to one (exactly one on both sides) |
| `\|\|--o\|` | One to zero-or-one |
| `\|\|--o{` | One to zero-or-many |
| `\|\|--\|{` | One to one-or-many |
| `o\|--o{` | Zero-or-one to zero-or-many |
| `}o--o{` | Zero-or-many to zero-or-many (use junction table) |

### Comprehensive Example

```
erDiagram
    DEPARTMENT {
        bigint id PK
        varchar name UK
        varchar code UK
        bigint parent_id FK "Self-referential"
        timestamp created_at
        timestamp updated_at
    }

    EMPLOYEE {
        bigint id PK
        varchar employee_code UK
        varchar first_name
        varchar last_name
        varchar email UK
        bigint department_id FK
        bigint manager_id FK "Self-referential"
        date hire_date
        varchar status "active/inactive/terminated"
        timestamp created_at
        timestamp updated_at
    }

    PROJECT {
        bigint id PK
        varchar name
        text description
        date start_date
        date end_date
        varchar status
        bigint owner_id FK
        timestamp created_at
        timestamp updated_at
    }

    PROJECT_MEMBER {
        bigint id PK
        bigint project_id FK
        bigint employee_id FK
        varchar role "lead/member/reviewer"
        date joined_at
        timestamp created_at
    }

    DEPARTMENT ||--o{ EMPLOYEE : "has members"
    EMPLOYEE ||--o{ EMPLOYEE : "manages"
    EMPLOYEE ||--o{ PROJECT : "owns"
    PROJECT ||--|{ PROJECT_MEMBER : "has"
    EMPLOYEE ||--o{ PROJECT_MEMBER : "participates in"
```

### Best Practices

1. **Include PK/FK/UK markers** — Makes constraints visible in the diagram
2. **Use data types** — Helps developers understand the schema at a glance
3. **Add comments for ambiguous columns** — Use quoted strings after the type
4. **Show junction tables explicitly** — Do not use many-to-many directly; model the junction table
5. **Keep diagrams focused** — For large schemas, split into domain-specific diagrams

### Common Mistakes

- Using plural table names ("users" instead of "user") — follow singular convention
- Omitting the relationship label (the string after `:`)
- Forgetting to model junction tables for many-to-many relationships
- Using spaces in entity or attribute names without quoting

## 4. Flowchart (flowchart / graph)

### Screen Transition Flows

```
flowchart LR
    Login[SCR-001: Login] -->|Success| Dashboard[SCR-002: Dashboard]
    Login -->|Forgot password| ResetPwd[SCR-003: Reset Password]
    ResetPwd -->|Email sent| Login
    Dashboard -->|Click user list| UserList[SCR-004: User List]
    Dashboard -->|Click settings| Settings[SCR-005: Settings]
    UserList -->|Click user| UserDetail[SCR-006: User Detail]
    UserDetail -->|Edit| UserEdit[SCR-007: User Edit]
    UserEdit -->|Save| UserDetail
    UserEdit -->|Cancel| UserDetail
```

### Decision Trees

```
flowchart TD
    Start([Start]) --> InputValidation{Input valid?}
    InputValidation -->|Yes| AuthCheck{Authenticated?}
    InputValidation -->|No| Error400[Return 400 Bad Request]
    AuthCheck -->|Yes| AuthzCheck{Authorized?}
    AuthCheck -->|No| Error401[Return 401 Unauthorized]
    AuthzCheck -->|Yes| Process[Process Request]
    AuthzCheck -->|No| Error403[Return 403 Forbidden]
    Process --> Success[Return 200 OK]
```

### Direction Options

| Direction | Meaning | Use Case |
|-----------|---------|----------|
| `TD` / `TB` | Top to bottom | Decision trees, process flows |
| `LR` | Left to right | Screen transitions, timelines |
| `BT` | Bottom to top | Hierarchical rollup |
| `RL` | Right to left | Reverse flows |

### Node Shapes

| Shape | Syntax | Use Case |
|-------|--------|----------|
| Rectangle | `[text]` | Process step, screen |
| Rounded | `(text)` | Start/end, sub-process |
| Stadium | `([text])` | Terminal (start/end) |
| Diamond | `{text}` | Decision |
| Hexagon | `{{text}}` | Preparation step |
| Parallelogram | `[/text/]` | Input/Output |
| Database | `[(text)]` | Database |

### Best Practices

1. **Use `LR` for screen transitions** — Horizontal flow maps to user navigation
2. **Use `TD` for decision logic** — Vertical flow maps to processing order
3. **Label all edges** — Every arrow should describe the condition or action
4. **Use consistent node shapes** — Screens as rectangles, decisions as diamonds
5. **Limit branching depth** — If more than 4 levels deep, consider splitting into sub-diagrams

### Common Mistakes

- Missing edge labels on conditional branches
- Inconsistent direction (mixing LR and TD in mental model)
- Overcrowded diagrams — keep to 15 nodes maximum per diagram
- Using `graph` keyword instead of `flowchart` — `flowchart` supports newer features

## 5. General Tips for Readable Diagrams

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Participant (sequence) | PascalCase alias, descriptive display name | `participant AS as Auth Service` |
| State | PascalCase | `PendingReview` |
| Entity (ER) | UPPER_SNAKE_CASE | `PROJECT_MEMBER` |
| Flowchart node | SCR-ID prefix | `SCR001[Login Screen]` |

### Size and Complexity Limits

| Diagram Type | Max Elements | Recommendation |
|-------------|-------------|----------------|
| Sequence | 6 participants, 20 messages | Split long flows into sub-sequences |
| State | 10 states | Use composite states for complexity |
| ER | 8 entities | Split by domain boundary |
| Flowchart | 15 nodes | Split into sub-flowcharts |

### Color and Styling (Optional)

Use `style` and `classDef` to highlight important elements:

```
flowchart LR
    classDef error fill:#f96,stroke:#333,color:#fff
    classDef success fill:#6f6,stroke:#333,color:#fff

    A[Process] -->|Error| B[Error Handler]:::error
    A -->|OK| C[Success]:::success
```

### Rendering Validation

Before including any Mermaid diagram in a specification:

1. Verify the diagram renders without errors in a Mermaid live editor
2. Check that all participants/states/entities are referenced
3. Ensure all `alt`/`opt`/`loop`/`par` blocks have matching `end` keywords
4. Confirm all relationship labels are present and descriptive
5. Verify the diagram reads naturally in the chosen direction (LR/TD)
