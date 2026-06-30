#!/usr/bin/env python3
"""nmap-automator — Automate common nmap scans with smart defaults."""

import subprocess
import sys
import argparse
import shutil
from pathlib import Path

VERSION = "1.1.0"

BANNER = f"""
╔══════════════════════════════════════╗
║        nmap-automator v{VERSION}         ║
║  Quick • Service • Full • Vuln      ║
╚══════════════════════════════════════╝
"""

SCAN_TYPES = {
    "quick":   {"args": ["-T4", "-F"],        "desc": "Quick port discovery (top 100 ports)"},
    "service": {"args": ["-T4", "-sC", "-sV", "-p-"], "desc": "Full port scan + service detection"},
    "full":    {"args": ["-T4", "-A", "-p-"],  "desc": "Full aggressive scan (OS, services, scripts)"},
    "vuln":    {"args": ["-T4", "-sV", "--script=vuln"], "desc": "Vulnerability scan"},
}

OUTPUT_FORMATS = {
    "nmap":     {"flag": "-oN", "ext": ".nmap"},
    "xml":      {"flag": "-oX", "ext": ".xml"},
    "grepable": {"flag": "-oG", "ext": ".gnmap"},
    "all":      {"flag": "-oA", "ext": ""},
}


def check_nmap():
    if not shutil.which("nmap"):
        print("[-] nmap not found. Install it with:")
        print("    sudo apt install nmap  (Debian/Ubuntu)")
        print("    brew install nmap      (macOS)")
        sys.exit(1)


def run_nmap(target, scan_type, output_dir, output_format, extra_args):
    if scan_type not in SCAN_TYPES:
        print(f"[-] Unknown scan type: {scan_type}")
        sys.exit(1)

    info = SCAN_TYPES[scan_type]
    fmt = OUTPUT_FORMATS.get(output_format, OUTPUT_FORMATS["nmap"])
    outfile = Path(output_dir) / f"{target}_{scan_type}{fmt['ext']}"
    outfile.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["nmap"] + info["args"] + [fmt["flag"], str(outfile), target]

    if extra_args:
        cmd += extra_args

    print(f"[*] Running {scan_type} scan on {target}")
    print(f"[*] Output:   {output_format.upper()} → {outfile}")
    print(f"[*] Command:  {' '.join(cmd)}")
    print()

    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"\n[+] Scan complete → {outfile}")
    else:
        print(f"\n[-] Scan failed (exit code {result.returncode})")
    return result.returncode


def main():
    if "--version" in sys.argv:
        print(f"nmap-automator v{VERSION}")
        sys.exit(0)

    print(BANNER)
    check_nmap()

    parser = argparse.ArgumentParser(
        description="Automate nmap scans with smart defaults",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  nmap_automator.py 10.10.10.1
  nmap_automator.py scanme.nmap.org -t service -o ./scans -f xml
  nmap_automator.py 10.10.10.0/24 -t quick -f all -- -T5
""")
    parser.add_argument("target", help="Target IP, hostname, or CIDR range")
    parser.add_argument("-t", "--type", choices=list(SCAN_TYPES.keys()),
                        default="quick", help="Scan type (default: quick)")
    parser.add_argument("-o", "--output", default="./results",
                        help="Output directory (default: ./results)")
    parser.add_argument("-f", "--format", choices=list(OUTPUT_FORMATS.keys()),
                        default="nmap", help="Output format (default: nmap)")
    parser.add_argument("extra", nargs=argparse.REMAINDER,
                        help="Extra nmap arguments (use -- before them)")

    args = parser.parse_args()

    print(f"[*] Target: {args.target}")
    print(f"[*] Type:   {args.type} — {SCAN_TYPES[args.type]['desc']}")
    print(f"[*] Format: {args.format.upper()}")
    print(f"[*] Output: {args.output}")
    print()

    extra = args.extra[1:] if args.extra and args.extra[0] == "--" else args.extra
    sys.exit(run_nmap(args.target, args.type, args.output, args.format, extra))


if __name__ == "__main__":
    main()
