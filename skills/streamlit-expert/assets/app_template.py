"""
Streamlit Application Template
Production-ready template with authentication, caching, and best practices.

Usage:
    1. Copy this template to your project
    2. Configure .streamlit/secrets.toml
    3. Customize the page functions
    4. Run with: streamlit run app.py
"""

from datetime import datetime
from typing import Optional

import pandas as pd
import streamlit as st

# ============================================================================
# Configuration
# ============================================================================

APP_CONFIG = {
    "page_title": "My Streamlit App",
    "page_icon": ":rocket:",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# ============================================================================
# Page Configuration (MUST be first Streamlit command)
# ============================================================================

st.set_page_config(**APP_CONFIG)

# ============================================================================
# Session State Initialization
# ============================================================================


def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "initialized": True,
        "current_page": "home",
        "user_preferences": {
            "theme": "auto",
            "page_size": 50,
        },
        "data_cache": {},
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


# ============================================================================
# Authentication
# ============================================================================


def check_authentication() -> bool:
    """
    Check if user is authenticated.

    Returns:
        bool: True if authenticated, False otherwise
    """
    # Uncomment below for OIDC authentication
    # return st.user.is_logged_in
    return True  # Remove this line when enabling auth


def show_login_page():
    """Display login page for unauthenticated users."""
    st.title("Welcome")
    st.write("Please sign in to continue.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.login()  # Requires [auth] section in secrets.toml

    st.stop()


def get_current_user() -> Optional[dict]:
    """
    Get current user information.

    Returns:
        dict: User information or None if not authenticated
    """
    if not check_authentication():
        return None

    # Uncomment below for OIDC authentication
    # return {
    #     "name": st.user.name,
    #     "email": st.user.email,
    #     "is_logged_in": st.user.is_logged_in,
    # }

    return {"name": "Guest", "email": "guest@example.com", "is_logged_in": True}


# ============================================================================
# Data Loading (with caching)
# ============================================================================


@st.cache_data(ttl=3600, show_spinner="Loading data...")
def load_data(source: str) -> pd.DataFrame:
    """
    Load and cache data from source.

    Args:
        source: Data source path or identifier

    Returns:
        pd.DataFrame: Loaded data
    """
    # Replace with actual data loading logic
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=100),
            "value": range(100),
            "category": ["A", "B", "C", "D"] * 25,
        }
    )


@st.cache_resource
def get_database_connection():
    """
    Get cached database connection.

    Returns:
        Connection object
    """
    # Replace with actual database connection
    # from sqlalchemy import create_engine
    # return create_engine(st.secrets["database"]["url"])
    return None


# ============================================================================
# Page Components
# ============================================================================


def show_sidebar():
    """Render sidebar navigation and controls."""
    with st.sidebar:
        st.title(APP_CONFIG["page_title"])

        # User info (if authenticated)
        user = get_current_user()
        if user:
            st.write(f"Welcome, {user['name']}")

        st.divider()

        # Navigation
        pages = {
            "home": "Home",
            "dashboard": "Dashboard",
            "settings": "Settings",
        }

        selected = st.radio(
            "Navigation",
            options=list(pages.keys()),
            format_func=lambda x: pages[x],
            label_visibility="collapsed",
        )
        st.session_state.current_page = selected

        st.divider()

        # Logout button (if authenticated)
        if user and user["is_logged_in"]:
            if st.button("Logout", use_container_width=True):
                st.logout()

        # Footer
        st.caption(f"v1.0.0 | {datetime.now().strftime('%Y-%m-%d')}")


def show_home_page():
    """Render home page content."""
    st.title("Home")
    st.write("Welcome to the application!")

    # Quick stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Users", "1,234", "+12%")

    with col2:
        st.metric("Revenue", "$45,678", "+8.5%")

    with col3:
        st.metric("Orders", "890", "-2%")

    with col4:
        st.metric("Satisfaction", "94%", "+1.2%")


def show_dashboard_page():
    """Render dashboard page content."""
    st.title("Dashboard")

    # Filters
    with st.expander("Filters", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            date_range = st.date_input("Date Range", value=(datetime(2024, 1, 1), datetime(2024, 12, 31)))

        with col2:
            categories = st.multiselect("Categories", options=["A", "B", "C", "D"], default=["A", "B"])

    # Load data
    df = load_data("main_data")

    # Apply filters
    if categories:
        df = df[df["category"].isin(categories)]

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Trend Over Time")
        st.line_chart(df.set_index("date")["value"])

    with col2:
        st.subheader("Distribution by Category")
        category_counts = df["category"].value_counts()
        st.bar_chart(category_counts)

    # Data table
    st.subheader("Data")
    st.dataframe(df, use_container_width=True, hide_index=True)


def show_settings_page():
    """Render settings page content."""
    st.title("Settings")

    with st.form("settings_form"):
        st.subheader("Preferences")

        theme = st.selectbox(
            "Theme",
            options=["auto", "light", "dark"],
            index=["auto", "light", "dark"].index(st.session_state.user_preferences["theme"]),
        )

        page_size = st.number_input(
            "Default Page Size",
            min_value=10,
            max_value=100,
            value=st.session_state.user_preferences["page_size"],
        )

        submitted = st.form_submit_button("Save Settings")

        if submitted:
            st.session_state.user_preferences["theme"] = theme
            st.session_state.user_preferences["page_size"] = page_size
            st.success("Settings saved!")


# ============================================================================
# Main Application
# ============================================================================


def main():
    """Main application entry point."""
    # Initialize session state
    init_session_state()

    # Check authentication
    if not check_authentication():
        show_login_page()
        return

    # Render sidebar
    show_sidebar()

    # Route to current page
    page_routes = {
        "home": show_home_page,
        "dashboard": show_dashboard_page,
        "settings": show_settings_page,
    }

    current_page = st.session_state.get("current_page", "home")
    page_function = page_routes.get(current_page, show_home_page)
    page_function()


if __name__ == "__main__":
    main()
