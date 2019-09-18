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
