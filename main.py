"""Menu Interface"""
import os

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
2) Analysis
3) Input Generation

q) Exit
    """)

    choice = input("\nSelection:\t")
    if choice == "1":
        data_manipulation()
    elif choice == "2":
        pass
    elif choice == "3":
        pass
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

main()
