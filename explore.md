---
layout: default
title: Explore the Data
---

<div class="explore-page">
  <div class="explore-header">
    <h1>Interactive Data Exploration</h1>
    <p>Dive deeper into NYC's noise complaint data with these interactive visualizations. Filter, sort, and explore the data to discover your own insights about how the pandemic transformed the city's soundscape.</p>
    
    <div class="storyline-connection">
      <div class="connection-icon"><i class="fas fa-link"></i></div>
      <div class="connection-text">
        <h3>Continuing from "The Quiet Before the Storm"</h3>
        <p>These visualizations allow you to explore in greater detail the data presented in the main story. Use these tools to answer your own questions about how NYC's noise landscape changed during the pandemic.</p>
      </div>
    </div>
  </div>

  <div class="explore-tabs">
    <button class="tab-button active" data-tab="time">Temporal Patterns</button>
    <button class="tab-button" data-tab="location">Spatial Analysis</button>
  </div>

  <div class="tab-content" id="time-content">
    <h2>Exploring Noise Complaints Over Time</h2>
    <p>Examine how noise complaints changed throughout 2019-2020, with special focus on the pandemic phases.</p>
    
    <div class="viz-container large">
      <iframe src="{{ '/assets/visualizations/category_composition_stacked_area.html' | relative_url }}" width="100%" height="500px" frameborder="0"></iframe>
      <div class="viz-caption">
        <i class="fas fa-info-circle"></i> <strong>Interactive:</strong> Stacked area chart showing the changing composition of noise complaint categories over time
      </div>
    </div>
    
    <div class="key-findings">
      <h3>Key Temporal Patterns</h3>
      <ul>
        <li>Overall complaints dropped by ~20% during initial lockdown (March-May 2020)</li>
        <li>Complaints surged by ~50% during reopening (June-December 2020)</li>
        <li>The composition of noise categories shifted dramatically during different pandemic phases</li>
        <li>Residential noise complaints increased during lockdown while commercial noise decreased</li>
        <li>Street/Sidewalk noise saw a significant surge during the reopening phase</li>
      </ul>
    </div>
  </div>

  <div class="tab-content" id="location-content" style="display: none;">
    <h2>Spatial Distribution of Noise Complaints</h2>
    <p>Explore how noise complaints varied across different boroughs and neighborhoods during pandemic phases.</p>
    
    <div class="viz-container full-width large">
      <iframe src="{{ '/assets/visualizations/nyc_noise_by_borough_phase.html' | relative_url }}" width="100%" height="500px" frameborder="0"></iframe>
      <div class="viz-caption">
        <i class="fas fa-map-marked-alt"></i> <strong>Interactive Visualization:</strong> Compare noise complaint patterns across boroughs during different pandemic phases
      </div>
    </div>
    
    <div class="viz-container full-width large">
      <iframe src="{{ '/assets/visualizations/borough_choropleth_map.html' | relative_url }}" width="100%" height="500px" frameborder="0"></iframe>
      <div class="viz-caption">
        <i class="fas fa-map-marked-alt"></i> <strong>Interactive Map:</strong> Click on boroughs to explore detailed neighborhood-level data
      </div>
    </div>
    
    <div class="key-findings">
      <h3>Key Spatial Insights</h3>
      <ul>
        <li>Manhattan saw the largest decrease during lockdown (-35%)</li>
        <li>The Bronx experienced minimal reduction during lockdown (-5%)</li>
        <li>Lower-income neighborhoods saw greater increases during reopening</li>
        <li>Brooklyn and Queens showed similar patterns but with different magnitudes</li>
        <li>Staten Island consistently had the lowest overall complaint volume</li>
      </ul>
    </div>
  </div>
</div>

<style>
  .explore-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 20px;
  }
  
  .explore-header {
    margin-bottom: 40px;
    text-align: center;
  }
  
  /* Storyline connection box */
  .storyline-connection {
    display: flex;
    align-items: center;
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 20px;
    margin: 30px auto;
    max-width: 800px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    text-align: left;
    border-left: 4px solid var(--primary-blue);
  }
  
  .connection-icon {
    font-size: 2rem;
    color: var(--primary-blue);
    margin-right: 20px;
    flex-shrink: 0;
  }
  
  .connection-text h3 {
    margin-top: 0;
    font-size: 1.2rem;
    color: #333;
  }
  
  .connection-text p {
    margin-bottom: 0;
    font-size: 0.95rem;
    color: #666;
  }
  
  /* Visualization captions */
  .viz-caption {
    padding: 8px 12px;
    background: #f5f5f5;
    border-top: 1px solid #eee;
    font-size: 0.8rem;
    color: #666;
  }
  
  .viz-caption i {
    color: var(--primary-blue);
  }
  
  .explore-tabs {
    display: flex;
    justify-content: center;
    margin-bottom: 30px;
    border-bottom: 1px solid #ddd;
  }
  
  .tab-button {
    padding: 12px 20px;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    color: #666;
    transition: all 0.3s ease;
    position: relative;
  }
  
  .tab-button:after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 100%;
    height: 3px;
    background-color: var(--primary-blue);
    transform: scaleX(0);
    transition: transform 0.3s ease;
  }
  
  .tab-button.active {
    color: var(--primary-blue);
  }
  
  .tab-button.active:after {
    transform: scaleX(1);
  }
  
  .tab-content {
    margin-bottom: 60px;
  }
  
  .key-findings {
    margin-top: 30px;
    padding: 20px;
    background-color: #f5f5f5;
    border-left: 4px solid var(--primary-blue);
    border-radius: 0 4px 4px 0;
  }
  
  .key-findings h3 {
    margin-top: 0;
    color: #333;
  }
  
  @media (max-width: 768px) {
    .explore-tabs {
      flex-wrap: wrap;
    }
    
    .tab-button {
      padding: 10px 15px;
      font-size: 14px;
    }
    
    .storyline-connection {
      flex-direction: column;
      text-align: center;
    }
    
    .connection-icon {
      margin-right: 0;
      margin-bottom: 15px;
    }
  }
</style>

<script>
  document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
      button.addEventListener('click', function() {
        // Update active tab button
        tabButtons.forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
        
        // Show corresponding tab content
        const tabId = this.getAttribute('data-tab');
        tabContents.forEach(content => {
          content.style.display = 'none';
        });
        document.getElementById(`${tabId}-content`).style.display = 'block';
        
        // Update URL hash without scrolling
        history.replaceState(null, null, `#${tabId}`);
      });
    });
    
    // Check URL hash on page load
    if (location.hash) {
      const tabId = location.hash.substring(1);
      const tabButton = document.querySelector(`.tab-button[data-tab="${tabId}"]`);
      if (tabButton) {
        tabButton.click();
      }
    }
    
    // Add smooth entrance animation
    const exploreHeader = document.querySelector('.explore-header');
    if (exploreHeader) {
      setTimeout(() => {
        exploreHeader.style.opacity = '1';
        exploreHeader.style.transform = 'translateY(0)';
      }, 100);
    }
  });
</script>
