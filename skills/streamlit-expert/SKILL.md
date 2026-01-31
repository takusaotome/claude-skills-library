---
name: streamlit-expert
description: Streamlit Web application development expert skill. Provides guidance on OIDC authentication (st.login/st.logout/st.user), secrets management, data visualization with Plotly/Altair, performance optimization with caching, and modern Streamlit features (v1.42-1.52+). Use this skill when building Streamlit apps, implementing user authentication, creating data dashboards, or optimizing app performance. Triggers include "streamlit app", "st.login", "data dashboard", "streamlit authentication", "streamlit visualization".
---

# Streamlit Expert

## Overview

Streamlit Web application development expert skill supporting the latest features from v1.42 to v1.52+ (2025-2026). Provides comprehensive guidance on:

- **Authentication**: Native OIDC authentication with `st.login()`, `st.logout()`, `st.user`
- **Data Visualization**: Optimal library selection (Plotly, Altair, native charts) and performance tuning
- **Secrets Management**: Secure credential handling with `st.secrets`
- **Performance Optimization**: Caching strategies, large dataset handling, session state management
- **Modern Features**: Custom themes, layout containers, multipage apps, Custom Components v2

## When to Use This Skill

Use this skill when:
- Building new Streamlit applications from scratch
- Implementing user authentication with OIDC providers (Google, Microsoft, Okta, Auth0)
- Creating data visualization dashboards
- Optimizing Streamlit app performance
- Managing secrets and credentials securely
- Implementing modern Streamlit features (v1.42+)

## Workflow Decision Tree

```
User Request
├── "Add authentication" → Authentication Workflow
├── "Create dashboard/visualization" → Visualization Workflow
├── "App is slow/optimize" → Performance Optimization Workflow
├── "New Streamlit app" → Project Setup Workflow
└── "Deploy app" → Deployment Workflow
```

---

## 1. Project Setup Workflow

### Initial Project Structure

```
my-streamlit-app/
├── .streamlit/
│   ├── config.toml          # App configuration
│   └── secrets.toml          # Secrets (DO NOT COMMIT)
├── pages/                    # Multipage app pages
│   ├── 1_Dashboard.py
│   └── 2_Settings.py
├── app.py                    # Main entry point
├── requirements.txt
├── .gitignore
└── README.md
```

### Essential .gitignore Entries

```gitignore
# Streamlit secrets - CRITICAL
.streamlit/secrets.toml

# Python
__pycache__/
*.pyc
.venv/
venv/
```

### Recommended Dependencies (2025-2026)

```txt
streamlit>=1.52.0
streamlit[auth]  # For authentication (includes Authlib>=1.3.2)
plotly>=5.18.0
altair>=5.2.0
pandas>=2.0.0
orjson  # Performance optimization for Plotly
```

---

## 2. Authentication Workflow

### Prerequisites

1. Install authentication dependencies:
   ```bash
   pip install "streamlit[auth]"
   ```

2. Configure identity provider (Google, Microsoft Entra ID, Okta, Auth0)

3. Obtain from provider:
   - Client ID
   - Client secret
   - Server metadata URL

### secrets.toml Configuration

#### Single Provider Setup

```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"  # Use https:// in production
cookie_secret = "your-strong-random-secret-here"  # Generate with: python -c "import secrets; print(secrets.token_hex(32))"
client_id = "your-client-id"
client_secret = "your-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"  # Google example
```

#### Multiple Providers Setup

```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-strong-random-secret-here"

[auth.google]
client_id = "google-client-id"
client_secret = "google-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

[auth.microsoft]
client_id = "microsoft-client-id"
client_secret = "microsoft-client-secret"
server_metadata_url = "https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration"
```

### Authentication Implementation Pattern

```python
import streamlit as st

# Check login status
if not st.user.is_logged_in:
    st.title("Welcome to My App")
    st.write("Please log in to continue.")

    # Single provider
    st.login()

    # Multiple providers
    # col1, col2 = st.columns(2)
    # with col1:
    #     st.login("google")
    # with col2:
    #     st.login("microsoft")

    st.stop()

# User is logged in - show main content
st.title(f"Welcome, {st.user.name}!")
st.write(f"Email: {st.user.email}")

# Logout button
if st.button("Logout"):
    st.logout()
```

### Accessing User Information

```python
# Available after successful login
st.user.is_logged_in  # bool
st.user.name          # str
st.user.email         # str

# With expose_tokens configured
st.user.tokens.id     # ID token (if "id" in expose_tokens)
st.user.tokens.access # Access token (if "access" in expose_tokens)
```

### Security Best Practices

1. **ALWAYS use HTTPS in production** for redirect_uri
2. **Generate strong cookie_secret**: `python -c "import secrets; print(secrets.token_hex(32))"`
3. **Never commit secrets.toml** - use environment variables or secrets management in deployment
4. **Identity cookies expire after 30 days** - users must re-authenticate
5. **Authentication not supported for embedded apps**

---

## 3. Visualization Workflow

### Library Selection Guide

| Use Case | Recommended Library | Reason |
|----------|-------------------|--------|
| Simple charts, KPIs | Native (`st.line_chart`, `st.bar_chart`) | Fastest, zero dependencies |
| Interactive exploration | Plotly | Best interactivity, zoom/pan/hover |
| Statistical visualizations | Altair | Declarative, publication-quality |
| Publication-quality static | Matplotlib/Seaborn | Fine control, PDF export |
| Geospatial mapping | PyDeck | 3D maps, large datasets |

### Performance Benchmarks

**Rendering Speed (fastest to slowest):**
1. Native Streamlit charts
2. Altair
3. Plotly
4. Matplotlib

### Large Dataset Handling

#### Altair Limitations and Solutions

```python
import altair as alt

# Altair has a 5,000 row limit by default
# Solution 1: Increase limit (use cautiously)
alt.data_transformers.disable_max_rows()

# Solution 2: Use data URL (recommended for >5000 rows)
# This sends data as a URL reference instead of embedding
alt.data_transformers.enable('vegafusion')  # If vegafusion installed

# Solution 3: Downsample data before plotting
def downsample_data(df, max_rows=5000):
    if len(df) > max_rows:
        return df.sample(n=max_rows, random_state=42)
    return df
```

#### Plotly Optimization

```python
import plotly.express as px
import streamlit as st

# Install orjson for faster serialization
# pip install orjson

# Use WebGL renderer for large datasets
fig = px.scatter(df, x='x', y='y', render_mode='webgl')

# Reduce data points for smoother interaction
fig.update_traces(marker=dict(size=3))

# Disable expensive animations
fig.update_layout(transition_duration=0)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
```

### Chart Configuration Best Practices

```python
import streamlit as st
import plotly.express as px

# Always use container width for responsiveness
st.plotly_chart(fig, use_container_width=True)

# Configure Plotly display options
config = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'chart',
        'height': 600,
        'width': 800,
        'scale': 2
    }
}
st.plotly_chart(fig, config=config)
```

---

## 4. Performance Optimization Workflow

### Caching Strategy

#### st.cache_data (for data)

```python
import streamlit as st
import pandas as pd

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data(file_path: str) -> pd.DataFrame:
    """Load and cache data from file."""
    return pd.read_csv(file_path)

@st.cache_data
def expensive_computation(df: pd.DataFrame) -> pd.DataFrame:
    """Cache expensive transformations."""
    # Heavy processing here
    return processed_df
```

#### st.cache_resource (for resources)

```python
import streamlit as st
from sqlalchemy import create_engine

@st.cache_resource
def get_database_connection():
    """Cache database connection (shared across users)."""
    return create_engine(st.secrets["database"]["url"])

@st.cache_resource
def load_ml_model():
    """Cache ML model loading."""
    import joblib
    return joblib.load("model.pkl")
```

### Session State Best Practices

```python
import streamlit as st

# Initialize session state
if "counter" not in st.session_state:
    st.session_state.counter = 0

if "data" not in st.session_state:
    st.session_state.data = None

# Use session state for user inputs that should persist
def increment():
    st.session_state.counter += 1

st.button("Increment", on_click=increment)
st.write(f"Count: {st.session_state.counter}")
```

### Fragment-Based Updates (Partial Reruns)

```python
import streamlit as st

@st.fragment
def chart_section():
    """Only this section reruns when its widgets change."""
    chart_type = st.selectbox("Chart Type", ["Line", "Bar", "Scatter"])
    # Chart rendering here
    st.line_chart(data)

@st.fragment
def filter_section():
    """Independent fragment for filters."""
    date_range = st.date_input("Date Range")
    category = st.multiselect("Categories", options)
    return date_range, category

# Main app
st.title("Dashboard")
filter_section()
chart_section()
```

### Memory Optimization for Large Datasets

```python
import streamlit as st
import pandas as pd

# Use appropriate dtypes
@st.cache_data
def load_optimized_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(
        file_path,
        dtype={
            'id': 'int32',
            'category': 'category',
            'value': 'float32'
        },
        parse_dates=['date']
    )
    return df

# Stream large files
def process_large_file(file):
    chunks = pd.read_csv(file, chunksize=10000)
    for chunk in chunks:
        # Process each chunk
        yield process_chunk(chunk)
```

---

## 5. Secrets Management

### Local Development

```toml
# .streamlit/secrets.toml (NEVER COMMIT)

[database]
host = "localhost"
port = 5432
username = "user"
password = "password"

[api_keys]
openai = "sk-..."
google_maps = "AIza..."

[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "dev-secret"
```

### Accessing Secrets

```python
import streamlit as st

# Dictionary-style access
db_host = st.secrets["database"]["host"]

# Attribute-style access
api_key = st.secrets.api_keys.openai

# Pass entire section as kwargs
import psycopg2
conn = psycopg2.connect(**st.secrets.database)
```

### Production Deployment

**Streamlit Community Cloud:**
- Use the "Secrets" section in app settings
- Paste secrets.toml content directly

**Docker/Kubernetes:**
- Use environment variables or mounted secret files
- Map to `.streamlit/secrets.toml` path

**Cloud Providers:**
- AWS: Use AWS Secrets Manager
- GCP: Use Secret Manager
- Azure: Use Key Vault

---

## 6. Modern Features (v1.42-1.52+)

### Theming (v1.44+)

```toml
# .streamlit/config.toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Runtime Theme Detection (v1.46+)

```python
import streamlit as st

# Detect current theme
theme = st.context.theme
if theme == "dark":
    chart_template = "plotly_dark"
else:
    chart_template = "plotly_white"
```

### Top Navigation (v1.46+)

```python
import streamlit as st

# Create top navigation
pages = st.navigation([
    st.Page("home.py", title="Home", icon="🏠"),
    st.Page("dashboard.py", title="Dashboard", icon="📊"),
    st.Page("settings.py", title="Settings", icon="⚙️"),
], position="top")

pages.run()
```

### Custom Components v2 (v1.51+)

```python
import streamlit as st
from streamlit.components.v1 import components

# Custom component with bidirectional data flow
my_component = components.declare_component(
    "my_component",
    path="frontend/build"
)

result = my_component(data=my_data, key="unique_key")
```

### New Widgets (v1.52)

```python
import streamlit as st
from datetime import datetime

# Combined date and time input
dt = st.datetime_input("Select date and time", value=datetime.now())

# Download button with callable
def generate_report():
    return create_pdf_report()

st.download_button(
    "Download Report",
    data=generate_report,  # Callable - generates on demand
    file_name="report.pdf"
)

# Chat input with audio
message = st.chat_input("Type or speak", accept_audio=True)
```

---

## 7. Common Patterns and Best Practices

### Application Structure Pattern

```python
import streamlit as st

def main():
    # 1. Page configuration (MUST be first)
    st.set_page_config(
        page_title="My App",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 2. Authentication check
    if not st.user.is_logged_in:
        show_login_page()
        st.stop()

    # 3. Initialize session state
    init_session_state()

    # 4. Sidebar navigation
    with st.sidebar:
        page = st.selectbox("Navigation", ["Dashboard", "Settings"])

    # 5. Main content
    if page == "Dashboard":
        show_dashboard()
    elif page == "Settings":
        show_settings()

if __name__ == "__main__":
    main()
```

### Error Handling Pattern

```python
import streamlit as st

def safe_operation():
    try:
        result = risky_operation()
        st.success("Operation completed!")
        return result
    except ConnectionError:
        st.error("Connection failed. Please check your network.")
    except ValueError as e:
        st.warning(f"Invalid input: {e}")
    except Exception as e:
        st.exception(e)  # Shows full traceback in dev
        # In production, use st.error() with user-friendly message
```

### Form Pattern (Prevent Unnecessary Reruns)

```python
import streamlit as st

with st.form("my_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Submit")

    if submitted:
        # Process form data
        save_user(name, email)
        st.success("Saved!")
```

---

## Resources

### references/
- `authentication_guide.md` - Detailed OIDC setup for major providers
- `performance_optimization.md` - Advanced caching and optimization techniques
- `visualization_best_practices.md` - Chart library comparison and usage patterns
- `release_notes_summary.md` - Key features by version

### assets/
- `app_template.py` - Production-ready application template
- `auth_template.py` - Authentication implementation template
- `dashboard_template.py` - Data dashboard template
- `secrets_template.toml` - secrets.toml template with comments

---

## Quick Reference

| Feature | Version | Key API |
|---------|---------|---------|
| Native Auth | 1.42+ | `st.login()`, `st.logout()`, `st.user` |
| Advanced Theming | 1.44+ | `config.toml [theme]` |
| Top Navigation | 1.46+ | `st.navigation(position="top")` |
| Theme Detection | 1.46+ | `st.context.theme` |
| Custom Components v2 | 1.51+ | `components.declare_component()` |
| Datetime Input | 1.52+ | `st.datetime_input()` |
| Callable Downloads | 1.52+ | `st.download_button(data=callable)` |
