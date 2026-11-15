# DabFonts Guideline

> **Version:** 1.0.0 · 2026-11-15
> **Read order:** this file → [`TYPESETTING.md`](TYPESETTING.md). This file is the summary; `TYPESETTING.md` is normative. The loading block below is copied from TYPESETTING §2.1 — canonical: TYPESETTING §2.1; if the two differ, §2.1 wins.

**One sentence: Chinese punctuation is spaced the way English punctuation is — the mark hugs the text before it, and one space follows it. Chinese only changes the codepoint; the spacing rule is identical to English.**

```text
English: Ship it. Then test.
Chinese: 先发布。 再测试。
```

## Loading

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

- `local("☺")` is **a font name that cannot exist**. It sits first in every `src` to force the browser to use the web font. Without it, a locally installed family of the same name takes priority and its weights and punctuation widths fall outside this specification. Both families need it on both faces.
- `"Dab Sans"` must be first in the body stack; system CJK fonts follow as fallback.
- Each family ships 400 and 600 only, one face per weight.
- `Dab Mono` belongs in the monospace stack only. Do not put it in `body`.

## Line height and weights

- **Set `line-height` explicitly.** Body copy uses 1.75–1.85; never go below 1.6. Han is scaled to 0.94, so glyphs are smaller than in a normal CJK font at the same size; leading must stay relatively loose.
- **Only 400 / 600.** 500 resolves to 400 and 700 to 600; do not rely on synthesized weights.
- **No italic, no small caps.** The font has neither; the browser would synthesize both. The emphasis treatment is the design system's decision.
- Exact font sizes, exact line-height values, measure, first-line indent, and weight-to-role mapping belong to the consuming design system. For the DabAZ site that is DabDesign's `core.md` §4.2 and §7; follow the project's pinned DabDesign revision. This repository owns the font and its consequences, not the scale.

## Monospace

- `Dab Mono` is built from Geist Mono and is used only for `code` / `pre` / `kbd` / `samp`; never for body text or headings. Its faces are declared in the canonical block above.
- Every character advances `0.6em`. The Latin side is raised by the same `0.0115em`, so inline `code` does not sit lower than the surrounding Han.
- The Chinese punctuation spacing rules do not apply inside code blocks.

## CJK–Latin mixing

- Between Han and Latin letters or digits: one space (`使用 Dab Sans 渲染 3,755 个汉字`).
- Between Han characters: zero (`中文字体`).
- Numbers and units: `10 GB`; the percent sign hugs the number: `12.8%`.
- English sentences use English punctuation; Chinese sentences use Chinese punctuation. Do not mix them.
- Never use U+3000 for indentation or alignment; use CSS `text-indent` / `margin` / `padding`. The indent value is the design system's decision.

## Do not write

`palt` / `halt` / `hwid` / `fwid` / `pwid`, `text-autospace`, `text-spacing-trim`, body `letter-spacing`, changed `word-spacing`, `font-style: italic`, `writing-mode: vertical-rl`, or a second `transform` on Latin runs.

## Fallback

The font contains 3,755 GB2312 level-1 Han characters. Rare characters fall back to system fonts and their glyphs run roughly 6% larger; check personal names, place names, and brand names one by one.
