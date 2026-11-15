# Dab Sans Typesetting Specification

> **Version:** 1.0.0 · 2026-11-15
> **Applies to:** `dist/DabSans-{Regular,SemiBold}.{ttf,woff2}` — Inter 4.001 + Noto Sans SC 2.004 merged build
> **Read order:** [`GUIDELINE.md`](GUIDELINE.md) is the entry point; this file is the normative reference. §2.1 is the canonical `@font-face` block.

Dab Sans puts Latin and Han into one family: Latin, digits, and Latin punctuation come from Inter; Han and Chinese punctuation come from Noto Sans SC. It is not “another Chinese font” but a typographic scheme that places both scripts on one set of metrics. Its rules differ from those of an ordinary Chinese font — **punctuation most of all**.

**Hard rule: punctuation in a Chinese page follows the spacing of an English page — a mark hugs the text before it, and one space follows it.**

An English page is written that way already:

```
Ship it. Then test.
```

A Chinese page set in Dab Sans is written like this:

```
先发布。 再测试。
```

The only difference is the codepoint: `。` instead of `.`. The spacing rule is the same.

This rule applies to Dab Sans only. With PingFang, Source Han Sans, or another full-width punctuation font, follow that font's rules and do not copy the spaces used here.

This document is read in system fonts and follows conventional typography without added spaces; every example shows the spacing a Dab Sans page should contain.

## 0. Quick reference

| Item | Rule |
|---|---|
| Chinese punctuation | Use Chinese codepoints; after a sentence mark or closing mark followed by text, one U+0020; zero before the mark |
| Paired marks | An opening mark hugs the preceding text and the content; a closing mark followed by text takes one space |
| Adjacent marks | No space: `。”`, `》，`, `）！` |
| Dash / ellipsis | `——`, `……`; no space around a dash; no space before an ellipsis |
| CJK–Latin | One space between Han and Latin letters or digits |
| Han–Han | No space; do not use U+3000 |
| Weights | 400 / 600 only |
| Italic | None; emphasize with 600 or color |
| Line height | Body 1.75–1.85; always set explicitly |
| OpenType | Never enable `palt` / `halt` / `hwid` / `fwid` / `pwid` |
| Vertical writing | Not supported |
| Rare characters | Fall back to system fonts; glyphs run slightly larger |

## 1. Capability boundaries

| Capability | Status | Notes |
|---|---|---|
| Han | 3,755 characters | GB2312 level 1; characters outside the set fall back to system fonts |
| Half-width Chinese punctuation | 28 marks | advance 470; see §3.4 |
| Latin / Greek / Cyrillic / Vietnamese | Yes | Inter |
| Japanese kana | Yes | Noto; do not set Japanese with this font, Han coverage is incomplete |
| Korean / Arabic / Devanagari / Thai | No | Falls back to system fonts |
| Emoji | No | Falls back to system fonts |
| Weights | 400 / 600 | No 300 / 500 / 700 |
| Italic | None | Do not synthesize |
| Small caps | None | Do not synthesize |
| Vertical writing | None | `vhea` / `vmtx` were deleted in the build |
| Variable axes | None | Instantiated in the build |
| Monospace | `Dab Mono` | Geist Mono 1.701 renamed build, 400 / 600, monospace runs only |

This table decides two things. First, Dab Sans can only be the primary font, never the only font; a system font stack must follow it. Second, any attempt to “compress the punctuation a little more” or “emphasize with italic” exceeds what the font provides.

## 2. Loading

### 2.1 Web

This is the canonical `@font-face` block. If a copy elsewhere differs, this section wins.

```css
@font-face {
  font-family: "Dab Sans";
  src: local("☺"), url("/fonts/DabSans-Regular.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: "Dab Sans";
  src: local("☺"), url("/fonts/DabSans-SemiBold.woff2") format("woff2");
  font-weight: 600;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: "Dab Mono";
  src: local("☺"), url("/fonts/DabMono-Regular.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: "Dab Mono";
  src: local("☺"), url("/fonts/DabMono-SemiBold.woff2") format("woff2");
  font-weight: 600;
  font-style: normal;
  font-display: swap;
}

:root {
  --font-sans: "Dab Sans", -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
}

body {
  font-family: var(--font-sans);
  font-weight: 400;
  font-synthesis: none;
}

button, input, select, textarea {
  font: inherit;
}
```

Preload the weight used above the fold; preloading both is about 1.6 MB and usually not worth it.

```html
<link rel="preload" href="/fonts/DabSans-Regular.woff2"
      as="font" type="font/woff2" crossorigin>
```

Hard requirements:

- **Dab Sans must be first in the font stack.** Putting `Inter` or `PingFang SC` ahead of it lets the earlier font take over Han or Latin, and the merge is wasted.
- **Write the CSS family name as `"Dab Sans"`**, not `"Dab Sans Regular"`; `font-weight` selects Regular or SemiBold.
- **`local("☺")` in every `src`, ahead of the URL.** It is a font name that cannot exist, so the browser is forced to use the web font. Without it, a locally installed family of the same name takes priority and its weights and punctuation widths are outside this specification. All four faces carry it.
- **`font-synthesis: none`.** The font has no italic and no intermediate weights, and the browser must not fake either.
- **`font-display: swap` for body text**; screenshot and comparison pages may use `block` to keep FOUT out of measurements.
- **Self-host the files**; do not hotlink `dist/` as a CDN.
- **If you subset a page, include U+0020 and every punctuation mark the page uses.** Without the space, the browser supplies the fallback font's space (usually wider than 278) and the spacing after punctuation suddenly widens; the whole rhythm changes.

### 2.2 Desktop

Install `dist/DabSans-Regular.ttf` and `dist/DabSans-SemiBold.ttf`; the family name is `Dab Sans`. Select 400 or 600 in the application. Do not install only one and let the system synthesize the other.

In design tools such as Figma, map Regular to 400 and SemiBold to 600. Do not create 500 / 700 styles: the tool either picks the nearest weight or synthesizes one.

## 3. Punctuation rules

### 3.1 The six rules

**Choose the codepoint by language; apply one spacing rule to both.** Chinese body text uses Chinese punctuation; English sentences, code, and URLs use ASCII punctuation. Both follow “the mark hugs the preceding text, one space follows it”.

The tables below use `␣` to mark one U+0020 space so the position is visible; in real writing, type an ordinary space.

| No. | Rule | Example |
|---|---|---|
| R1 | After a sentence mark followed by text, add one U+0020 | `字体。␣页面`, `Inter，␣中文`, `结论：␣先合并` |
| R2 | No space before a mark | Write `字体。`, not `字体␣。` |
| R3 | No space between two adjacent marks | `。”`, `》，`, `）！` |
| R4 | An opening quote, bracket, or title mark hugs the preceding text and the content | `他说：“好”`, `页面（测试）`, `一份《规范》` |
| R5 | A closing mark hugs the content; when text follows, add one U+0020 | `“好。”␣然后`, `（测试）␣通过`, `《规范》␣我读了` |
| R6 | No space around a dash or middle dot; no space before an ellipsis; one space after an ellipsis that ends a clause and is followed by text | `字体——很精细`, `想了想……␣然后`, `弗拉基米尔·纳博科夫` |

R3 takes precedence over R1: in `他说：“好。”` the colon is immediately followed by an opening quote, so the colon takes no space; the space goes after the closing quote. Likewise, when `。` sits inside a closing quote, `。` and `”` are adjacent and take no space; the space goes after `”`: `他说：“好。”␣然后走了。`

R4 is the Chinese-specific exception: English puts a space before an opening parenthesis (`word (test)`); Chinese does not. Opening quotes, brackets, and title marks always hug the preceding text.

### 3.2 Why a space follows the mark

In the build, the 28 Chinese punctuation marks are first reduced to Noto's 500 half-width metrics, then scaled with the whole CJK side by 0.94, ending at **advance 470/1000 em**; Han is 940. A Chinese mark therefore occupies exactly half a Han character, and the half-character of built-in white space that traditional full-width punctuation provides is gone.

More importantly, the ink stays on the left of the frame and leaves very little white space on the right. Regular, in units /1000 em:

| Mark | advance | Ink right edge | Built-in right sidebearing | With one space |
|---|---|---|---|---|
| `。` | 470 | 326 | 144 | 422 |
| `，` | 470 | 309 | 161 | 439 |
| `、` | 470 | 321 | 149 | 427 |
| `？` | 470 | 434 | 36 | 314 |
| `》` | 470 | 442 | 28 | 306 |
| `”` | 429 | 392 | 37 | 315 |
| `）` | 470 | 338 | 132 | 410 |

A U+0020 in Regular is 278 (SemiBold 249). The “with one space” column adds the mark's own sidebearing to 278 and excludes the left sidebearing of the next character. With the space, right-side white space returns to 300–450, close to the breathing room of normal Chinese setting; without it, question marks, title marks, and closing quotes sit directly against the next character.

The rule is therefore not “adding an English habit to Chinese” but the necessary consequence of half-width punctuation: English separates words and clauses with spaces, and Chinese punctuation now needs the same treatment.

> “Half-width” in this document means **advance of half a Han character (470/1000 em)**, not replacing Chinese punctuation with ASCII characters. The glyphs are still `。，、`; only the width is halved.

### 3.3 Correct and incorrect

| Case | Correct | Incorrect |
|---|---|---|
| Full stop | `先做字体。␣再做页面。` | `先做字体。再做页面。` |
| Comma | `底层用 Inter，␣中文用 Noto。` | `底层用 Inter，中文用 Noto。` |
| Enumeration comma | `苹果、␣香蕉、␣梨` | `苹果、香蕉、梨` |
| Colon | `结论：␣先合并字体。` | `结论：先合并字体。` |
| Question / exclamation | `真的吗？␣我不信！` | `真的吗？我不信！` |
| Quotes | `他说：“好。”␣然后走了。` | `他说：␣“好。”然后走了。` |
| Parentheses | `这一版（v3）␣只改了标点。` | `这一版（v3）只改了标点。` |
| Title marks | `我读了《规范》，␣记了两页。` | `我读了《规范》␣，记了两页。` |
| Closing title mark | `我读了《规范》␣两遍。` | `我读了《规范》两遍。` |
| Ellipsis | `他想了想……␣然后走了。` | `他想了想␣……然后走了。` |
| Dash | `这套字体——真的很精细。` | `这套字体␣——␣真的很精细。` |

Copy-ready block:

```
先做字体。 再做页面。
底层用 Inter， 中文用 Noto Sans SC。
苹果、 香蕉、 梨
结论： 先合并字体。
真的吗？ 我不信！
他说：“好。” 然后走了。
这一版（v3） 只改了标点。
我读了《规范》， 记了两页。
我读了《规范》 两遍。
他想了想…… 然后走了。
这套字体——真的很精细。
```

### 3.4 Choosing the character

Chinese body text uses Chinese glyphs, not ASCII punctuation. The ASCII full stop is a solid dot and the Chinese full stop is a hollow circle; the ASCII comma is narrower and sits further left, both obvious inside Han text.

**Half-width Chinese punctuation (28 marks, advance 470)**

| Group | Characters | Count |
|---|---|---|
| Sentence marks | `。` `、` `，` `．` `！` `：` `；` `？` | 8 |
| Paired marks | `（` `）` `［` `］` `｛` `｝` `〈` `〉` `《` `》` `「` `」` `『` `』` `【` `】` `〔` `〕` | 18 |
| Other | `／` `～` | 2 |

**Shared codepoints and other exceptions**

| Character | Source | advance | Use |
|---|---|---|---|
| `“` `”` | Inter | 429 | Chinese double quotes; narrower than conventional Chinese quotes |
| `‘` `’` | Inter | 253 | Chinese single quotes; narrower than conventional Chinese quotes |
| `…` | Inter | 841 | Write two `……` for a Chinese ellipsis |
| `—` | Inter | 1000 | Write two `——` for a Chinese dash |
| `·` | Inter | 280 | Middle dot |
| `〖` `〗` | Noto | 940 | Still full-width; rarely used |
| U+3000 | Noto | 940 | Do not use for indentation |

The advance column is Regular; SemiBold quotes, ellipsis, and middle dot are slightly wider.

Writing conventions:

- Write the Chinese ellipsis as two `……` (U+2026 ×2), not `...` and not `。。。`.
- Write the Chinese dash as two `——` (U+2014 ×2), not `--` and not a single `—`.
- Use `·` (U+00B7) for the middle dot, not `•` or `.`.
- Outer quotes are `“”` and inner quotes `‘’`; outer title marks are `《》` and inner title marks `〈〉`.
- Chinese quotes in Dab Sans are Inter's narrow quotes. Do not add spaces inside them to “restore width”; the inside always hugs the content.
- Do not use the ideographic space U+3000 for indentation or alignment. Use CSS `text-indent` / `margin` / `padding`.

### 3.5 Line breaking and line edges

- A line never starts with `。` `，` `、` `；` `：` `！` `？` `）` `］` `｝` `〉` `》` `」` `』` `】` `〕` `〗` `”` `’`. The browser's default line-breaking rules handle this; do not break them with `word-break: break-all`, and do not use `keep-all`, which prevents Chinese sentences from breaking between Han characters.
- The space after a mark collapses at the end of a line; do not delete it by hand, and do not leave two trailing spaces — two trailing spaces in Markdown become a hard break.
- One space is enough; never type two. HTML collapses consecutive spaces, but the source should contain one.
- Do not use `&nbsp;` in place of an ordinary space. Use it only for a local case such as a short label that must not break.
- Do not substitute `&thinsp;`, U+2009, U+200A, or other narrow spaces for U+0020. The widths vary and break across fonts.

## 4. CJK–Latin mixing

Dab Sans has no CJK–Latin tracking: `kern` covers Latin glyphs only, and neither Han nor Chinese punctuation is in its coverage. A real space is therefore **required** between Chinese and Latin; the font will not open or close the gap by itself.

- Put one space between Han and Latin letters or digits: `使用 Dab Sans 渲染 3,755 个汉字。`
- Put no space between Han characters: write `中文字体`, not `中 文 字 体`.
- Use English punctuation and English spacing inside English runs, and Chinese punctuation inside Chinese runs: `Dab Sans 有两个字重。 It ships in 400 and 600. 中文继续。`
- When a Chinese quote contains an English sentence, keep English punctuation inside the sentence: `他说：“It works.” 然后走了。`
- Use ASCII punctuation inside numbers, version numbers, dates, percentages, and URLs: `3,755`, `8,915`, `12.8%`, `v3.2.1`, `2026-01-31`.
- Follow English convention for a number and its unit: `10 GB`, `24 px`; the percent sign hugs the number: `12.8%`.
- Set code, command lines, paths, and URLs in the monospace family; they do not follow the Chinese punctuation rules: `/fonts/DabSans-Regular.woff2`.
- Do not break English words: `word-break: normal`; use `overflow-wrap: anywhere` only for an overlong URL.
- Do not use `text-autospace` to insert space automatically. Browser support differs and it can add to a typed space; the typed space is the only source.

The monospace family is the separate `Dab Mono` (Geist Mono) declared in §2.1:

```css
code, pre, kbd, samp {
  font-family: "Dab Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
}
```

The Latin side of `Dab Mono` is also raised by 0.0115em, so inline `code` does not sit lower than the surrounding Han. Use it for monospace runs only; never for body text or headings.

A complete mixed-script example:

```
使用 Dab Sans 渲染 3,755 个汉字。
Dab Sans 有两个字重。 It ships in 400 and 600. 中文继续。
他说：“It works.” 然后走了。
3,755 个汉字、 8,915 个码位、 12.8%、 10 GB
```

## 5. Vertical rhythm

### 5.1 Line height

Two things are mandatory:

- **Set `line-height` explicitly.** The font's `line-height: normal` is about 1.45 (hhea 1160 / −288), and some engines may use OS/2 typo metrics and produce about 1.0. Both are too tight for Chinese body text.
- **Never go below 1.6.** Chinese has no word spaces, so tight leading turns a paragraph into a solid block. Dab Sans also scales Han to 0.94, making the glyphs smaller; the leading needs to be relatively looser, not tighter.
- **Do not compensate for the 0.94 scale with tracking or by scaling Han alone.** At the same font size Han sets about 6% smaller than in a conventional CJK font. If a legacy layout must match PingFang's Han size exactly, divide the font size by 0.94 and accept that Latin grows with it.

For body text, use 1.75–1.85. Exact font sizes, exact line-height values, measure, first-line indent, and alignment strategy belong to the consuming design system. For the DabAZ site those are DabDesign's `core.md` §4.2 (type scale) and §7 (layout); follow the project's pinned DabDesign revision. This repository does not define them.

### 5.2 Weights and emphasis

There are only two real weights, 400 and 600. Which role uses which weight belongs to the consuming design system.

- Do not use 300, 500, 700, or intermediate values such as 450. CSS resolves 500 to 400 and 700 to 600; the font has no variable axis, so intermediate values do not interpolate. “It looks like it worked” only means the browser rounded to the nearest weight.
- Do not use italic. The font has no italic and the browser will synthesize an oblique; Han glyphs deform.
- Do not use `font-variant: small-caps`. There are no small capitals and the browser will synthesize them.

`<em>` and `<i>` are italic by default and must be reset. The replacement emphasis style (weight or color) is the design system's decision:

```css
em, i {
  font-style: normal;
}
```

### 5.3 Alignment, tracking, and features

Alignment strategy, tracking policy, and numeral style belong to the consuming design system. The points below are the font's constraints, not a second scale.

- Justified text stretches the spaces after punctuation along with everything else, which produces uneven gaps on lines with many marks. If the design system calls for `justify`, check each line.
- Body text uses `letter-spacing: 0`. If tracking is used at all, keep it at or below `0.02em`; `letter-spacing` also acts on punctuation and spaces and therefore erodes the calibrated half-width rhythm.
- Keep `word-spacing: normal`. Do not use it as a substitute for typed spaces.
- Keep the default `font-kerning`; Latin spacing is part of Inter and must not be disabled.
- Do not apply `transform: translateY`, `scale`, or a separate `font-size` to Latin `<span>` elements. The font already carries the 0.0115em Latin lift and the 0.94 Han scale; a second adjustment breaks baseline alignment.
- Keep `font-feature-settings` at its default. Use `font-variant-numeric: tabular-nums` for tabular figures, and `slashed-zero` when 0 and O must differ.
- `font-optical-sizing` has no effect: Inter was fixed at `opsz=16` in the build and the output has no variable axis.

## 6. CSS prohibition list

| Do not write | Reason | Instead |
|---|---|---|
| `font-feature-settings: "palt" 1` | The feature was removed from the font; fallback fonts may respond and widths diverge | Nothing; punctuation is already half-width |
| `font-feature-settings: "halt" 1` | Same | Same |
| `font-feature-settings: "hwid" 1` | Same | Same |
| `font-feature-settings: "fwid" 1` | Switches some ASCII punctuation back to full-width | Keep the default |
| `font-feature-settings: "pwid" 1` | Switches to proportional widths and breaks the 470 rhythm | Keep the default |
| `font-variant-east-asian: full-width` | Same | Keep the default |
| `font-variant-east-asian: proportional-width` | Same | Keep the default |
| `text-spacing-trim` / `text-autospace` | Inconsistent support; uncontrolled stacking with typed spaces | Type one U+0020 |
| Body `letter-spacing` | Stretches punctuation and spaces together | `0`; any tracking at most `0.02em` |
| Changed `word-spacing` | Changes the calibrated space width | `normal` |
| `font-style: italic` | No italic; the browser synthesizes an oblique | 600 or color |
| `font-weight: 300 / 500 / 700` | No such weights; 500 → 400, 700 → 600 | 400 / 600 |
| `font-variant: small-caps` | No small capitals; synthesis looks wrong | Uppercase or 600 |
| `font-stretch` | No width axis | Normal |
| `writing-mode: vertical-rl` | No `vhea` / `vmtx`; vertical metrics do not exist | Horizontal writing |
| Inline `transform` / `scale` on Latin | The font already contains the alignment; a second transform misaligns it | Leave it alone |
| Body `white-space: pre` | Preserves leading spaces and breaks space collapsing and line breaking | `normal` |

## 7. HTML / Markdown source rules

HTML collapses newlines and indentation into one space. For Dab Sans this is both a tool and a trap: after a punctuation mark it is exactly the space you want; between two Han characters it is a space that should not exist. Every rule below follows from the font itself, not from a separate content style:

- The space after a mark must be a real text node. When a mark and the next sentence sit in adjacent inline elements, keep the space between the tags:

```html
<p>先做字体。 <span class="accent">再做页面。</span></p>
```

  The font's 470 advance plus a real U+0020 is the calibrated pair; the space inside the opening tag is not emitted, and an inline element does not create it.
- Do not put the space inside a tag, and do not rely on a `display: block` child to produce the gap. The browser's rendered space is what the half-width metrics were matched to.
- Use `<p>` for Chinese paragraphs, not `<br>` to create paragraph spacing. The font's leading is carried by `line-height`; a forced break bypasses it.
- Write punctuation in the text, not with CSS `::before` / `::after`. Generated content cannot reliably supply the following U+0020, and whitespace at the edges of generated content is not preserved consistently.
- Set `lang="zh-CN"` on the page and `lang="en"` on English runs. The build deleted `locl`, so no `lang` attribute can switch shared codepoints to Noto's language-specific forms; Latin stays Inter's (`A` 686 units).
- In Markdown, two trailing spaces are a hard break. The space after punctuation must be one interior U+0020, never a trailing space.
- Set body `white-space: normal`; reserve `pre` for code blocks. Preserved whitespace defeats the collapsing that the punctuation spacing relies on.

## 8. Rare characters and fallback

Dab Sans keeps only the 3,755 GB2312 level-1 Han characters. `囧`, `屌`, `垚`, `犇`, `淼`, `龘`, and `𠮷` are not in the font and fall back to the system font later in the stack.

The problem with fallback is not “a missing character” but “a different one”:

- A system CJK font has a Han advance of 1000, Dab Sans has 940; at the same font size the rare character looks about 6% larger, and stroke weight and optical centre may differ.
- Personal names, place names, brand names, and classical quotations are the danger zones. Check every occurrence on a page.
- Japanese kana are in the font, but Han coverage is GB2312 level 1 only; do not set Japanese with Dab Sans.
- Korean, Arabic, Devanagari, Thai, and emoji fall back to system fonts; the stack must contain a complete system CJK fallback.
- If a page is mostly rare characters, do not use Dab Sans, or extend the subset; that is outside this specification.

## 9. Pre-release checklist

- [ ] All Chinese punctuation uses Chinese codepoints; no ASCII `. , ; : ! ?` substitutes
- [ ] Every sentence mark or closing mark followed by text has exactly one U+0020
- [ ] No space before a mark
- [ ] No space between adjacent marks (`。”`, `》，`, `）！`)
- [ ] No space inside an opening quote, bracket, or title mark
- [ ] A closing quote, bracket, or title mark followed by text has one space
- [ ] Dashes are `——` and ellipses are `……`
- [ ] Han and Latin letters or digits are separated by a space; Han characters are not
- [ ] U+3000 is not used in place of a normal space; `&nbsp;` appears only in short labels that must not break
- [ ] Only 400 / 600 are used; no italic, synthesized weight, or synthesized small caps
- [ ] Body `line-height` is at least 1.6
- [ ] `palt` / `halt` / `hwid` / `fwid` / `pwid` are not enabled
- [ ] Code blocks, URLs, and paths use the monospace family
- [ ] Personal names, place names, and rare characters were checked for fallback
- [ ] The page has `lang="zh-CN"` and English runs have `lang="en"`

Overall acceptance criteria: DabAgents rule 04, `rules/04-quality.md`.

## 10. Technical parameters

| Item | Value |
|---|---|
| Family | Dab Sans |
| Weights | Regular 400 / SemiBold 600 |
| UPM | 1000 |
| Codepoints / glyphs | 8,915 / 9,312 |
| Han | 3,755 GB2312 level-1 characters, advance 940 |
| Half-width Chinese punctuation | 28 marks, advance 470 (500 × 0.94) |
| Latin | Inter 4.001, `opsz=16`, raised 0.0115em |
| Han scale | 0.94, optical centre preserved |
| Space | 278 (Regular) / 249 (SemiBold) |
| Vertical metrics | typo 880 / −120 / 0; hhea and win 1160 / −288 |
| Default line height | `normal` ≈ 1.45 (do not rely on it) |
| Vertical writing | No `vhea` / `vmtx` |
| Italic / variable axes / small caps | None |
| Files | Sans per weight: TTF 1,947,056 B (Regular) / 1,946,776 B (SemiBold); woff2 820,348 B / 835,400 B (801.1 / 815.8 KiB). Mono per weight: TTF 102,424 B / 102,396 B; woff2 35,432 B / 36,744 B (34.6 / 35.9 KiB) |
| License | SIL Open Font License 1.1 |

OpenType features:

- Retained by default: `kern` (Latin only), `liga`, `calt`, `ccmp`, `mark`, `mkmk`.
- Available: `tnum`, `pnum`, `zero`, `sups`, `subs`, `case`.
- Removed: `locl`, `halt`, `palt`, `hwid`.
- Do not enable: `fwid`, `pwid`.

## 11. License

Dab Sans and Dab Mono are released under the SIL Open Font License 1.1. They may be embedded in web pages and PDFs and redistributed with a project; the font files may not be sold on their own, and derivatives must also be released under the OFL. Copyright notices are preserved in the font's `name` table.

- Inter: © The Inter Project Authors, OFL 1.1
- Noto Sans SC: © 2014–2021 Adobe, OFL 1.1, with Reserved Font Name `Source`
- Geist Mono: © 2024 The Geist Project Authors, OFL 1.1

The font `name` table carries the copyright notices and the OFL reference in IDs 0 and 13. Nothing there narrows the license: OFL 1.1 permits commercial use.

---

This document describes v1.0.0. All sizes and metrics were measured against the files in `dist/`. After changing `CJK_SCALE`, `LATIN_DY`, or `HALFWIDTH_PUNCT`, re-measure §3 and §10.
