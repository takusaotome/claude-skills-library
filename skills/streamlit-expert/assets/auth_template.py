"""
Streamlit Authentication Template
Template for implementing OIDC authentication with multiple providers.

Requirements:
    pip install "streamlit[auth]"

Setup:
    1. Configure your identity provider (Google, Microsoft, Okta, Auth0)
    2. Create .streamlit/secrets.toml with auth configuration
    3. Run with: streamlit run auth_template.py
"""

from functools import wraps
from typing import List, Optional

import streamlit as st

# ============================================================================
# Configuration
# ============================================================================

st.set_page_config(
    page_title="Authenticated App",
    page_icon=":lock:",
    layout="centered",
)

# Role-based access control configuration
ADMIN_EMAILS = [
    "admin@company.com",
]

ALLOWED_DOMAINS = [
    "company.com",
    "partner.com",
]

# ============================================================================
# Authentication Utilities
# ============================================================================


def get_user_email() -> Optional[str]:
    """Get current user's email if authenticated."""
    if st.user.is_logged_in:
        return st.user.email
    return None


def get_user_domain() -> Optional[str]:
    """Get domain from user's email."""
    email = get_user_email()
    if email and "@" in email:
        return email.split("@")[1]
    return None


def is_admin() -> bool:
    """Check if current user is an admin."""
    email = get_user_email()
    return email in ADMIN_EMAILS if email else False


def is_domain_allowed() -> bool:
    """Check if user's domain is in allowed list."""
    domain = get_user_domain()
    if not domain:
        return False
    if not ALLOWED_DOMAINS:  # Empty list means all domains allowed
        return True
    return domain in ALLOWED_DOMAINS


def get_user_role() -> str:
    """Determine user's role based on email."""
    if is_admin():
        return "admin"
    return "user"


# ============================================================================
# Authentication Decorators
# ============================================================================


def require_auth(func):
    """Decorator to require authentication for a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.user.is_logged_in:
            st.warning("Please log in to access this feature.")
            st.stop()
        return func(*args, **kwargs)

    return wrapper


def require_admin(func):
    """Decorator to require admin role for a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_admin():
            st.error("Access denied. Admin privileges required.")
            st.stop()
        return func(*args, **kwargs)

    return wrapper


def require_domain(allowed_domains: List[str]):
    """Decorator factory to require specific domain(s)."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            domain = get_user_domain()
            if domain not in allowed_domains:
                st.error(f"Access denied. Your organization ({domain}) is not authorized.")
                st.stop()
            return func(*args, **kwargs)

        return wrapper

    return decorator


# ============================================================================
# Login UI Components
# ============================================================================


def show_login_single_provider():
    """Show login page for single provider configuration."""
    st.title("Sign In")
    st.write("Please sign in with your company account to continue.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.login()

    st.caption("By signing in, you agree to our Terms of Service and Privacy Policy.")


def show_login_multiple_providers():
    """Show login page for multiple provider configuration."""
    st.title("Sign In")
    st.write("Choose your sign-in method:")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Google")
        st.write("Sign in with your Google account")
        st.login("google")

    with col2:
        st.subheader("Microsoft")
        st.write("Sign in with your Microsoft account")
        st.login("microsoft")

    st.divider()
    st.caption("By signing in, you agree to our Terms of Service and Privacy Policy.")


def show_user_info():
    """Display current user information."""
    if not st.user.is_logged_in:
        st.info("Not signed in")
        return

    st.subheader("User Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Name:**", st.user.name)
        st.write("**Email:**", st.user.email)

    with col2:
        st.write("**Role:**", get_user_role())
        st.write("**Domain:**", get_user_domain())


def show_logout_button():
    """Display logout button."""
    if st.user.is_logged_in:
        if st.button("Sign Out", type="secondary"):
            st.logout()


# ============================================================================
# Protected Content Examples
# ============================================================================


@require_auth
def show_protected_content():
    """Example of protected content requiring authentication."""
    st.subheader("Protected Content")
    st.write("This content is only visible to authenticated users.")
    st.balloons()


@require_admin
def show_admin_panel():
    """Example of admin-only content."""
    st.subheader("Admin Panel")
    st.write("This content is only visible to administrators.")

    with st.expander("User Management"):
        st.write("User management controls would go here...")

    with st.expander("System Settings"):
        st.write("System settings would go here...")


# ============================================================================
# Token Access Examples
# ============================================================================


def show_token_info():
    """
    Display token information (requires expose_tokens in secrets.toml).

    Add to secrets.toml:
        [auth]
        expose_tokens = ["id", "access"]
    """
    st.subheader("Token Information")

    if not st.user.is_logged_in:
        st.info("Sign in to view token information")
        return

    try:
        if hasattr(st.user, "tokens"):
            with st.expander("ID Token (truncated)"):
                id_token = st.user.tokens.id
                st.code(f"{id_token[:50]}..." if id_token else "Not available")

            with st.expander("Access Token (truncated)"):
                access_token = st.user.tokens.access
                st.code(f"{access_token[:50]}..." if access_token else "Not available")
        else:
            st.info("Tokens not exposed. Add expose_tokens to secrets.toml")
    except Exception as e:
        st.warning(f"Could not access tokens: {e}")


def make_api_call_with_token():
    """Example of using access token for API calls."""
    if not st.user.is_logged_in:
        return

    try:
        access_token = st.user.tokens.access

        # Example API call
        # import requests
        # headers = {"Authorization": f"Bearer {access_token}"}
        # response = requests.get("https://api.example.com/data", headers=headers)

        st.success("API call would be made with the access token")
    except Exception as e:
        st.error(f"Could not make API call: {e}")


# ============================================================================
# Main Application
# ============================================================================


def main():
    """Main application entry point."""

    # Check authentication
    if not st.user.is_logged_in:
        # Choose single or multiple provider login
        show_login_single_provider()
        # show_login_multiple_providers()  # Alternative for multiple providers
        st.stop()

    # Validate domain (optional)
    if ALLOWED_DOMAINS and not is_domain_allowed():
        st.error("Access denied. Your organization is not authorized to use this application.")
        show_logout_button()
        st.stop()

    # Main application content
    st.title(f"Welcome, {st.user.name}!")

    # Sidebar with user info and logout
    with st.sidebar:
        show_user_info()
        st.divider()
        show_logout_button()

    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Admin", "Debug"])

    with tab1:
        show_protected_content()

    with tab2:
        if is_admin():
            show_admin_panel()
        else:
            st.info("Admin access required for this section.")

    with tab3:
        show_token_info()


if __name__ == "__main__":
    main()
