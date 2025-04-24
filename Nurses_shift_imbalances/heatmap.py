import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import zip_longest

# File paths
csv_files = {
    "data_10_51_111_66": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_10_51_111_66_pareto.csv",
    "data_28_75_208_66": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_28_75_208_66_pareto.csv",
    "data_106_121_1096_33": "/Users/mct/Desktop/Nurses_shift_imbalances/results/data_106_121_1096_33_pareto.csv"
}

# Load Workload Std Devs from all datasets
std_dev_data = {}

for name, path in csv_files.items():
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df = df.rename(columns={"Workload Std Dev": "StdDev"})
    std_dev_data[name] = df["StdDev"].tolist()

# uniform data  in length by padding with NaN
all_data = list(zip_longest(*std_dev_data.values(), fillvalue=float("nan")))
df_matrix = pd.DataFrame(all_data, columns=std_dev_data.keys())

# Plot heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df_matrix.T, cmap="YlGnBu", annot=False, cbar=True,
            yticklabels=True, xticklabels=False)

plt.title("Workload Std Dev Heatmap Across Solutions & Datasets")
plt.xlabel("Solution Index")
plt.ylabel("Dataset")
plt.tight_layout()
plt.savefig("combined_workload_std_heatmap.png")
plt.show()

print(" Heatmap saved as 'combined_workload_std_heatmap.png'")