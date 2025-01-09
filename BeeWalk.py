# Required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, mannwhitneyu

# Load the dataset
file_path = 'BeeWalk_data.csv'
data = pd.read_csv(file_path, encoding='latin1', low_memory=False)

# Preprocess the data
# Convert StartDate to datetime
data['StartDate'] = pd.to_datetime(data['StartDate'], errors='coerce')

# Extract year, month, and assign seasons
data['Year'] = data['StartDate'].dt.year
data['Month'] = data['StartDate'].dt.month

def assign_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    elif month in [9, 10, 11]:
        return "Autumn"

data['Season'] = data['Month'].apply(assign_season)

# Define extreme climate thresholds
EXTREME_HEAT_THRESHOLD = 30  # Temperature > 30°C for summer
EXTREME_COLD_THRESHOLD = 5   # Temperature < 5°C for spring

# Mark extreme events in the dataset
data['ExtremeHeat'] = (data['Season'] == 'Summer') & (data['temperature'] > EXTREME_HEAT_THRESHOLD)
data['ExtremeCold'] = (data['Season'] == 'Spring') & (data['temperature'] < EXTREME_COLD_THRESHOLD)

# Create ExtremeEvent column
def mark_extreme(row):
    if row['ExtremeHeat']:
        return 'Extreme Heat'
    elif row['ExtremeCold']:
        return 'Extreme Cold'
    else:
        return 'No Extreme Event'

data['ExtremeEvent'] = data.apply(mark_extreme, axis=1)

# Filter data for spring and summer
spring_summer_data = data[data['Season'].isin(['Spring', 'Summer'])].copy()

# Total bee counts over the years
total_counts = data.groupby('Year')['TotalCount'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=total_counts, x='Year', y='TotalCount', marker="o")
plt.title("Total Bee Counts Over the Years")
plt.xlabel("Year")
plt.ylabel("Total Bee Counts")
plt.grid(True)
plt.savefig("total_bee_counts_over_years.png")
plt.show()

# Seasonal bee counts with faceted line plots
seasonal_counts = data.groupby(['Year', 'Season'])['TotalCount'].sum().reset_index()

g = sns.FacetGrid(seasonal_counts, col="Season", col_wrap=2, height=4, sharey=False)
g.map(sns.lineplot, "Year", "TotalCount", marker="o")
g.set_titles("{col_name}")
g.set_axis_labels("Year", "Total Bee Counts")
g.fig.suptitle("Seasonal Bee Counts Over the Years", fontsize=16)
plt.subplots_adjust(top=0.9)
g.savefig("seasonal_bee_counts.png")
plt.show()

# Heatmap for extreme climate events by season and year
heatmap_data = data.groupby(['Year', 'Season']).agg({'ExtremeHeat': 'sum', 'ExtremeCold': 'sum'}).reset_index()
heatmap_pivot_heat = heatmap_data.pivot(index='Year', columns='Season', values='ExtremeHeat').fillna(0)
heatmap_pivot_cold = heatmap_data.pivot(index='Year', columns='Season', values='ExtremeCold').fillna(0)

plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_pivot_heat, cmap="Reds", annot=True, fmt=".0f")
plt.title("Heatmap of Extreme Heat Events by Year and Season")
plt.xlabel("Season")
plt.ylabel("Year")
plt.savefig("extreme_heat_events_heatmap.png")
plt.show()

plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_pivot_cold, cmap="Blues", annot=True, fmt=".0f")
plt.title("Heatmap of Extreme Cold Events by Year and Season")
plt.xlabel("Season")
plt.ylabel("Year")
plt.savefig("extreme_cold_events_heatmap.png")
plt.show()

# Trends over time for extreme and non-extreme events
plt.figure(figsize=(12, 6))
sns.lineplot(data=spring_summer_data, x='Year', y='TotalCount', hue='ExtremeEvent', style='Season', markers=True, errorbar=None)
plt.title("Trends in Bee Counts with Extreme Events Highlighted")
plt.xlabel("Year")
plt.ylabel("Bee Counts")
plt.legend(title="Event Type")
plt.grid(True)
plt.savefig("trends_extreme_events.png")
plt.show()

# Compare bee counts for extreme vs non-extreme events in spring and summer
plt.figure(figsize=(12, 6))
sns.boxplot(data=spring_summer_data, x='Season', y='TotalCount', hue='ExtremeEvent')
plt.title("Comparison of Bee Counts for Extreme vs Non-Extreme Events")
plt.xlabel("Season")
plt.ylabel("Bee Counts")
plt.legend(title="Event Type")
plt.grid(True)
plt.savefig("comparison_extreme_non_extreme.png")
plt.show() # Statistical tests for extreme vs non-extreme events in spring and summer
spring_data = spring_summer_data[spring_summer_data['Season'] == 'Spring']
summer_data = spring_summer_data[spring_summer_data['Season'] == 'Summer']

# Function to perform tests with error handling
def perform_stat_tests(group1, group2, test_name):
    if len(group1) < 2 or len(group2) < 2:
        print(f"{test_name}: Not enough data points in one or both groups to perform the test.")
        return None
    ttest = ttest_ind(group1, group2, equal_var=False)
    mannwhitney = mannwhitneyu(group1, group2, alternative='two-sided')
    print(f"{test_name} - T-test: {ttest}")
    print(f"{test_name} - Mann-Whitney U-test: {mannwhitney}")

# Perform tests for spring (Extreme Cold vs No Extreme Event)
spring_extreme_cold = spring_data[spring_data['ExtremeEvent'] == 'Extreme Cold']['TotalCount']
spring_no_extreme = spring_data[spring_data['ExtremeEvent'] == 'No Extreme Event']['TotalCount']
perform_stat_tests(spring_extreme_cold, spring_no_extreme, "Spring (Extreme Cold vs No Extreme Event)")

# Perform tests for summer (Extreme Heat vs No Extreme Event)
summer_extreme_heat = summer_data[summer_data['ExtremeEvent'] == 'Extreme Heat']['TotalCount']
summer_no_extreme = summer_data[summer_data['ExtremeEvent'] == 'No Extreme Event']['TotalCount']
perform_stat_tests(summer_extreme_heat, summer_no_extreme, "Summer (Extreme Heat vs No Extreme Event)")

# Save results to CSV
spring_summer_data.to_csv('Spring_Summer_Extreme_Analysis.csv', index=False) 