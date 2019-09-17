import numpy as np
import sys, coor

def dist(vec1,vec2):
    return float(np.sqrt((vec1[0]-vec2[0])**2+(vec1[1]-vec2[1])**2+(vec1[2]-vec2[2])**2))

print('''
    ================================
           Neighbor Finder 
    ================================
''')

PRT = coor.PDB(sys.argv[1]).prot

SelCHAIN = input('Select chain...\t\t\t')
SelRSN = input('Select residue...\t\t')
print('\nDetected Atom Type in', SelRSN, PRT[SelCHAIN][SelRSN][0][2], ':\n')
for i in PRT[SelCHAIN][SelRSN]:
    print('>> ',i[1])

SelAT = input('\nSelect Atom Type:\t')

TGT=[i for i in PRT[SelCHAIN][SelRSN] if i[1]==SelAT][0]

distTGT={}

for i in PRT[SelCHAIN]:
    for j in PRT[SelCHAIN][i]:
        distance=dist([TGT[5], TGT[6], TGT[7]], [j[5], j[6], j[7]])
        if j[4] not in distTGT:
            distTGT[j[4]] = distance
        elif j[4] in distTGT:
            if distance < float(distTGT[j[4]]):
                distTGT[j[4]] = distance
        else:
            print('ERROR!')

POS_AA = ['ARG', 'HIS', 'LYS']
NEG_AA = ['ASP', 'GLU']

try:
    while True:
        THR_DIST = float(input('Select cutoff distance...\t'))
        print('\n\nResID\tDIST\tAA\tCHARGE\n'.format(THR_DIST))
        for i in distTGT:
            if distTGT[i] <= THR_DIST and PRT[SelCHAIN][i][0][2] in POS_AA:
                print('{}\t{:.3f}\t{}\t+1'.format(i, distTGT[i], PRT[SelCHAIN][i][0][2]))
            elif distTGT[i] <= THR_DIST and PRT[SelCHAIN][i][0][2] in NEG_AA:
                print('{}\t{:.3f}\t{}\t-1'.format(i, distTGT[i], PRT[SelCHAIN][i][0][2]))
            elif distTGT[i] <= THR_DIST:
                print('{}\t{:.3f}\t{}'.format(i, distTGT[i], PRT[SelCHAIN][i][0][2]))
except KeyboardInterrupt:
    print('\n\nClosed by user...bye bye...')
