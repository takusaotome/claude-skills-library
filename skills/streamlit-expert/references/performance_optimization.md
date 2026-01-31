# Streamlit Performance Optimization Guide

Advanced techniques for building high-performance Streamlit applications.

## Understanding Streamlit's Execution Model

Streamlit reruns the entire script on every user interaction. This design enables simplicity but requires careful optimization for performance-critical applications.

```
User Interaction → Full Script Rerun → UI Update
```

### Key Performance Principles

1. **Cache expensive operations** - Use `st.cache_data` and `st.cache_resource`
2. **Minimize rerun scope** - Use `st.fragment` for partial updates
3. **Optimize data transfer** - Reduce data sent to browser
4. **Efficient state management** - Use `st.session_state` wisely

---

## Caching Strategies

### st.cache_data vs st.cache_resource

| Aspect | st.cache_data | st.cache_resource |
|--------|--------------|-------------------|
| Use for | Data (DataFrames, lists, dicts) | Resources (DB connections, ML models) |
| Serialization | Yes (pickled) | No (reference) |
| Shared across users | No (per-user copy) | Yes |
| Mutation safe | Yes | No |
| TTL support | Yes | Yes |

### Caching Data

```python
import streamlit as st
import pandas as pd

@st.cache_data(ttl=3600, show_spinner="Loading data...")
def load_data(file_path: str) -> pd.DataFrame:
    """Cache data for 1 hour with loading spinner."""
    return pd.read_csv(file_path)

@st.cache_data(max_entries=100)
def compute_statistics(df: pd.DataFrame) -> dict:
    """Cache with LRU eviction after 100 entries."""
    return {
        "mean": df["value"].mean(),
        "std": df["value"].std(),
        "count": len(df)
    }

# Clear specific cache
load_data.clear()

# Clear all caches
st.cache_data.clear()
```

### Caching Resources

```python
import streamlit as st
from sqlalchemy import create_engine

@st.cache_resource
def get_db_engine():
    """Shared database connection pool."""
    return create_engine(
        st.secrets["database"]["url"],
        pool_size=5,
        max_overflow=10
    )

@st.cache_resource
def load_ml_model():
    """Load and cache ML model once."""
    import torch
    model = torch.load("model.pth")
    model.eval()
    return model

@st.cache_resource(ttl=86400)  # Refresh daily
def get_api_client():
    """Cached API client with daily refresh."""
    return APIClient(api_key=st.secrets["api_key"])
```

### Cache Key Customization

```python
import streamlit as st
import pandas as pd
from datetime import date

@st.cache_data
def fetch_daily_data(query: str, _conn, date: date) -> pd.DataFrame:
    """
    Underscore prefix excludes parameter from cache key.
    Connection object won't affect caching.
    """
    return pd.read_sql(query, _conn)

# Custom hash function for unhashable types
def hash_dataframe(df: pd.DataFrame) -> str:
    return pd.util.hash_pandas_object(df).sum()

@st.cache_data(hash_funcs={pd.DataFrame: hash_dataframe})
def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("category").sum()
```

---

## Fragment-Based Optimization

Use `@st.fragment` to create independently updating sections (v1.37+).

### Basic Fragment Usage

```python
import streamlit as st

@st.fragment
def real_time_metrics():
    """This section updates independently."""
    import time

    if st.button("Refresh Metrics", key="refresh_metrics"):
        pass  # Triggers only this fragment

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CPU", f"{get_cpu()}%")
    with col2:
        st.metric("Memory", f"{get_memory()}%")
    with col3:
        st.metric("Disk", f"{get_disk()}%")

@st.fragment
def chart_section():
    """Chart updates don't affect metrics."""
    chart_type = st.selectbox("Chart", ["Line", "Bar"], key="chart_type")
    st.line_chart(get_chart_data())

# Main app - fragments update independently
st.title("Dashboard")
real_time_metrics()
st.divider()
chart_section()
```

### Auto-Refreshing Fragments

```python
import streamlit as st

@st.fragment(run_every=5)  # Auto-refresh every 5 seconds
def live_data_feed():
    """Continuously updating data feed."""
    data = fetch_live_data()
    st.dataframe(data)
    st.caption(f"Last updated: {datetime.now()}")
```

---

## Large Dataset Optimization

### Memory-Efficient Loading

```python
import streamlit as st
import pandas as pd

@st.cache_data
def load_optimized_csv(file_path: str) -> pd.DataFrame:
    """Load CSV with optimized dtypes."""
    # First pass: infer types
    sample = pd.read_csv(file_path, nrows=1000)

    # Define optimal dtypes
    dtype_map = {}
    for col in sample.columns:
        if sample[col].dtype == 'int64':
            if sample[col].min() >= 0 and sample[col].max() <= 255:
                dtype_map[col] = 'uint8'
            elif sample[col].min() >= -128 and sample[col].max() <= 127:
                dtype_map[col] = 'int8'
            else:
                dtype_map[col] = 'int32'
        elif sample[col].dtype == 'float64':
            dtype_map[col] = 'float32'
        elif sample[col].dtype == 'object':
            if sample[col].nunique() / len(sample) < 0.5:
                dtype_map[col] = 'category'

    return pd.read_csv(file_path, dtype=dtype_map)

@st.cache_data
def load_parquet(file_path: str, columns: list = None) -> pd.DataFrame:
    """Load only needed columns from Parquet."""
    return pd.read_parquet(file_path, columns=columns)
```

### Streaming Large Files

```python
import streamlit as st
import pandas as pd

def process_large_csv(uploaded_file, chunk_size=50000):
    """Process large CSV in chunks with progress."""

    # Get total rows for progress
    total_rows = sum(1 for _ in uploaded_file) - 1
    uploaded_file.seek(0)

    progress = st.progress(0)
    status = st.empty()

    results = []
    for i, chunk in enumerate(pd.read_csv(uploaded_file, chunksize=chunk_size)):
        # Process chunk
        processed = process_chunk(chunk)
        results.append(processed)

        # Update progress
        progress.progress(min((i + 1) * chunk_size / total_rows, 1.0))
        status.text(f"Processed {min((i + 1) * chunk_size, total_rows):,} / {total_rows:,} rows")

    progress.empty()
    status.empty()

    return pd.concat(results, ignore_index=True)
```

### Pagination for Display

```python
import streamlit as st
import pandas as pd

def paginated_dataframe(df: pd.DataFrame, page_size: int = 100):
    """Display large DataFrame with pagination."""

    total_rows = len(df)
    total_pages = (total_rows - 1) // page_size + 1

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        page = st.number_input(
            f"Page (1-{total_pages})",
            min_value=1,
            max_value=total_pages,
            value=1,
            key="page_selector"
        )

    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total_rows)

    st.dataframe(df.iloc[start_idx:end_idx])
    st.caption(f"Showing rows {start_idx + 1:,} to {end_idx:,} of {total_rows:,}")
```

---

## Visualization Optimization

### Altair Performance

```python
import streamlit as st
import altair as alt
import pandas as pd

# Enable VegaFusion for server-side aggregation
alt.data_transformers.enable('vegafusion')

@st.cache_data
def create_optimized_chart(df: pd.DataFrame) -> alt.Chart:
    """Create chart with server-side aggregation."""

    # Pre-aggregate data for large datasets
    if len(df) > 10000:
        df = df.groupby(['category', pd.Grouper(key='date', freq='D')]).agg({
            'value': 'mean'
        }).reset_index()

    chart = alt.Chart(df).mark_line().encode(
        x='date:T',
        y='value:Q',
        color='category:N'
    ).properties(
        width='container',
        height=400
    )

    return chart
```

### Plotly Performance

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def create_optimized_scatter(df, x, y, color=None):
    """Create WebGL-rendered scatter plot for large datasets."""

    fig = px.scatter(
        df, x=x, y=y, color=color,
        render_mode='webgl'  # GPU acceleration
    )

    fig.update_traces(
        marker=dict(size=3, opacity=0.6),
        hoverinfo='skip'  # Disable hover for performance
    )

    fig.update_layout(
        transition_duration=0,  # Disable animations
        uirevision='constant'  # Preserve zoom/pan state
    )

    return fig

# Display with minimal config
st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        'displayModeBar': False,
        'staticPlot': False
    }
)
```

### Downsampling Strategies

```python
import streamlit as st
import pandas as pd
import numpy as np

def downsample_for_viz(df: pd.DataFrame, max_points: int = 5000) -> pd.DataFrame:
    """Intelligent downsampling preserving data distribution."""

    if len(df) <= max_points:
        return df

    # Method 1: Random sampling
    # return df.sample(n=max_points, random_state=42)

    # Method 2: LTTB (Largest Triangle Three Buckets)
    # Preserves visual shape better
    return lttb_downsample(df, max_points)

def lttb_downsample(df: pd.DataFrame, n_points: int) -> pd.DataFrame:
    """LTTB algorithm for time series downsampling."""
    # Implementation of LTTB algorithm
    # ... (see lttb library)
    pass
```

---

## Session State Optimization

### Efficient State Management

```python
import streamlit as st

# Initialize state efficiently
def init_state():
    """Initialize all session state at once."""
    defaults = {
        "user_settings": {"theme": "light", "page_size": 50},
        "filters": {"date_range": None, "categories": []},
        "cache": {}
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Avoid recomputation with state
def get_or_compute(key: str, compute_fn: callable):
    """Compute once and store in session state."""
    if key not in st.session_state:
        st.session_state[key] = compute_fn()
    return st.session_state[key]

# Usage
data = get_or_compute("processed_data", lambda: expensive_processing(raw_data))
```

### State Serialization for Large Objects

```python
import streamlit as st
import pickle
import tempfile
import os

def store_large_object(key: str, obj):
    """Store large object to temp file, keep path in state."""
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, f"st_state_{key}.pkl")

    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)

    st.session_state[f"_path_{key}"] = file_path

def retrieve_large_object(key: str):
    """Retrieve large object from temp file."""
    path_key = f"_path_{key}"
    if path_key not in st.session_state:
        return None

    with open(st.session_state[path_key], 'rb') as f:
        return pickle.load(f)
```

---

## Network Optimization

### Minimizing Data Transfer

```python
import streamlit as st
import pandas as pd

# Only send visible columns
def display_subset(df: pd.DataFrame, display_cols: list):
    """Display only selected columns to reduce transfer."""
    st.dataframe(df[display_cols])

# Use native types for smaller payloads
@st.cache_data
def prepare_for_display(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare DataFrame for efficient display."""
    df = df.copy()

    # Round floats to reduce precision
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = df[col].round(2)

    # Convert datetime to string for smaller transfer
    for col in df.select_dtypes(include=['datetime']).columns:
        df[col] = df[col].dt.strftime('%Y-%m-%d')

    return df
```

### Lazy Loading

```python
import streamlit as st

def lazy_load_section(section_name: str, render_fn: callable):
    """Only render section when expanded."""

    with st.expander(section_name, expanded=False):
        if st.session_state.get(f"expanded_{section_name}", False):
            render_fn()
        else:
            if st.button("Load Content", key=f"load_{section_name}"):
                st.session_state[f"expanded_{section_name}"] = True
                st.rerun()
```

---

## Profiling and Debugging

### Built-in Profiling

```python
import streamlit as st
import time

class Timer:
    """Context manager for timing code blocks."""

    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        elapsed = time.perf_counter() - self.start
        if "timings" not in st.session_state:
            st.session_state.timings = {}
        st.session_state.timings[self.name] = elapsed

# Usage
with Timer("data_loading"):
    df = load_data()

with Timer("chart_rendering"):
    st.plotly_chart(fig)

# Display timings in sidebar
with st.sidebar:
    if st.checkbox("Show Performance"):
        for name, elapsed in st.session_state.get("timings", {}).items():
            st.text(f"{name}: {elapsed:.3f}s")
```

### Memory Profiling

```python
import streamlit as st
import sys

def get_size(obj):
    """Get memory size of object."""
    return sys.getsizeof(obj)

def memory_report():
    """Display memory usage of session state."""
    st.subheader("Memory Usage")

    for key, value in st.session_state.items():
        size = get_size(value)
        if size > 1_000_000:  # > 1MB
            st.warning(f"{key}: {size / 1_000_000:.2f} MB")
        else:
            st.text(f"{key}: {size / 1_000:.2f} KB")
```

---

## Performance Checklist

- [ ] All data loading functions use `@st.cache_data`
- [ ] Database connections use `@st.cache_resource`
- [ ] ML models loaded with `@st.cache_resource`
- [ ] Large datasets are paginated or downsampled
- [ ] Charts use WebGL rendering for large datasets
- [ ] Independent sections use `@st.fragment`
- [ ] Session state initialized efficiently
- [ ] Only necessary columns sent to browser
- [ ] Appropriate TTL set for cached data
- [ ] Forms used to batch user inputs
