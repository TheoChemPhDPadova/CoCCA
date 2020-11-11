"""Trajectory Analyzer/Freezer"""
import sys, os
import utils
import numpy as np


def main():
    utils.TITLE("Trajectory Analyzer/Freezer")

    cat_d = [[], [], [], []]

    TRJ = utils.TRJ(input("Enter trajectory file path...\t"))
    print("\nATOM\tELEM\tSTD\t\tSTATUS\n")
    for i in range(0, TRJ.natoms):
        tmp = []
        for j in range(0, TRJ.nspas):
            tmp.append(TRJ.trajectory[j][i][1:])
        atom_std = np.std(tmp, axis=0)
        if np.sum(atom_std) < 0.001:
            FRZ_STATUS = "FROZEN"
            cat_d[0].append(i + 1)
        elif np.sum(atom_std) >= 0.001 and np.sum(atom_std) < 0.3:
            FRZ_STATUS = "+"
            cat_d[1].append(i + 1)
        elif np.sum(atom_std) >= 0.3 and np.sum(atom_std) < 0.5:
            FRZ_STATUS = "++"
            cat_d[2].append(i + 1)
        elif np.sum(atom_std) >= 0.5:
            FRZ_STATUS = "+++"
            cat_d[3].append(i + 1)

        print("{}\t{}\t{:.5f}\t\t{}".format(i + 1, TRJ.trajectory[j][i][0], np.sum(atom_std), FRZ_STATUS))

    print("\nDISPLACEMENTS\tATOMS\n")
    print("FROZEN:\t\t{}".format(" ".join([str(i) for i in cat_d[0]])))
    print("LOW:\t\t{}".format(" ".join([str(i) for i in cat_d[1]])))
    print("MEDIUM:\t\t{}".format(" ".join([str(i) for i in cat_d[2]])))
    print("HIGH:\t\t{}".format(" ".join([str(i) for i in cat_d[3]])))

    FRZ_LIST = input("\nDo you want to CONSTRAIN some particular atom along the TRJ?\n\n").split()
    FRZ_LIST = [int(i) for i in FRZ_LIST]
    with open("./newTRAJ.xyz", 'a') as out:
        for idx_i, val_i in enumerate(TRJ.trajectory):
            out.write("{}\n".format(str(TRJ.natoms)))
            out.write("Trajectory {}\n".format(idx_i + 1))
            for idx_j, val_j in enumerate(val_i):
                if idx_j + 1 in FRZ_LIST:
                    out.write("{} \t{:.10f}\t {:.10f}\t {:.10f} \n".format(
                        TRJ.trajectory[0][idx_j][0],
                        TRJ.trajectory[0][idx_j][1],
                        TRJ.trajectory[0][idx_j][2],
                        TRJ.trajectory[0][idx_j][3]
                    ))
                else:
                    out.write("{} \t{:.10f}\t {:.10f}\t {:.10f} \n".format(
                        val_j[0],
                        val_j[1],
                        val_j[2],
                        val_j[3]
                    ))

    utils.NT()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
