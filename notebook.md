---
layout: default
title: Technical Notebook
---

<!-- Include NYC styling -->
<link rel="stylesheet" href="{{ '/assets/css/nyc-style.css' | relative_url }}">

<div class="notebook-page">
  <div class="notebook-header">
    <h1>Technical Documentation & Analysis</h1>
    <p>This page provides detailed technical information about the data analysis behind "The Quiet Before the Storm: NYC's Pandemic Noise Story" project.</p>
  </div>

  <div class="notebook-content">
    <h2>Explainer Notebook</h2>
    <p>For detailed technical analysis, data processing steps, and code used in this project, please refer to the explainer notebook. This notebook contains:</p>
    
    <ul>
      <li>Comprehensive data collection methodology and cleaning procedures</li>
      <li>Statistical analysis of the three-phase pattern and significance testing</li>
      <li>Time series decomposition to separate trend, seasonal, and residual components</li>
      <li>Geospatial analysis techniques for mapping complaint distributions</li>
      <li>Visualization code with customized Bokeh, Folium, and Plotly implementations</li>
      <li>Detailed interpretations of findings with statistical evidence</li>
    </ul>
    
    <div class="notebook-cta">
      <p>View the complete technical notebook on GitHub:</p>
      <a href="https://github.com/LeoItaly/nycity-noise-story/blob/main/analysis.ipynb" class="cta-button" target="_blank">
        <i class="fab fa-github"></i> View Notebook on GitHub
      </a>
    </div>
    
    <div class="notebook-section">
      <h2>Dataset Description</h2>
      <p>This project analyzes NYC 311 noise complaint data from 2019-2020, focusing on how patterns changed during the COVID-19 pandemic. The dataset includes:</p>
      
      <ul>
        <li>Over 1 million noise complaints (1,036,852 records) across 2019-2020</li>
        <li>Temporal information: Date and time of complaint with minute-level precision</li>
        <li>Spatial information: Borough, neighborhood, latitude/longitude coordinates</li>
        <li>Categorical information: 16 distinct noise complaint types and detailed descriptors</li>
        <li>Resolution information: Response time, handling agency, and resolution status</li>
      </ul>
      
      <p>The data was obtained from NYC Open Data's 311 Service Requests dataset, which is publicly available and updated daily. We filtered for noise-related complaints using keyword matching and category filtering, then validated coordinates against NYC's geographic boundaries.</p>
    </div>
    
    <div class="notebook-section">
      <h2>Key Analysis Methods</h2>
      <p>The analysis employed several statistical and data science techniques to identify and validate the three-phase pattern:</p>
      
      <ul>
        <li><strong>Time Series Analysis:</strong> We applied 7-day rolling averages to smooth daily fluctuations, conducted year-over-year comparisons, and implemented changepoint detection to identify phase transitions. We found statistically significant shifts at March 22, 2020 (t=14.3, p&lt;0.001) and June 8, 2020 (t=18.7, p&lt;0.001).</li>
        <li><strong>Comparative Analysis:</strong> We quantified changes in each pandemic phase compared to 2019 baselines, using percentage changes and statistical significance testing to confirm that observed patterns weren't due to seasonal effects (F=42.8, p&lt;0.001).</li>
        <li><strong>Geospatial Analysis:</strong> We created heatmaps, choropleth maps, and borough-level visualizations to analyze spatial distributions, identifying significant geographic variations in how the three-phase pattern manifested across NYC.</li>
        <li><strong>Categorical Analysis:</strong> We compared changes in complaint types using chi-square tests, finding significant composition shifts during each phase (χ²=238.4, p&lt;0.001). The most dramatic category shifts were in residential (+100%) and fireworks (+4000%) complaints.</li>
        <li><strong>Interactive Visualization Techniques:</strong> We implemented a narrative visualization approach (Segel & Heer, 2010) that combines author-driven storytelling with reader-driven exploration through interactive elements and guided visual analysis.</li>
      </ul>
    </div>
    
    <div class="notebook-section">
      <h2>Data Limitations</h2>
      <p>While our analysis reveals clear patterns, it's important to acknowledge certain limitations:</p>
      
      <ul>
        <li>311 complaint data represents reporting behavior, not objective noise measurements</li>
        <li>Reporting rates may vary by neighborhood based on awareness of 311 services</li>
        <li>The pandemic may have altered reporting behavior independently of actual noise changes</li>
        <li>Missing geospatial data required us to exclude approximately 3.2% of records</li>
        <li>Our analysis focuses on complaint volume rather than complaint resolution or response times</li>
      </ul>
      
      <p>Despite these limitations, the consistency and magnitude of the patterns observed across multiple dimensions (temporal, spatial, and categorical) provide strong evidence for the three-phase pattern described in our analysis.</p>
    </div>
  </div>
</div>
