import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import time

X_train = pd.read_csv('data/X_train_own.csv')
y_train = pd.read_csv('data/y_train_own.csv').values.ravel()

print("Training data loaded:", X_train.shape)
print("Starting training...")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    random_state=42,
    n_jobs=-1,
    class_weight='balanced'
)

start_time = time.time()
model.fit(X_train, y_train)
end_time = time.time()

print(f"Training complete! Took {end_time - start_time:.2f} seconds")

joblib.dump(model, 'own_model.pkl')
print("Model saved as own_model.pkl")