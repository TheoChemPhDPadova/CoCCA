import coor
import constants

def molecule_compare(mol_1, mol_2, verbose=False):
    """
    Return True if the two molecules are equal and the .xyz files have the same ordering. 
    If a verbose output is required the flag "verbose=True" can be set
    """
    if isinstance(mol_1, MOL) == False or isinstance(mol_2, MOL) == False:
        print(""""ERROR: The function "molecule_compare" can handle only MOL class type objects""")
        quit()
    if mol_1.natoms != mol_2.natoms:
        if verbose==True: print("The two molecules have different number of atoms")
        return False
    if mol_1.composition() == mol_2.composition():
        if verbose==True: print("The two molecules have the same composition")
        if mol_1.element == mol_2.element:
            if verbose==True: print("The ordering of the two .xyz files is the same")
            return True
        else:
            if verbose==True: print("The ordering of the two .xyz files is different")
            return False


def rigid_linear_transit(mol_start, mol_end, steps, filename):
    """
    Generate the .xyz files corresponding to a rigid linear transit from the start structure
    "mol_start" to the end one "mol_end" with a number of step set by the variable "steps".
    The generated files have the name "root_step.xyz" in which root is set by the varibale "filename"
    """
    if molecule_compare(mol_start, mol_end) == False:
        print("ERROR: The starting and final molecules passed to the rigid linear transit routine are different")
        quit()
    total_displacement = []
    for atom in range(0, mol_start.natoms):
        my_list = []
        for coord in range(0, 3):
            my_list.append(mol_end.xyz[atom][coord] - mol_start.xyz[atom][coord])
        total_displacement.append(my_list)
    for step in range(1, steps+1):
        out_file = open(filename + "_" + str(step) + ".xyz", 'w')
        out_file.write(str(mol_start.natoms) + "\n")
        out_file.write('\n')
        for atom in range(0, mol_start.natoms):
            out_file.write(mol_start.element[atom])
            for coord in range(0, 3):
                new_coord = mol_start.xyz[atom][coord] + total_displacement[atom][coord]*step/(steps + 1)
                out_file.write('\t' + str(new_coord))
            out_file.write('\n')
        out_file.close()


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
    
    def load_hess_file(self, path, verbose=False):
        """
        The function loads into the MOL class object the data conteined into the .hess file
        specified in path. For a verbose output about errors use the flag "verbose=True"
        """
        def load_orca_hesstype_mat(datalist, header_position):
            matrix = []
            dim = [int(i) for i in datalist[header_position + 1].split()]
            spare_lines = dim[0]%5
            complete_blocks = int((dim[0] - spare_lines)/5)
            for row in range(0, dim[0]):
                matrix_row = []
                for block in range(0, complete_blocks):
                    line_index = header_position + 3 + block*(dim[0]+1) + row
                    splitted_line = datalist[line_index].split()
                    for col in range(0, 5):
                        matrix_row.append(float(splitted_line[col+1]))
                if spare_lines != 0:
                    line_index = header_position + 3 + complete_blocks*(dim[0]+1) + row
                    splitted_line = datalist[line_index].split()
                    for col in range(0, spare_lines):
                        matrix_row.append(float(splitted_line[col+1]))
                matrix.append(matrix_row)
            return matrix

        try:
            with open(path) as file:
                lines = file.readlines()
                lines = [line.strip('\n') for line in lines]
            try:
                hessian_index = lines.index("$hessian")
                self.hessian_matrix = load_orca_hesstype_mat(lines, hessian_index)
            except ValueError:
                if verbose == True: print("WARNING: no hessian matrix found")
            try:
                norm_modes_index = lines.index("$normal_modes")
                self.normal_modes_matrix = load_orca_hesstype_mat(lines, norm_modes_index)
            except ValueError:
                if verbose == True: print("WARNING: no normal modes matrix found")
            try:
                frequencies_index = lines.index("$vibrational_frequencies")
                self.vibr_frequencies = []
                dim = int(lines[frequencies_index + 1])
                for index in range(0, dim):
                    row = lines[frequencies_index + 2 + index].split()
                    self.vibr_frequencies.append(float(row[1]))
            except ValueError:
                if verbose == True: print("WARNING: no vibrational frequencies list found")
        except FileNotFoundError as detail:
            print("\n{}".format(detail))
            quit()

