"""Draw the arcade-style profile art: attract screen, one cartridge per project, inventory, continue screen.

    python scripts/arcade.py      writes assets/arcade/*.svg
"""
import os
import random

from pixel import CYAN, GOLD, INK, PINK, SANS, SHELL, SOFT, blink, crt, svg

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "arcade")


def bus(color, w=120, h=46):
    """A pixel bus facing right, drawn from its top-left corner."""
    win = "".join(f'<rect x="{12 + i * 22}" y="8" width="16" height="14" fill="#1a1036"/>' for i in range(4))
    return (f'<rect width="{w}" height="{h - 8}" rx="6" fill="{color}"/>{win}'
            f'<rect x="{w - 18}" y="8" width="12" height="22" fill="#1a1036"/>'
            f'<rect x="{w - 6}" y="26" width="6" height="6" fill="#fff6b0"/>'
            f'<rect x="6" y="26" width="{w - 30}" height="4" fill="#000" fill-opacity=".18"/>'
            f'<rect x="16" y="{h - 14}" width="16" height="14" rx="3" fill="#120826"/>'
            f'<rect x="{w - 40}" y="{h - 14}" width="16" height="14" rx="3" fill="#120826"/>')


# ---------------------------------------------------------------- attract screen
def hero():
    W, H = 1280, 560
    rnd = random.Random(7)
    stars = "".join(
        f'<rect x="{rnd.randrange(W)}" y="{rnd.randrange(330)}" width="{s}" height="{s}" fill="#fff" opacity="{rnd.uniform(.3, .9):.2f}">'
        + (f'<animate attributeName="opacity" values=".9;.1;.9" dur="{rnd.uniform(1.5, 4):.1f}s" repeatCount="indefinite"/>' if rnd.random() < .3 else "")
        + "</rect>"
        for s in (rnd.choice((2, 2, 3, 4)) for _ in range(90)))
    # skyline
    x, city = 0, []
    while x < W:
        bw, bh = rnd.randrange(50, 120), rnd.randrange(40, 115)
        top = 470 - bh
        city.append(f'<rect x="{x}" y="{top}" width="{bw}" height="{bh}" fill="#1d0d3d"/>')
        for wy in range(top + 12, 455, 18):
            for wx in range(x + 8, x + bw - 10, 16):
                r = rnd.random()
                if r < .28:
                    anim = (f'<animate attributeName="opacity" values="1;1;0;1" keyTimes="0;.7;.71;1" dur="{rnd.uniform(3, 9):.1f}s" repeatCount="indefinite"/>'
                            if r < .05 else "")
                    city.append(f'<rect x="{wx}" y="{wy}" width="8" height="8" fill="{rnd.choice((GOLD, GOLD, "#ffb35c", CYAN))}" opacity=".85">{anim}</rect>')
        x += bw + rnd.randrange(0, 8)
    title = []
    for y, word in ((178, "MOHAMMED"), (272, "BANABILH")):
        for dx, col, extra in ((-4, CYAN, "0 0;-3 0;2 0;0 0;0 0;5 0;0 0"), (4, PINK, "0 0;3 0;-2 0;0 0;0 0;-5 0;0 0")):
            title.append(f'<text x="{640 + dx}" y="{y}" class="p" font-size="76" text-anchor="middle" fill="{col}" opacity=".8">{word}'
                         f'<animateTransform attributeName="transform" type="translate" values="{extra}" dur="2.3s" calcMode="discrete" repeatCount="indefinite"/></text>')
        title.append(f'<text x="640" y="{y}" class="p" font-size="76" text-anchor="middle" fill="#fff">{word}</text>')
    body = f'''<rect width="{W}" height="{H}" fill="#170a35"/>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#12082c"/><stop offset=".55" stop-color="#2c0f52"/><stop offset=".8" stop-color="#5a1663"/></linearGradient></defs>
{stars}
<circle cx="1100" cy="110" r="46" fill="#ffd6f0" opacity=".9"/><circle cx="1084" cy="98" r="10" fill="#f0b5d8"/><circle cx="1112" cy="128" r="7" fill="#f0b5d8"/>
{''.join(city)}
<rect y="470" width="{W}" height="90" fill="#0f0624"/>
<g fill="{GOLD}" opacity=".7"><g><animateTransform attributeName="transform" type="translate" from="0 0" to="-80 0" dur=".9s" repeatCount="indefinite"/>
{''.join(f'<rect x="{i * 80}" y="513" width="40" height="5"/>' for i in range(18))}</g></g>
<g><g transform="translate(0 474)">{bus(GOLD)}</g><animateTransform attributeName="transform" type="translate" values="-140 0;1300 0" dur="9s" repeatCount="indefinite"/></g>
<g opacity=".9"><g transform="translate(0 512) scale(-1 1) translate(-120 0)">{bus("#b49cff")}</g>
  <animateTransform attributeName="transform" type="translate" values="1300 0;-140 0" dur="11s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values=".9;.9;.15;.6;.05;.9" keyTimes="0;.35;.42;.47;.55;1" dur="11s" repeatCount="indefinite"/></g>
<g class="p" font-size="18">
  <text x="48" y="48" fill="{PINK}">1UP<tspan x="48" y="76" fill="#fff">PLAYER 1</tspan></text>
  <text x="640" y="48" fill="{PINK}" text-anchor="middle">HI-SCORE<tspan x="640" y="76" fill="#fff">6 GAMES SHIPPED</tspan></text>
  <text x="1232" y="48" fill="{PINK}" text-anchor="end">CREDIT<tspan x="1232" y="76" fill="#fff">00</tspan></text>
</g>
{''.join(title)}
<text x="640" y="328" class="p" font-size="18" text-anchor="middle" fill="{CYAN}">AI + MACHINE LEARNING ENGINEER</text>
<text x="640" y="362" class="s" font-size="19" font-weight="600" text-anchor="middle" fill="{SOFT}">I build AI that works in Arabic and English, then run it in production.</text>
<text x="640" y="414" class="p" font-size="22" text-anchor="middle" fill="{GOLD}">INSERT COIN{blink()}</text>
{crt(W, H)}'''
    return svg(W, H, body, "Mohammed Banabilh, AI and machine learning engineer. Arcade-style title screen.")


# ---------------------------------------------------------------- cartridges
def keyed(i, n, total, hold_to=.94):
    """opacity animation: element i of n appears in turn, all vanish at the end of the loop."""
    a = round(.06 + i * (.8 / n), 3)
    return (f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{a};{a + .02:.3f};{hold_to};1" '
            f'dur="{total}s" repeatCount="indefinite"/>')


def m_nahem(c):
    msgs = [(True, "عندكم مندي؟"), (False, "أكيد! مندي لحم ٤٥ ريال 🍖"), (True, "أبي واحد مع سلطة"),
            (False, "تم ✓ أرسلت طلبك على واتساب")]
    out = ['<rect width="560" height="240" fill="#1a0f12"/>',
           f'<rect x="0" y="0" width="560" height="34" fill="{c}" opacity=".9"/>',
           '<text x="280" y="23" class="s" font-size="15" font-weight="700" fill="#1a0f12" text-anchor="middle">مساعد نهم · Nahem</text>']
    for i, (me, t) in enumerate(msgs):
        y = 48 + i * 46
        w = 18 + len(t) * 10.5
        x = 560 - 20 - w if me else 20
        out.append(f'<g opacity="0">{keyed(i, 4, 8)}<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="34" rx="12" '
                   f'fill="{c if me else "#3a2a30"}"/><text x="{x + w / 2:.0f}" y="{y + 23}" class="s" font-size="16" '
                   f'fill="{"#1a0f12" if me else "#fff"}" text-anchor="middle" direction="rtl">{t}</text></g>')
    return "".join(out)


def m_showme(c):
    lines = "".join(f'<rect x="150" y="{36 + i * 24}" width="{w}" height="10" rx="2" fill="#d9d4f0" opacity=".85"/>'
                    for i, w in enumerate((200, 250, 170, 230, 140, 210, 190, 120)))
    return f'''<rect width="560" height="240" fill="#0e1f1a"/>
<rect x="130" y="18" width="300" height="214" rx="6" fill="#273a35"/>{lines}
<rect x="144" y="82" width="244" height="22" rx="3" fill="none" stroke="{c}" stroke-width="3" opacity="0">{keyed(0, 1, 4.5, .9)}</rect>
<g><rect x="120" y="0" width="320" height="6" fill="{c}"/><rect x="120" y="-40" width="320" height="40" fill="{c}" opacity=".15"/>
<animateTransform attributeName="transform" type="translate" values="0 20;0 230;0 20" dur="4.5s" repeatCount="indefinite"/></g>
<g opacity="0">{keyed(0, 1, 4.5, .9)}<rect x="400" y="70" width="140" height="46" rx="8" fill="{c}"/>
<text x="470" y="99" class="p" font-size="13" fill="{INK}" text-anchor="middle">AR&gt;EN</text></g>'''


def m_seat(c):
    rnd = random.Random(3)
    seats = []
    for r in range(7):
        for k in range(18):
            x, y = 34 + k * 28 + (r % 2) * 6, 70 + r * 22
            d = rnd.uniform(0, 5)
            seats.append(f'<rect x="{x}" y="{y}" width="20" height="14" rx="3" fill="#2b3b5c">'
                         + (f'<animate attributeName="fill" values="#2b3b5c;{c};#2b3b5c" dur="5s" begin="{d:.1f}s" repeatCount="indefinite"/>' if rnd.random() < .25 else "")
                         + "</rect>")
    return f'''<rect width="560" height="240" fill="#0c1428"/>
<rect x="60" y="14" width="440" height="40" rx="6" fill="#1e7a46"/><rect x="60" y="14" width="440" height="40" rx="6" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2"/>
<line x1="280" y1="14" x2="280" y2="54" stroke="#fff" stroke-opacity=".5" stroke-width="2"/>
{''.join(seats)}
<g><path d="M0 -26 C-14 -26 -14 -8 0 6 C14 -8 14 -26 0 -26Z" fill="{GOLD}"/><circle cy="-17" r="5" fill="{INK}"/>
<animateTransform attributeName="transform" type="translate" values="300 128;300 118;300 128" dur=".8s" repeatCount="indefinite"/></g>'''


def m_football(c):
    stripes = "".join(f'<rect x="{i * 70}" y="0" width="35" height="240" fill="#fff" opacity=".04"/>' for i in range(8))
    return f'''<rect width="560" height="240" fill="#14532d"/>{stripes}
<rect x="10" y="10" width="540" height="220" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2"/>
<line x1="280" y1="10" x2="280" y2="230" stroke="#fff" stroke-opacity=".5" stroke-width="2"/><circle cx="280" cy="120" r="34" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2"/>
<rect x="514" y="84" width="36" height="72" fill="none" stroke="#fff" stroke-width="4"/>
<path id="kick" d="M120 170 Q 330 -20 532 118" fill="none"/>
<g><rect x="-7" y="-7" width="14" height="14" fill="#fff"/><rect x="-3" y="-3" width="6" height="6" fill="#222"/>
<animateMotion dur="2.6s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.6;1" calcMode="linear"><mpath href="#kick"/></animateMotion></g>
<g transform="translate(110 150)"><g><path d="M0 0 L-20 -16 L-18 8Z M0 0 L20 -16 L18 8Z" fill="{c}"/>
<animateTransform attributeName="transform" type="scale" values="1 1;.2 1;1 1" dur=".35s" repeatCount="indefinite"/></g><rect x="-2" y="-8" width="4" height="16" fill="#2a1030"/></g>
<text x="400" y="60" class="p" font-size="24" fill="{GOLD}" opacity="0">GOAL!<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.6;.62;.95;1" dur="2.6s" repeatCount="indefinite"/></text>'''


def m_worldcup(c):
    bars = "".join(
        f'<rect x="{330 + i * 62}" y="200" width="40" height="0" fill="{c}">'
        f'<animate attributeName="height" values="0;0;{h};{h};0" keyTimes="0;.55;.7;.95;1" dur="6s" repeatCount="indefinite"/>'
        f'<animate attributeName="y" values="200;200;{200 - h};{200 - h};200" keyTimes="0;.55;.7;.95;1" dur="6s" repeatCount="indefinite"/></rect>'
        for i, h in enumerate((150, 110, 90)))
    return f'''<rect width="560" height="240" fill="#1d1806"/>
<clipPath id="ty"><rect x="16" y="14" width="0" height="80"><animate attributeName="width" values="0;530;530;530" keyTimes="0;.4;.95;1" dur="6s" repeatCount="indefinite"/></rect></clipPath>
<g clip-path="url(#ty)" class="p" font-size="12"><text x="20" y="36" fill="#fff">&gt; top scorers in finals?</text>
<text x="20" y="62" fill="{c}">SELECT player, SUM(goals)</text><text x="20" y="84" fill="{c}">FROM finals GROUP BY 1</text></g>
<line x1="310" y1="200" x2="540" y2="200" stroke="#fff" stroke-opacity=".4" stroke-width="2"/>{bars}
<text x="20" y="200" class="p" font-size="12" fill="#fff" opacity="0">3 ROWS ✓<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.5;.52;.95;1" dur="6s" repeatCount="indefinite"/></text>'''


def m_ghost(c):
    return f'''<rect width="560" height="240" fill="#0d0a24"/>
<circle cx="470" cy="50" r="22" fill="#ffd6f0" opacity=".8"/>
<rect y="186" width="560" height="54" fill="#170f33"/>
<g fill="{GOLD}" opacity=".6">{''.join(f'<rect x="{i * 60}" y="210" width="30" height="4"/>' for i in range(10))}</g>
<rect x="400" y="96" width="6" height="92" fill="#8a84b0"/><rect x="380" y="84" width="46" height="30" rx="4" fill="{GOLD}"/>
<text x="403" y="105" class="p" font-size="12" fill="{INK}" text-anchor="middle">115</text>
<g><g transform="translate(0 142)">{bus(c)}</g>
<animateTransform attributeName="transform" type="translate" values="-140 0;600 0" dur="6s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="1;1;.2;.7;0;0;1" keyTimes="0;.3;.38;.42;.5;.98;1" dur="6s" repeatCount="indefinite"/></g>
<text x="440" y="74" class="p" font-size="34" fill="#fff" opacity="0">?<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.5;.52;.95;1" dur="6s" repeatCount="indefinite"/></text>
<text x="20" y="34" class="p" font-size="11" fill="{SOFT}">DUE 23:38</text><text x="20" y="54" class="p" font-size="11" fill="{c}">SEEN: ---<animate attributeName="opacity" values="1;0" dur=".6s" calcMode="discrete" repeatCount="indefinite"/></text>'''


GAMES = [
    ("nahem", "NAHEM", "Arabic ordering chatbot for a restaurant in Madinah", "PLAY DEMO", "#ff8a3d", m_nahem),
    ("show-me", "SHOW ME", "Point your camera at Arabic text, read it in English", "PLAY DEMO", "#4fd1a5", m_showme),
    ("seat-scout", "SEAT SCOUT", "AI agent that finds the best seat in the stadium", "VIEW CODE", "#6cb8ff", m_seat),
    ("football", "BUTTERFLY FX", "Change one match, simulate the whole season", "WATCH", "#f08cff", m_football),
    ("worldcup", "WC DATA CHAT", "Ask World Cup history in plain English, get SQL", "VIEW CODE", "#ffd84d", m_worldcup),
    ("ghost-bus", "GHOST BUS", "Finds Sheffield buses that never turned up, live", "LIVE NOW", "#b49cff", m_ghost),
]


def cartridge(n, slug, title, line, cta, c, motif):
    W, H = 640, 430
    ridges = "".join(f'<rect x="{200 + i * 24}" y="22" width="12" height="6" rx="2" fill="#000" opacity=".25"/>' for i in range(10))
    body = f'''<defs><clipPath id="lab"><rect width="560" height="240" rx="8"/></clipPath>
<linearGradient id="sh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2d1960"/><stop offset="1" stop-color="{SHELL}"/></linearGradient></defs>
<path d="M24 6 H616 a18 18 0 0 1 18 18 V412 a12 12 0 0 1 -12 12 H18 a12 12 0 0 1 -12 -12 V24 a18 18 0 0 1 18 -18Z" fill="url(#sh)" stroke="{c}" stroke-width="3"/>
{ridges}
<g transform="translate(40 44)"><g clip-path="url(#lab)">{motif(c)}{crt(560, 240, 8)}</g>
<rect width="560" height="240" rx="8" fill="none" stroke="#000" stroke-opacity=".5" stroke-width="4"/></g>
<text x="40" y="320" class="p" font-size="13" fill="{c}">STAGE {n}</text>
<text x="600" y="320" class="p" font-size="13" fill="{GOLD}" text-anchor="end">▶ {cta}<animate attributeName="opacity" values="1;1;.25;.25" keyTimes="0;.6;.61;1" dur="1.2s" repeatCount="indefinite"/></text>
<text x="40" y="360" class="p" font-size="26" fill="#fff">{title}</text>
<text x="40" y="396" class="s" font-size="19" fill="{SOFT}">{line}</text>'''
    return svg(W, H, body, f"{title.title()}: {line}")


# ---------------------------------------------------------------- inventory
TOOLS = ["PYTHON", "SKLEARN", "PANDAS", "MLFLOW", "FASTAPI", "DOCKER", "K8S", "HELM",
         "TERRAFORM", "ARGO CD", "PROMETHEUS", "ACTIONS", "TYPESCRIPT", "SQL", "JAVA", "THREE.JS"]


def inventory():
    W, H = 1280, 330
    cols, sw, sh, gap = 8, 140, 92, 12
    x0, y0 = (W - (cols * sw + (cols - 1) * gap)) // 2, 84
    slots = []
    for i, t in enumerate(TOOLS):
        x, y = x0 + (i % cols) * (sw + gap), y0 + (i // cols) * (sh + gap)
        slots.append(f'<rect x="{x}" y="{y}" width="{sw}" height="{sh}" rx="6" fill="{INK}" stroke="#3b2a72" stroke-width="3"/>'
                     f'<rect x="{x + 10}" y="{y + 12}" width="18" height="18" fill="{(PINK, CYAN, GOLD, "#b49cff")[i % 4]}"/>'
                     f'<text x="{x + sw / 2}" y="{y + 66}" class="p" font-size="13" fill="#fff" text-anchor="middle">{t}</text>')
    pos = ";".join(f"{x0 + (i % cols) * (sw + gap) - 4} {y0 + (i // cols) * (sh + gap) - 4}" for i in range(len(TOOLS)))
    body = f'''<rect width="{W}" height="{H}" rx="18" fill="#160a33"/>
<text x="{x0}" y="54" class="p" font-size="22" fill="#fff">INVENTORY</text>
<text x="{W - x0}" y="54" class="s" font-size="17" fill="{SOFT}" text-anchor="end">Tools I've shipped real projects with</text>
{''.join(slots)}
<rect width="{sw + 8}" height="{sh + 8}" rx="8" fill="none" stroke="{GOLD}" stroke-width="4">
<animateTransform attributeName="transform" type="translate" values="{pos}" dur="{len(TOOLS) * .7}s" calcMode="discrete" repeatCount="indefinite"/></rect>
{crt(W, H, 18)}'''
    return svg(W, H, body, "Tools: " + ", ".join(t.title() for t in TOOLS))


# ---------------------------------------------------------------- continue screen
def cont():
    W, H = 1280, 300
    digits = "".join(
        f'<text x="640" y="196" class="p" font-size="72" fill="{GOLD}" text-anchor="middle" opacity="0">{9 - i}'
        f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;{i / 10:.1f};{(i + 1) / 10:.1f}" calcMode="discrete" dur="10s" repeatCount="indefinite"/></text>'
        if i else
        f'<text x="640" y="196" class="p" font-size="72" fill="{GOLD}" text-anchor="middle">9'
        f'<animate attributeName="opacity" values="1;0" keyTimes="0;.1" calcMode="discrete" dur="10s" repeatCount="indefinite"/></text>'
        for i in range(10))
    body = f'''<rect width="{W}" height="{H}" rx="18" fill="#160a33"/>
<text x="640" y="96" class="p" font-size="40" fill="#fff" text-anchor="middle">CONTINUE?</text>
{digits}
<text x="640" y="256" class="s" font-size="20" fill="{SOFT}" text-anchor="middle">Open to ML engineering and MLOps internships now, and graduate roles from July 2027.</text>
{crt(W, H, 18)}'''
    return svg(W, H, body, "Continue? Open to ML engineering and MLOps internships, and graduate roles from July 2027.")


def main():
    os.makedirs(OUT, exist_ok=True)
    files = {"title.svg": hero(), "inventory.svg": inventory(), "continue.svg": cont()}
    for n, g in enumerate(GAMES, 1):
        files[f"{g[0]}.svg"] = cartridge(n, *g)
    for name, text in files.items():
        open(os.path.join(OUT, name), "w", encoding="utf-8").write(text)
    print("wrote", ", ".join(files))


if __name__ == "__main__":
    main()
