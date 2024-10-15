import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter
from matplotlib.colors import LinearSegmentedColormap

# Load the datasets
historical_df = pd.read_csv('Historical/Wife_duplicatedropped16-20.csv')
current_df = pd.read_csv('Current/Wife_dec22-feb23_profanedropped.csv')

# Filter out rows where 'selftext' contains '[removed]'
historical_df = historical_df[historical_df['selftext'] != '[removed]']
current_df = current_df[current_df['selftext'] != '[removed]']

# Function to process social media mentions
def process_social_media_mentions(df, column_name):
    # Convert empty lists to None for easier processing
    df[column_name] = df[column_name].apply(lambda x: eval(x) if isinstance(x, str) else [])
    
    # Generate pairs of co-occurrences, ignoring self-pairs
    cooccurrences = []
    for mentions in df[column_name]:
        mentions = sorted(set(mentions))  # Remove duplicates within each list
        if len(mentions) > 1:
            # Generate pairs, ignoring cases where both sites in the pair are identical
            cooccurrences.extend((site1, site2) for site1, site2 in combinations(mentions, 2) if site1 != site2)
    
    # Create a co-occurrence matrix
    cooccurrence_counts = Counter(cooccurrences)
    unique_sites = list(set([site for pair in cooccurrence_counts.keys() for site in pair]))  # Convert to list
    cooccurrence_matrix = pd.DataFrame(index=unique_sites, columns=unique_sites).fillna(0)
    
    for (site1, site2), count in cooccurrence_counts.items():
        cooccurrence_matrix.loc[site1, site2] = count
        cooccurrence_matrix.loc[site2, site1] = count

    # Normalize the matrix values from 0 to 100
    max_value = cooccurrence_matrix.to_numpy().max()
    if max_value > 0:  # Prevent division by zero
        cooccurrence_matrix = (cooccurrence_matrix / max_value) * 100
    
    return cooccurrence_matrix

# Process both dataframes
historical_cooccurrence = process_social_media_mentions(historical_df, 'social_media_mentions')
current_cooccurrence = process_social_media_mentions(current_df, 'social_media_mentions')

# Create a custom color map from light blue to dark red
colors = ["#b3cde3", "#fbb4b9", "#f768a1", "#7a0177"]  # Gradient from light blue to dark red
custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)

# Function to plot a heatmap with customized appearance and save it
def plot_heatmap(cooccurrence_matrix, filename):
    plt.figure(figsize=(20, 18))  # Increase height to fit larger labels
    
    # Apply custom styling for the heatmap
    heatmap = sns.heatmap(
        cooccurrence_matrix, 
        cmap=custom_cmap,  # Use the custom color map
        linewidths=0.5, 
        linecolor='gray', 
        cbar_kws={'shrink': 0.8}, 
        square=True,
        annot=False  # Remove the numbers inside the heatmap boxes
    )
    
    # Customize the color bar font size
    colorbar = heatmap.collections[0].colorbar
    colorbar.ax.tick_params(labelsize=22)  # Set font size for color bar
    
    # Customizing the axis labels
    plt.xticks(rotation=45, ha='right', fontsize=32, fontweight='bold')
    plt.yticks(rotation=0, fontsize=32, fontweight='bold')  # Horizontal y-axis labels
    
    # Capitalize only the first letter of each y-axis label
    ylabels = [label.get_text().capitalize() for label in plt.gca().get_yticklabels()]
    plt.gca().set_yticklabels(ylabels)
    
    # Capitalize only the first letter of each x-axis label
    xlabels = [label.get_text().capitalize() for label in plt.gca().get_xticklabels()]
    plt.gca().set_xticklabels(xlabels)
    
    # Save the figure to a high-quality PDF
    plt.savefig(f"{filename}.pdf", format='pdf', dpi=800, bbox_inches='tight')
    plt.show()

# Plot and save heatmaps
plot_heatmap(historical_cooccurrence, "historical_cooccurrence_heatmap")
plot_heatmap(current_cooccurrence, "current_cooccurrence_heatmap")
