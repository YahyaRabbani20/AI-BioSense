import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Read the data from the Excel file
df = pd.read_excel("133DNAfromDiffLeng-Final.xlsx")

# Extract the k-mers of length 10 from each DNA sequence
k = 3
df['kmers'] = df['DNA'].apply(lambda x: [x[i:i+k] for i in range(len(x)-k+1)])

# Flatten the list of k-mers
kmers_list = np.concatenate(df['kmers'].values)

# Create a DataFrame with the k-mers and their counts
kmer_counts = pd.Series(kmers_list).value_counts().reset_index()
kmer_counts.columns = ['kmer', 'count']

def plot_and_cluster(target):
    # Calculate the mean of response for each k-mer
    kmer_means = []
    for kmer in kmer_counts['kmer']:
        kmers_with_kmer = df[df['kmers'].apply(lambda x: kmer in x)]
        kmer_means.append(kmers_with_kmer[target].mean())

    # Add the k-mer means to the k-mer counts DataFrame
    kmer_counts[target] = kmer_means

    # # Plot the response for each k-mer
    # colors = ['red' if x > 70 else 'blue' for x in kmer_counts[target]]
    # plt.figure(figsize=(40, 6))
    # plt.bar(kmer_counts['kmer'], kmer_counts[target], color=colors)
    # plt.xticks(rotation=90, fontsize=10)
    # plt.xlabel('K-mer')
    # plt.ylabel(target)
    # plt.title(f'{target} by k-mer')
    # plt.savefig(f'K-mer {target}0.png', dpi=300, bbox_inches='tight')
    # plt.show()

    # Create a DataFrame with the k-mers and their occurrence frequencies
    kmer_freq = pd.DataFrame(pd.Series(kmers_list).value_counts()).reset_index()
    kmer_freq.columns = ['kmer', 'freq']

    # Calculate the mean response value for each k-mer and add it to the frequency DataFrame
    kmer_means = []
    for kmer in kmer_freq['kmer']:
        kmers_with_kmer = df[df['kmers'].apply(lambda x: kmer in x)]
        kmer_means.append(kmers_with_kmer[target].mean())
    kmer_freq[target] = kmer_means

    # Determine the optimal number of clusters using Elbow method
    distortions = []
    K = range(1,10)
    for k in K:
        kmeanModel = KMeans(n_clusters=k, random_state=42).fit(kmer_freq[['freq', target]])
        distortions.append(kmeanModel.inertia_)

    # Plotting the elbow plot
    plt.figure(figsize=(8,6))
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method showing the optimal k')
    plt.show()

    # Use k-means clustering to cluster the k-mers based on their occurrence frequency
    N = 3  # number of clusters (replace with optimal number of clusters based on elbow plot)
    kmeans = KMeans(n_clusters=N, random_state=42).fit(kmer_freq[['freq', target]])

    # Add the cluster labels to the k-mer frequency DataFrame
    kmer_freq['cluster'] = kmeans.labels_
    # Plot the frequency vs mean response for each k-mer
    plt.figure(figsize=(10, 6))
    plt.scatter(kmer_freq['freq'], kmer_freq[target], alpha=0.5, color='green')
    plt.xlabel('Frequency of k-mer')
    plt.ylabel(f'Mean {target} Value')
    plt.title('Scatter Plot of Frequency vs. Mean Response for k-mers')
    plt.grid(True)
    plt.show()

    # Plot the clusters and their corresponding mean response values
    plt.figure(figsize=(8, 6))
    for cluster in range(N):
        plt.scatter(kmer_freq[kmer_freq['cluster'] == cluster]['freq'], kmer_freq[kmer_freq['cluster'] == cluster][target], label=f'Cluster {cluster}')
    plt.xlabel('Occurrence frequency')
    plt.ylabel(f'Mean {target}(%)')
    plt.title('K-mer clusters')
    plt.legend()
    plt.savefig(f'clusters result for kmer_{target}.png', dpi=900, bbox_inches='tight')
    plt.show()

# Call the function for both 76Intensity and PL intensity
plot_and_cluster('(7,6) Intensity')
plot_and_cluster('(9,4) Intensity')


def report_high_response_kmers(target, freq_threshold, response_threshold):
    # Create a DataFrame with the k-mers and their occurrence frequencies
    kmer_freq = pd.DataFrame(pd.Series(kmers_list).value_counts()).reset_index()
    kmer_freq.columns = ['kmer', 'freq']

    # Calculate the mean response value for each k-mer and add it to the frequency DataFrame
    kmer_means = []
    for kmer in kmer_freq['kmer']:
        kmers_with_kmer = df[df['kmers'].apply(lambda x: kmer in x)]
        kmer_means.append(kmers_with_kmer[target].mean())
    kmer_freq[target] = kmer_means

    # Filter out the k-mers that meet the frequency and response thresholds
    high_freq_high_response_kmers = kmer_freq[(kmer_freq['freq'] >= freq_threshold) & (kmer_freq[target] >= response_threshold)]

    print(f"K-mers with high response and high frequency for {target}:")
    print(high_freq_high_response_kmers)

# Set the threshold values for frequency and response
freq_threshold = 45
response_threshold = 10

# Call the function for both 76Intensity and PL intensity
report_high_response_kmers('(7,6) Intensity', freq_threshold, response_threshold)
report_high_response_kmers('(9,4) Intensity', freq_threshold, response_threshold)



def report_high_response_kmers(freq_threshold, response_threshold_76Intensity, response_threshold_pl):
    plt.rcParams.update({'font.size': 20})
    # Calculate the mean response value for each k-mer and add it to the frequency DataFrame for both targets
    targets = ['(7,6) Intensity', '(9,4) Intensity']
    response_thresholds = {'(7,6) Intensity': response_threshold_76Intensity, '(9,4) Intensity': response_threshold_pl}
    kmer_freq = {}
    for target in targets:
        kmer_freq[target] = pd.DataFrame(pd.Series(kmers_list).value_counts()).reset_index()
        kmer_freq[target].columns = ['kmer', 'freq']
        kmer_means = []
        for kmer in kmer_freq[target]['kmer']:
            kmers_with_kmer = df[df['kmers'].apply(lambda x: kmer in x)]
            kmer_means.append(kmers_with_kmer[target].mean())
        kmer_freq[target][target] = kmer_means

    # Filter out the k-mers that meet the frequency and response thresholds for both targets
    high_freq_high_response_kmers = {}
    for target in targets:
        high_freq_high_response_kmers[target] = kmer_freq[target][(kmer_freq[target]['freq'] >= freq_threshold) & (kmer_freq[target][target] >= response_thresholds[target])]

    # Find the common k-mers for both targets
    common_kmers = pd.merge(high_freq_high_response_kmers['(7,6) Intensity'], high_freq_high_response_kmers['(9,4) Intensity'], on='kmer', suffixes=('_76Intensity', '_pl_intensity'))

    print("Common k-mers with high response and high frequency for both 76Intensity and PL intensity:")
    print(common_kmers)

    # Save the DataFrame to Excel
    common_kmers.to_excel('common_kmers.xlsx', index=False)

    # Plot the results
    fig, ax1 = plt.subplots(figsize=(14, 8))
    # Increase default font size
    plt.rcParams.update({'font.size': 18})
    for i in range(len(common_kmers)):
        ax1.scatter(common_kmers['freq_76Intensity'][i], common_kmers['(7,6) Intensity'][i], color='blue')
        ax1.text(common_kmers['freq_76Intensity'][i], common_kmers['(7,6) Intensity'][i], common_kmers['kmer'][i], fontsize=12, ha='right')
        ax1.set_xlabel('Occurrence Frequency', fontsize=20)
        ax1.set_ylabel('Mean 76Intensity(%)', color='blue', fontsize=20)
        ax1.tick_params(axis='y', labelcolor='blue', labelsize=18)
        
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    for i in range(len(common_kmers)):
        ax2.scatter(common_kmers['freq_pl_intensity'][i], common_kmers['(9,4) Intensity'][i], color='red')
        ax2.text(common_kmers['freq_pl_intensity'][i], common_kmers['(9,4) Intensity'][i], common_kmers['kmer'][i], fontsize=12, ha='right')
        ax2.set_ylabel('Mean PL intensity(%)', color='red', fontsize=20)  
        ax2.tick_params(axis='y', labelcolor='red',  labelsize=18)
        
    plt.tight_layout()
    plt.savefig('common_3mers.png', dpi=900, bbox_inches='tight')
    plt.show()

# Set the threshold values for frequency and response
freq_threshold =45
response_threshold_76Intensity =10
response_threshold_pl=10

# Call the function
report_high_response_kmers(freq_threshold, response_threshold_76Intensity, response_threshold_pl)


import pandas as pd
from itertools import product

import pandas as pd
from itertools import product, combinations

# Load the Excel file
df_kmers = pd.read_excel('common_3kmers.xlsx')

# Access the 'kmer' column and convert it to a list
k_mers = df_kmers['kmer'].tolist()

# Desired sequence lengths
target_lengths = [9,12,15]

# Initialize an empty list to store the sequences
sequences = []

# Function to generate sequences by combining k-mers of varying lengths
def generate_sequences(k_mers, target_length):
    # Explore combinations of k-mers, starting with 1 up to a maximum count that potentially forms the desired length
    max_kmer_count = target_length // min(len(k) for k in k_mers) + 1
    for num_kmers in range(1, max_kmer_count):
        # Check every possible combination of k-mers of size num_kmers
        for combo in combinations(k_mers, num_kmers):
            # Generate all sequences that can be made with this combination of k-mers
            for permutation in product(*([combo] * num_kmers)):
                sequence = ''.join(permutation)[:target_length]
                if len(sequence) == target_length:
                    sequences.append(sequence)

# Generate sequences for each target length
for length in target_lengths:
    generate_sequences(k_mers, length)

# Remove duplicates and create DataFrame
# Remove duplicates by converting the list to a set
unique_sequences = set(sequences)

# Convert the set back to a list if needed for further operations
unique_sequences_list = list(unique_sequences)

# Create DataFrame from the list of unique sequences
sequences_df = pd.DataFrame(unique_sequences_list, columns=['Sequence'])
# Save the DataFrame to an Excel file
sequences_df.to_excel('sequences_generate_from_3-mer.xlsx', index=False)

