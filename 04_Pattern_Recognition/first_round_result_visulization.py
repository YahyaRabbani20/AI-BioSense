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
plt.figure(figsize=(12, 6))

# Plot for (7,6) Intensity
plt.subplot(1, 2, 1)
plt.bar(df['Name tube'], df['(7,6) Intensity'], yerr=df['(7,6) Intensity_Std'], capsize=5, color=bar_color)
plt.title('Intensity at (7,6)')
plt.xlabel('DNA Sequence')
plt.ylabel('Intensity Change(%)')
plt.ylim(-10,20)

plt.xticks(rotation=45)

# Plot for (9,4) Intensity
plt.subplot(1, 2, 2)
plt.bar(df['Name tube'], df['(9,4) Intensity'], yerr=df['(9,4) Intensity_Std'], capsize=5, color=bar_color)
plt.title('Intensity at (9,4)')
plt.xlabel('DNA Sequence')
plt.ylabel('Intensity Change(%)')
plt.ylim(-10,20)
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('Intensity_Plots.png')  # Saving the plot as a PNG file
plt.show()

# Plotting Shift with standard deviation
plt.figure(figsize=(12, 6))

# Plot for (9,4) Shift
plt.subplot(1, 1, 1)  # Corrected the subplot index for a single plot
plt.bar(df['Name tube'], df['(9,4) Shift'], yerr=df['(9,4) Shift_Std'], capsize=5, color=bar_color)
plt.title('Shift at (9,4)')
plt.xlabel('DNA Sequence')
plt.ylabel('Peak Shift(nm)')
plt.ylim(-1,1)

plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('Shift_Plots.png')  # Saving the plot as a PNG file
plt.show()
