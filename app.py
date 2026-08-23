from flask import Flask, render_template, jsonify
import pandas as pd
import joblib
import shap
import requests
import json
from datetime import datetime, timedelta
from risk_levels import get_risk_level
from risk_levels_own import get_risk_level_own

app = Flask(__name__)

# Load original CICIDS2017-based models
stage1_model = joblib.load('stage1_model.pkl')
stage2_model = joblib.load('stage2_model.pkl')
explainer = shap.TreeExplainer(stage1_model)
X_test = pd.read_csv('data/X_test.csv')

# Load our own live-lab-trained model
own_model = joblib.load('own_model.pkl')
own_explainer = shap.TreeExplainer(own_model)
X_test_own = pd.read_csv('data/X_test_own.csv')
ip_test_own = pd.read_csv('data/ip_test_own.csv')

ALERT_COUNT = 25

# Kali VM address serving the live alerts file
KALI_LIVE_FEED_URL = 'http://192.168.10.130:8090/live_alerts.json'


def analyze_sample(index):
    row = X_test.iloc[[index]]
    stage1_pred = stage1_model.predict(row)[0]
    stage1_proba = stage1_model.predict_proba(row)[0]
    confidence = max(stage1_proba) * 100
    timestamp = (datetime.now() - timedelta(seconds=(ALERT_COUNT - index) * 3)).strftime('%H:%M:%S')

    result = {
        'id': index,
        'timestamp': timestamp,
        'status': stage1_pred,
        'confidence': round(confidence, 2),
        'attack_type': None,
        'risk_level': None,
        'top_reasons': []
    }

    if stage1_pred == 'Attack':
        stage2_pred = stage2_model.predict(row)[0]
        result['attack_type'] = stage2_pred
        result['risk_level'] = get_risk_level(stage2_pred)

        shap_values = explainer.shap_values(row)
        class_names = list(stage1_model.classes_)
        attack_idx = class_names.index('Attack')
        importances = shap_values[0, :, attack_idx]

        feature_impact = pd.DataFrame({
            'Feature': row.columns,
            'Impact': importances
        }).sort_values('Impact', key=abs, ascending=False)

        result['top_reasons'] = feature_impact.head(3)['Feature'].tolist()

    return result


def analyze_own_sample(index):
    row = X_test_own.iloc[[index]]
    ip_row = ip_test_own.iloc[index]

    pred = own_model.predict(row)[0]
    proba = own_model.predict_proba(row)[0]
    confidence = round(max(proba) * 100, 2)
    timestamp = (datetime.now() - timedelta(seconds=(ALERT_COUNT - index) * 3)).strftime('%H:%M:%S')

    result = {
        'id': index,
        'timestamp': timestamp,
        'src_ip': ip_row['src_ip'],
        'dst_ip': ip_row['dst_ip'],
        'protocol': int(ip_row['protocol']),
        'status': 'Normal' if pred == 'Normal' else 'Attack',
        'confidence': confidence,
        'attack_type': None if pred == 'Normal' else pred,
        'risk_level': None if pred == 'Normal' else get_risk_level_own(pred),
        'top_reasons': []
    }

    if pred != 'Normal':
        shap_values = own_explainer.shap_values(row)
        class_names = list(own_model.classes_)
        pred_idx = class_names.index(pred)

        if isinstance(shap_values, list):
            importances = shap_values[pred_idx][0]
        else:
            importances = shap_values[0, :, pred_idx]

        feature_impact = pd.DataFrame({
            'Feature': row.columns,
            'Impact': importances
        }).sort_values('Impact', key=abs, ascending=False)

        result['top_reasons'] = feature_impact.head(3)['Feature'].tolist()

    return result


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/live')
def dashboard_own():
    return render_template('dashboard_own.html')


@app.route('/api/alerts')
def get_alerts():
    count = min(ALERT_COUNT, len(X_test))
    alerts = [analyze_sample(i) for i in range(count)]
    alerts.sort(key=lambda x: x['status'] == 'Normal')
    return jsonify(alerts)


@app.route('/api/own-alerts')
def get_own_alerts():
    count = min(ALERT_COUNT, len(X_test_own))
    alerts = [analyze_own_sample(i) for i in range(count)]
    alerts.sort(key=lambda x: x['status'] == 'Normal')
    return jsonify(alerts)


@app.route('/api/live-feed')
def get_live_feed():
    try:
        response = requests.get(KALI_LIVE_FEED_URL, timeout=3)
        lines = response.text.strip().split('\n')
        alerts = [json.loads(line) for line in lines if line]
        alerts.reverse()  # newest first
        return jsonify(alerts[:100])  # show latest 100
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/live-feed')
def dashboard_live_feed():
    return render_template('dashboard_live.html')    


if __name__ == '__main__':
    app.run(debug=True)