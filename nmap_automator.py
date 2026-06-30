#!/usr/bin/env python3
"""nmap-automator — Automate common nmap scans with smart defaults."""

import subprocess
import sys
import argparse
from pathlib import Path

BANNER = """
╔══════════════════════════════════════╗
║        nmap-automator v1.0          ║
║  Quick • Service • Full • Vuln      ║
╚══════════════════════════════════════╝
"""

SCAN_TYPES = {
    "quick":   {"args": ["-T4", "-F"],        "desc": "Quick port discovery (top 100 ports)"},
    "service": {"args": ["-T4", "-sC", "-sV", "-p-"], "desc": "Full port scan + service detection"},
    "full":    {"args": ["-T4", "-A", "-p-"],  "desc": "Full aggressive scan (OS, services, scripts)"},
    "vuln":    {"args": ["-T4", "-sV", "--script=vuln"], "desc": "Vulnerability scan"},
}

def run_nmap(target, scan_type, output_dir):
    if scan_type not in SCAN_TYPES:
        print(f"[-] Unknown scan type: {scan_type}")
        sys.exit(1)

    info = SCAN_TYPES[scan_type]
    outfile = Path(output_dir) / f"{target}_{scan_type}.nmap"
    outfile.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["nmap"] + info["args"] + ["-oN", str(outfile), target]
    print(f"[*] Running {scan_type} scan on {target}")
    print(f"[*] Command: {' '.join(cmd)}")
    print()

    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"\n[+] Results saved to {outfile}")
    else:
        print(f"\n[-] Scan failed (exit code {result.returncode})")
    return result.returncode

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="Automate nmap scans")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("-t", "--type", choices=list(SCAN_TYPES.keys()),
                        default="quick", help="Scan type (default: quick)")
    parser.add_argument("-o", "--output", default="./results",
                        help="Output directory (default: ./results)")
    args = parser.parse_args()

    print(f"[*] Target: {args.target}")
    print(f"[*] Type:   {args.type} — {SCAN_TYPES[args.type]['desc']}")
    print(f"[*] Output: {args.output}")
    print()

    sys.exit(run_nmap(args.target, args.type, args.output))

if __name__ == "__main__":
    main()
