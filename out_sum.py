"""QM output reader"""
import sys
import argparse, QM_parser
import matplotlib.pyplot as plt


def main(path):
    with open(path) as file:
        out = file.read()

    if 'Amsterdam Density Functional  (ADF)' in out or 'Amsterdam Modeling Suite (AMS)' in out:
        src = QM_parser.AMS(path)
    elif 'O   R   C   A' in out:
        src = QM_parser.ORCA(path)
    else:
        print('\nSorry, output file not supported!')
        sys.exit()

    plt.rc('font', family='serif')
    fig = plt.figure()
    fig.canvas.set_window_title(src.version)

    ax1 = plt.subplot(331)
    plt.plot(src.ene, marker=".", markersize=7, lw=1)
    plt.ylabel('Hartree')
    plt.title('Energy')
    plt.xlim(0, len(src.ene)-1)

    plt.subplot(332)
    plt.plot(src.grdmax, marker=".", markersize=7, lw=1)
    plt.axhline(y=src.grdmaxlim, color='r', linestyle='-', lw=1.5)
    if src.grdmax[-1] < src.grdmaxlim:
        plt.axhline(y=src.grdmaxlim, color='#3bd636', linestyle='-', lw=1.5)
    else:
        plt.axhline(y=src.grdmaxlim, color='r', linestyle='-', lw=1.5)
    plt.ylabel('Hartree')
    plt.title('Gradient MAX')
    plt.xlim(0, len(src.ene)-1)

    plt.subplot(333)
    plt.plot(src.stpmax, marker=".", markersize=7, lw=1)
    plt.axhline(y=src.stpmaxlim, color='r', linestyle='-', lw=1.5)
    if src.stpmax[-1] < src.stpmaxlim:
        plt.axhline(y=src.stpmaxlim, color='#3bd636', linestyle='-', lw=1.5)
    else:
        plt.axhline(y=src.stpmaxlim, color='r', linestyle='-', lw=1.5)
    plt.ylabel('Hartree')
    plt.title('Displacement MAX')
    plt.xlim(0, len(src.ene)-1)

    plt.subplot(334)
    plt.plot(src.enechg, marker=".", markersize=7, lw=1)
    plt.axhline(y=src.enelim, color='r', linestyle='-', lw=1.5)
    if src.enechg[-1] < src.enelim:
        plt.axhline(y=src.enelim, color='#3bd636', linestyle='-', lw=1.5)
    else:
        plt.axhline(y=src.enelim, color='r', linestyle='-', lw=1.5)
    plt.ylabel('Hartree')
    plt.title('|Energy Change|')
    plt.xlim(0, len(src.ene)-1)

    plt.subplot(335)
    plt.plot(src.grdrms, marker=".", markersize=7, lw=1)
    plt.axhline(y=src.grdrmslim, color='r', linestyle='-', lw=1.5)
    if src.grdrms[-1] < src.grdrmslim:
        plt.axhline(y=src.grdrmslim, color='#3bd636', linestyle='-', lw=1.5)
    else:
        plt.axhline(y=src.grdrmslim, color='r', linestyle='-', lw=1.5)
    plt.ylabel('Hartree')
    plt.title('Gradient RMS')
    plt.xlim(0, len(src.ene)-1)

    plt.subplot(336)
    plt.plot(src.stprms, marker=".", markersize=7, lw=1)
    plt.axhline(y=src.stprmslim, color='r', linestyle='-', lw=1.5)
    if src.stprms[-1] < src.stprmslim:
        plt.axhline(y=src.stprmslim, color='#3bd636', linestyle='-', lw=1.5)
    else:
        plt.axhline(y=src.stprmslim, color='r', linestyle='-', lw=1.5)
    plt.ylabel('Hartree')
    plt.title('Displacement RMS')
    plt.xlim(0, len(src.ene)-1)

    plt.subplot(337)
    plt.plot(src.eigen[0], marker=".", markersize=7, lw=1)
    plt.plot(src.eigen[1], marker=".", markersize=7, lw=1)
    plt.plot(src.eigen[2], marker=".", markersize=7, lw=1)
    plt.plot(src.eigen[3], marker=".", markersize=7, lw=1)
    plt.plot(src.eigen[4], marker=".", markersize=7, lw=1)

    plt.axhline(y=0, color='black', linestyle='--', lw=1)
    plt.title('Hessian Eigenvector')
    plt.xlim(0, len(src.ene)-1)

    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-i", "--input", type=str, help="Path of the output file...")
    ARGS = PARSER.parse_args()
    main(ARGS.input)
