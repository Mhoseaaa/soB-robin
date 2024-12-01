class RobinPreemptive:
    pass
    

### RAW CODE

# Empty list checker
def lst_check(lst):
    return len(lst) == 0

## NON PREEMPTIVE

# Amount of Process
nP = int(input("How many Process do you need?: "))
# Quantum Time
qTi = int(input("What is the Quantum Time?: "))

# Process, Burst and Arrival Time list
Plist = []
Blist = []
Alist = []

pendingP = []
pendingB = []

# Arrival + Burst Time
for i in range(nP):
    aT = int(input(f"Project {i+1} Arrival time: "))
    bT = int(input(f"Project {i+1} Burst time: "))
    
    Plist.append(f"P{i+1}")
    Alist.append(aT)
    Blist.append(bT)

# Total Burst Time
TotT = sum(Blist)

# Time Elapsed
TE = 0
proc = False
qT = qTi
while len(Plist) > 0:
    if not lst_check(Alist) and TE >= Alist[0] and proc != True:
        print(f"Process {Plist[0]} is being processed at {TE}")
        Alist.pop(0)
        proc = True
    
    if len(pendingP) > 0 and proc != True:
        proc = True
        Plist.insert(0, pendingP.pop(0))
        Blist.insert(0, pendingB.pop(0))
        
    elif proc:
        Blist[0] -= 1
        qT -= 1
        
        if Blist[0] == 0:
            print(f"Process {Plist.pop(0)} is done at {TE}")
            Blist.pop(0)
            proc = False
            qT = qTi
            
        elif qT == 0:
            pendingB.append(Blist.pop(0))
            pendingP.append(Plist.pop(0))
            proc = False
            qT = qTi
            
    TE += 1