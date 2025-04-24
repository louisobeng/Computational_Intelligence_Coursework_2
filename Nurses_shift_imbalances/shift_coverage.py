import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_shift_coverage(csv_path):
    df = pd.read_csv(csv_path)
    dataset_name = os.path.basename(csv_path).split(".")[0]

    # Convert start and end times to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])

    # Optional: filter out unassigned shifts if Nurse ID is -1 or NaN
    df["Covered"] = df["Nurse ID"].notna() & (df["Nurse ID"] != -1)

    # Count how many shifts start in each hour
    df["Hour"] = df["Start Time"].dt.floor("H")  # Round down to nearest hour
    coverage_count = df.groupby(["Hour", "Covered"]).size().unstack(fill_value=0)

    # Plot the coverage bar chart
    plt.figure(figsize=(12, 6))
    coverage_count.plot(kind="bar", stacked=True, color=["salmon", "mediumseagreen"])

    plt.title(f"Shift Coverage by Hour – {dataset_name}")
    plt.xlabel("Hour")
    plt.ylabel("Number of Shifts")
    plt.xticks(rotation=45)
    plt.legend(["Uncovered", "Covered"], title="Shift Status")
    plt.tight_layout()

    output_path = f"{dataset_name}_shift_coverage_bar_chart.png"
    plt.savefig(output_path)
    plt.show()
    print(f" Saved: {output_path}")

# List of Pareto front CSV files
pareto_files = [
    "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_10_51_111_66_pareto.csv",
    "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_28_75_208_66_pareto.csv",
    "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_106_121_1096_33_pareto.csv"
]

# Run for each dataset
for file in pareto_files:
    plot_shift_coverage(file)