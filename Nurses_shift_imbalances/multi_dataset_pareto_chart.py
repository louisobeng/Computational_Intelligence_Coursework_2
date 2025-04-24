import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# List of Pareto CSVs
pareto_files = [
    "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_3_25_40_66_pareto.csv",
    "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_28_75_208_66_pareto.csv",
    "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_106_121_1096_33_pareto.csv"
]

for file in pareto_files:
    dataset_name = os.path.basename(file).split(".")[0]
    print(f"\n📂 Processing: {dataset_name}")

    # Correct: Read as comma-separated
    df = pd.read_csv(file, sep=",")
    df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
    print("🔎 Columns detected:", df.columns.tolist())

    # Rename columns to clean form
    df = df.rename(columns={
        "Solution #": "Solution",
        "Unfilled Shifts": "Unfilled",
        "Workload Std Dev": "StdDev"
    })

    # Bar Chart 1: Unfilled Shifts
    plt.figure(figsize=(12, 4))
    sns.barplot(x="Solution", y="Unfilled", data=df, palette="Reds")
    plt.title(f"Unfilled Shifts per Solution – {dataset_name}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{dataset_name}_unfilled_shifts_bar.png")
    plt.close()

    # Bar Chart 2: Workload Std Dev 
    plt.figure(figsize=(12, 4))
    sns.barplot(x="Solution", y="StdDev", data=df, palette="Blues")
    plt.title(f"Workload Std Dev per Solution – {dataset_name}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{dataset_name}_workload_stddev_bar.png")
    plt.close()

    # Scatter Plot: Pareto Front
    plt.figure(figsize=(7, 6))
    sns.scatterplot(data=df, x="Unfilled", y="StdDev", hue="Solution", palette="viridis", s=100)
    plt.title(f"Pareto Front – {dataset_name}")
    plt.xlabel("Unfilled Shifts")
    plt.ylabel("Workload Std Dev")
    plt.gca().invert_xaxis()  # Optional for Pareto visual
    plt.tight_layout()
    plt.savefig(f"{dataset_name}_pareto_front.png")
    plt.close()

    # Combined Plot 
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    sns.barplot(x="Solution", y="Unfilled", data=df, ax=axs[0], palette="Reds")
    axs[0].set_title("Unfilled Shifts")
    axs[0].tick_params(axis='x', rotation=45)

    sns.barplot(x="Solution", y="StdDev", data=df, ax=axs[1], palette="Blues")
    axs[1].set_title("Workload Std Dev")
    axs[1].tick_params(axis='x', rotation=45)

    sns.scatterplot(data=df, x="Unfilled", y="StdDev", hue="Solution", palette="viridis", s=80, ax=axs[2])
    axs[2].set_title("Pareto Front")
    axs[2].invert_xaxis()

    plt.suptitle(f"Multi-Objective Overview – {dataset_name}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(f"{dataset_name}_summary_plots.png")
    plt.close()

    print(f" Plots saved for {dataset_name}")