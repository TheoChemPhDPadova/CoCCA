"""Menu Interface"""
import os, sys

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

q) Exit
    """)

    choice = input("\nSelection:\t")
    if choice == "1":
        data_manipulation()
    elif choice == "2":
        analysis()
    elif choice == "3":
        input_generation()
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

if len(sys.argv) == 1:
    main()
elif sys.argv[1].split(".")[-1] == "interp":
    header()
    os.system("python3 " + sys.path[0] + "/neb_visualizer.py -i " + sys.argv[1])
