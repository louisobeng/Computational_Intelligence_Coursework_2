# Imports and dependencies
import os
import random
import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from deap import tools, algorithms
from data_parser import parse_dat_file
from moga_scheduler import create_moga

# Computes how often each job was left unfilled in the Pareto solutions
def plot_unfilled_heatmap(hof, num_jobs, nurse_qualifications):
    unfilled_counts = [0] * num_jobs
    for ind in hof:
        for job_idx, nurse_id in enumerate(ind):
            if job_idx not in nurse_qualifications.get(nurse_id, []):
                unfilled_counts[job_idx] += 1
    return unfilled_counts

# Computes how many times each nurse was assigned across all Pareto solutions
def plot_workload_heatmap(hof, num_nurses):
    nurse_loads = [0] * num_nurses
    for ind in hof:
        for nurse_id in ind:
            if 0 <= nurse_id < num_nurses:
                nurse_loads[nurse_id] += 1
    return nurse_loads

# Saves both heatmaps into a single figure

def save_combined_heatmap(unfilled_counts, nurse_loads, base_name, output_dir):
    fig, axs = plt.subplots(2, 1, figsize=(18, 6))

    sns.heatmap([unfilled_counts], annot=True, fmt="d", cmap="Reds", ax=axs[0],
                xticklabels=[f"J{j}" for j in range(len(unfilled_counts))],
                yticklabels=["Unfilled Count"])
    axs[0].set_title("Unfilled Shift Frequency (Pareto Set)")

    sns.heatmap([nurse_loads], annot=True, fmt="d", cmap="Blues", ax=axs[1],
                xticklabels=[f"N{n}" for n in range(len(nurse_loads))],
                yticklabels=["Workload Count"])
    axs[1].set_title("Nurse Workload Frequency (Pareto Set)")

    for ax in axs:
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{base_name}_combined_heatmap.png"))
    plt.close()

# Processes one .dat file, runs the optimiser, saves plots and results
def process_file(filepath, output_dir, summary_writer):
    print(f"\n[INFO] Processing file: {os.path.basename(filepath)}")
    try:
        num_jobs, num_nurses, jobs, nurse_qualifications = parse_dat_file(filepath)
        toolbox = create_moga(num_jobs, num_nurses, nurse_qualifications)
    except Exception as e:
        print(f"[ERROR] Failed to parse or setup for {filepath}: {e}")
        return

    # Run MOGA
    pop = toolbox.population(n=100)
    hof = tools.ParetoFront()

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    algorithms.eaMuPlusLambda(
        pop, toolbox, mu=100, lambda_=200,
        cxpb=0.7, mutpb=0.3,
        ngen=50, stats=stats, halloffame=hof, verbose=False
    )

    # Collect results
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    unfilled = [ind.fitness.values[0] for ind in hof]
    workload_std = [ind.fitness.values[1] for ind in hof]

    # Save Pareto front plot
    plt.figure(figsize=(8, 6))
    plt.scatter(unfilled, workload_std, c="blue", edgecolor="black")
    plt.xlabel("Unfilled Shifts")
    plt.ylabel("Workload Std Dev")
    plt.title(f"Pareto Front: {base_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{base_name}_pareto.png"))
    plt.close()

    # Save results as CSV
    with open(os.path.join(output_dir, f"{base_name}_pareto.csv"), mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Solution #", "Unfilled Shifts", "Workload Std Dev"])
        for i, ind in enumerate(hof):
            writer.writerow([i + 1, ind.fitness.values[0], ind.fitness.values[1]])

    # Save best solution summary
    best_idx = np.argmin([ind.fitness.values[0] + ind.fitness.values[1] for ind in hof])
    best = hof[best_idx]
    summary_writer.writerow([
        base_name,
        best.fitness.values[0],
        best.fitness.values[1]
    ])

    # Save heatmaps
    unfilled_counts = plot_unfilled_heatmap(hof, num_jobs, nurse_qualifications)
    nurse_loads = plot_workload_heatmap(hof, num_nurses)
    save_combined_heatmap(unfilled_counts, nurse_loads, base_name, output_dir)

    print(f"[DONE] Saved: {base_name}_pareto.png/.csv and heatmaps ")

# Main driver for batch processing all .dat files
def main():
    random.seed(42)
    np.random.seed(42)

    data_folder = "data"
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)

    dat_files = [f for f in os.listdir(data_folder) if f.endswith(".dat")]

    summary_csv = os.path.join(output_dir, "summary_all_results.csv")
    with open(summary_csv, mode='w', newline='') as summary_file:
        summary_writer = csv.writer(summary_file)
        summary_writer.writerow(["Dataset", "Best Unfilled Shifts", "Best Workload Std Dev"])

        for filename in dat_files:
            filepath = os.path.join(data_folder, filename)
            process_file(filepath, output_dir, summary_writer)

if __name__ == "__main__":
    main()
