"""Builds the pixel-art profile README assets (SVG) for github.com/mokiofficiial.

Run:  python gen.py
Everything is drawn as pixel blocks, same style as the Pixel Icons pack.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
os.makedirs(A, exist_ok=True)

# colours measured from the Moki mascot
YELLOW, YLINE, INK, CREAM, CLINE, RED, DRED, BROWN, MUTED, GREEN = (
    "#ecb61e", "#e2a912", "#141414", "#fdf6e8", "#efe3cc", "#ee5a44", "#d9443a", "#5e3a1e", "#7a6250", "#7a8b3e")
import base64  # noqa: E402
from sprite import svg_rects, SW, SH  # noqa: E402
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

# 5x5 block font
_F = """
A .###. #...# ##### #...# #...#
B ####. #...# ####. #...# ####.
C .#### #.... #.... #.... .####
D ####. #...# #...# #...# ####.
E ##### #.... ####. #.... #####
F ##### #.... ####. #.... #....
G .#### #.... #..## #...# .###.
H #...# #...# ##### #...# #...#
I ##### ..#.. ..#.. ..#.. #####
K #...# #..#. ###.. #..#. #...#
L #.... #.... #.... #.... #####
M #...# ##.## #.#.# #...# #...#
N #...# ##..# #.#.# #..## #...#
O .###. #...# #...# #...# .###.
P ####. #...# ####. #.... #....
R ####. #...# ####. #..#. #...#
S .#### #.... .###. ....# ####.
T ##### ..#.. ..#.. ..#.. ..#..
U #...# #...# #...# #...# .###.
V #...# #...# #...# .#.#. ..#..
W #...# #...# #.#.# ##.## #...#
X #...# .#.#. ..#.. .#.#. #...#
Y #...# .#.#. ..#.. ..#.. ..#..
0 .###. #..## #.#.# ##..# .###.
1 ..#.. .##.. ..#.. ..#.. .###.
2 ####. ....# .###. #.... #####
3 ####. ....# .###. ....# ####.
4 #...# #...# ##### ....# ....#
5 ##### #.... ####. ....# ####.
6 .###. #.... ####. #...# .###.
7 ##### ....# ...#. ..#.. ..#..
8 .###. #...# .###. #...# .###.
9 .###. #...# .#### ....# .###.
. ..... ..... ..... ..... ..#..
"""
FONT = {}
for _l in _F.strip().split("\n"):
    k, *rows = _l.split()
    FONT[k] = [(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == "#"]


def art(s):
    return [(x, y, c) for y, r in enumerate(s.strip("\n").split("\n")) for x, c in enumerate(r) if c != "."]


# 11x11 project glyphs, same grid + stroke as the icon pack
GLYPHS = {
    "knight": """
...####....
..#....#...
.#..#...#..
#.......#..
#..##....#.
.##.#....#.
...#.....#.
..#......#.
..#......#.
.#........#
.##########
""",
    "pack": """
#####.#####
#...#.#...#
#...#.#...#
#...#.#...#
#####.#####
...........
#####.#####
#...#.#...#
#...#.#...#
#...#.#...#
#####.#####
""",
    "sparkle": """
.....#.....
.....#.....
....#.#....
....#.#....
..##...##..
##.......##
..##...##..
....#.#....
....#.#....
.....#.....
.....#.....
""",
    "music": """
...########
...#......#
...########
...#......#
...#......#
...#......#
.###...####
#..#..#...#
#..#..#...#
.##....###.
...........
""",
    "notes": """
.#####.....
#.....#....
#.....###..
#.......#..
#.#####.#..
#.......#..
#.#####.#..
#.......#..
#.###...#..
#.......#..
.#######...
""",
}

STRAWBERRY = """
....GG.GG....
.....GGG.....
..RRRGGGRRR..
.RRsRRRRRsRR.
RRRRRRsRRRRRR
RsRRRRRRRRsRR
.RRRRsRRRRRR.
.RRsRRRRRsRR.
..RRRRRsRRR..
...RsRRRRR...
....RRRsR....
.....RRR.....
......R......
"""
SCOL = {"G": GREEN, "R": RED, "s": CREAM}
LINE = YLINE


def blocks(cells, x0, y0, s, fill=None, cls=None, delay=None):
    out = []
    for i, c in enumerate(cells):
        x, y = c[0], c[1]
        col = fill or SCOL.get(c[2], RED)
        style = f' style="animation-delay:{delay(x, y, i):.2f}s"' if delay else ""
        k = f' class="{cls}"' if cls else ""
        out.append(f'<rect x="{x0 + x * s}" y="{y0 + y * s}" width="{s}" height="{s}" fill="{col}"{k}{style}/>')
    return "".join(out)


def text_blocks(text, x0, y0, s, fill, cls=None, delay=None):
    out, x = [], x0
    for ch in text:
        if ch in FONT:
            out.append(blocks(FONT[ch], x, y0, s, fill, cls,
                              (lambda bx, by, i, ox=x: delay(ox + bx * s, by)) if delay else None))
        x += 6 * s
    return "".join(out), x - s


def grid(w, h, step, col=YLINE):
    g = [f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(step, w, step)]
    g += [f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(step, h, step)]
    return f'<g stroke="{col}" stroke-width="1">{"".join(g)}</g>'


ANIM = """<style>
.b{opacity:0;animation:pop .35s steps(2) forwards}
.bob{animation:bob 2.4s steps(2) infinite}
.cur{animation:blink 1s steps(1) infinite}
@keyframes pop{to{opacity:1}}
@keyframes bob{50%{transform:translateY(-8px)}}
@keyframes blink{50%{opacity:0}}
@media (prefers-reduced-motion:reduce){.b{opacity:1;animation:none}.bob,.cur{animation:none}}
</style>"""


def banner():
    W, H = 1200, 380
    moki, end = text_blocks("MOKI", 90, 78, 18, INK, "b", lambda x, y: 0.05 + x / 1400 + y / 900)
    motto, mend = text_blocks("CREATE BEFORE CLAIMING.", 92, 282, 5, DRED)
    jpg = base64.b64encode(open(os.path.join(A, "moki.jpg"), "rb").read()).decode()
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="MOKI - UI/UX, web design and original digital assets">
{ANIM}
<rect width="{W}" height="{H}" fill="{YELLOW}"/>
{grid(W, H, 40)}
<rect x="6" y="6" width="{W - 12}" height="{H - 12}" fill="none" stroke="{INK}" stroke-width="4"/>
{moki}
<text x="92" y="244" fill="{BROWN}" font-family="{MONO}" font-size="22" font-weight="700" letter-spacing="2">UI/UX  ·  WEB DESIGN  ·  ORIGINAL DIGITAL ASSETS</text>
{motto}
<rect x="{mend + 10}" y="282" width="12" height="25" fill="{DRED}" class="cur"/>
<g transform="translate(800 30)"><g class="bob">
<clipPath id="c"><circle cx="160" cy="160" r="152"/></clipPath>
<circle cx="160" cy="160" r="158" fill="{INK}"/>
<image x="6" y="6" width="308" height="308" clip-path="url(#c)" href="data:image/jpeg;base64,{jpg}"/>
</g></g>
</svg>'''
    open(os.path.join(A, "banner.svg"), "w", encoding="utf-8").write(svg)


def card(slug, title, glyph, lines, tags, accent):
    W, H = 480, 150
    g = art(GLYPHS[glyph])
    t, _ = text_blocks(title, 140, 30, 4, INK)
    desc = "".join(f'<text x="140" y="{78 + i * 20}" fill="{MUTED}" font-family="{MONO}" font-size="14">{l}</text>'
                   for i, l in enumerate(lines))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">
<rect width="{W}" height="{H}" fill="{CREAM}"/>
{grid(W, H, 30, CLINE)}
<rect x="2" y="2" width="{W - 4}" height="{H - 4}" fill="none" stroke="{INK}" stroke-width="4"/>
<line x1="112" y1="4" x2="112" y2="{H - 4}" stroke="{INK}" stroke-width="2"/>
{blocks(g, 12, 31, 8, accent)}
{t}
{desc}
<text x="140" y="130" fill="{DRED}" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="1">{tags}</text>
</svg>'''
    open(os.path.join(A, f"card-{slug}.svg"), "w", encoding="utf-8").write(svg)


def footer():
    W, H = 1200, 150
    _, end = text_blocks("THANKS FOR VISITING", 0, 0, 5, INK)
    total = end + 40 + SW * 2
    x0 = (W - total) // 2
    t, end = text_blocks("THANKS FOR VISITING", x0, 63, 5, INK)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Thanks for visiting">
{ANIM}
<rect width="{W}" height="{H}" fill="{YELLOW}"/>
{grid(W, H, 30)}
<rect x="6" y="6" width="{W - 12}" height="{H - 12}" fill="none" stroke="{INK}" stroke-width="4"/>
{t}
<g transform="translate({end + 40} {(H - SH * 2) // 2})"><g class="bob">{svg_rects(0, 0, 2)}</g></g>
</svg>'''
    open(os.path.join(A, "footer.svg"), "w", encoding="utf-8").write(svg)


def button(slug, glyph, label, handle, accent):
    W, H = 360, 76
    t, _ = text_blocks(label, 82, 16, 3, INK)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label} {handle}">
<rect width="{W}" height="{H}" fill="{CREAM}"/>
<rect x="2" y="2" width="{W - 4}" height="{H - 4}" fill="none" stroke="{INK}" stroke-width="4"/>
<rect x="4" y="4" width="62" height="{H - 8}" fill="{YELLOW}"/>
<line x1="66" y1="4" x2="66" y2="{H - 4}" stroke="{INK}" stroke-width="2"/>
{blocks(art(GLYPHS[glyph]), 13, 16, 4, accent)}
{t}
<text x="82" y="58" fill="{MUTED}" font-family="{MONO}" font-size="14">{handle}</text>
</svg>'''
    open(os.path.join(A, f"btn-{slug}.svg"), "w", encoding="utf-8").write(svg)


GLYPHS["linkedin"] = """
..#######..
.#.......#.
#.........#
#..#......#
#.........#
#..#.###..#
#..#.#..#.#
#..#.#..#.#
#..#.#..#.#
.#.......#.
..#######..
"""
GLYPHS["insta"] = """
..#######..
.#.......#.
#.......#.#
#...###...#
#..#...#..#
#..#...#..#
#..#...#..#
#...###...#
#.........#
.#.......#.
..#######..
"""
GLYPHS["threads"] = """
...#####...
.##.....##.
#.........#
#...###.#.#
#..#...##.#
#..#....#.#
#..#...##.#
#...###.##.
#..........
.##.....#..
...#####...
"""


if __name__ == "__main__":
    banner()
    button("linkedin", "linkedin", "LINKEDIN", "moki-officiial", INK)
    button("instagram", "insta", "INSTAGRAM", "@moki._.officials", INK)
    button("threads", "threads", "THREADS", "@moki._.officials", INK)
    card("chess3d", "CHESS 3D", "knight",
         ["3D chess in your browser: 14 bots,", "a capture animation for every piece."],
         "THREE.JS  ·  JAVASCRIPT", RED)
    card("pixel-icons", "PIXEL ICONS", "pack",
         ["Pixel-style icon pack for Android.", "Makes new icons from an app's own icon."],
         "ANDROID  ·  PYTHON", BROWN)
    card("moki-ui", "MOKI UI", "sparkle",
         ["40 animated React components:", "buttons, glass forms, cards, widgets."],
         "REACT  ·  TYPESCRIPT  ·  ANIME.JS", BROWN)
    card("meow-music", "MEOW MUSIC", "music",
         ["Landing page for Meow Music,", "a music app for Android."],
         "HTML  ·  CSS", RED)
    card("student-notes", "STUDENT NOTES", "notes",
         ["Website for Student Notes,", "the Android app for students."],
         "HTML  ·  CSS", RED)
    footer()
    print("assets written:", sorted(os.listdir(A)))
