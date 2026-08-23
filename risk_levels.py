# Risk level mapping based on typical real-world impact and severity
# Critical = severe data/system compromise risk
# High = major service disruption or compromised access
# Medium = reconnaissance or attempted (not yet successful) intrusion

RISK_LEVELS = {
    'Heartbleed': 'Critical',
    'Infiltration': 'Critical',
    'Web Attack': 'High',
    'Bot': 'High',
    'DDoS': 'High',
    'DoS Hulk': 'High',
    'DoS GoldenEye': 'High',
    'DoS slowloris': 'Medium',
    'DoS Slowhttptest': 'Medium',
    'FTP-Patator': 'Medium',
    'SSH-Patator': 'Medium',
    'PortScan': 'Medium',
}

def get_risk_level(attack_type):
    """Returns the risk level for a given attack type. Defaults to 'Medium' if unknown."""
    return RISK_LEVELS.get(attack_type, 'Medium')