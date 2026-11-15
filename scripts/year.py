"""My year on GitHub, drawn as a bus route, plus the player card.

Every day of the last year is a stop. The bus drives the whole grid, picking up every stop; busier days are bigger
stops. Ghost buses follow behind. The player card shows level, streaks and languages from the same data.

    python scripts/year.py                    fetch live data, write assets/year.svg and assets/player.svg
    python scripts/year.py --from data.json   use saved data instead (for testing)
"""
import datetime as dt
import json
import math
import os
import re
import sys
import urllib.request

from pixel import CYAN, GOLD, INK, PINK, SANS, SOFT, blink, crt, svg

USER = "Mohammed-890"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
VIOLET = "#b49cff"
WALL = "#4b39ff"


# ---------------------------------------------------------------- data
def get(url, token=None):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-readme"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


def fetch():
    html = get(f"https://github.com/users/{USER}/contributions")
    cells = dict(re.findall(r'data-date="(\d{4}-\d\d-\d\d)"[^>]*?id="([^"]+)"', html))
    cells.update({d: i for i, d in re.findall(r'id="([^"]+)"[^>]*?data-date="(\d{4}-\d\d-\d\d)"', html)})
    tips = dict(re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>\s*(\d+|No) contribution', html))
    days = sorted([d, 0 if tips.get(i, "No") == "No" else int(tips[i])] for d, i in cells.items())
    if len(days) < 300:
        raise RuntimeError(f"only {len(days)} days parsed")
    token = os.environ.get("GITHUB_TOKEN")
    repos = json.loads(get(f"https://api.github.com/users/{USER}/repos?per_page=100", token))
    langs = {}
    for r in repos:
        if r["fork"] or r["name"] in (USER, f"{USER}.github.io"):
            continue
        for k, v in json.loads(get(r["languages_url"], token)).items():
            langs[k] = langs.get(k, 0) + v
    return {"days": days, "repos": len(repos), "langs": langs}


def stats(data):
    days = data["days"]
    counts = [c for _, c in days]
    total, active = sum(counts), sum(1 for c in counts if c)
    best_i = max(range(len(days)), key=lambda i: counts[i])
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    cur, k = 0, len(counts) - 1
    if counts[k] == 0:            # today isn't over yet
        k -= 1
    while k >= 0 and counts[k]:
        cur, k = cur + 1, k - 1
    level = int(math.sqrt(total / 2)) + 1
    lo, hi = 2 * (level - 1) ** 2, 2 * level ** 2
    return {"total": total, "active": active, "best": counts[best_i], "best_day": days[best_i][0], "longest": longest,
            "streak": cur, "level": level, "xp": (total - lo) / (hi - lo), "to_next": hi - total}


# ---------------------------------------------------------------- shapes
def bus_top(color, ghost=False):
    """A bus seen from above, 30 x 14, centred, facing right."""
    win = "".join(f'<rect x="{-11 + i * 6}" y="-4.5" width="4" height="9" rx="1" fill="#1a1036" opacity="{.5 if ghost else 1}"/>' for i in range(3))
    return (f'<rect x="-15" y="-7" width="30" height="14" rx="3" fill="{color}"/>{win}'
            f'<rect x="8" y="-5" width="5" height="10" rx="1" fill="#1a1036" opacity="{.5 if ghost else 1}"/>'
            + ("" if ghost else '<rect x="14" y="-6" width="2" height="3" fill="#fff6b0"/><rect x="14" y="3" width="2" height="3" fill="#fff6b0"/>'))


# ---------------------------------------------------------------- the route
def year_svg(data, s):
    days = data["days"]
    first = dt.date.fromisoformat(days[0][0])
    off = (first.weekday() + 1) % 7                     # rows start on Sunday like GitHub
    W, H, cell = 1280, 420, 21
    cols = (off + len(days) + 6) // 7
    x0, y0 = (W - cols * cell) / 2, 168
    pos = lambda n: (x0 + (n // 7) * cell + cell / 2, y0 + (n % 7) * cell + cell / 2)

    # snake route: down column 0, up column 1, ...
    order = []
    for c in range(cols):
        rows = range(7) if c % 2 == 0 else range(6, -1, -1)
        order += [c * 7 + r for r in rows if 0 <= c * 7 + r - off < len(days)]
    step, pause = .055, 3.2
    run = step * (len(order) - 1)
    dur = run + pause
    frac = lambda k: k * step / dur
    pts = " L".join(f"{pos(n)[0]:.1f} {pos(n)[1]:.1f}" for n in order)

    hi = max(1, s["best"])
    dots, pops = [], []
    for k, n in enumerate(order):
        d, c = days[n - off]
        x, y = pos(n)
        t = frac(k)
        gone = f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{t:.4f};{min(t + .002, 1):.4f};1" dur="{dur:.2f}s" repeatCount="indefinite"/>'
        if c == 0:
            dots.append(f'<rect x="{x - 1.5:.1f}" y="{y - 1.5:.1f}" width="3" height="3" fill="#6d63a8">{gone}</rect>')
        else:
            lvl = c / hi
            r = 3 + 4.5 * min(1, lvl * 1.4)
            col = CYAN if lvl < .3 else PINK if lvl < .7 else GOLD
            extra = '<animate attributeName="fill-opacity" values="1;.35;1" dur=".5s" repeatCount="indefinite"/>' if lvl >= .7 else ""
            dots.append(f'<g>{gone}<rect x="{x - r:.1f}" y="{y - r:.1f}" width="{2 * r:.1f}" height="{2 * r:.1f}" rx="2" fill="{col}">{extra}</rect></g>')
            if c >= max(6, hi * .45):
                pops.append(f'<text x="{x:.0f}" y="{y - 14:.0f}" class="p" font-size="11" fill="{GOLD}" text-anchor="middle" opacity="0">+{c}'
                            f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;{t:.4f};{min(t + .004, 1):.4f};{min(t + .06, 1):.4f};1" dur="{dur:.2f}s" repeatCount="indefinite"/>'
                            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 -26;0 -26" keyTimes="0;{t:.4f};{min(t + .06, 1):.4f};1" dur="{dur:.2f}s" repeatCount="indefinite"/></text>')

    def mover(body, lag, extra=""):
        a, b = frac(lag), min(1, frac(lag) + run / dur)
        return (f'<g{extra}>{body}<animateMotion dur="{dur:.2f}s" repeatCount="indefinite" rotate="auto" path="M{pts}" '
                f'keyPoints="0;0;1;1" keyTimes="0;{a:.4f};{b:.4f};1" calcMode="linear"/></g>')

    ghosts = "".join(mover(f'<g opacity=".55">{bus_top(c, True)}<animate attributeName="opacity" values=".55;.15;.55;.4;.55" dur="{1.1 + i * .3:.1f}s" repeatCount="indefinite"/></g>', lag)
                     for i, (c, lag) in enumerate(((VIOLET, 9), (PINK, 15), (CYAN, 21))))
    me = mover(bus_top(GOLD), 0)

    # months under the grid
    months, seen = [], set()
    for i, (d, _) in enumerate(days):
        dd = dt.date.fromisoformat(d)
        if dd.day <= 7 and dd.month not in seen and (i + off) % 7 == 0:
            seen.add(dd.month)
            months.append(f'<text x="{pos(i + off)[0] - cell / 2:.0f}" y="{y0 + 7 * cell + 30}" class="p" font-size="11" fill="{SOFT}">{dd.strftime("%b").upper()}</text>')

    fw, fh = cols * cell + 24, 7 * cell + 24
    frame = (f'<rect x="{x0 - 12}" y="{y0 - 12}" width="{fw}" height="{fh}" rx="10" fill="none" stroke="{WALL}" stroke-width="4">'
             f'<animate attributeName="stroke" values="{WALL};{WALL};#fff;{WALL};#fff;{WALL}" keyTimes="0;{frac(len(order) + 4):.4f};{frac(len(order) + 8):.4f};{frac(len(order) + 14):.4f};{frac(len(order) + 20):.4f};1" calcMode="discrete" dur="{dur:.2f}s" repeatCount="indefinite"/></rect>'
             f'<rect x="{x0 - 5}" y="{y0 - 5}" width="{fw - 14}" height="{fh - 14}" rx="6" fill="none" stroke="{WALL}" stroke-opacity=".55" stroke-width="2"/>')
    clear_t = frac(len(order) + 2)
    clear = (f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{clear_t:.4f};{clear_t + .005:.4f};.985;1" dur="{dur:.2f}s" repeatCount="indefinite"/>'
             f'<rect x="{W / 2 - 250}" y="{y0 + 7 * cell / 2 - 34}" width="500" height="68" rx="8" fill="{INK}" stroke="{GOLD}" stroke-width="3"/>'
             f'<text x="{W / 2}" y="{y0 + 7 * cell / 2 + 10}" class="p" font-size="24" fill="{GOLD}" text-anchor="middle">ROUTE COMPLETE!{blink(".5s")}</text></g>')

    prog = (f'<rect x="{x0}" y="122" width="{cols * cell}" height="8" rx="4" fill="#24164d"/>'
            f'<rect x="{x0}" y="122" width="0" height="8" rx="4" fill="{GOLD}"><animate attributeName="width" values="0;{cols * cell};{cols * cell}" keyTimes="0;{run / dur:.4f};1" dur="{dur:.2f}s" repeatCount="indefinite"/></rect>')
    hud = "".join(f'<text x="{x}" y="64" class="p" font-size="13" fill="{PINK}" text-anchor="{a}">{k}<tspan x="{x}" y="96" font-size="22" fill="#fff">{v}</tspan></text>'
                  for x, a, k, v in ((W - x0 - 330, "end", "STOPS", f"{s['total']:,}"), (W - x0 - 170, "end", "STREAK", f"{s['streak']}D"),
                                     (W - x0, "end", "BEST DAY", f"{s['best']}")))
    body = f'''<rect width="{W}" height="{H}" rx="18" fill="{INK}"/>
<text x="{x0}" y="70" class="p" font-size="28" fill="#fff">ROUTE 365</text>
<text x="{x0}" y="102" class="s" font-size="17" fill="{SOFT}">My last year on GitHub. Every stop is a day, bigger stops mean busier days.</text>
{hud}{prog}
{frame}{''.join(dots)}{''.join(pops)}{ghosts}{me}{''.join(months)}{clear}
<text x="{x0}" y="{H - 26}" class="s" font-size="15" fill="{SOFT}">{s['active']} active days · longest streak {s['longest']} days · redrawn daily from my real activity</text>
<text x="{W - x0}" y="{H - 26}" class="p" font-size="11" fill="{VIOLET}" text-anchor="end">GHOST BUSES CHASING</text>
{crt(W, H, 18)}'''
    return svg(W, H, body, f"My last year on GitHub as a bus route: {s['total']} contributions over {s['active']} active days, "
               f"best day {s['best']}, current streak {s['streak']} days.")


# ---------------------------------------------------------------- the player card
def mascot(scale=1):
    """The Ghost Bus mascot: a friendly pixel ghost. 16 x 16 grid."""
    rows = ["....######......", "..##########....", ".############...", ".###..####..##..", "####..####..###.",
            "################", "################", "####.######.####", "#####......#####", "################",
            "################", "################", "################", "################", "##.###..###.###.", "#...#....#...#.."]
    eye = {(3, 4), (3, 5), (4, 4), (4, 5), (3, 10), (3, 11), (4, 10), (4, 11)}
    out = []
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == "#":
                out.append(f'<rect x="{x * scale}" y="{y * scale}" width="{scale}" height="{scale}" fill="#f6f1ff"/>')
            elif (y, x) in eye:
                out.append(f'<rect x="{x * scale}" y="{y * scale}" width="{scale}" height="{scale}" fill="{INK}"/>')
    out.append(f'<rect x="{4 * scale}" y="{4 * scale}" width="{scale}" height="{scale}" fill="{CYAN}"/><rect x="{10 * scale}" y="{4 * scale}" width="{scale}" height="{scale}" fill="{CYAN}"/>')
    out.append(f'<rect x="{1 * scale}" y="{7 * scale}" width="{2 * scale}" height="{scale}" fill="{PINK}" opacity=".7"/><rect x="{13 * scale}" y="{7 * scale}" width="{2 * scale}" height="{scale}" fill="{PINK}" opacity=".7"/>')
    return "".join(out)


LANG_COL = {"Python": "#3ff0ff", "JavaScript": "#ffe14d", "TypeScript": "#6cb8ff", "HTML": "#ff8a3d", "Java": "#ff3fa4",
            "CSS": "#b49cff", "Jupyter Notebook": "#f08cff", "Shell": "#4fd1a5", "HCL": "#9b8cff", "Dockerfile": "#3fa9ff"}


def player_svg(data, s):
    W, H = 1280, 440
    bars = []
    rows = (("CONTRIBUTIONS", s["total"], 500), ("ACTIVE DAYS", s["active"], 200), ("CURRENT STREAK", s["streak"], 30),
            ("LONGEST STREAK", s["longest"], 30), ("PUBLIC REPOS", data["repos"], 30))
    for i, (k, v, top) in enumerate(rows):
        y = 186 + i * 44
        segs = 20
        on = max(1, min(segs, round(segs * v / top)))
        cells = "".join(f'<rect x="{620 + j * 15}" y="{y - 16}" width="11" height="18" fill="{(CYAN if j < segs * .5 else GOLD if j < segs * .8 else PINK) if j < on else "#24164d"}" opacity="{0 if j < on else 1}">'
                        + (f'<animate attributeName="opacity" values="0;1" begin="{.4 + i * .15 + j * .03:.2f}s" dur=".01s" fill="freeze"/>' if j < on else "")
                        + "</rect>" for j in range(segs))
        bars.append(f'<text x="390" y="{y}" class="p" font-size="13" fill="{SOFT}">{k}</text>{cells}'
                    f'<text x="935" y="{y}" class="p" font-size="15" fill="#fff" text-anchor="end">{v:,}</text>')
    langs = sorted(data["langs"].items(), key=lambda kv: -kv[1])[:5]
    tot = sum(v for _, v in data["langs"].items()) or 1
    pw = []
    for i, (k, v) in enumerate(langs):
        y, share = 186 + i * 44, v / tot
        col = LANG_COL.get(k, VIOLET)
        pw.append(f'<rect x="990" y="{y - 14}" width="14" height="14" fill="{col}"/>'
                  f'<text x="1014" y="{y}" class="p" font-size="12" fill="#fff">{k.upper()[:12]}</text>'
                  f'<text x="1232" y="{y}" class="p" font-size="12" fill="{col}" text-anchor="end">{share:.0%}</text>'
                  f'<rect x="990" y="{y + 8}" width="242" height="5" fill="#24164d"/>'
                  f'<rect x="990" y="{y + 8}" width="0" height="5" fill="{col}"><animate attributeName="width" from="0" to="{242 * share:.0f}" begin="{.6 + i * .15:.2f}s" dur=".8s" fill="freeze"/></rect>')
    xpw = 545
    body = f'''<rect width="{W}" height="{H}" rx="18" fill="#160a33"/>
<rect x="40" y="40" width="300" height="360" rx="12" fill="{INK}" stroke="{PINK}" stroke-width="3"/>
<g><g transform="translate(110 90)">{mascot(10)}</g>
<animateTransform attributeName="transform" type="translate" values="0 0;0 -10;0 0" dur="2.4s" repeatCount="indefinite"/></g>
<ellipse cx="190" cy="282" rx="60" ry="8" fill="#000" opacity=".45"><animate attributeName="rx" values="60;46;60" dur="2.4s" repeatCount="indefinite"/></ellipse>
<text x="190" y="334" class="p" font-size="16" fill="#fff" text-anchor="middle">MOHAMMED</text>
<text x="190" y="364" class="p" font-size="11" fill="{CYAN}" text-anchor="middle">CLASS: ML ENGINEER</text>
<text x="390" y="78" class="p" font-size="13" fill="{PINK}">PLAYER 1</text>
<text x="390" y="116" class="p" font-size="30" fill="#fff">LEVEL {s['level']}</text>
<rect x="390" y="132" width="{xpw}" height="12" rx="3" fill="#24164d"/>
<rect x="390" y="132" width="0" height="12" rx="3" fill="{GOLD}"><animate attributeName="width" from="0" to="{xpw * s['xp']:.0f}" begin=".2s" dur="1.2s" fill="freeze"/></rect>
<text x="{390 + xpw}" y="116" class="p" font-size="11" fill="{SOFT}" text-anchor="end">{s['to_next']} XP TO LEVEL {s['level'] + 1}</text>
{''.join(bars)}
<text x="990" y="78" class="p" font-size="13" fill="{PINK}">POWER-UPS</text>
<text x="990" y="116" class="s" font-size="16" fill="{SOFT}">Languages in my public code</text>
{''.join(pw)}
<text x="1232" y="{H - 26}" class="p" font-size="11" fill="{GOLD}" text-anchor="end">READY!{blink(".9s")}</text>
{crt(W, H, 18)}'''
    lang_txt = ", ".join(f"{k} {v / tot:.0%}" for k, v in langs)
    return svg(W, H, body, f"Player card. Level {s['level']}. {s['total']} contributions, {s['active']} active days, current streak {s['streak']} days, "
               f"{data['repos']} public repos. Languages: {lang_txt}.")


def main():
    if "--from" in sys.argv:
        data = json.load(open(sys.argv[sys.argv.index("--from") + 1]))
    else:
        try:
            data = fetch()
        except Exception as e:              # keep yesterday's pictures rather than break the README
            print("fetch failed, keeping the old pictures:", e)
            return
    s = stats(data)
    for name, text in (("year.svg", year_svg(data, s)), ("player.svg", player_svg(data, s))):
        open(os.path.join(ROOT, "assets", name), "w", encoding="utf-8").write(text)
    print("level", s["level"], "total", s["total"], "streak", s["streak"])


if __name__ == "__main__":
    main()
