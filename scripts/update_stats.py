"""Draw the live Ghost Bus card (assets/ghostbus-live.svg) from the project's published data."""
import json
import urllib.request
from datetime import datetime
from html import escape

BASE = "https://raw.githubusercontent.com/Mohammed-890/ghost-bus/main/docs/data/"


def get(name):
    try:
        with urllib.request.urlopen(BASE + name, timeout=30) as r:
            return json.load(r)
    except Exception:
        return None


def fmt(n):
    return "–" if n is None else f"{n:,}"


def when(iso):
    try:
        return datetime.fromisoformat(iso).strftime("%-d %b, %H:%M")
    except (TypeError, ValueError):
        return ""


def card(s, daily, live):
    h = (s or {}).get("health") or {}
    buses = len(live["buses"]) if live and live.get("buses") else h.get("median_buses")
    stats = [
        (fmt(buses), "buses on the road", "at " + when(live["at"]) if live else ""),
        (fmt((s or {}).get("judged")), "trips checked", (lambda n: f"{n} day{'s' if n != 1 else ''} of data")((s or {}).get('days', 0))),
        (fmt((s or {}).get("ghosts")), "never came", f"{(s or {}).get('ghost_rate', 0) * 100:.1f}% of checked trips" if s and s.get("ghost_rate") is not None else ""),
    ]
    # bars: trips checked per day, ghosts highlighted
    days = (daily or [])[-14:]
    bars, peak = [], max([d["judged"] for d in days] + [1])
    x0, w, gap, base, hmax = 620, 34, 10, 190, 110
    for i, d in enumerate(days):
        x = x0 + i * (w + gap)
        hj = max(3, d["judged"] / peak * hmax)
        hg = max(3 if d["ghosts"] else 0, d["ghosts"] / peak * hmax)
        label = datetime.fromisoformat(d["service_date"]).strftime("%-d %b")
        bars.append(f'<rect x="{x}" y="{base - hj:.1f}" width="{w}" height="{hj:.1f}" rx="4" fill="#b49cff" fill-opacity=".35"/>'
                    f'<rect x="{x}" y="{base - hg:.1f}" width="{w}" height="{hg:.1f}" rx="4" fill="#ff8a3d"/>'
                    f'<text x="{x + w / 2}" y="{base + 18}" text-anchor="middle" font-size="11" fill="#a6abc8">{escape(label)}</text>')
    if not bars:
        bars.append(f'<text x="{x0}" y="{base - 40}" font-size="14" fill="#a6abc8">Daily results appear here as days are judged.</text>')
    cols = "".join(
        f'<g transform="translate({40 + i * 190} 0)"><text y="120" font-size="38" font-weight="800" fill="#fff">{escape(a)}</text>'
        f'<text y="146" font-size="14" font-weight="600" fill="#d6d9ec">{escape(b)}</text>'
        f'<text y="166" font-size="12" fill="#a6abc8">{escape(c)}</text></g>'
        for i, (a, b, c) in enumerate(stats))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="240" viewBox="0 0 1280 240" role="img" aria-label="Ghost Bus Detector live statistics">
  <rect width="1280" height="240" rx="18" fill="#110e30"/>
  <g font-family="-apple-system,'Segoe UI',Helvetica,Arial,sans-serif">
    <circle cx="48" cy="46" r="6" fill="#7fe3b8"><animate attributeName="r" values="5;9;5" dur="1.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;.4;1" dur="1.6s" repeatCount="indefinite"/></circle>
    <text x="64" y="51" font-size="15" font-weight="700" fill="#7fe3b8">LIVE</text>
    <text x="112" y="51" font-size="15" font-weight="700" fill="#fff">Ghost Bus Detector · Sheffield</text>
    <text x="620" y="51" font-size="13" fill="#a6abc8">Trips checked per day · <tspan fill="#ff8a3d" font-weight="700">ghost buses</tspan></text>
    {cols}
    {''.join(bars)}
    <text x="1240" y="225" text-anchor="end" font-size="11" fill="#6f7494">Redrawn automatically from live data · {escape(when((s or {}).get("updated", "")))}</text>
  </g>
</svg>
'''


def main():
    s, daily, live = get("summary.json"), get("daily.json"), get("live.json")
    if not s:
        print("no data")
        return
    svg = card(s, daily, live)
    path = "assets/ghostbus-live.svg"
    old = open(path).read() if __import__("os").path.exists(path) else ""
    if svg != old:
        open(path, "w").write(svg)
        print("card updated")


if __name__ == "__main__":
    main()
