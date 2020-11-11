"""Neb Visualizer"""
import sys, os
import argparse, utils
import matplotlib.pyplot as plt
import constants as k


def main(ARGS):
    utils.TITLE("NEB Visualizer (ORCA)")

    if ARGS.input:
        FILENAME = ARGS.input
    else:
        FILENAME = input("Enter .interp file path...\t\t")

    with open(FILENAME) as file:
        lines = file.readlines()

    idx_pts = []
    idx_int = []

    for idx, val in enumerate(lines):
        if "Images:" in val:
            idx_pts.append(idx + 1)
        elif "Interp.:" in val:
            idx_int.append(idx + 1)

    pts_n = idx_int[0] - 6

    if len(idx_pts) != 1:
        int_n = idx_pts[1] - idx_int[0] - 3
    else:
        int_n = len(lines) - idx_int[0]

    for i in idx_pts:
        if i == idx_pts[0]:
            x = [float(lines[j].split()[0]) for j in range(i, i+pts_n)]
            y = [float(lines[j].split()[2])*k.ha2kcal for j in range(i, i+pts_n)]
            plt.scatter(x, y, s=15, c="orange")
        elif i == idx_pts[-1]:
            x = [float(lines[j].split()[0]) for j in range(i, i+pts_n)]
            y = [float(lines[j].split()[2])*k.ha2kcal for j in range(i, i+pts_n)]
            plt.scatter(x, y, s=15, c="cornflowerblue", zorder=10)
        else:
            x = [float(lines[j].split()[0]) for j in range(i, i+pts_n)]
            y = [float(lines[j].split()[2])*k.ha2kcal for j in range(i, i+pts_n)]
            plt.scatter(x, y, s=7, c="gainsboro")

    for i in idx_int:
        if i == idx_int[0]:
            x = [float(lines[j].split()[0]) for j in range(i, i+int_n)]
            y = [float(lines[j].split()[2])*k.ha2kcal for j in range(i, i+int_n)]
            plt.plot(x, y, c="orange")
        elif i == idx_int[-1]:
            x = [float(lines[j].split()[0]) for j in range(i, i+int_n)]
            y = [float(lines[j].split()[2])*k.ha2kcal for j in range(i, i+int_n)]
            plt.plot(x, y, c="cornflowerblue", zorder=10)
        else:
            x = [float(lines[j].split()[0]) for j in range(i, i+int_n)]
            y = [float(lines[j].split()[2])*k.ha2kcal for j in range(i, i+int_n)]
            plt.plot(x, y, c="gainsboro")

    plt.xlim(0, 1)
    plt.show()


if __name__ == "__main__":
    try:
        PARSER = argparse.ArgumentParser()
        PARSER.add_argument("-i", "--input", type=str, help="Path of the .interp file (ORCA)")
        ARGS = PARSER.parse_args()
        main(ARGS)
    except KeyboardInterrupt:
        print("Interrupted by user")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
