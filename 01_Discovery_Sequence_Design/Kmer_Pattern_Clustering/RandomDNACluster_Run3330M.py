"""
Created on Wed Apr 12 17:39:23 2023

@author: Yahya Rbn
"""
N=100000000

#100M

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





df6=pd.concat([df3['DNA'],df4['DNA'],df5['DNA']],ignore_index=True).to_frame(name='DNA')
#df.columns = ['DNA']  # Properly naming both columns



filename='RandomDNAtest.csv'

import pandas as pd
from sklearn.cluster import KMeans
N='kmer'
X = df6.iloc[:,0] # DNA column

# Encoding the DNA sequences using motifs encoding
def motif_encode(seq, k=5):
    n = len(seq)
    assert n % k == 0, "DNA sequence length is not a multiple of k"
    subseqs = [seq[i:i+k] for i in range(0, n, k)]
    motif_counts = np.zeros((k, 4))
    for subseq in subseqs:
        for i, nucleotide in enumerate(subseq):
            if nucleotide == 'A':
                motif_counts[i][0] += 1
            elif nucleotide == 'C':
                motif_counts[i][1] += 1
            elif nucleotide == 'G':
                motif_counts[i][2] += 1
            elif nucleotide == 'T':
                motif_counts[i][3] += 1
    return motif_counts / len(subseqs)

# Encode the DNA sequences using motifs encoding
X_input = []
for seq in X:
    X2 = motif_encode(seq)
    X_input.append(X2)
X_input = np.asarray(X_input)

# Using the elbow method to find the optimal number of clusters
wcss = []
for i in range(1, 50):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(X_input.reshape(len(X_input), -1))
    wcss.append(kmeans.inertia_)

# Plotting the elbow plot
plt.plot(range(1, 50), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.savefig('Elbow_Kmeans_motifs10M_{}.png'.format(N), dpi=600, bbox_inches='tight')
plt.show()

# Training the K-Means model on the dataset

kmeans = KMeans(n_clusters=30, init='k-means++', random_state=42)
y_kmeans = kmeans.fit_predict(X_input.reshape(len(X_input), -1))


# Assuming df6 is already loaded and y_kmeans contains the cluster labels
df6['Cluster-kmeans'] = y_kmeans

# Group the data by the cluster number
grouped = df6.groupby('Cluster-kmeans')

# Initialize an empty DataFrame to store the selected DNA sequences
selected = pd.DataFrame(columns=['DNA', 'Cluster-kmeans'])

# Iterate over the clusters and select a random DNA sequence from each one
for cluster, group in grouped:
    sample = group.sample(n=1, random_state=42)
    selected = pd.concat([selected, sample], ignore_index=True)  # Using concat instead of append

# Also save the selected DNA sequences to a CSV file
selected.to_csv('selected_DNA_sequences100M.csv')



