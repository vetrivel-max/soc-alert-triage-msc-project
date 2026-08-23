import pandas as pd
import joblib
from risk_levels import get_risk_level

# Load both trained models
stage1_model = joblib.load('stage1_model.pkl')
stage2_model = joblib.load('stage2_model.pkl')

def analyze_traffic(X_row):
    """
    Takes one row of traffic data and returns a full triage result.
    """
    # Stage 1: Normal or Attack?
    stage1_pred = stage1_model.predict(X_row)[0]

    if stage1_pred == 'Normal':
        return {
            'status': 'Normal',
            'attack_type': None,
            'risk_level': None
        }
    else:
        # Stage 2: What specific attack type?
        stage2_pred = stage2_model.predict(X_row)[0]
        risk = get_risk_level(stage2_pred)
        return {
            'status': 'Attack',
            'attack_type': stage2_pred,
            'risk_level': risk
        }

# Test it on some real test data
X_test = pd.read_csv('data/X_test.csv')

print("Testing pipeline on first 10 test samples:\n")
for i in range(10):
    row = X_test.iloc[[i]]  # get one row, keep it as a DataFrame
    result = analyze_traffic(row)
    print(f"Sample {i+1}: {result}")