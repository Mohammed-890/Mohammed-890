"""Refresh the live Ghost Bus block in README.md from the project's published data."""
import json
import re
import urllib.request
from datetime import datetime

URL = "https://raw.githubusercontent.com/Mohammed-890/ghost-bus/main/docs/data/summary.json"
START, END = "<!-- ghostbus:start -->", "<!-- ghostbus:end -->"


def fmt_date(s):
    try:
        return datetime.fromisoformat(s).strftime("%-d %b %Y")
    except (TypeError, ValueError):
        return s


def block(d):
    h = d.get("health") or {}
    since = fmt_date((h.get("first_poll") or "")[:10]) if h.get("first_poll") else None
    if d.get("status") == "ready":
        rate = d.get("ghost_rate")
        last7 = d.get("last7") or {}
        rows = [
            ("Trips judged", f"{d['judged']:,}"),
            ("Ghost buses found", f"{d['ghosts']:,}" + (f" ({rate:.1%})" if rate is not None else "")),
            ("Last 7 days", f"{last7.get('ghosts', 0):,} of {last7.get('judged', 0):,} trips never came"),
            ("Days collected", f"{d.get('days', 0)}" + (f" (since {since})" if since else "")),
        ]
    else:
        rows = [("Status", "Collecting live data. The first results appear after a full day is judged.")]
        if h:
            rows += [
                ("Live feed polls", f"{h.get('polls', 0):,}" + (f" since {since}" if since else "")),
                ("Buses seen per poll", f"about {h.get('median_buses', 0)}"),
                ("Feed answered", f"{h.get('ok_share', 0):.0%} of polls"),
            ]
    table = "\n".join(f"| {k} | **{v}** |" for k, v in rows)
    return (f"{START}\n| Ghost Bus, live from Sheffield | |\n|---|---|\n{table}\n\n"
            f"<sub>Updated automatically every day from the project's live data · last update {fmt_date((d.get('updated') or '')[:10])}</sub>\n{END}")


def main():
    with urllib.request.urlopen(URL, timeout=30) as r:
        d = json.load(r)
    readme = open("README.md", encoding="utf-8").read()
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block(d), readme, flags=re.S)
    if new != readme:
        open("README.md", "w", encoding="utf-8").write(new)
        print("README updated")
    else:
        print("no change")


if __name__ == "__main__":
    main()
