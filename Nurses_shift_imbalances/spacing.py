import pandas as pd
import numpy as np
import os

# CSV paths
csv_files = {
    "data_10_51_111_66": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_10_51_111_66_pareto.csv",
    "data_28_75_208_66": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_28_75_208_66_pareto.csv",
    "data_106_121_1096_33": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_106_121_1096_33_pareto.csv"
}

def compute_spacing(points):
    distances = []
    for i in range(len(points)):
        current = points[i]
        others = np.delete(points, i, axis=0)
        d_i = np.min(np.linalg.norm(others - current, axis=1))
        distances.append(d_i)
    d_bar = np.mean(distances)
    spacing = np.sum(np.abs(distances - d_bar)) / (len(points) - 1)
    return spacing

spacing_results = []

for name, path in csv_files.items():
    try:
        df = pd.read_csv(path)
        df.columns = df.columns.str.strip()
        df = df.rename(columns={"Unfilled Shifts": "Unfilled", "Workload Std Dev": "StdDev"})
        points = df[["Unfilled", "StdDev"]].to_numpy()

        spacing = compute_spacing(points)

        spacing_results.append({
            "Dataset": name,
            "Num Solutions": len(points),
            "Spacing": round(spacing, 6)
        })

        print(f" Spacing for {name}: {spacing:.6f}")

    except Exception as e:
        print(f" Error processing {name}: {e}")

# Save results
spacing_df = pd.DataFrame(spacing_results)
spacing_df.to_csv("spacing_summary.csv", index=False)
print("📁 Spacing results saved to 'spacing_summary.csv'")