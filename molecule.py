import constants
import numpy as np
import matplotlib.pyplot as plt

def write_xmol(elements, coordinates, path):
        """Saving to the "path" a XMol type file from a list of "elements" and their
        "coordinates" arranged as a list of lists ordered ad [[x1, y1, z1],[x2, y2, z2]...]"""
        if len(elements) != len(coordinates):
            print("ERROR: the lists are of different length")
        draft = open(path, "w")
        draft.write("{}\n\n".format(str(len(elements))))
        for idnx, val in enumerate(elements):
            draft.write("{} \t{:.10f}\t {:.10f}\t {:.10f} \n".format(
                val,
                coordinates[idnx][0],
                coordinates[idnx][1],
                coordinates[idnx][2]
                ))

def molecule_compare(mol_1, mol_2, verbose=False):
    """
    Return True if the two molecules are equal and the .xyz files have the same ordering. 
    If a verbose output is required the flag "verbose=True" can be set
    """
    #Check if the arguments are MOL class istances
    if isinstance(mol_1, MOL) == False or isinstance(mol_2, MOL) == False:
        print(""""ERROR: The function "molecule_compare" can handle only MOL class type objects""")
        quit()
    #Check if the number of atoms in the two molecules are the same
    if mol_1.natoms != mol_2.natoms:
        if verbose==True: print("The two molecules have different number of atoms")
        return False
    #Check if the composition of the two molecule is the same
    if mol_1.composition() == mol_2.composition():
        if verbose==True: print("The two molecules have the same composition")
        #Check if the ordering of the atoms in the xyz file is the same
        if mol_1.element == mol_2.element:
            if verbose==True: print("The ordering of the two .xyz files is the same")
            return True
        else:
            if verbose==True: print("The ordering of the two .xyz files is different")
            return False


def rigid_linear_transit(mol_start, mol_end, steps, path):
    """
    Generate the .xyz files corresponding to a rigid linear transit from the start structure
    "mol_start" to the end one "mol_end" with a number of step set by the variable "steps".
    The generated files have the name "root_step.xyz" in which root is set by the varibale "path"
    """
    #Check if the molecules are isomers of the same molecule and if the atom ordering is the same
    if molecule_compare(mol_start, mol_end) == False:
        print("ERROR: The starting and final molecules passed to the rigid linear transit routine are different")
        quit()
    #Compute for each atom the distance between the start and end structure
    total_displacement = []
    for atom in range(0, mol_start.natoms):
        my_list = []
        for coord in range(0, 3):
            my_list.append(mol_end.xyz[atom][coord] - mol_start.xyz[atom][coord])
        total_displacement.append(my_list)
    #Iterate over each step of the linear transit
    for step in range(1, steps+1):
        new_path = str(path) + "_" + str(step) + ".xyz"
        new_coord = []
        for atom in range(0, mol_start.natoms):
            new_coord_line = []
            for coord in range(0, 3):
                new_coord_line.append(mol_start.xyz[atom][coord] + total_displacement[atom][coord]*step/(steps + 1))
            new_coord.append(new_coord_line)
        write_xmol(mol_start.element, new_coord, new_path)        


def plot_ir_spectrum(molecule, *args, style="bar", resolution=0.1, path="", show=True):
    """
    Plot the infrared spectrum of the molecule starting from the .hess file data. The molecule
    is passed via a MOL class object. The style of plot is set with the flag style: type="bar"
    simply return a stem plot of the intensities, style="gaussian" set the plot of the absorption
    profile with gaussian broadening, style="lorentzian" set the plot of the absorption profile
    with lorentzian broadening. If "gaussian" is selected the sigma of the gaussian in cm^-1 must
    be passed as an additiona argument. The same is true in the case of "lorentzian" in which the
    linewidth in cm^-1 must be passed as an additiona argument. The resolution of the plot is set,
    in cm^-1 units, by the flag resolution. By default the resolution in 0.1cm^-1. The flag 
    path="" allow the selection of the directory in which the spectrum must be saved, if nothing 
    is set as path no file will be saved. The flag show allow to activate (True) or deactivate 
    (False) the graphical output.
    """
    #Define the Gaussian and Lorentziam function of unitary height for x=x0
    def unitary_height_gaussian(x, x0, sigma):
        return np.exp(-(x-x0)**2/(2*sigma**2))
    def unitary_height_lorentzian(x, x0, gamma):
        return  (gamma/2)**2 /((x - x0)**2 + (gamma/2)**2)
    #Verify that, if needed, the width parameter is passed as the only additional value
    if len(args) > 1:
        print("""ERROR: Too many arguments passed to the function "plot_ir_spectrum" """)
    elif len(args) == 1:
        width = float(args[0])
    elif len(args) == 0 and style != "bar":
        print("""ERROR: Missing width parameter in function "plot_ir_spectrum" """)
    if isinstance(molecule, MOL) == False:
        print("""ERROR: The function "plot_ir_spectrum" can handle only MOL class type objects""")
        quit()
    #Extract the data of frequency and intensity for each band neglecting the zero frequency modes
    vibr_freq = []
    trans_int = []
    degeneracy = []
    if hasattr(molecule, 'ir_spectrum'):
        f_list = [i[0] for i in molecule.ir_spectrum]
        i_list = [i[1] for i in molecule.ir_spectrum]
        for i, element in enumerate(f_list):
            if element != 0:
                #Check if degenerate modes are present
                if element in vibr_freq:
                    degenerate_index = vibr_freq.index(element)
                    trans_int[degenerate_index] += i_list[i]
                    degeneracy[degenerate_index] += 1
                else:
                    vibr_freq.append(element)
                    trans_int.append(i_list[i])
                    degeneracy.append(1)
    else:
        print("ERROR: The object " + str(molecule) + " has no IR spectrum data loaded")
        quit()
    if show==True:
        print("IR spectrum data [frequency (cm^-1), intensity (km/mol), degeneracy]")
        for i, element in enumerate(vibr_freq):
            print(str(element) + "\t" + str(trans_int[i]) + "\t", str(degeneracy[i]))
    #Initialize a figure object
    fig, ax = plt.subplots(figsize=(18, 7))
    #Check the type of plot selected
    if style == "bar":
        ax.stem(vibr_freq, trans_int)
    elif style == "gaussian" or style == "lorentzian":
        frequency_axis = []
        spectrum = []
        #Generate the plot with the selected resolution keeping 200 cm^-1 at each side
        f = min(vibr_freq) - 200
        while f<= max(vibr_freq) + 200:
            frequency_axis.append(f)
            point = 0
            for index, center in enumerate(vibr_freq):
                if style == "gaussian":
                    point += trans_int[index]*unitary_height_gaussian(f, center, width)
                if style == "lorentzian":
                    point += trans_int[index]*unitary_height_lorentzian(f, center, width)
            spectrum.append(point)
            f += float(resolution)
        ax.plot(frequency_axis, spectrum, color='red')
        (markers, stemlines, baseline) = ax.stem(vibr_freq, trans_int, markerfmt=' ')
        plt.setp(baseline, visible=False)
    else:
        print("ERROR: The style option " + str(style) + " is not valid" )
    ax.set_xlabel(r"Wavenumber [$cm^{-1}$]")
    ax.set_ylabel(r"Intensity [$km/mol$]")
    ax.grid(b=True, which='major', color='#C0C0C0')
    ax.grid(b=True, which='minor', color='#E0E0E0')
    plt.tight_layout()
    #Save the file if needed
    if path != "":
        plt.savefig(path, dpi=600)
    #Show the plot if the option is selected
    if show == True:
        plt.show()


class MOL:
    """The MOL class allow the loading and the manipulation of molecular data"""
    def __init__(self, path):
        try:
            print("\nXYZ Loading...\t\t\t", end="", flush=True)
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
        self.name = path.split("/")[-1].split(".xyz")[-2]
        print("Molecule name:\t\t\t" + str(self.name))
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
        #Create a list of atoms divided by element with the relative number of them in the molecule
        for atom in self.element:
            known_atoms = [i[0] for i in comp] 
            if atom in known_atoms:
                comp[known_atoms.index(atom)][1] += 1
            else:
                comp.append([atom, 1, 0])
        #Complete the last column with the percentual in mass of each element
        for atom in comp:
            atom[2] = 100.*atom[1]*constants.atomic_mass[atom[0]]/self.mass()
        #Order the elements by abbundance in mass
        comp.sort(key=lambda x: x[2], reverse=True)
        #If selected order the elements by number
        if order == "number":
            comp.sort(key=lambda x: x[1], reverse=True) 
        return comp
    
    def load_hess_file(self, path, verbose=False):
        """
        The function loads into the MOL class object the data conteined into the .hess file
        specified in path. For a verbose output about errors use the flag "verbose=True"
        """
        #Define a function to load a matrix from an orca hessian file
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
            #Open the file stripping the newline escape code
            with open(path) as file:
                lines = file.readlines()
                lines = [line.strip('\n') for line in lines]
            #Search and load the hessian
            try:
                hessian_index = lines.index("$hessian")
                self.hessian_matrix = load_orca_hesstype_mat(lines, hessian_index)
            except ValueError:
                if verbose == True: print("WARNING: no hessian matrix found")
            #Search and load the normal mode matrix
            try:
                norm_modes_index = lines.index("$normal_modes")
                self.normal_modes_matrix = load_orca_hesstype_mat(lines, norm_modes_index)
            except ValueError:
                if verbose == True: print("WARNING: no normal modes matrix found")
            #Search and load the frequencies
            try:
                frequencies_index = lines.index("$vibrational_frequencies")
                self.vibr_frequencies = []
                dim = int(lines[frequencies_index + 1])
                for index in range(0, dim):
                    row = lines[frequencies_index + 2 + index].split()
                    self.vibr_frequencies.append(float(row[1]))
            except ValueError:
                if verbose == True: print("WARNING: no vibrational frequencies list found")
            #Search and load the vibrational spectrum
            try:
                ir_spectrum_index = lines.index("$ir_spectrum")
                dim = int(lines[frequencies_index + 1])
                self.ir_spectrum = []
                for index in range(0, dim):
                    row = lines[ir_spectrum_index + 2 + index].split()
                    self.ir_spectrum.append([float(i) for i in row])
            except ValueError:
                if verbose == True: print("WARNING: no infrared spectrum matrix found")
        except FileNotFoundError as detail:
            print("\n{}".format(detail))
            quit()
        
    def get_normal_mode(self, k, style="xyz", coord_type="cartesian", verbose=True):
        '''
        Returns the kth-normal mode of vibration. The output style can be selected by setting the
        flag style. If style is set to "linear" the mode is returned as a plain list of coefficients,
        while if the style is set to "xyz" (default) a list of lists containing the xyz displacement
        ordered by atom is returned. The coord_type of the dispacement can be set to "cartesian" (default)
        or "mass_weighted". The flag verbose allow to select if a verbose output is required
        '''
        if hasattr(self, "normal_modes_matrix"):
            if k < 0 or k >= self.natoms*3:
                if verbose == True: print("ERROR: Index of normal mode out of range")
                quit()
            column = [col[k] for col in self.normal_modes_matrix]   #Extract a column from the normal modes matrix
            if style == "linear":
                if coord_type == "cartesian":
                    return column                                   #If cartesian is selected directly return the column as list
                elif coord_type == "mass_weighted":
                    mass_weighted_mode = []
                    for index, value in enumerate(column):
                        atom = int((index-index%3)/3)                                       #Compute the index of the atom
                        mass_factor = np.sqrt(constants.atomic_mass[self.element[atom]])    #Compute the mass correction factor
                        mass_weighted_mode.append(mass_factor*value)                        #Compute the value of the component in mass weighted coordiantes
                    return mass_weighted_mode                                               #Return the mass weighted vector as a list
                else:
                    if verbose == True: print("ERROR: The coordinate type " + str(coord_type) + " is not a supported one")
                    quit()
            elif style == "xyz":
                list_format = self.get_normal_mode(k, style="linear", coord_type=coord_type, verbose=verbose)    #Call the linear module
                #Reshape the list as a list of lists as [x, y, z]
                xyz_format = []
                for atom in range(0, int(len(column)/3)):
                    line = []
                    for coord in range(0, 3):
                        line.append(list_format[3*atom + coord])
                    xyz_format.append(line)
                return xyz_format
            else:
                if verbose == True: print("ERROR: The style " + str(style) + " is not available")
            quit()
        else:
            if verbose == True: print("ERROR: no normal modes matrix found")
            quit()
