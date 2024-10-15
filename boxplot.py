import matplotlib.pyplot as plt
import seaborn as sns




data = [df1['matching_posts_count'], df2['matching_posts_count'], df3['matching_posts_count']]
# Create the figure and axis
plt.figure(figsize=(8, 6))
# Create boxplot with labels
sns.boxplot(data=data)
# Set the labels for the x-axis
plt.xticks([0, 1, 2], ['0.90', '0.95', '0.98'])
# Set title and labels
#plt.title('Boxplots of Matching Posts Count')
plt.xlabel('Matching Threshold')
plt.ylabel('Matching Posts Count')
# Show the plot
plt.grid(False)
plt.savefig("24_count_matchingposts.png", bbox_inches='tight', format="pdf", dpi=800)
plt.show()