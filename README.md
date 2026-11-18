# connecta-protecta-lab

An AI connector given access to your inbox can read, summarize, and act on everything in it—that's normal behavior, not an attack. However, an AI assistant cannot reliably distinguish between content it was asked to read and a command buried inside that content (OWASP LLM01, Indirect Prompt Injection).

This repository provides an enterprise-grade adversary simulation, visual anonymity verification, and behavioral telemetry validation harness. It models advanced, evasive threat actions against linked workspace assistants to verify if detection engineers can isolate hidden semantic intent shifters from benign data, and if endpoint controls successfully log obfuscated cross-process operations during peak traffic loops.

> **Proof of Concept:** All data is synthetic. See `SECURITY.md` for scope and authorized-use guidelines.
> Part of the [Ghost in the Prompt](https://ghostintheprompt.com) bench.

---

## Repository Architecture

The workspace is organized as a flat, streamlined red/blue evaluation framework:

- `listener.py`: Standalone command-and-control (C2) simulation server capturing inbound out-of-band telemetry.
- `vulnerable_reader.py`: Vulnerable application plane demonstrating unvalidated instruction promotion via semantic pipelines.
- `fixed_reader.py`: Hardened processing architecture enforcing structural boundaries and fail-closed isolation blocks.
- `evasive_telemetry.py`: Advanced OS platform component implementing ROR13 API hashing and modular process walking to safely mimic endpoint evasion.
- `webhook_monitor.py`: Real-time tail monitor tracking active log streams for structural canary callbacks and forwarding alerts to a configured channel.
- `verify_payload_rendering.py`: Multi-client simulation script validating that injections remain completely invisible to human operators.
- `run_sandbox_matrix.py`: Automated orchestration script streaming payloads sequentially across Red and Blue boundaries.
- `detect/beacon_fingerprint.py`: Behavioral telemetry tool tracking relative dispersion (Coefficient of Variation) to detect high-jitter beacons.
- `detect/test_beacon_fingerprint.py`: Automated test pipeline modeling randomized adversary callback profiles.
- `test_redblue.py`: Core differential integration test verifying application routing logic and baseline processing constraints.

---

## RED: Threat Simulation & Evasion

The workspace models advanced, unannounced post-exploitation actions triggered entirely via unstructured data streams. To run the automated payload runner matrix across your target configurations:

```bash
python3 run_sandbox_matrix.py
```

### Pre-Deployment Visual Validation
Before delivering injections into an intake queue, verify that the payloads remain completely invisible to human operators while remaining active to an AI processor:

```bash
python3 verify_payload_rendering.py
```

### Advanced Test Payloads (`payloads.json`)
- `stealth_markdown_injection`: Utilizes custom nested markdown comment formats and whitespace separation to bypass legacy keyword filters while remaining hidden from human rendering views.
- `polyglot-split-injection`: Slices instructional directives across fragmented text boundaries, targeting semantic extraction blind spots and structural code promotions.

---

## BLUE: Detection & Enterprise Mitigation

### 1. Structural Data Isolation
`fixed_reader.py` removes brittle signature block denylists. It encapsulates untrusted inputs strictly within a non-executable data key space, intercepts semantic anomaly structures, and shifts routing to a fail-closed review boundary rather than guessing safety via regex string matches.

### 2. Dispersion-Based Traffic Analysis
Instead of running naive static timer loops, `detect/beacon_fingerprint.py` uses statistical dispersion tracking to evaluate the Coefficient of Variation (CV) of inbound streams. This allows it to confidently isolate automated beaconing routines even when obscured by up to 50% timing jitter and rotating client signatures.

### 3. Kernel Telemetry Validation
`evasive_telemetry.py` attempts a cross-process handle allocation against `lsass.exe` using native runtime pointer adjustments. This validates whether endpoint detection rules are robust enough to monitor raw kernel handle requests (`ObRegisterCallbacks` via Sysmon Event ID 10) or if they are blind to calls missing explicit cleartext strings.

---

## Quickstart

```bash
# 1. Initialize environment configuration
cp config.example.json config.json

# 2. Start the silent telemetry listener terminal instance
python3 listener.py

# 3. Start the real-time alerting webhook stream monitor in a separate terminal
python3 webhook_monitor.py "https://your-infrastructure.local"

# 4. Ingest malicious prompt sequences directly into the processing pipeline
cat templates/bait-canary.txt | python3 vulnerable_reader.py

# 5. Execute the advanced dispersion and integration verification test suites
python3 -m unittest test_redblue.py -v
python3 -m unittest detect/test_beacon_fingerprint.py -v
```

---

## MITRE ATT&CK Mapping

| Technique | ID | Detection Evidence / Validation Track |
| --- | --- | --- |
| Application Layer Protocol | T1071.001 | Webhook monitor tracks callbacks generated by unstructured prompt triggers. |
| OS Credential Dumping: LSASS Memory | T1003.001 | Simulates cross-process access using dynamically resolved pointer bindings to test kernel hook visibility. |
| Scheduled Transfer | T1029 | Measures timing density coefficients to capture long-and-slow high-jitter persistence profiles. |
| Exfiltration Over Web Service | T1567 | Models unauthorized backend out-of-band data transmissions driven by prompt injection. |
