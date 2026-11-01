import requests

# --- Replace these with your own values ---
TELEGRAM_BOT_TOKEN = "8923247138:AAFZKpN6TWBi5hheN3eOWnBKsB_CLrMPlWw"
TELEGRAM_CHAT_ID = "5016908618"

def send_critical_alert(alert):
    """
    Sends a Telegram message when a Critical risk alert is detected.
    'alert' is expected to be a dictionary with alert details.
    """
    message = (
        f"🚨 *CRITICAL ALERT DETECTED*\n\n"
        f"*Attack Type:* {alert.get('attack_type', alert.get('prediction', 'Unknown'))}\n"
        f"*Source IP:* {alert.get('src_ip', 'N/A')}\n"
        f"*Destination IP:* {alert.get('dst_ip', 'N/A')}\n"
        f"*Confidence:* {alert.get('confidence', 'N/A')}%\n"
        f"*Time:* {alert.get('timestamp', alert.get('time', 'N/A'))}\n\n"
        f"Please check the dashboard immediately."
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, data=payload, timeout=5)
        if response.status_code == 200:
            print(f"[Telegram] Critical alert notification sent successfully.")
        else:
            print(f"[Telegram] Failed to send alert. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"[Telegram] Error sending alert: {e}")