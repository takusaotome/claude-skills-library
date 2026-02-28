# API Design Guide

This reference provides comprehensive guidance for designing RESTful APIs following industry best practices. Use this guide when creating API specifications (Workflow 3).

## 1. REST Design Principles

### Resource-Oriented Design

REST APIs are organized around resources — any named entity that the API exposes. Design endpoints around nouns (resources), not verbs (actions).

**Correct:**
```
GET    /api/v1/users          # List users
POST   /api/v1/users          # Create a user
GET    /api/v1/users/123      # Get a specific user
PUT    /api/v1/users/123      # Update a user (full replacement)
PATCH  /api/v1/users/123      # Partially update a user
DELETE /api/v1/users/123      # Delete a user
```

**Incorrect:**
```
GET    /api/v1/getUsers        # Verb in URL
POST   /api/v1/createUser      # Verb in URL
POST   /api/v1/deleteUser/123  # Using POST for deletion
```

### HTTP Methods and Their Semantics

| Method | Purpose | Idempotent | Safe | Request Body | Typical Response |
|--------|---------|-----------|------|-------------|-----------------|
| GET | Retrieve resource(s) | Yes | Yes | No | 200 with body |
| POST | Create a resource | No | No | Yes | 201 with body and Location header |
| PUT | Full replacement of a resource | Yes | No | Yes | 200 with body |
| PATCH | Partial update of a resource | No* | No | Yes | 200 with body |
| DELETE | Remove a resource | Yes | No | No | 204 No Content |

*PATCH can be made idempotent with JSON Merge Patch (RFC 7396).

### HTTP Status Codes

#### Success Codes

| Code | Meaning | When to Use |
|------|---------|------------|
| 200 OK | Request succeeded | GET, PUT, PATCH with response body |
| 201 Created | Resource created | POST when a new resource is created |
| 202 Accepted | Request accepted for processing | Async operations not yet completed |
| 204 No Content | Success, no body | DELETE, or PUT/PATCH with no response body |

#### Client Error Codes

| Code | Meaning | When to Use |
|------|---------|------------|
| 400 Bad Request | Malformed request | Invalid JSON, missing required fields, validation errors |
| 401 Unauthorized | Authentication required | Missing or invalid authentication token |
| 403 Forbidden | Insufficient permissions | Valid token but lacks required role/permission |
| 404 Not Found | Resource does not exist | Invalid resource ID or path |
| 409 Conflict | State conflict | Duplicate creation, version conflict |
| 422 Unprocessable Entity | Semantic error | Syntactically valid but semantically invalid (business rule violation) |
| 429 Too Many Requests | Rate limit exceeded | Client has sent too many requests |

#### Server Error Codes

| Code | Meaning | When to Use |
|------|---------|------------|
| 500 Internal Server Error | Unexpected server error | Unhandled exceptions, infrastructure failures |
| 502 Bad Gateway | Upstream service error | Dependency service returned invalid response |
| 503 Service Unavailable | Service temporarily unavailable | Maintenance, overload |
| 504 Gateway Timeout | Upstream timeout | Dependency service timed out |

## 2. URL Naming Conventions

### Structure Pattern

```
/api/v{version}/{resource-collection}/{resource-id}/{sub-resource-collection}/{sub-resource-id}
```

### Rules

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Use plural nouns for collections | `/users` | `/user` |
| Use lowercase with hyphens | `/order-items` | `/orderItems`, `/order_items` |
| No trailing slashes | `/users` | `/users/` |
| No file extensions | `/users/123` | `/users/123.json` |
| Use path params for identity | `/users/123` | `/users?id=123` |
| Use query params for filtering | `/users?status=active` | `/users/active` |
| Nest sub-resources max 2 levels | `/users/123/orders` | `/users/123/orders/456/items/789` |

### Special Endpoints

For actions that do not map to CRUD, use a verb suffix as a sub-resource:

```
POST /api/v1/users/123/activate        # Action on a resource
POST /api/v1/orders/456/cancel          # Action on a resource
POST /api/v1/reports/generate           # Trigger a process
GET  /api/v1/search?q=keyword           # Cross-resource search
```

## 3. Request/Response Body Standards

### Request Body Format

Always use JSON (`Content-Type: application/json`).

**Create request example:**
```json
{
  "email": "user@example.com",
  "name": "Taro Yamada",
  "role": "member",
  "department_id": 5
}
```

**Update (PATCH) request example:**
```json
{
  "name": "Taro Yamada Updated"
}
```

### Response Envelope Pattern

Use a consistent envelope for all responses:

**Success response (single resource):**
```json
{
  "data": {
    "id": 123,
    "email": "user@example.com",
    "name": "Taro Yamada",
    "role": "member",
    "department_id": 5,
    "created_at": "2025-01-15T09:30:00Z",
    "updated_at": "2025-01-15T09:30:00Z"
  }
}
```

**Success response (collection):**
```json
{
  "data": [
    { "id": 1, "name": "Item 1" },
    { "id": 2, "name": "Item 2" }
  ],
  "meta": {
    "total": 42,
    "page": 1,
    "per_page": 20,
    "total_pages": 3
  }
}
```

## 4. Error Response Format

### Standard Error Envelope

All error responses must follow this structure:

```json
{
  "error": {
    "code": "ERR_VALIDATION_FAILED",
    "message": "One or more fields failed validation.",
    "details": [
      {
        "field": "email",
        "code": "ERR_INVALID_FORMAT",
        "message": "Email must be a valid email address."
      },
      {
        "field": "name",
        "code": "ERR_REQUIRED",
        "message": "Name is required."
      }
    ]
  }
}
```

### Error Code Conventions

| Category | Code Pattern | Example |
|----------|-------------|---------|
| Validation | ERR_VALIDATION_* | ERR_VALIDATION_FAILED |
| Authentication | ERR_AUTH_* | ERR_AUTH_TOKEN_EXPIRED |
| Authorization | ERR_AUTHZ_* | ERR_AUTHZ_INSUFFICIENT_ROLE |
| Resource | ERR_RESOURCE_* | ERR_RESOURCE_NOT_FOUND |
| Business logic | ERR_BIZ_* | ERR_BIZ_INSUFFICIENT_BALANCE |
| System | ERR_SYS_* | ERR_SYS_DATABASE_UNAVAILABLE |

### Field-Level Error Codes

| Code | Meaning |
|------|---------|
| ERR_REQUIRED | Field is required but missing |
| ERR_INVALID_FORMAT | Field value format is invalid |
| ERR_TOO_LONG | Field value exceeds maximum length |
| ERR_TOO_SHORT | Field value is shorter than minimum length |
| ERR_OUT_OF_RANGE | Numeric value outside allowed range |
| ERR_DUPLICATE | Value already exists (unique constraint) |
| ERR_INVALID_REFERENCE | Foreign key reference is invalid |

## 5. Pagination

### Cursor-Based Pagination (Recommended)

Best for real-time data, large datasets, and stable page results.

**Request:**
```
GET /api/v1/orders?limit=20&cursor=eyJpZCI6MTAwfQ==
```

**Response:**
```json
{
  "data": [...],
  "meta": {
    "has_next": true,
    "next_cursor": "eyJpZCI6MTIwfQ==",
    "has_previous": true,
    "previous_cursor": "eyJpZCI6MTAxfQ=="
  }
}
```

**Implementation notes:**
- Cursor is an opaque, base64-encoded token (typically encodes the last seen ID)
- Stable under concurrent inserts/deletes
- Cannot jump to arbitrary pages

### Offset-Based Pagination

Simpler implementation, suitable for admin screens and small datasets.

**Request:**
```
GET /api/v1/users?page=2&per_page=20
```

**Response:**
```json
{
  "data": [...],
  "meta": {
    "total": 150,
    "page": 2,
    "per_page": 20,
    "total_pages": 8
  }
}
```

**Implementation notes:**
- Easy to understand and implement
- Supports jumping to arbitrary pages
- Results may shift when data is inserted/deleted between requests

### When to Use Which

| Factor | Cursor-Based | Offset-Based |
|--------|-------------|-------------|
| Large datasets (>10K records) | Recommended | Avoid |
| Real-time feeds | Recommended | Avoid |
| Admin dashboards | OK | Recommended |
| Search results | Recommended | OK |
| Reports with total counts | Avoid | Recommended |

## 6. Authentication Patterns

### Bearer Token (JWT)

```
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

**Use when:** Standard web/mobile API authentication
**Spec requirement:** Document token format, expiration, refresh mechanism

### API Key

```
X-API-Key: sk_live_abc123def456
```

**Use when:** Server-to-server integration, third-party access
**Spec requirement:** Document key rotation policy, rate limits per key

### Documentation Requirements

For each endpoint, specify:

| Field | Example |
|-------|---------|
| Auth required | Yes / No |
| Auth method | Bearer Token / API Key / None |
| Required roles | admin, manager |
| Required permissions | users:read, users:write |

## 7. Rate Limiting

### Response Headers

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
Retry-After: 60
```

### Documentation Requirements

| Parameter | Description | Example |
|-----------|-----------|---------|
| Rate limit | Requests per window | 1000/hour |
| Window type | Fixed or sliding | Sliding window |
| Scope | Per user, per IP, per API key | Per API key |
| Burst limit | Max concurrent requests | 50 |

### 429 Response Body

```json
{
  "error": {
    "code": "ERR_RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please retry after 60 seconds.",
    "details": [
      {
        "limit": 1000,
        "window": "1 hour",
        "retry_after": 60
      }
    ]
  }
}
```

## 8. Versioning Strategies

### URL Versioning (Recommended)

```
/api/v1/users
/api/v2/users
```

**Advantages:** Explicit, easy to route, cacheable
**Disadvantages:** URL changes between versions

### Header Versioning

```
Accept: application/vnd.myapp.v2+json
```

**Advantages:** Clean URLs
**Disadvantages:** Harder to test, less visible

### Recommendation

Use URL versioning for simplicity and clarity. Document the deprecation policy:

| Version | Status | Sunset Date | Notes |
|---------|--------|-------------|-------|
| v1 | Deprecated | 2026-06-30 | Migration guide available |
| v2 | Current | — | — |

## 9. HATEOAS Considerations

For APIs that benefit from discoverability, include navigation links:

```json
{
  "data": {
    "id": 123,
    "name": "Taro Yamada",
    "status": "active"
  },
  "links": {
    "self": "/api/v1/users/123",
    "orders": "/api/v1/users/123/orders",
    "department": "/api/v1/departments/5",
    "deactivate": "/api/v1/users/123/deactivate"
  }
}
```

**When to include HATEOAS:**
- Public APIs consumed by third-party developers
- APIs with complex navigation between resources
- Long-lived APIs where URL structure may evolve

**When to skip HATEOAS:**
- Internal APIs with tightly coupled clients
- Simple CRUD APIs
- Performance-sensitive endpoints

## 10. API Specification Checklist

Before finalizing any API endpoint specification, verify:

- [ ] HTTP method matches the operation semantics (GET for read, POST for create, etc.)
- [ ] URL follows naming conventions (plural, lowercase, hyphens)
- [ ] Request body includes all required fields with types and validation rules
- [ ] Response body matches the envelope pattern
- [ ] All error codes are documented with HTTP status and business error code
- [ ] Authentication and authorization requirements are specified
- [ ] Request/response examples use realistic data
- [ ] Pagination strategy is defined for collection endpoints
- [ ] Rate limiting policy is documented
- [ ] Content-Type headers are specified (application/json)
