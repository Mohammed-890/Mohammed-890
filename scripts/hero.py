"""The title screen: CRT power-on, neon sun over a moving grid, name drops in letter by letter, roles type
themselves out, and a bus races along the horizon with ghosts on its tail."""
import random

from pixel import CYAN, GOLD, INK, PINK, SOFT, blink, crt, svg

W, H = 1280, 640
HZ = 404                 # horizon
ROLES = ["AI + MACHINE LEARNING ENGINEER", "MLOPS: TRAIN, SHIP, MONITOR", "ARABIC + ENGLISH AI TOOLS",
         "FOUNDER, ORVO AI", "CS WITH AI, SHEFFIELD HALLAM"]


def side_bus(color):
    win = "".join(f'<rect x="{6 + i * 11}" y="4" width="8" height="7" fill="#1a1036"/>' for i in range(4))
    return (f'<rect width="60" height="19" rx="3" fill="{color}"/>{win}<rect x="51" y="4" width="6" height="11" fill="#1a1036"/>'
            f'<rect x="57" y="13" width="3" height="3" fill="#fff6b0"/><rect x="8" y="16" width="8" height="7" rx="2" fill="#120826"/>'
            f'<rect x="42" y="16" width="8" height="7" rx="2" fill="#120826"/>')


def ghost(color, s=3):
    rows = ["..####..", ".######.", "##.##.##", "########", "########", "#.##.##."]
    px = "".join(f'<rect x="{x * s}" y="{y * s}" width="{s}" height="{s}" fill="{color}"/>'
                 for y, r in enumerate(rows) for x, c in enumerate(r) if c == "#")
    return px + f'<rect x="{2 * s}" y="{2 * s}" width="{s}" height="{s}" fill="#fff"/><rect x="{5 * s}" y="{2 * s}" width="{s}" height="{s}" fill="#fff"/>'


def hero():
    rnd = random.Random(11)
    stars = "".join(
        f'<rect x="{rnd.randrange(W)}" y="{rnd.randrange(HZ - 60)}" width="{s}" height="{s}" fill="#fff" opacity="{rnd.uniform(.3, .9):.2f}">'
        + (f'<animate attributeName="opacity" values=".9;.1;.9" dur="{rnd.uniform(1.5, 4):.1f}s" repeatCount="indefinite"/>' if rnd.random() < .35 else "")
        + "</rect>" for s in (rnd.choice((2, 2, 2, 3)) for _ in range(110)))
    shooting = "".join(
        f'<g opacity="0"><line x1="0" y1="0" x2="-90" y2="-30" stroke="url(#trail)" stroke-width="3"/>'
        f'<animateTransform attributeName="transform" type="translate" values="{x} {y};{x + 360} {y + 120};{x + 360} {y + 120}" keyTimes="0;{1.1 / rep:.3f};1" dur="{rep}s" begin="{b}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;1;0;0" keyTimes="0;.02;{1.1 / rep:.3f};1" dur="{rep}s" begin="{b}s" repeatCount="indefinite"/></g>'
        for x, y, b, rep in ((180, 60, 2.5, 7), (760, 40, 6, 9)))

    # sun with retro cut lines that drift upward
    cuts = "".join(f'<rect x="440" y="{HZ - 120 + i * 22}" width="400" height="{3 + i * 2}" fill="#2a0c4a">'
                   f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -22" dur="2.6s" repeatCount="indefinite"/></rect>'
                   for i in range(7))
    sun = (f'<circle cx="640" cy="{HZ - 70}" r="170" fill="url(#sun)" opacity=".95"/>'
           f'<g clip-path="url(#sunclip)">{cuts}</g>')

    # skyline silhouette on the horizon, a few windows flicker
    x, city = 0, []
    while x < W:
        bw, bh = rnd.randrange(40, 100), rnd.randrange(24, 92)
        if 470 < x < 810:
            bh = rnd.randrange(14, 40)
        top = HZ - bh
        city.append(f'<rect x="{x}" y="{top}" width="{bw}" height="{bh}" fill="#16072e"/>')
        for wy in range(top + 8, HZ - 6, 14):
            for wx in range(x + 6, x + bw - 8, 12):
                r = rnd.random()
                if r < .22:
                    a = (f'<animate attributeName="opacity" values="1;1;0;1" keyTimes="0;.7;.71;1" dur="{rnd.uniform(3, 9):.1f}s" repeatCount="indefinite"/>' if r < .05 else "")
                    city.append(f'<rect x="{wx}" y="{wy}" width="6" height="6" fill="{rnd.choice((GOLD, "#ffb35c", CYAN, PINK))}" opacity=".8">{a}</rect>')
        x += bw + rnd.randrange(0, 6)

    # perspective grid floor
    vx = "".join(f'<line x1="640" y1="{HZ}" x2="{640 + k * 150}" y2="{H}" />' for k in range(-12, 13))
    hz_lines = "".join(
        f'<line x1="0" x2="{W}" y1="{HZ}" y2="{HZ}"><animate attributeName="y1" values="{HZ};{H}" dur="2.4s" begin="{-i * .6:.1f}s" repeatCount="indefinite" calcMode="spline" keySplines=".55 0 1 .45" keyTimes="0;1"/>'
        f'<animate attributeName="y2" values="{HZ};{H}" dur="2.4s" begin="{-i * .6:.1f}s" repeatCount="indefinite" calcMode="spline" keySplines=".55 0 1 .45" keyTimes="0;1"/></line>'
        for i in range(4))
    floor = (f'<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#floor)"/>'
             f'<g stroke="{PINK}" stroke-width="2" opacity=".55">{vx}{hz_lines}</g>'
             f'<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#fog)"/>'
             f'<line x1="0" x2="{W}" y1="{HZ}" y2="{HZ}" stroke="{PINK}" stroke-width="3"/>')

    # the chase along the horizon: bus, then three ghosts, then it loops
    chase = (f'<g><g transform="translate(0 {HZ - 24})">{side_bus(GOLD)}</g>'
             f'<animateTransform attributeName="transform" type="translate" values="-80 0;{W + 280} 0" dur="8s" begin="2.2s" repeatCount="indefinite"/></g>'
             + "".join(f'<g><g transform="translate(0 {HZ - 20})">{ghost(c)}<animateTransform attributeName="transform" type="translate" values="0 {HZ - 20};0 {HZ - 26};0 {HZ - 20}" dur=".5s" begin="{i * .17:.2f}s" repeatCount="indefinite"/></g>'
                       f'<animateTransform attributeName="transform" type="translate" values="{-120 - i * 40} 0;{W + 160 - i * 40} 0" dur="8s" begin="2.2s" repeatCount="indefinite"/></g>'
                       for i, c in enumerate((PINK, CYAN, "#b49cff"))))

    # name: letters drop in one by one, then a colour-split glitch every few seconds
    def word(text, y, start, fs=84):
        out, x0 = [], 640 - len(text) * fs / 2
        for i, ch in enumerate(text):
            b = start + i * .07
            x = x0 + i * fs + fs / 2
            out.append(f'<text x="{x:.0f}" y="{y}" class="p" font-size="{fs}" text-anchor="middle" fill="#fff" stroke="#14062b" stroke-width="10" paint-order="stroke" stroke-linejoin="round" transform="translate(0 -700)">{ch}'
                       f'<animateTransform attributeName="transform" type="translate" values="0 -700;0 14;0 -8;0 0" keyTimes="0;.6;.8;1" dur=".55s" begin="{b:.2f}s" fill="freeze"/></text>')
        return "".join(out)

    def split(text, y, fs=84):
        return "".join(
            f'<text x="{640 + dx}" y="{y}" class="p" font-size="{fs}" text-anchor="middle" fill="{c}" opacity="0">{text}'
            f'<animate attributeName="opacity" values="0;.85;0;0;.85;0;0" keyTimes="0;.02;.04;.5;.52;.55;1" dur="3.7s" begin="2.4s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{-dx} 0;0 0" dur=".12s" repeatCount="indefinite"/></text>'
            for dx, c in ((-6, CYAN), (6, PINK)))

    title = split("MOHAMMED", 196) + split("BANABILH", 298) + word("MOHAMMED", 196, .7) + word("BANABILH", 298, 1.25)

    # roles type themselves out, one after another
    per, n = 3.4, len(ROLES)
    roles = []
    for i, r in enumerate(ROLES):
        a, b = i / n, (i + 1) / n
        w = len(r) * 22 + 10
        roles.append(f'<clipPath id="r{i}"><rect x="{640 - w / 2}" y="320" height="40" width="0">'
                     f'<animate attributeName="width" values="0;0;{w};{w};0;0" keyTimes="0;{a:.3f};{a + .45 / n:.3f};{b - .1 / n:.3f};{b - .02 / n:.3f};1" dur="{per * n}s" begin="1.9s" repeatCount="indefinite"/></rect></clipPath>'
                     f'<text x="640" y="350" class="p" font-size="22" text-anchor="middle" fill="{CYAN}" stroke="#14062b" stroke-width="6" paint-order="stroke" clip-path="url(#r{i})">{r}</text>')
    start_pill = (f'<g><rect x="520" y="{H - 92}" width="240" height="46" rx="6" fill="{INK}" stroke="{GOLD}" stroke-width="3" opacity=".9"/>'
                  f'<text x="640" y="{H - 61}" class="p" font-size="18" fill="{GOLD}" text-anchor="middle">PRESS START{blink(".9s")}</text></g>')

    power_on = (f'<rect width="{W}" height="{H}" fill="#000"><animate attributeName="opacity" values="1;1;0" keyTimes="0;.5;1" dur=".8s" fill="freeze"/></rect>'
                f'<rect x="0" y="{H / 2 - 2}" width="{W}" height="4" fill="#fff" opacity="0">'
                f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.6;1" dur=".6s" fill="freeze"/>'
                f'<animate attributeName="y" values="{H / 2 - 2};{H / 2 - 2};0" keyTimes="0;.5;1" dur=".6s" fill="freeze"/>'
                f'<animate attributeName="height" values="4;4;{H}" keyTimes="0;.5;1" dur=".6s" fill="freeze"/></rect>')

    body = f'''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a0420"/><stop offset=".5" stop-color="#250c4d"/><stop offset="1" stop-color="#5c1460"/></linearGradient>
<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD}"/><stop offset=".55" stop-color="#ff7a59"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a0a45"/><stop offset="1" stop-color="#07021a"/></linearGradient>
<linearGradient id="fog" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff3fa4" stop-opacity=".35"/><stop offset=".25" stop-color="#ff3fa4" stop-opacity="0"/></linearGradient>
<linearGradient id="trail" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="sunclip"><circle cx="640" cy="{HZ - 70}" r="170"/></clipPath>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
{stars}{shooting}{sun}{''.join(city)}{floor}{chase}
<g class="p" font-size="17">
  <text x="44" y="50" fill="{PINK}">1UP<tspan x="44" y="78" fill="#fff">PLAYER 1</tspan></text>
  <text x="640" y="50" fill="{PINK}" text-anchor="middle">HI-SCORE<tspan x="640" y="78" fill="#fff">6 GAMES SHIPPED</tspan></text>
  <text x="1236" y="50" fill="{PINK}" text-anchor="end">CREDIT<tspan x="1236" y="78" fill="#fff">01</tspan></text>
</g>
{title}
{''.join(roles)}
{start_pill}
{crt(W, H)}
{power_on}'''
    return svg(W, H, body, "Mohammed Banabilh: AI and machine learning engineer, MLOps, Arabic and English AI tools, founder of Orvo AI. Animated arcade title screen.")
