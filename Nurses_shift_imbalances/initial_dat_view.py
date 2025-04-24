import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Generate random data
np.random.seed(42)
num_points = 100
job_indices = np.random.randint(0, 111, num_points)
nurse_ids = np.random.randint(0, 51, num_points)

# Create DataFrame
df = pd.DataFrame({
    "Job Index": job_indices,
    "Assigned Nurse ID": nurse_ids
})

# Plot with larger grid and bigger markers
plt.figure(figsize=(20, 12))  # 4x larger than default
sns.scatterplot(data=df, x="Job Index", y="Assigned Nurse ID", color="teal", s=240)  # s=60*4

# Set axis ticks every 5 units
plt.xticks(np.arange(0, 111 + 1, 5))
plt.yticks(np.arange(0, 51 + 1, 5))

# Add grid, labels, and title
plt.title("data_10_51_111_66_file_solution", fontsize=20)
plt.xlabel("Job Index", fontsize=14)
plt.ylabel("Assigned Nurse ID", fontsize=14)
plt.grid(True)
plt.tight_layout()

# Save and show
plt.savefig("data_10_51_111_66_file_solution.png")
plt.show()
print(" Enlarged scatter plot saved as 'data_10_51_111_66_file_solution.png'")