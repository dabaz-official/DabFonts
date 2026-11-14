# DabFonts

**Families:** `Dab Sans` (text) / `Dab Mono` (monospace). **Version:** 1.0.0. The repository keeps the project name DabFonts.

A mixed Chinese–English typeface for personal projects: the Latin side of **Inter 4.001** plus the Han side of **Noto Sans SC 2.004**, merged into one family.

- Han is limited to the **3,755 GB2312 level-1 characters**
- 28 Chinese punctuation marks are baked to Noto's **half-width** metrics (500 at bake time, advance 470 after the 0.94 scale)
- The CJK side is scaled to **0.94** to match the Latin/CJK proportion used on Apple's site
- Latin is raised **0.0115 em** to share the optical centre with Han

Result: 9,312 glyphs / 8,915 codepoints; TTF 1,947,056 B; woff2 820,348 B (801.1 KiB), Regular.

## Usage

Typography and loading rules live in [GUIDELINE.md](GUIDELINE.md); the normative reference is [TYPESETTING.md](TYPESETTING.md). TYPESETTING §2.1 is the canonical `@font-face` block; `GUIDELINE.md` carries a verbatim copy, and this README does not repeat it. The repository contract (pinned DabAgents commit, commands, Definition of Done, exceptions) is in [AGENTS.md](AGENTS.md). The one stack to use:

```css
body {
  font-family: "Dab Sans", -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  font-synthesis: none;
}

code, pre, kbd, samp {
  font-family: "Dab Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
}
```

- Only 400 / 600; 500 resolves to 400 and 700 to 600. Do not rely on synthesis.
- Do **not** enable `font-feature-settings: "palt"`; the punctuation is already half-width.
- Han outside the 3,755 falls back to the system stack; that is designed behavior.
- Monospace is the separate `Dab Mono` family (Geist Mono) and does not participate in the merge.

Desktop: install `dist/DabSans-Regular.ttf` and `dist/DabSans-SemiBold.ttf`; the family name is `Dab Sans`. Install `dist/DabMono-*.ttf` for monospace.

## Repository layout

| Path | Contents |
|---|---|
| `sources/` | `Inter-VF.ttf`, `NotoSansSC-VF.ttf`, `GeistMono-VF.ttf`, and `OFL-Inter.txt`, `OFL-NotoSansSC.txt`, `OFL-GeistMono.txt` |
| `scripts/` | `build_dabfonts.py` (main build), `build_web_assets.py` (page subsets), `serve.py` |
| `dist/` | `DabSans-{Regular,SemiBold}.{ttf,woff2}` (text), `DabMono-{Regular,SemiBold}.{ttf,woff2}` (monospace), `OFL.txt` |
| `history/` | Snapshots from before a glyph-metric change, for comparison and rollback |
| `demo/` | `index.html` (three-way comparison), `punct.html`, `scale.html`, `align.html` |
| `build/` | Intermediates, safe to delete |

## Build

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

make build   # writes dist/
make web     # writes demo/fonts/ and demo/dabfonts-demo.html
make serve   # http://127.0.0.1:8099/index.html
```

Run `make build` before `make web`. `demo/fonts/` and `demo/dabfonts-demo.html` are generated and gitignored, so a fresh clone has no demo fonts until both commands run.

`build_dabfonts.py` runs these steps:

1. `varLib.instancer` instances both variable fonts at the target weight (Inter is fixed at `opsz=16`)
2. Inter's UPM is scaled from 2048 to 1000, then raised by `LATIN_DY`
3. Noto's punctuation is baked to half-width, then the CJK side is scaled by `CJK_SCALE` and lifted back to its optical centre
4. The `post` table format is normalized (Inter is format 2, Noto format 3; the merger cannot reconcile them)
5. Noto-only `vhea` / `vmtx` / `BASE` tables are deleted
6. `Merger().merge([inter, noto])` merges with Inter first, so Latin wins ties
7. One subsetter pass keeps GB2312 level 1 and deletes `locl` / `halt` / `palt` / `hwid`
8. The `name` table is rewritten; Noto's horizontal-writing metrics (OS/2 typo and hhea/win) are kept so CJK line height stays sane; the vertical tables remain deleted; TTF and woff2 are written

## Design notes

### Codepoint mapping

| Codepoint | Source | Notes |
|---|---|---|
| Latin letters, digits, Latin punctuation | Inter | Includes Greek, Cyrillic, and Vietnamese |
| Han | Noto Sans SC | 3,755 GB2312 level-1 characters, advance 940 |
| Chinese punctuation (28 marks) | Noto Sans SC | `hwid` + `halt` baked in, advance 470 |
| `“ ” ‘ ’` `…` `—` `·` | **Inter** | Shared codepoints, handled as “Latin punctuation uses Inter” |
| `〖〗` | Noto Sans SC | Stays full-width at 940 |
| Other full-width forms | Noto Sans SC | |
| Monospace runs (`code` / `pre` / paths / versions) | **Geist Mono** (family `Dab Mono`) | Separate family, not merged |
| Korean / Arabic / Devanagari / Thai / Extension B | — | Falls back to system fonts |

### Half-width punctuation

The 28 Chinese punctuation marks move from a full-width 1000 to a half-width advance. No shape was invented; the build uses Noto's own data:

| Mechanism | Count | Examples |
|---|---|---|
| `hwid` (GSUB half-width variants) | 10 | （ ） ［］ ｛｝ ， ． ／ ～ |
| `halt` (GPOS half-width metrics) | 18 | 。 、 〈〉《》【】〔〕「」『』 ！ ： ； ？ |

`halt`'s `XPlacement −500` is baked into the glyph as well (an opening bracket moves left with it). Both features are then deleted, so a browser that enables `halt` again cannot compress the marks a second time. A glyph-by-glyph comparison with the reference project (DabMusic) found zero difference in the ink x-range for the 24 shared marks; `「」『』` are this project's addition.

### CJK scale

`SFProPingFangSC-Regular.woff2` on the apple.com.cn home page scales system PingFang to **0.886** and lifts it by **44/1000 em** (advance 887, ink 0.822, cap 762, quotes 476 all agree). It produces a Han ink / Latin cap height ratio of **1.167** (1.317 before treatment).

This project copies the **ratio**, not the absolute factor: Noto's Han ink is smaller than PingFang's, so the proportional solve gives **0.94**:

| | Before | After | Apple |
|---|---|---|---|
| Han advance | 1000 | 940 | 887 |
| Han ink | 0.919 em | 0.864 em | 0.822 em |
| Ink / cap height | 1.242 | 1.168 | 1.167 |

The scale applies to outlines, advances, and composite offsets; `OS/2` typo metrics are untouched, so **line spacing stays the same and the glyphs get smaller**. The CJK side is then lifted by `center × (1 − scale)` (22/1000 em) to put the optical centre back.

### Vertical alignment

| Pair | Latin cap centre | Han centre | Residual |
|---|---|---|---|
| Original Inter / Noto | 0.3640 | 0.3755 | 0.0115 |
| Dab Sans | 0.3700 | 0.3751 | 0.005 |
| Apple's SF Pro / PingFang | 0.3530 | 0.3563 | 0.0033 |

`LATIN_DY` is a **paired** constant; changing the Han font requires recomputing it. With PingFang (Han centre 0.3563), Inter would have to move down instead.

### The `locl` trap

Noto Sans SC's GSUB carries `locl` lookups for language-specific forms. In the 2.004 source used here they hold 28 single substitutions — digits, quotation marks, dashes, and the ellipsis — none of which are Latin letters. The build strips `locl` along with the baked `halt` / `palt` / `hwid` features in the same subsetter pass, so the output cannot change with the page's `lang` attribute. Latin keeps Inter's glyphs and metrics (`A` advance 686 units). The file-level cmap / hmtx / glyf tables look correct either way; the GSUB feature list is where the substitution lives.

### Known tradeoffs

1. **Shared codepoints go to Inter:** quotes in Chinese body text are the narrow Western quotes, the ellipsis is three dots on the baseline, and the dash is the Western em dash.
2. **Han is limited to GB2312 level 1:** characters outside the 3,755 fall back to system fonts.
3. **Punctuation is already half-width**, so `palt` is unnecessary.
4. **Han advance is 940 rather than 1000:** at the same font size a line holds about 6% more characters than a conventional CJK font. Set `CJK_SCALE = 1.0` to revert.
5. **Only two weights:** there is no 300, 500, or 700.

## History

`history/` keeps the builds from before a metric change; see [history/README.md](history/README.md):

| Version | Contents |
|---|---|
| `v1-fullwidth` | First merged build: 20,976 Han characters, full-width punctuation |
| `v2-halfwidth-unscaled` | Half-width punctuation, 3,755 common characters, no CJK scale |

## License

SIL Open Font License 1.1. Derivatives are released under the OFL as well, and the font files may not be sold on their own.

- Inter: © The Inter Project Authors, OFL 1.1, no Reserved Font Name
- Geist Mono: © 2024 The Geist Project Authors, OFL 1.1, no Reserved Font Name (renamed `Dab Mono`)
- Noto Sans SC: © 2014–2021 Adobe, OFL 1.1, Reserved Font Name `Source` (this font's name does not contain `Source`)

Copyright notices are preserved in the font `name` table, in IDs 0 and 13, together with the OFL reference; nothing there narrows the grant. [NOTICE.md](NOTICE.md) collects the third-party notices and points at the upstream texts under `sources/`; [LICENSE](LICENSE) carries the license, and `dist/OFL.txt` carries the same text for anyone who copies `dist/` alone.
