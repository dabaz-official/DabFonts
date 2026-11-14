#!/usr/bin/env python3
"""Build the demo page assets.

  demo/fonts/*.woff2        subset webfonts the pages reference
  demo/dabfonts-demo.html   self-contained copy with fonts inlined as data URIs
                            (works from file:// with no server and no CORS)

Run scripts/build_dabfonts.py first.
"""
import os, subprocess, sys, base64

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEMO = os.path.join(ROOT, "demo")
FONTS = os.path.join(DEMO, "fonts")
DIST = os.path.join(ROOT, "dist")
HIST = os.path.join(ROOT, "history")
BUILD = os.path.join(ROOT, "build")
os.makedirs(FONTS, exist_ok=True)

PAGES = ("index.html", "punct.html", "scale.html", "align.html")
html = open(os.path.join(DEMO, "index.html"), encoding="utf-8").read()
extra = ""
for page in PAGES[1:]:
    p = os.path.join(DEMO, page)
    if os.path.exists(p):
        extra += open(p, encoding="utf-8").read()

chars = sorted({c for c in (html + extra) if ord(c) > 0x7F})
text_file = os.path.join(BUILD, "demo-chars.txt")
open(text_file, "w", encoding="utf-8").write("".join(chars))
print(f"demo charset: {len(chars)} non-ASCII chars")

RANGES = ("U+0020-024F,U+0370-04FF,U+1E00-1EFF,U+2000-206F,"
          "U+20A0-20CF,U+2100-214F,U+3000-303F,U+FF00-FFEF")

jobs = [
    (os.path.join(BUILD, "inter-400.ttf"), os.path.join(FONTS, "inter-400.woff2")),
    (os.path.join(BUILD, "inter-600.ttf"), os.path.join(FONTS, "inter-600.woff2")),
    (os.path.join(BUILD, "noto-400.ttf"),  os.path.join(FONTS, "noto-400.woff2")),
    (os.path.join(BUILD, "noto-600.ttf"),  os.path.join(FONTS, "noto-600.woff2")),
    (os.path.join(DIST, "DabSans-Regular.ttf"), os.path.join(FONTS, "sans-400.woff2")),
    (os.path.join(DIST, "DabSans-SemiBold.ttf"), os.path.join(FONTS, "sans-600.woff2")),
    # history/v1: full-width punctuation, full Han set
    (os.path.join(HIST, "v1-fullwidth/DabFonts-Regular.ttf"),
     os.path.join(FONTS, "before-400.woff2")),
    (os.path.join(HIST, "v1-fullwidth/DabFonts-Bold.ttf"),
     os.path.join(FONTS, "before-700.woff2")),
    # history/v2: half-width punctuation, before the CJK scale
    (os.path.join(HIST, "v2-halfwidth-unscaled/DabFonts-Regular.ttf"),
     os.path.join(FONTS, "unscaled-400.woff2")),
    (os.path.join(HIST, "v2-halfwidth-unscaled/DabFonts-Bold.ttf"),
     os.path.join(FONTS, "unscaled-700.woff2")),
]

for src, out in jobs:
    if not os.path.exists(src):
        raise SystemExit(f"missing input: {src} (run build_dabfonts.py first)")
    subprocess.run([
        sys.executable, "-m", "fontTools.subset", src,
        f"--output-file={out}",
        "--flavor=woff2",
        f"--unicodes={RANGES}",
        f"--text-file={text_file}",
        "--layout-features=*",
        "--name-IDs=*",
        "--notdef-outline",
        "--recommended-glyphs",
    ], check=True)
    print(f"  {os.path.basename(out):22s} {os.path.getsize(out)/1024:8.1f} KB")

# ---- mono family: shipped whole, no subsetting needed (~35 KB) ----
import shutil
for style, name in (("Regular", "mono-400"), ("SemiBold", "mono-600")):
    src = os.path.join(DIST, f"DabMono-{style}.woff2")
    dst = os.path.join(FONTS, f"{name}.woff2")
    shutil.copyfile(src, dst)
    print(f"  {name + '.woff2':22s} {os.path.getsize(dst)/1024:8.1f} KB (copied)")

# ---- self-contained build (index.html only) ----
page = html
for name in ("inter-400", "inter-600", "noto-400", "noto-600",
             "sans-400", "sans-600", "before-400", "before-700",
             "unscaled-400", "unscaled-700", "mono-400", "mono-600"):
    path = os.path.join(FONTS, f"{name}.woff2")
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    page = page.replace(f"fonts/{name}.woff2", f"data:font/woff2;base64,{b64}")

out_html = os.path.join(DEMO, "dabfonts-demo.html")
open(out_html, "w", encoding="utf-8").write(page)
print(f"\nwrote {out_html} ({os.path.getsize(out_html)/1e6:.2f} MB)")
