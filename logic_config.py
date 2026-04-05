def get_thresholds(appetite):
    """Calculates dynamic bars based on bank lending appetite."""
    return {
        "decline_bar": 0.35 - (appetite * 0.30),
        "approve_bar": 0.85 - (appetite * 0.30),
        "pass_grade": 0.60 - (appetite * 0.20)
    }

def get_strategy_label(appetite):
    labels = {0.1: "Ultra-Conservative", 0.3: "Conservative", 
              0.5: "Neutral", 0.7: "Growth-Oriented", 0.9: "Ultra-Aggressive"}
    return labels.get(appetite, "Custom")