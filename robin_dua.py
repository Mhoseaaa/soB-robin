# for Table
import pandas as pd
# for Gantt Chart
import matplotlib.pyplot as plt

# Empty list checker
def is_empty(lst):
    return len(lst) == 0

# Integer value getter
def get_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Invalid Input! Enter a positive integer")
        except ValueError:
            print("Invalid Input! Please enter an Integer")

def get_arrival_integer(prompt, alist):
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                if is_empty(alist):
                    return value
                elif value >= alist[-1]:
                    return value
                else:
                    print("Invalid Input! Arrival Time must be bigger or equal to previous")
            else:
                print("Invalid Input! Enter positive integer")
        except ValueError:
            print("Invalid Input! Please enter an Integer")

# Amount of Process
nP = get_integer("How many Process do you need?: ")
# Quantum Time
qTi = get_integer("What is the Quantum Time?: ")

# Process, Burst and Arrival Time list
Plist = []
Blist = []
Alist = []

# Turn-around Time and Waiting Time list
TaT = []
WT = []

# Arrival + Burst Time
for i in range(nP):
    aT = get_arrival_integer(f"Process {i+1} Arrival time: ", Alist)
    bT = get_integer(f"Process {i+1} Burst time: ")
    
    Plist.append(f"P{i+1}")
    Alist.append(aT)
    Blist.append(bT)

# Time Elapsed
TE = 0

# Default Burst Time
dbt = Blist.copy()

# Gantt Chart Data
gantt_data = []

# Table Data
results = []

# Ready queue and pending processes
ready_queue = []

while len(Plist) > 0 or len(ready_queue) > 0:
    # Add processes to ready queue if their arrival time is <= current time
    while len(Plist) > 0 and Alist[0] <= TE:
        ready_queue.append((Plist.pop(0), Blist.pop(0), Alist.pop(0)))

    if not ready_queue:  # If no process is ready, increment time
        TE += 1
        continue

    # Select the first process from the ready queue
    current_process = ready_queue.pop(0)
    process_id, burst_time, arrival_time = current_process

    # Calculate execution time for this process (min of quantum time or remaining burst time)
    execution_time = min(qTi, burst_time)
    gantt_data.append([process_id, TE, TE + execution_time])  # Log Gantt chart
    TE += execution_time  # Increment time by execution time
    burst_time -= execution_time

    # If burst time remains, re-add to ready queue with updated burst time
    if burst_time > 0:
        # Add any newly arrived processes to the ready queue
        while len(Plist) > 0 and Alist[0] <= TE:
            ready_queue.append((Plist.pop(0), Blist.pop(0), Alist.pop(0)))
        ready_queue.append((process_id, burst_time, arrival_time))
    else:
        # Process is complete
        completion_time = TE
        turnaround_time = completion_time - arrival_time
        waiting_time = turnaround_time - dbt[int(process_id[1]) - 1] # Ambil string 1 dari P1 kemudian kurangi 1 untuk index 0
        results.append({
            "Process ID": process_id,
            "Arrival Time": arrival_time,
            "Burst Time": dbt[int(process_id[1]) - 1],
            "Completion Time": completion_time,
            "Turn Around Time": turnaround_time,
            "Waiting Time": waiting_time
        })

# Calculate averages
aTaT = round(sum([res["Turn Around Time"] for res in results]) / len(results), 2)
aWT = round(sum([res["Waiting Time"] for res in results]) / len(results), 2)

# Create DataFrame
df = pd.DataFrame(results)
df = df.sort_values(by='Process ID')
print(df.to_string(index=False, justify='center'))

print(f'Average Turn-around Time: {aTaT}')
print(f'Average Waiting Time: {aWT}')

# Plotting Gantt Chart
fig, ax = plt.subplots(figsize=(10, 6))

# Create bars for each process
for process, start_time, end_time in gantt_data:
    ax.barh(process, end_time - start_time, left=start_time, edgecolor="black", color="skyblue")

    ax.text(start_time, process, f'{start_time}',
            va='center', ha='right', fontsize=9, color='black')
    
    ax.text(end_time, process, f'{end_time}',
            va='center', ha='left', fontsize=9, color='black')

ax.set_xlabel("Time")
ax.set_ylabel("Processes")
ax.set_title("Gantt Chart")
ax.grid(True)
plt.show()