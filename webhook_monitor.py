"""
Connecta-Protecta Lab: Real-Time Webhook Alerting Monitor
Monitors passive log streams for structural canary callbacks and forwards them to a configured alerting channel.
"""
import sys
import json
import time
import urllib.request
from pathlib import Path

def send_webhook(webhook_url, payload_data):
    """Formats and transmits structured alerts to an external communication channel."""
    try:
        # Resolve assets from both legacy formats and the upgraded telemetry fields
        bait_asset = payload_data.get('bait') or payload_data.get('uri') or 'Unknown Canary Asset'
        source_ip = payload_data.get('ip') or payload_data.get('source_ip') or 'Unknown Source Address'
        timestamp = payload_data.get('time') or payload_data.get('timestamp') or 'N/A'
        
        formatted_message = {
            "content": (
                f"🚨 **[CONNECTA-PROTECTA ALERT] AI Telemetry Tripwire Triggered** 🚨\n"
                f"**Bait/URI Asset:** `{bait_asset}`\n"
                f"**Source IP:** `{source_ip}`\n"
                f"**User Agent:** `{payload_data.get('user_agent', 'None')[:120]}`\n"
                f"**Timestamp:** `{timestamp}`\n"
                f"**Analysis Profile:** `Adversarial Interaction Verified`"
            )
        }
        
        request_headers = {"Content-Type": "application/json", "User-Agent": "Security-Monitor-Engine/2.0"}
        encoded_data = json.dumps(formatted_message).encode("utf-8")
        
        req = urllib.request.Request(webhook_url, data=encoded_data, headers=request_headers, method="POST")
        with urllib.request.urlopen(req) as response:
            return response.status in [200, 204]
    except Exception:
        return False

def monitor_log_stream(log_path, webhook_url, check_interval=1.0):
    """Performs real-time tail monitoring against active JSONL logs to parse callbacks immediately."""
    p = Path(log_path)
    if not p.exists():
        p.touch()
        
    print(f"[+] Operational: Monitoring log stream at [{p.name}] for immediate webhook forwarding...")
    
    with open(p, "r") as f:
        # Move cursor directly to the end of the file to ignore stale historical entries
        f.seek(0, 2)
        while True:
            current_line = f.readline()
            if not current_line:
                time.sleep(check_interval)
                continue
            try:
                parsed_hit = json.loads(current_line.strip())
                
                # REVISED CONDITION: Validate key structural parameters instead of a rigid token string
                # This catches both simple canaries and the upgraded high-jitter, multi-agent footprints.
                if any(k in parsed_hit for k in ["token_id", "uri", "source_ip", "ip"]):
                    send_webhook(webhook_url, parsed_hit)
            except Exception:
                pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 webhook_monitor.py <WEBHOOK_URL> [LOG_FILE_PATH]")
        sys.exit(1)
        
    target_webhook = sys.argv[1]
    target_log = sys.argv[2] if len(sys.argv) > 2 else "captured_canaries.jsonl"
    
    try:
        monitor_log_stream(target_log, target_webhook)
    except KeyboardInterrupt:
        print("\n[-] Terminating real-time monitor.")
        sys.exit(0)
