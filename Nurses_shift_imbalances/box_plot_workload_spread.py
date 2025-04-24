import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Manually insert full paths to your CSV files 
csv_files = {
    "data_10_51_111_66": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_10_51_111_66_pareto.csv",
    "data_28_75_208_66": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_28_75_208_66_pareto.csv",
    "data_106_121_1096_33": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_106_121_1096_33_pareto.csv"
}

# Collect data for plotting
data_frames = []
for label, filepath in csv_files.items():
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        df["Dataset"] = label  # Add label for boxplot grouping
        data_frames.append(df[["Workload Std Dev", "Dataset"]])
    else:
        print(f" File not found: {filepath}")

# Combine and plot
if not data_frames:
    raise FileNotFoundError("None of the specified CSV files were found.")

combined_df = pd.concat(data_frames, ignore_index=True)

# Plot boxplot 
plt.figure(figsize=(10, 6))
sns.boxplot(x="Dataset", y="Workload Std Dev", data=combined_df, palette="Set2")
plt.title("Workload Spread (Standard Deviation) Across Datasets")
plt.xlabel("Dataset")
plt.ylabel("Workload Std Dev")
plt.tight_layout()

# Save & Show 
output_path = os.path.join(os.path.dirname(__file__), "workload_spread_boxplot.png")
plt.savefig(output_path)
plt.show()

# START SUMMARY BLOCK HERE 
summary_report = []

for dataset in combined_df["Dataset"].unique():
    subset = combined_df[combined_df["Dataset"] == dataset]["Workload Std Dev"]
    
    # Calculate summary statistics
    median = subset.median()
    mean = subset.mean()
    q1 = subset.quantile(0.25)
    q3 = subset.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = subset[(subset < lower_bound) | (subset > upper_bound)]

    # Generate summary
    summary = f"""
📊 Dataset: {dataset}
- Mean Workload Std Dev: {mean:.3f}
- Median Workload Std Dev: {median:.3f}
- IQR (Q3 - Q1): {iqr:.3f}
- Outliers Detected: {len(outliers)}
- Range (non-outliers): {subset[(subset >= lower_bound) & (subset <= upper_bound)].min():.3f} – {subset[(subset >= lower_bound) & (subset <= upper_bound)].max():.3f}
"""
    summary_report.append(summary)
    print(summary)

# Save to text file
report_path = os.path.join(os.path.dirname(__file__), "workload_analysis_summary.txt")
with open(report_path, "w") as f:
    f.writelines(summary_report)

print(f"\n Summary written to {report_path}")