"""Draw the live Ghost Bus high-score board (assets/ghostbus-live.svg) from the project's published data."""
import json
import os
import urllib.request
from datetime import datetime

from pixel import CYAN, GOLD, PINK, SOFT, crt, svg

BASE = "https://raw.githubusercontent.com/Mohammed-890/ghost-bus/main/docs/data/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "ghostbus-live.svg")


def get(name):
    try:
        with urllib.request.urlopen(BASE + name, timeout=30) as r:
            return json.load(r)
    except Exception:
        return None


def when(iso):
    try:
        return datetime.fromisoformat(iso).strftime("%-d %b %H:%M").upper()
    except (TypeError, ValueError):
        return ""


def card(s, daily, live):
    h = s.get("health") or {}
    buses = len(live["buses"]) if live and live.get("buses") else h.get("median_buses")
    rows = [
        ("BUSES DRIVING NOW", buses, CYAN),
        ("TRIPS CHECKED", s.get("judged"), "#fff"),
        ("GHOST BUSES FOUND", s.get("ghosts"), PINK),
        ("DAYS RUNNING", s.get("days"), GOLD),
    ]
    W, H = 1280, 360
    lines = []
    for i, (name, val, col) in enumerate(rows):
        y = 128 + i * 48
        v = "-" if val is None else f"{int(val):06d}"
        lines.append(f'<text x="60" y="{y}" class="p" font-size="13" fill="{SOFT}">{("1ST", "2ND", "3RD", "4TH")[i]}</text>'
                     f'<text x="130" y="{y}" class="p" font-size="17" fill="{col}">{name}</text>'
                     f'<text x="600" y="{y}" class="p" font-size="17" fill="{col}" text-anchor="end">{v}</text>')
    days = (daily or [])[-12:]
    peak = max([d["judged"] for d in days] + [1])
    x0, bw, gap, base, hmax = 700, 34, 12, 290, 140
    bars = []
    for i, d in enumerate(days):
        x = x0 + i * (bw + gap)
        nj = max(1, round(d["judged"] / peak * hmax / 10))
        ng = max(1 if d["ghosts"] else 0, round(d["ghosts"] / peak * hmax / 10))
        for k in range(nj):  # stacked pixel blocks, ghosts on top in pink
            col = PINK if k >= nj - ng else "#7b5cff"
            bars.append(f'<rect x="{x}" y="{base - (k + 1) * 10}" width="{bw}" height="8" fill="{col}"/>')
        bars.append(f'<text x="{x + bw / 2}" y="{base + 22}" class="p" font-size="9" fill="{SOFT}" text-anchor="middle">'
                    f'{datetime.fromisoformat(d["service_date"]).strftime("%d/%m")}</text>')
    if not days:
        bars.append(f'<text x="{x0}" y="200" class="p" font-size="12" fill="{SOFT}">FIRST DAY LOADING...</text>')
    body = f'''<rect width="{W}" height="{H}" rx="18" fill="#160a33"/>
<text x="60" y="58" class="p" font-size="24" fill="#fff">HIGH SCORES</text>
<circle cx="374" cy="49" r="7" fill="#3dff8a"><animate attributeName="opacity" values="1;.2;1" dur="1.2s" repeatCount="indefinite"/></circle>
<text x="390" y="57" class="p" font-size="14" fill="#3dff8a">LIVE</text>
<text x="60" y="86" class="s" font-size="16" fill="{SOFT}">Ghost Bus Detector, watching every bus in Sheffield. This board redraws itself from live data.</text>
{''.join(lines)}
<text x="{x0}" y="128" class="p" font-size="13" fill="#fff">TRIPS PER DAY</text>
<rect x="{x0 + 220}" y="119" width="12" height="8" fill="#7b5cff"/><text x="{x0 + 238}" y="128" class="p" font-size="10" fill="{SOFT}">RAN</text>
<rect x="{x0 + 290}" y="119" width="12" height="8" fill="{PINK}"/><text x="{x0 + 308}" y="128" class="p" font-size="10" fill="{SOFT}">GHOST</text>
{''.join(bars)}
<text x="1230" y="340" class="p" font-size="10" fill="#6f6a94" text-anchor="end">UPDATED {when(s.get("updated", ""))} UTC</text>
{crt(W, H, 18)}'''
    return svg(W, H, body, f"Ghost Bus live: {buses} buses on the road, {s.get('judged')} trips checked, {s.get('ghosts')} ghost buses found.")


def main():
    s, daily, live = get("summary.json"), get("daily.json"), get("live.json")
    if not s:
        print("no data")
        return
    out = card(s, daily, live)
    old = open(OUT).read() if os.path.exists(OUT) else ""
    if out != old:
        open(OUT, "w").write(out)
        print("card updated")


if __name__ == "__main__":
    main()
