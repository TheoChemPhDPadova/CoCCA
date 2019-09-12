"""Importing library"""

class XYZ:
    """Loading XMol cartesian coordinate"""
    def __init__(self, path):
        try:
            with open(path) as file:
                lines = file.readlines()
            self.natoms = int(lines[0])
            self.element = []
            self.xyz = []
            for line in lines[2:]:
                line = line.split()
                self.element.append(line[0])
                self.xyz.append([float(line[1]), float(line[2]), float(line[3])])
        except FileNotFoundError as detail:
            print("\n{}".format(detail))
            quit()

    def write_xmol(self, molecule, path):
        """Saving to XMol"""
        draft = open(path, "w")
        draft.write("{}\n\n".format(str(molecule.natoms)))
        for idx, val in enumerate(molecule.element):
            draft.write("{} \t{:.10f}\t {:.10f}\t {:.10f} \n".format(
                val,
                molecule.xyz[idx][0],
                molecule.xyz[idx][1],
                molecule.xyz[idx][2]
                ))
        