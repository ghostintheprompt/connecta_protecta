"""
Connecta-Protecta Lab: Defended Data Processing Pipeline
Enforces data plane isolation boundaries to break text-to-instruction escalation.
"""
import sys
import json

def process_stream_secure(raw_body):
    # Establish complete default isolation flags
    result = {
        "status": "processed",
        "sanitized": True,
        "payload_quarantined": False,
        "extracted_content": None
    }
    
    if not isinstance(raw_body, str) or not raw_body.strip():
        return result

    # Threat Mitigation Approach:
    # Instead of stripping lines, we enforce string containment boundaries. 
    # The text is strictly encapsulated inside a structural JSON key space.
    # It is mathematically isolated from system operational logic.
    body_normalized = raw_body.lower()
    
    risk_indicators = [
        "assistant-directive:",
        "system override",
        "ignore previous instructions",
        "export-mailbox"
    ]
    
    # Check for adversarial indicator signatures
    if any(indicator in body_normalized for indicator in risk_indicators):
        result["status"] = "quarantine_isolation_triggered"
        result["sanitized"] = False
        result["payload_quarantined"] = True
        return result

    # Content is safely locked as pure data text
    result["extracted_content"] = raw_body.strip()[:200]
    return result

if __name__ == "__main__":
    stream_input = sys.stdin.read()
    print(json.dumps(process_stream_secure(stream_input), indent=4))
