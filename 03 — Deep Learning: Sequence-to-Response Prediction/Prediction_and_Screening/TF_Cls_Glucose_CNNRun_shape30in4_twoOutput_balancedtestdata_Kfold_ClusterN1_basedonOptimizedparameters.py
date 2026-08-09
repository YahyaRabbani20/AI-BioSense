


# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 13:51:34 2024

@author: Yahya Rbn
"""
#best kfold

                            ### Part A: Preprocssenig of the data ###
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
plt.rcParams.update({
    'font.size': 12,  # Set the font size for all text
    'font.family': 'Arial',  # Set the font family for all text
    'axes.titlesize': 12,  # Set the font size for axes titles
    'axes.labelsize': 12,  # Set the font size for x and y labels
    'xtick.labelsize': 12,  # Set the font size for x tick labels
    'ytick.labelsize': 12,  # Set the font size for y tick labels
    'legend.fontsize': 12,  # Set the font size for legend
    'figure.titlesize': 12,  # Set the font size for figure title
    'figure.facecolor': 'white',  # Set the figure face color to white
    'axes.facecolor': 'white',  # Set the axes face color to white
    'axes.grid': False,  # Disable the grid by default
    'axes.edgecolor': 'black',  # Set the color of the edge of the plot area
})

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
plt.savefig('distplotforalldata.jpg',dpi=900)
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
plt.savefig('dataclass.jpg',dpi=900)

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



#num_folds	num_filters1	num_filters2	kernel_size	dense_units	dropout_rate	learning_rate	pooling_type	pool_size1	pool_size2	optimizer
#   2	      8               	8	         (2, 2)	       64     	0.196428867	    0.009915996	       average	    (4, 2)      	(4, 2)	  adam





#Model structure
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation,Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense,MaxPooling2D,AveragePooling2D
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation,Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam

#Train and Test split
from sklearn.model_selection import train_test_split
# Split the data ensuring an equal distribution of classes in train and test sets
X_train, X_test, y_train, y_test = train_test_split(X_input, y_output, test_size=0.2, random_state=42, stratify=y_output )
# Ensures proportionate distribution of classes by adding the stratify

results = []
best_fold=2 # from fold optimization
fold_no = 1
all_histories = []
predictions_list=[]
# Evaluate across the best-folds
print(f"Evaluating {best_fold} folds...")

kfold = KFold(n_splits=best_fold, shuffle=True)

for train_k, test_k in kfold.split(X_train, y_train):
    model = Sequential()
    # First convolutional layer, adapted for input shape of (30, 5, 1)
    model.add(Conv2D(8, kernel_size=(2, 2), padding='same', input_shape=(30, 5, 1)))
    model.add(Activation('relu'))
    
    # First Average Pooling layer
    model.add(AveragePooling2D(pool_size=(4,2)))
    
    # Second convolutional layer with different filter configuration
    model.add(Conv2D(8, kernel_size=(2, 2), padding='same'))
    model.add(Activation('relu'))
    
    # Second Average Pooling layer
    model.add(AveragePooling2D(pool_size=(4, 2)))
    
    # Flatten layer to vectorize the data
    model.add(Flatten())
    
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.196428867))

    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.196428867))

    # Output layer with 2 unit for binary classification
    model.add(Dense(2))
    model.add(Activation('sigmoid'))  # Using sigmoid for binary classification

    #Early stop
    early_stop = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=200)
    # For a binary classification problem
    optimizer = Adam(learning_rate=0.009915996)
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    history = model.fit(x=X_train[train_k], y=y_train[train_k], epochs=2000, validation_data=(X_train[test_k], y_train[test_k]), verbose=1 , callbacks=[early_stop] )
    model.summary()
    # Save the model
    model_path = f'model_fold_{fold_no}.h5'  # Using H5 format to save model
    model.save(model_path)
    print(f'Model saved: {model_path}')   
    
    # Predicting on test data
    predictions = model.predict(X_test)
    predictions_list.append(predictions)
    all_histories.append(history.history)
    fold_no += 1

# Averaging predictions across all folds
average_predictions = np.mean(predictions_list, axis=0)
     
 
                      ### PartC: Evaluation of the model ###
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# Convert probabilities to class labels based on a threshold of 0.5
binary_predictions = (average_predictions > 0.5).astype(int)

# Metrics for each output
for i in range(2):
    accuracy = accuracy_score(y_test[:, i], binary_predictions[:, i])
    precision = precision_score(y_test[:, i], binary_predictions[:, i])
    recall = recall_score(y_test[:, i], binary_predictions[:, i])
    f1 = f1_score(y_test[:, i], binary_predictions[:, i])
    roc_auc = roc_auc_score(y_test[:, i], average_predictions[:, i])

    print(f'Output {i+1} Metrics:')
    print(f'  Accuracy: {accuracy:.4f}')
    print(f'  Precision: {precision:.4f}')
    print(f'  Recall: {recall:.4f}')
    print(f'  F1 Score: {f1:.4f}')
    print(f'  ROC AUC Score: {roc_auc:.4f}\n')

import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# Assuming binary_predictions and y_test are already defined
metrics_data = []

for i in range(2):
    accuracy = accuracy_score(y_test[:, i], binary_predictions[:, i])
    precision = precision_score(y_test[:, i], binary_predictions[:, i])
    recall = recall_score(y_test[:, i], binary_predictions[:, i])
    f1 = f1_score(y_test[:, i], binary_predictions[:, i])
    roc_auc = roc_auc_score(y_test[:, i], average_predictions[:, i])

    metrics_data.append({
        'Output': f'Output {i+1}',
        'Accuracy': f'{accuracy:.4f}',
        'Precision': f'{precision:.4f}',
        'Recall': f'{recall:.4f}',
        'F1 Score': f'{f1:.4f}',
        'ROC AUC Score': f'{roc_auc:.4f}'
    })

# Create DataFrame
metrics_df = pd.DataFrame(metrics_data)

# Display the DataFrame
print(metrics_df.to_string(index=False))


import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

fig, axes = plt.subplots(1, 2, figsize=(16, 7))  # Adjust figure size as necessary
sns.set(font_scale=1.0)  # Adjust font scale for better readability

binary_predictions = (average_predictions > 0.5).astype(int)

for i in range(2):
    cm = confusion_matrix(y_test[:, i], binary_predictions[:, i])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Class 0', 'Class 1'], yticklabels=['Class 0', 'Class 1'], ax=axes[i])
    axes[i].set_title(f'Confusion Matrix for Output {i+1}')
    axes[i].set_xlabel('Predicted Labels')
    axes[i].set_ylabel('True Labels')

plt.tight_layout()
plt.savefig('Confusion Matrix.jpg', dpi=900)

plt.show()

from sklearn.metrics import roc_curve, auc

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
plt.rcParams.update({
    'font.size': 12,  # Set the font size for all text
    'font.family': 'Arial',  # Set the font family for all text
    'axes.titlesize': 12,  # Set the font size for axes titles
    'axes.labelsize': 12,  # Set the font size for x and y labels
    'xtick.labelsize': 12,  # Set the font size for x tick labels
    'ytick.labelsize': 12,  # Set the font size for y tick labels
    'legend.fontsize': 12,  # Set the font size for legend
    'figure.titlesize': 12,  # Set the font size for figure title
    'figure.facecolor': 'white',  # Set the figure face color to white
    'axes.facecolor': 'white',  # Set the axes face color to white
    'axes.grid': False,  # Disable the grid by default
    'axes.edgecolor': 'black',  # Set the color of the edge of the plot area
})
for i in range(2):
    fpr, tpr, _ = roc_curve(y_test[:, i], average_predictions[:, i])
    roc_auc = auc(fpr, tpr)

    axes[i].plot(fpr, tpr, color='red', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    axes[i].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    axes[i].set_xlim([0.0, 1.0])
    axes[i].set_ylim([0.0, 1.05])
    axes[i].set_xlabel('False Positive Rate')
    axes[i].set_ylabel('True Positive Rate')
    axes[i].set_title(f'Receiver Operating Characteristic for Output {i+1}')
    axes[i].legend(loc="lower right")

plt.tight_layout()
plt.savefig('Receiver Operating Characteristic_label.jpg', dpi=900)
plt.show()




import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import numpy as np

# Update matplotlib settings for fonts and other plot settings
plt.rcParams.update({
    'font.size': 15,  # Set the font size for all text
    'font.family': 'Arial',  # Set the font family for all text
    'axes.titlesize': 15,  # Set the font size for axes titles
    'axes.labelsize': 15,  # Set the font size for x and y labels
    'xtick.labelsize': 13,  # Set the font size for x tick labels
    'ytick.labelsize': 13,  # Set the font size for y tick labels
    'legend.fontsize': 13,  # Set the font size for legend
    'figure.titlesize': 13,  # Set the font size for figure title
    'figure.facecolor': 'white',  # Set the figure face color to white
    'axes.facecolor': 'white',  # Set the axes face color to white
    'axes.grid': False,  # Disable the grid by default
    'axes.edgecolor': 'black',  # Set the color of the edge of the plot area
    'axes.linewidth': 1.0  # Set the line width of the edge of the plot area
})


# Plot ROC curves
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

for i in range(2):
    fpr, tpr, _ = roc_curve(y_test[:, i], average_predictions[:, i])
    roc_auc = auc(fpr, tpr)

    axes[i].plot(fpr, tpr, color='red', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    axes[i].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    axes[i].set_xlim([0.0, 1.0])
    axes[i].set_ylim([0.0, 1.05])
    axes[i].set_xlabel('False Positive Rate')
    axes[i].set_ylabel('True Positive Rate')
    axes[i].set_title(f'Receiver Operating Characteristic for Output {i+1}')
    axes[i].legend(loc="lower right")

    # Remove grid and set background to white
    axes[i].grid(False)
    axes[i].set_facecolor('white')

    # Add a box around each subplot
    for spine in axes[i].spines.values():
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(1.0)

plt.tight_layout()
plt.savefig('Receiver Operating Characteristic_label-final.jpg', dpi=900)
plt.show()








from tensorflow.keras.models import load_model
#model.save('my_model2.keras')  # creates a HDF5 file 'my_model.h5'
# # later_model = load_model('my_model.keras')
# # later_model.predict(new_gem)



import matplotlib.pyplot as plt
import numpy as np

# Assume all_histories is already populated with the history objects from training each fold
num_folds = len(all_histories)
max_epochs = max(len(history['loss']) for history in all_histories)

# Prepare arrays to store aggregated loss data
all_train_losses = np.zeros((num_folds, max_epochs))
all_val_losses = np.zeros((num_folds, max_epochs))

# Predefined colors to distinguish different folds
colors = plt.cm.viridis(np.linspace(0, 1, num_folds))

# Fill the arrays with loss data, using NaN for padding shorter histories
for i, history in enumerate(all_histories):
    epochs = len(history['loss'])
    all_train_losses[i, :epochs] = history['loss']
    all_train_losses[i, epochs:] = np.nan  # Pad the rest with NaN
    all_val_losses[i, :epochs] = history['val_loss']
    all_val_losses[i, epochs:] = np.nan  # Pad the rest with NaN

# Compute the mean across all folds ignoring NaNs
avg_train_loss = np.nanmean(all_train_losses, axis=0)
avg_val_loss = np.nanmean(all_val_losses, axis=0)

# Plotting
plt.figure(figsize=(6, 5))

# Plot each fold's loss and validation loss
for i in range(num_folds):
    plt.plot(all_train_losses[i], label=f'Fold {i+1} Training Loss', linestyle='-', color=colors[i])
    plt.plot(all_val_losses[i], label=f'Fold {i+1} Validation Loss', linestyle='--', color=colors[i])

# Plot the average loss across all folds
plt.plot(avg_train_loss, color='black', linewidth=2, label='Average Training Loss')
plt.plot(avg_val_loss, color='red', linewidth=2, label='Average Validation Loss')

plt.title('Training and Validation Loss Across All Folds with Average')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))  # Adjust legend position to avoid clipping
plt.grid(True)
plt.xlim(0,200)
plt.tight_layout()
plt.savefig('Training and Validation Loss Across All Folds with Average.jpg', dpi=900)

plt.show()


                           ### PartC: Evaluation of the model ###

from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from matplotlib.colors import ListedColormap


# Assuming 'probabilities' is a numpy array with shape [n_samples, 2] from model.predict()
# And 'y_test' is similarly shaped with actual binary labels for comparison

# Convert probabilities to class labels based on a threshold of 0.5
probabilities = model.predict(X_test)
predictions = (probabilities > 0.5).astype(int)

# Iterate through each output (label)
for i in range(probabilities.shape[1]):
    print(f"Results for Label {i}:")

    # Generate and print the classification report
    print(classification_report(y_test[:, i], predictions[:, i]))

    # Generate the confusion matrix
    cm = confusion_matrix(y_test[:, i], predictions[:, i])
    print("Confusion Matrix:")
    print(cm)


    # Plot the confusion matrix
    mask = np.eye(cm.shape[0], cm.shape[1], dtype=bool)
    
    # Custom color map: light green for true predictions, light blue for others
    cmap = ListedColormap(['#add8e6', '#90ee90'])  # light blue, light green
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, mask=~mask, cmap=ListedColormap(['#90ee90']), cbar=False,
                xticklabels=['Class 0', 'Class 1'], yticklabels=['Class 0', 'Class 1'])
    sns.heatmap(cm, annot=True, mask=mask, cmap=ListedColormap(['#add8e6']), cbar=False,
                xticklabels=['Class 0', 'Class 1'], yticklabels=['Class 0', 'Class 1'])
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.title(f'Confusion Matrix for output {i+1}')
    plt.savefig(f'Confusion Matrix {i}.jpg', dpi=900)

    plt.show()

    # Calculate ROC curve and AUC
    fpr, tpr, thresholds = roc_curve(y_test[:, i], probabilities[:, i])
    roc_auc = auc(fpr, tpr)

    # Plot ROC curve6
    plt.figure(figsize=(5, 4))
    plt.plot(fpr, tpr, color='red', lw=2, label=f'ROC curve for label {i} (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--',label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.savefig(f'Receiver Operating Characteristic_label {i}.jpg', dpi=900)
    plt.show()

### prediction####

from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd

# Define the function to one-hot encode the DNA sequences
def one_hot_encode(seq, fixed_length=30):
    mapping = dict(zip("AGCTN", range(5)))  # Including 'N' for padding
    seq = (seq + 'N' * fixed_length)[:fixed_length]
    seq_encoded = [mapping[char] for char in seq]
    return np.eye(5)[seq_encoded]  # One-hot encoding

# Load new DNA sequences from an Excel file for prediction
new_data = pd.read_excel('Seq_from_data_analysis.xlsx')
X_new = new_data.iloc[:, 1]  # Adjust the index based on your data

# Preprocess the DNA sequences
X_new_input = np.array([one_hot_encode(seq) for seq in X_new])
X_new_input = X_new_input.reshape(-1, 30, 5, 1)  # Reshape for the CNN

# Load each model and predict
predictions = []
num_models = 2  # Number of k-fold models

for i in range(num_models):
    model = load_model(f'model_fold_{i+1}.h5')
    predictions.append(model.predict(X_new_input))

# Average predictions from all models
average_predictions = np.mean(predictions, axis=0)
binary_predictions = (average_predictions > 0.5).astype(int)

# Add predictions back to the DataFrame
new_data['Predicted Output 1 Probability'] = average_predictions[:, 0]
new_data['Predicted Output 2 Probability'] = average_predictions[:, 1]
new_data['Predicted Output 1'] = binary_predictions[:, 0]
new_data['Predicted Output 2'] = binary_predictions[:, 1]

# Save the results back to an Excel file
new_data.to_excel('predicted_classes_Seq_from_data_analysis.xlsx')

# Optionally, print the DataFrame for verification
print(new_data[['Predicted Output 1 Probability', 'Predicted Output 2 Probability', 'Predicted Output 1', 'Predicted Output 2']])




                                     ### prediction####

from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd

# Define the function to one-hot encode the DNA sequences
def one_hot_encode(seq, fixed_length=30):
    mapping = dict(zip("AGCTN", range(5)))  # Including 'N' for padding
    seq = (seq + 'N' * fixed_length)[:fixed_length]
    seq_encoded = [mapping[char] for char in seq]
    return np.eye(5)[seq_encoded]  # One-hot encoding

# Load new DNA sequences from an Excel file for prediction
new_data = pd.read_excel('Mutations_lib.xlsx')
X_new = new_data.iloc[:, 1]  # Adjust the index based on your data

# Preprocess the DNA sequences
X_new_input = np.array([one_hot_encode(seq) for seq in X_new])
X_new_input = X_new_input.reshape(-1, 30, 5, 1)  # Reshape for the CNN

# Load each model and predict
predictions = []
num_models = 2  # Number of k-fold models

for i in range(num_models):
    model = load_model(f'model_fold_{i+1}.h5')
    predictions.append(model.predict(X_new_input))

# Average predictions from all models
average_predictions = np.mean(predictions, axis=0)
binary_predictions = (average_predictions > 0.5).astype(int)

# Add predictions back to the DataFrame
new_data['Predicted Output 1 Probability'] = average_predictions[:, 0]
new_data['Predicted Output 2 Probability'] = average_predictions[:, 1]
new_data['Predicted Output 1'] = binary_predictions[:, 0]
new_data['Predicted Output 2'] = binary_predictions[:, 1]

# Save the results back to an Excel file
new_data.to_excel('predicted_class_Mutations_lib.xlsx')

# Optionally, print the DataFrame for verification
print(new_data[['Predicted Output 1 Probability', 'Predicted Output 2 Probability', 'Predicted Output 1', 'Predicted Output 2']])
