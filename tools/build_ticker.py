"""Builds assets/footer.svg, a scrolling ticker of projects, from assets/ticker.json.

The track holds the item list twice and scrolls by exactly half its own width
(CSS transform-box: fill-box), so the loop is seamless whatever the text length.
Usage: python tools/build_ticker.py
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
SECONDS_PER_ITEM = 9


def build() -> str:
    items = json.loads((ROOT / "assets" / "ticker.json").read_text(encoding="utf-8"))
    spans = "".join(
        f'<tspan fill="#1D9E75">▲ </tspan><tspan fill="#ffffff" font-weight="600">{escape(i["name"])}</tspan>'
        f'<tspan fill="#aab3c5">  {escape(i["metric"])}</tspan><tspan fill="#3a4357">      |      </tspan>'
        for i in items)
    duration = SECONDS_PER_ITEM * len(items)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="56" viewBox="0 0 1200 56">
<style>
  .track {{ transform-box: fill-box; animation: scroll {duration}s linear infinite; }}
  @keyframes scroll {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-50%); }} }}
  @media (prefers-reduced-motion: reduce) {{ .track {{ animation: none; }} }}
</style>
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#7F77DD"/><stop offset="1" stop-color="#1D9E75"/></linearGradient></defs>
<rect width="1200" height="56" fill="#0d1321"/>
<rect width="1200" height="2" fill="url(#g)"/>
<text class="track" x="0" y="35" font-family="{FONT}" font-size="15" letter-spacing="0.5" xml:space="preserve">{spans}{spans}</text>
</svg>
'''


if __name__ == "__main__":
    (ROOT / "assets" / "footer.svg").write_text(build(), encoding="utf-8")
    print("assets/footer.svg written")
