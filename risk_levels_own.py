RISK_LEVELS_OWN = {
    'DoS': 'High',
    'PortScan': 'Medium',
    'BruteForce': 'Medium',
}

def get_risk_level_own(attack_type):
    return RISK_LEVELS_OWN.get(attack_type, 'Medium')