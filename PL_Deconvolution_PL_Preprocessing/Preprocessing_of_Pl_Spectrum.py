
"""
Created on Thu Feb 16 12:27:10 2023
@author: Yahya Rbn
"""

import os
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from matplotlib import pyplot as plt


                             
                             ## LOADING THE DATA AND SAVE AS AN MATRIX ##
#The user for the directory and filename
directory = input("Enter the directory where the files are located: ")
filename = input("Enter the filename to search for (WithoutNumber): ")
time_point=int(input("Enter the time point: "))
sample_number=int(input("Enter the number of samples: "))
Replicate_number=int(input("Enter the number of replicate: "))
Analyte_number=int(input("Enter the number of analyte: "))

# Check if the directory exists
if not os.path.exists(directory):
    print(f"The directory {directory} does not exist.")
else:
    # Get a list of all csv files in the directory that match the filename
    files = [f for f in os.listdir(directory) if f.endswith('.csv') and f.startswith(filename)]


# Sort the files based on their numerical order
files = sorted(files, key=lambda f: int(f.split(' ')[-1].split('.')[0]))

# Microscope mesuerment information 
#Number of frames for each wavelength :
frameN = 1
#  excitation wavelength
#ex1=660 and ex2=730  by Step size of  80

# Dimensions of sensor
sensorX = 512 
sensorY = 640 # wavelenght

M = np.zeros((len(files), frameN*(sensorX + 1), sensorY))

# Read in csv files and store in Matrix (M)
for i, f in enumerate(files):
    M[i,:,:] = np.loadtxt(os.path.join(directory, f), delimiter=",")


x = M[0, 0, :]  # x-axis

AVG = np.zeros((len(files), len(M[0, 0, :])))

for i in range(len(files)):
    for j in range(len(M[i, 0, :])):
        for k in range(frameN):
            AVG[i,j] = (np.sum(M[i,:,j]) - frameN * x[j])  # should divide by power

np.savetxt(filename+".csv", AVG.T, delimiter=",")  # output a report w/ Filename, NOTE transpose

                          ## Remove the Background (blanck)##
# # Read in data
M = np.loadtxt(filename+".csv", delimiter=",")
# # # Separate even and odd indices to 660 and 730
M[:, 0::2] = M[:, 0::2]-M[:, -2].reshape((-1, 1))
# # # Delete the second last column of M
M[:, 1::2] = M[:, 1::2]-M[:, -1].reshape((-1, 1))
# # # Delete the last and second last columns of M of each time point

s=sample_number
r=Replicate_number
A=Analyte_number
t=time_point
c=0
cloumn_blank = []  # Initialize as an empty list
for i in range(t):
    cloumn_index= ((i+1)*r*s*A*2)+c+i  
    cloumn_blank.append(cloumn_index)
    cloumn_index=cloumn_index+1
    cloumn_blank.append(cloumn_index)
    c+=1

M = np.delete(M, cloumn_blank, axis=1)
                                    ## SMOOTHING PROCESS with Savitzky-Golay filter parameters ###
order = 4 # polynomial order of fitting
framelen = 31 # The length of the filter window for each step of fitting
## note :  polyorder must be less than window_length
# Apply filter
sgf = savgol_filter(M, window_length=framelen, polyorder=order, axis=0)

I = np.zeros((M.shape[0], M.shape[1]))

for i in range(M.shape[1]):
    I[:, i] = sgf[:, i] - np.mean(sgf[:50, i], axis=0)

# Write out smoothed data
np.savetxt(str(filename)+"after.csv", I, delimiter=",")

even660 = I[:, 0::2]
odd730 = I[:, 1::2]
# Write out even and odd data to separate files
np.savetxt(str(filename)+"after660.csv", even660, delimiter=",")
np.savetxt(str(filename)+"after730.csv", odd730, delimiter=",")
            ## visulation all spectrum ##
wl = np.genfromtxt('x1150Wide.csv', delimiter=',')
#Plot even dataset
plt.figure()
plt.plot(wl, even660)
plt.xlabel('Wavelength (nm)')
plt.ylabel('PL intensity (a.u.)')
plt.title('660')
plt.savefig('after-660.png', dpi=300, bbox_inches='tight')

#plt.plot(wl, even660[:,03])
# Plot odd dataset
plt.figure()
plt.plot(wl, odd730)
plt.xlabel('Wavelength (nm)')
plt.ylabel('PL intensity (a.u.)')
plt.title('730')
plt.savefig('after-730.png', dpi=300, bbox_inches='tight')
# Show the plots
plt.show()

print("Files were saved in the same directory")

# Calculate area under the curve for each even660 and odd730 spectrum
auc = np.zeros((I.shape[0], 2))
for i in range(I.shape[0]):
    auc[i, 0] = np.trapz(I[i, 0::2], x=wl)
    auc[i, 1] = np.trapz(I[i, 1::2], x=wl)

 # Output area under the curve results to excel file
df = pd.DataFrame(auc, columns=['even660_AUC', 'odd730_AUC'])
df.to_excel('AUC_results.xlsx', index=False)

print("AUC calculation completed and results saved to 'AUC_results.xlsx'")
