# Dab Sans 使用准则

> 精简版。完整规范与推导见 `TYPESETTING.md`。

**一句话：中文标点按英文的方式留白——标点紧贴前文，标点后空一格。中文只是换码位，留白规则和英文完全相同。**

```text
英文：Ship it. Then test.
中文：先发布。 再测试。
```

## 加载

```css
@font-face {
  font-family: "Dab Sans";
  src: local("☺"), url("/fonts/Dab Sans-Regular.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: "Dab Sans";
  src: local("☺"), url("/fonts/Dab Sans-SemiBold.woff2") format("woff2");
  font-weight: 600;
  font-style: normal;
  font-display: swap;
}

body {
  font-family: "Dab Sans", -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
  font-synthesis: none;
}
```

- `local("☺")` 是**一个不存在的字体名**，放在 `src` 最前面，用于强制浏览器使用后面的 Web Font。本机若装有同名或同族字体，不加这句浏览器会优先用本地版本，字重和标点宽度都不可控。
- `"Dab Sans"` 必须排在字体栈第一位，后面跟系统 CJK 字体兜底。
- 只有 400 / 600 两档。

## 标点

中文用中文码位，留白按英文：

| 位置 | 空格数 | 例子 |
|---|---|---|
| 标点后接正文 | 1 | `先发布。␣再测试。` |
| 标点前 | 0 | `字体。`，不写 `字体␣。` |
| 相邻标点之间 | 0 | `。”`　`》，`　`）！` |
| 开符号与前文、内侧 | 0 | `他说：“好”`　`一份《规范》` |
| 破折号、省略号前后 | 0 | `字体——很精细`　`想了想……` |

- 省略号写 `……`，破折号写 `——`，间隔号用 `·`。
- 中文引号在字体里是 Inter 的窄引号，内侧永远紧贴内容，不要为"补宽"加空格。
- 标点已半角化，advance 为半个汉字（470/1000 em），右侧不再自带留白——这正是要补一个空格的原因。

## 等宽

```css
code, pre, kbd, samp {
  font-family: "Dab Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
}
```

- `Dab Mono` 来自 Geist Mono，只有等宽场景用它；正文不要用。
- 它的拉丁基线同样上移了 0.0115 em，行内 `code` 不会比旁边的汉字低。
- 400 / 600 两档，与正文字重一一对应。

## 中英混排

- 汉字与拉丁字母、数字之间：1 个空格（`使用 Dab Sans 渲染 3,755 个汉字`）
- 汉字与汉字之间：0 个（`中文字体`）
- 数字与单位：`10 GB`；百分号紧贴：`12.8%`
- 英文句子用英文标点，中文句子用中文标点，不混用。
- 不用 U+3000 缩进，用 `text-indent: 1.88em`（两个汉字）。

## 字重与强调

- 只用 400 / 600；500 会落到 400，700 会落到 600。
- 没有斜体、没有小型大写：`<em>` 用 600 并把 `font-style` 设为 `normal`。

## 不要写

`palt` / `halt` / `hwid` / `fwid` / `pwid`、`text-autospace`、`text-spacing-trim`、正文 `letter-spacing`、改 `word-spacing`、`font-style: italic`、`writing-mode: vertical-rl`、对西文的二次 `transform`。

## 回落

字体只含 GB2312 一级 3,755 个汉字。生僻字会回落到系统字体，字面大约大 6%；人名、地名、品牌名要逐个检查。
