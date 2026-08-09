# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 18:05:59 2023

@author: LABO
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the data from the Excel file
df = pd.read_excel("133DNAfromDiffLeng-Final.xlsx")

## Calculate the proportion of each nucleotide in each DNA sequence
df['prop_G'] = df['DNA'].apply(lambda x: x.count('G') / len(x) )
df['prop_A'] = df['DNA'].apply(lambda x: x.count('A') / len(x) )
df['prop_C'] = df['DNA'].apply(lambda x: x.count('C') / len(x) )
df['prop_T'] = df['DNA'].apply(lambda x: x.count('T') / len(x) )

# Calculate the GC and AT content for each DNA sequence
df['GC_content'] = df['prop_G'] + df['prop_C']
df['AT_content'] = df['prop_A'] + df['prop_T']

# Calculate the mean response for each DNA sequence
df['(9,4) Intensity'] = df['(9,4) Intensity'].groupby([df['GC_content'], df['AT_content']]).transform('mean')
# Plot the mean response against the GC and AT content
# Define a color map to use for the scatter plot
cmap = plt.get_cmap('cool')

# Create a ScalarMappable object from the color map
sm = plt.cm.ScalarMappable(cmap=cmap)

# Plot the mean response against the GC and AT content, using a different color for each DNA sequence
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
for i, (axi, col) in enumerate(zip(ax.flat, ['GC_content', 'AT_content'])):
    sc = axi.scatter(df[col]*100, df['(9,4) Intensity'], c=df['(9,4) Intensity'], cmap=cmap, alpha=0.5)
    axi.set_xlabel(f'{col} (%)')
    axi.set_ylabel('(9,4) Intensity')
    
    # Add a colorbar to the plot
    # if i == 0:
    #     cbar = plt.colorbar(sm, ax=ax)
    #     cbar.ax.set_ylabel('Response')
        
for axi in ax.flat:
    axi.set_xlim([0, 100])
plt.tight_layout()
plt.savefig('GC_AT_content(9,4).png', dpi=900, bbox_inches='tight')
plt.show()


# Calculate the mean response for each DNA sequence
df['(7,6) Intensity'] = df['(7,6) Intensity'].groupby([df['GC_content'], df['AT_content']]).transform('mean')
# Plot the mean response against the GC and AT content
# Define a color map to use for the scatter plot
cmap = plt.get_cmap('cool')

# Create a ScalarMappable object from the color map
sm = plt.cm.ScalarMappable(cmap=cmap)

# Plot the mean response against the GC and AT content, using a different color for each DNA sequence
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
for i, (axi, col) in enumerate(zip(ax.flat, ['GC_content', 'AT_content'])):
    sc = axi.scatter(df[col]*100, df['(7,6) Intensity'], c=df['(7,6) Intensity'], cmap=cmap, alpha=0.5)
    axi.set_xlabel(f'{col} (%)')
    axi.set_ylabel('(7,6) Intensity')
    
    # Add a colorbar to the plot
    # if i == 0:
    #     cbar = plt.colorbar(sm, ax=ax)
    #     cbar.ax.set_ylabel('Response')
        
for axi in ax.flat:
    axi.set_xlim([0, 100])
plt.tight_layout()
plt.savefig('GC_AT_content(7,6).png', dpi=900, bbox_inches='tight')
plt.show()