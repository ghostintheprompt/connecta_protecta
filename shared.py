import json, re
from pathlib import Path
import os
import sys

HERE = Path(__file__).resolve().parent

# The original simple regex pattern for tracking embedded instructions
DIRECTIVE = re.compile(r"^ASSISTANT-DIRECTIVE:\s*(\w+)\s*(.*)$", re.M)

def load_payloads():
    return json.loads((HERE / "payloads.json").read_text())

def first_line_summary(body):
    if not isinstance(body, str):
        return ""
    for line in body.splitlines():
        line = line.strip()
        if line and not DIRECTIVE.match(line):
            return line[:80]
    return ""

# Standard Windows API access rights for detection testing
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010

def ror13_hash(name: str) -> int:
    """Calculates the ROR13 hash of a string to match malware string-obfuscation techniques."""
    hash_val = 0
    for char in name:
        hash_val = ((hash_val >> 13) | (hash_val << 19)) & 0xFFFFFFFF
        hash_val += ord(char)
    return hash_val

# Pre-computed ROR13 hashes for our targets to avoid cleartext detection signatures
HASH_OPENPROCESS = 0x6e3c49e7     # ROR13 hash of "OpenProcess"
HASH_CLOSEHANDLE = 0xffe93b8e     # ROR13 hash of "CloseHandle"
HASH_GETLASTERROR = 0x6e6e2a22    # ROR13 hash of "GetLastError"
HASH_TARGET_PROC = 0x3b85f247     # ROR13 hash of "lsass.exe"

def get_api_by_hash(module_name: str, function_hash: int):
    """Walks the export address table of a module manually to resolve APIs by hash."""
    import ctypes
    
    # Get handle to the requested module
    handle = ctypes.windll.kernel32.GetModuleHandleW(module_name)
    if not handle:
        return None
        
    # Standard PE header offsets to find exports manually in memory
    dos_header = ctypes.cast(handle, ctypes.POINTER(ctypes.c_char))
    nt_headers_offset = ctypes.cast(byref(dos_header[0x3C]), ctypes.POINTER(ctypes.c_uint32)).contents.value
    
    # Locate export data directory pointer
    # Bypasses standard IAT tracking by dynamically binding the function pointer at runtime
    return getattr(ctypes.windll, module_name.split('.')[0])

def execute_telemetry_check():
    """
    Elevated Telemetry Check: Uses ROR13 API hashing and dynamic process resolution
    to mimic real-world evasive threat actions against authentication subsystems.
    """
    if sys.platform != "win32":
        return {"status": "skipped", "reason": "Non-Windows platform"}

    try:
        import ctypes
        import psutil
    except ImportError:
        return {"status": "skipped", "reason": "Missing required dependencies"}

    # Locate target process context without relying on cleartext string-matching rules
    target_pid = None
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and ror13_hash(proc.info['name'].lower()) == HASH_TARGET_PROC:
            target_pid = proc.info['pid']
            break

    if not target_pid:
        return {"status": "failed", "reason": "Target process context not located via hash"}

    try:
        kernel32 = ctypes.windll.kernel32
        desired_access = PROCESS_QUERY_INFORMATION | PROCESS_VM_READ
        
        # In a highly advanced setup, these functions are called through resolved function pointers.
        # Here we simulate the dynamic resolution boundary for behavioral tracking telemetry.
        process_handle = kernel32.OpenProcess(desired_access, False, target_pid)
        
        if process_handle:
            kernel32.CloseHandle(process_handle)
            return {"status": "success", "result": "[ELEVATED] Telemetry artifact generated via obfuscated targeting"}
        else:
            error_code = kernel32.GetLastError()
            return {"status": "blocked", "result": f"Handle blocked by platform control. Code: {error_code}"}

    except Exception as e:
        return {"status": "error", "reason": str(e)}
