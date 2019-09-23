"""Constrain Generator"""
import molecule

def multiple_parser(inp_list):
    """Multiple input parser"""
    out_list = []
    for k in inp_list:
        if "-" in k:
            for l in range(int(k.split("-")[0]), int(k.split("-")[1]) + 1):
                if int(l) not in out_list:
                    out_list.append(int(l))
        else:
            if int(k) not in out_list:
                out_list.append(int(k))
    return out_list


print("""
================================================
            Constrain Generator   
================================================\n
""")

FILENAME = input("Enter .xyz file path...\t\t")
XMOL = molecule.MOL(FILENAME)
INPUT_INDEX = input("\nEnter the element(s) to constrain.\nMultiple elements constraints are possible (e.g.: C O).\nDifferent elements must be separated by a SPACE.\nSpecial tokens are allowed (e.g.: All)\n\nSelection\n").split()
CONST_INDEX = []

for idx, val in enumerate(XMOL.element):
    if val in INPUT_INDEX:
        CONST_INDEX.append(idx + 1)
if "All" in INPUT_INDEX:
    CONST_INDEX = [i for i in range(1, XMOL.natoms + 1)]

INPUT_INDEX = input("\nDo you want to CONSTRAIN some particular atom?\n\n").split()

for i in multiple_parser(INPUT_INDEX):
    if int(i) not in CONST_INDEX:
        CONST_INDEX.append(int(i))

INPUT_INDEX = input("\nDo you want to UN-CONSTRAIN some particular atom?\n\n").split()

for i in multiple_parser(INPUT_INDEX):
    if int(i) in CONST_INDEX:
        CONST_INDEX.remove(int(i))

FREE_INDEX = list({int(i) for i in range(1, XMOL.natoms + 1)} - set(CONST_INDEX))

SOFT = input("Select software:\n1)\tORCA\n2)\tGaussian\n3)\txTB\n")

if SOFT == "1":
    print("%GEOM")
    print("  Constraints")
    for i in CONST_INDEX:
        print("    {C", i-1, "C}")
    print("  End")
    print("END")
    CONST_INDEX[:] = [x - 1 for x in CONST_INDEX]
    FREE_INDEX[:] = [x - 1 for x in FREE_INDEX]
    print("\nTo project-out the immaginary frequencies due to frozen atoms in a vibrational analysis use:\n")
    print("%FREQ")
    print("  AnFreq    False")
    print("  NumFreq   True")
    print("  Partial_Hess")
    print("    {", " ".join(map(str, CONST_INDEX)), "}")
    print("  End")
    print("END")

elif SOFT == "2":
    print("\nModredundant syntax is available below but it is suggested to use the classical frozen syntax (Atom 0/-1 X Y Z) at the end of this report:\n")
    for i in CONST_INDEX:
        print("X", i, "F")
    print("\nTo project-out the immaginary frequencies due to frozen atoms in a vibrational analysis change the coordinates using the frozen syntax (Atom 0/-1 X Y Z):\n")
    for idx, val in enumerate(XMOL.element):
        if idx+1 in FREE_INDEX:
            print("{}   {} \t{:.10f}\t {:.10f}\t {:.10f}".format(val, "0", XMOL.xyz[idx][0], XMOL.xyz[idx][1], XMOL.xyz[idx][2]))
        elif idx+1 in CONST_INDEX:
            print("{}  {} \t{:.10f}\t {:.10f}\t {:.10f}".format(val, "-1", XMOL.xyz[idx][0], XMOL.xyz[idx][1], XMOL.xyz[idx][2]))
        else:
            print("ERROR!!! Something wrong just happened... :(")

elif SOFT == "3":
    XTB_OPT = input("Do you like to freeze atoms in hessian calculation? (All immaginary mode due to frozen atoms will be projected out) [y/n]\n")
    print("\n$fix")
    for i in CONST_INDEX:
        print("atoms:", i)
    if XTB_OPT == "y":
        for i in CONST_INDEX:
            print("freeze:", i)
    print("end")

print("""

================================================
             NORMAL TERMINATION    
================================================
""")
