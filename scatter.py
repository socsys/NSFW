import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv('domain_count.csv')

# Sort by 'Count' to display the highest values first, limiting to the top 20 domains for clarity
top_domains = data.sort_values('Count', ascending=False).head(20)

# Create a color palette with a variety of colors
palette = sns.color_palette("husl", len(top_domains) + 4)  # keep it 7

# Create the plot
plt.figure(figsize=(12, 8))

# Plot each domain as a scatter (dot plot) with color indicating frequency
for i, domain in enumerate(top_domains['Domain']):
    plt.scatter(i, top_domains['Count'].iloc[i], color=palette[len(palette) - i - 3], s=200)

# Labeling and title
plt.ylabel("Occurrence in posts", fontsize=25)
plt.xticks(range(len(top_domains)), top_domains['Domain'], fontsize=26, rotation=90)
plt.yticks(fontsize=25)
plt.title("Top 20 Domains by Frequency", fontsize=25, fontweight='bold')

# Show plot with tight layout
plt.tight_layout()

# Save the plot as PDF and JPG
file_title = 'domain_frequency'
plt.savefig(f"{file_title}.pdf", bbox_inches="tight", format='pdf')
plt.savefig(f"{file_title}.jpg", bbox_inches="tight")

plt.show()
