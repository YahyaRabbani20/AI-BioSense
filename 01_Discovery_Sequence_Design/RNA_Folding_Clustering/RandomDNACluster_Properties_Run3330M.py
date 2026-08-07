"""
Created on Wed Apr 12 17:39:23 2023

@author: Yahya Rbn
"""
N=100000000

#test

                                          ###10L##
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


import random

def random_dna_sequence(length):
    return ''.join(random.choice('ACTG') for _ in range(length))


def base_frequency(dna):
    d = {}
    for base in 'ATCG':
        d[base] = dna.count(base)/float(len(dna))
    return d
DNARAnF=[]
for i in range(N):
    dna = random_dna_sequence(10)
    Out=[dna, base_frequency(dna)]
    DNARAnF.append (Out)
print( DNARAnF[1])


df = pd.DataFrame(DNARAnF, columns=['DNA', 'Frequency'])
#df.to_excel('RandomFr-10000000.xlsx') 
#df.to_csv('Random1.csv') 

# Maximum base frequencies:
max_freq = {'A': {'dna': '', 'freq': 0},
            'T': {'dna': '', 'freq': 0},
            'C': {'dna': '', 'freq': 0},
            'G': {'dna': '', 'freq': 0}}

for dna_freq in DNARAnF:
    dna = dna_freq[0]
    freq_dict = dna_freq[1]
    for base, freq in freq_dict.items():
        if freq > max_freq[base]['freq']:
            max_freq[base]['dna'] = dna
            max_freq[base]['freq'] = freq

print("Maximum base frequencies:")
for base in ['A', 'T', 'C', 'G']:
    print(base + ":", max_freq[base]['freq'], "in DNA sequence", max_freq[base]['dna'])

# Unique DNA
unique_DNA = set()
unique_DNA_RAnF = []

for dna_ranf in DNARAnF:
    dna = dna_ranf[0]
    if dna not in unique_DNA:
        unique_DNA.add(dna)
        unique_DNA_RAnF.append(dna_ranf)

#print(unique_DNA_RAnF[1])
df2 = pd.DataFrame(unique_DNA_RAnF, columns=['DNA', 'Frequency'])

#df2.to_csv('Random1.csv') 

#compare DNA sequences from both ends to check if they are similar and remove one of them
unique_DNA = set()
unique_DNA_RAnF = []

for dna_ranf in DNARAnF:
    dna = dna_ranf[0]
    if dna not in unique_DNA and dna[::-1].translate(str.maketrans('ATCG', 'TAGC')) not in unique_DNA:
        unique_DNA.add(dna)
        unique_DNA_RAnF.append(dna_ranf)

#print(unique_DNA_RAnF[1])
df3 = pd.DataFrame(unique_DNA_RAnF, columns=['DNA', 'Frequency'])
#df3.to_csv('Randomtest1.csv')



                                               ###20L##


import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


import random

def random_dna_sequence(length):
    return ''.join(random.choice('ACTG') for _ in range(length))


def base_frequency(dna):
    d = {}
    for base in 'ATCG':
        d[base] = dna.count(base)/float(len(dna))
    return d
DNARAnF=[]
for i in range(N):
    dna = random_dna_sequence(20)
    Out=[dna, base_frequency(dna)]
    DNARAnF.append (Out)
print( DNARAnF[1])


df = pd.DataFrame(DNARAnF, columns=['DNA', 'Frequency'])
#df.to_excel('RandomFr-10000000.xlsx') 
#df.to_csv('Random1.csv') 

# Maximum base frequencies:
max_freq = {'A': {'dna': '', 'freq': 0},
            'T': {'dna': '', 'freq': 0},
            'C': {'dna': '', 'freq': 0},
            'G': {'dna': '', 'freq': 0}}

for dna_freq in DNARAnF:
    dna = dna_freq[0]
    freq_dict = dna_freq[1]
    for base, freq in freq_dict.items():
        if freq > max_freq[base]['freq']:
            max_freq[base]['dna'] = dna
            max_freq[base]['freq'] = freq

print("Maximum base frequencies:")
for base in ['A', 'T', 'C', 'G']:
    print(base + ":", max_freq[base]['freq'], "in DNA sequence", max_freq[base]['dna'])

# Unique DNA
unique_DNA = set()
unique_DNA_RAnF = []

for dna_ranf in DNARAnF:
    dna = dna_ranf[0]
    if dna not in unique_DNA:
        unique_DNA.add(dna)
        unique_DNA_RAnF.append(dna_ranf)

#print(unique_DNA_RAnF[1])
df2 = pd.DataFrame(unique_DNA_RAnF, columns=['DNA', 'Frequency'])

#df2.to_csv('Random1.csv') 

#compare DNA sequences from both ends to check if they are similar and remove one of them
unique_DNA = set()
unique_DNA_RAnF = []

for dna_ranf in DNARAnF:
    dna = dna_ranf[0]
    if dna not in unique_DNA and dna[::-1].translate(str.maketrans('ATCG', 'TAGC')) not in unique_DNA:
        unique_DNA.add(dna)
        unique_DNA_RAnF.append(dna_ranf)

#print(unique_DNA_RAnF[1])
df4 = pd.DataFrame(unique_DNA_RAnF, columns=['DNA', 'Frequency'])
#df4.to_csv('Randomtest2.csv')


                                                      ###30L##

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


import random

def random_dna_sequence(length):
    return ''.join(random.choice('ACTG') for _ in range(length))


def base_frequency(dna):
    d = {}
    for base in 'ATCG':
        d[base] = dna.count(base)/float(len(dna))
    return d
DNARAnF=[]
for i in range(N):
    dna = random_dna_sequence(30)
    Out=[dna, base_frequency(dna)]
    DNARAnF.append (Out)
print( DNARAnF[1])


df = pd.DataFrame(DNARAnF, columns=['DNA', 'Frequency'])
#df.to_excel('RandomFr-10000000.xlsx') 
#df.to_csv('Random1.csv') 

# Maximum base frequencies:
max_freq = {'A': {'dna': '', 'freq': 0},
            'T': {'dna': '', 'freq': 0},
            'C': {'dna': '', 'freq': 0},
            'G': {'dna': '', 'freq': 0}}

for dna_freq in DNARAnF:
    dna = dna_freq[0]
    freq_dict = dna_freq[1]
    for base, freq in freq_dict.items():
        if freq > max_freq[base]['freq']:
            max_freq[base]['dna'] = dna
            max_freq[base]['freq'] = freq

print("Maximum base frequencies:")
for base in ['A', 'T', 'C', 'G']:
    print(base + ":", max_freq[base]['freq'], "in DNA sequence", max_freq[base]['dna'])

# Unique DNA
unique_DNA = set()
unique_DNA_RAnF = []

for dna_ranf in DNARAnF:
    dna = dna_ranf[0]
    if dna not in unique_DNA:
        unique_DNA.add(dna)
        unique_DNA_RAnF.append(dna_ranf)

#print(unique_DNA_RAnF[1])
df2 = pd.DataFrame(unique_DNA_RAnF, columns=['DNA', 'Frequency'])

#df2.to_csv('Random1.csv') 

#compare DNA sequences from both ends to check if they are similar and remove one of them
unique_DNA = set()
unique_DNA_RAnF = []

for dna_ranf in DNARAnF:
    dna = dna_ranf[0]
    if dna not in unique_DNA and dna[::-1].translate(str.maketrans('ATCG', 'TAGC')) not in unique_DNA:
        unique_DNA.add(dna)
        unique_DNA_RAnF.append(dna_ranf)

#print(unique_DNA_RAnF[1])
df5 = pd.DataFrame(unique_DNA_RAnF, columns=['DNA', 'Frequency'])

#df3.to_csv('RandomDNA1M30lengths.csv') 
#df5.to_csv('Randomtest3.csv')





df=pd.concat([df3['DNA'],df4['DNA'],df5['DNA']],ignore_index=True).to_frame(name='DNA')
#df.columns = ['DNA']  # Properly naming both columns











#part A
# Define nucleotide properties and functions as before

atomic_numbers = {'A': 70, 'G': 78, 'C': 58, 'T': 66}
eiip = {'A': 0.1260, 'G': 0.0806, 'C': 0.1340, 'T': 0.1335}

def calculate_properties(seq):
    atomic_vals = [atomic_numbers[nuc] for nuc in seq]
    eiip_vals = [eiip[nuc] for nuc in seq]
    avg_atomic = sum(atomic_vals) / len(atomic_vals)
    avg_eiip = sum(eiip_vals) / len(eiip_vals)
    return avg_atomic, avg_eiip

# Molecular weights (example values, you should use accurate molecular weights)
mw = {'A': 331.2, 'G': 347.2, 'C': 307.2, 'T': 322.2}

# Function to calculate additional properties
def calculate_more_properties(seq):
    mw_vals = [mw[nuc] for nuc in seq]
    gc_content = (seq.count('G') + seq.count('C')) / len(seq)
    melting_temp = 64.9 + 41 * (gc_content - 0.5) / len(seq)  # Simplified Wallace Rule

    avg_mw = sum(mw_vals) / len(mw_vals)
    return avg_mw, melting_temp

# Function to calculate sequence entropy
def calculate_entropy(seq):
    bases = 'ACGT'
    base_frequencies = {base: seq.count(base) / len(seq) for base in bases if seq.count(base) > 0}
    entropy = -sum(frequency * np.log2(frequency) for frequency in base_frequencies.values())
    return entropy


# def calculate_mfe(seq):
#     # Convert DNA sequence to RNA (replace Thymine with Uracil)
#     rna_seq = seq.replace('T', 'U')
#     # Calculate MFE using ViennaRNA
#     structure, mfe = fold(rna_seq)
    # return mfe
import RNA
def calculate_all_properties(seq):
    # Basic nucleotide properties
    atomic_vals = [atomic_numbers[nuc] for nuc in seq]
    eiip_vals = [eiip[nuc] for nuc in seq]
    mw_vals = [mw[nuc] for nuc in seq]
    gc_content = (seq.count('G') + seq.count('C')) / len(seq)
    melting_temp = 64.9 + 41 * (gc_content - 0.5) / len(seq)
    seq_length = len(seq)
    seq_entropy = calculate_entropy(seq)
    
    # Convert DNA to RNA
    rna_seq = seq.replace('T', 'U')

    # Calculate ViennaRNA properties
    # Minimum Free Energy and structure
    mfe_structure, mfe = RNA.fold(rna_seq)
    
    # Ensemble Free Energy and partition function
    fc = RNA.fold_compound(rna_seq)
    ensemble_energy = fc.pf()  # This should only return the free energy as a float

    # Ensure only the numerical part of the ensemble energy is returned
    # If ensemble_energy is not just a float, extract the float part
    if isinstance(ensemble_energy, list):
        # Assuming the energy is the second element in a list
        ensemble_energy = ensemble_energy[1]  # adjust index based on actual structure

    # Centroid structure
    centroid_structure, centroid_distance = fc.centroid()

    # Get base pairing probability matrix
    bpp_matrix = fc.bpp()  # Base Pairing Probabilities matrix
    paired_probs = sum(bpp_matrix[i][j] for i in range(len(rna_seq)) for j in range(len(rna_seq)) if i < j)

    avg_atomic = sum(atomic_vals) / len(atomic_vals)
    avg_eiip = sum(eiip_vals) / len(eiip_vals)
    avg_mw = sum(mw_vals) / len(mw_vals)
    
    return avg_atomic, avg_eiip, avg_mw, melting_temp, seq_length, seq_entropy, mfe, ensemble_energy, centroid_structure, paired_probs

# Application to DataFrame
df['Avg_Atomic_Number'], df['Avg_EIIP'], df['Avg_Molecular_Weight'], df['Melting_Temp'], \
df['Seq_Length'], df['Seq_Entropy'], df['Seq_MFE'], df['Ensemble_Energy'], \
df['Centroid_Structure'], df['Paired_Probs'] = zip(*df['DNA'].apply(calculate_all_properties))


# Update clustering
# Clustering with updated features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
features = df[['Avg_Atomic_Number', 'Avg_EIIP', 'Avg_Molecular_Weight', 'Melting_Temp', 'Seq_Length', 'Seq_Entropy', 'Seq_MFE', 'Ensemble_Energy', 'Paired_Probs']]
scaled_features = scaler.fit_transform(features)

# kmeans = KMeans(n_clusters=3)
# df['Cluster'] = kmeans.fit_predict(scaled_features)

# df.to_excel('processed_sequences_with_All_properties plus RNA folding.xlsx')



import pandas as pd
from sklearn.cluster import KMeans






# ## Using the elbow method to find the optimal number of clusters
wcss = []
for i in range(1, 100):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
    kmeans.fit(scaled_features)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 100), wcss)
# plt.axvline(x=20, color='r', linestyle='--') # Add a vertical line at the elbow point
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.savefig('Elbow_Kmeans-oneHotencoding_properties100M.png', dpi=300, bbox_inches='tight') # save the plot with 300 dpi resolution and tight bounding box
plt.show()

### Training the K-Means model on the dataset
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters = 20, init = 'k-means++', random_state = 42)
y_kmeans = kmeans.fit_predict(scaled_features)
## export the result to the next cloumn in excell file
import pandas as pd

# Assuming df is your DataFrame after processing and y_kmeans are the cluster labels
df['Cluster-kmeans'] = y_kmeans

# Group the data by the cluster number directly in the df DataFrame
grouped = df.groupby('Cluster-kmeans')

# Initialize an empty DataFrame to store the selected DNA sequences and their properties
selected = pd.DataFrame()

# Iterate over the clusters and select a random DNA sequence from each one
for cluster, group in grouped:
    sample = group.sample(n=1, random_state=42)
    selected = pd.concat([selected, sample], ignore_index=True)

# Save the selected DNA sequences and their properties to an Excel file
with pd.ExcelWriter('Selected_DNA_Cluster_Properties_100M.xlsx', engine='openpyxl') as writer:
    selected.to_excel(writer, index=False)


