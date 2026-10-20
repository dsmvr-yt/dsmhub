#!/usr/bin/env python3
"""Wrap the whole site (index.html + config.js) into index.svg for jsDelivr.
Usage: python3 tools/build_svg.py [--same-origin]   (see README for the trade-off)"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgwrap import wrap

root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "index.html").read_text(encoding="utf-8")
cfg = (root / "config.js").read_text(encoding="utf-8")
html = html.replace('<script src="config.js"></script>', "<script>" + cfg.replace("</script", "<\\/script") + "</script>")
sandbox = "allow-scripts allow-popups allow-popups-to-escape-sandbox allow-forms allow-pointer-lock allow-modals"
if "--same-origin" in sys.argv:
    sandbox += " allow-same-origin"
out = wrap(html, sandbox, "DSMHub")
(root / "index.svg").write_text(out, encoding="utf-8")
print(f"index.svg written ({len(out)//1024} KB)")
