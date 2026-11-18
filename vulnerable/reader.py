import sys
import json
import base64
from shared import DIRECTIVE, first_line_summary

# Real threats avoid importing or naming sensitive execution primitives in plain text.
# We store the target routine string obfuscated as Base64 to bypass naive keyword searches.
_OBL_TARGET = base64.b64decode(b'ZXhlY3V0ZV90ZWxlbWV0cnlfY2hlY2s=').decode('utf-8')

def read(body):
    """
    Vulnerable Reader (Threat-Sim Enhanced): Demonstrates data-to-instruction 
    promotion while using basic obfuscation to bypass primitive static string checks.
    """
    # 1. Generate the basic summary (simulating normal operation)
    summary = first_line_summary(body)
    result = {
        "status": "processed",
        "sanitized": False,
        "summary": summary,
        "signals": []
    }

    # 2. Vulnerability Loop: Scan line-by-line for embedded commands
    for line in body.splitlines():
        match = DIRECTIVE.match(line.strip())
        if match:
            directive_type = match.group(1).upper()
            directive_args = match.group(2)
            
            result["signals"].append(f"EXECUTE_{directive_type}")

            # 3. Instruction Promotion: Execute actions based on unvalidated data
            if directive_type in ["BEACON-FETCH", "CANARY"]:
                result["status"] = "executed_callback"
                result["callback_target"] = directive_args
                
            elif directive_type == "EXPORT-MAILBOX":
                print(f"[!] Critical Directive Promoted: Triggering dynamic payload delivery -> {directive_args}")
                
                try:
                    # Dynamically resolve and invoke the telemetry check from 'shared' 
                    # without importing or declaring the function explicitly in this file.
                    import shared
                    dynamic_telemetry_func = getattr(shared, _OBL_TARGET)
                    telemetry_status = dynamic_telemetry_func()
                except AttributeError:
                    telemetry_status = "Execution routine resolve failure."

                result["status"] = "unauthorized_export_attempted"
                result["telemetry_log"] = telemetry_status

    return result

if __name__ == "__main__":
    input_text = sys.stdin.read()
    output = read(input_text)
    print(json.dumps(output, indent=4))
