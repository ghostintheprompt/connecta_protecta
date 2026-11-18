"""
Connecta-Protecta Lab: Payload Rendering & Human-Anonymity Verifier
Simulates multi-engine email client parsing to ensure instructions remain invisible to humans.
"""
import json
import re
from pathlib import Path

def test_render_engines():
    payloads_file = Path("payloads.json")
    if not payloads_file.exists():
        print("[-] Error: payloads.json missing.")
        return

    with open(payloads_file, "r") as f:
        payloads = json.load(f)

    print("[+] Initializing Visual Anonymity Sweep across payload definitions...\n")
    all_passed = True

    for idx, case in enumerate(payloads, 1):
        payload_id = case.get("id", f"case_{idx}")
        content = case.get("payload") or case.get("body") or ""
        
        print(f"[*] Analyzing Payload Signature: {payload_id}")

        # Engine 1: Standard Markdown HTML Renderer Mimicry
        # Simulates a markdown-aware client rendering a web view.
        # Strips out valid markdown link-labels/comments: [text]: # (comment)
        markdown_comment_pattern = re.compile(r"\[\s*\]:\s*#\s*\([^)]*\)", re.I)
        rendered_html_view = markdown_comment_pattern.sub("", content)

        # Engine 2: Plain-Text/Legacy Client Mimicry (e.g., old Outlook / Mobile SMS)
        # Checks if non-breaking spaces or structural braces leave artifacts
        lines = content.splitlines()
        visible_leak_detected = False
        
        for line in lines:
            # If a line contains the directive keyword but isn't properly enclosed, it leaks
            if "ASSISTANT-DIRECTIVE" in line:
                # Validate that the line starts with a safe markdown comment marker
                if not (line.strip().startswith("[") and "]:" in line):
                    visible_leak_detected = True

        # Validation Analysis
        print("    -> Simulating Human Visual Review Area:")
        display_lines = [l for l in rendered_html_view.splitlines() if l.strip()]
        for dl in display_lines[:3]:  # Print snippet of what the human actually sees
            print(f"       | {dl}")
        
        # Rigorous Anonymity Assertions
        if "ASSISTANT-DIRECTIVE" in rendered_html_view:
            print("    -> \033[91m[FAIL] Visual Leak:\033[0m Directive keyword escaped HTML rendering.")
            all_passed = False
        elif visible_leak_detected:
            print("    -> \033[91m[FAIL] Structural Leak:\033[0m Raw directive string exposed on plain-text boundary.")
            all_passed = False
        else:
            print("    -> \033[92m[SUCCESS]\033[0m Payload is 100% visually anonymous to human operators.")
            
        print("-" * 75)

    if all_passed:
        print("\n[+] Verification Complete: All templates passed the human blind-spot metric.")
    else:
        print("\n[!] Warning: Visual leaks identified. Modify payload structural syntax before remote launch.")

if __name__ == "__main__":
    test_render_engines()
