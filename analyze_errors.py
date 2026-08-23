import pandas as pd
import joblib

# Load test data and original labels (before we simplified to Normal/Attack)
X_test = pd.read_csv('data/X_test.csv')
y_test = pd.read_csv('data/y_test.csv').values.ravel()
model = joblib.load('stage1_model.pkl')

# We also need the ORIGINAL detailed labels (DDoS, PortScan, etc.) for the test rows
# Let's reload the full cleaned data and match it up
df = pd.read_csv('data/cleaned_data.csv')
df['Binary_Label'] = df['Label'].apply(lambda x: 'Normal' if x == 'BENIGN' else 'Attack')

from sklearn.model_selection import train_test_split
X = df.drop(columns=['Label', 'Binary_Label'])
y_binary = df['Binary_Label']
y_detailed = df['Label']

# Same split settings as before, so we get matching rows
_, X_test_check, _, y_test_detailed = train_test_split(
    X, y_detailed, test_size=0.2, random_state=42, stratify=y_binary
)

# Make predictions
y_pred = model.predict(X_test)

# Find the rows where the model WRONGLY said "Normal" but it was actually an attack
missed = (y_test == 'Attack') & (y_pred == 'Normal')

print("Total missed attacks:", missed.sum())
print("\nBreakdown by actual attack type:")
print(y_test_detailed[missed].value_counts())

# Also check the false alarms - what did it wrongly flag as Attack?
false_alarms = (y_test == 'Normal') & (y_pred == 'Attack')
print("\nTotal false alarms:", false_alarms.sum())