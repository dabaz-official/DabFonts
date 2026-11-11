# 历史快照

保留每次改变字形度量之前的构建，供对照和回退。

| 目录 | 汉字 | 标点 | 汉字 advance | 用途 |
|---|---|---|---|---|
| `v1-fullwidth/` | 20,976（全量） | 全角 1000 | 1000 | `demo/punct.html` 的「旧」栏 |
| `v2-halfwidth-unscaled/` | 3,755（GB2312 一级） | 半角 500 | 1000 | `demo/scale.html` 的「缩放前」栏 |

当前构建（`../DabFonts-*`）= v2 + 汉字缩放 0.94（advance 940）。

v1 只保留 TTF（网页对照用的子集由 `demo/build_web_assets.py` 生成）；
v2 保留 TTF + woff2。

回退方式：把对应目录里的文件复制回 `../` 覆盖即可，`build_web_assets.py` 会重新生成页面子集。
