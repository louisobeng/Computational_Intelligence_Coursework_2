import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Dataset info: total shifts and CSV paths
datasets = {
    "data_10_51_111_66": {"total_shifts": 111, "csv": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_10_51_111_66_pareto.csv"},
    "data_28_75_208_66": {"total_shifts": 208, "csv": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_28_75_208_66_pareto.csv"},
    "data_106_121_1096_33": {"total_shifts": 1096, "csv": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_106_121_1096_33_pareto.csv"},
}

# Collect data
chart_data = []

for name, info in datasets.items():
    df = pd.read_csv(info["csv"])
    df.columns = df.columns.str.strip()
    df = df.rename(columns={"Unfilled Shifts": "Unfilled"})
    
    min_unfilled = df["Unfilled"].min()
    covered = info["total_shifts"] - min_unfilled

    chart_data.append({
        "Dataset": name,
        "Covered Shifts": covered,
        "Unfilled Shifts": min_unfilled
    })

# Create DataFrame for plotting
plot_df = pd.DataFrame(chart_data)
plot_df = plot_df.set_index("Dataset")

# Plot stacked bar chart
plot_df[["Covered Shifts", "Unfilled Shifts"]].plot(kind="bar", stacked=True, figsize=(9, 6), colormap="Set2")

plt.title("Shift Coverage vs. Unfilled Shifts")
plt.xlabel("Dataset")
plt.ylabel("Number of Shifts")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("shift_coverage_vs_unfilled.png")
plt.show()

print(" Saved 'shift_coverage_vs_unfilled.png'")