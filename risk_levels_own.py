# Risk level mapping for the self-generated lab model
# Critical = severe, immediate action required
# High = significant threat, investigate promptly
# Medium = suspicious activity, worth checking
# Low = minor/reconnaissance activity, low urgency

RISK_LEVELS_OWN = {
    'DoS': 'High',
    'BruteForce': 'High',
    'PortScan': 'Medium',
}

def get_risk_level_own(attack_type, confidence=None):
    """
    Returns risk level for a given attack type.
    Optionally adjusts based on model confidence:
    - Low confidence detections get downgraded (less certain = less urgent)
    """
    base_risk = RISK_LEVELS_OWN.get(attack_type, 'Medium')

    if confidence is not None:
        if confidence < 60:
            downgrade_map = {'Critical': 'High', 'High': 'Medium', 'Medium': 'Low'}
            return downgrade_map.get(base_risk, 'Low')

    return base_risk