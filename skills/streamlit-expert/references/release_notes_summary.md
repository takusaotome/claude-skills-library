# Streamlit Release Notes Summary (2025)

Key features and changes by version for quick reference.

## Version 1.52.0 (December 2025)

### Major Features

- **`st.datetime_input`**: Combined date and time picker widget
- **Callable download buttons**: `st.download_button(data=callable)` for on-demand generation
- **Audio in chat**: `st.chat_input(accept_audio=True)` enables voice messages

### Notable Additions

- Keyboard shortcuts for buttons
- Query parameters in `st.switch_page` and `st.page_link`
- `st.html` with `unsafe_allow_javascript` parameter
- `st.metric` with `delta_arrow` parameter
- Text alignment in markdown/headings
- Spinners as icons and chat avatars
- Tooltips for `st.badge`
- Null value placeholders in dataframes
- Python 3.14 support
- Vega-Altair 6 support

### Breaking Changes

- `st.bokeh_chart` removed (use custom component)
- Widget identity now based solely on keys

---

## Version 1.51.0 (October 2025)

### Major Features

- **Custom Components v2**: Frameless UI, bidirectional data flow
- **Theme files**: Reusable `.streamlit/themes/` configurations
- **Light/dark simultaneous**: Configure both themes at once
- **`st.space`**: Explicit vertical/horizontal spacing

### Notable Additions

- Code and link text color configuration
- `ProgressColumn` color parameter
- `MultiselectColumn` auto-color inheritance
- `st.feedback` default value support
- Width parameters for chart types

### Breaking Changes

- Python 3.9 support ended

---

## Version 1.50.0 (September 2025)

### Major Features

- **`MultiselectColumn`**: Colorful, editable list columns in data editor
- **Color palette configuration**: Precise shade control
- **`st.bar_chart` sorting**: Sort bars by value

### Notable Changes

- Widget identity transitions to key-based system
- Chart column color configuration
- `st.metric` supports `decimal.Decimal`
- `st.audio_input` sample rate customization

### Deprecations

- `st.plotly_chart` `**kwargs` deprecated (use `config=`)

---

## Version 1.49.0 (August 2025)

### Major Features

- **`st.pdf`**: Native PDF rendering
- **Cell selections**: Dataframe cell click detection
- **Sparklines in metrics**: `st.metric(sparkline=data)`
- **Editable `ListColumn`**: Edit lists in data editor
- **Directory uploads**: `st.file_uploader(type="directory")`

### Deprecations

- `st.bokeh_chart` deprecated

---

## Version 1.48.0 (August 2025)

### Major Features

- **Horizontal flex containers**: Row layouts with alignment and gap configuration

```python
with st.horizontal():
    st.button("A")
    st.button("B")
    st.button("C")
```

---

## Version 1.47.0 (July 2025)

### Major Features

- Eight new theming configuration options
- Font customization
- Dataframe header styling
- Link color configuration

---

## Version 1.46.0 (June 2025)

### Major Features

- **Top navigation**: `st.navigation(..., position="top")`
- **Runtime theme detection**: `st.context.theme`
- **Unrestricted container nesting**: Columns in columns, tabs in tabs

```python
# Theme detection
if st.context.theme == "dark":
    # Dark mode specific code
    pass
```

---

## Version 1.45.0 (April 2025)

### Major Features

- **`st.user` GA**: General availability of user information API

```python
st.user.is_logged_in  # bool
st.user.name          # str
st.user.email         # str
```

---

## Version 1.44.0 (March 2025)

### Major Features

- **Advanced theming**: CSS-free theme customization
- **`st.badge`**: Colored badge component
- **`streamlit init`**: CLI project initialization

```python
st.badge("New", color="green")
st.badge("Beta", color="blue")
```

---

## Version 1.43.0 (March 2025)

### Major Features

- **File acceptance in chat**: `st.chat_input(accept_file=True)`
- **`JsonColumn`**: Display JSON objects in data editor

---

## Version 1.42.0 (February 2025)

### Major Features

- **Native authentication**: `st.login()`, `st.logout()`, `st.user`
- OIDC integration with major providers

```python
st.login()  # Redirects to identity provider
st.logout() # Clears session
```

---

## Migration Guide

### From pre-1.42 to 1.42+

1. **Authentication**: Replace third-party auth (streamlit-authenticator) with native
2. **Install**: `pip install "streamlit[auth]"` for Authlib dependency

### From pre-1.45 to 1.45+

1. **User API**: Replace `st.experimental_user` with `st.user`

### From pre-1.50 to 1.50+

1. **Widget keys**: Ensure all stateful widgets have unique keys
2. **Plotly config**: Replace `**kwargs` with `config=` parameter

### From pre-1.51 to 1.51+

1. **Python version**: Upgrade from 3.9 to 3.10+
2. **Custom components**: Consider migrating to v2 API

### From pre-1.52 to 1.52+

1. **Bokeh**: Migrate from `st.bokeh_chart` to custom component

---

## Deprecation Timeline

| Feature | Deprecated | Removed | Replacement |
|---------|-----------|---------|-------------|
| `st.experimental_user` | 1.42 | 1.45 | `st.user` |
| `st.experimental_dialog` | 1.44 | 1.52 | `st.dialog` |
| `st.experimental_fragment` | 1.44 | 1.52 | `st.fragment` |
| `st.bokeh_chart` | 1.49 | 1.52 | Custom component |
| `experimental_allow_widgets` (cache) | 1.44 | 1.52 | Removed |

---

## Feature Availability Matrix

| Feature | Minimum Version | Recommended Version |
|---------|-----------------|---------------------|
| Native authentication | 1.42.0 | 1.52.0+ |
| Fragments | 1.37.0 | 1.52.0+ |
| Multipage apps | 1.10.0 | 1.46.0+ |
| Top navigation | 1.46.0 | 1.52.0+ |
| Theme detection | 1.46.0 | 1.52.0+ |
| Custom Components v2 | 1.51.0 | 1.52.0+ |
| PDF rendering | 1.49.0 | 1.52.0+ |
| Datetime input | 1.52.0 | 1.52.0+ |

---

## Compatibility Notes

### Python Support

| Streamlit Version | Python Versions |
|-------------------|-----------------|
| 1.52.0 | 3.10 - 3.14 |
| 1.51.0 | 3.10 - 3.13 |
| 1.50.0 | 3.9 - 3.13 |
| 1.42.0 | 3.8 - 3.12 |

### Key Dependencies

| Streamlit Version | Altair | Plotly | Pandas |
|-------------------|--------|--------|--------|
| 1.52.0 | 5.x - 6.x | 5.x | 2.x |
| 1.51.0 | 5.x | 5.x | 2.x |
| 1.42.0 | 4.x - 5.x | 5.x | 1.x - 2.x |
