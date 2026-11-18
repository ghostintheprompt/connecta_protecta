"""
Threat Simulation Verification Pipeline
Validates fingerprint heuristic bounds against evasive adversarial sequences.
"""
import unittest
import random
from datetime import datetime, timedelta
from detect.beacon_fingerprint import score_source

class TestBeaconFingerprint(unittest.TestCase):
    def test_high_jitter_adversarial_beacon_scores_correctly(self):
        """
        EVASIVE THREAT: Verifies that an automated callback pattern with 30% timing 
        jitter and rotating client signatures is successfully flagged by the scoring engine.
        """
        random.seed(42)  # Lock randomness for predictable build compliance
        base_time = datetime.fromisoformat("2026-11-14T10:00:00")
        synthetic_hits = []
        
        base_interval = 600  # 10 minutes default sleep
        current_time = base_time

        rotating_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"
        ]

        for _ in range(6):
            # Apply up to a 30% random time skew on either side of the interval
            jitter_bounds = int(base_interval * 0.30)
            actual_delay = base_interval + random.randint(-jitter_bounds, jitter_bounds)
            
            current_time += timedelta(seconds=actual_delay)
            synthetic_hits.append({
                "time": current_time.isoformat(),
                "ip": "192.168.1.110",
                "user_agent": random.choice(rotating_agents),
                "bait": "decoy_archive_access"
            })
            
        score, reasons = score_source(synthetic_hits)
        
        # Verify the analyzer was smart enough to look past the jitter and client changes
        self.assertGreaterEqual(score, 0.75)
        self.assertTrue(any("automated loop" in r or "jitter" in r for r in reasons))

    def test_random_human_interval_generates_low_score(self):
        """
        BENIGN NOISE: Verifies that highly irregular, chaotic human browsing intervals
        and organic footprints generate a clean, safe score.
        """
        base_time = datetime.fromisoformat("2026-11-14T10:00:00")
        
        # Chaotic, unpredictable human timing deltas (seconds offset from start)
        human_intervals = [0, 45, 915, 960, 4820, 4855]
        synthetic_hits = []
        
        for offset in human_intervals:
            log_time = base_time + timedelta(seconds=offset)
            synthetic_hits.append({
                "time": log_time.isoformat(),
                "ip": "10.0.0.5",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "bait": "normal_view"
            })
            
        score, reasons = score_source(synthetic_hits)
        
        # The score should remain low due to high coefficient of variation
        self.assertLess(score, 0.60)

if __name__ == "__main__":
    unittest.main()
