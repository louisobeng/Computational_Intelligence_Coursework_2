import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial import ConvexHull
import numpy as np

# CSV file paths
csv_files = {
    "data_10_51_111_66": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_10_51_111_66_pareto.csv",
    "data_28_75_208_66": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_28_75_208_66_pareto.csv",
    "data_106_121_1096_33": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_106_121_1096_33_pareto.csv"
}

# Colors for each dataset
palette = {
    "data_10_51_111_66": "royalblue",
    "data_28_75_208_66": "darkorange",
    "data_106_121_1096_33": "seagreen"
}

plt.figure(figsize=(10, 7))
sns.set(style="whitegrid")

for name, path in csv_files.items():
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df = df.rename(columns={"Unfilled Shifts": "Unfilled", "Workload Std Dev": "StdDev"})

    # Scatter plot
    sns.scatterplot(data=df, x="Unfilled", y="StdDev", label=name, color=palette[name], s=60)

    # Annotate extreme points
    min_unfilled = df.loc[df["Unfilled"].idxmin()]
    min_stddev = df.loc[df["StdDev"].idxmin()]
    plt.text(min_unfilled["Unfilled"], min_unfilled["StdDev"], "Min UF", fontsize=9, color=palette[name])
    plt.text(min_stddev["Unfilled"], min_stddev["StdDev"], "Min SD", fontsize=9, color=palette[name])

    # Convex hull (optional)
    if len(df) >= 3:
        points = df[["Unfilled", "StdDev"]].to_numpy()
        hull = ConvexHull(points)
        for simplex in hull.simplices:
            plt.plot(points[simplex, 0], points[simplex, 1], linestyle="--", color=palette[name], alpha=0.4)

# Labels and formatting
plt.title("Pareto-Optimal Trade-offs: Unfilled Shifts vs Workload Std Dev", fontsize=14)
plt.xlabel("Unfilled Shifts", fontsize=12)
plt.ylabel("Workload Std Dev", fontsize=12)
plt.legend(title="Dataset", fontsize=9)
plt.tight_layout()

# Save and show
output_path = "pareto_tradeoffs_all_datasets.png"
plt.savefig(output_path)
plt.show()
print(f" Pareto front visual saved as '{output_path}'")