import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

# Function to calculate the response for each base in a given DNA sequence
def calculate_base_responses(dna_sequence, response, mean_responses):
    dna_length = len(dna_sequence)
    normalized_response = response / dna_length

    for i, base in enumerate(dna_sequence):
        if len(mean_responses) <= i:
            mean_responses.append({})

        if base not in mean_responses[i]:
            mean_responses[i][base] = []

        mean_responses[i][base].append(normalized_response)

    return mean_responses

# Function to prepare data for 3D plotting
def prepare_data_for_3d_plot(mean_response_data, nucleotides):
    positions = range(len(mean_response_data))
    nucleotide_mapping = {nuc: i for i, nuc in enumerate(nucleotides)}
    X, Y = np.meshgrid(positions, list(nucleotide_mapping.values()))
    Z = np.zeros(X.shape)

    for i, pos in enumerate(positions):
        for nuc, nuc_index in nucleotide_mapping.items():
            Z[nuc_index, i] = mean_response_data[i].get(nuc, 0)

    return X, Y, Z

# Modified function to create 3D surface plot with specific Y-axis labels and color bar
def plot_3d_surface(X, Y, Z, title, nucleotides, y_label):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    y_ticks = range(len(nucleotides))
    surf = ax.plot_surface(X, Y, Z, cmap='coolwarm')
    ax.set_xlabel('Position')
    ax.set_ylabel(y_label)
    ax.set_zlabel('Value')
    ax.set_title(title)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(nucleotides)
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Intensity')
    plt.show()

# Load the data from an Excel file
df = pd.read_excel("133DNAfromDiffLeng-Final.xlsx")

mean_responses_76Intensity = []
mean_responses_pl_intensity = []

for index, row in df.iterrows():
    dna_sequence = row['DNA']
    response_76Intensity = row['(7,6) Intensity']
    response_pl_intensity = row['(9,4) Intensity']

    mean_responses_76Intensity = calculate_base_responses(dna_sequence, response_76Intensity, mean_responses_76Intensity)
    mean_responses_pl_intensity = calculate_base_responses(dna_sequence, response_pl_intensity, mean_responses_pl_intensity)

# Processing data for mean responses
mean_response_data_76Intensity = []
for i in range(len(mean_responses_76Intensity)):
    mean_response_dict = {}
    for base, responses in mean_responses_76Intensity[i].items():
        mean_response = sum(responses) / len(responses)
        mean_response_dict[base] = mean_response
    mean_response_data_76Intensity.append(mean_response_dict)

mean_response_data_pl_intensity = []
for i in range(len(mean_responses_pl_intensity)):
    mean_response_dict = {}
    for base, responses in mean_responses_pl_intensity[i].items():
        mean_response = sum(responses) / len(responses)
        mean_response_dict[base] = mean_response
    mean_response_data_pl_intensity.append(mean_response_dict)

# List of nucleotides for plotting
nucleotides = ['A', 'C', 'G', 'T']

# Preparing data for 3D plotting
X_76Intensity, Y_76Intensity, Z_76Intensity = prepare_data_for_3d_plot(mean_response_data_76Intensity, nucleotides)
X_pl_intensity, Y_pl_intensity, Z_pl_intensity = prepare_data_for_3d_plot(mean_response_data_pl_intensity, nucleotides)

# Plotting 3D surface for 76Intensity with modified Y-axis label and color bar
plot_3d_surface(X_76Intensity, Y_76Intensity, Z_76Intensity, '3D Surface Plot - Mean 76Intensity Response for Each Nucleotide at Each Position', nucleotides, 'Mean 76Intensity Response')
plt.savefig('3d surface position-76Intensity', dpi=900)

# Plotting 3D surface for PL intensity with modified Y-axis label and color bar
plot_3d_surface(X_pl_intensity, Y_pl_intensity, Z_pl_intensity, '3D Surface Plot - Mean PL Intensity for Each Nucleotide at Each Position', nucleotides, 'Mean PL Intensity')
plt.savefig('3d surface position-Intensity', dpi=900)



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors

def plot_3d_surface_with_integrated_heatmap(X, Y, Z, title, nucleotides, y_label):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    y_ticks = range(len(nucleotides))

    # Plot the 3D surface
    surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', edgecolor='none')

    # Settings for the 3D plot
    ax.set_xlabel('Position')
    ax.set_ylabel(y_label)
    ax.set_zlabel('Value')
    ax.set_title(title)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(nucleotides)
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Intensity')

    # Calculate top plane Z value for the heatmap
    Z_top = np.max(Z) * 2  # slightly above the highest point of the 3D surface

    # Normalize Z data for color mapping
    norm = mcolors.Normalize(vmin=np.min(Z), vmax=np.max(Z))
    colors = plt.cm.coolwarm(norm(Z))

    # Create the heatmap on the top plane
    X_top, Y_top = np.meshgrid(np.arange(X.shape[1]), np.arange(Y.shape[0]))
    ax.plot_surface(X_top, Y_top, Z_top*np.ones_like(X_top), facecolors=colors, shade=False)


# Example of how you would call this function, assuming you have the X, Y, Z data
plot_3d_surface_with_integrated_heatmap(X_76Intensity, Y_76Intensity, Z_76Intensity, '3D Surface Plot - Mean 76Intensity Response for Each Nucleotide at Each Position', nucleotides, 'Mean 76Intensity Response')
plt.savefig('3d surface position-76Intensity-join with heatmap', dpi=900)
plt.show()



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors

def plot_3d_surface_with_integrated_heatmap(X, Y, Z, title, nucleotides, y_label):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    y_ticks = range(len(nucleotides))

    # Plot the 3D surface
    surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', edgecolor='none')

    # Settings for the 3D plot
    ax.set_xlabel('Position')
    ax.set_ylabel(y_label)
    ax.set_zlabel('Value')
    ax.set_title(title)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(nucleotides)
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Intensity')

    # Calculate top plane Z value for the heatmap
    Z_top = np.max(Z) * 2  # slightly above the highest point of the 3D surface

    # Normalize Z data for color mapping
    norm = mcolors.Normalize(vmin=np.min(Z), vmax=np.max(Z))
    colors = plt.cm.coolwarm(norm(Z))

    # Create the heatmap on the top plane
    X_top, Y_top = np.meshgrid(np.arange(X.shape[1]), np.arange(Y.shape[0]))
    ax.plot_surface(X_top, Y_top, Z_top*np.ones_like(X_top), facecolors=colors, shade=False)

  

# Example of how you would call this function for the PL Intensity data
plot_3d_surface_with_integrated_heatmap(X_pl_intensity, Y_pl_intensity, Z_pl_intensity, '3D Surface Plot - Mean PL Intensity for Each Nucleotide at Each Position', nucleotides, 'Mean PL Intensity')
plt.savefig('3d surface position-94Intensity-join with heatmap', dpi=900)
plt.show()


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import Normalize
import numpy as np

def plot_3d_surface_with_integrated_heatmap(X, Y, Z, title, nucleotides, y_label, cmap='coolwarm', elev=30, azim=30):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    y_ticks = range(len(nucleotides))

    # Adjust normalization and colormap
    norm = Normalize(vmin=np.min(Z), vmax=np.max(Z))
    surf = ax.plot_surface(X, Y, Z, cmap=cmap, edgecolor='none', norm=norm)

    # Settings for the 3D plot
    ax.set_xlabel('Position')
    ax.set_ylabel(y_label)
    ax.set_zlabel('Value')
    ax.set_title(title)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(nucleotides)
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Intensity')

    # Set the viewing angle
    ax.view_init(elev=elev, azim=azim)

    # Calculate top plane Z value for the heatmap
    Z_top = np.max(Z) * 2  # slightly above the highest point of the 3D surface
    X_top, Y_top = np.meshgrid(np.arange(X.shape[1]), np.arange(Y.shape[0]))
    colors = plt.cm.get_cmap(cmap)(norm(Z))
    ax.plot_surface(X_top, Y_top, Z_top*np.ones_like(X_top), facecolors=colors, shade=False)

    plt.show()

# Example of how you would call this function for the 76Intensity data
plot_3d_surface_with_integrated_heatmap(X_76Intensity, Y_76Intensity, Z_76Intensity, '3D Surface Plot - Mean 76Intensity Response for Each Nucleotide at Each Position', nucleotides, 'Mean 76Intensity Response', elev=30, azim=40)


import plotly.graph_objects as go
import numpy as np

def plotly_3d_surface_with_heatmap(X, Y, Z, title, nucleotides):
    # Create the 3D surface plot
    fig = go.Figure(data=[go.Surface(z=Z, x=X[0], y=Y[:, 0], colorscale='Viridis')])

    # Adding heatmap on top plane
    Z_top = np.max(Z) * 1.05
    fig.add_trace(go.Surface(z=Z_top*np.ones(Z.shape), x=X[0], y=Y[:, 0], surfacecolor=Z, colorscale='Viridis', showscale=False))

    # Update plot layout
    fig.update_layout(title=title, autosize=True,
                      scene=dict(
                          xaxis_title='Position',
                          yaxis_title='Nucleotide Index',
                          zaxis_title='Value',
                          xaxis=dict(nticks=10, range=[np.min(X), np.max(X)]),
                          yaxis=dict(nticks=10, range=[0, len(nucleotides)-1], ticktext=nucleotides, tickvals=list(range(len(nucleotides)))),
                          zaxis=dict(nticks=10),
                      ))

    # Save the plot as an HTML file
    fig.write_html('3d_plot.html')

# Assuming X_76Intensity, Y_76Intensity, Z_76Intensity are numpy arrays formatted correctly
plotly_3d_surface_with_heatmap(X_76Intensity, Y_76Intensity, Z_76Intensity, '3D Surface Plot - Mean 76Intensity', nucleotides=['A', 'C', 'G', 'T'])
