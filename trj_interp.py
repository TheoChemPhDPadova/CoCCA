"""
Script to extend a trajectory from ORCA NEB run/General TRJ file to redistribute or 
include more/less images by linear interpolation. 
New number of images is given by the variable npts

Thanks to original author: Vilhjalmur Asgeirsson (UI, 2018) - Script extended and adapted
"""
import sys, readline, glob, os, utilities
import numpy as np

def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

def Displacement(ndim, nim, R):

    """
    Computes straight line distances between adjacent pair of images
    and then sums up the distances
    """
    displ = np.zeros(shape=(nim,))
    for i in range(1, nim):
        R0 = R[(i - 1) * ndim:(i) * ndim]
        R1 = R[(i) * ndim:(i + 1) * ndim]
        dR = R1-R0
        displ[i] = displ[i - 1] + np.sqrt(np.dot(dR.T,dR))

    return displ

def LinearInterpolateData(nlen, xData, yData, xnew):

    """
    Linear interpolation of data points (xData, yData) to point xnew
    """
    i = 0
    if (xnew >= xData[nlen - 2]):
        i = nlen - 2
    else:
        while (xnew > xData[i + 1]):
            i = i + 1

    xL = xData[i]
    yL = yData[i]
    xR = xData[i + 1]
    yR = yData[i + 1]

    if (xnew < xL):
        yR = yL
    if (xnew > xR):
        yL = yR
    dydx = (yR - yL) / (xR - xL)

    return yL + dydx * (xnew - xL)


def GenerateNewPath(ndim, nim, npoints, S, R):

    """
    Generates new path, newR of npoints images, from path R with nim images
    """
    
    newR = np.zeros(shape=(ndim * npoints, 1))
    xi = np.linspace(S[0], S[-1], npoints)

    for i in range(ndim):
        Rdof = np.zeros(shape=(nim, 1))
        dRdof = np.zeros(shape=(nim, 1))
        for j in range(nim):
            Rdof[j] = R[j * ndim + i]

        for xpt in range(npoints):
            new_y = LinearInterpolateData(nim, S, Rdof, xi[xpt])
            newR[xpt * ndim + i] = new_y

    return newR

def ReadFirstLineOfFile(fname):
    with open(fname) as f:
        first_line = f.readline()
    return first_line

def WriteTraj(fname, ndim, nim, R, E, symb3, restart = "n"):

    if len(symb3) != ndim:
        raise RuntimeError("Error in WriteTraj. Dimension mismatch: symb3")
    if len(E) != nim:
        raise RuntimeError("Error in WriteTraj. Dimension mismatch: E")
    if len(R) != ndim*nim:
        raise RuntimeError("Error in WriteTraj. Dimension mismatch: R")
    
    f = open(fname, 'w')
    natoms = ndim / 3
    for i in range(nim):
        hnit = R[i * ndim:(i + 1) * ndim]
        f.write("%i \n" % natoms )
        f.write('E=%12.8f \n' % E[i])
        for j in range(0, len(hnit), 3):
            f.write('%s %12.8f %12.8f %12.8f\n' % (symb3[j].strip(), hnit[j], hnit[j + 1], hnit[j + 2]))
        if restart == "y" and i + 1 != nim:
            f.write('>\n')
    f.close()
    
    return None

def ReadTraj(fname):
    if not os.path.isfile(fname):
        raise RuntimeError("File %s not found " % fname)

    extension = fname.split('.')[-1]
    
    # Get first line of the file (i.e. number of atoms)
    first_line = ReadFirstLineOfFile(fname)

    try:
        natoms = int(first_line)
    except:
        raise TypeError("%s is not correctly formatted trajectory file")
    
    ndim = natoms * 3

    # begin by reading the contents of the file to a list
    contents = []
    f = open(fname).readlines()
    for i, line in enumerate(f):
        contents.append(line)
    
    if ">\n" in contents:
        print('\n--ORCA Restart file detected!')
        contents = [i for i in contents if i != ">\n"]
    else:
        print('\n--Normal TRJ file detected!')

    # get number of lines and hence number of images
    number_of_lines = i + 1
    nim = int((number_of_lines) / (natoms + 2))

    RPATH = []
    ind = 0
    for i in range(nim):
        symb3 = []
        ind = ind + 2
        for j in range(natoms):
            geom_line = contents[ind]
            geom_line = geom_line.split()
            symb3.append(geom_line[0].strip())
            symb3.append(geom_line[0].strip())
            symb3.append(geom_line[0].strip())
            RPATH.append(float(geom_line[1]))
            RPATH.append(float(geom_line[2]))
            RPATH.append(float(geom_line[3]))
            ind += 1

    RPATH = np.reshape(RPATH, (nim * ndim, 1))

    return RPATH, ndim, nim, symb3


if __name__ == "__main__":

    print("""
================================================
     Linear interpolation of a trajectory
================================================
""")

    # ============================================
    # default values
    # ============================================
    fname = input("Enter .xyz trajectory file path...\t")
    TRJ = utilities.TRJ(fname)

    npts = int(input("\nNumber of final points...\t"))

    # ============================================
    # Get inp arguments
    # ============================================

    # Notice that the order of the arguments matters.
    for i in range(len(sys.argv)):
        if i == 1:
            fname = sys.argv[1]
        if i == 2:
            try:
                npts = int(sys.argv[2])
            except:
                raise TypeError("Int. expected as a second arg")

    file_extension = fname.split('.')[1]
    # ============================================
    # Read trajectory file
    # ============================================
    name_string = fname.split('.')
    basename = name_string[0]
    file_extension = name_string[1]

    R, ndim, nim, symb3 = ReadTraj(fname)
    print('--Found %i images with %i atoms' %  (nim, ndim/3))
    print('--Interpolating to %i points' % (npts))
    restart = input("\nSave as a ORCA Restart file? [y/n]...\t")
    if npts > nim:
        fname_output = basename+'_exte.'+file_extension
    elif npts == nim:
        fname_output = basename+'_redistri.'+file_extension
    else:
        fname_output = basename+'_reduc.'+file_extension
    
    if restart == "y":
        fname_output = 'restart.allxyz'
    
    print('--output file: %s' % fname_output)
    

    # ============================================
    # Perform interpolation
    # ============================================
    S = Displacement(ndim, nim, R)
    newR = GenerateNewPath(ndim, nim, npts, S, R)
    
    # ============================================
    # Write new trajectory file
    # ============================================
    E = np.zeros(shape=(npts,1))
    if restart == "y":
        WriteTraj(fname_output, ndim, npts, newR, E, symb3, restart)
    else:
        WriteTraj(fname_output, ndim, npts, newR, E, symb3)
    
    RP_SAVE = input("\nSave R/P files? [y/n]...\t")
    if RP_SAVE == 'y':
        with open("./R.xyz", 'a') as out:
            out.write("{}\n".format(str(TRJ.natoms)))
            out.write("Reactants\n")
            for i in TRJ.trajectory[0]:
                out.write("{} \t{:.10f}\t {:.10f}\t {:.10f} \n".format(i[0], i[1], i[2], i[3]))
        with open("./P.xyz", 'a') as out:
            out.write("{}\n".format(str(TRJ.natoms)))
            out.write("Products\n")
            for i in TRJ.trajectory[-1]:
                out.write("{} \t{:.10f}\t {:.10f}\t {:.10f} \n".format(i[0], i[1], i[2], i[3]))

    print('Done.')
