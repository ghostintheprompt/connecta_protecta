"""
Advanced Behavioral Telemetry Analyzer
Uses relative dispersion and asset-clustering heuristics to detect high-jitter beacons.
"""
from datetime import datetime
import math

def score_source(hits):
    """
    Scores a stream of logs from a single source IP for automated beaconing profiles.
    Accounts for up to 50% timing jitter and randomized user-agent strings.
    Returns: (float score [0.0 - 1.0], list of reasons)
    """
    reasons = []
    if len(hits) < 4:
        return 0.1, ["Insufficient data points to map behavior profile"]

    # 1. Parse timestamps and calculate sorting order
    timestamps = []
    user_agents = set()
    targeted_baits = set()

    for hit in hits:
        timestamps.append(datetime.fromisoformat(hit["time"]))
        user_agents.add(hit.get("user_agent", ""))
        targeted_baits.add(hit.get("bait", ""))

    timestamps.sort()

    # 2. Extract time deltas in seconds
    deltas = []
    for i in range(len(timestamps) - 1):
        delta = (timestamps[i+1] - timestamps[i]).total_seconds()
        deltas.append(max(delta, 1.0)) # Prevent division by zero

    # 3. Statistical Analysis: Mean and Standard Deviation
    mean_delta = sum(deltas) / len(deltas)
    variance = sum((x - mean_delta) ** 2 for x in deltas) / len(deltas)
    std_dev = math.sqrt(variance)

    # Coefficient of Variation (CV) measures relative jitter independent of scale
    coef_of_variation = std_dev / mean_delta

    score = 0.0

    # Heuristic Rule A: Bounded Timing Distribution (Catches Jitter <= 40%)
    if coef_of_variation < 0.25:
        score += 0.50
        reasons.append(f"Low timing jitter profile identified (CV: {coef_of_variation:.2f})")
    elif coef_of_variation < 0.45:
        score += 0.40
        reasons.append(f"Moderate timing jitter detected; consistent with evasive automated loop (CV: {coef_of_variation:.2f})")
    else:
        reasons.append(f"High variance timing distribution suggests chaotic human activity (CV: {coef_of_variation:.2f})")

    # Heuristic Rule B: High Target Affinity / Focus
    # If the source continuously hits the exact same honeypot/bait asset
    if len(targeted_baits) == 1 and "decoy" in list(targeted_baits)[0]:
        score += 0.25
        reasons.append("High destination affinity: focused exclusively on a single high-value canary asset")

    # Heuristic Rule C: Monitored Resource Density
    if mean_delta < 1200:  # Average callback window under 20 minutes
        score += 0.15
        reasons.append("Frequent sequence density matches persistence pacing profiles")

    # Heuristic Rule D: Behavioral Evasion Signatures
    # Rotating user agents from a single source host hitting the same file is highly anomalous
    if len(user_agents) > 1 and len(targeted_baits) == 1:
        score += 0.10
        reasons.append(f"Anomalous host signature rotation: {len(user_agents)} user-agents targeting single asset")

    return min(round(score, 2), 1.0), reasons
