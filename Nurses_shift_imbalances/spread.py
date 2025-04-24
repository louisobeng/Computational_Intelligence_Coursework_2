import pandas as pd
import numpy as np

# CSV files with Pareto fronts
csv_files = {
    "data_10_51_111_66": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_10_51_111_66_pareto.csv",
    "data_28_75_208_66": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_28_75_208_66_pareto.csv",
    "data_106_121_1096_33": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_106_121_1096_33_pareto.csv"
}

spread_results = []

for name, path in csv_files.items():
    try:
        df = pd.read_csv(path)
        df.columns = df.columns.str.strip()

        df = df.rename(columns={
            "Unfilled Shifts": "Unfilled",
            "Workload Std Dev": "StdDev"
        })

        # Get max and min values for both objectives
        uf_min, uf_max = df["Unfilled"].min(), df["Unfilled"].max()
        sd_min, sd_max = df["StdDev"].min(), df["StdDev"].max()

        # Calculate spread (Euclidean distance between extremes)
        spread = np.sqrt((uf_max - uf_min)**2 + (sd_max - sd_min)**2)

        spread_results.append({
            "Dataset": name,
            "Unfilled Shifts Range": f"{uf_min} – {uf_max}",
            "Workload Std Dev Range": f"{sd_min:.3f} – {sd_max:.3f}",
            "Spread (Δ)": round(spread, 4)
        })

        print(f"Spread for {name}: {spread:.4f}")

    except Exception as e:
        print(f"Error with {name}: {e}")

# Save results
spread_df = pd.DataFrame(spread_results)
spread_df.to_csv("spread_summary.csv", index=False)
print("Spread results saved to 'spread_summary.csv'")