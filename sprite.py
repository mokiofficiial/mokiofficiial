"""Pixel Moki, made from the original mascot by pixelize.py (same structure)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# colours of pixelize.PALETTE (kept here so the daily Action needs no Pillow)
PAL = {'k': '#141414', 'c': '#fdf4e4', 'w': '#ffffff', 'r': '#e65442', 's': '#f0806c', 'p': '#f6b2a0', 'b': '#5c341e', 'm': '#96593a', 'g': '#707a3a', 'y': '#f0be28', 'u': '#3278be'}


def load(name="sprite_art.txt"):
    rows = open(os.path.join(HERE, name)).read().split()
    return [(x, y, c) for y, r in enumerate(rows) for x, c in enumerate(r) if c != "."]


CELLS = load()                       # 56 wide
SMALL = load("sprite_art_44.txt")    # 44 wide (passport avatar)
SW = 1 + max(x for x, _, _ in CELLS)
SH = 1 + max(y for _, y, _ in CELLS)


def svg_rects(x0, y0, s, cls=None):
    k = f' class="{cls}"' if cls else ""
    return "".join(f'<rect x="{x0 + x * s}" y="{y0 + y * s}" width="{s}" height="{s}" fill="{PAL[c]}"{k}/>'
                   for x, y, c in CELLS)
