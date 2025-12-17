import collections
import datetime
import os
import tempfile
from typing import Any, Dict, List, Tuple

from flask import Flask, redirect, render_template_string, request, url_for
from scapy.all import DNS, DNSQR, IP, IPv6, Raw, TCP, UDP, rdpcap


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20 MB upload cap


def _format_time(ts: float) -> str:
    return datetime.datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M:%S")


def analyze_pcap(pcap_path: str) -> Dict[str, Any]:
    packets = rdpcap(pcap_path)
    total = len(packets)
    if total == 0:
        return {
            "total_packets": 0,
            "duration": 0.0,
            "start": None,
            "end": None,
            "protocols": [],
            "top_sources": [],
            "top_destinations": [],
            "conversations": [],
            "dns_queries": [],
            "http_hosts": [],
            "alerts": ["Empty capture"],
        }

    protocols = collections.Counter()
    top_sources = collections.Counter()
    top_destinations = collections.Counter()
    conversations = collections.Counter()
    dns_queries: List[Dict[str, Any]] = []
    http_hosts = collections.Counter()
    syn_without_ack = 0
    synack = 0

    for pkt in packets:
        ip = pkt.getlayer(IP) or pkt.getlayer(IPv6)
        src = getattr(ip, "src", None) if ip else None
        dst = getattr(ip, "dst", None) if ip else None

        if src:
            top_sources[src] += 1
        if dst:
            top_destinations[dst] += 1

        proto_label = None
        if pkt.haslayer(TCP):
            proto_label = "TCP"
            protocols["TCP"] += 1
            if src and dst:
                conversations[(src, dst, "TCP")] += 1
            flags = pkt[TCP].flags
            if flags & 0x02 and not (flags & 0x10):
                syn_without_ack += 1
            if flags & 0x12:
                synack += 1
        elif pkt.haslayer(UDP):
            proto_label = "UDP"
            protocols["UDP"] += 1
            if src and dst:
                conversations[(src, dst, "UDP")] += 1
        elif pkt.haslayer(DNS):
            proto_label = "DNS"
            protocols["DNS"] += 1
        else:
            # fallback to last layer name for protocol mix
            proto_label = pkt.lastlayer().name
            protocols[proto_label] += 1

        if pkt.haslayer(DNS) and pkt[DNS].qd and isinstance(pkt[DNS].qd, DNSQR):
            qname = pkt[DNS].qd.qname.decode(errors="ignore").rstrip(".")
            dns_queries.append(
                {
                    "time": pkt.time,
                    "src": src,
                    "dst": dst,
                    "qname": qname,
                    "qtype": pkt[DNS].qd.qtype,
                }
            )

        if pkt.haslayer(Raw):
            payload = bytes(pkt[Raw].load)
            if b"Host:" in payload:
                for line in payload.split(b"\r\n"):
                    if line.lower().startswith(b"host:"):
                        host = line.split(b":", 1)[1].strip().decode(errors="ignore")
                        if host:
                            http_hosts[host] += 1
                        break

    start_ts = float(packets[0].time)
    end_ts = float(packets[-1].time)
    duration = max(0.0, end_ts - start_ts)

    alerts: List[str] = []
    if syn_without_ack > synack * 3 and syn_without_ack > 20:
        alerts.append("High SYN without ACK ratio observed (possible scan).")

    return {
        "total_packets": total,
        "duration": duration,
        "start": _format_time(start_ts),
        "end": _format_time(end_ts),
        "protocols": protocols.most_common(),
        "top_sources": top_sources.most_common(10),
        "top_destinations": top_destinations.most_common(10),
        "conversations": [(*k, v) for k, v in conversations.most_common(10)],
        "dns_queries": sorted(dns_queries, key=lambda x: x["time"])[:20],
        "http_hosts": http_hosts.most_common(10),
        "alerts": alerts,
    }


TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PCAP Investigator</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; background: #0b1021; color: #f5f5f5; }
    header { padding: 16px 24px; background: #141a32; position: sticky; top: 0; }
    h1 { margin: 0; font-size: 22px; }
    main { padding: 24px; }
    .card { background: #161c35; border: 1px solid #232a4a; border-radius: 12px; padding: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.2); }
    .grid { display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }
    .table { width: 100%; border-collapse: collapse; margin-top: 8px; }
    .table th, .table td { border-bottom: 1px solid #232a4a; padding: 6px 8px; text-align: left; }
    .table th { color: #9bb0ff; font-weight: 600; }
    .pill { display: inline-block; background: #232a4a; padding: 4px 10px; border-radius: 20px; margin: 4px 4px 0 0; }
    .muted { color: #9aa3c4; font-size: 13px; }
    input[type=file] { color: #dce3ff; }
    button { background: linear-gradient(135deg, #4e5dfc, #7f8fff); color: white; border: none; padding: 10px 16px; border-radius: 8px; cursor: pointer; font-weight: 600; }
    button:hover { opacity: 0.92; }
    .alert { background: #40213d; color: #ffcedf; padding: 10px 12px; border-radius: 8px; margin-top: 10px; }
    .section { margin-top: 20px; }
  </style>
</head>
<body>
  <header>
    <h1>PCAP / Wireshark File Analyzer</h1>
    <div class="muted">Upload a .pcap to extract investigation-ready highlights.</div>
  </header>
  <main>
    <form action="{{ url_for('analyze') }}" method="post" enctype="multipart/form-data" class="card">
      <label class="muted">Choose pcap file (max 20MB)</label><br>
      <input type="file" name="pcap" accept=".pcap" required>
      <button type="submit">Analyze</button>
    </form>

    {% if summary %}
    <section class="section">
      <div class="grid">
        <div class="card">
          <div class="muted">Packets</div>
          <h2>{{ summary.total_packets }}</h2>
          <div class="muted">Duration: {{ "%.2f"|format(summary.duration) }}s</div>
          <div class="muted">From {{ summary.start }} to {{ summary.end }}</div>
        </div>
        <div class="card">
          <div class="muted">Protocol Mix</div>
          {% for proto, count in summary.protocols %}
            <span class="pill">{{ proto }} — {{ count }}</span>
          {% else %}
            <div class="muted">No protocol data</div>
          {% endfor %}
        </div>
        <div class="card">
          <div class="muted">HTTP Hosts</div>
          {% for host, count in summary.http_hosts %}
            <div>{{ host }} <span class="muted">({{ count }})</span></div>
          {% else %}
            <div class="muted">No HTTP host headers</div>
          {% endfor %}
        </div>
        <div class="card">
          <div class="muted">Alerts</div>
          {% for alert in summary.alerts %}
            <div class="alert">{{ alert }}</div>
          {% else %}
            <div class="muted">No alerts flagged</div>
          {% endfor %}
        </div>
      </div>
    </section>

    <section class="section card">
      <div class="muted">Top Sources</div>
      <table class="table">
        <tr><th>Source</th><th>Packets</th></tr>
        {% for ip, count in summary.top_sources %}
          <tr><td>{{ ip }}</td><td>{{ count }}</td></tr>
        {% else %}
          <tr><td colspan="2" class="muted">No data</td></tr>
        {% endfor %}
      </table>
    </section>

    <section class="section card">
      <div class="muted">Top Destinations</div>
      <table class="table">
        <tr><th>Destination</th><th>Packets</th></tr>
        {% for ip, count in summary.top_destinations %}
          <tr><td>{{ ip }}</td><td>{{ count }}</td></tr>
        {% else %}
          <tr><td colspan="2" class="muted">No data</td></tr>
        {% endfor %}
      </table>
    </section>

    <section class="section card">
      <div class="muted">Top Conversations</div>
      <table class="table">
        <tr><th>Src</th><th>Dst</th><th>Proto</th><th>Pkts</th></tr>
        {% for src, dst, proto, count in summary.conversations %}
          <tr><td>{{ src }}</td><td>{{ dst }}</td><td>{{ proto }}</td><td>{{ count }}</td></tr>
        {% else %}
          <tr><td colspan="4" class="muted">No data</td></tr>
        {% endfor %}
      </table>
    </section>

    <section class="section card">
      <div class="muted">DNS Queries (first 20)</div>
      <table class="table">
        <tr><th>Time</th><th>Src</th><th>Dst</th><th>Query</th><th>Type</th></tr>
        {% for row in summary.dns_queries %}
          <tr>
            <td>{{ row.time | round(3) }}</td>
            <td>{{ row.src }}</td>
            <td>{{ row.dst }}</td>
            <td>{{ row.qname }}</td>
            <td>{{ row.qtype }}</td>
          </tr>
        {% else %}
          <tr><td colspan="5" class="muted">No DNS traffic</td></tr>
        {% endfor %}
      </table>
    </section>
    {% endif %}
  </main>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(TEMPLATE, summary=None)


@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("pcap")
    if not file or file.filename == "":
        return redirect(url_for("index"))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pcap") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        summary = analyze_pcap(tmp_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return render_template_string(TEMPLATE, summary=summary)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
