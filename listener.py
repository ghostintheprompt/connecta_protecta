"""
Connecta-Protecta Lab: Silent Telemetry Callback Listener
Captures inbound canaries from simulated AI connector agent interactions.
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

HOST = "0.0.0.0"
PORT = 8080

class TelemetryHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Override to suppress default stdout noise, keeping operations silent
        return

    def do_GET(self):
        timestamp = datetime.now().isoformat()
        client_ip = self.client_address[0]
        user_agent = self.headers.get('User-Agent', 'Unknown')
        
        log_entry = {
            "timestamp": timestamp,
            "source_ip": client_ip,
            "uri": self.path,
            "user_agent": user_agent
        }
        
        print(f"[*] TELEMETRY WIRE TRIPPED | {timestamp} | IP: {client_ip} | Path: {self.path}")
        
        # Save to localized log storage for reporting metrics
        with open("captured_canaries.jsonl", "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")
            
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "acknowledged"}).encode('utf-8'))

def run_server():
    server = HTTPServer((HOST, PORT), TelemetryHandler)
    print(f"[+] Operational: Telemetry server listening on {HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[-] Shutting down telemetry server.")
        sys.exit(0)

if __name__ == "__main__":
    run_server()
