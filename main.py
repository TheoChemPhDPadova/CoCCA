"""Menu Interface"""
import sys, os
import utils, trj_int, trj_ana, trj_pru, trj_qst, pro_pru, con_gen
import neb_vis, nei_fin, out_sum
import molecule as mol

__VERSION__ = '1.0'


def main():
    utils.header(__VERSION__)
    print("""
1) Trajectory Manipulation
2) PDB Tools
3) Others
4) Molecular properties and vibrations

q) Exit
    """)

    choice = input("\nSelection:\t")
    if choice == "1":
        data_manipulation()
    elif choice == "2":
        analysis()
    elif choice == "3":
        input_generation()
    elif choice == "4":
        molecule_interface()
    elif choice == "q":
        sys.exit()


def data_manipulation():
    """Trajectory Manipulation"""
    utils.header(__VERSION__)
    print("""
1) Resizer                      (TRJ/GENERAL/ORCA)
2) Analyzer/Freezer             (TRJ/GENERAL)
3) Slicer                       (TRJ/GENERAL)
4) TRJ 2 QST2/QST3              (TRJ/Gaussian)

b) Back to Main Menu
q) Exit
    """)
    choice = input("\nSelection:\t")
    if choice == "1":
        trj_int.main()
    elif choice == "2":
        trj_ana.main()
    elif choice == "3":
        trj_pru.main()
    elif choice == "4":
        trj_qst.main()
    elif choice == "b":
        main()
    elif choice == "q":
        sys.exit()


def analysis():
    """PDB Tools menu"""
    utils.header(__VERSION__)
    print("""
1) Neighbor Finder              (PDB)
2) Catalytic Pocket Selector    (PDB)

b) Back to Main Menu
q) Exit
    """)
    choice = input("\nSelection:\t")
    if choice == "1":
        nei_fin.main()
    elif choice == "2":
        pro_pru.main()
    elif choice == "b":
        main()
    elif choice == "q":
        sys.exit()


def input_generation():
    """Others menu"""
    utils.header(__VERSION__)
    print("""
1) Constraints Generator              (XYZ/GENERAL)

b) Back to Main Menu
q) Exit
    """)
    choice = input("\nSelection:\t")
    if choice == "1":
        con_gen.main()
    elif choice == "b":
        main()
    elif choice == "q":
        sys.exit()


def molecule_interface():
    """Molecule class menu"""
    def ask_ID():
        ID = int(input("Select the molecule ID (from 1 to " + str(len(MOL_LIST)) + "):\t"))
        if ID < 1 and ID > len(MOL_LIST):
            print("ERROR: The selected ID does not exist")
            molecule_interface()
        print("Selected ID: " + str(ID) + "\tMolecule name: " + str(MOL_LIST[ID-1].name) + "\n")
        return ID


    def list_molecules():
        print("\n            LIST OF LOADED MOLECULES")
        print("------------------------------------------------\n")
        print("ID\tNAME\n")
        for i, myclass in enumerate(MOL_LIST):
            print(str(i+1) + "\t" + myclass.name)

    utils.header(__VERSION__)
    print("""
1) Load molecule from .xyz file
2) Load vibrational data from .hess file (ORCA)
3) Plot IR spectra
4) Compute properties
5) Linear transit

l) List loaded molecules

b) Back to Main Menu
q) Exit
    """)
    choice = input("\nSelection:\t")
    if choice == "1":
        utils.header(__VERSION__)
        path = input("\nSelect the path of the .xyz file:\t")
        MOL_LIST.append(mol.MOL(path))
        print("\nMolecule saved with the ID:\t" + str(len(MOL_LIST))) 
        input("\nPress enter to return to the menu ...   ")
        molecule_interface()
    elif choice == "2":
        utils.header(__VERSION__)
        path = input("\nSelect the path of the .hess file:\t")
        ID = ask_ID()
        MOL_LIST[ID-1].load_hess_file(path, verbose=True)
        input("\nPress enter to return to the menu ...   ")
        molecule_interface()
    elif choice == "3":
        os.system("clear")
        print("================================================")
        print("               VIBRATIONAL SPECTRUM")
        print("================================================\n")
        ID = ask_ID()
        type_of_plot = input("Select the type of plot (gaussian, lorentzian, bar):\t")
        if type_of_plot == "gaussian" or type_of_plot == "lorentzian":
            width = input("Select the amplitude parameter (in cm^-1): ")
            mol.plot_ir_spectrum(MOL_LIST[ID-1], width, style=type_of_plot)
            save_state = input("\nDo you want to save the plot (y/n):\t")
            if save_state == "y":
                path = input("Select the path to the destination folder:\t")
                mol.plot_ir_spectrum(MOL_LIST[ID-1], width, style=type_of_plot, path=path, show=False)
        else:
            mol.plot_ir_spectrum(MOL_LIST[ID-1], style=type_of_plot)
            save_state = input("\nDo you want to save the plot (y/n):\t")
            if save_state == "y":
                path = input("Select the path to the destination folder:\t")
                mol.plot_ir_spectrum(MOL_LIST[ID-1], style=type_of_plot, path=path, show=False)
        molecule_interface()
    elif choice == "4":
        os.system("clear")
        print("================================================")
        print("       MOLECULAR PROPERTIES COMPUTATION")
        print("================================================\n")
        print("""
1) General informations

b) Back
q) Exit
        """)
        calculation_choice = input("\nSelection:\t")
        if calculation_choice == "1":
            os.system("clear")
            print("================================================")
            print("               GENERAL PROPERTIES")
            print("================================================")
            list_molecules()
            print("\n================================================")
            molecule_selection = input("""
Select the ID of the molecules divided by comma
(type "all" if you want all the entries):\t""")
            if molecule_selection == "all":
                molecule_selection = list(range(0, len(MOL_LIST)))
            else:
                molecule_selection = [int(i) for i in molecule_selection.split(",")]
            os.system("clear")
            print("================================================")
            print("               GENERAL PROPERTIES")
            print("================================================")
            print("\nSelected molecules: ", molecule_selection)
            for myID in molecule_selection:
                myMol = MOL_LIST[myID-1]
                print("\n Molecule: " + myMol.name + "\t(ID: " + str(myID) + ")" )
                print("------------------------------------------------\n")
                print("Composition:")
                comp_list = myMol.composition()
                print("ATOM\tN\t%MASS")
                for line in comp_list:
                    print(str(line[0]) + "\t" + str(line[1]) + "\t" + str(line[2]))
                print("\n")
                print("Center of mass (Angstrom):")
                print("\tx:\t" + str(myMol.rcm()[0]))
                print("\ty:\t" + str(myMol.rcm()[1]))
                print("\tz:\t" + str(myMol.rcm()[2]))
            input("\nPress enter to return to the menu ...   ")
            molecule_interface()
        elif calculation_choice == "b":
            molecule_interface()
        elif calculation_choice == "q":
            sys.exit()
    elif choice == "5":
        os.system("clear")
        print("================================================")
        print("              LINEAR TRANSIT MODULE")
        print("================================================")
        print("Select the ID for the start and end structures\n")
        ID_start = ask_ID()
        ID_end = ask_ID()
        n_steps = int(input("Select the number of intermediate structures:\t"))
        path = input("Select the destination path (without final extension):\t")
        print('\n')
        mol.rigid_linear_transit(MOL_LIST[ID_start-1], MOL_LIST[ID_end-1], n_steps, path)
        molecule_interface()
    elif choice == "l":
        utils.header(__VERSION__)
        list_molecules()
        input("\nPress enter to return to the menu ...   ")
        molecule_interface()
    elif choice == "b":
        main()
    elif choice == "q":
        sys.exit()


MOL_LIST = []

if len(sys.argv) == 1:
    main()
else:
    utils.header(__VERSION__)
    if sys.argv[1].split(".")[-1] == "interp":
        print("\nQUICK MODE: Detected .interp file. Opening as fast as I can...")
        neb_vis.main(sys.argv[1])
    elif sys.argv[1].split(".")[-1] == "out":
        print("\nQUICK MODE: Detected .out file. Opening as fast as I can...")
        out_sum.main(sys.argv[1])
    elif sys.argv[1] == "load":
        print("\nQUICK MODE: Detected load instruction.\nLoading .xyz files...")
        print("------------------------------------------------")
        for i, argument in enumerate(sys.argv):
            if i > 1 and argument.split(".")[-1] == "xyz":
                MOL_LIST.append(mol.MOL(argument))
                print("Molecule saved with the ID:\t" + str(len(MOL_LIST)))
        print("------------------------------------------------")
        print("Loading DONE. " + str(len(MOL_LIST)) + " files loaded succesfully")
        input("\nPress enter to continue ...   ")
        main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
