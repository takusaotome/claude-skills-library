# Streamlit Data Visualization Best Practices

Comprehensive guide to choosing and optimizing visualization libraries in Streamlit.

## Library Comparison Matrix

| Library | Interactivity | Performance | Customization | Learning Curve | Best For |
|---------|--------------|-------------|---------------|----------------|----------|
| Native Streamlit | Basic | Excellent | Limited | Easy | Quick KPIs, simple charts |
| Plotly | Excellent | Good | Excellent | Medium | Interactive dashboards |
| Altair | Good | Very Good | Good | Medium | Statistical visualization |
| Matplotlib | None | Fair | Excellent | Medium | Publication-quality |
| Seaborn | None | Fair | Good | Easy | Statistical plots |
| PyDeck | Excellent | Excellent | Good | Hard | Geospatial/3D |
| Bokeh | Excellent | Good | Good | Hard | Interactive plots |

---

## Native Streamlit Charts

Best for: Quick visualizations, prototyping, KPIs.

### Available Chart Types

```python
import streamlit as st
import pandas as pd
import numpy as np

# Sample data
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=100),
    'value1': np.random.randn(100).cumsum(),
    'value2': np.random.randn(100).cumsum()
})

# Line chart
st.line_chart(df.set_index('date'))

# Area chart
st.area_chart(df.set_index('date'))

# Bar chart
st.bar_chart(df.set_index('date'))

# Scatter chart (v1.47+)
st.scatter_chart(df, x='value1', y='value2')
```

### Customization Options

```python
import streamlit as st

st.line_chart(
    df,
    x='date',
    y=['value1', 'value2'],
    color=['#FF4B4B', '#0068C9'],  # Custom colors
    width=800,                      # Fixed width (v1.50+)
    height=400,                     # Fixed height
    use_container_width=True        # Responsive width
)
```

### When to Use Native Charts

- Prototyping and quick exploration
- Simple KPI displays
- When external dependencies should be minimized
- Real-time data with frequent updates

---

## Plotly

Best for: Interactive dashboards, complex visualizations.

### Basic Usage

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Plotly Express (simple API)
fig = px.scatter(
    df, x='x', y='y',
    color='category',
    size='value',
    hover_data=['name']
)
st.plotly_chart(fig, use_container_width=True)

# Plotly Graph Objects (full control)
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['x'], y=df['y'], mode='lines+markers'))
fig.update_layout(title='My Chart', xaxis_title='X', yaxis_title='Y')
st.plotly_chart(fig)
```

### Performance Optimization

```python
import streamlit as st
import plotly.express as px

# Use WebGL for large datasets (>1000 points)
fig = px.scatter(df, x='x', y='y', render_mode='webgl')

# Reduce hover data
fig.update_traces(hoverinfo='skip')  # or 'x+y' for minimal

# Disable animations
fig.update_layout(transition_duration=0)

# Preserve zoom/pan state on rerun
fig.update_layout(uirevision='constant')

# Optimized display
st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        'scrollZoom': True
    }
)
```

### Common Chart Types

```python
import plotly.express as px

# Line chart with multiple traces
fig = px.line(df, x='date', y=['value1', 'value2'], title='Time Series')

# Bar chart with grouping
fig = px.bar(df, x='category', y='value', color='subcategory', barmode='group')

# Histogram
fig = px.histogram(df, x='value', nbins=50, marginal='box')

# Box plot
fig = px.box(df, x='category', y='value', points='outliers')

# Heatmap
fig = px.imshow(correlation_matrix, text_auto=True, aspect='auto')

# Sunburst / Treemap
fig = px.sunburst(df, path=['region', 'country', 'city'], values='sales')

# 3D Scatter
fig = px.scatter_3d(df, x='x', y='y', z='z', color='category')
```

### Subplots and Facets

```python
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Faceted charts
fig = px.scatter(df, x='x', y='y', facet_col='category', facet_row='year')

# Custom subplots
fig = make_subplots(rows=2, cols=2, subplot_titles=['A', 'B', 'C', 'D'])
fig.add_trace(go.Scatter(x=x, y=y1), row=1, col=1)
fig.add_trace(go.Bar(x=x, y=y2), row=1, col=2)
fig.add_trace(go.Pie(values=values), row=2, col=1)
fig.add_trace(go.Heatmap(z=z), row=2, col=2)
fig.update_layout(height=600)
```

---

## Altair

Best for: Statistical visualization, declarative grammar.

### Basic Usage

```python
import streamlit as st
import altair as alt
import pandas as pd

chart = alt.Chart(df).mark_point().encode(
    x='x:Q',
    y='y:Q',
    color='category:N',
    tooltip=['name', 'value']
).properties(
    width='container',
    height=400
).interactive()

st.altair_chart(chart, use_container_width=True)
```

### Handling Large Datasets

```python
import altair as alt

# Method 1: Disable row limit (use cautiously)
alt.data_transformers.disable_max_rows()

# Method 2: Use data URL transformer
alt.data_transformers.enable('default', max_rows=None)

# Method 3: Server-side aggregation with VegaFusion
# pip install vegafusion vegafusion-python-embed
alt.data_transformers.enable('vegafusion')

# Method 4: Pre-aggregate in Python
@st.cache_data
def prepare_altair_data(df, max_rows=5000):
    if len(df) <= max_rows:
        return df
    return df.sample(n=max_rows, random_state=42)
```

### Common Chart Types

```python
import altair as alt

# Line chart
line = alt.Chart(df).mark_line().encode(
    x='date:T',
    y='value:Q',
    color='series:N'
)

# Bar chart
bar = alt.Chart(df).mark_bar().encode(
    x='category:N',
    y='count():Q',
    color='subcategory:N'
)

# Scatter with regression
points = alt.Chart(df).mark_point().encode(x='x', y='y')
line = points.transform_regression('x', 'y').mark_line(color='red')
chart = points + line

# Histogram with density
hist = alt.Chart(df).mark_bar().encode(
    alt.X('value:Q', bin=alt.Bin(maxbins=50)),
    y='count()'
)

# Heatmap
heatmap = alt.Chart(df).mark_rect().encode(
    x='month:O',
    y='day:O',
    color='value:Q'
)

# Boxplot
box = alt.Chart(df).mark_boxplot().encode(
    x='category:N',
    y='value:Q'
)
```

### Layering and Concatenation

```python
import altair as alt

# Layer (overlay charts)
base = alt.Chart(df).encode(x='date:T')
line = base.mark_line().encode(y='value:Q')
points = base.mark_point().encode(y='value:Q')
layered = line + points

# Horizontal concatenation
chart1 | chart2

# Vertical concatenation
chart1 & chart2

# Faceting
chart.facet(column='category:N', row='year:O')
```

### Interactive Selection

```python
import altair as alt

# Brush selection
brush = alt.selection_interval()

chart = alt.Chart(df).mark_point().encode(
    x='x:Q',
    y='y:Q',
    color=alt.condition(brush, 'category:N', alt.value('lightgray'))
).add_params(brush)

# Linked charts
brush = alt.selection_interval()

scatter = alt.Chart(df).mark_point().encode(
    x='x:Q', y='y:Q',
    color=alt.condition(brush, 'category:N', alt.value('lightgray'))
).add_params(brush)

bars = alt.Chart(df).mark_bar().encode(
    x='category:N',
    y='count()',
    color='category:N'
).transform_filter(brush)

chart = scatter | bars
```

---

## Matplotlib/Seaborn

Best for: Publication-quality static visualizations.

### Basic Usage

```python
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['x'], df['y'])
ax.set_title('My Chart')
ax.set_xlabel('X')
ax.set_ylabel('Y')
st.pyplot(fig)
plt.close()  # Important: close figure to free memory

# Seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df, x='x', y='y', hue='category', ax=ax)
st.pyplot(fig)
plt.close()
```

### Performance Considerations

```python
import streamlit as st
import matplotlib.pyplot as plt

# Cache figure creation
@st.cache_data
def create_matplotlib_figure(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data['x'], data['y'])
    return fig

fig = create_matplotlib_figure(df)
st.pyplot(fig)

# Use Agg backend for server-side rendering
import matplotlib
matplotlib.use('Agg')
```

### Common Seaborn Charts

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Pairplot (correlation matrix)
fig = sns.pairplot(df, hue='category')
st.pyplot(fig)

# Heatmap
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Violin plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.violinplot(data=df, x='category', y='value', ax=ax)
st.pyplot(fig)

# Joint plot
g = sns.jointplot(data=df, x='x', y='y', kind='hex')
st.pyplot(g.fig)
```

---

## PyDeck (Geospatial)

Best for: Maps, geospatial data, 3D visualization.

### Basic Usage

```python
import streamlit as st
import pydeck as pdk

# Simple scatter map
layer = pdk.Layer(
    'ScatterplotLayer',
    data=df,
    get_position='[longitude, latitude]',
    get_color='[200, 30, 0, 160]',
    get_radius=200,
    pickable=True
)

view_state = pdk.ViewState(
    latitude=df['latitude'].mean(),
    longitude=df['longitude'].mean(),
    zoom=11,
    pitch=50
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={'text': '{name}'}
))
```

### Common Layer Types

```python
import pydeck as pdk

# Hexagon layer (aggregation)
hex_layer = pdk.Layer(
    'HexagonLayer',
    data=df,
    get_position='[longitude, latitude]',
    radius=100,
    elevation_scale=4,
    elevation_range=[0, 1000],
    extruded=True
)

# Path layer
path_layer = pdk.Layer(
    'PathLayer',
    data=routes,
    get_path='path',
    get_color='[255, 0, 0]',
    width_scale=10
)

# GeoJSON layer
geojson_layer = pdk.Layer(
    'GeoJsonLayer',
    data=geojson_url,
    filled=True,
    get_fill_color='[0, 100, 200, 100]'
)

# 3D columns
column_layer = pdk.Layer(
    'ColumnLayer',
    data=df,
    get_position='[longitude, latitude]',
    get_elevation='value',
    elevation_scale=100,
    get_fill_color='[255, 140, 0]',
    radius=50
)
```

---

## Chart Selection Guide

### By Data Type

| Data Type | Recommended | Alternative |
|-----------|-------------|-------------|
| Time series | Plotly line, Altair line | Native line_chart |
| Categorical comparison | Plotly bar, Altair bar | Native bar_chart |
| Distribution | Plotly histogram, Seaborn | Altair histogram |
| Correlation | Seaborn heatmap | Plotly heatmap |
| Part-to-whole | Plotly pie/sunburst | Altair arc |
| Geospatial | PyDeck | Plotly scatter_mapbox |
| Statistical | Seaborn, Altair | Plotly |

### By Audience

| Audience | Recommended | Reason |
|----------|-------------|--------|
| Data scientists | Altair, Seaborn | Statistical rigor |
| Business users | Plotly | Interactivity |
| General public | Native, Plotly | Simplicity |
| Publications | Matplotlib, Seaborn | Customization |

### By Dataset Size

| Size | Recommended | Strategy |
|------|-------------|----------|
| < 1,000 rows | Any | Direct plotting |
| 1,000-10,000 | Plotly, Altair | Consider aggregation |
| 10,000-100,000 | Plotly WebGL | Pre-aggregation required |
| > 100,000 | PyDeck, sampling | Streaming/chunking |

---

## Theming and Styling

### Streamlit Theme Integration

```python
import streamlit as st
import plotly.io as pio

# Detect and apply Streamlit theme
if st.context.theme == "dark":
    pio.templates.default = "plotly_dark"
else:
    pio.templates.default = "plotly_white"
```

### Custom Color Palettes

```python
import streamlit as st

# Define consistent color palette
COLORS = {
    'primary': '#FF4B4B',
    'secondary': '#0068C9',
    'success': '#09AB3B',
    'warning': '#FACA2B',
    'error': '#FF2B2B',
    'neutral': '#808495'
}

CATEGORICAL_COLORS = [
    '#FF4B4B', '#0068C9', '#09AB3B',
    '#FACA2B', '#7D4CDB', '#00D4AA'
]

# Apply to Plotly
fig.update_layout(colorway=CATEGORICAL_COLORS)

# Apply to Altair
alt.Chart(df).mark_bar().encode(
    color=alt.Color('category:N', scale=alt.Scale(range=CATEGORICAL_COLORS))
)
```

---

## Accessibility Guidelines

1. **Color contrast**: Ensure 4.5:1 ratio for text, 3:1 for graphics
2. **Color-blind friendly**: Use color + shape/pattern
3. **Labels**: Always label axes and provide legends
4. **Alt text**: Use `st.caption()` for chart descriptions
5. **Font size**: Minimum 12px for labels

```python
import plotly.express as px

fig = px.scatter(df, x='x', y='y', color='category', symbol='category')  # Shape + color
fig.update_layout(
    font=dict(size=14),
    legend=dict(title='Category', font=dict(size=12))
)
st.plotly_chart(fig)
st.caption("Scatter plot showing relationship between X and Y variables by category")
```
