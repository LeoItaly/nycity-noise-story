---
layout: default
title: Explore NYC Noise Data
---

<!-- Include NYC styling -->
<link rel="stylesheet" href="{{ '/assets/css/nyc-style.css' | relative_url }}">

<div class="explore-page">
  <div class="explore-header">
    <h1>Explore the Data</h1>
    <p>Dive deeper into NYC's noise complaint patterns during the pandemic</p>
  </div>

  <div class="exploration-intro">
    <p>This interactive exploration space allows you to investigate NYC's noise patterns during the pandemic through multiple perspectives. Use the visualizations below to discover patterns by borough, noise type, and time period.</p>
    
    <div class="viz-legend">
      <div class="legend-item manhattan" data-category="manhattan">
        <div class="legend-color"></div>
        <div class="legend-label">Manhattan</div>
      </div>
      <div class="legend-item brooklyn" data-category="brooklyn">
        <div class="legend-color"></div>
        <div class="legend-label">Brooklyn</div>
      </div>
      <div class="legend-item queens" data-category="queens">
        <div class="legend-color"></div>
        <div class="legend-label">Queens</div>
      </div>
      <div class="legend-item bronx" data-category="bronx">
        <div class="legend-color"></div>
        <div class="legend-label">Bronx</div>
      </div>
      <div class="legend-item staten-island" data-category="staten-island">
        <div class="legend-color"></div>
        <div class="legend-label">Staten Island</div>
      </div>
    </div>
  </div>

  <div class="explore-tabs">
    <button class="tab-button active" data-tab="tab1">Geographic Patterns</button>
    <button class="tab-button" data-tab="tab2">Noise Types</button>
    <button class="tab-button" data-tab="tab3">Time Trends</button>
  </div>

  <div class="tab-content" id="tab1">
    <div class="exploration-section">
      <h2>Geographic Patterns of Noise</h2>
      
      <div class="viz-container large">
        <iframe src="{{ '/assets/visualizations/borough_choropleth_map.html' | relative_url }}" width="100%" height="600px" frameborder="0"></iframe>
        <div class="viz-caption">
          <i class="fas fa-map-marked-alt"></i> <strong>Interactive Map:</strong> Explore the geographic distribution of noise complaints across NYC's five boroughs. Click on a borough to see detailed statistics.
        </div>
      </div>
      
      <div class="exploration-insight">
        <h3><i class="fas fa-lightbulb"></i> Key Geographic Insights</h3>
        <ul>
          <li>The <span class="bronx-mention">Bronx</span> saw the most dramatic increase in noise complaints during reopening (+166%)</li>
          <li><span class="manhattan-mention">Manhattan</span> experienced the biggest drop during lockdown (-32%)</li>
          <li>All boroughs saw increases in the reopening phase, but with significantly different magnitudes</li>
          <li>Lower-income areas like the Bronx had a more modest initial decrease but a much larger subsequent surge, pointing to socioeconomic factors</li>
          <li>Staten Island consistently maintained the lowest complaint volume but still saw a substantial +58.9% increase during reopening</li>
          <li>Brooklyn (+147.5%) and Queens (+138.9%) showed similar patterns in noise complaint increases during reopening</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="tab-content" id="tab2" style="display:none;">
    <div class="exploration-section">
      <h2>Noise Complaint Categories</h2>
      
      <div class="viz-container">
        <iframe src="{{ '/assets/visualizations/noise_category_mix.html' | relative_url }}" width="100%" height="500px" frameborder="0"></iframe>
        <div class="viz-caption">
          <i class="fas fa-sliders-h"></i> <strong>Interactive:</strong> Compare noise categories by borough and year. Use the controls to switch between 2019 and 2020 data.
        </div>
      </div>
      
      <div class="exploration-insight">
        <h3><i class="fas fa-lightbulb"></i> Key Category Insights</h3>
        <ul>
          <li>"Residential" noise became the dominant category across all boroughs during reopening</li>
          <li>"Commercial" noise complaints plummeted during lockdown (-65%)</li>
          <li>"Street/Sidewalk" noise emerged as a major category during reopening, particularly in <span class="manhattan-mention">Manhattan</span></li>
          <li>Helicopter noise saw the largest percentage increase (+248.5%), possibly related to increased surveillance and medical transport</li>
          <li>Park noise increased substantially (+110.1%) as residents sought outdoor recreation options</li>
          <li>The composition of noise categories shifted dramatically: residential noise increased from 35% to 62% of all complaints during lockdown</li>
          <li>Statistical analysis showed strong positive correlations (0.88) between street noise and residential noise, suggesting outdoor activity increases led to indoor complaint rises</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="tab-content" id="tab3" style="display:none;">
    <div class="exploration-section">
      <h2>Temporal Patterns & Trends</h2>
      
      <div class="viz-container large">
        <iframe src="{{ '/assets/visualizations/nyc_noise_by_borough_phase.html' | relative_url }}" width="100%" height="600px" frameborder="0"></iframe>
        <div class="viz-caption">
          <i class="fas fa-chart-line"></i> <strong>Time Series:</strong> Observe how each borough's noise patterns evolved through the pandemic phases. Hover for detailed values.
        </div>
      </div>
      
      <div class="exploration-insight">
        <h3><i class="fas fa-lightbulb"></i> Key Temporal Insights</h3>
        <ul>
          <li>Weekend noise complaints showed the most dramatic increase during reopening (+124%)</li>
          <li>Night-time noise (10pm-6am) saw a sustained rise from June 2020 onward</li>
          <li>Seasonal patterns were disrupted by pandemic phases, overwhelming traditional trends</li>
          <li>The overall complaint volume saw a 69.5% increase from 2019 to 2020</li>
          <li>Pre-COVID (2019) period averaged ~663 complaints per day</li>
          <li>Early Lockdown (Mar-May 2020) period averaged ~540 complaints per day (-18.6%)</li>
          <li>Reopening (Jun-Dec 2020) period surged to ~1,135 complaints per day (+71.2%)</li>
          <li>The peak complaint surge occurred on June 20, 2020, with a 152.4% increase compared to 2019</li>
          <li>Traditional weekend/weekday patterns disappeared during lockdown as work-from-home became widespread</li>
          <li>The noise surge began precisely in the first week of June 2020, coinciding with Phase 1 reopening preparations</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  // Tab functionality
  const tabButtons = document.querySelectorAll('.tab-button');
  const tabContents = document.querySelectorAll('.tab-content');
  
  tabButtons.forEach(button => {
    button.addEventListener('click', function() {
      // Remove active class from all buttons
      tabButtons.forEach(btn => btn.classList.remove('active'));
      // Add active class to clicked button
      this.classList.add('active');
      
      // Hide all tab contents
      tabContents.forEach(content => {
        content.style.display = 'none';
      });
      
      // Show the selected tab content
      const tabId = this.getAttribute('data-tab');
      document.getElementById(tabId).style.display = 'block';
    });
  });
});
</script>
