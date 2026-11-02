"""Shared pieces for the arcade-style SVGs: the embedded pixel font, colours, CRT overlay."""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = base64.b64encode(open(os.path.join(HERE, "..", "assets", "pixel.woff2"), "rb").read()).decode()

INK = "#0d0620"      # screen black-violet
SHELL = "#22124a"    # cabinet plastic
PINK = "#ff3fa4"
CYAN = "#3ff0ff"
GOLD = "#ffe14d"
SOFT = "#c9c3e6"
SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"


def svg(w, h, body, label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">
<defs>
<style>@font-face{{font-family:P;src:url(data:font/woff2;base64,{FONT}) format("woff2")}}.p{{font-family:P,monospace}}.s{{font-family:{SANS}}}</style>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" fill-opacity=".22"/></pattern>
<radialGradient id="vig" cx="50%" cy="50%" r="75%"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
</defs>
{body}
</svg>
'''


def crt(w, h, rx=0):
    return (f'<rect width="{w}" height="{h}" rx="{rx}" fill="url(#scan)" pointer-events="none"/>'
            f'<rect width="{w}" height="{h}" rx="{rx}" fill="url(#vig)" pointer-events="none"/>')


def blink(dur="1.1s"):
    return f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.55;.56;1" dur="{dur}" repeatCount="indefinite"/>'
