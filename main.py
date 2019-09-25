"""Menu Interface"""
import os, sys
import molecule as mol

def header():
    """Logo"""
    os.system("clear")
    print("""
================================================
         __
   ///  /  )   _____       _____  _____   ___  
  |@  \/   )  /  __ \     /  __ \/  __ \ / _ \     
 < (  (____)  | /  \/ ___ | /  \/| /  \// /_\ \\
   \      )   | |    / _ \| |    | |    |  _  |
    \____/    | \__/\ (_) | \__/\| \__/\| | | |
    __||__     \____/\___/ \____/ \____/\_| |_/
    
================================================""")

def main():
    """MainMenu"""
    header()
    print("""
1) Data Manipulation
2) Structure Analysis
3) Input Generation
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
        quit()

def data_manipulation():
    """Data Manipulation menu"""
    header()
    print("""
1) ...

b) Back to Main Menu
q) Exit
    """)
    choice = input("\nSelection:\t")
    if choice == "1":
        pass
    elif choice == "b":
        main()
    elif choice == "q":
        quit()

def analysis():
    """Structure Analysis menu"""
    header()
    print("""
1) Neighbor Finder (PDB)
2) NEB Visualizer (ORCA)

b) Back to Main Menu
q) Exit
    """)
    choice = input("\nSelection:\t")
    if choice == "1":
        os.system("python3 " + sys.path[0] + "/neigh_finder.py")
    elif choice == "2":
        os.system("python3 " + sys.path[0] + "/neb_visualizer.py")
    elif choice == "b":
        main()
    elif choice == "q":
        quit()

def input_generation():
    """Input Generation menu"""
    header()
    print("""
1) Constraints Generator (XYZ)

b) Back to Main Menu
q) Exit
    """)
    choice = input("\nSelection:\t")
    if choice == "1":
        os.system("python3 " + sys.path[0] + "/const_generator.py")
    elif choice == "b":
        main()
    elif choice == "q":
        quit()

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

    header()
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
        header()
        path = input("\nSelect the path of the .xyz file:\t")
        MOL_LIST.append(mol.MOL(path))
        print("\nMolecule saved with the ID:\t" + str(len(MOL_LIST))) 
        input("\nPress enter to return to the menu ...   ")
        molecule_interface()
    elif choice == "2":
        header()
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
            quit()
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
        header()
        list_molecules()
        input("\nPress enter to return to the menu ...   ")
        molecule_interface()
    elif choice == "b":
        main()
    elif choice == "q":
        quit()

MOL_LIST = []

if len(sys.argv) == 1:
    main()
else:
    header()
    if sys.argv[1].split(".")[-1] == "interp":
        print("\nQUICK MODE: Detected .interp file. Opening as fast as I can...")
        os.system("python3 " + sys.path[0] + "/neb_visualizer.py -i " + sys.argv[1])
    elif sys.argv[1].split(".")[-1] == "out":
        header()
        print("\nQUICK MODE: Detected .out file. Opening as fast as I can...")
        os.system("python3 " + sys.path[0] + "/output_sum.py " + sys.argv[1])
    elif sys.argv[1] == "load":
        print("\nQUICK MODE: Detected load instruction.\nLoading .xyz files...")
        print("------------------------------------------------")
        for i, argument in enumerate(sys.argv):
            if i>1 and argument.split(".")[-1] == "xyz":
                MOL_LIST.append(mol.MOL(argument))
                print("Molecule saved with the ID:\t" + str(len(MOL_LIST)))
        print("------------------------------------------------")
        print("Loading DONE. " + str(len(MOL_LIST)) + " files loaded succesfully")
        input("\nPress enter to continue ...   ")
        main()
