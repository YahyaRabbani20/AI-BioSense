
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


##Adjacency matrix
# import networkx as nx

# def dna_to_kmer_graph_adjacency(sequence, k):
#     """
#     Converts a DNA sequence to a directed graph based on k-mers and returns the adjacency matrix.
    
#     Parameters:
#         sequence (str): The DNA sequence.
#         k (int): The size of each k-mer.

#     Returns:
#         np.array: Adjacency matrix of the graph.
#     """
#     # Generate k-mers
#     kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]

#     # Create a directed graph
#     G = nx.DiGraph()

#     # Add nodes (each unique k-mer)
#     G.add_nodes_from(kmers)

#     # Add edges
#     for i in range(len(kmers) - 1):
#         if kmers[i][1:] == kmers[i+1][:-1]:
#             G.add_edge(kmers[i], kmers[i+1])

#     # Generate adjacency matrix
#     adjacency_matrix = nx.adjacency_matrix(G).todense()

#     return adjacency_matrix

# # Example usage
# # dna_sequence = "AGCTGACTTGGTC"
# # k = 3
# # adj_matrix = dna_to_kmer_graph_adjacency(dna_sequence, k)
# # print("Adjacency Matrix:\n", adj_matrix)
# ##
# k=3
# X_input=[]
# for i in X:
#     X2=dna_to_kmer_graph_adjacency(i,k)
#     X_input.append(X2)

# #print(X_input)
# X_input=np.asarray(X_input)
# #np.info(X_input)
# print(X_input[0])
# np.info(X_input[0])



#Graph2Vec
import networkx as nx
from karateclub import Graph2Vec

import networkx as nx
from karateclub import Graph2Vec

def dna_to_graph2vec_embedding(sequence, k):
    """
    Converts a DNA sequence to a graph based on k-mers and returns a graph embedding using Graph2Vec,
    ensuring the graph is properly indexed with consecutive integers.
    
    Parameters:
        sequence (str): The DNA sequence.
        k (int): The size of each k-mer.

    Returns:
        list: A list containing the embedding vector of the graph, or None if no graph can be constructed.
    """
    if len(sequence) < k:
        print("Sequence too short to form any k-mers.")
        return None

    # Generate k-mers
    kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Check for no possible k-mers
    if not kmers:
        print("No k-mers generated.")
        return None
    
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
        print("Graph is empty or improperly constructed.")
        return None

    # Initialize and fit Graph2Vec
    try:
        model = Graph2Vec(dimensions=64, workers=2)
        model.fit([G])
    except Exception as e:
        print("Error during model fitting:", str(e))
        return None

    # Get the embedding
    embedding = model.get_embedding()[0] if G.number_of_nodes() > 0 else None
    
    return embedding


# Example usage
dna_sequence = "AGCTGACTTGGTC"
k = 3
embedding = dna_to_graph2vec_embedding(dna_sequence, k)
print("Graph Embedding:\n", embedding)

k=3
X_input=[]
for i in X:
    X2=dna_to_graph2vec_embedding(i,k)
    X_input.append(X2)

#print(X_input)
X_input=np.asarray(X_input)
#np.info(X_input)
print(X_input[0])
np.info(X_input[0])



#Train and Test split
from sklearn.model_selection import train_test_split
# Split
X_train, X_test, y_train, y_test = train_test_split(X_input,y_output,test_size=0.1,random_state=42)
X_train.shape
y_train.shape




import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# Define the model
model = Sequential([
    Dense(128, activation='relu', input_dim=64),  # Assuming embedding size is 64
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(2, activation='softmax')  # Change 'num_classes' based on your classification needs
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',  # or 'categorical_crossentropy' if labels are one-hot encoded
              metrics=['accuracy'])



# Example training command
history = model.fit(X_train, y_train, epochs=1000, validation_split=0.1)

# Evaluate the model on the test set
test_loss, test_acc = model.evaluate(X_test, y_test)
print('Test Accuracy:', test_acc)






import matplotlib.pyplot as plt

# Plot training & validation loss values
plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'], label='Training loss')
plt.plot(history.history['val_loss'], label='Validation loss')
plt.title('Model Loss Over Epochs')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()

import numpy as np

# Predict probabilities for each class
probabilities = model.predict(X_test)
# Convert probabilities to class labels
y_pred = np.argmax(probabilities, axis=1)
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

conf_matrix = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix)
disp.plot()

from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# Compute ROC curve and ROC area for each class
fpr, tpr, _ = roc_curve(y_test, probabilities[:, 1])  # probabilities[:, 1]: probability of the positive class
roc_auc = auc(fpr, tpr)

# Plotting
plt.figure()
lw = 2  # Line width
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()

# # For ROC Curve
# plt.savefig('roc_curve.png')

# # For Confusion Matrix
# plt.figure()
# disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=[0, 1])
# disp.plot()
# plt.savefig('confusion_matrix.png')

