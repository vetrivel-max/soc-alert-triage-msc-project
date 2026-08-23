import pandas as pd
from sklearn.model_selection import train_test_split

# Load the cleaned data
df = pd.read_csv('data/cleaned_data.csv')
print("Loaded data:", df.shape)

# Create a new column: Normal vs Attack
df['Binary_Label'] = df['Label'].apply(lambda x: 'Normal' if x == 'BENIGN' else 'Attack')

print("\nBinary label counts:")
print(df['Binary_Label'].value_counts())

# Separate features (X) from the answer/target (y)
# X = everything the model looks at to make a decision
# y = the correct answer we want it to learn to predict
X = df.drop(columns=['Label', 'Binary_Label'])
y = df['Binary_Label']

# Split into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\nTraining set size:", X_train.shape)
print("Testing set size:", X_test.shape)

# Save these splits so we don't have to redo this every time
X_train.to_csv('data/X_train.csv', index=False)
X_test.to_csv('data/X_test.csv', index=False)
y_train.to_csv('data/y_train.csv', index=False)
y_test.to_csv('data/y_test.csv', index=False)

print("\nAll files saved! Ready for training.")