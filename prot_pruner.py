"""PDB CatPocket Pruning Tool"""
import itertools, coor, readline, glob, utilities
import numpy as np

def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind('tab: complete')
readline.set_completer(complete)

def multiple_parser(inp_list):
    """Multiple input parser"""
    out_list = []
    for k in inp_list:
        if "-" in k:
            for l in range(int(k.split('-')[0]), int(k.split('-')[1]) + 1):
                if int(l) not in out_list:
                    out_list.append(int(l))
        else:
            if int(k) not in out_list:
                out_list.append(int(k))
    return out_list

def group_ranges(L):
    """
    Collapses a list of integers into a list of the start and end of
    consecutive runs of numbers. Returns a generator of generators.
    """
    for w, z in itertools.groupby(L, lambda x, y=itertools.count(): next(y)-x):
        grouped = list(z)
        yield (x for x in [grouped[0], grouped[-1]][:len(grouped)])

def saturate(C_tgt, ref_atom):
    """Saturate the valence of a carbon atom with hydrogen

    Args:
        C_tgt (list): Cartesian coordinate of C atom to saturate [X, Y, Z]
        ref_atom (list): Cartesian coordinate of an atom directly bonded to C_tgt. This is used to create a vector for the rotation of hydrogen atoms [X, Y, Z]
    Returns:
        [type]: Distance between atom_a and atom_b
    """
    MG = [
        ['H', -0.510365374578, -0.883978759193, 0.399020000000],
        ['H', 1.020730749156, 0.000000000000, 0.399020000000],
        ['H', -0.510365374578, 0.883978759193, 0.399020000000]
    ]

    vec_MG = [0.0, 0.0, -1.4]
    vec_TGT = [
        ref_atom[0] - C_tgt[0],
        ref_atom[1] - C_tgt[1],
        ref_atom[2] - C_tgt[2],
    ]

    rot_mat = utilities.rot_mat_v(vec_MG, vec_TGT)
    H_end = []
    for i in MG:
        MG_rot = np.matmul(rot_mat, np.array(i[1:4]))
        MG_rot = MG_rot + C_tgt
        H_end.append([i[0], MG_rot[0], MG_rot[1], MG_rot[2]])

    return H_end


print("""
================================================
         PDB CatPocket Pruning Tool
================================================
""")

filename = input('Enter .PDB file name...\t\t')
PRO = coor.PDB(filename)
SelC = input('Select chain/s...\t\t')
SelRSN = multiple_parser(input('Select residues...\t\t').split())
SelRSN.sort()

GrpRSN = [list(x) for x in group_ranges(SelRSN)]

print('\nNumber of groups detected...\t{}'.format(len(GrpRSN)))
print('Number of terminations...\t{}'.format(2*len(GrpRSN)))

for idx, val in enumerate(GrpRSN):
    print('\n>> Group:\t{}'.format(str(idx + 1)))
    for j in range(val[0], val[-1] + 1):
        print('\t', PRO.prot[SelC][str(j)][0][2], str(j))

TGroup = input('\nSelect terminations:\n1)   ACE/NME\n2)   Marker Atom\n3)   No Terminations\n\nSelection: ')

if TGroup == '2':
    Mk_Atom = input('\nWhich atom do you like to place as a marker?...\t')

MOL = []
for GRP in GrpRSN:
    for AA in range(GRP[0], GRP[-1] + 1):
        for ATOM in PRO.prot[SelC][str(AA)]:
            MOL.append("{} \t{:.3f}\t {:.3f}\t {:.3f}".format(ATOM[8], ATOM[5], ATOM[6], ATOM[7]))

        #ACE
        if AA == GRP[0] and TGroup == '1':
            for ATOM in PRO.prot[SelC][str(AA - 1)]:
                if ATOM[1] == 'O':
                    MOL.append("{} \t{:.3f}\t {:.3f}\t {:.3f}".format(ATOM[8], ATOM[5], ATOM[6], ATOM[7]))
                elif ATOM[1] == 'C':
                    C_atom = ATOM
                    MOL.append("{} \t{:.3f}\t {:.3f}\t {:.3f}".format(ATOM[8], ATOM[5], ATOM[6], ATOM[7]))
                elif ATOM[1] == 'CA':
                    CA_atom = ATOM
                    MOL.append("{} \t{:.3f}\t {:.3f}\t {:.3f}".format(ATOM[8], ATOM[5], ATOM[6], ATOM[7]))

            H_Met = saturate(CA_atom[5:8], C_atom[5:8])
            for i in H_Met:
                MOL.append("{} \t{:.3f}\t {:.3f}\t {:.3f}".format(i[0], i[1], i[2], i[3]))

        #NME
        if AA == GRP[-1] and TGroup == '1':
            for ATOM in PRO.prot[SelC][str(AA + 1)]:
                if ATOM[1] == 'NH':
                    MOL.append("{} \t{:.3f}\t {:.3f}\t {:.3f}".format(ATOM[8], ATOM[5], ATOM[6], ATOM[7]))
                elif ATOM[1] == 'N':
                    C_atom = ATOM
                    MOL.append("{} \t{:.3f}\t {:.3f}\t {:.3f}".format(ATOM[8], ATOM[5], ATOM[6], ATOM[7]))
                elif ATOM[1] == 'CA':
                    CA_atom = ATOM
                    MOL.append("{} \t{:.3f}\t {:.3f}\t {:.3f}".format(ATOM[8], ATOM[5], ATOM[6], ATOM[7]))
                    
            H_Met = saturate(CA_atom[5:8], C_atom[5:8])
            for i in H_Met:
                MOL.append("{} \t{:.3f}\t {:.3f}\t {:.3f}".format(i[0], i[1], i[2], i[3]))

        if AA == GRP[0] and TGroup == '2':
            for ATOM in PRO.prot[SelC][str(AA - 1)]:
               if ATOM[1] == 'C':
                   MOL.append("{} \t{:.3f}\t {:.3f}\t {:.3f}".format(Mk_Atom, ATOM[5], ATOM[6], ATOM[7]))

        if AA == GRP[-1] and TGroup == '2':
            for ATOM in PRO.prot[SelC][str(AA + 1)]:
                if ATOM[1] == 'N':
                    MOL.append("{} \t{:.3f}\t {:.3f}\t {:.3f}".format(Mk_Atom, ATOM[5], ATOM[6], ATOM[7]))


with open(filename + '.' + SelC + '.pruned.xyz', 'w') as out:
    out.write(str(len(MOL)) + '\n')
    out.write('AA: ' + str(SelRSN) + ' Chain: ' + SelC + '\n')
    for i in MOL:
        out.write(i + '\n')
    out.close()

print("""

Pruned structure has been saven in: {}

================================================
             NORMAL TERMINATION    
================================================
""".format(filename + '.' + SelC + '.pruned.xyz'))
