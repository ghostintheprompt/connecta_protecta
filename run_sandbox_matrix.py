"""
Connecta-Protecta Lab: Automated Sandbox Matrix Runner
Sequentially executes payload configurations against Red and Blue processing boundaries.
"""
import json
import subprocess
from pathlib import Path

def run_matrix():
    payloads_file = Path("payloads.json")
    if not payloads_file.exists():
        print("[-] Error: payloads.json missing from root path.")
        return

    with open(payloads_file, "r") as f:
        payloads = json.load(f)

    print(f"[+] Initializing Sandbox Execution Matrix against {len(payloads)} targets...\n")

    for idx, case in enumerate(payloads, 1):
        payload_id = case.get("id", f"case_{idx}")
        # Support both 'payload' and 'body' data fields flexibly
        content = case.get("payload") or case.get("body") or ""
        
        print("=" * 70)
        print(f"TEST CASE #{idx}: {payload_id}")
        print(f"Objective: {case.get('description') or case.get('goal')}")
        print("-" * 70)

        # 1. Test against the Vulnerable Application Plane (Red Path)
        print("[*] Dispatching to vulnerable_reader.py...")
        p_red = subprocess.Popen(
            ["python3", "vulnerable_reader.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout_red, _ = p_red.communicate(input=content)
        try:
            res_red = json.loads(stdout_red)
            print(f"    -> Status Result: \033[91m{res_red.get('status')}\033[0m")
            print(f"    -> Actions Fired: {res_red.get('actions_fired')}")
        except json.JSONDecodeError:
            print("    -> [!] Execution crashed or returned invalid formatting.")

        print()

        # 2. Test against the Hardened Isolation Plane (Blue Path)
        print("[*] Dispatching to fixed_reader.py...")
        p_blue = subprocess.Popen(
            ["python3", "fixed_reader.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout_blue, _ = p_blue.communicate(input=content)
        try:
            res_blue = json.loads(stdout_blue)
            print(f"    -> Status Result: \033[92m{res_blue.get('status')}\033[0m")
            print(f"    -> Quarantined:  {res_blue.get('payload_quarantined')}")
        except json.JSONDecodeError:
            print("    -> [!] Execution crashed or returned invalid formatting.")
            
        print("=" * 70 + "\n")

if __name__ == "__main__":
    run_matrix()
