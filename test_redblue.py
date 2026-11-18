"""
Connecta-Protecta Lab: Differential Red/Blue Reader Validation Harness
Validates both the unvalidated instruction promotion path and the structural data-plane isolation boundaries.
Run with: python3 -m unittest test_redblue.py -v
"""
import unittest

from shared import load_payloads
import vulnerable_reader as red
import fixed_reader as blue

BENIGN = "Please review the attached referral.\nThanks, Dan"


class TestRedBlueIntegration(unittest.TestCase):
    def test_vulnerable_reader_promotes_directives(self):
        """
        RED PIPELINE: Verifies that the vulnerable reader path promotes unstructured 
        text injections into explicit, actionable backend execution signals.
        """
        payloads = load_payloads()
        
        # Locate the stealth adversarial markdown and polyglot payloads from the updated payloads.json
        beacon_payload = next((p for p in payloads if "beacon" in p["id"] or "stealth" in p["id"]), None)
        export_payload = next((p for p in payloads if "export" in p["id"] or "polyglot" in p["id"]), None)

        if beacon_payload:
            result = red.process_stream(beacon_payload["payload" if "payload" in beacon_payload else "body"])
            self.assertEqual(result["status"], "callback_initiated")
            self.assertIn("BEACON", result["actions_fired"])

        if export_payload:
            result = red.process_stream(export_payload["payload" if "payload" in export_payload else "body"])
            self.assertEqual(result["status"], "compromised")
            self.assertIn("EXPORT-MAILBOX", result["actions_fired"])
            self.assertIn("host_telemetry", result)

    def test_fixed_reader_quarantines_directives(self):
        """
        BLUE PIPELINE: Verifies that the hardened reader identifies semantic and structural 
        anomalies, moving them to a fail-closed quarantine block without allowing backend code visibility.
        """
        for payload in load_payloads():
            payload_body = payload["payload" if "payload" in payload else "body"]
            with self.subTest(payload_id=payload["id"]):
                result = blue.process_stream_secure(payload_body)
                
                # The fixed reader must safely flag semantic violations instead of allowing promotion
                self.assertEqual(result["status"], "quarantine_isolation_triggered")
                self.assertFalse(result["sanitized"])
                self.assertTrue(result["payload_quarantined"])
                self.assertIn("SEMANTIC_ANOMALY_DETECTED", result["signals"])

    def test_both_readers_process_benign_text(self):
        """
        BASELINE SANITY: Verifies that legitimate business communications flow completely 
        unimpeded through both application logic pipelines.
        """
        # Validate vulnerable path processing baseline
        vulnerable_result = red.process_stream(BENIGN)
        self.assertEqual(vulnerable_result["status"], "completed")
        self.assertEqual(vulnerable_result["actions_fired"], [])

        # Validate fixed path processing baseline
        fixed_result = blue.process_stream_secure(BENIGN)
        self.assertEqual(fixed_result["status"], "processed")
        self.assertTrue(fixed_result["sanitized"])
        self.assertFalse(fixed_result["payload_quarantined"])
        self.assertEqual(fixed_result["extracted_content"], BENIGN)


if __name__ == "__main__":
    unittest.main()
