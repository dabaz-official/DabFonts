# AGENTS.md

This repository is a **typography dependency repository**, not a web application. It ships font files and the specification for using them. There is no `package.json`, no npm package, and no deploy target; consumers copy files from `dist/`.

## Required reading

1. **DabAgents** @ `v1.0.2` — <https://github.com/dabaz-official/DabAgents>. Start at `rules/01-operating.md`, which routes to the other rules.
2. **This repository** — [`GUIDELINE.md`](GUIDELINE.md), then [`TYPESETTING.md`](TYPESETTING.md). `GUIDELINE.md` is the only entry point; `TYPESETTING.md` §2.1 is the canonical `@font-face` block.

Branching, commits, releases, and review follow DabAgents rule 03. Record a project exception here rather than restating the rule.

Conflict order: the consuming project's `AGENTS.md`, then this repository's `GUIDELINE.md` / `TYPESETTING.md`, then DabAgents.

## Commands

```sh
make venv    # create .venv and install requirements.txt
make build   # rebuild dist/ from sources/
make web     # rebuild demo/fonts/ and demo/dabfonts-demo.html
make serve   # serve the demo at http://127.0.0.1:8099/index.html
make clean   # remove build/ and generated demo assets
```

## Definition of Done

- [ ] Documentation and `dist/` agree: every file size, glyph count, advance, and metric in the docs was measured from the shipped files, not copied from memory.
- [ ] `make web` completes, given `dist/` and the `build/` intermediates from `make build`.
- [ ] `GUIDELINE.md` still routes to `TYPESETTING.md`, and the `@font-face` block exists only in TYPESETTING §2.1 plus its verbatim copy in `GUIDELINE.md`.
- [ ] The fallback stack is identical in `GUIDELINE.md`, `TYPESETTING.md`, and `README.md`.
- [ ] No claim about a weight, feature, or table that the binaries do not contain.
- [ ] Repository artifacts and commit messages are in English.

## Boundaries

This repository owns the font files, family names, `@font-face`, the fallback stack, `font-synthesis`, `font-display`, preload, the available weights, the absence of italics and small caps, Chinese punctuation spacing, CJK–Latin spacing, capability limits, fallback behavior, and licensing.

DabDesign owns the type scale (`type-*` font sizes), exact line-height values, measure, first-line indent, alignment strategy, tracking, numeral style, and weight-to-role mapping. Do not add those values here; link to `DabDesign/GUIDELINE.md` instead.

## Versioning

Versions are this repository's own; they do not track DabAgents or DabDesign.
Consumers pin all three independently.

- **Major** — the glyph set, a metric, or the family and `name` table changes,
  so an existing page reflows or the family stops being a drop-in.
- **Minor** — the specification gains a rule or a capability that leaves
  existing rendering unchanged.
- **Patch** — licensing, notices, wording, or metadata that does not change
  rendering.

## Exceptions

Recorded under DabAgents rule 04 §9. Owner: repository maintainer. Review date: 2027-11-14.

- **No CI.** `rule 04 §3`. The repository produces static font files and Markdown; there is no test runner or service to exercise. Verification is `make web`, `ls -l dist/`, and the fact-checking commands in the release checklist.
- **No unit tests.** `rule 04 §7`. The build is a one-shot artifact pipeline whose output is inspected as fonts and rendered pages, not as library functions. A change is verified by comparing `dist/` metrics and the demo pages.
- **No deploy target.** `rule 06`. Consumers copy `dist/` into their own projects. There is no staging or production surface to deploy.
- **No package-script gate.** `rule 04 §1` / `§8`. The repository has no `package.json`; the Makefile targets replace the canonical scripts, and `make web` plus the release checklist replace `pnpm check`.
- **Committed `dist/` and `history/`.** `rule 03 §7`. Here `dist/` is the product (TTF, woff2, and the OFL notice) and `history/` holds rollback snapshots, so both are versioned on purpose. Review date: 2027-11-14.

## Language

Repository artifacts are written in English. Replies to the user follow the user's language.
