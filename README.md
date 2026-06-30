# nmap-automator

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Lint](https://img.shields.io/github/actions/workflow/status/gnaixnaij/nmap-automator/lint.yml?branch=main&label=lint&logo=github)](https://github.com/gnaixnaij/nmap-automator/actions)
[![Release](https://img.shields.io/github/v/release/gnaixnaij/nmap-automator?logo=github)](https://github.com/gnaixnaij/nmap-automator/releases)
[![Python](https://img.shields.io/badge/python-3.6+-3776AB?logo=python&logoColor=white)](https://python.org)

Automate common nmap scans with smart defaults. Four scan modes:

| Mode | Description |
|------|-------------|
| `quick` | Top 100 ports, fast discovery |
| `service` | Full port scan + service/version detection |
| `full` | Aggressive OS detection, scripts, traceroute |
| `vuln` | Vulnerability script scan |

## Usage

```bash
chmod +x nmap_automator.py
./nmap_automator.py 10.10.10.1 -t quick
./nmap_automator.py scanme.nmap.org -t service -o ./scans
```

## Requirements

- Python 3.6+
- nmap (`sudo apt install nmap` or `brew install nmap`)

## License

MIT
