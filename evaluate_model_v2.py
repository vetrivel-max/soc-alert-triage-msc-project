import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

X_test = pd.read_csv('data/X_test.csv')
y_test = pd.read_csv('data/y_test.csv').values.ravel()
model = joblib.load('stage1_model_v2.pkl')

print("Test data loaded:", X_test.shape)
print("Making predictions...")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\nOverall Accuracy: {accuracy * 100:.2f}%")

print("\nDetailed report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))