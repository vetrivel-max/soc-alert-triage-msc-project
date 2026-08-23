import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Load data
df = pd.read_csv('data/own_dataset.csv', low_memory=False)
print("Original shape:", df.shape)

# Keep a copy of IP addresses for DISPLAY purposes only (not used in training)
ip_data = df[['src_ip', 'dst_ip', 'protocol']].copy()

# Drop identifier/non-numeric columns that shouldn't be used as ML features
drop_cols = [
    'id', 'expiration_id', 'src_ip', 'src_mac', 'src_oui', 'dst_ip', 'dst_mac', 'dst_oui',
    'src_port', 'dst_port', 'vlan_id', 'tunnel_id',
    'bidirectional_first_seen_ms', 'bidirectional_last_seen_ms',
    'src2dst_first_seen_ms', 'src2dst_last_seen_ms',
    'dst2src_first_seen_ms', 'dst2src_last_seen_ms',
    'application_name', 'application_category_name', 'application_is_guessed',
    'requested_server_name', 'client_fingerprint', 'server_fingerprint',
    'user_agent', 'content_type'
]
df = df.drop(columns=[c for c in drop_cols if c in df.columns])

print("After dropping identifier columns:", df.shape)

# Handle missing/infinite values
df.replace([np.inf, -np.inf], np.nan, inplace=True)
valid_idx = df.dropna().index
df = df.loc[valid_idx]
ip_data = ip_data.loc[valid_idx]

print("After cleaning:", df.shape)

print("\nLabel counts after cleaning:")
print(df['Label'].value_counts())

# Features and target
X = df.drop(columns=['Label'])
y = df['Label']

# Split into train/test, keeping IP metadata aligned with the same split
X_train, X_test, y_train, y_test, ip_train, ip_test = train_test_split(
    X, y, ip_data, test_size=0.2, random_state=42, stratify=y
)

print("\nTraining set size:", X_train.shape)
print("Testing set size:", X_test.shape)

# Save everything
X_train.to_csv('data/X_train_own.csv', index=False)
X_test.to_csv('data/X_test_own.csv', index=False)
y_train.to_csv('data/y_train_own.csv', index=False)
y_test.to_csv('data/y_test_own.csv', index=False)
ip_test.to_csv('data/ip_test_own.csv', index=False)

print("\nAll files saved (including IP metadata for display)!")