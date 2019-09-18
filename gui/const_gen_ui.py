"""Constrain Generator"""
import coor
vecout=[]
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
def pippo():
    print("CIAO")

def const_gen():

            FILENAME = "./example.xyz"
            XMOL = coor.XYZ(FILENAME)

            vecout.append(("\nNumber of atoms:\t\t" + str(XMOL.natoms)))
            vecout.append(("Elements in molecule:\t\t" + ", ".join(set(XMOL.element))))

            INPUT_INDEX = FormWidget.const_elem_list.split() #input("\nEnter the element(s) to constrain.\nMultiple elements constraints are possible (e.g.: C O).\nDifferent elements must be separated by a SPACE.\nSpecial tokens are allowed (e.g.: All)\n\nSelection\n").split()
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

            SOFT =  1 #input("Select software:\n1)\tORCA\n2)\tGaussian\n3)\txTB\n")

            if SOFT == "1":
                    vecout.append(("%GEOM"))
                    vecout.append(("  Constraints"))
                    for i in CONST_INDEX:
                        vecout.append(("    {C", i-1, "C}"))
                        vecout.append(("  End"))
                    vecout.append(("END"))
                    CONST_INDEX[:] = [x - 1 for x in CONST_INDEX]
                    FREE_INDEX[:] = [x - 1 for x in FREE_INDEX]
                    vecout.append(("\nTo project-out the immaginary frequencies due to frozen atoms in a vibrational analysis use:\n"))
                    vecout.append(("%FREQ"))
                    vecout.append(("  AnFreq    False"))
                    vecout.append(("  NumFreq   True"))
                    vecout.append(("  Partial_Hess"))
                    vecout.append(("    {", " ".join(map(str, CONST_INDEX)), "}"))
                    vecout.append(("  End"))
                    vecout.append(("END"))

            elif SOFT == "2":
                    vecout.append(("\nModredundant syntax is available below but it is suggested to use the classical frozen syntax (Atom 0/-1 X Y Z) at the end of this report:\n"))
                    for i in CONST_INDEX:
                        vecout.append(("X", i, "F"))
                        vecout.append(("\nTo project-out the immaginary frequencies due to frozen atoms in a vibrational analysis change the coordinates using the frozen syntax (Atom 0/-1 X Y Z):\n"))
                    for idx, val in enumerate(XMOL.element):
                        if idx+1 in FREE_INDEX:
                            vecout.append(("{}   {} \t{:.10f}\t {:.10f}\t {:.10f}".format(val, "0", XMOL.xyz[idx][0], XMOL.xyz[idx][1], XMOL.xyz[idx][2])))
                        elif idx+1 in CONST_INDEX:
                            vecout.append(("{}  {} \t{:.10f}\t {:.10f}\t {:.10f}".format(val, "-1", XMOL.xyz[idx][0], XMOL.xyz[idx][1], XMOL.xyz[idx][2])))
                        else:
                            vecout.append(("ERROR!!! Something wrong just happened... :("))

            elif SOFT == "3":
                    XTB_OPT = "y"#input("Do you like to freeze atoms in hessian calculation? (All immaginary mode due to frozen atoms will be projected out) [y/n]\n")
                    vecout.append(("\n$fix"))
                    for i in CONST_INDEX:
                        vecout.append(("atoms:", i))
                    if XTB_OPT == "y":
                        for i in CONST_INDEX:
                            vecout.append(("freeze:", i))
                            vecout.append(("end"))
