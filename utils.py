"""Collection of useful functions"""

from os import system, name
import numpy as np
import sys


def clear():
    """System independent clear screen
    """
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def header(VER):
    """Logo
    """
    clear()
    print("""
================================================
         __
   ///  /  )   _____       _____  _____   ___  
  |@  \/   )  /  __ \     /  __ \/  __ \ / _ \     
 < (  (____)  | /  \/ ___ | /  \/| /  \// /_\ \\
   \      )   | |    / _ \| |    | |    |  _  |
    \____/    | \__/\ (_) | \__/\| \__/\| | | |
    __||__     \____/\___/ \____/ \____/\_| |_/

======================================== Mk. {}""".format(VER))


def NT():
    print("\n=== NORMAL TERMINATION")
    sys.exit()


def TITLE(tle):
    print("\n=== {}\n".format(tle))


def dist(atom_a, atom_b):
    """Calulate the distance between two atoms

    Args:
        atom_a (list): Cartesian coordinate of atom a [X, Y, Z]
        atom_b (list): Cartesian coordinate of atom b [X, Y, Z]
    Returns:
        [type]: Distance between atom_a and atom_b
    """
    atom_a = np.array(atom_a)
    atom_b = np.array(atom_b)
    return np.linalg.norm(atom_a - atom_b)


def ang(atom_a, atom_b, atom_c):
    """Calulate the angle given three atoms

    Args:
        atom_a (list): Cartesian coordinate of atom a [X, Y, Z]
        atom_b (list): Cartesian coordinate of atom b [X, Y, Z]
        atom_c (list): Cartesian coordinate of atom c [X, Y, Z]

    Returns:
        float: Angle in radiants among atom_a, atom_b, atom_c
    """
    atom_a = np.array(atom_a)
    atom_b = np.array(atom_b)
    atom_c = np.array(atom_c)
    b_a = atom_a - atom_b
    b_c = atom_c - atom_b
    rad_angle = np.arccos(
        np.dot(b_a, b_c) / (dist(atom_a, atom_b) * dist(atom_b, atom_c))
    )
    return rad_angle


def rot_mat(ang, vec):
    """Rotation Matrix

    Args:
        ang (float): Rotational angle in rad
        vec (list): Vector used as reference for the rotation

    Returns:
        list: Rotation Matrix
    """
    vecx = vec[0]
    vecy = vec[1]
    vecz = vec[2]

    return [
        [np.cos(ang)+(vecx**2)*(1-np.cos(ang)),
         vecx*vecy*(1-np.cos(ang))-vecz*np.sin(ang),
         vecx*vecz*(1-np.cos(ang))+vecy*np.sin(ang)],
        [vecy*vecx*(1-np.cos(ang))+vecz*np.sin(ang),
         np.cos(ang)+(vecy**2)*(1-np.cos(ang)),
         vecy*vecz*(1-np.cos(ang))-vecx*np.sin(ang)],
        [vecz*vecx*(1-np.cos(ang))-vecy*np.sin(ang),
         vecz*vecy*(1-np.cos(ang))+vecx*np.sin(ang),
         np.cos(ang)+(vecz**2)*(1-np.cos(ang))]
    ]


def rot_mat_v(ref, tgt):
    """Rotation Matrix from two arbitary vectors: R * ref = tgt

    Args:
        ref (list): Starting vector
        tgt (list): Vector used as target

    Returns:
        list: Rotation Matrix
    """
    ref = np.array(ref) / np.linalg.norm(ref)
    tgt = np.array(tgt) / np.linalg.norm(tgt)
    dt = np.dot(ref, tgt)
    cr = np.cross(ref, tgt)
    v_mat = np.array(
        [
            [0.0, -cr[2], cr[1]],
            [cr[2], 0.0, -cr[0]],
            [-cr[1], cr[0], 0.0]
        ]
    )
    return np.identity(3) + v_mat + (np.matmul(v_mat, v_mat)*(1/(1 + dt)))


def ref_mat(vec):
    """Reflection Matrix

    Args:
        vec (list): Normal vector of the reflection plane

    Returns:
        list: Reflection Matrix
    """
    normx = vec[0]
    normy = vec[1]
    normz = vec[2]
    return [
        [-normx**2+normz**2+normy**2, -2*normx*normy, -2*normx*normz],
        [-2*normy*normx, -normy**2+normx**2+normz**2, -2*normy*normz],
        [-2*normz*normx, -2*normz*normy, -normz**2+normy**2+normx**2]
    ]


class TRJ:
    """Loading XMol trajectory"""
    def __init__(self, path):
        try:
            print("TRJ Loading...\t\t\t", end="", flush=True)
            with open(path) as file:
                lines = file.readlines()
            print("Done!")
            self.natoms = int(lines[0])
            print("Atoms...\t\t\t{}".format(str(self.natoms)))
            self.trajectory = []
            xyz = []
            snapsidx = [idx for idx, i in enumerate(lines) if i == lines[0]]
            self.nspas = len(snapsidx)
            print("Snapshots...\t\t\t{}".format(str(self.nspas)))

            for i in snapsidx:
                xyz = []
                line = lines[i + 2:i + 2 + self.natoms]
                for j in line:
                    xyz.append([str(j.split()[0]), float(j.split()[1]), float(j.split()[2]), float(j.split()[3])])
                self.trajectory.append(xyz)

        except FileNotFoundError as detail:
            print("\n{}".format(detail))
            sys.exit()


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
            sys.exit()


atomic_mass = {
        'H': 1.00794, 'He': 4.00260, 'Li': 6.94100, 'Be': 9.01218, 'B': 10.81100, 'C': 12.01070, 'N': 14.00670, 'O': 15.99940,
        'F': 18.99840, 'Ne': 20.17970, 'Na': 22.98977, 'Mg': 24.30500, 'Al': 26.98154, 'Si': 28.08550, 'P': 30.97376,
        'S': 32.06500, 'Cl': 35.45300, 'Ar': 39.94800, 'K': 39.09830, 'Ca': 40.07800, 'Sc': 44.95591, 'Ti': 47.86700, 'V': 50.94150,
        'Cr': 51.99610, 'Mn': 54.93805, 'Fe': 55.84500, 'Co': 58.93320, 'Ni': 58.69340, 'Cu': 63.54600, 'Zn': 65.40900, 'Ga': 69.72300,
        'Ge': 72.64000, 'As': 74.92160, 'Se': 78.96000, 'Br': 79.90400, 'Kr': 83.79800, 'Rb': 85.46780, 'Sr': 87.62000, 'Y': 88.90585,
        'Zr': 91.22400, 'Nb': 92.90638, 'Mo': 95.94000, 'Tc': 98.00000, 'Ru': 101.07000, 'Rh': 102.90550, 'Pd': 106.42000,
        'Ag': 107.86820, 'Cd': 112.41100, 'In': 114.81800, 'Sn': 118.71000, 'Sb': 121.76000, 'Te': 127.60000, 'I': 126.90447,
        'Xe': 131.29300, 'Cs': 132.90545, 'Ba': 137.32700, 'La': 138.90550, 'Ce': 140.11600, 'Pr': 140.90765, 'Nd': 144.24000,
        'Pm': 145.00000, 'Sm': 150.36000, 'Eu': 151.96400, 'Gd': 157.25000, 'Tb': 158.92534, 'Dy': 162.50000, 'Ho': 164.93032,
        'Er': 167.25900, 'Tm': 168.93421, 'Yb': 173.04000, 'Lu': 174.96700, 'Hf': 178.49000, 'Ta': 180.94790, 'W': 183.84000,
        'Re': 186.20700, 'Os': 190.23000, 'Ir': 192.21700, 'Pt': 195.07800, 'Au': 196.96655, 'Hg': 200.59000, 'Tl': 204.38330,
        'Pb': 207.20000, 'Bi': 208.98038, 'Po': 209.00000, 'At': 210.00000, 'Rn': 222.00000, 'Fr': 223.00000, 'Ra': 226.00000,
        'Ac': 227.00000, 'Th': 232.03810, 'Pa': 231.03588, 'U': 238.02891, 'Np': 237.00000, 'Pu': 244.00000, 'Am': 243.00000,
        'Cm': 247.00000, 'Bk': 247.00000, 'Cf': 251.00000, 'Es': 252.00000, 'Fm': 257.00000, 'Md': 258.00000, 'No': 259.00000,
        'Lr': 262.00000, 'Rf': 261.00000, 'Db': 262.00000, 'Sg': 266.00000, 'Bh': 264.00000, 'Hs': 277.00000, 'Mt': 268.00000,
        'Ds': 281.00000, 'Rg': 280.00000, 'Cn': 285.00000, 'D': 2.01363, 'T': 3.01605
}

atomic_number = {
        1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O", 9: "F", 10: "Ne", 11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P",
        16: "S", 17: "Cl", 18: "Ar", 19: "K", 20: "Ca", 21: "Sc", 22: "Ti", 23: "V", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co", 28: "Ni", 29: "Cu",
        30: "Zn", 31: "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br", 36: "Kr", 37: "Rb", 38: "Sr", 39: "Y", 40: "Zr", 41: "Nb", 42: "Mo", 43: "Tc",
        44: "Ru", 45: "Rh", 46: "Pd", 47: "Ag", 48: "Cd", 49: "In", 50: "Sn", 51: "Sb", 52: "Te", 53: "I", 54: "Xe", 55: "Cs", 56: "Ba", 57: "La",
        58: "Ce", 59: "Pr", 60: "Nd", 61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd", 65: "Tb", 66: "Dy", 67: "Ho", 68: "Er", 69: "Tm", 70: "Yb", 71: "Lu",
        72: "Hf", 73: "Ta", 74: "W", 75: "Re", 76: "Os", 77: "Ir", 78: "Pt", 79: "Au", 80: "Hg", 81: "Tl", 82: "Pb", 83: "Bi", 84: "Po", 85: "At",
        86: "Rn", 87: "Fe", 88: "Ra", 89: "Ac", 90: "Th", 91: "Pa", 92: "U", 93: "Np", 94: "Pu", 95: "Am", 96: "Cm", 97: "Bk", 98: "Cf", 99: "Es",
        100: "Fm", 101: "Md", 102: "No", 103: "Lr", 104: "Rf", 105: "Db", 106: "Sg", 107: "Bh", 108: "Hs", 109: "Mt", 110: "Ds", 111: "Rg",
        112: "Cn", 113: "Nh", 114: "Fl", 115: "Mc", 116: "Lv", 117: "Ts", 118: "Og"
}

ha2kcal = 627.5096080306
