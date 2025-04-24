import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the hypervolume summary
hv_df = pd.read_csv("hypervolume_summary.csv")

# Set plot style
sns.set(style="whitegrid")

# Create figure and axis
fig, ax1 = plt.subplots(figsize=(10, 6))

# Bar plot for Hypervolume
color_hv = "tab:blue"
sns.barplot(data=hv_df, x="Dataset", y="Hypervolume", ax=ax1, color=color_hv, alpha=0.8)
ax1.set_ylabel("Hypervolume", color=color_hv, fontsize=12)
ax1.tick_params(axis='y', labelcolor=color_hv)
ax1.set_xlabel("Dataset", fontsize=12)
ax1.set_title("Hypervolume & Number of Solutions per Dataset", fontsize=14)

# Annotate Hypervolume bars
for i, hv in enumerate(hv_df["Hypervolume"]):
    ax1.text(i, hv + max(hv_df["Hypervolume"]) * 0.01, f"{hv:.1f}", ha="center", color=color_hv)

# Create secondary y-axis for number of solutions
ax2 = ax1.twinx()
color_ns = "tab:green"
sns.lineplot(data=hv_df, x="Dataset", y="Num Solutions", ax=ax2, color=color_ns, marker="o", linewidth=2)
ax2.set_ylabel("Number of Solutions", color=color_ns, fontsize=12)
ax2.tick_params(axis='y', labelcolor=color_ns)

# Annotate Number of Solutions
for i, num in enumerate(hv_df["Num Solutions"]):
    ax2.text(i, num + max(hv_df["Num Solutions"]) * 0.02, f"{num}", ha="center", color=color_ns)

# Layout and save
plt.tight_layout()
plt.savefig("hypervolume_and_solution_count_comparison.png")
plt.show()

print("Plot saved as 'hypervolume_and_solution_count_comparison.png'")