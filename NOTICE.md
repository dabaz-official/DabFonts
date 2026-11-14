# Third-party notices

Dab Sans and Dab Mono are distributed under the SIL Open Font License,
Version 1.1 — see [`LICENSE`](LICENSE). This file records what each family is
built from, which upstream notices travel with it, and which reserved font
names apply.

## What each family is built from

| Family | Sources | Upstream license text |
|---|---|---|
| `Dab Sans` | Inter 4.001 — Latin, Greek, Cyrillic, digits, Latin punctuation — merged with Noto Sans SC 2.004 — GB2312 level-1 Han (3,755 characters) and CJK punctuation baked to half-width metrics | [`sources/OFL-Inter.txt`](sources/OFL-Inter.txt), [`sources/OFL-NotoSansSC.txt`](sources/OFL-NotoSansSC.txt) |
| `Dab Mono` | Geist Mono 1.701, statically instanced and renamed | [`sources/OFL-GeistMono.txt`](sources/OFL-GeistMono.txt) |

Both families are **Modified Versions** under OFL 1.1 §5: they are renamed, they
carry the upstream copyright notices, and they are released under the OFL and
no other license.

## Reserved font names

Noto Sans SC carries Reserved Font Name `Source`. OFL 1.1 §3 forbids a Modified
Version from using a reserved name, so the merged family is called `Dab Sans`.

The shipped binaries use these names:

| `name` ID | Dab Sans | Dab Mono |
|---|---|---|
| 1 (family) | `Dab Sans` | `Dab Mono` |
| 2 (style) | `Regular`, `SemiBold` | `Regular`, `SemiBold` |
| 4 (full) | `Dab Sans Regular`, `Dab Sans SemiBold` | `Dab Mono Regular`, `Dab Mono SemiBold` |
| 6 (PostScript) | `DabSans-Regular`, `DabSans-SemiBold` | `DabMono-Regular`, `DabMono-SemiBold` |

None of them contains `Source`, `Noto`, `Inter`, or `Geist`.

## Where the notices travel

- [`LICENSE`](LICENSE) — the license and the copyright notices, at the
  repository root.
- [`dist/OFL.txt`](dist/OFL.txt) — the same text, so a consumer who copies
  `dist/` alone still carries it.
- `sources/OFL-*.txt` — the upstream license files, kept verbatim.
- `name` IDs 0 and 13 in every binary — the copyright notices, readable by the
  user from the font itself (OFL 1.1 §2).

## Name table

`name` IDs 0 and 13 in every binary carry the copyright notices and the OFL
reference, and nothing else. An earlier build appended “created for personal,
non-commercial use”; that sentence was removed, because a statement in the
metadata reads like a license term and OFL 1.1 permits commercial use.
