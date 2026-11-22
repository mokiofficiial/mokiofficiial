"""Pixel-art Moki sprite (hand-placed, mascot colours)."""
PAL = {"k": "#141414", "c": "#fdf6e8", "r": "#ee5a44", "d": "#d9443a", "p": "#f4a08c",
       "b": "#5e3a1e", "g": "#7a8b3e", "w": "#ffffff", "y": "#ecb61e", "s": "#f7c6b6"}
SPRITE = """
........gg...gg.........
.......gggg.gggg........
.........ggggg..........
.......kkkkkwkkkkk......
.....kkrrrrwywrrrrkk....
....krrsrrrrwrrrrrrrkk..
...krrrrrrrrrrrrrrrrrrk.
...krrrrrrrrrrrrrrrrrrk.
....kkkkkkkkkkkkkkkkkk..
...kcccccccccccccccccck.
..kcccccccccccccccccccck
..kcccccckcccccckcccccck
..kcccccckcccccckcccccck
..kcppcccccccccccccppcck
..kccccccccccccccccccck.
..kcrrccrrccrrccrrccrrk.
..krrrrrrrrrrrrrrrrrrrk.
..krrccrrccrrccrrccrrck.
..kccccccccccccccccccck.
...kkbbbbkkkkkkkbbbbkk..
....kbbbbbk...kbbbbbk...
.....kkkkk.....kkkkk....
"""
CELLS = [(x, y, ch) for y, row in enumerate(SPRITE.strip("\n").split("\n"))
         for x, ch in enumerate(row) if ch != "."]


def svg_rects(x0, y0, s, cls=None):
    k = f' class="{cls}"' if cls else ""
    return "".join(f'<rect x="{x0 + x * s}" y="{y0 + y * s}" width="{s}" height="{s}" fill="{PAL[c]}"{k}/>'
                   for x, y, c in CELLS)


if __name__ == "__main__":
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (26 * 14, 24 * 14), "#ecb61e")
    d = ImageDraw.Draw(im)
    for x, y, c in CELLS:
        d.rectangle([14 + x * 14, 14 + y * 14, 27 + x * 14, 27 + y * 14], fill=PAL[c])
    im.save(r"C:/Users/risha/AppData/Local/Temp/claude/b1566b25184d20ac/86d67d40-b9d2-4c67-8e30-aecfda8ea286/scratchpad/moki_sprite.png")
