# Visualization Placeholder Guide

This document provides instructions for replacing the visualization placeholders with your actual generated visualizations.

## Required Visualizations

The website is designed to accommodate the following visualizations. Generate these files and place them in the appropriate directories to complete the website:

### Main Story Visualizations

1. **bar_chart_race.html** - Animated bar chart race showing noise complaint evolution over time

   - Place in: `assets/visualizations/bar_chart_race.html`
   - Used on: Landing page

2. **daily_noise_timeseries.html** - Time series of daily noise complaints with pandemic phase markers

   - Place in: `assets/visualizations/daily_noise_timeseries.html`
   - Used on: Three-Phase Story section & Explore page

3. **year_over_year_change.html** - Bar chart showing percent change in complaints by category

   - Place in: `assets/visualizations/year_over_year_change.html`
   - Used on: Great Quieting section

4. **borough_impact_barchart.png** - Bar chart of percent change during lockdown by borough

   - Place in: `assets/visualizations/borough_impact_barchart.png`
   - Used on: Borough Disparities section

5. **borough_choropleth_map.html** - Interactive choropleth map of complaint changes

   - Place in: `assets/visualizations/borough_choropleth_map.html`
   - Used on: Borough Disparities section

6. **monthly_category_trends.html** - Line chart of monthly trends by noise category

   - Place in: `assets/visualizations/monthly_category_trends.html`
   - Used on: Noise Awakening section

7. **noise_category_mix.html** - Visualization showing changing mix of complaint types

   - Place in: `assets/visualizations/noise_category_mix.html`
   - Used on: Noise Awakening section

8. **dynamic_heatmap.html** - Interactive heatmap of noise complaints across NYC

   - Place in: `assets/visualizations/dynamic_heatmap.html`
   - Used on: Explore the Transformation section

9. **borough_category_heatmap.html** - Heatmap of borough/category relationships
   - Place in: `assets/visualizations/borough_category_heatmap.html`
   - Used on: Key Findings section

### Explore Page Visualizations

10. **interactive_borough_map.html** - Interactive borough-level map

    - Place in: `assets/visualizations/interactive_borough_map.html`
    - Used on: Explore page (Spatial Analysis tab)

11. **category_breakdown.html** - Visualization of noise complaint type composition

    - Place in: `assets/visualizations/category_breakdown.html`
    - Used on: Explore page (Noise Categories tab)

12. **category_time_series.html** - Line chart of categories over time

    - Place in: `assets/visualizations/category_time_series.html`
    - Used on: Explore page (Noise Categories tab)

13. **multi_dimension_comparison.html** - Interactive tool for custom comparisons
    - Place in: `assets/visualizations/multi_dimension_comparison.html`
    - Used on: Explore page (Comparisons tab)

## How to Replace Placeholders

1. Generate the visualization files using your data analysis tools (Bokeh, Folium, etc.)
2. Save the files with the exact names listed above
3. Place the files in the `assets/visualizations/` directory
4. The website will automatically load your visualizations in place of the placeholders

## Visualization Best Practices

For best results with your visualizations:

- Use the color scheme defined in the CSS (blues, oranges, greens)
- Include clear titles and labels
- Ensure interactive elements have tooltips or instructions
- For Bokeh visualizations, use the minimal theme with transparent background
- Keep file sizes reasonable for web performance
- Test all interactive features before deploying

## Static Fallbacks

If you encounter issues with interactive visualizations, consider providing static image fallbacks:

1. Generate PNG or JPEG versions of your visualizations
2. Save them with the same filenames but different extensions
3. Place them in `assets/visualizations/fallbacks/`
4. Update the website to use these if needed

For any questions or issues with visualization integration, please refer to the documentation for the specific libraries you're using (Bokeh, Folium, etc.).
