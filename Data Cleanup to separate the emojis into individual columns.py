import pandas as pd
import re
from collections import defaultdict

# Function to extract emojis and their counts from a text
def extract_emojis_counts(text):
    text = str(text)  # Convert to string in case of non-string types
    emoji_count_dict = defaultdict(int)
    emoji_count_pairs = re.findall(r'([^\s\d]+) (\d+)', text)
    for emoji, count in emoji_count_pairs:
        emoji_count_dict[emoji] += int(count)
    return emoji_count_dict

# Load the Excel file, treating the first row as data
file_path = 'XXX'  # Replace with your file path
df = pd.read_excel(file_path, header=None)

# Extracting emojis and their counts for all rows
emoji_data = df.iloc[:, 8].apply(extract_emojis_counts)  # Adjust the column index as needed

# Identifying all unique emojis
unique_emojis = set()
for row in emoji_data:
    unique_emojis.update(row.keys())

# Alternative DataFrame construction from a list of dictionaries
emoji_counts_list = [extract_emojis_counts(row) for row in df.iloc[:, 8]]
emoji_counts_df = pd.DataFrame(emoji_counts_list)
emoji_counts_df.fillna(0, inplace=True)
emoji_counts_df = emoji_counts_df.astype(int)

# Concatenate the original DataFrame with the new emoji counts DataFrame
result_df = pd.concat([df, emoji_counts_df], axis=1)

# Saving the modified DataFrame back into an Excel file
modified_file_path = 'XXX'  # Replace with your desired file path
result_df.to_excel(modified_file_path, index=False)


