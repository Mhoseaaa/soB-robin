class RobinPreemptive:
    pass
    

### RAW CODE

## NON PREEMPTIVE

# Amount of Process
nP = int(input("How many Process do you need?: "))
# Quantum Time
qT = int(input("What is the Quantum Time?: "))

# Process, Burst and Arrival Time list
Plist = []
Blist = []
Alist = []

# Arrival + Burst Time
for i in range(nP):
    aT = input(f"Project {i+1} Arrival time: ")
    bT = input(f"Project {i+1} Burst time: ")
    
    Plist.append(f"P{i+1}")
    Alist.append(aT)
    Blist.append(bT)

# Total Burst Time
TotT = sum(Blist)

# Time Elapsed
TE = 0
proc = False
while TE < TotT:
    if TE >= Alist[0] and proc != True:
        print(f"Process {Plist[0]} is being processed at {TE}")
        Alist.pop(0)
        proc = True
    elif proc:
        Blist[0] -= 1
        qT -= 1
        
        if Blist[0] == 0:
            print(f"Process {Plist.pop(0)} is done at {TE}")
            Blist.pop(0)
            proc = False
    
    TE += 1