"""Neighbor finder module"""
import utilities as ut

print("""
================================================
                Neighbor Finder
================================================
""")
FILENAME = input("Enter .pdb file path...\t\t")
PRT = ut.PDB(FILENAME).prot
SEL_CHAIN = input("Select chain...\t\t\t")
SEL_RSN = input("Select residue...\t\t")
print("\nDetected Atom Type in", SEL_RSN, PRT[SEL_CHAIN][SEL_RSN][0][2], ":\n")
for i in PRT[SEL_CHAIN][SEL_RSN]:
    print(">> ", i[1])

SEL_AT = input("\nSelect Atom Type:\t")

TGT = [i for i in PRT[SEL_CHAIN][SEL_RSN] if i[1] == SEL_AT][0]

DIST_TGT = {}

for i in PRT[SEL_CHAIN]:
    for j in PRT[SEL_CHAIN][i]:
        distance = ut.dist([TGT[5], TGT[6], TGT[7]], [j[5], j[6], j[7]])
        if j[4] not in DIST_TGT:
            DIST_TGT[j[4]] = distance
        elif j[4] in DIST_TGT:
            if distance < float(DIST_TGT[j[4]]):
                DIST_TGT[j[4]] = distance
        else:
            print("ERROR!")

POS_AA = ["ARG", "HIS", "LYS"]
NEG_AA = ["ASP", "GLU"]

try:
    while True:
        THR_DIST = float(input("Select cutoff distance...\t"))
        print("\n\nResID\tDIST\tAA\tCHARGE\n")
        for i in DIST_TGT:
            if DIST_TGT[i] <= THR_DIST and PRT[SEL_CHAIN][i][0][2] in POS_AA:
                print("{}\t{:.3f}\t{}\t+1".format(i, DIST_TGT[i], PRT[SEL_CHAIN][i][0][2]))
            elif DIST_TGT[i] <= THR_DIST and PRT[SEL_CHAIN][i][0][2] in NEG_AA:
                print("{}\t{:.3f}\t{}\t-1".format(i, DIST_TGT[i], PRT[SEL_CHAIN][i][0][2]))
            elif DIST_TGT[i] <= THR_DIST:
                print("{}\t{:.3f}\t{}".format(i, DIST_TGT[i], PRT[SEL_CHAIN][i][0][2]))
except KeyboardInterrupt:
    print("""

================================================
            CLOSED BY USER - BYE BYE    
================================================
""")
