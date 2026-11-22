"""Live parts of the profile, refreshed every day by .github/workflows/update.yml:

  assets/stats.svg      public repos, stars, followers, days on GitHub, top languages
  assets/moki-says.svg  pixel Moki with a line that changes every day

Run:  python stats.py      (uses GITHUB_TOKEN if set, works without it too)
"""
import datetime as dt
import json
import os
import urllib.request

from gen import A, CREAM, CLINE, INK, MUTED, MONO, RED, BROWN, YELLOW, DRED, grid, text_blocks, ANIM
from sprite import svg_rects

USER = "mokiofficiial"
SKIP = {USER}                      # the profile repo itself is not a project

LINES = [
    "Create before claiming.",
    "Small steps, every day.",
    "Every pixel counts.",
    "Ship it, then make it pretty.",
    "Stay curious, stay kind.",
    "Drink water. Push code.",
    "Make something you would use yourself.",
    "Good design is quiet.",
    "Done is better than perfect.",
    "Sketch first, code later.",
    "Strawberries make everything better.",
    "Bugs are just features in disguise.",
    "Rest is part of the work.",
    "One more commit, then snacks.",
]


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}",
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-stats"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect():
    user = api(f"/users/{USER}")
    repos = [r for r in api(f"/users/{USER}/repos?per_page=100&type=owner")
             if not r["fork"] and not r["private"] and r["name"] not in SKIP]
    langs = {}
    for r in repos:
        for k, v in api(f"/repos/{USER}/{r['name']}/languages").items():
            langs[k] = langs.get(k, 0) + v
    since = dt.datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
    return {
        "repos": len(repos),
        "stars": sum(r["stargazers_count"] for r in repos),
        "followers": user["followers"],
        "days": (dt.datetime.now(dt.timezone.utc) - since).days,
        "langs": sorted(langs.items(), key=lambda kv: -kv[1])[:5],
    }


def stats_svg(d):
    W, H = 1200, 300
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="{d["repos"]} public repos, {d["stars"]} stars, {d["followers"]} followers">',
           f'<rect width="{W}" height="{H}" fill="{CREAM}"/>', grid(W, H, 30, CLINE),
           f'<rect x="4" y="4" width="{W - 8}" height="56" fill="{YELLOW}"/>',
           f'<line x1="4" y1="60" x2="{W - 4}" y2="60" stroke="{INK}" stroke-width="3"/>',
           f'<rect x="2" y="2" width="{W - 4}" height="{H - 4}" fill="none" stroke="{INK}" stroke-width="4"/>']
    t, _ = text_blocks("MOKI STATS", 30, 20, 4, INK)
    out.append(t)
    out.append(f'<text x="{W - 30}" y="40" text-anchor="end" fill="{BROWN}" font-family="{MONO}" font-size="13">'
               f'updated {dt.date.today().isoformat()}</text>')

    # left: four numbers in pixel digits
    items = [(d["repos"], "PUBLIC REPOS"), (d["stars"], "STARS"), (d["followers"], "FOLLOWERS"), (d["days"], "DAYS HERE")]
    for i, (num, label) in enumerate(items):
        x, y = 30 + (i % 2) * 260, 90 + (i // 2) * 100
        t, _ = text_blocks(str(num), x, y, 8, RED if i % 3 == 0 else BROWN)
        out.append(t)
        out.append(f'<text x="{x}" y="{y + 64}" fill="{MUTED}" font-family="{MONO}" font-size="13" '
                   f'letter-spacing="2">{label}</text>')
    out.append(f'<line x1="560" y1="80" x2="560" y2="{H - 24}" stroke="{INK}" stroke-width="2"/>')

    # right: top languages as pixel bars (20 blocks = 100 %)
    total = sum(v for _, v in d["langs"]) or 1
    out.append(f'<text x="600" y="98" fill="{INK}" font-family="{MONO}" font-size="14" font-weight="700" '
               f'letter-spacing="2">TOP LANGUAGES</text>')
    for i, (name, v) in enumerate(d["langs"]):
        y = 124 + i * 32
        pct = v / total
        n = max(1, round(pct * 20))
        out.append(f'<text x="600" y="{y + 13}" fill="{BROWN}" font-family="{MONO}" font-size="14">{name}</text>')
        for k in range(20):
            col = (RED if i % 2 == 0 else BROWN) if k < n else CLINE
            out.append(f'<rect x="{760 + k * 18}" y="{y}" width="14" height="14" fill="{col}"/>')
        out.append(f'<text x="{1130}" y="{y + 13}" fill="{MUTED}" font-family="{MONO}" font-size="13">'
                   f'{pct * 100:.0f}%</text>')
    out.append("</svg>")
    open(os.path.join(A, "stats.svg"), "w", encoding="utf-8").write("".join(out))


def says_svg():
    W, H = 1200, 170
    line = LINES[dt.date.today().toordinal() % len(LINES)]
    bw = 70 + len(line) * 13
    bx = 210
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Moki says: {line}">
{ANIM}
<rect width="{W}" height="{H}" fill="{YELLOW}"/>
{grid(W, H, 30)}
<rect x="6" y="6" width="{W - 12}" height="{H - 12}" fill="none" stroke="{INK}" stroke-width="4"/>
<g transform="translate(50 25)"><g class="bob">{svg_rects(0, 0, 5)}</g></g>
<rect x="{bx}" y="40" width="{bw}" height="74" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>
<rect x="{bx - 12}" y="74" width="12" height="8" fill="{INK}"/>
<rect x="{bx - 22}" y="82" width="10" height="8" fill="{INK}"/>
<text x="{bx + 28}" y="70" fill="{DRED}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="2">MOKI SAYS</text>
<text x="{bx + 28}" y="96" fill="{INK}" font-family="{MONO}" font-size="21">{line}</text>
<rect x="{bx + 32 + len(line) * 12.6:.0f}" y="80" width="10" height="20" fill="{DRED}" class="cur"/>
</svg>'''
    open(os.path.join(A, "moki-says.svg"), "w", encoding="utf-8").write(svg)


if __name__ == "__main__":
    d = collect()
    stats_svg(d)
    says_svg()
    print(d)
