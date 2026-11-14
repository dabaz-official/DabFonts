# Changelog

All notable changes to this repository are recorded here. The format follows Keep a Changelog; versions follow semantic versioning.

## [Unreleased]

### Changed

- The font `name` table no longer carries a “personal, non-commercial use” sentence in IDs 0 and 13. It was never a term of the OFL, but a statement in the metadata reads like one; `LICENSE`, `NOTICE.md`, and the binaries now agree.
- File sizes in `README.md` and `TYPESETTING.md` were re-measured from the rebuilt `dist/`.

## [1.0.0] - 2026-11-15

First semantic-version release, aligned with DabAgents 1.0.0. The repository stays a font-and-specification dependency: no package, no npm artifact, no deploy target.

### Added

- `AGENTS.md`: repository role, pinned DabAgents commit, read order, commands, Definition of Done, and recorded exceptions.
- `LICENSE`: SIL Open Font License 1.1 notice with the Inter, Noto Sans SC, and Geist Mono copyrights, and the full license text.
- `dist/OFL.txt`: the same notice and license, so a consumer who copies `dist/` alone still receives it.
- `CHANGELOG.md`.
- `GUIDELINE.md` as the single English entry point, with a version and read-order header that routes to `TYPESETTING.md`.

### Changed

- `README.md` rewritten in English and reordered: identity and version, consumer usage, repository layout, build, design notes, history, license. Design derivation moved after usage and build.
- `TYPESETTING.md` rewritten in English section by section; technical constants, punctuation tables, and measured advances are preserved.
- The `@font-face` block now has one canonical copy in TYPESETTING §2.1, with all four faces carrying `local("☺")`. `GUIDELINE.md` holds a verbatim copy with a pointer to §2.1; `README.md` keeps only a pointer and the stack.
- The fallback stack is fixed to `"Dab Sans", -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif` in all three documents.
- File sizes, space widths, and font metrics now record measurements from the shipped `dist/` files.
- `README.md` and `TYPESETTING.md` state that Noto's horizontal metrics are kept and the vertical tables are deleted.
- `README.md` lists `GeistMono-VF.ttf` and `OFL-GeistMono.txt` in `sources/`.

### Removed

- The font-size table, the measure, and the first-line-indent values from `TYPESETTING.md` §5. Type scale, exact line-height values, measure, indent, and alignment strategy belong to DabDesign (`core.md` §4.2 and §7).
- The duplicated `@font-face` blocks from `README.md`.
- Stale claims that the family ships a third weight or keeps Noto's vertical metrics.

### Fixed

- Stale weight names corrected to `SemiBold` throughout the file paths, font-weight text, and metrics tables.
- The SemiBold space advance is documented as the measured 249 units.
- The `locl` note corrected: the Noto Sans SC 2.004 source carries 28 single substitutions (digits and punctuation), not 668 Latin substitutions; Inter's `A` stays at 686 units.
- woff2 and TTF sizes replaced with byte-exact values for all eight shipped files.
- The contradictory version/build date lines in `TYPESETTING.md` replaced by 1.0.0 and the release date.
- The weight list corrected: the font ships 400 and 600 only, with no 300, 500, or 700.
- `history/README.md` paths corrected to `../dist/DabSans-*`, `dist/`, and `scripts/build_web_assets.py`.
- The `build_web_assets.py` mono comment now records the measured ~35 KB size.
- The DabAgents pin now points to `ebd76db` on `main`; the previous SHA was an unreachable squash experiment.
- `AGENTS.md` exceptions now cite rule numbers and record the release-branch and no-package-script exceptions.
- `README.md` now states that `make build` must precede `make web`; the demo assets are generated and gitignored.

## Pre-1.0

Milestones before this changelog existed:

- Renamed the families to `Dab Sans` and `Dab Mono`.
- Shipped 400 and 600 instead of 400 and 700.
- Scaled the CJK side to 0.94 to match Apple's Latin/CJK proportion.
- Baked 28 Chinese punctuation marks to half-width metrics.
