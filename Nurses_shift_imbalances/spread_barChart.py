import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load spread summary
df = pd.read_csv("spread_summary.csv")

# Set plot style
sns.set(style="whitegrid")

# Plot bar chart
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="Dataset", y="Spread (Δ)", palette="Blues_d")

# Add value annotations
for i, val in enumerate(df["Spread (Δ)"]):
    plt.text(i, val + max(df["Spread (Δ)"]) * 0.01, f"{val:.2f}", ha='center', color='black')

# Labeling
plt.title("Spread (Δ) of Pareto Fronts Across Datasets")
plt.xlabel("Dataset")
plt.ylabel("Spread (Δ)")
plt.tight_layout()

# Save and show
plt.savefig("pareto_spread_comparison.png")
plt.show()

print(" Spread plot saved as 'pareto_spread_comparison.png'")