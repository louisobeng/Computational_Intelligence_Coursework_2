import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Manually provide your results
data = {
    "Dataset": ["data_10_51_111_66", "data_28_75_208_66", "data_106_121_1096_33"],
    "Spacing": [0.042315, 0.060832, 0.158920]
}

df = pd.DataFrame(data)

# Plot
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="Dataset", y="Spacing", palette="coolwarm")

# Annotate each bar with spacing value
for i, val in enumerate(df["Spacing"]):
    plt.text(i, val + 0.005, f"{val:.3f}", ha="center", fontsize=10)

# Labeling
plt.title("Spacing of Pareto Front Solutions (Lower is Better)", fontsize=14)
plt.xlabel("Dataset")
plt.ylabel("Spacing")
plt.tight_layout()

# Save and show
plt.savefig("corrected_spacing_plot.png")
plt.show()
print(" Spacing chart saved as 'corrected_spacing_plot.png'")