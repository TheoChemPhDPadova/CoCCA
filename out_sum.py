"""TO-BE-FIXED"""
import sys, os
import matplotlib.pyplot as plt
import fileinput

def main(input):
	plt.rc('font', family='serif')
	tmp=[]
	E=[]
	EC=[]
	EClim=[]
	Rg=[]
	Rglim=[]
	Mg=[]
	Mglim=[]
	Rs=[]
	Rslim=[]
	Ms=[]
	Mslim=[]
	eigen=0
	counter=1
	Eigen1=[]
	Eigen2=[]
	Eigen3=[]
	Eigen4=[]
	Eigen5=[]

	for line in fileinput.input():
		if "Geometry Convergence after Step" in line:
			version="ADFnew"
			break
		if " Geometry Convergence Tests" in line:
			version="ADFold"
			break
		if "FINAL SINGLE POINT ENERGY" in line:
			version="ORCA"
			break
		if "Predicted change in Energy" in line:
			version="G16"
			break

	fileinput.close()

	if version=="ADFnew":
		for line in fileinput.input():
			if "current energy" in line:
				tmp=line.split()
				E.append(float(tmp[2]))
			if "energy change" in line:
				tmp=line.split()
				EC.append(asb(float(tmp[2])))
				EClim.append(float(tmp[3]))
			if "constrained gradient rms" in line:
				tmp=line.split()
				Rg.append(float(tmp[3]))
				Rglim.append(float(tmp[4]))
			if "constrained gradient max" in line:
				tmp=line.split()
				Mg.append(float(tmp[3]))
				Mglim.append(float(tmp[4]))
			if "cart. step rms" in line:
				tmp=line.split()
				Rs.append(float(tmp[3]))
				Rslim.append(float(tmp[4]))
			if "cart. step max" in line:
				tmp=line.split()
				Ms.append(float(tmp[3]))
				Mslim.append(float(tmp[4]))
		fig = plt.figure() 
		fig.canvas.set_window_title('ADF (New Version)')
		EC[0]=None

	if version=="ADFold":
		for line in fileinput.input():
			if "         new :" in line:
				tmp=line.split()
				E.append(float(tmp[2]))
			if "change in energy" in line:
				tmp=line.split()
				EC.append(abs(float(tmp[3])))
				EClim.append(float(tmp[4]))
			if "gradient rms" in line:
				tmp=line.split()
				Rg.append(float(tmp[2]))
				Rglim.append(float(tmp[3]))
			if "gradient max" in line:
				tmp=line.split()
				Mg.append(float(tmp[2]))
				Mglim.append(float(tmp[3]))
			if "cart. step rms" in line:
				tmp=line.split()
				Rs.append(float(tmp[3]))
				Rslim.append(float(tmp[4]))
			if "cart. step max" in line:
				tmp=line.split()
				Ms.append(float(tmp[3]))
				Mslim.append(float(tmp[4]))
		fig = plt.figure() 
		fig.canvas.set_window_title('ADF (Old Version)')
		EC[0]=None
		
	if version=="ORCA":
		for line in fileinput.input():
			if "FINAL SINGLE POINT ENERGY" in line:
				tmp=line.split()
				E.append(float(tmp[4]))
			if "          Energy change" in line:
				tmp=line.split()
				EC.append(abs(float(tmp[2])))
				EClim.append(float(tmp[3]))
			if "          RMS gradient" in line:
				tmp=line.split()
				Rg.append(float(tmp[2]))
				Rglim.append(float(tmp[3]))
			if "          MAX gradient" in line:
				tmp=line.split()
				Mg.append(float(tmp[2]))
				Mglim.append(float(tmp[3]))
			if "          RMS step" in line:
				tmp=line.split()
				Rs.append(float(tmp[2]))
				Rslim.append(float(tmp[3]))
			if "          MAX step" in line:
				tmp=line.split()
				Ms.append(float(tmp[2]))
				Mslim.append(float(tmp[3]))
			if eigen==1:
				tmp=line.split()
				Eigen1.append(float(tmp[0]))
				Eigen2.append(float(tmp[1]))
				Eigen3.append(float(tmp[2]))
				Eigen4.append(float(tmp[3]))
				Eigen5.append(float(tmp[4]))
				print(str(counter) + '   ' + str(line.strip()))
				counter=counter+1
				eigen=0
			if "Lowest eigenvalues" in line:
				eigen=1


		fig = plt.figure() 
		fig.canvas.set_window_title('ORCA')
		EC.insert(0, None)
		EClim.insert(0, EClim[1])
		del E[-1]

	if version=="G16":
		for line in fileinput.input():
			if "SCF Done:" in line:
				tmp=line.split()
				E.append(float(tmp[4]))
			if "RMS     Force" in line:
				tmp=line.split()
				Rg.append(float(tmp[2]))
				Rglim.append(float(tmp[3]))
			if "Maximum Force" in line:
				tmp=line.split()
				Mg.append(float(tmp[2]))
				Mglim.append(float(tmp[3]))
			if "RMS     Displacement" in line:
				tmp=line.split()
				Rs.append(float(tmp[2]))
				Rslim.append(float(tmp[3]))
			if "Maximum Displacement" in line:
				tmp=line.split()
				Ms.append(float(tmp[2]))
				Mslim.append(float(tmp[3]))
			if "Eigenvalues ---   -" in line:
				tmp=line.split()
				Eigen1.append(float(tmp[2]))
				Eigen2.append(float(tmp[3]))
				Eigen3.append(float(tmp[4]))
				Eigen4.append(float(tmp[5]))
				Eigen5.append(float(tmp[6]))
				print(str(counter) + ':   ' + line.strip())
				counter=counter+1
		fig = plt.figure() 
		fig.canvas.set_window_title('Gaussian 16 (G16)')
		for idx, val in enumerate(E):
			EC.append(abs(val-E[idx-1]))
		EC[0]=None

	ax1=plt.subplot(331)
	plt.plot (E, marker=".", markersize=7, lw=1)
	plt.ylabel('Hartree')
	plt.title("Energy")
	plt.xlim(0, len(E)-1)

	plt.subplot(332)
	plt.plot(EC, marker=".", markersize=7, lw=1)
	plt.plot (EClim,'r--')
	plt.ylabel('Hartree')
	plt.title("|Energy Change|")
	plt.xlim(0, len(E)-1)

	plt.subplot(333)
	plt.plot (Rg, marker=".", markersize=7, lw=1)
	plt.plot (Rglim,'r--')
	plt.ylabel('Hartree')
	if version=="G16":
		plt.title("RMS Force")
	else:
		plt.title("RMS gradient")
	plt.xlim(0, len(E)-1)

	plt.subplot(334)
	plt.plot (Mg, marker=".", markersize=7, lw=1)
	plt.plot (Mglim,'r--')
	plt.ylabel('Hartree')
	if version=="G16":
		plt.title("MAX Force")
	else:
		plt.title("MAX gradient")
	plt.xlim(0, len(E)-1)

	plt.subplot(335)
	plt.plot (Rs, marker=".", markersize=7, lw=1)
	plt.plot (Rslim,'r--')
	plt.ylabel('Hartree')
	plt.title("RMS step displacement")
	plt.xlim(0, len(E)-1)

	plt.subplot(336)
	plt.plot (Ms, marker=".", markersize=7, lw=1)
	plt.plot (Mslim,'r--')
	plt.ylabel('Hartree')
	plt.title("MAX step displacement")
	plt.xlim(0, len(E)-1)

	plt.subplot(337)
	plt.plot (Eigen1, marker=".", markersize=7, lw=2)
	plt.plot (Eigen2, marker=".", markersize=7, lw=1)
	plt.plot (Eigen3, marker=".", markersize=7, lw=1)
	plt.plot (Eigen4, marker=".", markersize=7, lw=1)
	plt.plot (Eigen5, marker=".", markersize=7, lw=1)
	plt.title("Hessian Eigenvector")
	plt.xlim(0, len(E)-1)


	#plt.tight_layout()
	mng = plt.get_current_fig_manager()
	mng.full_screen_toggle()
	plt.show()

if __name__ == "__main__":
    try:
        main(input)
    except KeyboardInterrupt:
        print("Interrupted by user")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)