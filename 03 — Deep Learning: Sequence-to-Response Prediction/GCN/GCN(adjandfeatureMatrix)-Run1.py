
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 13:57:33 2024

@author: yahya
"""


                            ### Part A: Preprocssenig of the data ###
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

              # Read the dataset##
dataset=pd.read_excel('GlucoseDataTest.xlsx')
X=dataset.iloc[:,0]
#One output
y=dataset['(9,4) Intensity']
#dataset['class']
y_output=np.asarray(y)
#two Output
#y=dataset.iloc[:,[5,7]]
#y_output=np.asarray(y)

# preprocessing

plt.figure(figsize=(10, 6))
sns.distplot(dataset['(9,4) Intensity'], label='PL intensity')
#sns.distplot(y['Quenching'], label='Quenching')
plt.legend()
plt.xlabel('Value')
plt.ylabel('Density')
plt.show()

# classification of the data

y_cls= y.apply(lambda x:1 if x >20 else 0 )
#y['Quenching_class']= y['Quenching'].apply(lambda x:1 if x >78 else 0 )
y_output=np.asarray(y_cls)
#y_output=y_output[:,2:4]

#sns.scatterplot(x=np.arange(len(y)), y='Intensity_class', data=y, hue='Quenching_class', palette='flare',edgecolor=None,alpha=0.6)

plt.figure(figsize=(12,8))
sns.histplot(y_cls, kde=True, label='PL intensity', color='blue')
#sns.histplot(y['Quenching_class'], kde=True, label='Quenching', color='red')
plt.legend()
plt.show()



import numpy as np
import networkx as nx

def one_hot_encode_kmer(kmer):
    mapping = {'A': [1, 0, 0, 0], 'C': [0, 1, 0, 0], 'G': [0, 0, 1, 0], 'T': [0, 0, 0, 1]}
    return np.array([mapping[char] for char in kmer]).flatten()

def create_kmer_graph_and_features(sequence, k):
    """
    Converts a DNA sequence into a graph of k-mers, along with node features suitable for GCNs.
    """
    sequence = str(sequence)  # Ensure the sequence is a string

    if len(sequence) < k:
        print("Sequence too short to form any k-mers.")
        return None, None

    # Generate k-mers
    kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Map k-mers to integer indices
    kmer_to_index = {kmer: idx for idx, kmer in enumerate(set(kmers))}
    
    # Add nodes with integer indices
    G.add_nodes_from(kmer_to_index.values())

    # Add edges with integer indices
    for i in range(len(kmers) - 1):
        if kmers[i][1:] == kmers[i+1][:-1]:
            G.add_edge(kmer_to_index[kmers[i]], kmer_to_index[kmers[i+1]])

    # Check for empty graph
    if G.number_of_nodes() == 0 or G.number_of_edges() == 0:
        return None, None

    # Create adjacency matrix and feature matrix
    A = nx.adjacency_matrix(G)
    features = np.array([one_hot_encode_kmer(kmer) for kmer in kmer_to_index.keys()])

    return A, features

# Assuming X is your list of DNA sequences
k = 3
adj_matrices = []  # List to store adjacency matrices
feature_matrices = []  # List to store feature matrices

for sequence in X:
    adjacency_matrix, feature_matrix = create_kmer_graph_and_features(sequence, k)
    if adjacency_matrix is not None and feature_matrix is not None:
        adj_matrices.append(adjacency_matrix)
        feature_matrices.append(feature_matrix)
    else:
        print("Failed to create graph for sequence:", sequence)

print(type(X[0]))  # Check the type of the first item in X
print(X[0])  # Print the first item to understand its format
print(adj_matrices[0])  # Print the first item to understand its format
print(feature_matrices[0])  # Print the first item to understand its format



import numpy as np
import tensorflow as tf
from spektral.data import Graph, Dataset, BatchLoader
from spektral.layers import GCNConv
from spektral.models import GeneralGNN



# Create a custom Spektral Dataset
class MyDataset(Dataset):
    def read(self):
        graphs = []
        for adj, features in zip(adj_matrices, feature_matrices):
            graph = Graph(x=features, a=adj)
            graphs.append(graph)
        return graphs

dataset = MyDataset()

# Create a loader
loader = BatchLoader(dataset, batch_size=2, shuffle=True)

# Define the GCN model
class MyGCN(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.conv1 = GCNConv(32, activation='relu')
        self.conv2 = GCNConv(32, activation='relu')
        self.dense = tf.keras.layers.Dense(1, activation='sigmoid')  # Assuming binary classification

    def call(self, inputs):
        x, a = inputs
        x = self.conv1([x, a])
        x = self.conv2([x, a])
        return self.dense(tf.reduce_mean(x, axis=0, keepdims=True))

model = MyGCN()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Prepare labels for training
y = np.array(y_output)  # Ensure labels are in NumPy array

# Train the model
for epoch in range(10):  # Training for 10 epochs
    for batch in loader:
        x, a = batch
        batch_y = y[:x.shape[0]]  # Adjust the labels batch
        model.fit((x, a), batch_y, epochs=1, batch_size=2, verbose=1)

# Print the model summary
model.summary()