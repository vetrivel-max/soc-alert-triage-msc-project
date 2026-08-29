import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import json
import time

print("Loading data...")
X_train = pd.read_csv('data/X_train.csv')
y_train = pd.read_csv('data/y_train.csv').values.ravel()
X_test = pd.read_csv('data/X_test.csv')
y_test = pd.read_csv('data/y_test.csv').values.ravel()

# Convert labels to numeric for XGBoost
y_train_numeric = (y_train == 'Attack').astype(int)
y_test_numeric = (y_test == 'Attack').astype(int)

results = {}

# Model 1: Random Forest (already trained, reload it)
print("\nEvaluating existing Random Forest model...")
rf_model = joblib.load('stage1_model.pkl')
start = time.time()
y_pred_rf = rf_model.predict(X_test)
rf_time = time.time() - start

results['Random Forest'] = {
    'accuracy': accuracy_score(y_test, y_pred_rf),
    'precision': precision_score(y_test, y_pred_rf, pos_label='Attack'),
    'recall': recall_score(y_test, y_pred_rf, pos_label='Attack'),
    'f1': f1_score(y_test, y_pred_rf, pos_label='Attack'),
    'predict_time': rf_time
}

# Model 2: Logistic Regression
print("Training Logistic Regression...")
lr_model = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
start = time.time()
lr_model.fit(X_train, y_train)
lr_train_time = time.time() - start

start = time.time()
y_pred_lr = lr_model.predict(X_test)
lr_predict_time = time.time() - start

results['Logistic Regression'] = {
    'accuracy': accuracy_score(y_test, y_pred_lr),
    'precision': precision_score(y_test, y_pred_lr, pos_label='Attack'),
    'recall': recall_score(y_test, y_pred_lr, pos_label='Attack'),
    'f1': f1_score(y_test, y_pred_lr, pos_label='Attack'),
    'predict_time': lr_predict_time
}
print(f"  Logistic Regression training took {lr_train_time:.2f}s")

# Model 3: XGBoost
print("Training XGBoost...")
xgb_model = XGBClassifier(n_estimators=100, max_depth=10, random_state=42, eval_metric='logloss')
start = time.time()
xgb_model.fit(X_train, y_train_numeric)
xgb_train_time = time.time() - start

start = time.time()
y_pred_xgb_numeric = xgb_model.predict(X_test)
xgb_predict_time = time.time() - start
y_pred_xgb = pd.Series(y_pred_xgb_numeric).map({1: 'Attack', 0: 'Normal'}).values

results['XGBoost'] = {
    'accuracy': accuracy_score(y_test, y_pred_xgb),
    'precision': precision_score(y_test, y_pred_xgb, pos_label='Attack'),
    'recall': recall_score(y_test, y_pred_xgb, pos_label='Attack'),
    'f1': f1_score(y_test, y_pred_xgb, pos_label='Attack'),
    'predict_time': xgb_predict_time
}
print(f"  XGBoost training took {xgb_train_time:.2f}s")

# Print summary
print("\n=== MODEL COMPARISON RESULTS ===")
for model_name, metrics in results.items():
    print(f"\n{model_name}:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")

# Save results for the dashboard to use
with open('model_comparison.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nResults saved to model_comparison.json")

# Save the new models too
joblib.dump(lr_model, 'lr_model.pkl')
joblib.dump(xgb_model, 'xgb_model.pkl')
print("Models saved: lr_model.pkl, xgb_model.pkl")