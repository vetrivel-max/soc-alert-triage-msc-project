import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

X_test = pd.read_csv('data/X_test_stage2.csv')
y_test = pd.read_csv('data/y_test_stage2.csv').values.ravel()
model = joblib.load('stage2_model.pkl')

print("Test data loaded:", X_test.shape)
print("Making predictions...")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\nOverall Accuracy: {accuracy * 100:.2f}%")

print("\nDetailed report (per attack type):")
print(classification_report(y_test, y_pred))