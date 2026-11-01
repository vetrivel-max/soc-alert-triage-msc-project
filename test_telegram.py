from telegram_notify import send_critical_alert

test_alert = {
    'attack_type': 'DoS',
    'src_ip': '192.168.10.130',
    'dst_ip': '192.168.10.129',
    'confidence': 99,
    'timestamp': '12:00:00'
}

send_critical_alert(test_alert)
print("Test finished - check your Telegram now.")