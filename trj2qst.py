"""Generate a QST2/QST3 input from a trajectory file"""

import coor

print("""
================================================
 TRJ 2 Synchronous Transit-Guided Quasi-Newton 
================================================\n
""")

TRAJ = coor.TRJ(input("Enter trajectory file path...\t"))
R_SNAP = int(input("\nSnapshot number before TS...\t"))
TS_SNAP = input("Snapshot number of TS guess...\t")
if TS_SNAP == "":
    print("Switching to a QST2 input generation...")
else:
    print("Switching to a QST3 input generation...")
    TS_SNAP = int(TS_SNAP)
P_SNAP = int(input("Snapshot number after TS...\t"))
CHARGE = int(input("Totale charge of the system...\t"))
MULT = int(input("Multiplicity of the system...\t"))
FROZ = input("List of frozen atoms (if any)...\t").split()
FROZ = [int(i) for i in FROZ]

if TS_SNAP == "":
    print("\n#Opt(QST2)")
else:
    print("\n#Opt(QST3)")

print("\nReactant Guess\n")
print(CHARGE, MULT)
for idx, val in enumerate(TRAJ.trajectory[R_SNAP]):
    if FROZ != []:
        if idx + 1 in FROZ:
            FROZ_STAT = "-1"
        else:
            FROZ_STAT = "0"
    else:
        FROZ_STAT = ""
    print("{} {} \t{:.10f}\t {:.10f}\t {:.10f}".format(
        val[0],
        FROZ_STAT,
        val[1],
        val[2],
        val[3]
    ))

if TS_SNAP == "":
    print("\n\nProduct Guess\n")
else:
    print("\nProduct Guess\n")
print(CHARGE, MULT)

for idx, val in enumerate(TRAJ.trajectory[P_SNAP]):
    if FROZ != []:
        if idx + 1 in FROZ:
            FROZ_STAT = "-1"
        else:
            FROZ_STAT = "0"
    else:
        FROZ_STAT = ""
    print("{} {} \t{:.10f}\t {:.10f}\t {:.10f}".format(
        val[0],
        FROZ_STAT,
        val[1],
        val[2],
        val[3]
    ))

if TS_SNAP != "":
    print("\nTS Guess\n")
    print(CHARGE, MULT)
    for idx, val in enumerate(TRAJ.trajectory[TS_SNAP]):
        if FROZ != []:
            if idx + 1 in FROZ:
                FROZ_STAT = "-1"
            else:
                FROZ_STAT = "0"
        else:
            FROZ_STAT = ""
        print("{} {} \t{:.10f}\t {:.10f}\t {:.10f}".format(
            val[0],
            FROZ_STAT,
            val[1],
            val[2],
            val[3]
        ))
