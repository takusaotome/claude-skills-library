# API Specification: {API_ID} — {API_NAME}

---

## Endpoint Overview

| Field | Value |
|-------|-------|
| Endpoint ID | {API_ID} |
| Method | {HTTP_METHOD} |
| Path | `{API_PATH}` |
| Description | {API_DESCRIPTION} |
| Version | v1 |
| Status | Draft / Approved / Deprecated |

---

## Authentication & Authorization

| Field | Value |
|-------|-------|
| Authentication required | Yes / No |
| Authentication method | Bearer Token / API Key / None |
| Required roles | {REQUIRED_ROLES} |
| Required permissions | {REQUIRED_PERMISSIONS} |

---

## Request

### Headers

| Header | Required | Value | Description |
|--------|----------|-------|-------------|
| Content-Type | Yes | application/json | Request body format |
| Authorization | Yes | Bearer {token} | Authentication token |
| X-Request-ID | No | UUID v4 | Request tracking ID |
| Accept-Language | No | ja, en | Preferred response language |

### Path Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| {PATH_PARAM_1} | {TYPE_1} | Yes | {DESC_1} | {EXAMPLE_1} |

### Query Parameters

| Parameter | Type | Required | Default | Description | Example |
|-----------|------|----------|---------|-------------|---------|
| page | integer | No | 1 | Page number (offset-based pagination) | 2 |
| per_page | integer | No | 20 | Items per page (max: 100) | 50 |
| sort | string | No | created_at | Sort field | name |
| order | string | No | desc | Sort direction (asc/desc) | asc |
| {QUERY_PARAM_1} | {TYPE_1} | {REQUIRED_1} | {DEFAULT_1} | {DESC_1} | {EXAMPLE_1} |

### Request Body

**Content-Type:** application/json

**Schema:**

| Field | Type | Required | Validation | Description |
|-------|------|----------|-----------|-------------|
| {FIELD_1} | {TYPE_1} | {REQUIRED_1} | {VALIDATION_1} | {DESC_1} |
| {FIELD_2} | {TYPE_2} | {REQUIRED_2} | {VALIDATION_2} | {DESC_2} |
| {FIELD_3} | {TYPE_3} | {REQUIRED_3} | {VALIDATION_3} | {DESC_3} |

**Example:**

```json
{
  "{FIELD_1}": "{EXAMPLE_VALUE_1}",
  "{FIELD_2}": "{EXAMPLE_VALUE_2}",
  "{FIELD_3}": "{EXAMPLE_VALUE_3}"
}
```

---

## Response

### Success Response

**Status Code:** {SUCCESS_STATUS_CODE} {SUCCESS_STATUS_TEXT}

**Headers:**

| Header | Value | Description |
|--------|-------|-------------|
| Content-Type | application/json | Response body format |
| X-Request-ID | UUID v4 | Echo of request tracking ID |
| Location | /api/v1/{resource}/{id} | (201 only) URL of created resource |

**Body:**

```json
{
  "data": {
    "id": {EXAMPLE_ID},
    "{FIELD_1}": "{EXAMPLE_VALUE_1}",
    "{FIELD_2}": "{EXAMPLE_VALUE_2}",
    "{FIELD_3}": "{EXAMPLE_VALUE_3}",
    "created_at": "2025-01-15T09:30:00Z",
    "updated_at": "2025-01-15T09:30:00Z"
  }
}
```

**Collection Response (for GET list endpoints):**

```json
{
  "data": [
    {
      "id": 1,
      "{FIELD_1}": "{EXAMPLE_VALUE_1}",
      "created_at": "2025-01-15T09:30:00Z"
    },
    {
      "id": 2,
      "{FIELD_1}": "{EXAMPLE_VALUE_2}",
      "created_at": "2025-01-14T10:00:00Z"
    }
  ],
  "meta": {
    "total": {TOTAL_COUNT},
    "page": 1,
    "per_page": 20,
    "total_pages": {TOTAL_PAGES}
  }
}
```

### Error Responses

#### 400 Bad Request — Validation Error

**Condition:** Request body or parameters fail validation.

```json
{
  "error": {
    "code": "ERR_VALIDATION_FAILED",
    "message": "One or more fields failed validation.",
    "details": [
      {
        "field": "{FIELD_1}",
        "code": "ERR_REQUIRED",
        "message": "{FIELD_1} is required."
      },
      {
        "field": "{FIELD_2}",
        "code": "ERR_INVALID_FORMAT",
        "message": "{FIELD_2} must be a valid email address."
      }
    ]
  }
}
```

#### 401 Unauthorized — Authentication Error

**Condition:** Missing, expired, or invalid authentication token.

```json
{
  "error": {
    "code": "ERR_AUTH_TOKEN_INVALID",
    "message": "The provided authentication token is invalid or expired."
  }
}
```

#### 403 Forbidden — Authorization Error

**Condition:** Authenticated user lacks the required role or permission.

```json
{
  "error": {
    "code": "ERR_AUTHZ_INSUFFICIENT_ROLE",
    "message": "You do not have permission to perform this action. Required role: {REQUIRED_ROLES}."
  }
}
```

#### 404 Not Found — Resource Not Found

**Condition:** The requested resource does not exist or has been deleted.

```json
{
  "error": {
    "code": "ERR_RESOURCE_NOT_FOUND",
    "message": "The requested {RESOURCE_NAME} with ID {id} was not found."
  }
}
```

#### 409 Conflict — Resource Conflict

**Condition:** The request conflicts with the current state of the resource (e.g., duplicate key, version mismatch).

```json
{
  "error": {
    "code": "ERR_RESOURCE_CONFLICT",
    "message": "A {RESOURCE_NAME} with the same {UNIQUE_FIELD} already exists."
  }
}
```

#### 422 Unprocessable Entity — Business Rule Violation

**Condition:** Request is syntactically valid but violates a business rule.

```json
{
  "error": {
    "code": "ERR_BIZ_{RULE_CODE}",
    "message": "{BUSINESS_RULE_DESCRIPTION}"
  }
}
```

#### 429 Too Many Requests — Rate Limit Exceeded

**Condition:** Client has exceeded the allowed request rate.

**Headers:**

| Header | Value |
|--------|-------|
| Retry-After | 60 |
| X-RateLimit-Limit | 1000 |
| X-RateLimit-Remaining | 0 |
| X-RateLimit-Reset | 1640995200 |

```json
{
  "error": {
    "code": "ERR_RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please retry after 60 seconds."
  }
}
```

#### 500 Internal Server Error — System Error

**Condition:** An unexpected error occurred on the server.

```json
{
  "error": {
    "code": "ERR_SYS_INTERNAL",
    "message": "An internal server error occurred. Please contact support with request ID: {X-Request-ID}."
  }
}
```

---

## Error Code Reference

| Error Code | HTTP Status | Description | Resolution |
|-----------|------------|-------------|------------|
| ERR_REQUIRED | 400 | Required field missing | Include the field in the request |
| ERR_INVALID_FORMAT | 400 | Field format is invalid | Check the field format requirements |
| ERR_TOO_LONG | 400 | Field exceeds max length | Shorten the field value |
| ERR_OUT_OF_RANGE | 400 | Numeric value outside range | Use a value within the allowed range |
| ERR_DUPLICATE | 409 | Duplicate value exists | Use a unique value |
| ERR_AUTH_TOKEN_INVALID | 401 | Invalid auth token | Obtain a new token |
| ERR_AUTH_TOKEN_EXPIRED | 401 | Expired auth token | Refresh the token |
| ERR_AUTHZ_INSUFFICIENT_ROLE | 403 | Lacks required role | Request role assignment |
| ERR_RESOURCE_NOT_FOUND | 404 | Resource does not exist | Verify the resource ID |
| ERR_RESOURCE_CONFLICT | 409 | State conflict | Resolve the conflict |
| ERR_RATE_LIMIT_EXCEEDED | 429 | Too many requests | Wait and retry |
| ERR_SYS_INTERNAL | 500 | Server error | Contact support |

---

## Example Request/Response

### Request

```bash
curl -X {HTTP_METHOD} \
  '{BASE_URL}{API_PATH}' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIs...' \
  -d '{
    "{FIELD_1}": "{EXAMPLE_VALUE_1}",
    "{FIELD_2}": "{EXAMPLE_VALUE_2}"
  }'
```

### Response

```
HTTP/1.1 {SUCCESS_STATUS_CODE} {SUCCESS_STATUS_TEXT}
Content-Type: application/json
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000

{
  "data": {
    "id": {EXAMPLE_ID},
    "{FIELD_1}": "{EXAMPLE_VALUE_1}",
    "{FIELD_2}": "{EXAMPLE_VALUE_2}",
    "created_at": "2025-01-15T09:30:00Z",
    "updated_at": "2025-01-15T09:30:00Z"
  }
}
```

---

## Notes and Constraints

- {NOTE_1}
- {NOTE_2}
- {CONSTRAINT_1}

---

## Related Endpoints

| API ID | Method | Path | Relationship |
|--------|--------|------|-------------|
| {RELATED_API_1} | {RELATED_METHOD_1} | {RELATED_PATH_1} | {RELATIONSHIP_1} |
| {RELATED_API_2} | {RELATED_METHOD_2} | {RELATED_PATH_2} | {RELATIONSHIP_2} |

---

## Sequence Diagram

```mermaid
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant S as {SERVICE_NAME}
    participant DB as Database

    C->>GW: {HTTP_METHOD} {API_PATH}
    GW->>GW: Validate token
    GW->>S: Forward request

    alt Validation passes
        S->>DB: {DB_OPERATION}
        DB-->>S: Result
        S-->>GW: {SUCCESS_STATUS_CODE} {SUCCESS_STATUS_TEXT}
        GW-->>C: {SUCCESS_STATUS_CODE} with response body
    else Validation fails
        S-->>GW: 400 Bad Request
        GW-->>C: 400 with error details
    end
```
