import pandas as pd
import joblib
import pickle

# Load everything
model = joblib.load('stage1_model.pkl')
X_test = pd.read_csv('data/X_test.csv')
y_test = pd.read_csv('data/y_test.csv').values.ravel()

with open('shap_explainer.pkl', 'rb') as f:
    explainer = pickle.load(f)

# Pick one specific attack sample to explain
sample = X_test.iloc[:100]
predictions = model.predict(sample)

# Find the first sample that was predicted as "Attack"
attack_index = None
for i, pred in enumerate(predictions):
    if pred == 'Attack':
        attack_index = i
        break

print(f"Explaining sample #{attack_index}, predicted as: {predictions[attack_index]}")
print(f"Actual label was: {y_test[attack_index]}\n")

# Get SHAP values for this one sample
shap_values = explainer.shap_values(sample.iloc[[attack_index]])

# shap_values shape is (1, 78, 2) - we want the "Attack" class (index 1, usually)
# Let's check which class index corresponds to "Attack"
class_names = model.classes_
print("Model classes:", class_names)
attack_class_index = list(class_names).index('Attack')

# Get feature importance for THIS prediction
feature_names = sample.columns
importances = shap_values[0, :, attack_class_index]

# Combine feature names with their importance, sort by impact
feature_impact = pd.DataFrame({
    'Feature': feature_names,
    'Impact': importances
}).sort_values('Impact', key=abs, ascending=False)

print("\nTop 10 features that influenced this decision:")
print(feature_impact.head(10).to_string(index=False))