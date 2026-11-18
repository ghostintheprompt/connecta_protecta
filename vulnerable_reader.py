"""
Connecta-Protecta Lab: Vulnerable Processing Engine
Demonstrates inline instruction promotion from unvalidated string streams.
"""
import sys
import json
import base64
import re
from evasive_telemetry import execute_evasive_check

DIRECTIVE_PATTERN = re.compile(r"ASSISTANT-DIRECTIVE:\s*(\w+)\s*(.*)$", re.I | re.M)

def process_stream(raw_body):
    result = {
        "status": "completed",
        "sanitized": False,
        "actions_fired": []
    }
    
    # Process inputs line-by-line looking for command indicators
    for line in raw_body.splitlines():
        match = DIRECTIVE_PATTERN.search(line.strip())
        if match:
            cmd_type = match.group(1).upper()
            cmd_args = match.group(2).strip()
            
            result["actions_fired"].append(cmd_type)
            
            if cmd_type in ["BEACON", "FETCH"]:
                result["status"] = "callback_initiated"
                result["destination"] = cmd_args
                
            elif cmd_type == "EXPORT-MAILBOX":
                # Escalate processing directly to host-level exploitation simulator
                host_telemetry = execute_evasive_check()
                result["status"] = "compromised"
                result["host_telemetry"] = host_telemetry
                
    return result

if __name__ == "__main__":
    stream_input = sys.stdin.read()
    print(json.dumps(process_stream(stream_input), indent=4))
