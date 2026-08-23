import pandas as pd

df = pd.read_csv('data/own_dataset.csv')

print("Shape (rows, columns):", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nLabel counts:")
print(df['Label'].value_counts())
print("\nFirst few rows:")
print(df.head())