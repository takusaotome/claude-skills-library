"""
Streamlit Data Dashboard Template
Performance-optimized template for data visualization dashboards.

Features:
    - Cached data loading
    - Fragment-based updates
    - Multiple chart libraries (Plotly, Altair, native)
    - Large dataset handling
    - Responsive layout

Usage:
    1. Replace sample data functions with your data sources
    2. Customize chart configurations
    3. Run with: streamlit run dashboard_template.py
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st

# Optional imports (install as needed)
try:
    import plotly.express as px
    import plotly.graph_objects as go

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import altair as alt

    ALTAIR_AVAILABLE = True
except ImportError:
    ALTAIR_AVAILABLE = False

# ============================================================================
# Configuration
# ============================================================================

st.set_page_config(
    page_title="Data Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Dashboard configuration
CONFIG = {
    "refresh_interval": 60,  # seconds
    "default_date_range_days": 30,
    "max_display_rows": 1000,
    "chart_height": 400,
}

# ============================================================================
# Data Loading (with caching)
# ============================================================================


@st.cache_data(ttl=CONFIG["refresh_interval"], show_spinner="Loading data...")
def load_main_data() -> pd.DataFrame:
    """
    Load main dataset with caching.

    Replace this function with your actual data source.
    """
    # Sample data generation
    np.random.seed(42)
    n_rows = 10000

    dates = pd.date_range(end=datetime.now(), periods=n_rows, freq="h")

    df = pd.DataFrame(
        {
            "timestamp": dates,
            "value": np.random.randn(n_rows).cumsum() + 100,
            "volume": np.random.exponential(1000, n_rows),
            "category": np.random.choice(["A", "B", "C", "D"], n_rows),
            "region": np.random.choice(["North", "South", "East", "West"], n_rows),
            "is_active": np.random.choice([True, False], n_rows, p=[0.8, 0.2]),
        }
    )

    return df


@st.cache_data(ttl=CONFIG["refresh_interval"])
def compute_summary_stats(df: pd.DataFrame) -> dict:
    """Compute and cache summary statistics."""
    return {
        "total_records": len(df),
        "active_rate": df["is_active"].mean() * 100,
        "avg_value": df["value"].mean(),
        "total_volume": df["volume"].sum(),
        "categories": df["category"].nunique(),
        "date_range": (df["timestamp"].min(), df["timestamp"].max()),
    }


@st.cache_data
def filter_data(
    df: pd.DataFrame,
    date_range: Tuple[datetime, datetime],
    categories: list,
    regions: list,
) -> pd.DataFrame:
    """Filter data based on user selections."""
    filtered = df.copy()

    # Date filter
    filtered = filtered[
        (filtered["timestamp"].dt.date >= date_range[0]) & (filtered["timestamp"].dt.date <= date_range[1])
    ]

    # Category filter
    if categories:
        filtered = filtered[filtered["category"].isin(categories)]

    # Region filter
    if regions:
        filtered = filtered[filtered["region"].isin(regions)]

    return filtered


# ============================================================================
# Chart Functions
# ============================================================================


def create_kpi_cards(stats: dict):
    """Display KPI metric cards."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Records",
            f"{stats['total_records']:,}",
            help="Total number of records in the filtered dataset",
        )

    with col2:
        st.metric(
            "Active Rate",
            f"{stats['active_rate']:.1f}%",
            delta=f"{stats['active_rate'] - 75:.1f}%" if stats["active_rate"] != 75 else None,
        )

    with col3:
        st.metric(
            "Avg Value",
            f"${stats['avg_value']:,.2f}",
        )

    with col4:
        st.metric(
            "Total Volume",
            f"{stats['total_volume']:,.0f}",
        )


def create_time_series_chart(df: pd.DataFrame, chart_library: str = "native"):
    """Create time series chart using specified library."""
    # Resample data for better performance
    daily = df.groupby(df["timestamp"].dt.date).agg({"value": "mean", "volume": "sum"}).reset_index()
    daily.columns = ["date", "value", "volume"]

    if chart_library == "plotly" and PLOTLY_AVAILABLE:
        fig = px.line(
            daily,
            x="date",
            y="value",
            title="Value Over Time",
        )
        fig.update_layout(
            height=CONFIG["chart_height"],
            xaxis_title="Date",
            yaxis_title="Value",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_library == "altair" and ALTAIR_AVAILABLE:
        chart = (
            alt.Chart(daily)
            .mark_line()
            .encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y("value:Q", title="Value"),
            )
            .properties(height=CONFIG["chart_height"], title="Value Over Time")
        )
        st.altair_chart(chart, use_container_width=True)

    else:
        st.subheader("Value Over Time")
        st.line_chart(daily.set_index("date")["value"], height=CONFIG["chart_height"])


def create_category_chart(df: pd.DataFrame, chart_library: str = "native"):
    """Create category distribution chart."""
    category_stats = df.groupby("category").agg({"value": "mean", "volume": "sum", "timestamp": "count"}).reset_index()
    category_stats.columns = ["category", "avg_value", "total_volume", "count"]

    if chart_library == "plotly" and PLOTLY_AVAILABLE:
        fig = px.bar(
            category_stats,
            x="category",
            y="count",
            color="category",
            title="Records by Category",
        )
        fig.update_layout(height=CONFIG["chart_height"], showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_library == "altair" and ALTAIR_AVAILABLE:
        chart = (
            alt.Chart(category_stats)
            .mark_bar()
            .encode(
                x=alt.X("category:N", title="Category"),
                y=alt.Y("count:Q", title="Count"),
                color="category:N",
            )
            .properties(height=CONFIG["chart_height"], title="Records by Category")
        )
        st.altair_chart(chart, use_container_width=True)

    else:
        st.subheader("Records by Category")
        st.bar_chart(category_stats.set_index("category")["count"], height=CONFIG["chart_height"])


def create_region_chart(df: pd.DataFrame, chart_library: str = "native"):
    """Create regional distribution chart."""
    region_stats = df.groupby("region")["volume"].sum().reset_index()

    if chart_library == "plotly" and PLOTLY_AVAILABLE:
        fig = px.pie(
            region_stats,
            values="volume",
            names="region",
            title="Volume by Region",
        )
        fig.update_layout(height=CONFIG["chart_height"])
        st.plotly_chart(fig, use_container_width=True)

    elif chart_library == "altair" and ALTAIR_AVAILABLE:
        chart = (
            alt.Chart(region_stats)
            .mark_arc()
            .encode(
                theta="volume:Q",
                color="region:N",
            )
            .properties(height=CONFIG["chart_height"], title="Volume by Region")
        )
        st.altair_chart(chart, use_container_width=True)

    else:
        st.subheader("Volume by Region")
        st.bar_chart(region_stats.set_index("region")["volume"], height=CONFIG["chart_height"])


# ============================================================================
# Fragment-Based Components (for partial updates)
# ============================================================================


@st.fragment(run_every=CONFIG["refresh_interval"])
def auto_refresh_metrics(df: pd.DataFrame):
    """Auto-refreshing metrics section."""
    stats = compute_summary_stats(df)
    create_kpi_cards(stats)
    st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")


@st.fragment
def interactive_chart_section(df: pd.DataFrame):
    """Interactive chart section with independent updates."""
    col1, col2 = st.columns([3, 1])

    with col2:
        chart_type = st.selectbox(
            "Chart Type",
            ["Time Series", "Category", "Region"],
            key="chart_type_selector",
        )

        chart_library = st.selectbox(
            "Library",
            ["native", "plotly", "altair"],
            key="chart_library_selector",
        )

    with col1:
        if chart_type == "Time Series":
            create_time_series_chart(df, chart_library)
        elif chart_type == "Category":
            create_category_chart(df, chart_library)
        else:
            create_region_chart(df, chart_library)


# ============================================================================
# Sidebar Filters
# ============================================================================


def render_sidebar_filters(df: pd.DataFrame) -> dict:
    """Render sidebar filter controls and return filter values."""
    with st.sidebar:
        st.header("Filters")

        # Date range
        date_min = df["timestamp"].min().date()
        date_max = df["timestamp"].max().date()
        default_start = date_max - timedelta(days=CONFIG["default_date_range_days"])

        date_range = st.date_input(
            "Date Range",
            value=(max(default_start, date_min), date_max),
            min_value=date_min,
            max_value=date_max,
        )

        # Ensure tuple of two dates
        if len(date_range) != 2:
            date_range = (date_min, date_max)

        st.divider()

        # Category filter
        categories = st.multiselect(
            "Categories",
            options=sorted(df["category"].unique()),
            default=[],
        )

        # Region filter
        regions = st.multiselect(
            "Regions",
            options=sorted(df["region"].unique()),
            default=[],
        )

        st.divider()

        # Reset filters button
        if st.button("Reset Filters", use_container_width=True):
            st.rerun()

        st.divider()

        # Data info
        with st.expander("Data Info"):
            st.write(f"**Total Records:** {len(df):,}")
            st.write(f"**Date Range:** {date_min} to {date_max}")
            st.write(f"**Categories:** {df['category'].nunique()}")
            st.write(f"**Regions:** {df['region'].nunique()}")

    return {
        "date_range": date_range,
        "categories": categories,
        "regions": regions,
    }


# ============================================================================
# Main Application
# ============================================================================


def main():
    """Main dashboard entry point."""
    st.title("Data Dashboard")

    # Load data
    df = load_main_data()

    # Render filters
    filters = render_sidebar_filters(df)

    # Apply filters
    filtered_df = filter_data(
        df,
        filters["date_range"],
        filters["categories"],
        filters["regions"],
    )

    # Check if data exists after filtering
    if filtered_df.empty:
        st.warning("No data matches the selected filters. Please adjust your selections.")
        return

    # KPI Section
    st.subheader("Key Metrics")
    auto_refresh_metrics(filtered_df)

    st.divider()

    # Charts Section
    st.subheader("Analytics")

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Overview", "Detailed Charts", "Data Table"])

    with tab1:
        # Overview with all charts
        col1, col2 = st.columns(2)

        with col1:
            create_time_series_chart(filtered_df, "native")

        with col2:
            create_category_chart(filtered_df, "native")

    with tab2:
        # Interactive chart section
        interactive_chart_section(filtered_df)

    with tab3:
        # Data table with pagination
        st.subheader("Raw Data")

        # Limit rows for display
        display_df = filtered_df.head(CONFIG["max_display_rows"])

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "timestamp": st.column_config.DatetimeColumn("Timestamp", format="YYYY-MM-DD HH:mm"),
                "value": st.column_config.NumberColumn("Value", format="$%.2f"),
                "volume": st.column_config.NumberColumn("Volume", format="%d"),
                "is_active": st.column_config.CheckboxColumn("Active"),
            },
        )

        if len(filtered_df) > CONFIG["max_display_rows"]:
            st.caption(f"Showing {CONFIG['max_display_rows']:,} of {len(filtered_df):,} records")

        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            "Download CSV",
            csv,
            "dashboard_data.csv",
            "text/csv",
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
