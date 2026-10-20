#!/usr/bin/env python3
"""Scan games/<name>/ folders (an .html file + logo.png). For each game, write games/<name>/play.svg
(the HTML wrapped so jsDelivr can run it) and list everything in games/games.json."""
import json, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgwrap import wrap

root = pathlib.Path(__file__).resolve().parent.parent
gdir = root / "games"
gdir.mkdir(exist_ok=True)
# Same-origin lets games save progress; it is isolated from DSMHub because the origins differ.
SANDBOX = "allow-scripts allow-same-origin allow-popups allow-forms allow-pointer-lock allow-modals"

games = []
for d in sorted(p for p in gdir.iterdir() if p.is_dir() and not p.name.startswith(".")):
    htmls = sorted(f for f in d.iterdir() if f.is_file() and f.suffix.lower() in (".html", ".htm"))
    main = next((h for h in htmls if h.name.lower() == "index.html"), htmls[0] if htmls else None)
    if not main:
        print(f"skip {d.name}: no .html file"); continue
    html = main.read_text(encoding="utf-8", errors="replace")
    title = re.sub(r"[-_]+", " ", d.name).strip().title()
    (d / "play.svg").write_text(wrap(html, SANDBOX, title), encoding="utf-8")
    icon = next((f.name for f in d.iterdir() if f.name.lower() == "logo.png"), None)
    games.append({"id": d.name, "title": title, "icon": icon, "play": "play.svg"})
    print(f"ok   {d.name} ({main.name}{'' if icon else ', no logo.png'})")

(gdir / "games.json").write_text(json.dumps(games, indent=1), encoding="utf-8")
print(f"games.json: {len(games)} game(s)")
