import math


def calculate_current(power_kw, voltage, pf, phase):
    """Calculate current for single or three phase systems"""
    if phase == "Single Phase":
        current = (power_kw * 1000) / (voltage * pf)
    else:  # Three Phase
        current = (power_kw * 1000) / (math.sqrt(3) * voltage * pf)

    return round(current, 2)


def breaker_size(current):
    """Select standard breaker size"""
    ratings = [6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100,
               125, 160, 200, 250, 315, 400, 500, 630]

    for rating in ratings:
        if current <= rating:
            return rating
    return ratings[-1]


def select_transformer(kva):
    """Select nearest standard transformer size"""
    ratings = [100, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600]

    for r in ratings:
        if kva <= r:
            return r
    return ratings[-1]


def calculate_voltage_drop(current, length, resistance):
    """Calculate voltage drop using approximate formula"""
    vd = (1.732 * current * resistance * length) / 1000
    return round(vd, 2)


def recommend_cable(current, installation):
    """Recommend cable size based on current and installation method"""
    if installation == "Buried":
        if current <= 25:
            return 4
        elif current <= 40:
            return 6
        elif current <= 63:
            return 10
        elif current <= 100:
            return 16
        else:
            return 25

    elif installation == "Cable Tray" or installation == "Ladder":
        if current <= 25:
            return 2.5
        elif current <= 40:
            return 4
        elif current <= 63:
            return 6
        elif current <= 100:
            return 10
        else:
            return 16

    else:  # Conduit (default)
        if current <= 25:
            return 2.5
        elif current <= 40:
            return 6
        elif current <= 63:
            return 10
        elif current <= 100:
            return 16
        else:
            return 25


def design_status(vd_percent, vd_limit=5.0):
    """Determine overall voltage drop status"""
    if vd_percent <= vd_limit * 0.6:
        return "GOOD"
    elif vd_percent <= vd_limit:
        return "ACCEPTABLE"
    else:
        return "NOT ACCEPTABLE"


def design_check(current, breaker, cable):
    """Improved design validation with better messages"""
    issues = []

    # Breaker check with safety margin
    if breaker < current * 1.25:
        issues.append(f"Breaker ({breaker}A) is undersized for load current ({current:.1f}A). Consider next higher size.")

    # Cable check
    if cable < 2.5:
        issues.append(f"Cable size ({cable} mm²) is below minimum recommended standard.")

    if current > 100 and cable < 25:
        issues.append("Cable size may be insufficient for high current applications.")

    # Final result
    if not issues:
        return "Design checks passed. All components appear adequately sized."
    else:
        return " | ".join(issues)


def transformer_status(loading):
    """Evaluate transformer loading status"""
    if loading <= 70:
        return "GOOD RESERVE CAPACITY"
    elif loading <= 90:
        return "ACCEPTABLE"
    else:
        return "HIGH LOADING"