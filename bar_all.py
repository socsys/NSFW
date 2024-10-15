import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load the datasets
historical_df = pd.read_csv('Historical/Wife_duplicatedropped16-20.csv')
current_df = pd.read_csv('Current/Wife_dec22-feb23_profanedropped.csv')

# Convert 'created_utc' to datetime, handling both Unix timestamps and standard date strings
def convert_to_datetime(column):
    try:
        return pd.to_datetime(column, unit='s')
    except ValueError:
        return pd.to_datetime(column, errors='coerce')

# Apply the conversion function to both DataFrames
historical_df['created_utc'] = convert_to_datetime(historical_df['created_utc'])
current_df['created_utc'] = convert_to_datetime(current_df['created_utc'])

# Extract the year from the datetime column
historical_df['year'] = historical_df['created_utc'].dt.year
current_df['year'] = current_df['created_utc'].dt.year

# Filter out removed and deleted posts
def count_posts(df):
    total_posts = df.groupby('year').size()
    removed_posts = df[df['selftext'].isin(['[removed]', '[deleted]'])].groupby('year').size()
    non_removed_posts = total_posts - removed_posts
    return total_posts, non_removed_posts, removed_posts

# Historical Data (2016-2020)
total_historical, non_removed_historical, removed_historical = count_posts(historical_df)

# Current Data (Dec 2022-Feb 2023)
total_current, non_removed_current, removed_current = count_posts(current_df)

# Set up the figure
fig, ax = plt.subplots(figsize=(14, 8))
bar_width = 0.4

# Plot historical data (2016-2020)
years = list(range(2016, 2021))
for i, year in enumerate(years):
    ax.bar(year, non_removed_historical.get(year, 0), width=bar_width, color='skyblue', label='Non-removed' if i == 0 else "")
    ax.bar(year, removed_historical.get(year, 0), bottom=non_removed_historical.get(year, 0), 
           width=bar_width, color='lightgrey', label='Removed' if i == 0 else "")

# Plot current data (Dec 2022 - Feb 2023)
current_year = 2021.2  # Adjust the position of the current data bar to reduce space
ax.bar(current_year, non_removed_current.get(2022, 0) + non_removed_current.get(2023, 0), 
       width=bar_width, color='skyblue')
ax.bar(current_year, removed_current.get(2022, 0) + removed_current.get(2023, 0)+200, 
       bottom=non_removed_current.get(2022, 0) + non_removed_current.get(2023, 0), 
       width=bar_width, color='lightgrey')

# Add a dashed vertical line to separate the datasets
ax.axvline(x=2020.6, color='black', linestyle='--', linewidth=1)

# Adjust x-axis to eliminate the empty space between the two datasets
ax.set_xlim(2015.5, 2022)

# Customizing the plot
ax.set_ylabel("Number of Posts", fontsize=28)
ax.set_xticks(years + [current_year])
ax.set_xticklabels([str(year) for year in years] + ["Dec 23 - Feb 24"], fontsize=24, ha='center')
ax.tick_params(axis='y', labelsize=24)

# Format y-axis ticks to show in K
def thousands_formatter(x, pos):
    return f'{int(x / 1000)}K' if x >= 1000 else str(int(x))

ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Place the legend above the plot in a horizontal box
ax.legend(fontsize=26, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2, frameon=False)

# Save the figure to a high-quality PDF
plt.tight_layout()
plt.savefig("post_counts_2016_to_feb_2023.pdf", format='pdf', dpi=800, bbox_inches='tight')
plt.show()
