


"""
Created on Tue Mar  5 13:51:34 2024

@author: Yahya Rbn
"""


                            ### Part A: Preprocssenig of the data ###
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

              # Read the dataset##
dataset=pd.read_excel('133DNAfromDiffLeng-Final.xlsx')
X=dataset.iloc[:,1]
#Two output
y=dataset.iloc[:,[3,7]]
y_output=np.asarray(y)


    ## Data Preprocessing ##
# Distribution plot
plt.figure(figsize=(10, 6))
sns.distplot(y['(9,4) Intensity'], label='(9,4) Intensity Change %')
sns.distplot(y['(7,6) Intensity'], label='(7,6) Intensity Change %')
plt.legend()
plt.xlabel('Value')
plt.ylabel('Density')
plt.show()

# classification of the data #Thershold=12
y['Intensity_class94']= y['(9,4) Intensity'].apply(lambda x:1 if x >12 else 0 )
y['Intensity_class76']= y['(7,6) Intensity'].apply(lambda x:1 if x >12 else 0 )
y_output=np.asarray(y)
y_output=y_output[:,2:4]

#Distribution of the data per each class
plt.figure(figsize=(12,8))
sns.histplot(y['Intensity_class94'], label='PL intensity', color='blue')
sns.histplot(y['Intensity_class76'],  label='PL intensity76', color='red')
plt.legend()
plt.show()


## Convert my input DNA sequence to the matrix 
def one_hot_encode(seq, fixed_length=30): # Set the maximum length with fixed length

    mapping = dict(zip("AGCTN", range(5)))  # Add 'N' for padding if the length shorter
    seq = (seq + 'N' * fixed_length)[:fixed_length]
    seq_encoded = [mapping[char] for char in seq]
    return np.eye(5)[seq_encoded]  # One-hot encoding 

X_input = []
for i in X:
    X2 = one_hot_encode(i)
    X_input.append(X2)
X_input = np.array(X_input)
X_input = X_input.reshape(-1, 30, 5, 1) # reshaper to be suitable for CNN input 

print(X_input.shape)
np.info(X_input)

