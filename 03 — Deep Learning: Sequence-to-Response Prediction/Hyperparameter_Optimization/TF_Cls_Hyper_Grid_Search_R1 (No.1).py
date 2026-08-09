
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 10:16:23 2024

@author: Yahya Rbn
"""


                            ### Part A: Preprocssenig of the data ###
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

              # Read the dataset##
dataset=pd.read_excel('All_Data(152 DNA_seq) -Seperated_class.xlsx')
X=dataset.iloc[:,4]
#One output
y=dataset.iloc[:,[5,7]]
#dataset['class']
y_output=np.asarray(y)
#two Output
#y=dataset.iloc[:,[5,7]]
#y_output=np.asarray(y)

# preprocessing

plt.figure(figsize=(10, 6))
sns.distplot(y['PL intensity'], label='PL intensity')
sns.distplot(y['Quenching'], label='Quenching')
plt.legend()
plt.xlabel('Value')
plt.ylabel('Density')
plt.show()

# classification of the data

y['Intensity_class']= y['PL intensity'].apply(lambda x:1 if x >88 else 0 )
y['Quenching_class']= y['Quenching'].apply(lambda x:1 if x >78 else 0 )
y_output=np.asarray(y)
y_output=y_output[:,2:4]

#sns.scatterplot(x=np.arange(len(y)), y='Intensity_class', data=y, hue='Quenching_class', palette='flare',edgecolor=None,alpha=0.6)

plt.figure(figsize=(12,8))
sns.histplot(y['Intensity_class'], kde=True, label='PL intensity', color='blue')
sns.histplot(y['Quenching_class'], kde=True, label='Quenching', color='red')
plt.legend()
plt.show()





# converting the DNA seq
def one_hot_encode(seq):
    mapping = dict(zip("AGCT", range(4)))    
    seq2 = [mapping[i] for i in seq]
    return np.eye(4)[seq2]

#Example:
E = one_hot_encode("AG")
E1 = one_hot_encode("AG").reshape(8,1) # convert to array
##
X_input=[]
for i in X:
    X2=one_hot_encode(i).reshape(120)
    X_input.append(X2)

#print(X_input)
X_input=np.asarray(X_input)
#np.info(X_input)
print(X_input)
np.info(X_input)



                                         ### Part B: Training###

#Train and Test split
from sklearn.model_selection import train_test_split
# Split
X_train, X_test, y_train, y_test = train_test_split(X_input,y_output,test_size=0.1,random_state=42)
X_train.shape
y_train.shape

#Model structure

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
from tensorflow.keras.regularizers import l2
from sklearn.model_selection import train_test_split

# Define hyperparameter options for grid search
optimizers = ['adam', 'sgd', 'rmsprop']
learning_rates = [0.001, 0.01]  # Example ranges for learning rates
num_layers_options = [3, 5]  # Number of hidden layers
units_options = [10,50,100]  # Number of neurons in each layer
activations = ['relu', 'tanh']  # Activation functions
dropout_rates = [0.1,0.5]  # Dropout rates
l2_regularizations = [0.001, 0.01]  # L2 regularization values

# Define the output units for classification with 2 outputs
output_units = 2

# Define the model building function for classification
def build_classification_model(optimizer, learning_rate, num_layers, units, activation, dropout_rate, l2_regularization):
    if optimizer == 'adam':
        optimizer = Adam(learning_rate=learning_rate)
    elif optimizer == 'sgd':
        optimizer = SGD(learning_rate=learning_rate)
    elif optimizer == 'rmsprop':
        optimizer = RMSprop(learning_rate=learning_rate)

    model = Sequential()
    for _ in range(num_layers):
        model.add(Dense(units=units, activation=activation, kernel_regularizer=l2(l2_regularization)))
        model.add(BatchNormalization())
        model.add(Dropout(rate=dropout_rate))
    model.add(Dense(output_units, activation='sigmoid'))  # Sigmoid activation for binary classification
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    return model


import matplotlib.pyplot as plt

def plot_history(history):
    # Plot training & validation accuracy values
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    
    # Plot training & validation loss values
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    
    plt.tight_layout()
    plt.show()


# Split data - Assuming you have already defined X_train and y_train
X_train_sub, X_val, y_train_sub, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

best_model = None
best_accuracy = 0

for optimizer in optimizers:
    for lr in learning_rates:
        for num_layers in num_layers_options:
            for units in units_options:
                for activation in activations:
                    for dropout in dropout_rates:
                        for l2_reg in l2_regularizations:
                            model = build_classification_model(optimizer, lr, num_layers, units, activation, dropout, l2_reg)
                            history = model.fit(X_train_sub, y_train_sub, epochs=10, validation_data=(X_val, y_val), verbose=0)
                            val_loss, val_accuracy = model.evaluate(X_val, y_val, verbose=0)
                            if val_accuracy > best_accuracy:
                                best_accuracy = val_accuracy
                                best_model = model
                                best_params = (optimizer, lr, num_layers, units, activation, dropout, l2_reg)
                                best_history = history  # Capture the best model's training history
# After grid search
plot_history(best_history)  # Plot the best model's performance


print("Best validation accuracy:", best_accuracy)
print("Best parameters:", best_params)



