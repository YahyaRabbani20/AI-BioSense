# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 12:41:36 2024

@author: yahya
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 


data=pd.read_excel('First Round.xlsx')
data_lengths=pd.read_excel('First Round.xlsx',sheet_name='lengths effect')
df=data_lengths



# Define the color for the bars
bar_color = 'lightblue'

# Plotting Intensity with standard deviation
plt.figure(figsize=(5, 4))

# Plot for (7,6) Intensity
plt.bar(df['Name tube'], df['(7,6) Intensity'], yerr=df['(7,6) Intensity_Std'], capsize=5, color=bar_color)
plt.title('(7,6)')
plt.xlabel('DNA Sequence')
plt.ylabel('Intensity Change(%)')
plt.ylim(-10,20)
plt.xticks(rotation=45)

plt.savefig('Intensity_7,6.png',dpi=900)  # Saving the plot as a PNG file


# Plot for (9,4) Intensity
plt.figure(figsize=(5, 4))
plt.bar(df['Name tube'], df['(9,4) Intensity'], yerr=df['(9,4) Intensity_Std'], capsize=5, color=bar_color)
plt.title('(9,4)')
plt.xlabel('DNA Sequence')
plt.ylabel('Intensity Change(%)')
plt.ylim(-10,20)
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('Intensity_9,4.png',dpi=900)  # Saving the plot as a PNG file
plt.show()

# Plotting Shift with standard deviation
plt.figure(figsize=(5, 4))

# Plot for (9,4) Shift
plt.subplot(1, 1, 1)  # Corrected the subplot index for a single plot
plt.bar(df['Name tube'], df['(9,4) Shift'], yerr=df['(9,4) Shift_Std'], capsize=5, color=bar_color)
plt.title('(9,4)')
plt.xlabel('DNA Sequence')
plt.ylabel('Peak Shift(nm)')
plt.ylim(-1,1)

plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('Shift_Plots.png',dpi=900)  # Saving the plot as a PNG file
plt.show()





import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from matplotlib import cm

# Load data (ensure your data loading here)
df = data

# Define the colormap
cmap = cm.Blues

# Normalize the data to use for the color mapping
# Custom normalization range - adjust these values as needed
custom_min = 0.0  # Set your custom minimum value
custom_max = 50  # Set your custom maximum value

# Normalize the data using the custom range
norm = plt.Normalize(custom_min, custom_max)
# Plotting Intensity with standard deviation
plt.figure(figsize=(15, 4))

# Plot for (7,6) Intensity with color based on value
colors = cmap(norm(df['(7,6) Intensity']))
plt.bar(df['Num'], df['(7,6) Intensity'], yerr=df['(7,6) Intensity_Std'], capsize=5, color=colors)
plt.title('(7,6)')
plt.xlabel('DNA Sequence')
plt.ylabel('Intensity Change(%)')
plt.ylim(-10, 100)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Intensity_7,6_All.png',dpi=900)  # Saving the plot as a PNG file
plt.show()

# Normalize the data for (9,4) Intensity
custom_min = 0.0  # Set your custom minimum value
custom_max = 80   # Set your custom maximum value

# Normalize the data using the custom range
norm = plt.Normalize(custom_min, custom_max)
plt.figure(figsize=(15, 4))
colors = cmap(norm(df['(9,4) Intensity']))
plt.bar(df['Num'], df['(9,4) Intensity'], yerr=df['(9,4) Intensity_Std'], capsize=5, color=colors)
plt.title('(9,4)')
plt.xlabel('DNA Sequence')
plt.ylabel('Intensity Change(%)')
plt.ylim(-10, 100)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Intensity_9,4_All.png',dpi=900)  # Saving the plot as a PNG file
plt.show()

cmap = cm.Blues_r

# Custom normalization range - adjust these values as needed
custom_min = -3.0  # Set your custom minimum value
custom_max = 0.0   # Set your custom maximum value

# Normalize the data using the custom range
norm = plt.Normalize(custom_min, custom_max)

plt.figure(figsize=(15, 4))
colors = cmap(norm(df['(9,4) Shift']))
plt.bar(df['Num'], df['(9,4) Shift'], yerr=df['(9,4) Shift_Std'], capsize=2, color=colors)
plt.title('(9,4)')
plt.xlabel('DNA Sequence')
plt.ylabel('Peak Shift(nm)')
plt.ylim(-3, 3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Shift_Plots_All.png',dpi=900)  # Saving the plot as a PNG file
plt.show()


#sort by len




# Load data (ensure your data loading here)
df=pd.read_excel('First Round_len.xlsx')

# Define the colormap
cmap = cm.Blues

# Normalize the data to use for the color mapping
# Custom normalization range - adjust these values as needed
custom_min = 0.0  # Set your custom minimum value
custom_max = 50  # Set your custom maximum value

# Normalize the data using the custom range
norm = plt.Normalize(custom_min, custom_max)
# Plotting Intensity with standard deviation
plt.figure(figsize=(15, 3))

# Plot for (7,6) Intensity with color based on value
colors = cmap(norm(df['(7,6) Intensity']))
plt.bar(df['Num'], df['(7,6) Intensity'], yerr=df['(7,6) Intensity_Std'], capsize=5, color=colors)
plt.title('(7,6)')
plt.xlabel('DNA Sequence')
plt.ylabel('Intensity Change(%)')
plt.ylim(-10, 60)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Intensity_7,6_All_len.png',dpi=900)  # Saving the plot as a PNG file
plt.show()

# Normalize the data for (9,4) Intensity
custom_min = 0.0  # Set your custom minimum value
custom_max = 80   # Set your custom maximum value

# Normalize the data using the custom range
norm = plt.Normalize(custom_min, custom_max)
plt.figure(figsize=(15, 3))
colors = cmap(norm(df['(9,4) Intensity']))
plt.bar(df['Num'], df['(9,4) Intensity'], yerr=df['(9,4) Intensity_Std'], capsize=5, color=colors)
plt.title('(9,4)')
plt.xlabel('DNA Sequence')
plt.ylabel('Intensity Change(%)')
plt.ylim(-10, 100)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Intensity_9,4_Al_len.png',dpi=900)  # Saving the plot as a PNG file
plt.show()

cmap = cm.Blues_r

# Custom normalization range - adjust these values as needed
custom_min = -3.0  # Set your custom minimum value
custom_max = 0.0   # Set your custom maximum value

# Normalize the data using the custom range
norm = plt.Normalize(custom_min, custom_max)

plt.figure(figsize=(15, 3))
colors = cmap(norm(df['(9,4) Shift']))
plt.bar(df['Num'], df['(9,4) Shift'], yerr=df['(9,4) Shift_Std'], capsize=2, color=colors)
plt.title('(9,4)')
plt.xlabel('DNA Sequence')
plt.ylabel('Peak Shift(nm)')
plt.ylim(-3, 1)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Shift_Plots_All_len.png',dpi=900)  # Saving the plot as a PNG file
plt.show()


### box plot


# Load data (make sure you load your DataFrame here)
df = data

# Creating a boxplot with an overlaid scatter plot for (7,6) Intensity
plt.figure(figsize=(5, 4))
ax = df.boxplot(column='(7,6) Intensity', by='len', grid=False)
plt.title('Box Plot with Scatter of (7,6) Intensity by Sequence Length')
plt.xlabel('Sequence Length')
plt.ylabel('(7,6) Intensity')
plt.suptitle('')

# Adding scatter plot
for i, (name, group) in enumerate(df.groupby('len'), start=1):
    y = group['(7,6) Intensity']
    x = np.random.normal(i, 0.04, size=len(y))  # Add some jitter to the x-axis
    plt.scatter(x, y, alpha=0.6)

plt.xticks(rotation=45)
plt.savefig('Box_Scatter_7,6_Intensity_by_Length.png',dpi=900)
plt.show()

# Creating a boxplot with an overlaid scatter plot for (9,4) Intensity
plt.figure(figsize=(5, 4))
ax = df.boxplot(column='(9,4) Intensity', by='len', grid=False)
plt.title('Box Plot with Scatter of (9,4) Intensity by Sequence Length')
plt.xlabel('Sequence Length')
plt.ylabel('(9,4) Intensity')
plt.suptitle('')

# Adding scatter plot
for i, (name, group) in enumerate(df.groupby('len'), start=1):
    y = group['(9,4) Intensity']
    x = np.random.normal(i, 0.04, size=len(y))  # Add some jitter to the x-axis
    plt.scatter(x, y, alpha=0.6)

plt.xticks(rotation=45)
plt.savefig('Box_Scatter_9,4_Intensity_by_Length.png',dpi=900)
plt.show()

# Creating a boxplot with an overlaid scatter plot for (9,4) Shift
plt.figure(figsize=(5, 4))
ax = df.boxplot(column='(9,4) Shift', by='len', grid=False)
plt.title('Box Plot with Scatter of (9,4) Shift by Sequence Length')
plt.xlabel('Sequence Length')
plt.ylabel('(9,4) Shift (nm)')
plt.suptitle('')

# Adding scatter plot
for i, (name, group) in enumerate(df.groupby('len'), start=1):
    y = group['(9,4) Shift']
    x = np.random.normal(i, 0.04, size=len(y))  # Add some jitter to the x-axis
    plt.scatter(x, y, alpha=0.6)

plt.xticks(rotation=45)
plt.savefig('Box_Scatter_9,4_Shift_by_Length.png',dpi=900)
plt.show()


