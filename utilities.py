"""Collectio of useful functions"""
import numpy as np

def dist(atom_a, atom_b):
    """
    Calulate the distance between two atoms
    atom_a = [X, Y, Z]
    """
    atom_a = np.array(atom_a)
    atom_b = np.array(atom_b)
    return np.linalg.norm(atom_a - atom_b)

def ang(atom_a, atom_b, atom_c):
    """
    Calulate the angle given three atoms
    atom_a = [X, Y, Z]
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
