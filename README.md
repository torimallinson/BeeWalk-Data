# README for BeeWalk Dataset Analysis

## Project Overview
This project analyses the BeeWalk dataset to investigate seasonal variations in bee counts and their relationship with extreme climate events, including extreme heat during summer and extreme cold during spring. The analysis incorporates statistical tests, data visualisation, and the generation of outputs for further insights.

## Features of the Analysis
1. **Seasonal Analysis:**
   - Faceted line plots to visualise bee count trends for each season across years.

2. **Extreme Climate Events:**
   - Heatmaps showcasing extreme heat and cold events across years and seasons.
   - Analysis of trends in bee counts during extreme and non-extreme climate events.

3. **Statistical Tests:**
   - T-tests and Mann-Whitney U-tests to compare bee counts in extreme vs non-extreme climate events for spring and summer.

## Prerequisites
- **Python version:** 3.7 or higher
- **Required Python libraries:**
  - pandas
  - matplotlib
  - seaborn
  - scipy

You can install the required libraries using the following command:
```bash
pip install pandas matplotlib seaborn scipy
```

## Dataset
The dataset `BeeWalk_data.csv` contains the following key columns:
- `Year`: Year of observation.
- `Month`: Month of observation.
- `temperature`: Temperature recorded during observations.
- `TotalCount`: Total number of bees observed.

### Derived Columns:
- `Season`: Assigned based on the month (Winter, Spring, Summer, Autumn).
- `ExtremeHeat`: Indicates extreme heat events during summer.
- `ExtremeCold`: Indicates extreme cold events during spring.
- `ExtremeEvent`: Combines `ExtremeHeat` and `ExtremeCold` into a single categorical variable.

## Steps to Run the Code
1. Place the `BeeWalk_data.csv` file in the same directory as the script.
2. Run the script using the following command:
   ```bash
   python BeeWalk.py
   ```

## Outputs
### Visualisation Outputs:
1. `total_bee_counts_over_years.png`: Total bee counts over the years.
2. `seasonal_bee_counts.png`: Seasonal bee counts faceted by season.
3. `extreme_heat_events_heatmap.png`: Heatmap of extreme heat events by year and season.
4. `extreme_cold_events_heatmap.png`: Heatmap of extreme cold events by year and season.
5. `trends_extreme_events.png`: Trends in bee counts for extreme and non-extreme events.
6. `comparison_extreme_non_extreme.png`: Boxplots comparing bee counts for extreme vs non-extreme events by season.

### Statistical Test Outputs:
- **T-test Results:**
  - Extreme Cold vs No Extreme Event (Spring)
  - Extreme Heat vs No Extreme Event (Summer)
- **Mann-Whitney U-test Results:**
  - Extreme Cold vs No Extreme Event (Spring)
  - Extreme Heat vs No Extreme Event (Summer)

### CSV Outputs:
- `Spring_Summer_Extreme_Analysis.csv`: Processed data for spring and summer, including extreme events.

## Key Functions
- `assign_season(month)`: Assigns seasons based on the month.
- `mark_extreme(row)`: Categorises rows based on extreme heat or cold events.
- `perform_stat_tests(group1, group2, test_name)`: Performs T-tests and Mann-Whitney U-tests with error handling.

## Notes
- Ensure the dataset contains sufficient data for statistical tests; otherwise, results may not be meaningful.
- Thresholds for extreme events can be adjusted in the script:
  ```python
  EXTREME_HEAT_THRESHOLD = 30  # Adjust for summer
  EXTREME_COLD_THRESHOLD = 5   # Adjust for spring
  ```

## Contact
For any questions or issues, please contact the author of this analysis.
