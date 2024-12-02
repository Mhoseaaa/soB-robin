# Empty list checker
def is_empty(lst):
    return len(lst) == 0

# Amount of Process
nP = int(input("How many Process do you need?: "))
# Quantum Time
qTi = int(input("What is the Quantum Time?: "))

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
    aT = int(input(f"Project {i+1} Arrival time: "))
    bT = int(input(f"Project {i+1} Burst time: "))
    
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

while len(Plist) > 0 or len(pendingP) > 0:
    if not is_empty(Alist) and TE >= Alist[0] and proc != True:
        print(f"Process {Plist[0]} is being processed at {TE}")
        pendingA.append(Alist.pop(0))
        proc = True
    
    if len(pendingP) > 0 and proc != True:
        proc = True
        Plist.insert(0, pendingP.pop(0))
        Blist.insert(0, pendingB.pop(0))
        
    elif proc:
        Blist[0] -= 1
        qT -= 1
        
        if Blist[0] == 0:
            print(f"Process {Plist.pop(0)} is done at {TE+1}")
            Blist.pop(0)
            qT = qTi
            
            TaT.append((TE+1) - pendingA.pop(0))
            WT.append(TaT[wti] - dbt.pop(0))
            wti += 1
            
            if is_empty(pendingP):
                proc = False
            else:
                Plist.insert(0, pendingP.pop(0))
                Blist.insert(0, pendingB.pop(0))
                       
        elif qT == 0:
            if len(Plist) < 2:
                qT = qTi
            else:
                pendingB.append(Blist.pop(0))
                pendingP.append(Plist.pop(0))
                proc = False
                qT = qTi
            
    TE += 1
# Average Turn-Around Time
aTaT = round(sum(TaT) / len(TaT), 2)
# Average Waiting Time
aWT = round(sum(WT) / len(WT), 2)

print(f'Average Turn-around Time: {aTaT}')
print(f'Average Waiting Time: {aWT}')