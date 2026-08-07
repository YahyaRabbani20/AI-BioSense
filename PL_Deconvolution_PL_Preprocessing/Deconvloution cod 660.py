# ---------------  660 ---------------------#
# ---------------  including module ---------------------#
import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

# functions
def lor(x, p):
    numerator = (p[0] / 2)
    denominator = ( x - (p[1]) )**2 + (p[0] / 2)**2
    y = (p[0]*p[2]/2)*(numerator/denominator)
    return y

def mP(p, y, x):
    n = int(len(p) / 3)
    fit = 0
    for i in range(n):
        fit = fit + lor(x, p[3*i:3*i+3])
    err = y - fit
    return err



# Initialization
# Directory where csv files are located
#directory = "C:\\Users\yahya\Desktop\PL response 05.05.2023"

dataM = np.genfromtxt('ReversibilityBeforeFiltrationafter660.csv', delimiter=',')
wl = np.genfromtxt('x1150Wide.csv', delimiter=',')

sampleN = dataM.shape[1]                 # Number of spectrums to fit
n_peaks = 8                               # Number of peaks
PeakSummary = np.zeros([n_peaks*3,sampleN])  # 3 for three parameters
MaxData = np.amax(dataM)                     # Largest data as upper bound
# Deconvolution, code from fiting
p = [20, 975, 1,
     20, 1000, 1,
     10, 1050, 1,
     20, 1090, 1,
     20, 1150, 1,
     20, 1200, 1,
     20, 1292, 1,
     20, 1320, 1]        # Initial guess parameters, [fwhm, wl, intensity]
lb =[0, 955, 0,
     0, 985, 0,
     0, 1030, 0,
     0, 1070, 0,
     0, 1120, 0,
     0, 1180, 0,
     0, 1260, 0,
     0, 1300, 0]        # Lower bound
ub =[40, 1000, MaxData,
     40, 1019, MaxData,
     40, 1070, MaxData,
     40, 1100, MaxData,
     60, 1180, MaxData,
     40, 1220, MaxData,
     40, 1305, MaxData,
     40, 1350, MaxData]   # Upper bound MaxData


# Reshape bound condition
bound = np.zeros(shape=[2,n_peaks*3])
bound[0,:]= lb
bound[1,:]= ub

# -------------------------------------------------------#

for i in range(0,sampleN,1):
    # dataM[:,i] = normalize(dataM[:,i])  # Normalized line was removed at the moment
    # shift the baseline to zero based on the intensity below cutoff (<927 nm, 100th point)
    # dataM[:, i] = dataM[:, i] - np.amin(dataM[0:10, i])
    pbest = least_squares(mP, p, bounds=bound, args=(dataM[:, i], wl[:]))
    best_parameters = pbest.x
    PeakSummary[:, i] = best_parameters
    p = best_parameters           # set the next initial value to be the solution of the present step
    # Right now the normalization is removed. If put it back,
    # then the intensity should multiply back the maximum (only the intensity cells) with: np.amax(v)

np.savetxt('ReversibilityBeforeFiltrationafter660 dec.csv', PeakSummary, delimiter=',')          # Saving peak as csv
# -------------------------------------------------------#
# for checking plot, the last frame

fit = list(range(n_peaks))
for i in range(n_peaks):
    fit[i] = lor(wl, p[3*i:3*i+3])

accumulative = np.zeros_like(fit[0])
for fitp in fit:
    plt.plot(wl, fitp, 'r-', lw = 2)   # individual peaks as red
    accumulative = np.add(accumulative, np.array(fitp))

for i in range(n_peaks):               # residual as green
    plt.plot(wl,dataM[:,sampleN-1]- accumulative, 'g-', lw = 2)

plt.plot(wl,dataM[:,sampleN-1],'k-')        # original spectrum as black dot
plt.plot(wl,accumulative,'b-')              # simulated combined spectrum as blue line
plt.axhline(0,c='k',lw = 1)
plt.xlabel('Wavelength (nm)')
plt.ylabel('PL intensity (a.u.)')

plt.show()


