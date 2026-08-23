import pandas as pd

y_train = pd.read_csv('data/y_train.csv')
df = pd.read_csv('data/cleaned_data.csv')

# How many Bot examples exist in the whole dataset?
print("Bot examples in full dataset:")
print(df[df['Label'] == 'Bot'].shape[0])

print("\nCompare to biggest classes:")
print("BENIGN:", df[df['Label'] == 'BENIGN'].shape[0])
print("DoS Hulk:", df[df['Label'] == 'DoS Hulk'].shape[0])