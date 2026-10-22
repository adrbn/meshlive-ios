"""Regenerates the README art in docs/assets/ from real Mac captures in docs/assets/readme-src/.

    python3 docs/assets/make_svgs.py

The captures are the Mac app launched with `-NearbyFixture populated` (made-up people and streams, no real IDs).
Everything is SMIL crossfades between embedded JPEGs, so it renders inside GitHub's <img> sandbox.
"""
import base64
from pathlib import Path

OUT = Path(__file__).parent
SRC = OUT / "readme-src"
FONT = "-apple-system,BlinkMacSystemFont,'SF Pro Text','Segoe UI',Helvetica,Arial,sans-serif"
RED = "#E5484D"  # liveRed, Design/design-tokens.json
DARK = {"bg": "#0d1117", "ink": "#ffffff", "dim": "#8E8E93", "edge": "#30363d"}
LIGHT = {"bg": "#ffffff", "ink": "#000000", "dim": "#6e6e73", "edge": "#d0d7de"}
HOLD, FADE = 3.2, 0.8  # seconds per screen, crossfade


def uri(name: str, kind: str = "jpeg") -> str:
    return f"data:image/{kind};base64," + base64.b64encode((SRC / name).read_bytes()).decode()


def svg(w: int, h: int, body: str, title: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n')


def fades(n: int) -> tuple[float, list[str]]:
    """Opacity animations for layers 1..n-1 over a static layer 0: each fades in on top, drops once covered,
    and the last fades out to reveal layer 0 again, so the loop is seamless and complete at t=0."""
    total = n * (HOLD + FADE)
    out = []
    for i in range(1, n):
        s = i * (HOLD + FADE) - FADE
        end = s + HOLD + 2 * FADE if i < n - 1 else total
        pts = [(0, 0), (s, 0), (s + FADE, 1), (end - FADE if i == n - 1 else end, 1)]
        pts += [(total, 0)] if i == n - 1 else [(end, 0), (total, 0)]
        kt = ";".join(f"{t / total:.4f}" for t, _ in pts)
        vs = ";".join(str(v) for _, v in pts)
        out.append(f'<animate attributeName="opacity" dur="{total}s" repeatCount="indefinite" keyTimes="{kt}" values="{vs}"/>')
    return total, out


def stack(names: list[str], x: float, y: float, w: float, h: float, view: tuple, clip: str) -> str:
    """Crossfading captures, each cropped to `view` (x, y, w, h in 1024x768 capture pixels)."""
    vx, vy, vw, vh = view
    sx, sy = w / vw, h / vh
    _, anims = fades(len(names))
    layers = []
    for i, n in enumerate(names):
        a = anims[i - 1] if i else ""
        layers.append(f'<g opacity="{0 if i else 1}">{a}<image width="1024" height="768" xlink:href="{uri(n + ".jpg")}" '
                      f'transform="translate({x - vx * sx:.2f} {y - vy * sy:.2f}) scale({sx:.4f} {sy:.4f})"/></g>')
    return f'<g clip-path="url(#{clip})">{"".join(layers)}</g>'


HERO = [("live", "Live nearby"), ("people", "Recent calls"), ("call-incoming", "Incoming call"),
        ("call-active", "In a call"), ("golive", "Go live")]


def hero(c: dict) -> str:
    w, h, pad = 1200, 640, 24
    ww, wh = 792, 594
    names = [n for n, _ in HERO]
    total, _ = fades(len(names))
    win = stack(names, pad, pad, ww, wh, (0, 0, 1024, 768), "win")
    tx = pad + ww + 48
    rows = "".join(f'<text x="{tx + 22}" y="{330 + i * 40}" font-size="19" font-weight="600" fill="{c["ink"]}">{label}</text>'
                   for i, (_, label) in enumerate(HERO))
    body = f"""<rect width="{w}" height="{h}" fill="{c['bg']}"/>
<defs><clipPath id="win"><rect x="{pad}" y="{pad}" width="{ww}" height="{wh}" rx="11"/></clipPath></defs>
{win}<rect x="{pad + .5}" y="{pad + .5}" width="{ww - 1}" height="{wh - 1}" rx="11" fill="none" stroke="{c['edge']}"/>
<clipPath id="icon"><rect x="{tx}" y="96" width="112" height="112" rx="25"/></clipPath>
<image x="{tx}" y="96" width="112" height="112" clip-path="url(#icon)" xlink:href="{uri('icon.png', 'png')}"/>
<rect x="{tx + .5}" y="96.5" width="111" height="111" rx="24.5" fill="none" stroke="{c['edge']}"/>
<g font-family="{FONT}">
<text x="{tx}" y="258" font-size="40" font-weight="700" fill="{c['ink']}">MeshLive</text>
<text x="{tx}" y="290" font-size="19" fill="{c['dim']}">for iPhone and Mac</text>
{rows}
<circle cx="{tx + 6}" cy="324" r="5" fill="{RED}"><animate attributeName="cy" dur="{total}s" repeatCount="indefinite" calcMode="spline"
 keyTimes="{';'.join(f'{t:.4f}' for t in keyframes(total))}" values="{';'.join(str(v) for v in cy_values())}"
 keySplines="{';'.join(['.4 0 .2 1'] * (len(cy_values()) - 1))}"/></circle>
<text x="{tx}" y="{h - 40}" font-size="15" fill="{c['dim']}">Real captures, made-up people.</text>
</g>"""
    return svg(w, h, body, "MeshLive on the Mac: live streams nearby, recent calls with a missed call in red, an incoming call, a call in progress and the Go live sheet")


def keyframes(total: float) -> list[float]:
    ts = [0.0]
    for i in range(1, len(HERO)):
        s = i * (HOLD + FADE) - FADE
        ts += [s / total, (s + FADE) / total]
    return ts + [(total - FADE) / total, 1.0]


def cy_values() -> list[int]:
    vs = [324]
    for i in range(1, len(HERO)):
        vs += [324 + (i - 1) * 40, 324 + i * 40]
    return vs + [324 + (len(HERO) - 1) * 40, 324]


CARDS = {
    "mac": (["live", "contacts"], (0, 0, 640, 480), "A real Mac app"),
    "calls": (["call-incoming", "call-active"], (192, 248, 640, 480), "Calls, no internet"),
    "missed": (["people"], (240, 20, 640, 480), "Missed calls in red"),
    "golive": (["golive"], (190, 150, 640, 480), "Go live: video or radio"),
    "background": (["experiments", "experiments-on"], (240, 10, 560, 420), "Reachable in the background"),
    "people": (["contacts"], (236, 0, 640, 480), "Contacts, one tap to call"),
}


def card(key: str) -> str:
    names, view, title = CARDS[key]
    w, h, m, ih = 400, 352, 12, 282
    pics = stack(names, m, m, w - 2 * m, ih, view, f"c-{key}")
    body = f"""<rect width="{w}" height="{h}" rx="14" fill="#0d1117"/><rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="13.5" fill="none" stroke="#30363d"/>
<defs><clipPath id="c-{key}"><rect x="{m}" y="{m}" width="{w - 2 * m}" height="{ih}" rx="8"/></clipPath></defs>{pics}
<text x="{w / 2}" y="{m + ih + 38}" text-anchor="middle" font-family="{FONT}" font-size="19" font-weight="600" fill="#fff">{title}</text>"""
    return svg(w, h, body, title)


ICONS = {  # 24-unit stroke icons
    "build": "M8 6l-6 6 6 6M16 6l6 6-6 6",
    "adds": "M12 5v14M5 12h14",
    "status": "M12 3l9 16H3zM12 10v4M12 17v.5",
    "upstream": "M7 17L17 7M9 7h8v8",
}
BUTTONS = {"build": ("Build it", "Compiler"), "adds": ("What it adds", "Ce qu'il ajoute"),
           "status": ("Status", "État"), "upstream": ("Upstream", "Projet d'origine")}


def button(icon: str, label: str, primary: bool) -> str:
    tw = len(label) * 9.2
    w, h = round(tw + 72), 48
    bg, fg, edge = ("#ffffff", "#000000", "#d0d7de") if primary else ("#0d1117", "#ffffff", "#30363d")
    body = f"""<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{h / 2 - .5}" fill="{bg}" stroke="{edge}"/>
<path transform="translate(20 14) scale(.83)" d="{ICONS[icon]}" fill="none" stroke="{RED if not primary else fg}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
<text x="50" y="30.5" font-family="{FONT}" font-size="16" font-weight="600" fill="{fg}">{label}</text>"""
    return svg(w, h, body, label)


def main() -> None:
    files = {"hero.svg": hero(DARK), "hero-light.svg": hero(LIGHT)}
    files.update({f"card-{k}.svg": card(k) for k in CARDS})
    for k, (en, fr) in BUTTONS.items():
        files[f"btn-{k}.svg"] = button(k, en, k == "build")
        files[f"btn-{k}-fr.svg"] = button(k, fr, k == "build")
    for name, text in files.items():
        (OUT / name).write_text(text)
        print(f"{name:24} {len(text.encode()) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
