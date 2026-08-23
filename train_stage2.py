import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import time

X_train = pd.read_csv('data/X_train_stage2.csv')
y_train = pd.read_csv('data/y_train_stage2.csv').values.ravel()

print("Training data loaded:", X_train.shape)
print("Starting training... this may take a few minutes")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    random_state=42,
    n_jobs=-1,
    class_weight='balanced'  # important here - some attack types have very few examples
)

start_time = time.time()
model.fit(X_train, y_train)
end_time = time.time()

print(f"\nTraining complete! Took {end_time - start_time:.2f} seconds")

joblib.dump(model, 'stage2_model.pkl')
print("Model saved as stage2_model.pkl")