# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 11:48:56 2024

@author: yahya
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Define a function to calculate the response for each base in a given DNA sequence
def calculate_base_responses(dna_sequence, response, mean_responses):
    # Calculate the length of the DNA sequence
    dna_length = len(dna_sequence)

    # Divide the response by the length of the DNA sequence
    normalized_response = response / dna_length

    # Loop through each position in the DNA sequence
    for i, base in enumerate(dna_sequence):
        # If this is the first base for this position, add a new dictionary to the list
        if len(mean_responses) <= i:
            mean_responses.append({})

        # If the base is not already in the dictionary for this position, initialize its response to zero
        if base not in mean_responses[i]:
            mean_responses[i][base] = []

        # Add the normalized response to the response for this base at this position
        mean_responses[i][base].append(normalized_response)

    return mean_responses

# Load the data from an Excel file
df = pd.read_excel("133DNAfromDiffLeng-Final.xlsx")

# Create a list to store the mean responses for each nucleotide at each position for 76Intensity
mean_responses_76Intensity = []

# Create a list to store the mean responses for each nucleotide at each position for PL intensity
mean_responses_94Intensity = []

# Iterate through each row of the DataFrame and calculate the response for each base at each position
for index, row in df.iterrows():
    dna_sequence = row['DNA']  # Get the DNA sequence from the 'DNA' column of the row
    response_76Intensity = row['(7,6) Intensity']  # Get the 76Intensity response from the '(7,6) Intensity' column of the row
    response_94Intensity = row['(9,4) Intensity']  # Get the PL intensity response from the '(9,4) Intensity' column of the row

    # Calculate the base responses for 76Intensity
    mean_responses_76Intensity = calculate_base_responses(dna_sequence, response_76Intensity, mean_responses_76Intensity)

    # Calculate the base responses for PL intensity
    mean_responses_94Intensity = calculate_base_responses(dna_sequence, response_94Intensity, mean_responses_94Intensity)

# Calculate the mean response for each nucleotide at each position for 76Intensity
mean_response_data_76Intensity = []
for i in range(len(mean_responses_76Intensity)):
    mean_response_dict = {}
    for base, responses in mean_responses_76Intensity[i].items():
        mean_response = sum(responses) / len(responses)
        mean_response_dict[base] = mean_response
    mean_response_data_76Intensity.append(mean_response_dict)

# Calculate the mean response for each nucleotide at each position for PL intensity
mean_response_data_94Intensity = []
for i in range(len(mean_responses_94Intensity)):
    mean_response_dict = {}
    for base, responses in mean_responses_94Intensity[i].items():
        mean_response = sum(responses) / len(responses)
        mean_response_dict[base] = mean_response
    mean_response_data_94Intensity.append(mean_response_dict)

# Convert the mean response data to DataFrames for 76Intensity and PL intensity
mean_response_df_76Intensity = pd.DataFrame(mean_response_data_76Intensity)
mean_response_df_94Intensity = pd.DataFrame(mean_response_data_94Intensity)

# Create a heatmap of the mean response data for 76Intensity
plt.figure(figsize=(10, 6))
sns.heatmap(mean_response_df_76Intensity, cmap='coolwarm', annot=True, cbar_kws={'label': 'Mean Intensity Change(%)'},yticklabels=np.arange(1, len(mean_responses_76Intensity) + 1))
plt.xlabel('Nucleotide')
plt.ylabel('Position')
plt.title('Mean (7,6)Intensity Change for Each Nucleotide at Each Position')
plt.savefig('Mean_(7,6) Intensity_for_Each_Nucleotide_at_Each_Position', dpi=900, bbox_inches='tight')
plt.show()


# Create a heatmap of the mean response data for PL intensity
plt.figure(figsize=(10, 6))
sns.heatmap(mean_response_df_94Intensity, cmap='coolwarm', annot=True, cbar_kws={'label': 'Mean Intensity Change(%)'},yticklabels=np.arange(1, len(mean_responses_76Intensity) + 1))
plt.xlabel('Nucleotide')
plt.ylabel('Position')
plt.title('Mean (9,4) Intensity Change for Each Nucleotide at Each Position')
plt.savefig('Mean_(9,4) Intensity_for_Each_Nucleotide_at_Each_Position', dpi=900, bbox_inches='tight')
plt.show()







import random
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Adjust the range for sequence length from a minimum of 8 to a maximum of 30.
min_sequence_length = 8
max_sequence_length = 14

# Initialize a set to store the sequences (sets only allow unique elements).
sequences = set()

# Initialize a counter to limit the number of attempts to generate a unique sequence.
max_attempts = 100000
attempts = 0

# Generate 500 unique sequences with varying lengths.
while len(sequences) < 100000 and attempts < max_attempts:
    sequence_length = random.randint(min_sequence_length, max_sequence_length)
    sequence = ""
    for i in range(sequence_length):
        # Adjust for the range of positions available in mean_response_df_76Intensity and mean_response_df_94Intensity.
        # Using modulo to wrap around if i exceeds the dataframe index.
        position = i % len(mean_response_df_76Intensity)
        
        top_two_bases_76Intensity = mean_response_df_76Intensity.iloc[position].nlargest(2).index.tolist()
        top_two_bases_94Intensity = mean_response_df_94Intensity.iloc[position].nlargest(2).index.tolist()

        # Find the intersection of the two base lists
        common_bases = list(set(top_two_bases_76Intensity) & set(top_two_bases_94Intensity))

        if common_bases:
            sequence += random.choice(common_bases)
        else:
            all_bases = set(top_two_bases_76Intensity + top_two_bases_94Intensity)
            base_values_76Intensity = {base: mean_response_df_76Intensity.iloc[position, base] for base in all_bases}
            base_values_94Intensity = {base: mean_response_df_94Intensity.iloc[position, base] for base in all_bases}
            max_value_base_76Intensity = max(base_values_76Intensity, key=lambda x: base_values_76Intensity[x])
            max_value_base_94Intensity = max(base_values_94Intensity, key=lambda x: base_values_94Intensity[x])
            sequence += random.choice([max_value_base_76Intensity, max_value_base_94Intensity])
            
    sequences.add(sequence)
    attempts += 1

# Calculate the sum of responses for each sequence.
sum_responses_76Intensity = []
sum_responses_94Intensity = []

for sequence in sequences:
    sum_response_76Intensity = 0
    sum_response_94Intensity = 0
    for i, base in enumerate(sequence):
        position = i % len(mean_response_df_76Intensity)
        sum_response_76Intensity += mean_response_df_76Intensity.loc[position, base]
        sum_response_94Intensity += mean_response_df_94Intensity.loc[position, base]

    sum_responses_76Intensity.append(sum_response_76Intensity)
    sum_responses_94Intensity.append(sum_response_94Intensity)

# Convert the sequences set to a list to preserve the order of sequences.
sequences_list = list(sequences)

# Create a DataFrame with the sequences and their corresponding sum of responses.
df_sequences = pd.DataFrame({
    'Sequence': sequences_list,
    'Sum of 76Intensity Responses': sum_responses_76Intensity,
    'Sum of PL Intensity Responses': sum_responses_94Intensity
})

# Export the DataFrame to an Excel file.
df_sequences.to_excel("sequences_with_High.xlsx", index=False)

# Plotting
fig, ax = plt.subplots(figsize=(6, 6))
bar_width = 0.35
num_sequences = len(df_sequences)
index = np.arange(num_sequences)
bar_colors = ['green', 'black']

ax.bar(index, df_sequences['Sum of 76Intensity Responses'], bar_width, label='Sum of 76Intensity Responses', color=bar_colors[0])
ax.bar(index + bar_width, df_sequences['Sum of PL Intensity Responses'], bar_width, label='Sum of PL Intensity Responses', color=bar_colors[1])

ax.set_xticks(index + bar_width / 4)
ax.set_xticklabels(df_sequences['Sequence'], rotation=90, horizontalalignment='right')
ax.set_title('Sum of Responses for Each Sequence')
ax.set_xlabel('New DNA Sequences')
ax.set_ylabel('Sum of Responses')
ax.legend()

plt.savefig("sequences.jpg", format='jpeg', dpi=300, bbox_inches='tight')
plt.show()


# Correct the column names in the calculation for 'Total Intensity Response'
if 'Sum of 76Intensity Responses' in df_sequences and 'Sum of PL Intensity Responses' in df_sequences:
    df_sequences['Total Intensity Response'] = df_sequences['Sum of 76Intensity Responses'] + df_sequences['Sum of PL Intensity Responses']
    print("Total Intensity Response column added successfully!")
else:
    print("Error: Necessary columns are missing.")

# Now proceed with sorting and selecting the top 10 percent
df_sequences_sorted = df_sequences.sort_values(by='Total Intensity Response', ascending=False)
top_10_percent_count = int(len(df_sequences_sorted) * 0.1)
top_10_percent_sequences = df_sequences_sorted.head(top_10_percent_count)

# Export these top 10 percent entries to an Excel file
top_10_percent_sequences.to_excel("top_10_percent_sequences_with_high_responses.xlsx", index=False)

# Optionally, print to inspect the top 10 percent data
print(top_10_percent_sequences)




import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Adjust the range for sequence length from a minimum of 8 to a maximum of 14.
min_sequence_length = 8
max_sequence_length = 14

# Initialize a set to store the sequences (sets only allow unique elements).
sequences = set()

# Initialize a counter to limit the number of attempts to generate a unique sequence.
max_attempts = 10000
attempts = 0

# Generate 50000 unique sequences with varying lengths.
while len(sequences) < 10000 and attempts < max_attempts:
    sequence_length = random.randint(min_sequence_length, max_sequence_length)
    sequence = ""
    for i in range(sequence_length):
        # Adjust for the range of positions available in mean_response_df_76Intensity and mean_response_df_94Intensity.
        # Using modulo to wrap around if i exceeds the dataframe index.
        position = i % len(mean_response_df_76Intensity)
        
        # Get the base with the minimum response at this position from both dataframes
        min_base_76Intensity = mean_response_df_76Intensity.iloc[position].idxmin()
        min_base_94Intensity = mean_response_df_94Intensity.iloc[position].idxmin()
        
        # Choose randomly between the two minimum bases
        sequence += random.choice([min_base_76Intensity, min_base_94Intensity])
            
    sequences.add(sequence)
    attempts += 1

# Calculate the sum of responses for each sequence.
sum_responses_76Intensity = []
sum_responses_94Intensity = []

for sequence in sequences:
    sum_response_76Intensity = 0
    sum_response_94Intensity = 0
    for i, base in enumerate(sequence):
        position = i % len(mean_response_df_76Intensity)
        sum_response_76Intensity += mean_response_df_76Intensity.at[position, base]
        sum_response_94Intensity += mean_response_df_94Intensity.at[position, base]

    sum_responses_76Intensity.append(sum_response_76Intensity)
    sum_responses_94Intensity.append(sum_response_94Intensity)

# Convert the sequences set to a list to preserve the order of sequences.
sequences_list = list(sequences)

# Create a DataFrame with the sequences and their corresponding sum of responses.
df_sequences = pd.DataFrame({
    'Sequence': sequences_list,
    'Sum of 76Intensity Min Responses': sum_responses_76Intensity,
    'Sum of PL Intensity Min Responses': sum_responses_94Intensity
})

# Export the DataFrame to an Excel file.
df_sequences.to_excel("sequences_with_Min.xlsx", index=False)

# Plotting
fig, ax = plt.subplots(figsize=(6, 6))
bar_width = 0.35
num_sequences = len(df_sequences)
index = np.arange(num_sequences)
bar_colors = ['blue', 'red']

ax.bar(index, df_sequences['Sum of 76Intensity Min Responses'], bar_width, label='Sum of 76Intensity Min Responses', color=bar_colors[0])
ax.bar(index + bar_width, df_sequences['Sum of PL Intensity Min Responses'], bar_width, label='Sum of PL Intensity Min Responses', color=bar_colors[1])

ax.set_xticks(index + bar_width / 4)
ax.set_xticklabels(df_sequences['Sequence'], rotation=90, horizontalalignment='right')
ax.set_title('Minimum Sum of Responses for Each Sequence')
ax.set_xlabel('New DNA Sequences')
ax.set_ylabel('Sum of Responses')
ax.legend()

plt.savefig("sequences_min.jpg", format='jpeg', dpi=300, bbox_inches='tight')
