import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Convert minutes to formatted datetime string 
def minutes_to_time(mins):
    base = datetime(2025, 4, 22)  # Reference day
    return base + timedelta(minutes=int(mins))

# Load start-end time pairs from text file 
with open("/Users/mct/Desktop/Nurses_shift_imbalances/start_end_times.txt", "r") as f:
    lines = [line.strip() for line in f if line.strip()]
    start_end_pairs = [list(map(int, line.split())) for line in lines]

# Assign jobs to nurses in round-robin fashion
num_nurses = 5  #  adjust this based on your actual dataset
nurse_names = [f"Nurse {i+1}" for i in range(num_nurses)]

schedule_data = []
for job_id, (start, end) in enumerate(start_end_pairs):
    nurse = nurse_names[job_id % num_nurses]  # Round-robin
    schedule_data.append({
        "Nurse": nurse,
        "Job": f"Job {job_id+1}",
        "Start Time": minutes_to_time(start),
        "End Time": minutes_to_time(end)
    })

# Create DataFrame 
df = pd.DataFrame(schedule_data)

# Create Gantt Chart 
fig = px.timeline(df,
                  x_start="Start Time",
                  x_end="End Time",
                  y="Nurse",
                  color="Job",
                  title="Nurse Schedule Gantt Chart",
                  labels={"Nurse": "Nurse", "Job": "Job Assignment"})

fig.update_yaxes(categoryorder="total ascending")
fig.update_layout(xaxis_title="Time", yaxis_title="Nurses")

# Show and Save
fig.show()
fig.write_image("nurse_schedule_gantt_chart.png")
print("Gantt chart saved as 'nurse_schedule_gantt_chart.png'")