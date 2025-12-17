# PCAP / Wireshark File Analyzer (GUI)

A lightweight Flask-based GUI to inspect `.pcap` captures and extract investigation-ready highlights: packet counts, protocol mix, top talkers, conversations, DNS queries, HTTP hosts, and simple alerts (SYN scan heuristic).

## Quick start

```bash
cd /home/runner/work/semprojectcn/semprojectcn
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
# Open http://localhost:5000 and upload a .pcap (max 20 MB)
```

## What you get

- Packet totals, duration, capture start/end
- Protocol distribution
- Top sources/destinations and conversations
- DNS query list (first 20)
- HTTP host header extraction
- Alert: high SYN-without-ACK ratio (rudimentary scan indicator)

## Notes

- Uses Scapy to parse captures; no admin privileges needed for offline analysis.
- Upload limit is capped at 20 MB to avoid excessive memory use.
