"""Importing library"""

class XYZ:
    """Loading XMol cartesian coordinate"""
    def __init__(self, path):
        try:
            print("XYZ Loading...\t\t\t", end="", flush=True)
            with open(path) as file:
                lines = file.readlines()
            self.natoms = int(lines[0])
            self.element = []
            self.xyz = []
            for line in lines[2:]:
                line = line.split()
                self.element.append(line[0])
                self.xyz.append([float(line[1]), float(line[2]), float(line[3])])
            print("Done!")
            print("Atoms...\t\t\t{}".format(str(self.natoms)))
            print("Elements in molecule:\t\t{}".format(", ".join(set(self.element))))
        except FileNotFoundError as detail:
            print("\n{}".format(detail))
            quit()

    def write_xmol(self, molecule, path):
        """Saving to XMol"""
        draft = open(path, "w")
        draft.write("{}\n\n".format(str(molecule.natoms)))
        for idnx, val in enumerate(molecule.element):
            draft.write("{} \t{:.10f}\t {:.10f}\t {:.10f} \n".format(
                val,
                molecule.xyz[idnx][0],
                molecule.xyz[idnx][1],
                molecule.xyz[idnx][2]
                ))
<<<<<<< HEAD
=======

class PDB:
    """
    Loading PDB standard (Hierarchical Structure below)
    CHAIN { RSN { ATOMS [ ATOM [] ] } }
    ATOM = [ IDN, AT, AAT, CHAIN, RSN, X, Y, Z, ELEMENT ]
    """
    def __init__(self, path):
        try:
            print("PDB Loading...\t\t\t", end="", flush=True)
            with open(path) as file:
                lines = file.readlines()
            self.natoms = 0
            self.prot = {}
            atom = []
            for line in lines:
                if line.startswith("HETATM") or line.startswith("ATOM"):
                    idn = line[6:12].strip()
                    at = line[12:17].strip()
                    aat = line[17:21].strip()
                    chain = line[21:22].strip()
                    rsn = line[22:27].strip()
                    x_cart = line[30:39].strip()
                    y_cart = line[38:47].strip()
                    z_cart = line[46:55].strip()
                    if line[76:79].strip() != "":
                        element = line[76:79].strip()
                    elif line[76:79].strip() == "":
                        element = "H"
                    atom = [
                        idn,
                        at,
                        aat,
                        chain,
                        rsn,
                        float(x_cart),
                        float(y_cart),
                        float(z_cart),
                        element
                    ]
                    if chain not in self.prot:
                        self.prot[chain] = {}
                        self.prot[chain][rsn] = [atom]
                    else:
                        if rsn not in self.prot[chain]:
                            self.prot[chain][rsn] = [atom]
                        else:
                            self.prot[chain][rsn].append(atom)
                    self.natoms += 1
            print("Done!")
            print("Atoms...\t\t\t{}".format(str(self.natoms)))
            print("Chains...\t\t\t{} ({})".format(len(self.prot), "/".join([*self.prot])))
        except FileNotFoundError as detail:
            print("\n{}".format(detail))
            quit()
>>>>>>> master
