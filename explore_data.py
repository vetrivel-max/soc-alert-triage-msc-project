import pandas as pd
import glob
import numpy as np

# Load and combine all files
csv_files = glob.glob('data/*.csv')
df_list = [pd.read_csv(file) for file in csv_files]
df = pd.concat(df_list, ignore_index=True)

# Clean column names (remove extra spaces)
df.columns = df.columns.str.strip()

print("Before cleaning:", df.shape)

# Step 1: Replace infinite values with NaN (empty)
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Step 2: Remove rows with any missing values
df.dropna(inplace=True)

# Step 3: Remove duplicate rows
df.drop_duplicates(inplace=True)

print("After cleaning:", df.shape)

# Save the cleaned data so we don't have to redo this every time
df.to_csv('data/cleaned_data.csv', index=False)
print("\nCleaned data saved to data/cleaned_data.csv")

print("\nFinal label counts:")
print(df['Label'].value_counts())