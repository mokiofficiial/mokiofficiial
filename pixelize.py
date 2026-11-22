"""Original Moki mascot -> pixel sprite, keeping its exact structure.

1. every pixel of the original is snapped to the mascot palette (nearest colour);
   the yellow circle background becomes transparent
2. the character's bounding box is cut into an N-wide grid
3. each cell takes the MOST COMMON palette colour inside it (no blending, so no
   muddy in-between colours) - except black: if >= 20 % of a cell is outline,
   the cell is outline, so the shapes keep their ink lines
Writes sprite_art.txt (one char per cell) that sprite.py reads.
"""
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "moki.jpg")

# char: (reference colours from the mascot, output colour)
PALETTE = {
    "k": ([(20, 16, 14), (45, 30, 25)], "#141414"),            # ink outline, eyes
    "c": ([(253, 244, 228), (246, 236, 214)], "#fdf4e4"),      # cream body / hand / palette
    "w": ([(255, 255, 255)], "#ffffff"),                       # flower petals
    "r": ([(232, 84, 66), (222, 70, 58)], "#e65442"),          # strawberry red
    "s": ([(240, 128, 108), (244, 150, 128)], "#f0806c"),      # salmon (light red, halftone)
    "p": ([(246, 178, 160), (250, 196, 180)], "#f6b2a0"),      # blush pink
    "b": ([(92, 52, 30), (110, 64, 38)], "#5c341e"),           # dark brown feet
    "m": ([(150, 90, 55), (170, 105, 65)], "#96593a"),         # brush stick brown
    "g": ([(112, 120, 58), (132, 140, 70)], "#707a3a"),        # leaves
    "y": ([(240, 190, 40), (232, 182, 30)], "#f0be28"),        # yellow dots / flower centre
    "u": ([(50, 120, 190), (60, 135, 200)], "#3278be"),        # blue paint
    ".": ([(236, 182, 30), (226, 172, 24), (240, 196, 60)], None),   # background
}
REF = [(k, c) for k, (cols, _) in PALETTE.items() for c in cols]


def nearest(px):
    r, g, b = px
    best, bk = 1e9, "."
    for k, (cr, cg, cb) in REF:
        dd = (r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2
        if dd < best:
            best, bk = dd, k
    return bk


def run(n):
    im = Image.open(SRC).convert("RGB")
    W = im.width
    # quantise at a working size (fast, still far finer than the target grid)
    work = 360
    im = im.resize((work, work), Image.LANCZOS)
    cx = cy = work / 2
    rad = work / 2 * 0.95
    lab = {}
    for y in range(work):
        for x in range(work):
            if (x - cx) ** 2 + (y - cy) ** 2 > rad * rad:
                continue
            k = nearest(im.getpixel((x, y)))
            if k != ".":
                lab[(x, y)] = k
    xs = [p[0] for p in lab]
    ys = [p[1] for p in lab]
    x0, x1, y0, y1 = min(xs), max(xs) + 1, min(ys), max(ys) + 1
    cell = (x1 - x0) / n
    rows = round((y1 - y0) / cell)
    out = []
    for gy in range(rows):
        row = ""
        for gx in range(n):
            votes, tot = {}, 0
            for y in range(int(y0 + gy * cell), int(y0 + (gy + 1) * cell)):
                for x in range(int(x0 + gx * cell), int(x0 + (gx + 1) * cell)):
                    tot += 1
                    k = lab.get((x, y), ".")
                    votes[k] = votes.get(k, 0) + 1
            if votes.get("k", 0) >= KTH * tot:
                row += "k"
            else:
                row += max(votes, key=lambda q: (votes[q], q != "."))
        out.append(row)
    return smooth(out)


KTH = 0.14          # outline wins a cell at 14 % ink


def smooth(rows):
    """3x3 majority filter on colour cells (outline and background untouched):
    removes halftone speckles, keeps every shape."""
    g = [list(r) for r in rows]
    H, W = len(g), len(g[0])
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            c = g[y][x]
            if c in "k.":
                continue
            votes = {}
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if 0 <= y + dy < H and 0 <= x + dx < W:
                        q = g[y + dy][x + dx]
                        if q not in "k.":
                            votes[q] = votes.get(q, 0) + 1
            best = max(votes, key=votes.get)
            if votes[best] >= 5 and votes.get(c, 0) <= 2:
                out[y][x] = best
    # lonely outline pixels inside a colour field are halftone noise
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if out[y][x] == "k":
                n = sum(out[y + dy][x + dx] == "k" for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - 1
                if n == 0:
                    out[y][x] = max(("c", "r", "s"), key=lambda q: sum(
                        out[y + dy][x + dx] == q for dy in (-1, 0, 1) for dx in (-1, 0, 1)))
    return ["".join(r) for r in out]


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 48
    rows = run(n)
    open(os.path.join(HERE, "sprite_art.txt"), "w").write("\n".join(rows) + "\n")
    print(n, "x", len(rows))
    print("\n".join(rows))
