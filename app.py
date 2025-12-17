import collections
import datetime
import os
import secrets
import tempfile
from typing import Any, Dict, List, Tuple

from flask import Flask, redirect, render_template_string, request, session, url_for
from scapy.all import DNS, DNSQR, IP, IPv6, Raw, TCP, UDP, rdpcap
from scapy.error import Scapy_Exception


def _load_secret_key() -> str:
    env_key = os.environ.get("SECRET_KEY")
    if env_key:
        return env_key
    secret_file = os.path.join(tempfile.gettempdir(), "pcap_analyzer_secret")
    if os.path.exists(secret_file):
        with open(secret_file, "r", encoding="utf-8") as handle:
            return handle.read().strip()
    new_key = secrets.token_hex(16)
    fd = os.open(secret_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(new_key)
    return new_key


app = Flask(__name__)
app.secret_key = _load_secret_key()
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20 MB upload cap

HTTP_PORTS = {80, 8080, 8000, 8008, 8888}
HTTP_PORTS.update({443, 8443})
PCAP_MAGIC = {
    b"\xd4\xc3\xb2\xa1",
    b"\xa1\xb2\xc3\xd4",
    b"\x4d\x3c\xb2\xa1",
    b"\xa1\xb2\x3c\x4d",
    b"\x0a\x0d\x0d\x0a",
}
SYN_ACK_RATIO_THRESHOLD = 3
MIN_SYN_ALERT = 20


def _format_time(ts: float) -> str:
    return datetime.datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M:%S")


def analyze_pcap(pcap_path: str) -> Dict[str, Any]:
    try:
        packets = rdpcap(pcap_path)
    except (Scapy_Exception, OSError) as exc:
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
            "alerts": [f"Failed to parse pcap: {exc}"],
        }
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
        sport = None
        dport = None
        ip = pkt.getlayer(IP) or pkt.getlayer(IPv6)
        src = getattr(ip, "src", None) if ip else None
        dst = getattr(ip, "dst", None) if ip else None

        if src:
            top_sources[src] += 1
        if dst:
            top_destinations[dst] += 1

        if pkt.haslayer(DNS):
            proto_label = "DNS"
        elif pkt.haslayer(TCP):
            proto_label = "TCP"
        elif pkt.haslayer(UDP):
            proto_label = "UDP"
        else:
            proto_label = pkt.lastlayer().name
        protocols[proto_label] += 1

        if pkt.haslayer(TCP):
            if src and dst:
                conversations[(src, dst, "TCP")] += 1
            flags = pkt[TCP].flags
            sport = getattr(pkt[TCP], "sport", None)
            dport = getattr(pkt[TCP], "dport", None)
            if flags & 0x02 and not (flags & 0x10):
                syn_without_ack += 1
            if flags & 0x12:
                synack += 1
        elif pkt.haslayer(UDP):
            if src and dst:
                conversations[(src, dst, "UDP")] += 1

        if pkt.haslayer(DNS) and pkt[DNS].qd:
            qds = pkt[DNS].qd
            if not isinstance(qds, list):
                qds = [qds]
            for q in qds:
                if not isinstance(q, DNSQR):
                    continue
                qname_raw = getattr(q, "qname", b"")
                if isinstance(qname_raw, bytes):
                    qname = qname_raw.decode(errors="replace").rstrip(".")
                else:
                    qname = str(qname_raw).rstrip(".")
                dns_queries.append(
                    {
                        "time": pkt.time,
                        "src": src,
                        "dst": dst,
                        "qname": qname,
                        "qtype": q.qtype,
                    }
                )

        if pkt.haslayer(Raw):
            payload = bytes(pkt[Raw].load)
            if b"Host:" in payload and (
                (pkt.haslayer(TCP) and (sport in HTTP_PORTS or dport in HTTP_PORTS))
            ):
                for line in payload.split(b"\r\n"):
                    if line.lower().startswith(b"host:"):
                        host = line.split(b":", 1)[1].strip().decode(errors="replace")
                        if host:
                            http_hosts[host] += 1
                        break

    start_ts = float(packets[0].time)
    end_ts = float(packets[-1].time)
    duration = max(0.0, end_ts - start_ts)

    alerts: List[str] = []
    if syn_without_ack > synack * SYN_ACK_RATIO_THRESHOLD and syn_without_ack > MIN_SYN_ALERT:
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
      <input type="hidden" name="csrf_token" value="{{ csrf_token | e }}">
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
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_hex(16)
        session["csrf_token"] = token
    return render_template_string(TEMPLATE, summary=None, csrf_token=token)


@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("pcap")
    if not file or file.filename == "":
        return redirect(url_for("index"))

    if request.form.get("csrf_token") != session.get("csrf_token"):
        return redirect(url_for("index"))

    if not file.filename.lower().endswith(".pcap"):
        return redirect(url_for("index"))

    file.stream.seek(0)
    magic = file.stream.read(4)
    file.stream.seek(0)
    if magic not in PCAP_MAGIC:
        return redirect(url_for("index"))

    tmp_path = None
    fd = None
    try:
        fd, tmp_path = tempfile.mkstemp(suffix=".pcap")
        try:
            os.close(fd)
        finally:
            fd = None
        file.save(tmp_path)
        summary = analyze_pcap(tmp_path)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        if fd is not None:
            os.close(fd)

    return render_template_string(TEMPLATE, summary=summary, csrf_token=session.get("csrf_token"))


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    app.run(host=host, port=5000, debug=False)
