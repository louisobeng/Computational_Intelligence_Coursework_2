import os
import matplotlib.pyplot as plt
import random
from collections import defaultdict

def parse_dat_file(filepath):
    with open(filepath, 'r') as file:
        lines = [line.strip() for line in file if line.strip() and not line.startswith("#")]

    num_jobs = int([line for line in lines if "Jobs" in line][0].split('=')[1])
    jobs_start_index = next(i for i, l in enumerate(lines) if "Jobs" in l) + 1
    job_requirements = [int(line.split()[0]) for line in lines[jobs_start_index:jobs_start_index + num_jobs]]

    num_nurses = int([line for line in lines if "Qualifications" in line][0].split('=')[1])
    quals_start_index = next(i for i, l in enumerate(lines) if "Qualifications" in l) + 1
    nurse_qualifications = defaultdict(list)

    for nurse_id, line in enumerate(lines[quals_start_index:quals_start_index + num_nurses]):
        tokens = line.split()
        skills = [int(tok) for tok in tokens if not tok.endswith(':')]
        nurse_qualifications[nurse_id] = skills

    return num_jobs, num_nurses, job_requirements, nurse_qualifications

def generate_random_assignment(num_jobs, num_nurses):
    return [random.randint(0, num_nurses - 1) for _ in range(num_jobs)]

def plot_gantt_chart(individual, num_nurses, base_name):
    nurse_schedules = defaultdict(list)
    current_time = defaultdict(int)

    for job_id, nurse in enumerate(individual):
        start = current_time[nurse]
        nurse_schedules[nurse].append((start, 1, job_id))  # (start time, duration, job_id)
        current_time[nurse] += 1

    colors = plt.cm.tab20.colors
    fig, ax = plt.subplots(figsize=(12, 6))

    for nurse in range(num_nurses):
        if nurse in nurse_schedules:
            for (start, duration, job_id) in nurse_schedules[nurse]:
                ax.barh(y=f'Nurse {nurse}', left=start, width=duration,
                        color=colors[nurse % len(colors)], edgecolor='black')
                ax.text(start + duration / 2, nurse, f'{job_id}', va='center', ha='center',
                        fontsize=8, color='white')

    ax.set_title(f"Gantt Chart of One Initial Individual - {base_name}")
    ax.set_xlabel("Time (arbitrary units)")
    ax.set_ylabel("Nurses")
    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig(f"results/{base_name}_initial_gantt.png")
    plt.close()
    print(f" Gantt chart saved for {base_name}")

# Datasets with names
datasets = [
    ("/Users/mct/Desktop/Nurses_shift_imbalances/data/data_10_51_111_66.dat", "data_10_51_111_66"),
    ("/Users/mct/Desktop/Nurses_shift_imbalances/data/data_28_75_208_66.dat", "data_28_75_208_66"),
    ("/Users/mct/Desktop/Nurses_shift_imbalances/data/data_106_121_1096_33.dat", "data_106_121_1096_33"),
]

for path, name in datasets:
    num_jobs, num_nurses, job_requirements, nurse_qualifications = parse_dat_file(path)
    individual = generate_random_assignment(num_jobs, num_nurses)
    plot_gantt_chart(individual, num_nurses, name)