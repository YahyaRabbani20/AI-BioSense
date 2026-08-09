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
    #plt.show()

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


# Matplotlib plots are already using 'coolwarm' colormap
plot_3d_surface(X_76Intensity, Y_76Intensity, Z_76Intensity, '3D Surface Plot - Mean 76Intensity Response for Each Nucleotide at Each Position', nucleotides, 'Mean 76Intensity Response')
plt.savefig('3d_surface_position-76Intensity.png', dpi=900)

plot_3d_surface(X_pl_intensity, Y_pl_intensity, Z_pl_intensity, '3D Surface Plot - Mean 94Intensity for Each Nucleotide at Each Position', nucleotides, 'Mean 94Intensity')
plt.savefig('3d_surface_position-94Intensity.png', dpi=900)


import plotly.graph_objects as go
import pandas as pd
import numpy as np



# Function to create interactive 3D surface plot with Plotly, and return the figure object
def plotly_3d_surface(X, Y, Z, title, nucleotides, y_label):
    # Custom color scale to mimic 'coolwarm'
    coolwarm_colorscale = [
        [0.0, 'rgb(59,76,192)'],
        [0.5, 'rgb(220,220,220)'],
        [1.0, 'rgb(180,4,38)']
    ]
    
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale=coolwarm_colorscale)])
    fig.update_layout(title=title, autosize=True,
                      scene=dict(
                          xaxis_title='Position',
                          yaxis_title=y_label,
                          zaxis_title='Value',
                          yaxis=dict(
                              tickvals=list(range(len(nucleotides))),
                              ticktext=nucleotides
                          )
                      ))
    return fig

# ... [Use this function to plot your data and get the figure object] ...

fig_76Intensity = plotly_3d_surface(X_76Intensity, Y_76Intensity, Z_76Intensity, 'Interactive 3D Plot - Mean 76Intensity Response for Each Nucleotide at Each Position', nucleotides, 'Mean 76Intensity Response')
fig_pl_intensity = plotly_3d_surface(X_pl_intensity, Y_pl_intensity, Z_pl_intensity, 'Interactive 3D Plot - Mean 94 Intensity for Each Nucleotide at Each Position', nucleotides, 'Mean 94 Intensity')

# Save the plots as HTML files
fig_76Intensity.write_html("76Intensity_plot.html")
fig_pl_intensity.write_html("94_intensity_plot.html")
