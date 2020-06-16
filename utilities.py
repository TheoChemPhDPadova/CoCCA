"""Collectio of useful functions"""
import numpy as np

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
        [np.cos(ang)+(vecx**2)*(1-np.cos(ang)), vecx*vecy*(1-np.cos(ang))-vecz*np.sin(ang), vecx*vecz*(1-np.cos(ang))+vecy*np.sin(ang)],
        [vecy*vecx*(1-np.cos(ang))+vecz*np.sin(ang), np.cos(ang)+(vecy**2)*(1-np.cos(ang)), vecy*vecz*(1-np.cos(ang))-vecx*np.sin(ang)],
        [vecz*vecx*(1-np.cos(ang))-vecy*np.sin(ang), vecz*vecy*(1-np.cos(ang))+vecx*np.sin(ang), np.cos(ang)+(vecz**2)*(1-np.cos(ang))]
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
                line = lines[i+2:i+2+self.natoms]
                for j in line:
                    xyz.append([str(j.split()[0]), float(j.split()[1]), float(j.split()[2]), float(j.split()[3])])
                self.trajectory.append(xyz)

        except FileNotFoundError as detail:
            print("\n{}".format(detail))
            quit()

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