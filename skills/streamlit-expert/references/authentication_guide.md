# Streamlit Authentication Guide

Detailed OIDC setup instructions for major identity providers.

## Overview

Streamlit v1.42+ provides native OIDC authentication via `st.login()`, `st.logout()`, and `st.user`. This guide covers setup for the most common identity providers.

## Prerequisites

```bash
pip install "streamlit[auth]"
# This installs Authlib>=1.3.2
```

---

## Google Identity Setup

### 1. Google Cloud Console Configuration

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Navigate to **APIs & Services** > **Credentials**
4. Click **Create Credentials** > **OAuth client ID**
5. Select **Web application**
6. Configure:
   - **Name**: Your app name
   - **Authorized JavaScript origins**: `http://localhost:8501` (dev), `https://your-domain.com` (prod)
   - **Authorized redirect URIs**: `http://localhost:8501/oauth2callback` (dev), `https://your-domain.com/oauth2callback` (prod)
7. Note your **Client ID** and **Client secret**

### 2. secrets.toml Configuration

```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-strong-random-secret"
client_id = "your-google-client-id.apps.googleusercontent.com"
client_secret = "your-google-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

### 3. Optional: Restrict to Specific Domain

```toml
[auth]
# ... other settings ...
client_kwargs = { hd = "yourcompany.com" }  # Restrict to company domain
```

---

## Microsoft Entra ID (Azure AD) Setup

### 1. Azure Portal Configuration

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to **Microsoft Entra ID** > **App registrations**
3. Click **New registration**
4. Configure:
   - **Name**: Your app name
   - **Supported account types**: Choose based on your needs
   - **Redirect URI**: Web, `http://localhost:8501/oauth2callback`
5. After creation, go to **Certificates & secrets**
6. Create a new **Client secret** and note the value
7. Note your **Application (client) ID** and **Directory (tenant) ID**

### 2. API Permissions

1. Go to **API permissions**
2. Add **Microsoft Graph** > **Delegated permissions**:
   - `openid`
   - `profile`
   - `email`
3. Grant admin consent if required

### 3. secrets.toml Configuration

```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-strong-random-secret"
client_id = "your-application-client-id"
client_secret = "your-client-secret-value"
server_metadata_url = "https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration"
```

Replace `{tenant-id}` with your Directory (tenant) ID.

### 4. Multi-Tenant Configuration

For apps supporting multiple organizations:

```toml
server_metadata_url = "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration"
```

---

## Okta Setup

### 1. Okta Admin Console Configuration

1. Go to your Okta Admin Console
2. Navigate to **Applications** > **Create App Integration**
3. Select **OIDC - OpenID Connect** and **Web Application**
4. Configure:
   - **App integration name**: Your app name
   - **Grant type**: Authorization Code
   - **Sign-in redirect URIs**: `http://localhost:8501/oauth2callback`
   - **Sign-out redirect URIs**: `http://localhost:8501`
   - **Assignments**: Configure user/group access

### 2. Note Required Values

- **Client ID**: Found in application settings
- **Client secret**: Found in application settings
- **Okta domain**: e.g., `dev-12345678.okta.com`

### 3. secrets.toml Configuration

```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-strong-random-secret"
client_id = "your-okta-client-id"
client_secret = "your-okta-client-secret"
server_metadata_url = "https://dev-12345678.okta.com/.well-known/openid-configuration"
```

---

## Auth0 Setup

### 1. Auth0 Dashboard Configuration

1. Go to [Auth0 Dashboard](https://manage.auth0.com/)
2. Navigate to **Applications** > **Create Application**
3. Select **Regular Web Applications**
4. Go to **Settings** tab
5. Configure:
   - **Allowed Callback URLs**: `http://localhost:8501/oauth2callback`
   - **Allowed Logout URLs**: `http://localhost:8501`
   - **Allowed Web Origins**: `http://localhost:8501`

### 2. Note Required Values

- **Domain**: e.g., `your-tenant.auth0.com`
- **Client ID**: Found in application settings
- **Client Secret**: Found in application settings

### 3. secrets.toml Configuration

```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-strong-random-secret"
client_id = "your-auth0-client-id"
client_secret = "your-auth0-client-secret"
server_metadata_url = "https://your-tenant.auth0.com/.well-known/openid-configuration"
```

---

## Multiple Providers Configuration

Support multiple identity providers in a single app:

```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-strong-random-secret"

[auth.google]
client_id = "google-client-id"
client_secret = "google-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

[auth.microsoft]
client_id = "microsoft-client-id"
client_secret = "microsoft-client-secret"
server_metadata_url = "https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration"

[auth.okta]
client_id = "okta-client-id"
client_secret = "okta-client-secret"
server_metadata_url = "https://dev-12345678.okta.com/.well-known/openid-configuration"
```

### Implementation

```python
import streamlit as st

if not st.user.is_logged_in:
    st.title("Sign In")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Google")
        st.login("google")

    with col2:
        st.subheader("Microsoft")
        st.login("microsoft")

    with col3:
        st.subheader("Okta")
        st.login("okta")

    st.stop()

# User is logged in
st.write(f"Welcome, {st.user.name}!")
```

---

## Exposing Tokens

To access ID and access tokens for downstream API calls:

```toml
[auth]
# ... other settings ...
expose_tokens = ["id", "access"]
```

### Usage

```python
import streamlit as st

if st.user.is_logged_in:
    # Access tokens for API calls
    id_token = st.user.tokens.id
    access_token = st.user.tokens.access

    # Use access token for API calls
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.example.com/data", headers=headers)
```

---

## Custom OIDC Parameters

Override default OIDC parameters:

```toml
[auth]
# ... other settings ...
client_kwargs = {
    scope = "openid profile email custom_scope",
    prompt = "login",  # Force re-authentication
    hd = "company.com"  # Google: restrict to domain
}
```

---

## Security Best Practices

### 1. Generate Strong Cookie Secret

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Use HTTPS in Production

```toml
# Production secrets.toml
[auth]
redirect_uri = "https://your-app.example.com/oauth2callback"
```

### 3. Validate User Domain (if needed)

```python
import streamlit as st

ALLOWED_DOMAINS = ["company.com", "partner.com"]

if st.user.is_logged_in:
    email_domain = st.user.email.split("@")[1]
    if email_domain not in ALLOWED_DOMAINS:
        st.error("Access denied. Your organization is not authorized.")
        st.logout()
        st.stop()
```

### 4. Role-Based Access Control

```python
import streamlit as st

# Define roles based on email or claims
ADMIN_EMAILS = ["admin@company.com"]

def get_user_role():
    if st.user.email in ADMIN_EMAILS:
        return "admin"
    return "user"

if st.user.is_logged_in:
    role = get_user_role()

    if role == "admin":
        st.sidebar.page_link("pages/admin.py", label="Admin Panel")
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Redirect loop | Incorrect redirect_uri | Ensure exact match with provider config |
| Invalid client | Wrong client_id/secret | Verify credentials |
| CORS errors | Missing origins in provider | Add origins to provider config |
| Token expired | 30-day cookie expiry | User must re-authenticate |

### Debug Mode

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Provider Metadata

Verify your provider's OIDC configuration:

```python
import requests
url = "https://accounts.google.com/.well-known/openid-configuration"
print(requests.get(url).json())
```
