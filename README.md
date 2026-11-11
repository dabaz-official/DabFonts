# DabFonts

个人项目用的中英混排字体：**Inter 4.001** 的拉丁部分 + **Noto Sans SC 2.004** 的中文部分，合并成单一字族。

- 汉字只保留 **GB2312 一级 3,755 个常用字**
- 中文标点烘焙成 Noto 自带的**半角**度量（烘焙时 500，随汉字缩到 0.94 后 advance 470）
- 中文字面整体缩到 **0.94**，以对齐 Apple 官网的中西文比例
- 拉丁上移 **0.0115 em**，与汉字光学中心重合

成果：9,312 字形 / 8,915 码位，TTF 1.9 MB，woff2 802 KB。

## 用法

排版与使用规范（中文标点空格、中英混排、字重与行高）见 [TYPESETTING.md](TYPESETTING.md)。

### 网页

```css
@font-face {
  font-family: "DabFonts";
  font-weight: 400;
  font-display: swap;
  src: url("/fonts/DabFonts-Regular.woff2") format("woff2");
}
@font-face {
  font-family: "DabFonts";
  font-weight: 700;
  font-display: swap;
  src: url("/fonts/DabFonts-Bold.woff2") format("woff2");
}

body {
  font-family: "DabFonts", -apple-system, BlinkMacSystemFont,
               "PingFang SC", "Microsoft YaHei", sans-serif;
}
```

- 只有 400 / 700 两个字重；中间字重会就近取用（500 → 400，600 → 700），不要依赖合成
- **不要**再开 `font-feature-settings: "palt"`，标点已经是半角
- 3,755 字之外的汉字会自动回落到后面的系统字体，这是设计行为

### 桌面

安装 `dist/DabFonts-Regular.ttf` 与 `dist/DabFonts-Bold.ttf` 即可，族名 `DabFonts`。

## 目录

```
sources/     Inter / Noto Sans SC 可变字体原件 + OFL 许可
scripts/     build_dabfonts.py（主构建）/ build_web_assets.py（页面子集）/ serve.py
dist/        DabFonts-{Regular,Bold}.{ttf,woff2}
history/     改动前的快照，供对照与回退
demo/        index.html（三方案对照）/ punct.html（标点）/ scale.html（缩放）/ align.html（垂直对齐）
build/       中间产物，可删
```

## 映射规则

| 码位 | 来源 | 备注 |
|---|---|---|
| 拉丁字母、数字、英文标点 | Inter | 含希腊文、西里尔文、越南文 |
| 汉字 | Noto Sans SC | GB2312 一级 3,755 字，advance 940 |
| 中文标点（28 个） | Noto Sans SC | `hwid` + `halt` 烘死，advance 470 |
| `“ ” ‘ ’` `…` `—` `·` | **Inter** | 共用码位，按"英文标点用 Inter"处理 |
| `〖〗` | Noto Sans SC | 保持全角 940 |
| 其他全角形式 | Noto Sans SC | |
| 韩文 / 阿拉伯文 / 天城文 / 泰文 / 扩展 B | — | 回落到系统字体 |

## 构建

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

make build   # 生成 dist/
make web     # 生成 demo/fonts/ 与 demo/dabfonts-demo.html
make serve   # http://127.0.0.1:8099/index.html
```

`build_dabfonts.py` 的流程：

1. `varLib.instancer` 把两个可变字体实例化到指定字重（Inter 固定 `opsz=16`）
2. Inter 的 UPM 从 2048 缩放到 1000，再上移 `LATIN_DY`
3. Noto 侧烘焙半角标点，再整体缩放 `CJK_SCALE` 并抬回光学中心
4. 统一 `post` 表格式（Inter format 2 / Noto format 3，合并器无法协调）
5. 删除 Noto 独有的 `vhea`/`vmtx`/`BASE`
6. `Merger().merge([inter, noto])`，Inter 在前 = 拉丁优先
7. 一次 subsetter：裁到 GB2312 一级 + 删除 `locl`/`halt`/`palt`/`hwid`
8. 重写 name 表，竖排度量沿用 Noto，输出 TTF + woff2

## 设计决策

### 半角标点

28 个中文标点从全角 1000 改成半角，没有自制造型，用的是 Noto 自带的两套数据：

| 机制 | 数量 | 例子 |
|---|---|---|
| `hwid`（GSUB 半角变体） | 10 | （ ） ［］ ｛｝ ， ． ／ ～ |
| `halt`（GPOS 半角度量） | 18 | 。 、 〈〉《》【】〔〕「」『』 ！ ： ； ？ |

`halt` 的 `XPlacement −500` 也一并烘进字形（开括号连带左移）。两套特性随后删除，
浏览器即使再次启用 `halt` 也不会二次压缩。与参考项目（DabMusic）的产物逐字比对，
24 个共有标点的墨迹 x 范围差值为 0；`「」『』` 是本项目额外加的。

### 中文字面缩放

apple.com.cn 首页的 `SFProPingFangSC-Regular.woff2` 是把系统 PingFang 整体缩到 **0.886**
再上移 **44/1000 em**（advance 887、墨迹 0.822、cap 762、引号 476 四项指标一致）。
它换来的是 汉字墨迹 / 拉丁大写高 = **1.167**（未处理 1.317）。

本项目复制这个**比例**而非绝对系数——Noto 汉字墨迹比 PingFang 小，按比例反解得 **0.94**：

| | 缩放前 | 缩放后 | Apple |
|---|---|---|---|
| 汉字 advance | 1000 | 940 | 887 |
| 汉字墨迹 | 0.919 em | 0.864 em | 0.822 em |
| 墨迹 / 大写高 | 1.242 | 1.168 | 1.167 |

缩放作用于轮廓、advance 和复合字形偏移；`OS/2` typo 度量不动，所以**行距不变、字变小**。
随后按 `center × (1 − scale)` 上移 22/1000 em 把光学中心抬回原位。

### 垂直对齐

| 对象 | 拉丁大写中心 | 汉字中心 | 残差 |
|---|---|---|---|
| 原始 Inter / Noto | 0.3640 | 0.3755 | 0.0115 |
| DabFonts | 0.3700 | 0.3751 | 0.005 |
| Apple 官网 SF Pro / PingFang | 0.3530 | 0.3563 | 0.0033 |

`LATIN_DY` 是**成对**常数，换中文字体要重算：若改用 PingFang（汉字中心 0.3563），Inter 反而要下移。

### 必须知道的坑：`locl`

Noto Sans SC 的 GSUB 带一个 `locl` 查找，包含 668 条拉丁字形替换。浏览器在 `lang=zh-CN`
页面上会自动启用，把每个 Inter 字母换回 Noto 版本（`A` 字宽 686 → 608），合并等于白做。
文件层面的 cmap / hmtx / glyf 全都正常，只有渲染出来量宽度才能发现。构建第 7 步整体剥离。

## 已知取舍

1. **共用码位归 Inter**：中文正文里的引号是西文窄引号、省略号是左下三点、破折号是西文 em dash。
2. **汉字限定 GB2312 一级**：3,755 字之外回落系统字体。
3. **标点已是半角**，不需要 `palt`。
4. **汉字 advance 940 而非 1000**：中文比常规 CJK 字体窄 6%，同字号一行能多放几个字。
   改 `CJK_SCALE = 1.0` 可退回。
5. **只有两个字重**，没有 300/500/600。

## 历史

`history/` 保存改动前的构建，详见 `history/README.md`：

| 版本 | 内容 |
|---|---|
| `v1-fullwidth` | 最初合并版：全量 20,976 汉字、全角标点 |
| `v2-halfwidth-unscaled` | 半角标点、3,755 常用字、未缩放 |

## 许可

SIL Open Font License 1.1。衍生字体同样以 OFL 发布，不得单独售卖字体本身。

- Inter：© The Inter Project Authors，OFL 1.1，无 Reserved Font Name
- Noto Sans SC：© 2014-2021 Adobe，OFL 1.1，保留字体名 `Source`（本字体名称不含 `Source`）

版权声明保留在字体 name 表中。本项目仅用于个人非商业用途。
