import pandas as pd
import matplotlib.pyplot as plt

# Empty list checker
def is_empty(lst):
    return len(lst) == 0

# Integer value getter
def get_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            else:
                print("Invalid Input! Enter a neutral-positive integer")
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

def get_burst_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
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

# Waiting Time Index
wti = 0

# Pending Processes
pendingP = []
pendingB = []
pendingA = []

# Arrival + Burst Time
for i in range(nP):
    aT = get_arrival_integer(f"Project {i+1} Arrival time: ", Alist)
    bT = get_burst_integer(f"Project {i+1} Burst time: ")
    
    Plist.append(f"P{i+1}")
    Alist.append(aT)
    Blist.append(bT)

# Time Elapsed
TE = 0

# Process Checker
proc = False

# Quantum Time setter
qT = qTi

# default Burst Time
dbt = Blist.copy()

# Pending Checker
pchk = 0

# Table Data
results = []

# Gantt Chart Data
gantt_data = []


while len(Plist) > 0 or len(pendingP) > 0:
    if not is_empty(Alist) and TE >= Alist[0] and proc != True and pchk == 0:
        print(f"Process {Plist[0]} is being processed at {TE}")
        gantt_data.append([Plist[0], TE, None])  # Start time
        pendingA.append(Alist.pop(0))
        proc = True
    
    if len(pendingP) > 0 and proc != True:
        gantt_data.append([pendingP[0], TE, None])  # Start time
        proc = True
        if pchk == 0:
            pchk = len(pendingP)
        Plist.insert(0, pendingP.pop(0))
        Blist.insert(0, pendingB.pop(0))
    
    # Start Process
    
    TE += 1
    if proc:
        Blist[0] -= 1
        qT -= 1
        
        if Blist[0] == 0:
            if proc and Blist[0] == 0:
                for entry in gantt_data:
                    if entry[0] == Plist[0] and entry[2] is None:  # Find process entry with no end time
                        entry[2] = TE  # Add end time
            
            Fproc = Plist.pop(0)
            print(f"Process {Fproc} is done at {TE}")
            Blist.pop(0)
            qT = qTi
            
            arrival = pendingA.pop(0)
            burst = dbt.pop(0)
            TaT.append((TE) - arrival)
            WT.append(TaT[wti] - burst)
            
            results.append({
                "Process ID": Fproc,
                "Arrival Time": arrival,
                "Burst Time": burst,
                "Completion Time": TE+1,
                "Turn Around Time": TaT[wti],
                "Waiting Time": WT[wti]
            })
            
            wti += 1
            
            if pchk > 0:
                pchk -= 1
            
            if is_empty(pendingP) != True and pchk > 0:
                gantt_data.append([pendingP[0], TE, None])  # Start time
                Plist.insert(0, pendingP.pop(0))
                Blist.insert(0, pendingB.pop(0))
            else:
                proc = False
                       
        elif qT == 0:
            if pchk > 0:
                pchk -= 1
            
            if len(Plist) < 2:
                qT = qTi
            else:
                if proc:
                    for entry in gantt_data:
                        if entry[0] == Plist[0] and entry[2] is None:  # Find process entry with no end time
                            entry[2] = TE  # Add end time
                pendingB.append(Blist.pop(0))
                pendingP.append(Plist.pop(0))
                proc = False
                qT = qTi
            

# Average Turn-Around Time
aTaT = round(sum(TaT) / len(TaT), 2)
# Average Waiting Time
aWT = round(sum(WT) / len(WT), 2)

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
    
    ax.text(end_time,process, f'{end_time}',
            va='center', ha='left', fontsize=9, color='black')

ax.set_xlabel("Time")
ax.set_ylabel("Processes")
ax.set_title("Gantt Chart")
ax.grid(True)
plt.show()