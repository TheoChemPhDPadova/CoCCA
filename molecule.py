import coor

atomic_mass = {'H':1.00794,'He':4.00260,'Li':6.94100,'Be':9.01218,'B':10.81100,'C':12.01070,'N':14.00670,'O':15.99940,
        'F':18.99840, 'Ne':20.17970,'Na':22.98977,'Mg':24.30500,'Al':26.98154,'Si':28.08550,'P':30.97376,
        'S':32.06500,'Cl':35.45300,'Ar':39.94800,'K':39.09830,'Ca':40.07800,'Sc':44.95591,'Ti':47.86700,'V':50.94150,
        'Cr':51.99610,'Mn':54.93805,'Fe':55.84500,'Co':58.93320,'Ni':58.69340,'Cu':63.54600,'Zn':65.40900,'Ga':69.72300,
        'Ge':72.64000,'As':74.92160,'Se':78.96000,'Br':79.90400,'Kr':83.79800,'Rb':85.46780,'Sr':87.62000,'Y':88.90585,
        'Zr':91.22400,'Nb':92.90638,'Mo':95.94000,'Tc':98.00000,'Ru':101.07000,'Rh':102.90550,'Pd':106.42000,
        'Ag':107.86820,'Cd':112.41100,'In':114.81800,'Sn':118.71000,'Sb':121.76000,'Te':127.60000,'I':126.90447,
        'Xe':131.29300,'Cs':132.90545,'Ba':137.32700,'La':138.90550,'Ce':140.11600,'Pr':140.90765,'Nd':144.24000,
        'Pm':145.00000,'Sm':150.36000,'Eu':151.96400,'Gd':157.25000,'Tb':158.92534,'Dy':162.50000,'Ho':164.93032,
        'Er':167.25900,'Tm':168.93421,'Yb':173.04000,'Lu':174.96700,'Hf':178.49000,'Ta':180.94790,'W':183.84000,
        'Re':186.20700,'Os':190.23000,'Ir':192.21700,'Pt':195.07800,'Au':196.96655,'Hg':200.59000,'Tl':204.38330,
        'Pb':207.20000,'Bi':208.98038,'Po':209.00000,'At':210.00000,'Rn':222.00000,'Fr':223.00000,'Ra':226.00000,
        'Ac':227.00000,'Th':232.03810,'Pa':231.03588,'U':238.02891,'Np':237.00000,'Pu':244.00000,'Am':243.00000,
        'Cm':247.00000,'Bk':247.00000,'Cf':251.00000,'Es':252.00000,'Fm':257.00000,'Md':258.00000,'No':259.00000,
        'Lr':262.00000,'Rf':261.00000,'Db':262.00000,'Sg':266.00000,'Bh':264.00000,'Hs':277.00000,'Mt':268.00000,
        'Ds':281.00000,'Rg':280.00000,'Cn':285.00000,'D':2.01363,'T':3.01605}

def molecule_compare(molecule_a, molecule_b):
    if isinstance(molecule_a, MOL) == False or isinstance(molecule_b, MOL) == False:
        print(""""ERROR: The function "molecule_compare" can handle only MOL class type objects""")
    


class MOL(coor.XYZ):
    """The MOL class allow the loading and the manipulation of molecular data"""
    def mass(self):
        """Returns the mass of the molecule in u.m.a."""
        m = 0
        for atom in self.element:
            m += atomic_mass[atom]
        return m
    
    def rcm(self):
        """Returns the position of the center of mass of the molecule"""
        r = []
        for col in range(0, 3):
            var = 0
            for row in range(0, self.natoms):
                var += atomic_mass[self.element[row]]*self.xyz[row][col]
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
            atom[2] = 100.*atom[1]*atomic_mass[atom[0]]/self.mass()
        if order == "number":
            comp.sort(key=lambda x: x[1], reverse=True)
        else:
            comp.sort(key=lambda x: x[2], reverse=True)
        return comp



    

molecola = MOL("./example.xyz")
print(molecola.composition())

