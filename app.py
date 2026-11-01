from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from functools import wraps
import pandas as pd
import joblib
import shap
import requests
import json
import os
from datetime import datetime, timedelta
from risk_levels import get_risk_level
from risk_levels_own import get_risk_level_own
from telegram_notify import send_critical_alert

app = Flask(__name__)
app.secret_key = 'soc-alert-triage-change-this-secret-key-2026'

# --- Login credentials (simple, for project demo purposes) ---
USERNAME = 'admin'
PASSWORD = 'SocAlert2026!'

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

notified_alert_ids = set()  # Keeps track of Critical alerts we've already texted about

# --- Analyst feedback (True Positive / False Positive) storage ---
FEEDBACK_FILE = 'feedback_data.json'


def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE) as f:
            return json.load(f)
    return {}


def save_feedback(data):
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(data, f)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('username') == USERNAME and request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


def calculate_stats(alerts):
    total = len(alerts)
    attacks = sum(1 for a in alerts if a['status'] == 'Attack')
    normal = total - attacks
    risk_counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
    for a in alerts:
        if a.get('risk_level') in risk_counts:
            risk_counts[a['risk_level']] += 1
    return {
        'total': total,
        'attacks': attacks,
        'normal': normal,
        'risk_counts': risk_counts
    }


def check_and_notify_critical(alerts, feedback_data=None):
    """Sends a Telegram message for any new Critical alert not seen before.
    Skips alerts the analyst already marked as False Positive."""
    feedback_data = feedback_data or {}
    for alert in alerts:
        if alert.get('risk_level') == 'Critical':
            alert_feedback = feedback_data.get(str(alert.get('id')))
            if alert_feedback and alert_feedback.get('verdict') == 'false_positive':
                continue  # analyst already dismissed this one, don't re-notify

            # Build a unique signature for this alert so we don't notify twice
            signature = f"{alert.get('src_ip')}_{alert.get('dst_ip')}_{alert.get('timestamp')}_{alert.get('attack_type')}"
            if signature not in notified_alert_ids:
                notified_alert_ids.add(signature)
                send_critical_alert(alert)


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
        'risk_level': None if pred == 'Normal' else get_risk_level_own(pred, confidence),
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
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/live')
@login_required
def dashboard_own():
    return render_template('dashboard_own.html')


@app.route('/live-feed')
@login_required
def dashboard_live_feed():
    return render_template('dashboard_live.html')


@app.route('/model-comparison')
@login_required
def model_comparison_page():
    return render_template('model_comparison.html')


@app.route('/api/alerts')
@login_required
def get_alerts():
    count = min(ALERT_COUNT, len(X_test))
    alerts = [analyze_sample(i) for i in range(count)]
    alerts.sort(key=lambda x: x['status'] == 'Normal')
    stats = calculate_stats(alerts)
    return jsonify({'alerts': alerts, 'stats': stats})


@app.route('/api/own-alerts')
@login_required
def get_own_alerts():
    count = min(ALERT_COUNT, len(X_test_own))
    alerts = [analyze_own_sample(i) for i in range(count)]
    alerts.sort(key=lambda x: x['status'] == 'Normal')
    stats = calculate_stats(alerts)
    return jsonify({'alerts': alerts, 'stats': stats})


@app.route('/api/live-feed')
@login_required
def get_live_feed():
    try:
        response = requests.get(KALI_LIVE_FEED_URL, timeout=3)
        lines = response.text.strip().split('\n')
        alerts = [json.loads(line) for line in lines if line]
        alerts.reverse()
        alerts = alerts[:200]

        feedback_data = load_feedback()
        confirmed_count = 0
        false_positive_count = 0
        for alert in alerts:
            fb = feedback_data.get(str(alert['id']))
            alert['feedback'] = fb
            if fb:
                if fb.get('verdict') == 'confirmed':
                    confirmed_count += 1
                elif fb.get('verdict') == 'false_positive':
                    false_positive_count += 1

        marked_total = confirmed_count + false_positive_count
        fp_rate = round((false_positive_count / marked_total) * 100, 1) if marked_total else 0

        stats = calculate_stats(alerts)
        stats['feedback'] = {
            'confirmed': confirmed_count,
            'false_positive': false_positive_count,
            'rate': fp_rate
        }

        check_and_notify_critical(alerts, feedback_data)
        return jsonify({'alerts': alerts, 'stats': stats})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/feedback', methods=['POST'])
@login_required
def submit_feedback():
    data = request.get_json()
    alert_id = str(data.get('id'))
    verdict = data.get('verdict')  # 'confirmed', 'false_positive', or None to clear

    feedback_data = load_feedback()
    if verdict is None:
        feedback_data.pop(alert_id, None)
    else:
        feedback_data[alert_id] = {
            'verdict': verdict,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
    save_feedback(feedback_data)
    return jsonify({'success': True})


@app.route('/api/model-comparison')
@login_required
def get_model_comparison():
    with open('model_comparison.json') as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
