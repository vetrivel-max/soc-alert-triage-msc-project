import pandas as pd
import joblib
import shap
import numpy as np
import matplotlib.pyplot as plt

X_test = pd.read_csv("data/X_test.csv")
model = joblib.load("stage1_model.pkl")

X_sample = X_test.sample(n=500, random_state=42)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_sample)

if isinstance(shap_values, list):
    # older SHAP: list of arrays, one per class
    values = shap_values[1]
elif shap_values.ndim == 3:
    # newer SHAP: shape (samples, features, classes)
    values = shap_values[:, :, 1]
else:
    values = shap_values

mean_abs_shap = np.abs(values).mean(axis=0)

print("Shape check - mean_abs_shap:", mean_abs_shap.shape)
print("Shape check - columns:", len(X_sample.columns))

feature_importance = pd.Series(mean_abs_shap, index=X_sample.columns).sort_values(ascending=False)

top_features = feature_importance.head(15)

plt.figure(figsize=(8, 6))
top_features.sort_values().plot(kind="barh")
plt.xlabel("Mean |SHAP value| (average impact on model output)")
plt.title("Top 15 Features by Global SHAP Importance")
plt.tight_layout()
plt.savefig("shap_global_importance.png", dpi=150)
print("Saved plot as shap_global_importance.png")
print("\nTop 15 features:")
print(top_features.sort_values(ascending=False))