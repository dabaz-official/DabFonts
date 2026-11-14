#!/usr/bin/env python3
"""Dab Sans + Dab Mono build.

  Latin / Greek / Cyrillic / digits / Latin punctuation -> Inter 4.001
  Han (GB2312 level-1, 3,755 characters)                -> Noto Sans SC 2.004
  CJK punctuation                                       -> Noto, baked to its own
                                                           half-width metrics (hwid + halt)
  Anything else                                         -> Inter if it has the codepoint,
                                                           otherwise absent (system fallback)

Outputs dist/DabSans-{Regular,SemiBold}.{ttf,woff2} and
  dist/DabMono-{Regular,SemiBold}.{ttf,woff2}.
Intermediates land in build/ and are inputs for scripts/build_web_assets.py.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.ttLib.scaleUpem import scale_upem
from fontTools.merge import Merger

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "dist")
BUILD = os.path.join(ROOT, "build")
for d in (OUT, BUILD):
    os.makedirs(d, exist_ok=True)

OFL_NOTICE = (
    "Copyright (c) 2016 The Inter Project Authors (https://github.com/rsms/inter). "
    "Copyright 2014-2021 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'. "
    "Copyright 2022 The Noto Project Authors. "
    "Dab Sans is a merge of Inter and Noto Sans SC. "
    "Licensed under the SIL Open Font License, Version 1.1: "
    "https://openfontlicense.org"
)

# --------------------------------------------------------------------------
# Optical geometry
#   LATIN_DY     em, positive = move Latin UP. Inter cap centre 0.3640 vs
#                Noto Han centre 0.3755 -> +0.0115 lands them together.
#   LATIN_SCALE  optical size multiplier for the Latin side.
#   CJK_SCALE    uniform scale for the whole CJK side (advances included).
#                Apple ships PingFang x 0.886 + 44/1000 em on apple.com.cn;
#                we copy the resulting ratio (Han ink / cap height = 1.167),
#                which for Noto's smaller Han ink works out to 0.94.
LATIN_DY = 0.0115
LATIN_SCALE = 1.0
CJK_SCALE = 0.94

# Punctuation that should sit on a half-width advance. Quotes are absent on
# purpose: Inter supplies “ ” ‘ ’ … — · in the merge. 〖〗 stays full-width.
HALFWIDTH_PUNCT = [
    0x3001, 0x3002,                                      # 、 。
    0x3008, 0x3009, 0x300A, 0x300B,                      # 〈 〉 《 》
    0x300C, 0x300D, 0x300E, 0x300F,                      # 「 」 『 』
    0x3010, 0x3011, 0x3014, 0x3015,                      # 【 】 〔 〕
    0xFF01, 0xFF08, 0xFF09, 0xFF0C, 0xFF0E, 0xFF0F,      # ！ （ ） ， ． ／
    0xFF1A, 0xFF1B, 0xFF1F,                              # ： ； ？
    0xFF3B, 0xFF3D, 0xFF5B, 0xFF5D, 0xFF5E,              # ［ ］ ｛ ｝ ～
]

MONO_SRC = "GeistMono-VF.ttf"
MONO_NOTICE = (
    "Copyright 2024 The Geist Project Authors (https://github.com/vercel/geist-font). "
    "Dab Mono is a renamed, statically-instanced build of Geist Mono. "
    "Licensed under the SIL Open Font License, Version 1.1: "
    "https://openfontlicense.org"
)

# Han blocks removed from the build; GB2312 level-1 is re-added afterwards.
HAN_RANGES = [(0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF), (0x20000, 0x3FFFF)]


def set_name(font, family, style, full, ps, copyright_, license_desc):
    name = font["name"]
    for rec in list(name.names):
        if rec.nameID in (0, 1, 2, 3, 4, 6, 13, 14, 16, 17):
            name.removeNames(nameID=rec.nameID)
    vals = {
        0: copyright_,
        1: family,
        2: style,
        3: f"{family} {style} 1.0",
        4: full,
        6: ps,
        13: license_desc,
        14: "https://openfontlicense.org",
        16: family,
        17: style,
    }
    for nid, val in vals.items():
        name.setName(val, nid, 3, 1, 0x409)
        name.setName(val, nid, 1, 0, 0)


def _transform(font, scale, dy):
    """Scale every glyph about the baseline, then shift it by dy units."""
    if scale == 1.0 and dy == 0:
        return
    glyf = font["glyf"]
    for name in font.getGlyphOrder():
        g = glyf[name]
        if g.numberOfContours == 0:
            continue
        if g.isComposite():
            for comp in g.components:
                comp.x = round(comp.x * scale)
                comp.y = round(comp.y * scale + dy)
            g.recalcBounds(glyf)
        else:
            g.coordinates.scale((scale, scale))
            g.coordinates.translate((0, dy))
            g.coordinates.toInt()
            g.recalcBounds(glyf)
    if scale != 1.0:
        for name, (adv, lsb) in list(font["hmtx"].metrics.items()):
            font["hmtx"].metrics[name] = (round(adv * scale), round(lsb * scale))


def transform_latin(font, dy_em, scale):
    if dy_em == 0 and scale == 1.0:
        return
    upm = font["head"].unitsPerEm
    _transform(font, scale, round(dy_em * upm))
    print(f"    latin transform: dy={round(dy_em * upm)} units, scale={scale}", flush=True)


def cjk_optical_center(font, sample="中字国永大天"):
    """Average ink centre of a few Han glyphs, in em above the baseline."""
    cm = font.getBestCmap()
    vals = []
    for ch in sample:
        gn = cm.get(ord(ch))
        if gn and font["glyf"][gn].numberOfContours:
            g = font["glyf"][gn]
            vals.append((g.yMin + g.yMax) / 2)
    return (sum(vals) / len(vals)) / font["head"].unitsPerEm if vals else 0.375


def transform_cjk(font, scale):
    """Scale the CJK side and lift it so the optical centre stays put."""
    if scale == 1.0:
        return
    upm = font["head"].unitsPerEm
    center = cjk_optical_center(font)
    dy = round(center * (1 - scale) * upm)
    _transform(font, scale, dy)
    print(f"    cjk transform: scale={scale}, optical centre {center:.4f} kept, dy={dy}", flush=True)


def _gsub_single(font, tag):
    if "GSUB" not in font:
        return {}
    tbl = font["GSUB"].table
    idx = set()
    for fr in tbl.FeatureList.FeatureRecord:
        if fr.FeatureTag == tag:
            idx.update(fr.Feature.LookupListIndex)
    out = {}
    for i in idx:
        for st in tbl.LookupList.Lookup[i].SubTable:
            if hasattr(st, "ExtSubTable"):
                st = st.ExtSubTable
            out.update(getattr(st, "mapping", None) or {})
    return out


def _gpos_single_adj(font, tag):
    if "GPOS" not in font:
        return {}
    tbl = font["GPOS"].table
    idx = set()
    for fr in tbl.FeatureList.FeatureRecord:
        if fr.FeatureTag == tag:
            idx.update(fr.Feature.LookupListIndex)
    out = {}
    for i in idx:
        for st in tbl.LookupList.Lookup[i].SubTable:
            if hasattr(st, "ExtSubTable"):
                st = st.ExtSubTable
            cov = st.Coverage.glyphs if getattr(st, "Coverage", None) else []
            vals = st.Value
            vals = [vals] * len(cov) if not isinstance(vals, list) else vals
            for gn, v in zip(cov, vals):
                out[gn] = (getattr(v, "XAdvance", 0) or 0, getattr(v, "XPlacement", 0) or 0)
    return out


def _translate_x(font, name, dx):
    if not dx:
        return
    glyf = font["glyf"]
    g = glyf[name]
    if g.numberOfContours == 0:
        return
    if g.isComposite():
        for comp in g.components:
            comp.x = round(comp.x + dx)
    else:
        g.coordinates.translate((dx, 0))
        g.coordinates.toInt()
    g.recalcBounds(glyf)


def apply_halfwidth(font, cps):
    """Bake Noto's own half-width punctuation metrics into the outlines.

    Noto expresses half-width forms two ways:
      * `hwid` (GSUB) — dedicated alternate glyphs at 500/1000, e.g. （ ） ，
      * `halt` (GPOS) — advance/placement deltas on the normal glyph,
                        e.g. 。 、 《 【 ！ ： ； ？
    Both are applied here; finalize() then drops the features so a browser
    cannot apply them a second time.
    """
    hwid = _gsub_single(font, "hwid")
    halt = _gpos_single_adj(font, "halt")
    best = font.getBestCmap()
    stats = {"hwid": 0, "halt": 0, "none": 0}
    for cp in cps:
        gn = best.get(cp)
        if gn is None:
            stats["none"] += 1
            continue
        alt = hwid.get(gn)
        if alt:
            for table in font["cmap"].tables:
                if cp in table.cmap:
                    table.cmap[cp] = alt
            stats["hwid"] += 1
            continue
        adj = halt.get(gn)
        if adj:
            xadv, xpl = adj
            _translate_x(font, gn, xpl)
            adv, lsb = font["hmtx"][gn]
            font["hmtx"][gn] = (adv + xadv, lsb + xpl)
            stats["halt"] += 1
            continue
        stats["none"] += 1
    print(f"    halfwidth punctuation: {stats['hwid']} via hwid, "
          f"{stats['halt']} via halt, {stats['none']} untouched", flush=True)


def gb2312_level1():
    """3,755 characters of GB2312 level 1 — the usual 'common characters' set."""
    chars = set()
    for hi in range(0xB0, 0xD8):
        for lo in range(0xA1, 0xFF):
            try:
                chars.add(bytes([hi, lo]).decode("gb2312"))
            except UnicodeDecodeError:
                pass
    return chars


def build_charset(font):
    cmap = font.getBestCmap()
    keep = {cp for cp in cmap if not any(a <= cp <= b for a, b in HAN_RANGES)}
    common = {ord(ch) for ch in gb2312_level1() if ord(ch) in cmap}
    keep |= common
    return keep, len(common)


def finalize(font, unicodes):
    """One subsetter pass: restrict the charset and drop baked-out features.

    `locl` is removed because browsers apply it under lang=zh-CN and it would
    replace every Inter letter with Noto's Latin glyphs (A: 686 -> 608 units).
    `halt` / `palt` / `hwid` are removed because their effect is now baked.
    """
    from fontTools import subset as ftsubset

    tags = set()
    for tag in ("GSUB", "GPOS"):
        if tag in font:
            tags.update(fr.FeatureTag for fr in font[tag].table.FeatureList.FeatureRecord)
    keep_features = sorted(tags - {"locl", "halt", "palt", "hwid", "vhal", "vpal"})

    opts = ftsubset.Options()
    opts.layout_features = keep_features
    opts.name_IDs = ["*"]
    opts.name_legacy = True
    opts.name_languages = ["*"]
    opts.notdef_outline = True
    opts.glyph_names = False
    opts.drop_tables = []
    opts.passthrough_tables = False

    before = len(font.getGlyphOrder())
    ss = ftsubset.Subsetter(options=opts)
    ss.populate(unicodes=unicodes)
    ss.subset(font)
    print(f"    subset: {before} -> {len(font.getGlyphOrder())} glyphs, "
          f"features kept: {len(keep_features)}", flush=True)


def build(weight, style):
    print(f"[{style}] instancing Inter wght={weight} opsz=16 ...", flush=True)
    inter = TTFont(os.path.join(SRC, "Inter-VF.ttf"))
    inter = instantiateVariableFont(inter, {"wght": weight, "opsz": 16}, inplace=False)
    scale_upem(inter, 1000)
    transform_latin(inter, LATIN_DY, LATIN_SCALE)

    print(f"[{style}] instancing Noto Sans SC wght={weight} ...", flush=True)
    noto = TTFont(os.path.join(SRC, "NotoSansSC-VF.ttf"))
    noto = instantiateVariableFont(noto, {"wght": weight}, inplace=False)
    apply_halfwidth(noto, HALFWIDTH_PUNCT)
    transform_cjk(noto, CJK_SCALE)

    tmp_i = os.path.join(BUILD, f"inter-{weight}.ttf")
    tmp_n = os.path.join(BUILD, f"noto-{weight}.ttf")

    # Normalise the `post` table: Inter ships format 2, Noto format 3.
    for f in (inter, noto):
        p = f["post"]
        p.formatType = 3.0
        p.__dict__.pop("mapping", None)
        p.__dict__.pop("extraNames", None)

    # vhea/vmtx/BASE exist only in Noto; the merger cannot reconcile a table
    # that is missing on one side.
    for tag in ("vhea", "vmtx", "BASE"):
        if tag in noto:
            del noto[tag]

    inter.save(tmp_i)
    noto.save(tmp_n)

    print(f"[{style}] merging (Inter has priority) ...", flush=True)
    merged = Merger().merge([tmp_i, tmp_n])

    charset, n_common = build_charset(merged)
    print(f"[{style}] charset: {len(charset)} codepoints, {n_common} common Han", flush=True)
    finalize(merged, charset)

    set_name(
        merged,
        family="Dab Sans",
        style=style,
        full=f"Dab Sans {style}",
        ps=f"DabSans-{style}",
        copyright_=OFL_NOTICE,
        license_desc=OFL_NOTICE,
    )

    # OS/2 / hhea: keep Noto's vertical metrics so CJK line-height stays sane
    merged["OS/2"].sTypoAscender = noto["OS/2"].sTypoAscender
    merged["OS/2"].sTypoDescender = noto["OS/2"].sTypoDescender
    merged["OS/2"].sTypoLineGap = noto["OS/2"].sTypoLineGap
    merged["OS/2"].usWinAscent = noto["OS/2"].usWinAscent
    merged["OS/2"].usWinDescent = noto["OS/2"].usWinDescent
    merged["hhea"].ascent = noto["hhea"].ascent
    merged["hhea"].descent = noto["hhea"].descent

    out = os.path.join(OUT, f"DabSans-{style}.ttf")
    merged.save(out)
    print(f"[{style}] wrote {out} ({os.path.getsize(out)/1e6:.1f} MB)", flush=True)

    merged.flavor = "woff2"
    out_w2 = out.replace(".ttf", ".woff2")
    merged.save(out_w2)
    print(f"[{style}] wrote {out_w2} ({os.path.getsize(out_w2)/1e6:.2f} MB)", flush=True)


def build_mono(weight, style):
    """Geist Mono stays a separate family — it is only used for monospace runs."""
    print(f"[Mono {style}] instancing Geist Mono wght={weight} ...", flush=True)
    font = TTFont(os.path.join(SRC, MONO_SRC))
    font = instantiateVariableFont(font, {"wght": weight}, inplace=False)
    # Same optical lift as the Latin side so inline <code> sits level with the body.
    transform_latin(font, LATIN_DY, 1.0)

    set_name(
        font,
        family="Dab Mono",
        style=style,
        full=f"Dab Mono {style}",
        ps=f"DabMono-{style}",
        copyright_=MONO_NOTICE,
        license_desc=MONO_NOTICE,
    )

    out = os.path.join(OUT, f"DabMono-{style}.ttf")
    font.save(out)
    print(f"[Mono {style}] wrote {out} ({os.path.getsize(out)/1e6:.2f} MB)", flush=True)

    font.flavor = "woff2"
    out_w2 = out.replace(".ttf", ".woff2")
    font.save(out_w2)
    print(f"[Mono {style}] wrote {out_w2} ({os.path.getsize(out_w2)/1e6:.2f} MB)", flush=True)


if __name__ == "__main__":
    for w, s in ((400, "Regular"), (600, "SemiBold")):
        build(w, s)
    for w, s in ((400, "Regular"), (600, "SemiBold")):
        build_mono(w, s)
