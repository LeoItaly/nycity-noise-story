---
layout: default
title: Home
---

<!-- Story Navigation Guide -->
<div class="story-guide">
  <div class="guide-content">
    <i class="fas fa-map-signs"></i>
    <h3>How to Navigate This Story</h3>
    <p>Scroll down to journey through NYC's changing soundscape during the pandemic. Interactive visualizations and key insights will guide you through this three-phase story.</p>
    <div class="guide-instructions">
      <div class="guide-item">
        <i class="fas fa-mouse"></i>
        <span>Scroll to navigate</span>
      </div>
      <div class="guide-item">
        <i class="fas fa-hand-pointer"></i>
        <span>Click visualizations to explore</span>
      </div>
      <div class="guide-item">
        <i class="fas fa-circle-dot"></i>
        <span>Use the side navigation to jump between sections</span>
      </div>
    </div>
    <button class="guide-close"><i class="fas fa-times"></i></button>
  </div>
</div>

<!-- Progress Navigation -->
<nav class="progress-nav">
  <a href="#landing" data-title="Introduction"></a>
  <a href="#story-intro" data-title="The Three-Phase Story"></a>
  <a href="#great-quieting" data-title="The Great Quieting"></a>
  <a href="#borough-disparities" data-title="Borough Disparities"></a>
  <a href="#noise-awakening" data-title="The Noise Awakening"></a>
  <a href="#explore" data-title="Explore the Data"></a>
  <a href="#findings" data-title="Key Findings"></a>
</nav>

<div class="slide-container">
  <!-- Landing Slide -->
  <section id="landing" class="slide">
    <div class="slide-content">
      <h1 class="slide-title fade-in">The Quiet Before the Storm</h1>
      <h2 class="slide-subtitle fade-in">NYC's Pandemic Noise Story</h2>
      
      <p class="fade-in">
        In early 2020, as COVID-19 swept through New York City, the bustling metropolis experienced a dramatic transformation in its soundscape. What followed was a fascinating three-part story of silence and noise that revealed surprising patterns about urban life and neighborhood inequalities.
      </p>
      
      <div class="viz-container large fade-in">
        <iframe src="{{ '/assets/visualizations/bar_chart_race.html' | relative_url }}" width="100%" height="500px" frameborder="0"></iframe>
        <div class="viz-caption">
          <i class="fas fa-chart-bar"></i> <strong>Animation:</strong> Watch how noise complaints evolved month by month through the pandemic
        </div>
      </div>
      
      <div class="timeline-nav fade-in">
        <div class="timeline-point timeline-point-pre-pandemic active" data-target="story-intro">
          <div class="timeline-label"></div>
        </div>
        <div class="timeline-point timeline-point-lockdown" data-target="great-quieting">
          <div class="timeline-label"></div>
        </div>
        <div class="timeline-point timeline-point-reopening" data-target="noise-awakening">
          <div class="timeline-label"></div>
        </div>
      </div>
      
      <div class="scroll-indicator fade-in">
        <i class="fas fa-chevron-down"></i>
      </div>
    </div>
  </section>
  
  <!-- Introduction Slide -->
  <section id="story-intro" class="slide">
    <div class="slide-content">
      <h2 class="slide-title fade-in">The Three-Phase Story</h2>
      
      <p class="fade-in">
        New York City's noise complaint data tells a compelling story about how the COVID-19 pandemic reshaped urban soundscapes. By analyzing over 1 million 311 noise complaints from 2019-2020, we can trace a clear three-phase pattern that unfolded as the city navigated through crisis.
      </p>
      
      <div class="viz-container fade-in">
        <iframe src="{{ '/assets/visualizations/nyc_noise_timeseries.html' | relative_url }}" width="100%" height="500px" frameborder="0"></iframe>
        <div class="viz-caption">
          <i class="fas fa-info-circle"></i> <strong>Interactive:</strong> Hover over the timeline to see specific values and phase transitions
        </div>
      </div>
      
      <div class="key-finding fade-in">
        <h3>What's a 311 Noise Complaint?</h3>
        <p>NYC's 311 system allows residents to report non-emergency issues, including noise disturbances. These complaints are categorized by type (construction, music, parties, etc.) and provide valuable data about urban quality of life.</p>
        <div class="data-point"><span class="data-value">1M+</span> Noise complaints analyzed</div>
      </div>
      
      <p class="fade-in">
        The data reveals three distinct phases in NYC's pandemic soundscape:
      </p>
      
      <div class="story-phases fade-in">
        <div class="phase-card phase-pre">
          <div class="phase-icon"><i class="fas fa-city"></i></div>
          <h4>Pre-Pandemic Normal</h4>
          <p>Jan-Feb 2020: Typical noise patterns consistent with previous years</p>
        </div>
        <div class="phase-card phase-lockdown">
          <div class="phase-icon"><i class="fas fa-volume-mute"></i></div>
          <h4>The Great Quieting</h4>
          <p>Mar-May 2020: Initial lockdown period with significantly reduced complaints</p>
        </div>
        <div class="phase-card phase-reopen">
          <div class="phase-icon"><i class="fas fa-volume-high"></i></div>
          <h4>The Noise Awakening</h4>
          <p>Jun-Dec 2020: Reopening phase with a dramatic surge beyond pre-pandemic levels</p>
        </div>
      </div>
      
      <a href="#great-quieting" class="cta-button fade-in">Explore Phase 2: The Great Quieting</a>
    </div>
  </section>
  
  <!-- The Great Quieting Slide -->
  <section id="great-quieting" class="slide">
    <div class="slide-content">
      <span class="phase-indicator phase-lockdown fade-in">Phase 2: Mar-May 2020</span>
      <h2 class="slide-title fade-in">The Great Quieting</h2>
      
      <p class="fade-in">
        When New York City went into lockdown in March 2020, the city experienced what many called the "Great Quieting." As businesses closed, traffic diminished, and people stayed home, the city's sonic landscape transformed dramatically.
      </p>
      
      <div class="viz-container fade-in">
        <iframe src="{{ '/assets/visualizations/year_over_year_change.html' | relative_url }}" width="100%" height="500px" frameborder="0"></iframe>
        <div class="viz-caption">
          <i class="fas fa-info-circle"></i> <strong>Interactive:</strong> Click on categories to compare year-over-year changes
        </div>
      </div>
      
      <div class="stats-row fade-in">
        <div class="stat-card">
          <div class="stat-value">-20%</div>
          <div class="stat-label">Overall Noise<br>Complaints</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">-30%</div>
          <div class="stat-label">Construction<br>Noise</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">+15%</div>
          <div class="stat-label">Residential<br>Noise</div>
        </div>
      </div>
      
      <div class="key-finding fade-in">
        <h3>Surprising Finding</h3>
        <p>Despite the overall decrease, residential noise complaints actually increased during this period, as more people spent time at home and became more sensitive to neighbor noise.</p>
      </div>
      
      <a href="#borough-disparities" class="cta-button fade-in">Discover Borough Differences</a>
    </div>
  </section>
  
  <!-- Borough Disparities Slide -->
  <section id="borough-disparities" class="slide">
    <div class="slide-content">
      <span class="phase-indicator phase-lockdown fade-in">Spatial Analysis</span>
      <h2 class="slide-title fade-in">Borough Disparities: Uneven Impacts</h2>
      
      <p class="fade-in">
        The pandemic's effect on noise was not experienced equally across the city. Examining complaints by borough reveals striking disparities that mirror broader social and economic inequalities.
      </p>
      
      <div class="viz-container fade-in">
        <img src="{{ '/assets/visualizations/borough_impact_barchart.png' | relative_url }}" alt="Bar chart comparing the percent change in noise complaints during lockdown by borough" width="100%">
      </div>
      
      <a href="#noise-awakening" class="cta-button fade-in">Discover What Happened Next</a>
    </div>
  </section>
  
  <!-- The Noise Awakening Slide -->
  <section id="noise-awakening" class="slide">
    <div class="slide-content">
      <span class="phase-indicator phase-reopening fade-in">Phase 3: Jun-Dec 2020</span>
      <h2 class="slide-title fade-in">The Noise Awakening: What Changed?</h2>
      
      <p class="fade-in">
        As New York City began reopening in June 2020, noise complaints didn't just return to normal—they surged dramatically beyond pre-pandemic levels, creating what we call "The Noise Awakening."
      </p>
      
      <div class="viz-container fade-in">
        <iframe src="{{ '/assets/visualizations/monthly_noise_trends_by_category.html' | relative_url }}" width="100%" height="500px" frameborder="0"></iframe>
        <div class="viz-caption">
          <i class="fas fa-chart-line"></i> <strong>Category Trends:</strong> See how different noise categories evolved throughout the pandemic period
        </div>
      </div>
      
      <div class="note-box fade-in">
        <i class="fas fa-external-link-alt"></i>
        <span>For a more detailed breakdown of noise categories over time, <a href="{{ '/explore#time' | relative_url }}">explore the Temporal Patterns section</a> of our interactive data explorer.</span>
      </div>
      
      <div class="stats-row highlight fade-in">
        <div class="stat-card">
          <div class="stat-value">+50%</div>
          <div class="stat-label">Overall Noise<br>Increase</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">+100%</div>
          <div class="stat-label">Residential<br>Complaints</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">+4000%</div>
          <div class="stat-label">Fireworks<br>Reports</div>
        </div>
      </div>
      
      <div class="viz-container fade-in">
        <iframe src="{{ '/assets/visualizations/noise_category_mix.html' | relative_url }}" width="100%" height="500px" frameborder="0"></iframe>
        <div class="viz-caption">
          <i class="fas fa-chart-pie"></i> <strong>Category Mix:</strong> See how the composition of noise complaints transformed during reopening
        </div>
      </div>
      
      <div class="key-finding fade-in">
        <h3>Why the Surge?</h3>
        <p>The dramatic increase likely stems from multiple factors: changed noise patterns, increased sensitivity after the quiet period, more people at home to notice and report noise, and psychological effects of prolonged lockdown leading to more noise-generating activities.</p>
      </div>
      
      <a href="#explore" class="cta-button fade-in">Explore the Full Transformation</a>
    </div>
  </section>
  
  <!-- Explore Slide -->
  <section id="explore" class="slide">
    <div class="slide-content">
      <h2 class="slide-title fade-in">Explore the Transformation</h2>
      
      <p class="fade-in">
        The interactive map below allows you to explore how noise complaints changed throughout NYC during the pandemic. You can filter by time period, complaint type, and zoom into specific neighborhoods.
      </p>
      
      <div class="viz-container full-width large fade-in">
        <iframe src="{{ '/assets/visualizations/dynamic_heatmap.html' | relative_url }}" width="100%" height="600px" frameborder="0"></iframe>
        <div class="viz-caption">
          <i class="fas fa-map-marked-alt"></i> <strong>Interactive Heatmap:</strong> Use the controls to filter data and explore different time periods
        </div>
      </div>
      
      <div class="interactive-note fade-in">
        <i class="fas fa-lightbulb"></i>
        <span>Try comparing the lockdown period (Mar-May) with the same months in 2019 to see the dramatic difference</span>
      </div>
      
      <a href="{{ '/explore' | relative_url }}" class="cta-button secondary fade-in">View More Interactive Visualizations</a>
    </div>
  </section>
  
  <!-- Key Findings Slide -->
  <section id="findings" class="slide">
    <div class="slide-content">
      <h2 class="slide-title fade-in">Key Findings & Implications</h2>
      
      <div class="findings-grid fade-in">
        <div class="key-finding">
          <h3>The Noise Inequality Gap</h3>
          <p>The pandemic amplified existing neighborhood disparities in noise exposure. Lower-income areas experienced less relief during lockdown and more severe noise increases during reopening.</p>
        </div>
        
        <div class="key-finding">
          <h3>The Changing Nature of Urban Noise</h3>
          <p>The pandemic shifted noise from commercial to residential sources, raising questions about urban planning and building design in a post-pandemic world.</p>
        </div>
        
        <div class="key-finding">
          <h3>Noise as a Vital Sign</h3>
          <p>Noise complaint patterns served as a "vital sign" of urban health, reflecting social, economic, and psychological conditions during the crisis.</p>
        </div>
      </div>
      
      <div class="viz-container fade-in">
        <iframe src="{{ '/assets/visualizations/borough_category_heatmap.html' | relative_url }}" width="100%" height="500px" frameborder="0"></iframe>
        <div class="viz-caption">
          <i class="fas fa-th"></i> <strong>Heatmap:</strong> Explore relationships between boroughs, complaint types, and pandemic phases
        </div>
      </div>
      
      <p class="conclusion fade-in">
        This analysis provides valuable insights for urban planners, policymakers, and residents as cities continue to adapt to post-pandemic realities. The "Quiet Before the Storm" pattern reveals how quickly urban soundscapes can transform and how these changes connect to broader social dynamics.
      </p>
      
      <div class="note-box data-sources fade-in">
        <i class="fas fa-database"></i>
        <span>This analysis uses data from <a href="https://data.cityofnewyork.us/resource/erm2-nwe9.csv" target="_blank">NYC 311 Service Requests (CSV)</a> and <a href="https://data.cityofnewyork.us/resource/gthc-hcne.geojson" target="_blank">NYC Borough Boundaries (GeoJSON)</a> from NYC Open Data.</span>
      </div>
      
      <div class="action-buttons fade-in">
        <a href="{{ '/notebook' | relative_url }}" class="cta-button">View Technical Notebook</a>
        <a href="{{ '/explore' | relative_url }}" class="cta-button secondary">Explore More Data</a>
        <a href="#landing" class="cta-button outline">Back to Top</a>
      </div>
    </div>
  </section>
</div>

<style>
    /* Story Guide */
    .story-guide {
        position: fixed;
        top: 80px;
        left: 20px;
        z-index: 200;
        max-width: 300px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        transition: transform 0.3s ease, opacity 0.3s ease;
    }
    
    .story-guide.hidden {
        transform: translateX(-320px);
        opacity: 0;
    }
    
    .guide-content {
        padding: 15px;
        position: relative;
    }
    
    .guide-content > i {
        color: var(--primary-blue);
        font-size: 1.5rem;
        margin-bottom: 10px;
    }
    
    .guide-content h3 {
        margin-top: 0;
        font-size: 1rem;
    }
    
    .guide-content p {
        font-size: 0.85rem;
        color: #666;
    }
    
    .guide-instructions {
        margin-top: 15px;
        border-top: 1px solid #eee;
        padding-top: 10px;
    }
    
    .guide-item {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
        font-size: 0.8rem;
    }
    
    .guide-item i {
        margin-right: 8px;
        color: var(--primary-blue);
        width: 16px;
        text-align: center;
    }
    
    .guide-close {
        position: absolute;
        top: 10px;
        right: 10px;
        background: none;
        border: none;
        font-size: 0.8rem;
        cursor: pointer;
        color: #999;
    }
    
    .guide-close:hover {
        color: #333;
    }
    
    /* Phase Cards */
    .story-phases {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin: 20px 0;
    }
    
    .phase-card {
        flex: 1;
        min-width: 180px;
        padding: 15px;
        border-radius: 8px;
        background: #f9f9f9;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .phase-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .phase-card.phase-pre {
        border-top: 3px solid var(--pre-pandemic-color);
    }
    
    .phase-card.phase-lockdown {
        border-top: 3px solid var(--lockdown-color);
    }
    
    .phase-card.phase-reopen {
        border-top: 3px solid var(--reopening-color);
    }
    
    .phase-icon {
        width: 40px;
        height: 40px;
        background: #f5f5f5;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px;
    }
    
    .phase-pre .phase-icon i {
        color: var(--pre-pandemic-color);
    }
    
    .phase-lockdown .phase-icon i {
        color: var(--lockdown-color);
    }
    
    .phase-reopen .phase-icon i {
        color: var(--reopening-color);
    }
    
    .phase-card h4 {
        margin: 0 0 5px 0;
        font-size: 0.9rem;
    }
    
    .phase-card p {
        margin: 0;
        font-size: 0.8rem;
        color: #666;
    }
    
    /* Data point */
    .data-point {
        display: inline-flex;
        align-items: center;
        background: rgba(49, 130, 189, 0.1);
        padding: 5px 10px;
        border-radius: 20px;
        margin-top: 10px;
        font-size: 0.9rem;
    }
    
    .data-value {
        font-weight: bold;
        color: var(--primary-blue);
        margin-right: 5px;
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
    
    /* Stats row */
    .stats-row {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin: 30px 0;
    }
    
    .stats-row.highlight {
        margin-top: -10px;
        padding: 5px;
    }
    
    .stat-card {
        flex: 1;
        min-width: 120px;
        background: #f9f9f9;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        transition: transform 0.3s ease;
        border-bottom: 3px solid var(--primary-blue);
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: var(--primary-blue);
        margin-bottom: 5px;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: #666;
    }
    
    /* Key findings grid */
    .findings-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    /* Conclusion */
    .conclusion {
        font-size: 1.1rem;
        line-height: 1.6;
        border-left: 4px solid var(--primary-blue);
        padding-left: 15px;
        margin: 30px 0;
        color: #555;
    }
    
    /* Action buttons */
    .action-buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-top: 30px;
    }
    
    .cta-button.secondary {
        background-color: var(--secondary-blue);
    }
    
    .cta-button.secondary:hover {
        background-color: var(--primary-blue);
    }
    
    .cta-button.outline {
        background-color: transparent;
        border: 2px solid var(--primary-blue);
        color: var(--primary-blue);
    }
    
    .cta-button.outline:hover {
        background-color: var(--light-blue);
        color: var(--primary-blue);
    }
    
    /* Note box for calls to action */
    .note-box {
        display: flex;
        align-items: center;
        background-color: var(--light-blue);
        border-radius: 6px;
        padding: 15px;
        margin: 20px 0;
        border-left: 4px solid var(--primary-blue);
    }
    
    .note-box i {
        color: var(--primary-blue);
        font-size: 1.2rem;
        margin-right: 15px;
    }
    
    .note-box span {
        font-size: 0.95rem;
        color: #444;
    }
    
    .note-box a {
        color: var(--primary-blue);
        font-weight: 600;
        text-decoration: none;
    }
    
    .note-box a:hover {
        text-decoration: underline;
    }
    
    /* Scroll indicator */
    .scroll-indicator {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 40px;
        color: #666;
        font-size: 0.9rem;
    }
    
    .scroll-indicator i {
        margin-top: 5px;
        animation: bounce 2s infinite;
        color: var(--primary-blue);
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        60% {
            transform: translateY(-5px);
        }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .story-guide {
            top: auto;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            max-width: 90%;
        }
        
        .story-guide.hidden {
            transform: translateY(200px) translateX(-50%);
        }
        
        .story-phases {
            flex-direction: column;
        }
        
        .findings-grid {
            grid-template-columns: 1fr;
        }
        
        .action-buttons {
            flex-direction: column;
        }
        
        .cta-button {
            width: 100%;
            text-align: center;
        }
    }
</style>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Story guide close button
        const storyGuide = document.querySelector('.story-guide');
        const guideClose = document.querySelector('.guide-close');
        
        if (storyGuide && guideClose) {
            guideClose.addEventListener('click', function() {
                storyGuide.classList.add('hidden');
                localStorage.setItem('storyGuideHidden', 'true');
            });
            
            // Check if user has previously closed the guide
            if (localStorage.getItem('storyGuideHidden') === 'true') {
                storyGuide.classList.add('hidden');
            }
            
            // Hide guide after scrolling past first section
            window.addEventListener('scroll', function() {
                const introSection = document.getElementById('story-intro');
                if (introSection) {
                    const introTop = introSection.getBoundingClientRect().top;
                    if (introTop < 0 && !storyGuide.classList.contains('hidden')) {
                        storyGuide.classList.add('hidden');
                    }
                }
            });
        }
    });
</script>
