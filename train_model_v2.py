import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
import joblib
import time

X_train = pd.read_csv('data/X_train.csv')
y_train = pd.read_csv('data/y_train.csv').values.ravel()

print("Original training data:", X_train.shape)
print("Original class counts:")
print(pd.Series(y_train).value_counts())

# SMOTE creates synthetic examples of the minority class (Attack)
# to give the model more to learn from
print("\nApplying SMOTE... this may take a few minutes")
smote = SMOTE(random_state=42, sampling_strategy=0.5)  # boost Attack to 50% of Normal count
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

print("Balanced training data:", X_train_balanced.shape)
print("Balanced class counts:")
print(pd.Series(y_train_balanced).value_counts())

# Train the model on the balanced data
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    random_state=42,
    n_jobs=-1,
    class_weight='balanced'
)

start_time = time.time()
model.fit(X_train_balanced, y_train_balanced)
end_time = time.time()

print(f"\nTraining complete! Took {end_time - start_time:.2f} seconds")

joblib.dump(model, 'stage1_model_v2.pkl')
print("Model saved as stage1_model_v2.pkl")