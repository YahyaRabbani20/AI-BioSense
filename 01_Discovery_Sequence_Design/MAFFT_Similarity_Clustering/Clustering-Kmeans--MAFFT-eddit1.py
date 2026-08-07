# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 11:33:55 2023

@author: LABO
"""

from Bio.Align.Applications import MafftCommandline
from Bio import SeqIO, AlignIO
import os
import pandas as pd
from io import StringIO
from Bio.Seq import Seq
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
# Read the Excel file containing DNA sequences
df =pd.read_csv('Selected_DNA_Cluster_Properties.csv',delimiter=None)

# Convert the DNA sequences to a list of Seq objects
seq_list = [Seq(seq) for seq in df['DNA'].tolist()]

# Write the sequences to a temporary FASTA file
with open('temp.fasta', 'w') as f:
    for i, seq in enumerate(seq_list):
        f.write(f'>seq{i}\n{seq}\n')

# Perform multiple sequence alignment using MAFFT
mafft_cline = MafftCommandline(input='temp.fasta', auto=True)
stdout, stderr = mafft_cline()

# Parse the resulting alignment and print it to the console
alignment = AlignIO.read(StringIO(stdout), 'fasta')
print(alignment)

# Calculate similarity index for each sequence compared to all other sequences
similarity_indices = []
for i, seq1 in enumerate(seq_list):
    sim_index = 0
    for j, seq2 in enumerate(seq_list):
        if i == j:
            continue
        for a, b in zip(seq1, seq2):
            if a == b:
                sim_index += 1
        sim_index /= max(len(seq1), len(seq2))
    similarity_indices.append(sim_index)

# Calculate the within-cluster sum of squares for different number of clusters
X = [[sim_index] for sim_index in similarity_indices]
wcss = []
for i in range(1, 50):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

# Plot the elbow curve
plt.plot(range(1, 50), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.savefig('Elbow_Kmeans_MAFFT50k1024.png', dpi=300, bbox_inches='tight')
plt.show()


# Cluster the similarity indices using KMeans with 3 clusters
kmeans = KMeans(n_clusters=10, init='k-means++', random_state=0).fit(X)
labels = kmeans.labels_

### Training the K-Means model on the dataset
#kmeans = KMeans(n_clusters = 10, init = 'k-means++', random_state = 42)
y_kmeans = kmeans.fit_predict(X)
## export the result to the next cloumn in excell file
df = pd.DataFrame(df['DNA'])
df['Cluster-kmeans'] = y_kmeans
df.to_excel('Length library Maftt50k1024.xlsx', index=False)

### Group the cluster and select the random from each cluster
# Load the data from the Excel file
dataset = pd.read_excel('Length library Maftt50k1024.xlsx')
# Group the data by the cluster number
grouped = dataset.groupby('Cluster-kmeans')
# Initialize an empty DataFrame to store the selected DNA sequences
selected = pd.DataFrame(columns=['DNA', 'Cluster-kmeans'])
# Iterate over the clusters and select a random DNA sequence from each one
for cluster, group in grouped:
    sample = group.sample(n=1, random_state=42)
    selected = selected.append(sample)
# Save the selected DNA sequences to Sheet 2 of the Excel file
with pd.ExcelWriter('Length library Maftt50k1024.xlsx', engine='openpyxl', mode='a') as writer:
    selected.to_excel(writer, sheet_name='Sheet 2', index=False)




# Plot the similarity indices with different colors for each cluster
colors = ['r', 'g', 'b', 'y', 'c', 'm','r', 'g', 'b', 'y']
for i, sim_index in enumerate(similarity_indices):
    plt.scatter(i, sim_index, color=colors[labels[i]])
plt.xlabel('Sequence Index')
plt.ylabel('Similarity Index')
plt.savefig('Kmeans_MAFFT50k1024.png', dpi=300, bbox_inches='tight')

plt.show()

# Delete the temporary file
os.remove('temp.fasta')

