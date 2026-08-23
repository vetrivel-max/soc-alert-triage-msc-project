import pandas as pd
from sklearn.model_selection import train_test_split

# Load the cleaned data
df = pd.read_csv('data/cleaned_data.csv')

# Keep only Attack rows (remove BENIGN/Normal)
attack_df = df[df['Label'] != 'BENIGN'].copy()

# Merge all Web Attack subtypes into one single category
attack_df['Label'] = attack_df['Label'].apply(
    lambda x: 'Web Attack' if 'Web Attack' in x else x
)

print("Total attack rows:", attack_df.shape[0])
print("\nAttack type counts (after merging Web Attacks):")
print(attack_df['Label'].value_counts())

# Features (X) and target (y)
X = attack_df.drop(columns=['Label'])
y = attack_df['Label']

# Split into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\nTraining set size:", X_train.shape)
print("Testing set size:", X_test.shape)

# Save the splits
X_train.to_csv('data/X_train_stage2.csv', index=False)
X_test.to_csv('data/X_test_stage2.csv', index=False)
y_train.to_csv('data/y_train_stage2.csv', index=False)
y_test.to_csv('data/y_test_stage2.csv', index=False)

print("\nAll Stage 2 files saved!")