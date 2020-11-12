"""General parser for QM softwares"""


class AMS:
    """Parser for Amsterdam Density Functional/Amsterdam Modeling Suite"""
    def __init__(self, path):
        self.version = ""
        self.ene = []
        self.enechg = []
        self.grdmax = []
        self.grdrms = []
        self.stpmax = []
        self.stprms = []
        self.eigen = []

        with open(path) as file:
            lines = file.readlines()

        for idx, val in enumerate(lines):
            if ('*   Amsterdam Density Functional  (ADF)' in val or 'Amsterdam Modeling Suite (AMS)' in val) and self.version == '':
                self.version = val.split()[5]

            if 'Geometry Convergence after Step' in val:
                self.ene.append(float(lines[idx+2].split()[2]))
                self.enechg.append(abs(float(lines[idx+3].split()[2])))
                self.enelim = float(lines[idx+3].split()[3])

                self.grdmax.append(float(lines[idx+4].split()[3]))
                self.grdmaxlim = float(lines[idx+4].split()[4])
                self.grdrms.append(float(lines[idx+5].split()[3]))
                self.grdrmslim = float(lines[idx+5].split()[4])

                self.stpmax.append(float(lines[idx+8].split()[3]))
                self.stpmaxlim = float(lines[idx+8].split()[4])
                self.stprms.append(float(lines[idx+9].split()[3]))
                self.stprmslim = float(lines[idx+9].split()[4])

        self.enechg[0] = None


class ORCA:
    """Parser for ORCA"""
    def __init__(self, path):
        self.version = ""
        self.ene = []
        self.enechg = []
        self.grdmax = []
        self.grdrms = []
        self.stpmax = []
        self.stprms = []
        self.eigen = [[], [], [], [], []]

        with open(path) as file:
            lines = file.readlines()

        for idx, val in enumerate(lines):
            if '* O   R   C   A *' in val and self.version == '':
                self.version = lines[idx+19].split()[2]

            elif 'FINAL SINGLE POINT ENERGY' in val:
                self.ene.append(float(val.split()[4]))

            elif '          Energy change' in val:
                self.enechg.append(abs(float(val.split()[2])))
                self.enelim = float(val.split()[3])
            elif '          MAX gradient' in val:
                self.grdmax.append(float(val.split()[2]))
                self.grdmaxlim = float(val.split()[3])
            elif '          RMS gradient' in val:
                self.grdrms.append(float(val.split()[2]))
                self.grdrmslim = float(val.split()[3])
            elif '          MAX step' in val:
                self.stpmax.append(float(val.split()[2]))
                self.stpmaxlim = float(val.split()[3])
            elif '          RMS step' in val:
                self.stprms.append(float(val.split()[2]))
                self.stprmslim = float(val.split()[3])
            elif 'Lowest eigenvalues of augmented Hessian:' in val:
                self.eigen[0].append(float(lines[idx+1].split()[0]))
                self.eigen[1].append(float(lines[idx+1].split()[1]))
                self.eigen[2].append(float(lines[idx+1].split()[2]))
                self.eigen[3].append(float(lines[idx+1].split()[3]))
                self.eigen[4].append(float(lines[idx+1].split()[4]))

        self.enechg.insert(0, None)


class G16:
    """Parser for G16"""
    def __init__(self, path):
        self.version = ""
        self.ene = []
        self.enelim = ''
        self.enechg = []
        self.grdmax = []
        self.grdrms = []
        self.stpmax = []
        self.stprms = []
        self.eigen = [[], [], [], [], []]

        with open(path) as file:
            lines = file.readlines()

        for idx, val in enumerate(lines):
            if ' Gaussian 16,' in val and self.version == '':
                self.version = lines[idx].split()[3].replace(',','')
                print(self.version)
            elif ' SCF Done:' in val:
                self.ene.append(float(val.split()[4]))
            elif '         Item               Value     Threshold  Converged' in val:
                self.grdmax.append(float(lines[idx+1].split()[2]))
                self.grdmaxlim = float(lines[idx+1].split()[3])
                self.grdrms.append(float(lines[idx+2].split()[2]))
                self.grdrmslim = float(lines[idx+2].split()[3])
                self.stpmax.append(float(lines[idx+3].split()[2]))
                self.stpmaxlim = float(lines[idx+3].split()[3])
                self.stprms.append(float(lines[idx+4].split()[2]))
                self.stprmslim = float(lines[idx+4].split()[3])
            elif '     Eigenvalues ---' in val and len(self.eigen[0]) != len(self.ene):
                self.eigen[0].append(float(val.split()[2]))
                self.eigen[1].append(float(val.split()[3]))
                self.eigen[2].append(float(val.split()[4]))
                self.eigen[3].append(float(val.split()[5]))
                self.eigen[4].append(float(val.split()[6]))

        self.enechg = [self.ene[idx]-self.ene[idx-1] for idx, val in enumerate(self.ene)]
        self.enechg[0] = None
