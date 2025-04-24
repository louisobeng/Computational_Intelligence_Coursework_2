# moga_scheduler.py
import random
import numpy as np
from deap import base, creator, tools

# Prevent redefinition warnings during repeated imports
if not hasattr(creator, "FitnessMulti"):
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0))  # Minimise both
if not hasattr(creator, "Individual"):
    creator.create("Individual", list, fitness=creator.FitnessMulti)

def create_moga(num_jobs, num_nurses, nurse_qualifications):
    toolbox = base.Toolbox()

    #Solution Encoding: each position is a nurse assigned to that job
    def random_assignment():
        return [random.randint(0, num_nurses - 1) for _ in range(num_jobs)]

    toolbox.register("individual", tools.initIterate, creator.Individual, random_assignment)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Evaluation Function
    def evaluate(individual):
        unfilled = 0
        workload = [0] * num_nurses

        for job_idx, nurse_id in enumerate(individual):
            if job_idx not in nurse_qualifications.get(nurse_id, []):
                unfilled += 1
            else:
                workload[nurse_id] += 1

        workload_std = np.std(workload)
        return unfilled, workload_std

    # Register GA Operators
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, low=0, up=num_nurses-1, indpb=0.1)
    toolbox.register("select", tools.selNSGA2)

    return toolbox