import coor
import constants

def molecule_compare(molecule_a, molecule_b, verbose=False):
    """
    Return True if the two molecules are equal and the .xyz files have the same ordering. 
    If a verbose output is required the flag "verbose=True" can be set
    """
    if isinstance(molecule_a, MOL) == False or isinstance(molecule_b, MOL) == False:
        print(""""ERROR: The function "molecule_compare" can handle only MOL class type objects""")
        quit()
    if molecule_a.natoms != molecule_b.natoms:
        if verbose==True: print("The two molecules have different number of atoms")
        return False
    if molecule_a.composition() == molecule_b.composition():
        if verbose==True: print("The two molecules have the same composition")
        if molecule_a.element == molecule_b.element:
            if verbose==True: print("The ordering of the two .xyz files is the same")
            return True
        else:
            if verbose==True: print("The ordering of the two .xyz files is different")
            return False


class MOL(coor.XYZ):
    """The MOL class allow the loading and the manipulation of molecular data"""
    def mass(self):
        """Returns the mass of the molecule in u.m.a."""
        m = 0
        for atom in self.element:
            m += constants.atomic_mass[atom]
        return m
    
    def rcm(self):
        """Returns the position of the center of mass of the molecule"""
        r = []
        for col in range(0, 3):
            var = 0
            for row in range(0, self.natoms):
                var += constants.atomic_mass[self.element[row]]*self.xyz[row][col]
            r.append(var/self.mass())
        return r

    def type_of_atom(self, atom_name):
        """Returns the number of atom of type "atom_name" contained in the molecule"""
        n = 0
        for atom in self.element:
            if atom_name == atom:
                n += 1
        return n
    
    def composition(self, order="mass"):
        """
        Returns the composition of the molecule as a list of lists of type [element, number, %mass].
        The list can be ordered as %mass abbundance (default) or by number of atoms selecting order="number"
        """
        comp = []
        for atom in self.element:
            known_atoms = [i[0] for i in comp] 
            if atom in known_atoms:
                comp[known_atoms.index(atom)][1] += 1
            else:
                comp.append([atom, 1, 0])
        for atom in comp:
            atom[2] = 100.*atom[1]*constants.atomic_mass[atom[0]]/self.mass()

        comp.sort(key=lambda x: x[2], reverse=True)
        if order == "number":
            comp.sort(key=lambda x: x[1], reverse=True)
            
        return comp


