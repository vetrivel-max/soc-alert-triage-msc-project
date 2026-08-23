import pandas as pd
import joblib
import shap

# Load the Stage 1 model and some test data
model = joblib.load('stage1_model.pkl')
X_test = pd.read_csv('data/X_test.csv')

# SHAP can be slow on huge datasets, so we'll explain just a small sample first
sample = X_test.iloc[:100]  # first 100 rows

print("Creating SHAP explainer... this may take a minute")
explainer = shap.TreeExplainer(model)

print("Calculating SHAP values for 100 samples...")
shap_values = explainer.shap_values(sample)

print("Done! SHAP values calculated.")
print("Shape of shap_values:", shap_values.shape if hasattr(shap_values, 'shape') else len(shap_values))

# Save the explainer and shap values so we can reuse them
import pickle
with open('shap_explainer.pkl', 'wb') as f:
    pickle.dump(explainer, f)

print("Explainer saved as shap_explainer.pkl")