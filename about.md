---
layout: default
title: About
---

<div class="about-page">
  <div class="about-header">
    <h1>About This Project</h1>
  </div>

  <div class="about-content">
    <h2>Project Overview</h2>
    <p>"The Quiet Before the Storm: NYC's Pandemic Noise Story" is a data visualization project that explores how New York City's noise complaints transformed during the COVID-19 pandemic. The project analyzes over 1 million 311 noise complaint records from 2019-2020 to reveal patterns in urban soundscapes and neighborhood inequalities.</p>
    
    <div class="about-section">
      <h2>Methodology</h2>
      <p>This project uses data from NYC Open Data's 311 Service Requests dataset, focusing specifically on noise-related complaints. The analysis involves:</p>
      
      <ul>
        <li>Data cleaning and preprocessing of raw 311 service request data</li>
        <li>Temporal analysis of complaint patterns before, during, and after lockdown</li>
        <li>Spatial analysis of complaint distributions across boroughs and neighborhoods</li>
        <li>Categorical analysis of different types of noise complaints</li>
        <li>Interactive visualizations created with Bokeh, Folium, and other tools</li>
      </ul>
      
      <p>For a detailed technical explanation of the methodology, please refer to the <a href="{{ '/notebook' | relative_url }}">Technical Notebook</a>.</p>
    </div>
    
    <div class="about-section">
      <h2>Project Inspiration</h2>
      <p>This project was inspired by personal observations of how urban soundscapes changed during the pandemic. As streets emptied, businesses closed, and people stayed home, cities around the world experienced unprecedented transformations in their acoustic environments.</p>
      
      <p>NYC's comprehensive 311 complaint data offered a unique opportunity to quantify these changes and explore how they varied across different neighborhoods and time periods. The findings reveal not just changes in noise levels, but also deeper insights about urban life, community resilience, and social inequality.</p>
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

<style>
  .about-page {
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px;
  }
  
  .about-header {
    margin-bottom: 40px;
    border-bottom: 1px solid #eaeaea;
    padding-bottom: 20px;
  }
  
  .about-content {
    font-size: 16px;
    line-height: 1.6;
  }
  
  .about-section {
    margin: 40px 0;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
  }
  
  .about-section h2 {
    margin-top: 0;
  }
  
  .contact-links {
    margin-top: 20px;
    display: flex;
    gap: 15px;
  }
  
  .contact-link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background-color: #f1f1f1;
    border-radius: 4px;
    text-decoration: none;
    color: #333;
    font-weight: 600;
    transition: background-color 0.2s ease;
  }
  
  .contact-link:hover {
    background-color: #e5e5e5;
    text-decoration: none;
  }
</style>
