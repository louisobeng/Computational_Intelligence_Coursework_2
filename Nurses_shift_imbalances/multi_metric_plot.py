import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Load all metric files
hv_df = pd.read_csv("hypervolume_summary.csv")
spread_df = pd.read_csv("spread_summary.csv")
spacing_df = pd.read_csv("spacing_summary.csv")

# Merge on Dataset
combined_df = hv_df.merge(spread_df[["Dataset", "Spread (Δ)"]], on="Dataset")
combined_df = combined_df.merge(spacing_df[["Dataset", "Spacing"]], on="Dataset")

# Melt for grouped bar chart
melted = pd.melt(combined_df, id_vars="Dataset", value_vars=["Hypervolume", "Spread (Δ)", "Spacing"],
                 var_name="Metric", value_name="Value")

# Plot grouped bar chart
plt.figure(figsize=(10, 6))
sns.barplot(data=melted, x="Dataset", y="Value", hue="Metric", palette="Set2")

# Annotate values
for i, bar in enumerate(plt.gca().patches):
    height = bar.get_height()
    if height > 0:
        plt.gca().text(bar.get_x() + bar.get_width()/2, height + 0.01 * height, f"{height:.2f}", 
                       ha='center', va='bottom', fontsize=8)

# Format
plt.title("Comparison of Optimizer Metrics Across Datasets")
plt.xlabel("Dataset")
plt.ylabel("Metric Value")
plt.legend(title="Metric")
plt.tight_layout()
plt.savefig("optimizer_metrics_comparison.png")
plt.show()

print(" Saved 'optimizer_metrics_comparison.png'")