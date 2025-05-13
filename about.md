---
layout: default
title: About
---

<!-- Include NYC styling -->
<link rel="stylesheet" href="{{ '/assets/css/nyc-style.css' | relative_url }}">

<div class="about-page">
  <div class="about-header">
    <h1>About This Project</h1>
  </div>

  <div class="about-content">
    <h2>Project Overview</h2>
    <p>"The Quiet Before the Storm: NYC's Pandemic Noise Story" is a data visualization project that explores how New York City's noise complaints transformed during the COVID-19 pandemic. The project analyzes over 1 million 311 noise complaint records from 2019-2020 to reveal a distinct three-phase pattern in urban soundscapes: Pre-Pandemic Normal, The Great Quieting, and The Noise Awakening.</p>
    
    <div class="about-section">
      <h2>Methodology</h2>
      <p>This project uses data from NYC Open Data's 311 Service Requests dataset, focusing specifically on noise-related complaints. The analysis follows a structured approach to uncover temporal, spatial, and categorical patterns:</p>
      
      <ul>
        <li><strong>Data Collection and Preprocessing:</strong> We extracted and cleaned 1,036,852 noise complaints from the NYC 311 dataset spanning Jan 2019-Dec 2020. We filtered by complaint type, standardized borough names, and validated geospatial coordinates.</li>
        <li><strong>Temporal Analysis:</strong> We examined daily, weekly, and monthly complaint patterns, creating comparative year-over-year visualizations to identify significant changes during each pandemic phase.</li>
        <li><strong>Spatial Analysis:</strong> We mapped complaint distributions across the five boroughs and created choropleth maps to visualize geographic patterns and borough-level differences.</li>
        <li><strong>Categorical Analysis:</strong> We analyzed changes in specific noise types (residential, commercial, construction, etc.) to understand how complaint composition shifted throughout the pandemic.</li>
        <li><strong>Statistical Significance Testing:</strong> We applied time-series analysis and statistical tests to confirm that observed changes were significant and not due to normal seasonal variations.</li>
        <li><strong>Interactive Visualization Development:</strong> We created 12 interactive visualizations using Bokeh, Folium, and other tools to enable exploration of the three-phase pattern from multiple perspectives.</li>
      </ul>
      
      <p>For a detailed technical explanation of the methodology, please refer to the <a href="{{ '/notebook' | relative_url }}">Technical Notebook</a>.</p>
    </div>
    
    <div class="about-section">
      <h2>Project Inspiration</h2>
      <p>This project was inspired by personal observations of how urban soundscapes changed during the pandemic. As streets emptied, businesses closed, and people stayed home, cities around the world experienced unprecedented transformations in their acoustic environments.</p>
      
      <p>NYC's comprehensive 311 complaint data offered a unique opportunity to quantify these changes and explore how they varied across different neighborhoods and time periods. The findings reveal not just changes in noise levels, but also deeper insights about how urban noise patterns shifted during each phase of the pandemic response.</p>
      
      <p>Our approach to this project was informed by narrative visualization principles from Segel & Heer's "Narrative Visualization: Telling Stories with Data" (2010), creating a balance between author-driven storytelling and reader-driven exploration through interactive elements.</p>
    </div>
    
    <div class="about-section">
      <h2>About the Author</h2>
      <p>This project was created as part of the Social Data Analysis and Visualization course at the Technical University of Denmark (DTU). The analysis was conducted using Python with libraries including Pandas, Matplotlib, Bokeh, and Folium.</p>
      
      <div class="contact-links">
        <a href="https://github.com/LeoItaly/nycity-noise-story" target="_blank" class="contact-link">
          <i class="fab fa-github"></i> GitHub Repository
        </a>
      </div>
    </div>
    
    <div class="about-section">
      <h2>Data Sources</h2>
      <p>This project relies on the following data sources:</p>
      
      <ul>
        <li><a href="https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9" target="_blank">NYC 311 Service Requests</a> - The primary dataset containing noise complaints</li>
        <li><a href="https://data.cityofnewyork.us/resource/erm2-nwe9.csv" target="_blank">NYC 311 Service Requests (CSV)</a> - Direct access to the dataset in CSV format</li>
        <li><a href="https://data.cityofnewyork.us/City-Government/Borough-Boundaries/tqmj-j8zm" target="_blank">NYC Borough Boundaries</a> - Geographic data for mapping</li>
        <li><a href="https://data.cityofnewyork.us/resource/gthc-hcne.geojson" target="_blank">NYC Borough Boundaries (GeoJSON)</a> - Direct access to the borough boundaries in GeoJSON format</li>
        <li><a href="https://data.cityofnewyork.us/City-Government/Neighborhood-Tabulation-Areas-NTA-/cpf4-rkhq" target="_blank">NYC Neighborhood Tabulation Areas</a> - For neighborhood-level analysis</li>
      </ul>
    </div>
    
    <div class="about-section">
      <h2>Acknowledgements</h2>
      <p>Special thanks to:</p>
      
      <ul>
        <li>The instructors and teaching assistants of the Social Data Analysis and Visualization course at DTU</li>
        <li>NYC Open Data for making comprehensive urban data publicly available</li>
        <li>The open-source communities behind Python, Pandas, Bokeh, Folium, and other tools used in this project</li>
      </ul>
    </div>
  </div>
</div>
