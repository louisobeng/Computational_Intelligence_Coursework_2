import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Simulated Pareto front evolution data (for illustration purposes)
pareto_evolution = [
    [(20, 15), (18, 18), (25, 10)],
    [(18, 14), (17, 16), (22, 9)],
    [(16, 13), (15, 15), (20, 8)],
    [(14, 12), (13, 14), (18, 7)],
    [(12, 10), (11, 12), (16, 6)],
    [(10, 9), (9, 11), (14, 5)]
]

fig, ax = plt.subplots()
sc = ax.scatter([], [], c='blue', edgecolors='black')
ax.set_xlim(5, 30)
ax.set_ylim(5, 20)
ax.set_xlabel('Unfilled Shifts')
ax.set_ylabel('Workload Std Dev')
ax.set_title('Pareto Front Evolution Over Generations')

def update(frame):
    data = np.array(pareto_evolution[frame])
    sc.set_offsets(data)
    ax.set_title(f'Pareto Front - Generation {frame+1}')
    return sc,

ani = animation.FuncAnimation(fig, update, frames=len(pareto_evolution), interval=1000, repeat=False)

# Save the animation as a GIF
gif_path = "/Users/mct/Desktop/Nurses_shift_imbalances/data/pareto_evolution.gif"
ani.save(gif_path, writer='pillow')
gif_path 