import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# Load the data
df = pd.read_csv('CCRB-Complaint-Data_202007271729/allegations_202007271729.csv')
df['is_substantiated'] = df['board_disposition'].str.contains('Substantiated', na=False)

# Calculate yearly statistics (2000-2019)
yearly_stats = df[(df['year_received'] >= 2000) & (df['year_received'] <= 2019)].groupby('year_received').agg({
    'complaint_id': 'count',
    'is_substantiated': ['sum', 'mean']
}).reset_index()

yearly_stats.columns = ['year', 'total_allegations', 'substantiated_count', 'substantiation_rate']
yearly_stats['substantiation_rate'] = yearly_stats['substantiation_rate'] * 100

##############################################################################
# VISUALIZATION 1: FOR THE PROPOSITION
# "NYPD accountability has significantly improved since 2010"
##############################################################################

# DECEPTIVE TECHNIQUE 1: Cherry-pick the timeframe (2010-2019, excluding the dip in 2017)
# and use a TRUNCATED Y-AXIS starting at 15% instead of 0%
for_data = yearly_stats[yearly_stats['year'] >= 2010].copy()

# DECEPTIVE TECHNIQUE 2: Apply non-linear smoothing to exaggerate the upward trend
# Using a polynomial fit to create an upward trajectory
z = np.polyfit(for_data['year'], for_data['substantiation_rate'], 2)
p = np.poly1d(z)
for_data['trend'] = p(for_data['year'])

fig1 = go.Figure()

# Add area chart for dramatic effect (makes increases look more substantial)
fig1.add_trace(go.Scatter(
    x=for_data['year'],
    y=for_data['substantiation_rate'],
    mode='lines+markers',
    name='Substantiation Rate',
    line=dict(color='#2ecc71', width=4),
    marker=dict(size=12, symbol='circle', line=dict(color='white', width=2)),
    fill='tozeroy',
    fillcolor='rgba(46, 204, 113, 0.3)',
    hovertemplate='<b>Year %{x}</b><br>Substantiation Rate: %{y:.1f}%<extra></extra>'
))

# Add trend line
fig1.add_trace(go.Scatter(
    x=for_data['year'],
    y=for_data['trend'],
    mode='lines',
    name='Upward Trend',
    line=dict(color='#27ae60', width=3, dash='dash'),
    hovertemplate='<b>Trend: %{y:.1f}%</b><extra></extra>'
))

# DECEPTIVE TECHNIQUE 3: Aspirational annotation emphasizing the peak
fig1.add_annotation(
    x=2015,
    y=35.12,
    text="<b>Record High: 35%</b><br>Accountability Peak",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="#27ae60",
    ax=-80,
    ay=-60,
    font=dict(size=14, color="#27ae60", family="Arial Black"),
    bordercolor="#27ae60",
    borderwidth=2,
    borderpad=6,
    bgcolor="#e8f8f5"
)

# Highlight improvement from 2010 to 2019
fig1.add_annotation(
    x=2010,
    y=17.5,
    text="2010: 17.5%",
    showarrow=False,
    font=dict(size=11, color="#95a5a6"),
    yshift=-20
)

fig1.add_annotation(
    x=2019,
    y=30.9,
    text="<b>2019: 30.9%</b><br><i>+76% increase</i>",
    showarrow=True,
    arrowhead=2,
    ax=40,
    ay=-40,
    font=dict(size=12, color="#27ae60"),
    bordercolor="#27ae60",
    borderwidth=1,
    borderpad=4,
    bgcolor="#e8f8f5"
)

fig1.update_layout(
    title={
        'text': '<b>Rising Accountability:</b> NYPD Complaint Substantiation Rates Show Major Improvement',
        'font': {'size': 22, 'color': '#2c3e50', 'family': 'Arial Black'},
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis=dict(
        title=dict(text='<b>Year</b>', font=dict(size=16)),
        tickfont=dict(size=13),
        gridcolor='#ecf0f1',
        showgrid=True,
        dtick=1
    ),
    yaxis=dict(
        title=dict(text='<b>Substantiation Rate (%)</b>', font=dict(size=16)),
        tickfont=dict(size=13),
        gridcolor='#ecf0f1',
        showgrid=True,
        range=[15, 37],  # TRUNCATED AXIS - doesn't start at 0!
        ticksuffix='%'
    ),
    plot_bgcolor='white',
    paper_bgcolor='#f8f9fa',
    hovermode='x unified',
    showlegend=True,
    legend=dict(
        x=0.02,
        y=0.98,
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='#bdc3c7',
        borderwidth=1
    ),
    height=600,
    margin=dict(t=100, b=80, l=80, r=40)
)

# Add source note (appears credible but cherry-picked data)
fig1.add_annotation(
    xref="paper", yref="paper",
    x=0, y=-0.12,
    text="<i>Source: NYC Civilian Complaint Review Board (CCRB) Data, 2010-2019</i>",
    showarrow=False,
    font=dict(size=10, color="#7f8c8d"),
    xanchor='left'
)

fig1.write_html('visualization_for.html')
print("✓ Created visualization_for.html")

##############################################################################
# VISUALIZATION 2: AGAINST THE PROPOSITION
# "NYPD accountability has NOT significantly improved since 2010"
##############################################################################

# DECEPTIVE TECHNIQUE 1: Use FULL time range (2000-2019) to show volatility
# This makes the recent increase look like just another fluctuation
against_data = yearly_stats.copy()

# DECEPTIVE TECHNIQUE 2: Calculate total complaints (absolute numbers) 
# alongside percentages to show scale
against_data['unsubstantiated_count'] = against_data['total_allegations'] - against_data['substantiated_count']

# Create subplots to show multiple perspectives
fig2 = make_subplots(
    rows=2, cols=1,
    subplot_titles=('Substantiation Rates: High Volatility, No Consistent Improvement', 
                    'The Reality: Most Complaints Still Go Unsubstantiated'),
    vertical_spacing=0.15,
    row_heights=[0.5, 0.5]
)

# Top chart: Show full 20-year view with proper 0-100% scale
fig2.add_trace(go.Scatter(
    x=against_data['year'],
    y=against_data['substantiation_rate'],
    mode='lines+markers',
    name='Substantiation Rate',
    line=dict(color='#e74c3c', width=3),
    marker=dict(size=8, color='#e74c3c'),
    hovertemplate='<b>%{x}</b><br>Rate: %{y:.1f}%<extra></extra>'
), row=1, col=1)

# Add horizontal reference line at mean
mean_rate = against_data['substantiation_rate'].mean()
fig2.add_hline(
    y=mean_rate, 
    line_dash="dash", 
    line_color="#95a5a6",
    annotation_text=f"20-Year Average: {mean_rate:.1f}%",
    annotation_position="right",
    row=1, col=1
)

# Highlight 2017 drop to show it's not consistent improvement
fig2.add_annotation(
    x=2017,
    y=25.3,
    text="<b>2017: Dropped to 25%</b><br>Progress reversed",
    showarrow=True,
    arrowhead=2,
    arrowcolor="#c0392b",
    ax=50,
    ay=40,
    font=dict(size=11, color="#c0392b"),
    bordercolor="#e74c3c",
    borderwidth=1,
    borderpad=4,
    bgcolor="#fadbd8",
    row=1, col=1
)

# Bottom chart: Stacked bar showing substantiated vs unsubstantiated (absolute numbers)
# This visually emphasizes how few are substantiated
fig2.add_trace(go.Bar(
    x=against_data['year'],
    y=against_data['unsubstantiated_count'],
    name='Unsubstantiated/Exonerated',
    marker_color='#95a5a6',
    hovertemplate='<b>%{x}</b><br>Unsubstantiated: %{y}<extra></extra>'
), row=2, col=1)

fig2.add_trace(go.Bar(
    x=against_data['year'],
    y=against_data['substantiated_count'],
    name='Substantiated',
    marker_color='#3498db',
    hovertemplate='<b>%{x}</b><br>Substantiated: %{y}<extra></extra>'
), row=2, col=1)

# Update subplot layouts
fig2.update_xaxes(title_text="<b>Year</b>", title_font=dict(size=14), row=1, col=1, dtick=2, gridcolor='#ecf0f1')
fig2.update_xaxes(title_text="<b>Year</b>", title_font=dict(size=14), row=2, col=1, dtick=2, gridcolor='#ecf0f1')

# CRITICAL: Y-axis starts at 0 (earnest) showing true scale
fig2.update_yaxes(
    title_text="<b>Substantiation Rate (%)</b>",
    title_font=dict(size=14),
    row=1, col=1, 
    range=[0, 40],  # Starts at 0! Shows true proportions
    gridcolor='#ecf0f1',
    ticksuffix='%'
)

fig2.update_yaxes(
    title_text="<b>Number of Allegations</b>",
    title_font=dict(size=14),
    row=2, col=1,
    gridcolor='#ecf0f1'
)

fig2.update_layout(
    title={
        'text': '<b>The Accountability Illusion:</b> NYPD Complaint Substantiation Remains Inconsistent',
        'font': {'size': 22, 'color': '#2c3e50', 'family': 'Arial Black'},
        'x': 0.5,
        'xanchor': 'center'
    },
    barmode='stack',
    plot_bgcolor='white',
    paper_bgcolor='#f8f9fa',
    hovermode='x unified',
    showlegend=True,
    legend=dict(
        x=0.02,
        y=0.48,
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='#bdc3c7',
        borderwidth=1
    ),
    height=900,
    margin=dict(t=100, b=80, l=80, r=40)
)

# Add comprehensive source note
fig2.add_annotation(
    xref="paper", yref="paper",
    x=0, y=-0.08,
    text="<i>Source: NYC Civilian Complaint Review Board (CCRB) Complete Dataset, 2000-2019 | Note: 2020 data incomplete</i>",
    showarrow=False,
    font=dict(size=10, color="#7f8c8d"),
    xanchor='left'
)

# Add annotation about scale
fig2.add_annotation(
    xref="paper", yref="paper",
    x=0.98, y=0.52,
    text="<i>Even at 'record high', 65% of<br>complaints go unsubstantiated</i>",
    showarrow=False,
    font=dict(size=11, color="#7f8c8d", family="Arial"),
    xanchor='right',
    bgcolor='rgba(255,255,255,0.8)',
    bordercolor='#bdc3c7',
    borderwidth=1,
    borderpad=6
)

fig2.write_html('visualization_against.html')
print("✓ Created visualization_against.html")

print("\n" + "="*60)
print("Both visualizations created successfully!")
print("="*60)
print("\nDECEPTIVE TECHNIQUES USED (Intentionally Detectable):")
print("\nFOR Visualization:")
print("  • Truncated Y-axis (starts at 15%, not 0%) - makes growth look steeper")
print("  • Cherry-picked timeframe (2010-2019 only) - hides historical context")
print("  • Area fill under curve - exaggerates visual impact")
print("  • Polynomial trend line - suggests continuous improvement")
print("  • Emphatic language: 'Record High', 'Major Improvement'")
print("\nAGAINST Visualization:")
print("  • Y-axis starts at 0 (earnest) - shows true proportions")
print("  • Full 20-year view - reveals volatility and inconsistency")
print("  • Stacked bars showing raw numbers - emphasizes scale")
print("  • Highlighting the 2017 drop - contradicts 'improvement' narrative")
print("  • Language: 'Illusion', 'Inconsistent' - frames skeptically")
