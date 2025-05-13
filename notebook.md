---
layout: default
title: Technical Notebook
---

<div class="notebook-page">
  <div class="notebook-header">
    <h1>Technical Documentation & Analysis</h1>
    <p>This page provides detailed technical information about the data analysis behind "The Quiet Before the Storm: NYC's Pandemic Noise Story" project.</p>
  </div>

  <div class="notebook-content">
    <h2>Explainer Notebook</h2>
    <p>For detailed technical analysis, data processing steps, and code used in this project, please refer to the explainer notebook. This notebook contains:</p>
    
    <ul>
      <li>Data collection methodology and sources</li>
      <li>Data cleaning and preprocessing steps</li>
      <li>Statistical analysis methods</li>
      <li>Visualization code and techniques</li>
      <li>Detailed interpretations of findings</li>
    </ul>
    
    <div class="notebook-cta">
      <p>View the complete technical notebook on GitHub:</p>
      <a href="https://github.com/LeoItaly/nycity-noise-story/blob/main/notebook.ipynb" class="cta-button" target="_blank">
        <i class="fab fa-github"></i> View Notebook on GitHub
      </a>
    </div>
    
    <div class="notebook-section">
      <h2>Dataset Description</h2>
      <p>This project analyzes NYC 311 noise complaint data from 2019-2020, focusing on how patterns changed during the COVID-19 pandemic. The dataset includes:</p>
      
      <ul>
        <li>Over 1 million noise complaints</li>
        <li>Temporal information (date/time of complaint)</li>
        <li>Spatial information (borough, neighborhood, coordinates)</li>
        <li>Categorical information (complaint type, descriptor)</li>
        <li>Resolution information (response time, agency, etc.)</li>
      </ul>
      
      <p>The data was obtained from NYC Open Data's 311 Service Requests dataset, which is publicly available and updated daily.</p>
    </div>
    
    <div class="notebook-section">
      <h2>Key Analysis Methods</h2>
      <p>The analysis employed several statistical and data science techniques:</p>
      
      <ul>
        <li><strong>Time Series Analysis:</strong> To identify changes in complaint patterns over time</li>
        <li><strong>Comparative Analysis:</strong> Year-over-year comparisons to account for seasonal effects</li>
        <li><strong>Geospatial Analysis:</strong> Examining spatial distributions and neighborhood disparities</li>
        <li><strong>Categorical Analysis:</strong> Investigating changes in the types of noise complaints</li>
        <li><strong>Data Visualization:</strong> Using interactive and static visualizations to communicate findings</li>
      </ul>
    </div>
  </div>
</div>

<style>
  .notebook-page {
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px;
  }
  
  .notebook-header {
    margin-bottom: 40px;
    border-bottom: 1px solid #eaeaea;
    padding-bottom: 20px;
  }
  
  .notebook-header h1 {
    margin-bottom: 10px;
  }
  
  .notebook-content {
    font-size: 16px;
    line-height: 1.6;
  }
  
  .notebook-section {
    margin: 40px 0;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
  }
  
  .notebook-section h2 {
    margin-top: 0;
  }
  
  .notebook-cta {
    margin: 40px 0;
    text-align: center;
    padding: 30px;
    background-color: #f5f5f5;
    border-radius: 8px;
  }
  
  .notebook-cta p {
    margin-bottom: 15px;
    font-size: 18px;
  }
</style>
