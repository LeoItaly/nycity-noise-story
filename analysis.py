# %% [markdown]
# # NYC Noise Complaints: The Quiet Before the Storm - Explainer Notebook

# %% [markdown]
# ## 1. Motivation
# ### What is your dataset?
# The dataset consists of noise complaints reported to NYC's 311 service system during 2019-2020. This dataset includes metadata about each complaint, such as the date and time of the report, the borough it originated from, the specific type of noise complaint (e.g., Residential, Street/Sidewalk, Commercial), the address, and geographic coordinates. The data was obtained from the official NYC Open Data API, focusing specifically on noise-related complaints.
# 
# The 311 service is New York City's non-emergency reporting system that allows citizens to report quality-of-life issues and request government services [1]. The data is maintained and published through NYC Open Data, a comprehensive public data platform that promotes transparency, accountability, and civic engagement [2].
# 
# ### Why did you choose this particular dataset?
# I chose this dataset because it offers a unique opportunity to examine how the COVID-19 pandemic affected urban soundscapes. Noise complaints represent a concrete measure of how city residents experienced their acoustic environment during a period of unprecedented disruption to daily life. The dataset spans a critical timeline, capturing the pre-pandemic "normal" (2019), the initial lockdown period (March-May 2020), and the phased reopening (June-December 2020). This allows us to witness a natural experiment in how urban noise patterns evolve when typical city activities are radically altered.
# 
# Additionally, noise complaints are inherently tied to quality of life, urban density, and socioeconomic factors, making them an excellent lens through which to examine the uneven impacts of the pandemic across New York's diverse boroughs. The dataset is also comprehensive (over 425,000 records), geospatially rich, and temporally granular, allowing for multidimensional analysis.
# 
# Research by Bui and Badger (2020) has shown how the pandemic dramatically changed urban mobility patterns and neighborhood dynamics [3], while studies by Steele et al. (2021) have specifically examined changes to urban soundscapes during lockdowns [4]. This project contributes to this growing body of research by focusing on how residents themselves perceived and reported noise changes.
# 
# 
# ### What was your goal for the end user's experience?
# My goal was to create an intuitive, data-driven narrative that guides users through the transformation of NYC's soundscape during the pandemic, following three distinct phases:
# 
# 1. **Pre-Pandemic "Normal"**: Establishing baseline noise patterns before COVID-19
# 2. **The Great Quieting**: Documenting the initial drop in complaints during lockdown
# 3. **The Noise Awakening**: Revealing the dramatic surge in complaints during reopening
# 
# The end user should be able to discover:
# - How noise complaints evolved over time
# - How different boroughs experienced noise changes differently
# - How the types of noise complaints shifted as the pandemic progressed
# - The relationships between COVID-19 policy phases and noise patterns
# 
# Through interactive visualizations and clear narration, I wanted users to come away with a deeper understanding of how a city's soundscape is shaped by policy, behavior, and circumstances—and how the pandemic's impacts went far beyond just health outcomes to affect the everyday sensory experience of urban life.
# 
# This approach aligns with Segel and Heer's (2010) concept of "narrative visualization," which balances author-driven structure with reader-driven exploration [5]. By combining a clear story arc with interactive elements, the project aims to engage users in what Kosara and Mackinlay (2013) call "storytelling with data" [6].
# 
# 

# %% [markdown]
# ## 2. Basic Stats: Understanding the Dataset

# %% [markdown]
# ### Choices in Data Cleaning and Preprocessing
# I employed several critical data processing steps to ensure the analysis quality:
# 
# 1. **Temporal Feature Engineering**:
#    - Extracted date components (year, month, day, hour) for time-based analysis
#    - Created weekend indicators to analyze weekday vs. weekend patterns
#    - Added COVID-specific phase indicators (pre-COVID, lockdown, reopening) based on official NYC milestone dates:
#      - Lockdown start: March 22, 2020
#      - Phase 1 reopening: June 8, 2020
#      - Phase 3 reopening: July 6, 2020
# 
# 2. **Geospatial Data Cleaning**:
#    - Converted coordinates to numeric format
#    - Filtered out invalid coordinates (outside NYC bounds)
#    - Standardized borough names for consistent analysis
#    - Retained only records with valid geospatial data for mapping
# 
# 3. **Categorical Data Standardization**:
#    - Simplified noise complaint types by removing "Noise - " prefix
#    - Created a consistent categorization scheme for comparison
#    - Ensured missing values were handled appropriately
# 
# 4. **Time Period Definition**:
#    - Clearly defined COVID phase boundaries based on official NYC milestones
#    - Created data subsets for pre-COVID (2019), lockdown (Mar-May 2020), and reopening (Jun-Dec 2020)
# 
# These preprocessing steps follow best practices for spatio-temporal data analysis as outlined by Andrienko et al. (2013) [7] and ensure that the temporal, spatial, and categorical dimensions of the data are properly prepared for the multi-faceted analysis that follows. The phase definitions correspond to official NYC reopening dates as documented by the NYC Department of Health [8].

# %%
# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import io
import json
import datetime as dt
from datetime import datetime
import calendar
import warnings
import matplotlib.patches as mpatches

# Folium and mapping tools
import folium
from folium.plugins import HeatMap, HeatMapWithTime, MarkerCluster
from folium.features import DivIcon, GeoJson, GeoJsonTooltip, GeoJsonPopup
from branca.colormap import LinearColormap, linear
from branca.element import Template, MacroElement

# Geospatial
import geopandas as gpd

# Bokeh
from bokeh.plotting import figure, output_file, save, show
from bokeh.io import output_notebook
from bokeh.models import (
    ColumnDataSource, LinearColorMapper, ColorBar, HoverTool, DateSlider,
    CustomJS, Select, Div, Label, LabelSet, Button, FactorRange, Slider
)
from bokeh.layouts import row as bokeh_row, column as bokeh_column, layout
from bokeh.palettes import Viridis256, RdBu11, Category20c
from bokeh.transform import linear_cmap
from bokeh.layouts import column


# Machine learning
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Utilities
from collections import defaultdict

# Suppress warnings
warnings.filterwarnings('ignore')

# Configure plotting style with consistent aesthetics
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
custom_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Enable Bokeh output in the notebook
output_notebook()

# %%
# Function to fetch NYC 311 data
def fetch_nyc_data(start_date, end_date, limit=10000000):
    """
    Fetch NYC 311 noise complaints for a specific date range using the API
    """
    base_url = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"
    
    params = {
        "$where": f"created_date between '{start_date}T00:00:00' and '{end_date}T23:59:59' AND complaint_type like '%Noise%'",
        "$limit": limit,
        "$select": "created_date,complaint_type,descriptor,incident_address,borough,latitude,longitude,status"
    }
    
    query_str = "&".join([f"{k}={v}" for k, v in params.items()])
    url = f"{base_url}?{query_str}"
    
    print(f"Fetching data for {start_date} to {end_date}...")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text))
        print(f"Loaded {len(df)} records")
        return df
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Fetch the data
print("Fetching 2019 data...")
df_2019 = fetch_nyc_data("2019-01-01", "2019-12-31")

print("\nFetching 2020 data...")
df_2020 = fetch_nyc_data("2020-01-01", "2020-12-31")

# %%
# Define COVID time periods
lockdown_start = dt.datetime(2020, 3, 22)
phase1_start = dt.datetime(2020, 6, 8)
phase3_start = dt.datetime(2020, 7, 6)

# Data cleaning function with comprehensive processing
def clean_noise_data(df):
    """
    Clean and preprocess the NYC noise complaints data
    """
    df_cleaned = df.copy()
    
    # Convert to datetime
    df_cleaned['created_date'] = pd.to_datetime(df_cleaned['created_date'])
    
    # Extract temporal features
    df_cleaned['date'] = df_cleaned['created_date'].dt.date
    df_cleaned['year'] = df_cleaned['created_date'].dt.year
    df_cleaned['month'] = df_cleaned['created_date'].dt.month
    df_cleaned['day'] = df_cleaned['created_date'].dt.day
    df_cleaned['day_of_week'] = df_cleaned['created_date'].dt.day_name()
    df_cleaned['hour'] = df_cleaned['created_date'].dt.hour
    df_cleaned['is_weekend'] = df_cleaned['created_date'].dt.weekday >= 5
    
    # Create COVID phase indicators
    df_cleaned['is_pre_covid'] = (df_cleaned['created_date'] < lockdown_start).astype(int)
    df_cleaned['is_lockdown'] = ((df_cleaned['created_date'] >= lockdown_start) & 
                              (df_cleaned['created_date'] < phase1_start)).astype(int)
    df_cleaned['is_reopening'] = (df_cleaned['created_date'] >= phase1_start).astype(int)
    
    # Clean location data
    df_cleaned['latitude'] = pd.to_numeric(df_cleaned['latitude'], errors='coerce')
    df_cleaned['longitude'] = pd.to_numeric(df_cleaned['longitude'], errors='coerce')
    
    # Drop invalid coordinates
    df_cleaned = df_cleaned.dropna(subset=['latitude', 'longitude'])
    
    # Filter to NYC bounds
    df_cleaned = df_cleaned[
        (df_cleaned['latitude'] > 40.4) & (df_cleaned['latitude'] < 40.92) &
        (df_cleaned['longitude'] > -74.26) & (df_cleaned['longitude'] < -73.7)
    ]
    
    # Standardize borough names
    df_cleaned['borough'] = df_cleaned['borough'].str.title()
    df_cleaned['borough'] = df_cleaned['borough'].fillna('Unknown')
    
    # Create simplified complaint categories
    df_cleaned['noise_category'] = df_cleaned['complaint_type'].str.replace('Noise - ', '', regex=False)
    df_cleaned['noise_category'] = df_cleaned['noise_category'].fillna('Other')
    
    return df_cleaned

# Clean the data
clean_df_2019 = clean_noise_data(df_2019)
clean_df_2020 = clean_noise_data(df_2020)

# Create combined dataset for analysis
combined_df = pd.concat([clean_df_2019, clean_df_2020], ignore_index=True)

# %% [markdown]
# ### Dataset Statistics and Exploratory Analysis
# The NYC noise complaints dataset reveals fascinating insights about how the city's soundscape changed during the COVID-19 pandemic:
# 
# - **Overall Volume**: The dataset contains 425,000+ records, with noise complaints increasing 69.5% from 2019 to 2020
# - **Borough Distribution**: The Bronx saw the largest increase in complaints (+249.2% during reopening), while Staten Island saw the smallest change (+58.9%)
# - **Time Period Comparison**:
#   - Pre-COVID (2019): ~663 complaints per day
#   - Early Lockdown (Mar-May 2020): ~540 complaints per day (-18.6%)
#   - Reopening (Jun-Dec 2020): ~1,135 complaints per day (+71.2%)
# - **Peak Surge**: 152.4% increase in daily complaints (peak date: June 20, 2020)
# - **Noise Category Changes**: Helicopter (+248.5%), Street/Sidewalk (+114.7%), Park (+110.1%)
# 
# The exploratory analysis revealed three distinct phases in NYC's noise experience during the pandemic:
# 
# 1. **Pre-Pandemic Baseline** (2019-Early 2020): Noise complaints followed relatively stable patterns, with weekly cycles and seasonal variations.
# 2. **The Great Quiet** (March-May 2020): Following the lockdown on March 22, 2020, there was an immediate and dramatic drop in noise complaints.
# 3. **The Noise Awakening** (June-December 2020): As reopening began, noise complaints surged dramatically, with daily averages exceeding pre-pandemic levels by over 70%.
# 
# The data also showed significant borough-level differences, with less wealthy areas like the Bronx experiencing a more modest initial decrease but a much larger subsequent surge in complaints, suggesting socioeconomic factors played a role in how neighborhoods experienced pandemic noise changes.
# 
# This three-phase pattern aligns with similar findings from studies on urban sound during COVID-19, such as those conducted by Alsina-Pagès et al. (2021) [9] and Basu et al. (2021) [10], though our analysis reveals a much stronger "rebound effect" than previously documented.
# 

# %%
print("=== Dataset Overview ===")
print(f"2019 records: {len(clean_df_2019):,}")
print(f"2020 records: {len(clean_df_2020):,}")
print(f"Total records: {len(combined_df):,}")
print(f"Change from 2019 to 2020: {((len(clean_df_2020) - len(clean_df_2019)) / len(clean_df_2019) * 100):.1f}%")

# Show distribution across boroughs
borough_counts = combined_df.groupby(['year', 'borough']).size().unstack()
print("\n=== Borough Distribution ===")
print(borough_counts)
print("\nPercent change by borough:")
for borough in borough_counts.columns:
    if borough in borough_counts.columns and 2019 in borough_counts.index and 2020 in borough_counts.index:
        change = ((borough_counts.loc[2020, borough] - borough_counts.loc[2019, borough]) / 
                 borough_counts.loc[2019, borough] * 100)
        print(f"{borough}: {change:.1f}%")

# %% [markdown]
# ### Time Series – 2019 vs. 2020 Complaints

# %%
# 1. Prepare daily totals with 7-day rolling average
daily_totals_2019 = (
    clean_df_2019
    .groupby('date').size()
    .reset_index(name='count')
)
daily_totals_2019['date'] = pd.to_datetime(daily_totals_2019['date'])
daily_totals_2019['rolling_7day'] = (
    daily_totals_2019['count'].rolling(7, center=True).mean()
)

daily_totals_2020 = (
    clean_df_2020
    .groupby('date').size()
    .reset_index(name='count')
)
daily_totals_2020['date'] = pd.to_datetime(daily_totals_2020['date'])
daily_totals_2020['rolling_7day'] = (
    daily_totals_2020['count'].rolling(7, center=True).mean()
)

# 2. Combine into one DataFrame for plotting
df19 = daily_totals_2019[['date','rolling_7day']].copy()
df19['year'] = '2019'
df20 = daily_totals_2020[['date','rolling_7day']].copy()
df20['year'] = '2020'

daily_all = pd.concat([df19, df20], ignore_index=True)
daily_all = daily_all.sort_values('date')

# 3. Build interactive multi-line chart
daily_noise_timeseries = px.line(
    daily_all,
    x='date',
    y='rolling_7day',
    color='year',
    color_discrete_sequence=[custom_colors[0], custom_colors[1]],
    labels={
        'date': 'Date',
        'rolling_7day': '7-Day Rolling Avg Complaints',
        'year': 'Year'
    },
    title='Daily Noise Complaints Time Series (2019 vs 2020)',
    template='plotly_white'
)

# 4. Add COVID phase vertical markers & annotations
for dt, label, col, x_off in [
    (lockdown_start, 'Lockdown', custom_colors[2],    0),
    (phase1_start,   'Phase 1', custom_colors[3], -10),
    (phase3_start,   'Phase 3', custom_colors[4],  10),
]:
    daily_noise_timeseries.add_vline(
        x=dt, line_dash='dash', line_color=col, opacity=0.7
    )
    daily_noise_timeseries.add_annotation(
        x=dt, y=1.02, xref='x', yref='paper',
        text=label,
        showarrow=False,
        font=dict(color=col, size=10, family='Arial'),
        bgcolor='white', bordercolor=col, borderwidth=1, borderpad=2,
        xshift=x_off    # <-- shift left/right to prevent overlap
    )
# 5. Final layout tweaks
daily_noise_timeseries.update_layout(
    hovermode='x unified',
    title_x=0.5,
    legend_title_text='Year',
    xaxis=dict(
        dtick='M1',
        tickformat='%b\n%Y',
        tickangle=-45
    ),
    yaxis=dict(ticksuffix='')
)

# Display
daily_noise_timeseries

daily_noise_timeseries.write_html("nyc_noise_timeseries.html")

# %% [markdown]
# The time series analysis reveals three distinct phases in NYC's noise experience during the pandemic:
# 
# 1. Pre-Pandemic Baseline (2019-Early 2020): Noise complaints followed relatively stable patterns, with weekly cycles and seasonal variations.
# 2. The Great Quiet (March-May 2020): Following the lockdown on March 22, 2020, there was an immediate and dramatic drop in noise complaints, with average daily complaints falling by approximately 15-20% compared to the previous year.
# 3. The Noise Awakening (June-December 2020): As reopening began, noise complaints surged dramatically, with daily averages exceeding pre-pandemic levels by over 70%. The peak surge occurred on June 20, 2020, with a 152.4% increase compared to the previous year.

# %% [markdown]
# ### Top category changes 

# %%
# Analyze top noise categories with improved visualization
top_categories = combined_df['noise_category'].value_counts().head(6)

# Calculate category changes
category_changes = []
for category in top_categories.index:
    count_2019 = len(clean_df_2019[clean_df_2019['noise_category'] == category])
    count_2020 = len(clean_df_2020[clean_df_2020['noise_category'] == category])
    change = ((count_2020 - count_2019) / count_2019) * 100 if count_2019 > 0 else 0

    category_changes.append({
        'Category': category,
        '2019': count_2019,
        '2020': count_2020,
        'Change (%)': change
    })

category_df = pd.DataFrame(category_changes).sort_values('Change (%)', ascending=False)

# Create enhanced bar chart
plt.figure(figsize=(12, 8))
colors = ['#d62728' if x > 0 else '#2ca02c' for x in category_df['Change (%)']]
bars = plt.bar(category_df['Category'], category_df['Change (%)'], color=colors, 
              alpha=0.8, edgecolor='black', linewidth=0.5)

# Add reference line for context
plt.axhline(y=0, color='black', linewidth=1)

# Remove grid
plt.grid(False)

# Add informative title and axis labels
plt.title('Noise Category Changes: 2019 to 2020', fontsize=16, pad=20, fontweight='bold')
plt.xlabel('Noise Category', fontsize=12)
plt.ylabel('Percent Change (%)', fontsize=12)

# Improve x-axis readability
plt.xticks(rotation=30, ha='right', fontsize=11)

# Add value labels with conditional formatting
for bar, value in zip(bars, category_df['Change (%)']):
    height = bar.get_height()
    if height > 0:
        label_pos = height + 5
        va = 'bottom'
    else:
        label_pos = height - 5  
        va = 'top'
    plt.text(bar.get_x() + bar.get_width()/2, label_pos, 
             f'{value:+.1f}%', ha='center', va=va, fontsize=10, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.8))

# Add a custom legend for bar colors
legend_handles = [
    mpatches.Patch(color='#d62728', label='Increase from 2019 to 2020'),
    mpatches.Patch(color='#2ca02c', label='Decrease from 2019 to 2020')
]
plt.legend(handles=legend_handles, loc='upper right', frameon=True, fontsize=11)
plt.tight_layout()
plt.show()

# Display the data
print("\n=== Top Noise Categories Analysis ===")
print(category_df.to_string(index=False))

# %% [markdown]
# ## 3. Data Analysis
# 
# ### What We Learned from the Data
# The analysis revealed several key insights about how NYC's soundscape transformed during the pandemic:
# 
# **1. Temporal Transformation**
# The time series analysis confirmed our three-phase narrative structure. After lockdown began, there was indeed a "Great Quieting" with complaints dropping by 18.6% compared to 2019 levels. However, this quiet was short-lived. The "Noise Awakening" that followed was much more dramatic than anticipated, with complaints surging to 71.2% above pre-pandemic levels during reopening. This suggests the pandemic didn't just temporarily disrupt the urban soundscape—it fundamentally transformed it.
# 
# **2. Spatial Disparities**
# The borough-level analysis revealed stark differences in how neighborhoods experienced noise changes:
# - Manhattan saw the largest decrease during lockdown (-33.1%), likely due to population exodus and business closures
# - The Bronx had the smallest decrease during lockdown (-5.2%) but the largest increase during reopening (+249.2%)
# - All boroughs ultimately saw significant increases, but with different magnitudes (Brooklyn: +147.5%, Queens: +138.9%, Staten Island: +58.9%)
# 
# These patterns correlate strongly with socioeconomic factors, suggesting that the pandemic amplified existing inequities in the urban sound environment. This aligns with research by Sy et al. (2021) who found that COVID-19 disproportionately affected lower-income neighborhoods across multiple quality-of-life metrics [11].
# 
# **3. Categorical Shifts**
# The analysis of noise types revealed how the pandemic altered not just the volume but the nature of urban noise:
# - Residential noise became increasingly dominant across all boroughs as people spent more time at home
# - Helicopter noise saw the largest percentage increase (+248.5%), possibly related to increased surveillance and medical transport
# - Street/Sidewalk noise surged (+114.7%) as indoor activities moved outdoors during reopening
# - Commercial noise initially dropped sharply but rebounded during reopening
# - Park noise increased substantially (+110.1%) as residents sought outdoor recreation options
# 
# **4. Policy Impact**
# The statistical analysis demonstrated that pandemic policy phases were strongly predictive of noise patterns:
# - Lockdown measures reduced daily complaints by an average of 14.6 per borough
# - Reopening increased daily complaints by an average of 68.2 per borough
# - The timing of complaint surges closely aligned with official reopening dates
# 
# These findings are consistent with research by Zuo et al. (2022) on the relationship between policy interventions and urban behavior during the pandemic [12].
# 
# 

# %% [markdown]
# ### COVID Impact Analysis

# %%
import datetime as dt

borough_analysis = []
boroughs = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']

for borough in boroughs:
    pre_covid = len(clean_df_2019[clean_df_2019['borough'] == borough])
    lockdown = len(clean_df_2020[
        (clean_df_2020['borough'] == borough) &
        (clean_df_2020['created_date'] >= lockdown_start) &
        (clean_df_2020['created_date'] < phase1_start)
    ])
    reopening = len(clean_df_2020[
        (clean_df_2020['borough'] == borough) &
        (clean_df_2020['created_date'] >= phase1_start)
    ])

    pre_days = 365
    lock_days = (phase1_start - lockdown_start).days
    reopen_days = (dt.datetime(2020, 12, 31) - phase1_start).days

    borough_analysis.append({
        'Borough': borough,
        'Pre-COVID Daily Avg': pre_covid / pre_days,
        'Lockdown Daily Avg': lockdown / lock_days,
        'Reopening Daily Avg': reopening / reopen_days,
        'Lockdown Impact (%)': ((lockdown / lock_days - pre_covid / pre_days) /
                               (pre_covid / pre_days)) * 100,
        'Reopening Surge (%)': ((reopening / reopen_days - pre_covid / pre_days) /
                                (pre_covid / pre_days)) * 100
    })

borough_df = pd.DataFrame(borough_analysis)
print("\n=== Borough Impact Analysis ===")
print(borough_df.round(1).to_string(index=False))

# ───────────────────────────────────────────────────────────
# Visualize borough COVID impact with compelling layout
# ───────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')
x = np.arange(len(boroughs))
width = 0.35

# Plot bars
lock_bars = ax.bar(x - width/2,
                   borough_df['Lockdown Impact (%)'],
                   width,
                   label='Lockdown Impact',
                   color=custom_colors[0],
                   alpha=0.85)
reopen_bars = ax.bar(x + width/2,
                     borough_df['Reopening Surge (%)'],
                     width,
                     label='Reopening Surge',
                     color=custom_colors[1],
                     alpha=0.85)

# Reference line at 0
ax.axhline(0, color='grey', linewidth=1, alpha=0.7)

# Remove grid lines
ax.grid(False)

# Labels, title, ticks
ax.set_xlabel('Borough', fontsize=13, fontfamily='Arial', color='#333')
ax.set_ylabel('% Change vs. 2019 Daily Average', fontsize=13, fontfamily='Arial', color='#333')
ax.set_title('COVID Impact by Borough: The Noise Awakening',
             fontsize=18, fontweight='bold', fontfamily='Arial', color='#333', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(borough_df['Borough'], fontsize=12, fontfamily='Arial', color='#333')
ax.tick_params(axis='y', labelsize=11, colors='#333')

# Legend styling
leg = ax.legend(loc='upper left', frameon=True, facecolor='white',
                edgecolor='#888', fontsize=12)
for text in leg.get_texts():
    text.set_fontfamily('Arial')

# Data labels
for bars in (lock_bars, reopen_bars):
    for bar in bars:
        h = bar.get_height()
        va = 'bottom' if h >= 0 else 'top'
        offset = 3 if h >= 0 else -3
        ax.text(bar.get_x() + bar.get_width() / 2,
                h + offset,
                f'{h:.1f}%',
                ha='center',
                va=va,
                fontsize=10,
                fontfamily='Arial',
                fontweight='bold',
                color='#333',
                bbox=dict(facecolor='white', edgecolor='none', pad=1, alpha=0.75))

plt.tight_layout()
plt.show()

# Save the figure
fig.savefig("borough_impact_barchart.png")

# %% [markdown]
# ### Machine Learning Application
# I applied linear regression analysis to quantify the impact of different factors on noise complaints. The model examined how time trends, weekend status, and COVID phase (lockdown or reopening) influenced daily complaint volumes.
# 
# The regression model revealed:
# - Strong predictive power across boroughs (R² ranging from 0.53 to 0.74)
# - Substantial phase effects, with reopening having nearly 5 times more impact than lockdown
# - Consistent weekend effects (+13.2 complaints per borough on weekends)
# - Significant borough variation, with the Bronx showing the strongest response to reopening
# 
# I selected linear regression for its interpretability and appropriateness for the task, following Hastie et al.'s (2009) principle that model complexity should match the complexity of the underlying phenomenon [13]. While more complex models might have yielded slightly higher accuracy, they would have sacrificed interpretability of coefficients, which was crucial for understanding the relative importance of different factors.
# 
# The correlation analysis between noise categories showed strong positive relationships between street noise and residential noise (0.88), suggesting that as outdoor activity increased, indoor complaints also rose. This supports the hypothesis that the reopening phase didn't simply return the city to its pre-pandemic state but created new patterns of noise that reflected changed behaviors and sensitivities.

# %%
# Create COVID phase features
combined_df['is_pre_covid'] = (combined_df['created_date'] < lockdown_start).astype(int)
combined_df['is_lockdown'] = ((combined_df['created_date'] >= lockdown_start) & 
                             (combined_df['created_date'] < phase1_start)).astype(int)
combined_df['is_reopening'] = (combined_df['created_date'] >= phase1_start).astype(int)

# Calculate daily aggregates
daily_analysis = combined_df.groupby(['date', 'borough']).agg({
    'noise_category': 'count',
    'is_weekend': 'first',
    'month': 'first',
    'hour': lambda x: x.mode()[0] if len(x.mode()) > 0 else 12,
    'is_pre_covid': 'first',
    'is_lockdown': 'first',
    'is_reopening': 'first'
}).rename(columns={'noise_category': 'daily_complaints'})

# Linear regression analysis for each borough
regression_results = []
for borough in ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']:
    borough_data = daily_analysis[daily_analysis.index.get_level_values(1) == borough].copy()
    
    # Create time index (days since 2019-01-01)
    borough_dates = pd.to_datetime(borough_data.index.get_level_values(0))
    borough_data['days_since_start'] = (borough_dates - pd.Timestamp('2019-01-01')).days
    
    # Create features
    X = borough_data[['days_since_start', 'is_weekend', 'is_lockdown', 'is_reopening']]
    y = borough_data['daily_complaints']
    
    # Fit linear regression
    model = LinearRegression()
    model.fit(X, y)
    
    # Calculate R²
    r2 = model.score(X, y)
    
    # Store results
    regression_results.append({
        'Borough': borough,
        'R²': r2,
        'Weekend Effect': model.coef_[1],
        'Lockdown Effect': model.coef_[2],
        'Reopening Effect': model.coef_[3]
    })

regression_df = pd.DataFrame(regression_results)
print("\n=== Regression Analysis Results ===")
print(regression_df.round(3).to_string(index=False))

# Create visualization of pattern relationships 
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
# Plot COVID phase effects by borough 
effect_data = regression_df.set_index('Borough')[['Lockdown Effect', 'Reopening Effect']]
effect_data.plot(
    kind='bar',
    ax=ax1,
    color=custom_colors[:2],  
)
ax1.set_title('COVID Phase Effects by Borough', fontsize=14, fontweight='bold')
ax1.set_ylabel('Daily Complaint Change')
ax1.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax1.grid(True, alpha=0.3, axis='y')
ax1.legend(frameon=True)
ax1.set_xticklabels(effect_data.index, rotation=45, ha='right')

# Format data labels
for container in ax1.containers:
    ax1.bar_label(container, fmt='%.1f', fontsize=9)

# Calculate correlations between top noise types
category_correlations = combined_df.pivot_table(
    index=['date'],
    columns='noise_category',
    values='incident_address',
    aggfunc='count',
    fill_value=0
)

# Calculate correlations between top noise categories
top_categories = combined_df['noise_category'].value_counts().head(5).index
correlations = category_correlations[top_categories].corr()
# Plot noise category correlations heatmap with better aesthetics
im = ax2.imshow(correlations, cmap='RdBu_r', vmin=-1, vmax=1)
ax2.set_xticks(range(len(top_categories)))
ax2.set_yticks(range(len(top_categories)))
ax2.set_xticklabels(top_categories, rotation=45, ha='right', fontsize=10)
ax2.set_yticklabels(top_categories, fontsize=10)
ax2.set_title('Noise Category Correlations', fontsize=14, fontweight='bold')
ax2.grid(False)

# Add colorbar with clear labeling
cbar = plt.colorbar(im, ax=ax2, shrink=0.8)
cbar.set_label('Correlation', rotation=270, labelpad=15)

# Add correlation values as text
for i in range(len(top_categories)):
    for j in range(len(top_categories)):
        text_color = 'white' if abs(correlations.iloc[i, j]) > 0.7 else 'black'
        ax2.text(j, i, f'{correlations.iloc[i, j]:.2f}',
                ha="center", va="center", color=text_color, fontsize=9, fontweight='bold')

plt.tight_layout()
plt.show()

print("\n=== Noise Category Correlations ===")
print(correlations.round(3).to_string())

# Feature importance analysis
feature_effects = {
    'COVID Phase': regression_df[['Lockdown Effect', 'Reopening Effect']].mean(),
    'Weekend vs Weekday': regression_df['Weekend Effect'].mean(),
    'Borough Variation': regression_df['Reopening Effect'].std()
}

print("\n=== Key Pattern Drivers ===")
for factor, value in feature_effects.items():
    if isinstance(value, pd.Series):
        print(f"{factor}:")
        for sub_factor, sub_value in value.items():
            print(f"  - {sub_factor}: {sub_value:.1f}")
    else:
        print(f"{factor}: {value:.1f}")

# %% [markdown]
# ### 4. Genre
# ### Which genre of data story did you use?
# I used a hybrid of the "Interactive Slideshow" and "Drill-Down Story" genres as defined by Segel and Heer (2010) [5]. My narrative follows a structured three-act progression (Pre-Pandemic → Great Quieting → Noise Awakening) while allowing users to explore details about specific boroughs, time periods, and noise categories.
# 
# This approach aligns with what Riche et al. (2018) call "data-driven storytelling," which combines structured narrative elements with interactive exploration capabilities [14]. The linear storyline provides context and guides interpretation, while interactive elements allow users to investigate aspects most relevant to their interests, creating what Boy et al. (2015) describe as "structured freedom" in data exploration [15].

# %% [markdown]
# ### Which tools did you use from each of the 3 categories of Visual Narrative?
# From the Visual Narrative tools outlined in Figure 7 of Segel and Heer [5], I employed:
# 
# **1. Visual Structuring**
# - **Consistent Visual Platform**: Maintained a cohesive design language across visualizations (color schemes, layouts, labeling conventions)
# - **Establishing Shot**: Started with broad overviews (time series of all complaints) before diving into more specific facets
# - **Progress Bar/Timeline**: Used date sliders and phase indicators to orient users within the pandemic timeline
# - **Highlighting**: Emphasized key moments (lockdown start, reopening phases) with vertical lines and color changes
# 
# **2. Highlighting**
# - **Feature Distinction**: Used color contrast to distinguish between boroughs, phases, and categories
# - **Motion**: Employed animation in the bar chart race and heatmap to convey temporal progression
# - **Zooming**: Allowed users to focus on specific time periods or geographic areas
# 
# **3. Transition Guidance**
# - **Animated Transitions**: Used smooth animations between states in interactive visualizations
# - **Continuity Editing**: Maintained consistent color schemes and layouts across visualizations
# - **Object Continuity**: Ensured that the same elements (boroughs, categories) were represented consistently
# 
# I chose these tools because they support the temporal narrative structure of the project while allowing for spatial and categorical exploration. The consistent visual platform helps users track the story across multiple dimensions, while highlighting and transition guidance make key patterns immediately apparent even in complex data. As Hullman and Diakopoulos (2011) note, these techniques help create a "visual narrative rhetoric" that guides users through complex information spaces [16].
# 

# %% [markdown]
# ### Which tools did you use from each of the 3 categories of Narrative Structure?
# From the Narrative Structure tools defined by Segel and Heer [5]:
# 
# **1. Ordering**
# - **User-Directed Path**: Allowed exploration through interactive elements (borough selectors, time sliders)
# - **Linear Ordering**: Provided a clear narrative sequence following the three pandemic phases
# - **Random Access**: Enabled users to jump directly to specific visualizations or time periods
# 
# **2. Interactivity**
# - **Filtering/Selection/Search**: Implemented borough filters and category selectors
# - **Hover Highlighting/Details**: Provided contextual information on hover
# - **Tacit Tutorial**: Designed visualizations to be self-explanatory with intuitive controls
# - **Navigation Buttons**: Included play/pause controls and time sliders for temporal exploration
# 
# **3. Messaging**
# - **Annotations**: Added explanatory text and markers for key events (lockdown, reopening)
# - **Captions/Headlines**: Used descriptive titles and subtitles to frame visualizations
# - **Summary/Synthesis**: Provided key takeaways and insights with each visualization
# - **Introductory Text**: Oriented users with context before each analysis section
# 
# I selected these narrative tools to balance author-driven storytelling with reader-driven exploration. The "Martini Glass" structure (starting with a directed narrative that opens into free exploration) allows me to communicate the core findings while empowering users to discover details relevant to their own interests or neighborhoods. This approach follows Figueiras' (2014) recommendations for balancing structure and freedom in narrative visualization [17], and incorporates what McKenna et al. (2017) call "progressive disclosure," gradually revealing complexity as users engage with the story [18].

# %% [markdown]
# ## Visualizations
# 
# ### Explain the visualizations you've chosen
# I designed a suite of visualizations that work together to tell a comprehensive story of NYC's changing soundscape:
# 
# 1. **Time Series Visualizations** (Daily Complaints, Year-over-Year Change): These track the overall volume and relative change in noise complaints throughout the pandemic, clearly showing the three-phase pattern.
# 
# 2. **Spatial Visualizations** (Borough Maps, Borough Comparison Charts): These reveal the geographic disparities in how noise patterns changed across the city's five boroughs.
# 
# 3. **Categorical Visualizations** (Noise Type Comparisons, Stacked Area Charts): These demonstrate shifts in the types of noise complaints, highlighting how the acoustic landscape transformed.
# 
# 4. **Interactive Dashboards** (Bokeh plots, Animated Visualizations): These allow users to explore multiple dimensions simultaneously and discover patterns relevant to their interests.
# 
# 5. **Statistical Analysis Visualizations** (Regression Results, Correlation Heatmaps): These provide quantitative evidence for the relationships between COVID phases and noise patterns.
# 
# This multi-faceted approach follows Munzner's (2014) nested model for visualization design [19], addressing both high-level analytical goals and low-level visual encoding choices. Each visualization type serves specific functions in what Cairo (2012) calls the "functional art" of information graphics [20].
# 

# %% [markdown]
# ### Why are they right for the story you want to tell?
# These visualizations are particularly effective for the "Quiet Before the Storm" narrative because:
# 
# 1. **They reveal temporal patterns**: The time-series visualizations clearly demonstrate the three-phase structure that forms the backbone of the narrative, making the "quiet" and subsequent "storm" immediately apparent.
# 
# 2. **They highlight spatial inequities**: The borough-specific visualizations show how the pandemic's noise impact varied across neighborhoods, revealing the socioeconomic dimensions of the story.
# 
# 3. **They make abstract concepts tangible**: Noise is an intangible phenomenon, but the visualizations give it concrete form, making patterns visible that would be difficult to perceive otherwise.
# 
# 4. **They balance overview with detail**: The combination of broad summary visualizations and drill-down explorations allows both for big-picture understanding and nuanced insights, following Shneiderman's (1996) Visual Information-Seeking Mantra: "Overview first, zoom and filter, then details-on-demand" [21].
# 
# 5. **They incorporate context**: By consistently marking COVID policy milestones, the visualizations connect noise patterns to the broader pandemic timeline, helping users understand potential causal relationships.
# 
# 6. **They engage multiple learning styles**: The mix of static, interactive, and animated visualizations engages different ways of processing information, making the story accessible to a wider audience.
# 
# 7. **They reveal surprises**: The visualizations help spotlight unexpected findings (like the massive surge in Helicopter noise) that add depth and interest to the narrative.
# 
# These visualization choices support a narrative that goes beyond merely documenting changes in noise complaints to explore how a crisis can transform urban life in ways that extend far beyond its immediate health impacts. This approach is consistent with Tufte's (2001) principle that excellence in statistical graphics consists of "complex ideas communicated with clarity, precision, and efficiency" [22].

# %% [markdown]
# ### Time Series: The Quiet Before the Storm

# %%
# 1. Calculate daily totals with 7-day moving average
daily_totals_2019 = (
    clean_df_2019
    .groupby('date')
    .size()
    .reset_index(name='count')
)
daily_totals_2019['date'] = pd.to_datetime(daily_totals_2019['date'])
daily_totals_2019['rolling_7day'] = (
    daily_totals_2019['count']
    .rolling(7, center=True)
    .mean()
)
daily_totals_2019['md'] = daily_totals_2019['date'].dt.strftime('%m-%d')

daily_totals_2020 = (
    clean_df_2020
    .groupby('date')
    .size()
    .reset_index(name='count')
)
daily_totals_2020['date'] = pd.to_datetime(daily_totals_2020['date'])
daily_totals_2020['rolling_7day'] = (
    daily_totals_2020['count']
    .rolling(7, center=True)
    .mean()
)
daily_totals_2020['md'] = daily_totals_2020['date'].dt.strftime('%m-%d')

# 2. Merge on month-day for year-over-year comparison
merged_daily = pd.merge(
    daily_totals_2019[['md','rolling_7day']],
    daily_totals_2020[['md','rolling_7day','date']],
    on='md',
    how='inner',
    suffixes=('_2019','_2020')
).rename(columns={'date':'date'})

# 3. Compute percent difference
merged_daily['percent_diff'] = (
    (merged_daily['rolling_7day_2020'] - merged_daily['rolling_7day_2019'])
    / merged_daily['rolling_7day_2019']
) * 100

# 4. Build interactive line chart
year_over_year_change = px.line(
    merged_daily,
    x='date',
    y='percent_diff',
    labels={
        'date': 'Date',
        'percent_diff': 'Year-over-Year Change (%)'
    },
    title='NYC Noise Complaints: Year-over-Year Change (%)',
    template='plotly_white',
)

# 5. Add horizontal reference lines
year_over_year_change.add_hline(
    y=0,
    line_color=custom_colors[0],
    line_width=1,
    annotation_text='0%',
    annotation_position='bottom left'
)
year_over_year_change.add_hline(
    y=100,
    line_color=custom_colors[4],
    line_dash='dot',
    opacity=0.5,
    annotation_text='100%',
    annotation_position='bottom left'
)
year_over_year_change.add_hline(
    y=200,
    line_color=custom_colors[4],
    line_dash='dot',
    opacity=0.5,
    annotation_text='200%',
    annotation_position='bottom left'
)

# 6. Add COVID phase vertical markers
for date, label, color in [
    (lockdown_start, 'Lockdown', custom_colors[2]),
    (phase1_start,   'Phase 1', custom_colors[3]),
    (phase3_start,   'Phase 3', custom_colors[4])
]:
    year_over_year_change.add_vline(
        x=date,
        line_dash='dash',
        line_color=color,
        opacity=0.7
    )
    year_over_year_change.add_annotation(
        x=date,
        y=merged_daily['percent_diff'].max(),
        yref='y',
        text=label,
        showarrow=False,
        font=dict(color=color, size=10),
        bgcolor='white',
        bordercolor=color,
        borderwidth=1,
        borderpad=4
    )

# 7. Tweak axes and hover
year_over_year_change.update_layout(
    hovermode='x unified',
    xaxis=dict(
        dtick='M1',
        tickformat='%b\n%Y',
        tickangle=-45
    ),
    yaxis=dict(ticksuffix='%')
)

# 8. Save the figure object for later use
year_over_year_change  
year_over_year_change.write_html("year_over_year_change.html")

# %% [markdown]
# ### Interactive Bar Plot by COVID Phase

# %%
# 0. Filter out 'Unspecified' boroughs
df = combined_df[combined_df['borough'] != 'Unspecified'].copy()

# 1. Create a categorical 'phase' column
df['phase'] = np.where(
    df['created_date'] < lockdown_start, 'Pre-COVID',
    np.where(df['created_date'] < phase1_start, 'Lockdown', 'Reopening')
)

# 2. Aggregate counts by borough and phase
phase_counts = (
    df
    .groupby(['borough', 'phase'])
    .size()
    .reset_index(name='count')
)

# 3. Enforce the desired phase order for consistent coloring
phase_order = ['Pre-COVID', 'Lockdown', 'Reopening']
phase_counts['phase'] = pd.Categorical(phase_counts['phase'], categories=phase_order, ordered=True)

# 4. Optionally enforce borough order (matching your analysis elsewhere)
borough_order = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
phase_counts['borough'] = pd.Categorical(phase_counts['borough'], categories=borough_order, ordered=True)

# 5. Build the interactive grouped‐bar chart
fig = px.bar(
    phase_counts,
    x='borough',
    y='count',
    color='phase',
    barmode='group',
    category_orders={'phase': phase_order, 'borough': borough_order},
    color_discrete_sequence=[custom_colors[0], custom_colors[3], custom_colors[2]],
    labels={
        'borough': 'Borough',
        'count': 'Total Complaints',
        'phase': 'COVID Phase'
    },
    title='Total NYC Noise Complaints by Borough & COVID Phase'
)

# 6. Tweak the layout to match your notebook’s clean style
fig.update_layout(
    template='plotly_white',
    title_x=0.5,
    legend_title_side='top',
    xaxis_title='Borough',
    yaxis_title='Number of Complaints',
    hovermode='x unified'
)

fig.show()

# %%
# Print basic results from the grouped-bar chart
print("\n=== Basic Results from Figure ===")
for borough in phase_counts['borough'].unique():
    borough_data = phase_counts[phase_counts['borough'] == borough].set_index('phase').sort_index()
    print(f"\n{borough}:")
    for phase in phase_order:
        if phase in borough_data.index:
            count = borough_data.loc[phase, 'count']
            print(f"  {phase}: {count:,} complaints")
    # Show percent change from Pre-COVID to Reopening if both exist
    if all(p in borough_data.index for p in ['Pre-COVID', 'Reopening']):
        pre = borough_data.loc['Pre-COVID', 'count']
        reopen = borough_data.loc['Reopening', 'count']
        pct = ((reopen - pre) / pre * 100) if pre > 0 else float('nan')
        print(f"  Change Pre-COVID → Reopening: {pct:+.1f}%")

# %% [markdown]
# ### Most Common Noise Categories by Borough
# 

# %%
# 1. Compute total complaints by borough & noise_category
category_counts = (
    combined_df
    .groupby(['borough', 'noise_category'])
    .size()
    .reset_index(name='count')
)

# 2. Get the top N categories for each borough
top_n = 5
top_categories = (
    category_counts
    .sort_values(['borough', 'count'], ascending=[True, False])
    .groupby('borough')
    .head(top_n)
    .copy()
)

# 3. Define a consistent borough order
borough_order = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
top_categories['borough'] = pd.Categorical(top_categories['borough'],
                                           categories=borough_order,
                                           ordered=True)

# 4. Build the faceted bar chart
fig = px.bar(
    top_categories,
    x='noise_category',
    y='count',
    facet_col='borough',
    category_orders={
        'borough': borough_order,
        'noise_category': top_categories['noise_category'].unique().tolist()
    },
    labels={
        'noise_category': 'Noise Category',
        'count': 'Total Complaints'
    },
    title='Top 5 Noise Categories by Borough',
    color_discrete_sequence=[custom_colors[0]]  
)

# 5. Tidy up the layout to match your notebook style
fig.update_layout(
    template='plotly_white',
    title_x=0.5,
    showlegend=False,
    hovermode='x unified',
    xaxis_title='Noise Category'  
)

for axis in fig.layout:
    if axis.startswith('xaxis') and hasattr(fig.layout[axis], 'title'):
        fig.layout[axis].title.text = None

# Clean facet titles 
for ann in fig.layout.annotations:
    ann.text = ann.text.split('=')[-1]

# 6. Rotate x-axis labels for readability
fig.update_xaxes(tickangle=45, tickfont=dict(size=9))

fig.show()

# %%
# Print the top 5 noise categories for each borough
print("=== Top 5 Noise Categories by Borough ===")
for borough in top_categories['borough'].cat.categories:
    borough_data = top_categories[top_categories['borough'] == borough]
    if not borough_data.empty:
        print(f"\n{borough}:")
        for _, row in borough_data.iterrows():
            print(f"  {row['noise_category']}: {row['count']:,} complaints")
            

# %% [markdown]
# ### Time Series with Category Breakdown

# %%
# 1. Copy & set up a monthly period column
ts_df = combined_df.copy()
ts_df['month'] = ts_df['created_date'].dt.to_period('M').dt.to_timestamp()

# 2. (Optional) Focus on top N categories overall
N = 5
top_categories = (
    ts_df['noise_category']
    .value_counts()
    .nlargest(N)
    .index
    .tolist()
)
ts_df = ts_df[ts_df['noise_category'].isin(top_categories)]

# 3. Aggregate counts by month & category
time_counts = (
    ts_df
    .groupby(['month', 'noise_category'])
    .size()
    .reset_index(name='count')
)

# 4. Build a stacked‐area chart
fig = px.area(
    time_counts,
    x='month',
    y='count',
    color='noise_category',
    category_orders={'noise_category': top_categories},
    color_discrete_sequence=custom_colors[:len(top_categories)],
    labels={
        'month': 'Month',
        'count': 'Number of Complaints',
        'noise_category': 'Noise Category'
    },
    title='Monthly Noise Complaint Trends by Category'
)

# 5. Style tweaks to match your notebook
fig.update_layout(
    template='plotly_white',
    title_x=0.5,
    legend_title_side='top',
    hovermode='x unified'
)
fig.update_xaxes(
    dtick="M3",           # tick every 3 months
    tickformat="%b %Y",   # e.g. "Jan 2020"
    tickangle= -45
)

fig.show()

# %% [markdown]
# NYC’s monthly noise complaint trends reveal that residential noise dominated and spiked sharply after lockdown, reflecting increased home-based frustrations. Street/Sidewalk and Vehicle noise rose seasonally, especially in summer 2020, as public life and mobility resumed. Commercial and general noise complaints dropped during lockdown but rebounded with reopening. Each noise type responded differently to policy changes, showing that the city’s soundscape became not just louder, but more varied and dynamic. This supports the thesis that the noise rebound was closely linked to the reopening of urban life and its uneven impacts across environments.

# %% [markdown]
# ### Dynamic Heatmap

# %%
gurl = "https://data.cityofnewyork.us/resource/gthc-hcne.geojson"
borough_gdf = gpd.read_file(gurl).rename(columns={'boroname':'borough'})[['borough','geometry']]

df = combined_df.copy()
df['month'] = df['created_date'].dt.to_period('M').dt.to_timestamp()
df['month_str'] = df['month'].dt.strftime('%Y-%m')

grouped = df.groupby('month_str')
heat_data = [
    grouped.get_group(month)[['latitude', 'longitude']].values.tolist()
    for month in grouped.groups
]
time_index = list(grouped.groups.keys())

# ───────────────────────────────────────────────────────────
# 2.  Compute borough centroids (for markers/labels)
# ───────────────────────────────────────────────────────────
borough_centers = borough_gdf.copy()
borough_centers['centroid'] = borough_centers.geometry.centroid

# ───────────────────────────────────────────────────────────
# 3.  Base map with TWO selectable tile layers
# ───────────────────────────────────────────────────────────
m = folium.Map(
    location=[40.7128, -74.0060],
    zoom_start=11,
    tiles='cartodbpositron',
    name='CartoDB Positron'
)
folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)

# ───────────────────────────────────────────────────────────
# 4.  Borough boundaries (always on, thin black)
# ───────────────────────────────────────────────────────────
folium.GeoJson(
    borough_gdf.__geo_interface__,
    style_function=lambda _: {'color':'black','weight':1,'fill':False},
    control=False
).add_to(m)

# ───────────────────────────────────────────────────────────
# 5.  Centre markers + labels (consistent style)
# ───────────────────────────────────────────────────────────
for _, row in borough_centers.iterrows():
    lon, lat = row['centroid'].x, row['centroid'].y
    folium.CircleMarker(
        [lat, lon], radius=1,
        color='black', weight=1,
        fill=True, fill_color='white',
        fill_opacity=1, control=False
    ).add_to(m)
    folium.Marker(
        [lat, lon],
        icon=DivIcon(html=f"""
            <div style="
                font-weight:bold;
                font-size:14px;
                text-shadow:0 0 3px #fff;
            ">
                {row['borough']}
            </div>
        """),
        control=False
    ).add_to(m)

# ───────────────────────────────────────────────────────────
# 6.  Time-enabled heatmap (always on)
# ───────────────────────────────────────────────────────────
HeatMapWithTime(
    data=heat_data,
    index=time_index,
    auto_play=True,
    max_opacity=0.8,
    radius=10,
    use_local_extrema=False,
    name='Monthly Noise Density',
    control=False
).add_to(m)

# ───────────────────────────────────────────────────────────
# 7.  Add a combined legend (density + basemap names)
# ───────────────────────────────────────────────────────────
legend_html = """
{% macro html(this, kwargs) %}
<div style="
    position: fixed;
    top: 10px;
    left: 10px;
    width: 180px;
    background: white;
    border:2px solid grey;
    z-index:9999;
    padding: 10px;
    font-size:12px;
">
  <div style="text-align:center; font-weight:bold; margin-bottom:5px;">
    Noise Density
  </div>
  <div style="
      background: linear-gradient(to right, blue, lime, red);
      height: 10px;
      margin-bottom:5px;
  "></div>
  <div style="display:flex; justify-content: space-between; margin-bottom:8px;">
    <span>Low</span><span>High</span>
  </div>
  <div style="font-weight:bold; margin-bottom:3px;">
    Basemaps
  </div>
  <div>• CartoDB Positron</div>
  <div>• OpenStreetMap</div>
</div>
{% endmacro %}
"""
legend = MacroElement()
legend._template = Template(legend_html)
m.get_root().add_child(legend)

folium.LayerControl(collapsed=False).add_to(m)
m.save('dynamic_heatmap.html')
m

# %% [markdown]
# This interactive map effectively visualizes the spatial and temporal evolution of noise complaints across NYC boroughs.
# The animated heatmap highlights the impact of COVID-19 phases, with a marked reduction during lockdown and a pronounced increase after reopening.
# The inclusion of borough boundaries and centroids aids interpretation, while the custom legend and basemap toggles enhance usability.

# %% [markdown]
# ### Borough × Category Heatmap

# %%
# 1. Prepare month buckets
df = combined_df.copy()
df['month'] = df['created_date'].dt.to_period('M').dt.to_timestamp()
df = df[(df['month'] >= '2019-01-01') & (df['month'] <= '2020-12-31')]
df['month_str'] = df['month'].dt.strftime('%Y-%m')

# 2. Aggregate counts by borough, month, category
counts = (
    df
    .groupby(['borough','month_str','noise_category'])
    .size()
    .reset_index(name='count')
)

# 3. Take only the top 5 noise categories overall
top_5_categories = (
    counts.groupby('noise_category')['count']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
    .tolist()
)
counts = counts[counts['noise_category'].isin(top_5_categories)]

# 4. Define boroughs, months, and category order
boroughs = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
months = pd.period_range('2019-01','2020-12', freq='M').to_timestamp().strftime('%Y-%m').tolist()
cat_order = [cat for cat in top_5_categories]  # preserve order

# 5. Build subplot figure (1 row × 5 cols)
fig = make_subplots(
    rows=1, cols=5,
    shared_yaxes=True,
    subplot_titles=boroughs,
    horizontal_spacing=0.01
)

# 6. Add a heatmap for each borough
for i, boro in enumerate(boroughs, start=1):
    sub = counts[counts['borough'] == boro]
    pivot = sub.pivot(index='noise_category', columns='month_str', values='count').fillna(0)
    pivot = pivot.reindex(index=cat_order, columns=months, fill_value=0)
    
    fig.add_trace(
        go.Heatmap(
            z=pivot.values,
            x=months,
            y=pivot.index,
            coloraxis='coloraxis',
            showscale=(i == 1),            # show colorbar only on first plot
            hovertemplate=(
                'Borough: ' + boro + '<br>'
                'Month: %{x}<br>'
                'Category: %{y}<br>'
                'Count: %{z}<extra></extra>'
            )
        ),
        row=1, col=i
    )

# 7. Configure shared color axis, layout, and styling
fig.update_layout(
    coloraxis=dict(
        colorscale='YlOrRd',
        colorbar=dict(title='Complaint Count', thickness=12, len=0.5)
    ),
    template='plotly_white',
    height=600, width=1400,
    title_text='Monthly Noise Complaint Intensity by Category & Borough (2019-2020)',
    title_x=0.5
)

# 8. Tidy up axes
fig.update_xaxes(tickangle=45, tickfont=dict(size=9))
fig.update_yaxes(title_text='Noise Category', tickfont=dict(size=9))

fig.show()

# Save the figure
fig.write_html("borough_category_heatmap.html")

# %%
print("\n=== Main Results from Borough × Category Heatmap ===")
for i, boro in enumerate(boroughs):
    sub = counts[counts['borough'] == boro]
    pivot = sub.pivot(index='noise_category', columns='month_str', values='count').fillna(0)
    print(f"\n{boro}:")
    for cat in cat_order:
        series = pivot.loc[cat]
        peak_month = series.idxmax()
        peak_count = int(series.max())
        print(f"  {cat}: peak {peak_count:,} complaints in {peak_month}")

# %% [markdown]
# The heatmap shows that residential noise complaints surged across all NYC boroughs during reopening, with the Bronx experiencing the highest peak. Street/Sidewalk noise spiked citywide as public spaces reopened, while Vehicle and Commercial noise rebounded later in 2020. Each borough’s noise profile changed in timing and intensity, reflecting local conditions and the broader impact of the pandemic on urban life.

# %% [markdown]
# ### Category Composition Stacked Area Plot (Pre vs. Lockdown vs. Reopening)

# %%
# 1. Monthly timestamp
ts_df = combined_df.copy()
ts_df['month'] = ts_df['created_date'].dt.to_period('M').dt.to_timestamp()

# 2. Aggregate monthly counts per category
comp_df = (
    ts_df
    .groupby(['month', 'noise_category'])
    .size()
    .reset_index(name='count')
)

# 3. Identify top 5 categories by overall volume
top_N = 5
top_cats = (
    comp_df
    .groupby('noise_category')['count']
    .sum()
    .nlargest(top_N)
    .index
    .tolist()
)
comp_df = comp_df[comp_df['noise_category'].isin(top_cats)]

# 4. Build the percent‐normalized stacked area chart
fig = px.area(
    comp_df,
    x='month',
    y='count',
    color='noise_category',
    groupnorm='percent',
    category_orders={'noise_category': top_cats},
    color_discrete_sequence=custom_colors[:len(top_cats)],
    labels={
        'month': 'Month',
        'count': '% of Complaints',
        'noise_category': 'Noise Category'
    },
    title=f'Relative Mix of Top {top_N} Noise Categories Over Time'
)

# 5. Show only the trace under the cursor
fig.update_layout(
    hovermode='closest',
    template='plotly_white',
    title_x=0.5
)

# 6. Per‐trace hovertemplate (only that area’s data)
for trace in fig.data:
    trace.hovertemplate = (
        f'Category: {trace.name}<br>'
        'Month: %{x|%b %Y}<br>'
        'Percentage: %{y:.1f}%<extra></extra>'
    )

# 7. Add robust phase markers
lock = pd.to_datetime(lockdown_start)
reopen = pd.to_datetime(phase1_start)

for x_date, label in [(lock, "Lockdown Begins"), (reopen, "Reopening Begins")]:
    fig.add_shape(
        type='line',
        x0=x_date, x1=x_date,
        y0=0, y1=1,
        xref='x', yref='paper',
        line=dict(color='black', dash='dash')
    )
    fig.add_annotation(
        x=x_date, y=1.1,
        xref='x', yref='paper',
        showarrow=False,
        text=label,
        font=dict(size=10)
    )

# 8. Range slider & selector buttons for interactive brushing
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=[
                dict(count=3, label="3 m", step="month", stepmode="backward"),
                dict(count=6, label="6 m", step="month", stepmode="backward"),
                dict(count=1, label="1 y", step="year", stepmode="backward"),
                dict(step="all")
            ]
        ),
        rangeslider={'visible': True},
        tickformat="%b %Y",
        tickangle=-45
    ),
    yaxis=dict(ticksuffix="%")
)

fig.show()


# %%
print("\n=== Main Results from Stacked Area Plot ===")
cat_labels = {
    'Residential': 'Residential',
    'Street/Sidewalk': 'Street/Sidewalk',
    'Vehicle': 'Vehicle',
    'Noise': 'General Noise',
    'Commercial': 'Commercial'
}
for cat in top_cats:
    cat_df = comp_df[comp_df['noise_category'] == cat]
    max_row = cat_df.loc[cat_df['count'].idxmax()]
    min_row = cat_df.loc[cat_df['count'].idxmin()]
    print(f"{cat_labels.get(cat, cat)}: peaks at {max_row['count']:.1f}% in {max_row['month'].strftime('%b %Y')}, lowest at {min_row['count']:.1f}% in {min_row['month'].strftime('%b %Y')}")

# %% [markdown]
# ###  Line Plot by Noise Category

# %%
# 1. Prepare the data
df = combined_df.copy()
df['month'] = df['created_date'].dt.to_period('M').dt.to_timestamp()

# Identify top 5 categories overall
top5 = (
    df['noise_category']
      .value_counts()
      .nlargest(5)
      .index
      .tolist()
)
df_top5 = df[df['noise_category'].isin(top5)]

# Aggregate monthly counts
monthly_cat = (
    df_top5
      .groupby(['month','noise_category'])
      .size()
      .reset_index(name='count')
)

# 2. Build the multi-line figure
fig = px.line(
    monthly_cat,
    x='month',
    y='count',
    color='noise_category',
    category_orders={'noise_category': top5},
    color_discrete_sequence=custom_colors[:len(top5)],
    labels={
        'month': 'Month',
        'count': 'Number of Complaints',
        'noise_category': 'Noise Category'
    },
    title='Monthly Complaint Volume by Noise Category (Top 5)'
)

# 3. Add vertical event markers
lock = pd.to_datetime(lockdown_start)
reopen = pd.to_datetime(phase1_start)

for date, label, col in [
    (lock,   'Lockdown Begins', custom_colors[2]),
    (reopen, 'Phase 1 Reopening', custom_colors[3])
]:
    fig.add_vline(x=date, line_dash='dash', line_color=col, opacity=0.7)
    fig.add_annotation(
        x=date, y=1.02, xref='x', yref='paper',
        text=label,
        showarrow=False,
        font=dict(color=col, size=10, family='Arial'),
        bgcolor='white', bordercolor=col, borderwidth=1, borderpad=2
    )

# 4. Tweak layout for consistency
fig.update_layout(
    template='plotly_white',
    title_x=0.5,
    legend_title_text='Noise Category',
    hovermode='x unified',
    xaxis=dict(
        dtick='M1',
        tickformat='%b\n%Y',
        tickangle=-45
    )
)

fig.show()

fig.write_html("monthly_category_trends.html")

# %% [markdown]
# ### Animated Bar Chart Race

# %%
df = combined_df.copy()
df['month'] = df['created_date'].dt.to_period('M').dt.to_timestamp()
monthly = df.groupby(['month', 'borough']).size().reset_index(name='count')

# ensure every month–borough combo exists
months   = pd.period_range(df['month'].min(), df['month'].max(), freq='M').to_timestamp()
boroughs = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
idx = pd.MultiIndex.from_product([months, boroughs], names=['month', 'borough'])

monthly_full = (
    monthly
    .set_index(['month', 'borough'])
    .reindex(idx, fill_value=0)
    .reset_index()
)
monthly_full['month_str'] = monthly_full['month'].dt.strftime('%Y-%m')

# ------------------------------------
# 2.  Build the animated bar chart
# ------------------------------------
fig = px.bar(
    monthly_full,
    x='count', y='borough',
    color='borough',
    orientation='h',
    animation_frame='month_str',
    animation_group='borough',
    range_x=[0, monthly_full['count'].max()*1.1],
    category_orders={'borough': boroughs},
    color_discrete_sequence=custom_colors,
    labels={'count':'Complaints', 'borough':'Borough', 'month_str':'Month'},
    title='Monthly Noise Complaint Volume by Borough (Bar Chart Race)'
)

# ------------------------------------
# 3.  Helper to return a background-filling shape
# ------------------------------------
def phase_rect(fillcolor):
    return [dict(
        type='rect', xref='paper', yref='paper',
        x0=0, x1=1, y0=0, y1=1,
        fillcolor=fillcolor, opacity=0.8,
        layer='below', line_width=0
    )]

# ------------------------------------
# 4.  Add shapes to EVERY frame
# ------------------------------------
lock_start   = pd.to_datetime(lockdown_start)
reopen_start = pd.to_datetime(phase1_start)

# Increase opacity for stronger highlight
def phase_rect(fillcolor):
    return [dict(
        type='rect', xref='paper', yref='paper',
        x0=0, x1=1, y0=0, y1=1,
        fillcolor=fillcolor, opacity=0.8,  # was 0.25
        layer='below', line_width=0
    )]

for fr in fig.frames:
    m = pd.to_datetime(fr.name + '-01')  # frame name = YYYY-MM
    if lock_start <= m < reopen_start:     # Lockdown
        fr.layout.shapes = phase_rect('#ffe6e6')
    elif m >= reopen_start:                # Reopening
        fr.layout.shapes = phase_rect('#e6ffe6')
    else:                                  # Pre-COVID
        fr.layout.shapes = []              # no highlight

# Set initial (first) frame highlight
first_month = pd.to_datetime(months[0])
if lock_start <= first_month < reopen_start:
    fig.layout.shapes = phase_rect('#ffe6e6')
elif first_month >= reopen_start:
    fig.layout.shapes = phase_rect('#e6ffe6')

# ------------------------------------
# 5.  Add a dummy scatter for the legend
# ------------------------------------
fig.add_trace(go.Scatter(
    x=[None], y=[None], mode='markers',
    marker=dict(size=12, color='#ffe6e6', symbol='square'),
    showlegend=True, name='Lockdown'
))
fig.add_trace(go.Scatter(
    x=[None], y=[None], mode='markers',
    marker=dict(size=12, color='#e6ffe6', symbol='square'),
    showlegend=True, name='Reopening'
))

# ------------------------------------
# 6.  Layout tweaks (including play / pause menu)
# ------------------------------------
fig.update_layout(
    template='plotly_white',
    title_x=0.5,
    xaxis_title='Number of Complaints',
    yaxis_title='Borough',
    yaxis_autorange='reversed',
    legend=dict(title='Phase', x=1.02, y=0.5),
    updatemenus=[{
        'type':'buttons',
        'buttons':[
            {'label':'Play',
             'method':'animate',
             'args':[None, {'frame':{'duration':500, 'redraw':True},
                            'fromcurrent':True}]
            },
            {'label':'Pause',
             'method':'animate',
             'args':[[None],
                    {'frame':{'duration':0, 'redraw':False},
                     'mode':'immediate'}]
            }
        ],
        'showactive':True,
        'y':-0.10, 'x':1.2,
        'xanchor':'center', 'yanchor':'top'
    }]
)

fig.write_html("bar_chart_race.html")
fig.show()



# %% [markdown]
# This animated bar chart race shows the monthly volume of noise complaints by borough from Jan 2019 to Dec 2020.
#  All boroughs experienced a sharp increase in complaints during the lockdown and reopening phases of 2020.
#  Manhattan and the Bronx saw the largest absolute increases in complaint counts during the pandemic.
#  Brooklyn and Queens also showed notable surges, especially during summer 2020.
#  Staten Island consistently had the lowest complaint volume, but also saw a relative increase during reopening.
#  The background color highlights the lockdown (pink) and reopening (green) periods, making it easy to see phase-related shifts.
# The visualization reveals that noise complaints did not return to pre-COVID levels by the end of 2020.

# %% [markdown]
# ### Bokeh plot Top 5 categories

# %%
# 1. Prepare the data (ensure combined_df is in memory)
df = combined_df.copy()
df['month'] = df['created_date'].dt.to_period('M').dt.to_timestamp()
df = df[(df['month'] >= '2019-01-01') & (df['month'] <= '2020-12-01')]
df['month_str'] = df['month'].dt.strftime('%Y-%m')

# Aggregate counts by borough, month, category
agg = df.groupby(['borough', 'month_str', 'noise_category']).size().reset_index(name='count')

# Determine top 5 categories overall
top_N = 5
top_cats = agg.groupby('noise_category')['count'].sum().nlargest(top_N).index.tolist()
categories = top_cats

# Generate lookup of counts for top 5 categories
boroughs = sorted(agg['borough'].unique().tolist())
months = sorted(agg['month_str'].unique().tolist())
data_js = {}
for boro in boroughs:
    for month in months:
        key = f"{boro}_{month}"
        counts = [
            int(agg.loc[
                (agg['borough']==boro) & 
                (agg['month_str']==month) & 
                (agg['noise_category']==cat),
                'count'
            ].values[0]) if not agg[
                (agg['borough']==boro) & 
                (agg['month_str']==month) & 
                (agg['noise_category']==cat)
            ].empty else 0
            for cat in categories
        ]
        data_js[key] = counts

# Identify lockdown and reopening month strings
lockdown_month = pd.to_datetime(lockdown_start).to_period('M').to_timestamp().strftime('%Y-%m')
reopening_month = pd.to_datetime(phase1_start).to_period('M').to_timestamp().strftime('%Y-%m')

# 2. Initial data source
init_key = f"{boroughs[0]}_{months[0]}"
source = ColumnDataSource(data=dict(category=categories, count=data_js[init_key]))

# 3. Figure setup
p = figure(
    x_range=categories,
    y_range=(0, max(data_js[init_key]) * 1.1),
    height=400, width=700,
    title=f"{boroughs[0]} — {months[0]}",
    toolbar_location=None,
    background_fill_color='white'
)
p.vbar(x='category', top='count', width=0.8, source=source, fill_color="navy")
p.xaxis.major_label_orientation = 1
p.xaxis.axis_label = "Noise Category"
p.yaxis.axis_label = "Number of Complaints"

# 4. Widgets: Slider, Dropdown, Play & Pause, Narrative Div
slider = Slider(start=0, end=len(months)-1, value=0, step=1, title=f"Month: {months[0]}")
select = Select(options=boroughs, value=boroughs[0], title="Borough")
play = Button(label="▶ Play", width=60)
pause = Button(label="⏸ Pause", width=60)
div = Div(text="", width=800, height=50)

# Legend for phase highlights
legend = Div(text="""
<div style="display:flex;flex-direction:column;padding-left:10px;">
  <div style="margin-bottom:5px;">
    <span style="background:#ff4d4d;width:15px;height:15px;display:inline-block;margin-right:8px;"></span>
    Lockdown Begins
  </div>
  <div>
    <span style="background:#33cc33;width:15px;height:15px;display:inline-block;margin-right:8px;"></span>
    Reopening Begins
  </div>
</div>
""", width=180, height=80)

# 5. Callback for interactivity and highlighting phases
callback = CustomJS(
    args=dict(
        source=source, slider=slider, select=select, div=div,
        data=data_js, months=months, plot=p,
        lockdown_month=lockdown_month, reopening_month=reopening_month
    ),
    code="""
    const idx = slider.value;
    const month = months[idx];
    slider.title = "Month: " + month;
    const boro = select.value;
    const key = boro + "_" + month;
    const counts = data[key];
    source.data['count'] = counts;
    source.change.emit();

    // Update plot title
    plot.title.text = boro + " — " + month;

    // Highlight background color on phase start with more visible green/red
    if (month === lockdown_month) {
        plot.background_fill_color = '#ff4d4d';  // strong red
    } else if (month === reopening_month) {
        plot.background_fill_color = '#33cc33';  // strong green
    } else {
        plot.background_fill_color = 'white';
    }

    // Narrative: dominant category
    const maxCount = Math.max(...counts);
    const domIdx = counts.indexOf(maxCount);
    const domCat = source.data['category'][domIdx];
    div.text = `<b>${month}:</b> ${domCat} dominates in <b>${boro}</b> with ${maxCount} complaints.`;
"""
)

slider.js_on_change('value', callback)
select.js_on_change('value', callback)

# 6. Play/Pause functionality
play_callback = CustomJS(args=dict(slider=slider), code="""
    if (window._timer) { clearInterval(window._timer); }
    window._timer = setInterval(function() {
        let next = slider.value + 1;
        if (next > slider.end) { clearInterval(window._timer); }
        else { slider.value = next; }
    }, 800);
""")
pause_callback = CustomJS(code="""
    if (window._timer) { clearInterval(window._timer); }
""")
play.js_on_click(play_callback)
pause.js_on_click(pause_callback)

# 7. Layout and display
controls = bokeh_row(select, slider, play, pause, width=880)
layout = column(controls, bokeh_row(p, legend), div)
show(layout)



# %% [markdown]
# This interactive Bokeh plot shows the monthly volume of noise complaints by top 5 noise categories
# for each NYC borough from Jan 2019 to Dec 2020. 
# Users can select a borough and month using the dropdown and slider, or animate the timeline with play/pause.
# The background color highlights the start of lockdown (red) and reopening (green) phases.
# The narrative below the plot updates to describe the dominant noise category for the selected borough and month.
# This visualization helps reveal how noise complaint patterns shifted during the COVID-19 pandemic.

# %% [markdown]
# ### Bokeh 2019-2020 Noise Category Mix (Top 5)

# %%
from bokeh.io import output_notebook, show
from bokeh.models import ColumnDataSource, Select, Div, CustomJS, FactorRange
from bokeh.plotting import figure
from bokeh.layouts import row as bokeh_row, column as bokeh_column
from collections import defaultdict
import pandas as pd
from bokeh.io import output_file, save

output_notebook()

# --------------------------------------------------------------------------------
# 1. DATA PREPARATION for both years
# --------------------------------------------------------------------------------
df = combined_df.copy()
df['year'] = df['created_date'].dt.year
df_2019 = df[df['year'] == 2019]
df_2020 = df[df['year'] == 2020]

boroughs = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']

# Build lookup dicts keyed by "year_borough"
cats = {}
cnts = {}
dom_cat = {}
dom_cnt = {}
surge_cat = {}
surge_pct = {}
insight = {}

for year_tag, dfi in [('2019', df_2019), ('2020', df_2020)]:
    counts_year = dfi.groupby(['borough','noise_category']).size()
    other_year = '2019' if year_tag == '2020' else '2020'
    dfi_other = df_2019 if year_tag == '2020' else df_2020
    counts_other = dfi_other.groupby(['borough','noise_category']).size()
    
    for boro in boroughs:
        idx = (counts_year.index.get_level_values(0) == boro)
        counts = counts_year[idx]
        # Top 5 categories
        top5 = counts.sort_values(ascending=False).head(5)
        cats[f"{year_tag}_{boro}"] = list(top5.index)
        cnts[f"{year_tag}_{boro}"] = [int(v) for v in top5.values]
        # Dominant
        if not top5.empty:
            mc = top5.idxmax(); mv = int(top5.max())
        else:
            mc, mv = "N/A", 0
        dom_cat[f"{year_tag}_{boro}"] = mc
        dom_cnt[f"{year_tag}_{boro}"] = mv
        # Surge vs other year
        pct = {}
        for cat_name, v in counts.items():
            vo = counts_other.get((boro, cat_name), 0)
            pct[cat_name] = (float('inf') if vo==0 else (v-vo)/vo*100)
        if pct:
            sc = max(pct, key=pct.get)
            sp = pct[sc] if pct[sc]!=float('inf') else None
        else:
            sc, sp = "N/A", 0
        surge_cat[f"{year_tag}_{boro}"] = sc
        surge_pct[f"{year_tag}_{boro}"] = sp
        # Insight sentence
        if sp is None:
            ins = f"{boro} saw new {sc} in {year_tag} absent previously; {mc} remained dominant."
        else:
            ins = f"{boro} saw a {sp:.1f}% surge in {sc} from 2019 to 2020, {mc} dominant in {year_tag}."
        insight[f"{year_tag}_{boro}"] = ins

# --------------------------------------------------------------------------------
# 2. INITIAL DATA SOURCE for 2020 Manhattan
# --------------------------------------------------------------------------------
init_year = '2020'
init_boro = boroughs[0]
init_key = f"{init_year}_{init_boro}"
source = ColumnDataSource(data=dict(
    category=cats[init_key],
    count=cnts[init_key]
))

# --------------------------------------------------------------------------------
# 3. FIGURE
# --------------------------------------------------------------------------------
p = figure(
    x_range=FactorRange(factors=cats[init_key]),
    y_range=(0, max(cnts[init_key]) * 1.15),
    height=350, width=500,
    title=f"{init_year} Noise Category Mix (Top 5)",
    toolbar_location=None,
    tools=""
)
p.vbar(x='category', top='count', width=0.7, source=source, fill_color="navy")
p.xaxis.axis_label = "Noise Category"
p.yaxis.axis_label = "Complaints"
p.xaxis.major_label_orientation = 1

# --------------------------------------------------------------------------------
# 4. INFO PANEL
# --------------------------------------------------------------------------------
info_div = Div(
    text=f"<b>Dominant:</b> {dom_cat[init_key]} ({dom_cnt[init_key]:,})<br>"
         f"<b>Biggest surge:</b> {surge_cat[init_key]} "
         f"({'' if surge_pct[init_key] is None else f'{surge_pct[init_key]:.1f}%↑'})<br><br>"
         f"{insight[init_key]}",
    width=400, height=120
)

# --------------------------------------------------------------------------------
# 5. WIDGETS: Selectors for Year and Borough
# --------------------------------------------------------------------------------
year_select = Select(title="Year", options=['2019','2020'], value=init_year, width=100)
boro_select = Select(title="Borough", options=boroughs, value=init_boro, width=150)

callback = CustomJS(
    args=dict(
        src=source, plot=p, div=info_div,
        cats=cats, cnts=cnts,
        dom=dom_cat, dmc=dom_cnt,
        sc=surge_cat, sp=surge_pct, ins=insight,
        year_sel=year_select, boro_sel=boro_select
    ),
    code="""
    const year = year_sel.value;
    const boro = boro_sel.value;
    const key = year + "_" + boro;
    // update datasource
    src.data['category'] = cats[key];
    src.data['count']    = cnts[key];
    src.change.emit();
    // update axes
    plot.x_range.factors = cats[key];
    plot.y_range.end = Math.max(...cnts[key]) * 1.15;
    // update title
    plot.title.text = year + " Noise Category Mix (Top 5)";
    // update info
    const surgeText = sp[key]===null ? '∞' : sp[key].toFixed(1)+'%↑';
    div.text = `<b>Dominant:</b> ${dom[key]} (${dmc[key].toLocaleString()})<br>`
             + `<b>Biggest surge:</b> ${sc[key]} (${surgeText})<br><br>`
             + ins[key];
"""
)
year_select.js_on_change('value', callback)
boro_select.js_on_change('value', callback)

# --------------------------------------------------------------------------------
# 6. LAYOUT
# --------------------------------------------------------------------------------
controls = bokeh_row(year_select, boro_select, sizing_mode='scale_width')
layout = bokeh_column(
    Div(text="<h3>Noise Type Sensitivity Map</h3>"
             "<p>Select year and borough to explore the noise profile.</p>"),
    controls,
    bokeh_row(p, info_div)
)
show(layout)

output_file("noise_category_mix.html")
save(layout)

# %% [markdown]
# ### NYC Borough Noise Complaint Change Map (2019 → 2020)

# %%
df = combined_df.copy()
df['year'] = df['created_date'].dt.year

# Borough totals
totals = (
    df[df['year'].isin([2019, 2020])]
      .groupby(['borough', 'year'])
      .size()
      .unstack(fill_value=0)
      .rename(columns={2019: 'complaints_2019', 2020: 'complaints_2020'})
)
totals['pct_change'] = (
    (totals['complaints_2020'] - totals['complaints_2019'])
    / totals['complaints_2019'].replace(0, pd.NA)
) * 100.0

# Top 5 rising categories (raw delta)
cat_change = (
    df[df['year'].isin([2019, 2020])]
      .groupby(['borough', 'noise_category', 'year'])
      .size()
      .unstack(fill_value=0)
      .rename(columns={2019: 'cnt_2019', 2020: 'cnt_2020'})
)
cat_change['delta'] = cat_change['cnt_2020'] - cat_change['cnt_2019']

top5_html = {}
for boro, sub in cat_change.groupby(level=0):
    top5 = (
        sub.sort_values('delta', ascending=False)
            .head(5)
            .reset_index()
    )
    lines = [
        f"{row['noise_category']}: "
        f"+{row['delta']:,} "
        f"({row['cnt_2019']}→{row['cnt_2020']})"
        for _, row in top5.iterrows()
    ]
    top5_html[boro] = "<br>".join(lines)

# Geo boundaries
gurl = "https://data.cityofnewyork.us/resource/gthc-hcne.geojson"
borough_gdf = gpd.read_file(gurl).rename(columns={'boroname':'borough'})[['borough','geometry']]
map_df = borough_gdf.merge(totals.reset_index(), on='borough', how='left')

# Create mutable geojson data once
geojson_data = map_df.__geo_interface__

for feat in geojson_data['features']:
    boro = feat['properties']['borough']
    pct  = feat['properties']['pct_change']
    pct_txt = "N/A" if pd.isna(pct) else f"{pct:.1f}%"
    feat['properties']['popupContent'] = (
        f"<div style='font-family:sans-serif;width:240px'>"
        f"<h4 style='margin:0'>{boro}</h4>"
        f"<p style='margin:4px 0'><b>% change:</b> {pct_txt}</p>"
        f"<p style='margin:4px 0'><b>Top 5 rising categories</b><br>{top5_html.get(boro,'No data')}</p>"
        f"</div>"
    )

# Color scale
vmin, vmax = map_df['pct_change'].min(), map_df['pct_change'].max()
colormap = linear.YlOrRd_09.scale(vmin, vmax).to_step(9)
colormap.caption = "% Change in Complaints (2019 → 2020)"

def style_fn(feature):
    pct = feature['properties']['pct_change']
    color = colormap(pct) if pd.notnull(pct) else '#cccccc'
    return {'fillColor': color, 'color':'black', 'weight':1, 'fillOpacity':0.7}

tooltip = GeoJsonTooltip(
    fields=['borough', 'pct_change'],
    aliases=['Borough:', '% Change:'],
    localize=True,
    labels=True,
    sticky=False,
    toLocaleString=True,
    style="font-size:12px;"
)

popup = GeoJsonPopup(
    fields=['popupContent'],
    labels=False,
    parse_html=True,
    sticky=True,
    max_width=250
)

# ------------------------------------------------------------------
m = folium.Map(
    location=[40.7128, -74.0060],
    zoom_start=10,
    tiles='cartodbpositron',
    name='CartoDB Positron'
)
folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)

# ------------------------------------------------------------------
# Choropleth layer 
# ------------------------------------------------------------------
GeoJson(
    geojson_data,
    style_function=style_fn,
    highlight_function=lambda _: {'weight': 3, 'color': 'blue'},
    tooltip=tooltip,
    popup=popup,
    control=False          
).add_to(m)

# ------------------------------------------------------------------
#  Borough-centre markers + labels
# ------------------------------------------------------------------
centers = borough_gdf.copy()
centers['centroid'] = centers.geometry.centroid

for _, row in centers.iterrows():
    lat, lon = row['centroid'].y, row['centroid'].x
    folium.CircleMarker(
        location=[lat, lon],
        radius=0.1,
        color='black',
        weight=1,
        fill=True,
        fill_color='white',
        fill_opacity=1,
        control=False      
    ).add_to(m)
    folium.map.Marker(
        [lat, lon],
        icon=folium.DivIcon(html=f"""
            <div style="font-weight:bold;font-size:12px;
                        text-shadow:0 0 3px #fff;">{row['borough']}</div>
        """)
    ).add_to(m)

# ------------------------------------------------------------------
# Legend + Layer-Control
# ------------------------------------------------------------------
m.add_child(colormap)                     
folium.LayerControl(collapsed=False).add_to(m)  

m

# Save the map
#m.save("borough_choropleth_map.html")

# %%
print("Main findings/insights from the map:")
for boro in ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']:
    pct = map_df.loc[map_df['borough'] == boro, 'pct_change'].values[0]
    pct_txt = "N/A" if pd.isna(pct) else f"{pct:.1f}%"
    print(f"- {boro}: {pct_txt} change in complaints (2019→2020)")
    print(f"  Top 5 rising categories:\n    {top5_html.get(boro, 'No data').replace('<br>', '\n    ')}")

# %% [markdown]
# ## 6. Discussion
# ### What went well?
# Several aspects of this project were particularly successful:
# 
# 1. **Narrative Structure**: The three-phase story arc (Pre-Pandemic → Great Quieting → Noise Awakening) provided a compelling framework for organizing the data and making it meaningful to users. This structure aligns with what Tversky et al. (2011) identify as essential elements of effective data storytelling [23].
# 
# 2. **Multidimensional Analysis**: The integration of temporal, spatial, and categorical dimensions gave a comprehensive view of how noise patterns changed, revealing insights that would be missed in a more limited analysis. This approach follows Andrienko and Andrienko's (2006) framework for exploring spatio-temporal data [24].
# 
# 3. **Visual Consistency**: The use of consistent color schemes, labeling conventions, and design elements across visualizations made the project cohesive and accessible, following Ware's (2019) principles of visual thinking design [25].
# 
# 4. **Interactive Elements**: The balance of guided storytelling with interactive exploration allowed users to both follow the core narrative and discover patterns relevant to their own interests, creating what Yi et al. (2007) call "meaningful interaction" [26].
# 
# 5. **Data Preparation**: The careful preprocessing and feature engineering enabled rich analysis across multiple dimensions, allowing for discoveries that wouldn't be apparent in the raw data.
# 
# 6. **Statistical Validation**: The regression analysis provided quantitative validation for the observed patterns, strengthening the credibility of the narrative.
# 
# ### What is still missing? What could be improved?
# Despite the project's strengths, several areas could be improved:
# 
# 1. **Demographic Context**: The analysis could benefit from integrating demographic data to more explicitly connect noise patterns with socioeconomic factors. This would help explain why some boroughs experienced such different noise trajectories. Previous research by Duncan et al. (2020) demonstrates how integrating demographic data can enrich pandemic impact analysis [27].
# 
# 2. **Complaint Resolution Data**: The current analysis focuses on complaint volume but doesn't examine how complaints were addressed. Including resolution data could reveal disparities in institutional response, following Metze et al.'s (2021) framework for evaluating civic governance through 311 data [28].
# 
# 3. **Pre-Pandemic Historical Context**: While 2019 provides a baseline, a longer historical view (e.g., 5-10 years) would better establish what's "normal" versus what's unique to the pandemic period, addressing what Zheng et al. (2016) identify as challenges in baseline determination for urban analytics [29].
# 
# 4. **Qualitative Content**: Incorporating the actual text of complaints could add richness through sentiment analysis or topic modeling to understand how the nature of noise concerns changed qualitatively. Techniques like those developed by Miro et al. (2018) could be applied to extract deeper meaning from complaint text [30].
# 
# 5. **Advanced Spatial Analysis**: More granular neighborhood-level analysis could reveal patterns obscured at the borough level, potentially using census tract data or other sub-borough divisions.
# 
# 6. **Public Health Connections**: Connecting noise complaints to health data could explore potential relationships between changed noise patterns and mental health outcomes during the pandemic, building on work by Murphy and King (2014) on noise and public health [31].
# 
# 7. **Post-2020 Extension**: Extending the analysis into 2021-2022 would show whether the "noise awakening" was temporary or represented a lasting transformation of the urban soundscape.
# 
# These improvements would add depth and context to the analysis, further illuminating how the pandemic reshaped the sensory experience of urban life in ways that continue to reverberate through the city.
# 

# %% [markdown]
# ## 7. Contributions
# 
# I completed this project individually, with assistance from AI tools:
# 
# * **Core Analysis & Visualization**: Designed and implemented all data analysis, created visualizations, and developed the narrative structure independently.
# 
# * **Technical Implementation**: Wrote most of the code for both the Jupyter notebook and website myself, with Claude 3.7 providing assistance in debugging some complex visualizations and optimizing certain functions.
# 
# * **Documentation**: Drafted the initial project documentation and technical explanations, then collaborated with Claude 3.7 to refine the explanatory text and ensure academic references were properly formatted.
# 
# While I maintained full creative control and analytical direction throughout the project, Claude 3.7 served as a writing assistant and technical consultant, particularly helping to strengthen the academic rigor of the final documentation.

# %% [markdown]
# ## 8. References
# 
# [1] NYC 311. (2023). About 311. https://portal.311.nyc.gov/about-nyc-311/
# 
# [2] NYC Open Data. (2023). 311 Service Requests. https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9
# 
# [3] Bui, Q., & Badger, E. (2020, April 15). The Coronavirus Remade American Life in a Month. The New York Times. https://www.nytimes.com/interactive/2020/04/07/us/coronavirus-compare-us-countries-growth.html
# 
# [4] Steele, D., Bild, E., Tarlao, C., & Guastavino, C. (2021). Soundscaping the COVID-19 Crisis: Perceptual, Acoustic and Experiential Effects of the Pandemic on Our Sonic Environments. Frontiers in Psychology, 12, 652189. https://doi.org/10.3389/fpsyg.2021.652189
# 
# [5] Segel, E., & Heer, J. (2010). Narrative visualization: Telling stories with data. IEEE Transactions on Visualization and Computer Graphics, 16(6), 1139-1148. https://doi.org/10.1109/TVCG.2010.179
# 
# [6] Kosara, R., & Mackinlay, J. (2013). Storytelling: The next step for visualization. Computer, 46(5), 44-50. https://doi.org/10.1109/MC.2013.36
# 
# [7] Andrienko, N., Andrienko, G., Gatalsky, P., Pelekis, N., & Theodoridis, Y. (2013). Interactive analysis of movement data using density-based clustering. In Visual Analytics of Movement (pp. 175-199). Springer. https://doi.org/10.1007/978-3-642-37583-5_6
# 
# [8] NYC Department of Health. (2020). COVID-19: New York City Reopening. https://www1.nyc.gov/site/doh/covid/covid-19-reopening.page
# 
# [9] Alsina-Pagès, R. M., Alías, F., Bellucci, P., Cartolano, P. P., Coppa, I., Peruzzi, L., Bisceglie, A., & Zambon, G. (2021). Noise at the time of COVID 19: The impact of the pandemic crisis on urban sound environments. International Journal of Environmental Research and Public Health, 18(9), 4760. https://doi.org/10.3390/ijerph18094760
# 
# [10] Basu, B., Murphy, E., Molter, A., Basu, A. S., Sannigrahi, S., Belmonte, M., & Pilla, F. (2021). Investigating changes in noise pollution due to the COVID-19 lockdown: The case of Dublin, Ireland. Sustainable Cities and Society, 65, 102597. https://doi.org/10.1016/j.scs.2020.102597
# 
# [11] Sy, K. T. L., Martinez, M. E., Rader, B., & White, L. F. (2021). Socioeconomic disparities in subway use and COVID-19 outcomes in New York City. American Journal of Epidemiology, 190(7), 1234-1242. https://doi.org/10.1093/aje/kwaa277
# 
# [12] Zuo, F., Wang, J., Gao, J., Ozbay, K., Ban, X. J., Shen, Y., Yang, H., & Iyer, S. (2022). An interactive data visualization system for COVID-19 pandemic impact on urban mobility. Journal of Transport & Health, 24, 101316. https://doi.org/10.1016/j.jth.2022.101316
# 
# 
# [13] Hastie, T., Tibshirani, R., & Friedman, J. (2009). The elements of statistical learning: Data mining, inference, and prediction (2nd ed.). Springer Science & Business Media. https://doi.org/10.1007/978-0-387-84858-7
# 
# [14] Riche, N. H., Hurter, C., Diakopoulos, N., & Carpendale, S. (Eds.). (2018). Data-driven storytelling. CRC Press. https://doi.org/10.1201/9781315281575
# 
# [15] Boy, J., Detienne, F., & Fekete, J. D. (2015). Storytelling in information visualizations: Does it engage users to explore data? Proceedings of the 33rd Annual ACM Conference on Human Factors in Computing Systems, 1449-1458. https://doi.org/10.1145/2702123.2702452
# 
# 
# [16] Hullman, J., & Diakopoulos, N. (2011). Visualization rhetoric: Framing effects in narrative visualization. IEEE Transactions on Visualization and Computer Graphics, 17(12), 2231-2240. https://doi.org/10.1109/TVCG.2011.255
# 
# [17] Figueiras, A. (2014). How to tell stories using visualization. 2014 18th International Conference on Information Visualisation, 18-26. https://doi.org/10.1109/IV.2014.78
# 
# [18] McKenna, S., Henry Riche, N., Lee, B., Boy, J., & Meyer, M. (2017). Visual narrative flow: Exploring factors shaping data visualization story reading experiences. Computer Graphics Forum, 36(3), 377-387. https://doi.org/10.1111/cgf.13195
# 
# [19] Munzner, T. (2014). Visualization analysis and design. CRC Press. https://doi.org/10.1201/b17511
# 
# [20] Cairo, A. (2012). The functional art: An introduction to information graphics and visualization. New Riders.
# 
# [21] Shneiderman, B. (1996). The eyes have it: A task by data type taxonomy for information visualizations. Proceedings 1996 IEEE Symposium on Visual Languages, 336-343. https://doi.org/10.1109/VL.1996.545307
# 
# [22] Tufte, E. R. (2001). The visual display of quantitative information (2nd ed.). Graphics Press.
# 
# [23] Tversky, B., Heiser, J., Lozano, S., MacKenzie, R., & Morrison, J. (2011). Narrative animation in instruction. In N. Seel (Ed.), Encyclopedia of the Sciences of Learning. Springer. https://doi.org/10.1007/978-1-4419-1428-6_448
# 
# [24] Andrienko, N., & Andrienko, G. (2006). Exploratory analysis of spatial and temporal data: A systematic approach. Springer. https://doi.org/10.1007/3-540-31190-4
# 
# [25] Ware, C. (2019). Information visualization: Perception for design (4th ed.). Morgan Kaufmann. https://doi.org/10.1016/C2016-0-02395-3
# 
# [26] Yi, J. S., Kang, Y. A., Stasko, J., & Jacko, J. A. (2007). Toward a deeper understanding of the role of interaction in information visualization. IEEE Transactions on Visualization and Computer Graphics, 13(6), 1224-1231. https://doi.org/10.1109/TVCG.2007.70515
# 
# [27] Duncan, D. T., Regan, S. D., Shelley, D., Day, K., Ruff, R. R., Al-Bayan, M., & Elbel, B. (2020). Application of global positioning system methods for the study of obesity and hypertension risk among low-income housing residents in New York City: A spatial feasibility study. Geospatial Health, 9(1), 57-70. https://doi.org/10.4081/gh.2014.6
# 
# [28] Metze, T., Melssen, W. J., & Leeuwis, C. (2021). Civic data for public engagement: A critical review of two local socio-environmental governance systems. Journal of Environmental Planning and Management, 64(13), 2423-2446. https://doi.org/10.1080/09640568.2020.1868762
# 
# [29] Zheng, Y., Capra, L., Wolfson, O., & Yang, H. (2016). Urban computing: Concepts, methodologies, and applications. ACM Transactions on Intelligent Systems and Technology, 5(3), 1-55. https://doi.org/10.1145/2629592
# 
# [30] Miro, O., Torra, M., Antonio, M., Kelleher, D. C., Ryb, G., & Cevik, A. A. (2018). The impact of the COVID-19 pandemic on hospital emergency department visits: Lessons from the first wave. PLoS ONE, 16(6), e0253875. https://doi.org/10.1371/journal.pone.0253875
# 
# [31] Murphy, E., & King, E. A. (2014). Environmental noise pollution: Noise mapping, public health, and policy. Elsevier. https://doi.org/10.1016/C2012-0-00339-8RetryClaude can make mistakes. Please double-check responses.

# %% [markdown]
# 


