


# -*- coding: utf-8 -*-
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


                      ### Part B: Training ###

# Set seeds for reproducibility
import random
import tensorflow as tf
np.random.seed(42)       # NumPy random generator
random.seed(42)          # Python random generator
tf.random.set_seed(42)   # TensorFlow random generator


#Model structure
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense,MaxPooling2D,AveragePooling2D,Activation,Dropout
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import KFold
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
import optuna


#Train and Test split
from sklearn.model_selection import train_test_split
# Split the data ensuring an equal distribution of classes in train and test sets
X_train, X_test, y_train, y_test = train_test_split(X_input, y_output, test_size=0.2, random_state=42, stratify=y_output )
# Ensures proportionate distribution of classes by adding the stratify


def create_model(trial):
    num_filters1 = trial.suggest_categorical('num_filters1', [8,16, 32, 64,128])
    num_filters2 = trial.suggest_categorical('num_filters2', [4,8, 16, 32,64])
    kernel_size = trial.suggest_categorical('kernel_size', [(2, 2),(3, 3), (4, 4) ,(5, 5)])
    dense_units = trial.suggest_categorical('dense_units', [32, 64])
    dropout_rate = trial.suggest_uniform('dropout_rate', 0.0, 0.2)
    learning_rate = trial.suggest_loguniform('learning_rate', 1e-4, 1e-1)
    pooling_type = trial.suggest_categorical('pooling_type', ['max', 'average'])
    pool_size1 = trial.suggest_categorical('pool_size1', [(2, 1),(2, 2) ,(3, 1),(3, 2) ,(3, 3),(4, 1),(4, 2)])  # Pooling kernel for the first layer
    pool_size2 = trial.suggest_categorical('pool_size2', [(2, 1),(2, 2) ,(3, 1),(3, 2) ,(3, 3),(4, 1),(4, 2)])  # Pooling kernel for the second layer

    # Selecting the optimizer
    optimizer_options = trial.suggest_categorical('optimizer', ['adam', 'sgd', 'rmsprop'])
    if optimizer_options == 'adam':
        optimizer = Adam(learning_rate=learning_rate)
    elif optimizer_options == 'sgd':
        momentum = trial.suggest_uniform('momentum', 0.0, 1.0)
        optimizer = SGD(learning_rate=learning_rate, momentum=momentum)
    elif optimizer_options == 'rmsprop':
        optimizer = RMSprop(learning_rate=learning_rate)

    model = Sequential()
    model.add(Conv2D(num_filters1, kernel_size=kernel_size, padding='same', input_shape=(30, 5, 1)))
    model.add(Activation('relu'))
    if pooling_type == 'max':
        model.add(MaxPooling2D(pool_size=pool_size1, padding='same'))
    else:
        model.add(AveragePooling2D(pool_size=pool_size1, padding='same'))
    model.add(Conv2D(num_filters2, kernel_size=kernel_size, padding='same'))
    model.add(Activation('relu'))
    if pooling_type == 'max':
        model.add(MaxPooling2D(pool_size=pool_size2, padding='same'))
    else:
        model.add(AveragePooling2D(pool_size=pool_size2, padding='same'))
    model.add(Flatten())
    model.add(Dense(dense_units))
    model.add(Activation('relu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(dense_units // 2))
    model.add(Activation('relu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(2))
    model.add(Activation('sigmoid'))

    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    return model

def objective(trial):
    num_folds = trial.suggest_int('num_folds', 2,4)  #Start from at least 2
    kfold = KFold(n_splits=num_folds, shuffle=True, random_state=42)
    losses = []

    for train_k, test_k in kfold.split(X_train, y_train):
        model = create_model(trial)
        early_stop = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=50)
        model.fit(x=X_train[train_k], y=y_train[train_k], epochs=1200, validation_data=(X_train[test_k], y_train[test_k]),
                  verbose=1, callbacks=[early_stop])
        loss = model.evaluate(X_train[test_k], y_train[test_k], verbose=0)
        losses.append(loss[0])

    return np.mean(losses)

study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=100)

print("Best hyperparameters: ", study.best_trial.params)

best_params = study.best_trial.params
df = pd.DataFrame([best_params])
df.to_csv('best_hyperparameters.csv', index=False)
