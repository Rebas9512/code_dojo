# 31 · 字体统一成 Helvetica 风格并打包进应用，界面打磨一轮

## 背景

用户 2026-11-23 说："然后UI可以优化一下把一个固定字体打包进去行吗 用Helvetica吧"

Helvetica 是商业字体，不能打包分发。主控定的方案：
- **拉丁字母**：用 **TeX Gyre Heros**。它照 Helvetica 的字形做，GUST Font License 允许自由分发和嵌入。
- **中文**：用 **Noto Sans SC**（OFL）。
- **代码**：继续用 **JetBrains Mono**（OFL）。

三种字体都**打包在前端资源里**：不从网络加载，断网也能用，三个系统看起来一样。

现状：
- `web/src/main.tsx` 用 `@fontsource` 加载 IBM Plex Sans、Source Serif 4（标题用的衬线）、JetBrains Mono。
- 设计约定在 `.impeccable.md`：安静专注、字少、深色为主。

**并行**：30 号任务在同时做 Electron 外壳。它会新建 `web/src/components/DesktopBridge.tsx`，并在 `App.tsx` 里挂载。你不要动这两处，其余前端的样式和视觉归你。先读 `codex/PLAN.md`。

## 要做的事

1. **字体资源**：
   - TeX Gyre Heros：常规、粗体，需要的话加斜体。官方发布的是 OTF，转成 woff2 放进 `web/src/fonts/` 或 `web/public/fonts/`，附上许可证文件。
   - Noto Sans SC：用可变字体，或者 400 和 600 两个字重的 woff2。体积要控制，可以用 `unicode-range` 按需加载分片：@fontsource 的 Noto Sans SC 就是这么分片的，可以直接用它，它是打包在本地的。
   - JetBrains Mono：保留。
   - 去掉 IBM Plex Sans 和 Source Serif 4 的依赖。
2. **字体栈和排版**（CSS 变量）：
   - 正文和界面：`"TeX Gyre Heros", "Helvetica Neue", Helvetica, Arial, "Noto Sans SC", sans-serif`。拉丁字母走 Heros，中文落到 Noto Sans SC。确认中英文混排时基线和字号协调，中文可以略微调大或者调字距。
   - 标题：原来是衬线体，改用同一族 Heros 的粗体。按 Helvetica 的瑞士风格重新定字号层级、字距（大标题字距略收紧）、行高。
   - 代码：Monaco 编辑器、代码块、结果表、数字（等宽数字）都用 JetBrains Mono。Monaco 的 `fontFamily` 设置一并改。
3. **`.impeccable.md`**：排版部分改成新字体，写上"用户 2026-11-23 定：Helvetica 风格，用 TeX Gyre Heros 打包代替"。
4. **界面打磨一轮**：换字体以后，逐页过一遍，修间距节奏、层级、对齐、深色和浅色两种主题的对比度。不改功能和信息结构，遵守 `.impeccable.md`。要过的页面：
   - 学习地图（两个标签）
   - 题目列表
   - 知识点页
   - 做题页：题目、课、附加题标签、编辑器、结果、助教栏
   - 看数据作答题
   - SQL 题的结果表
   - 今日计划
   - 手感统计
   - 登录页
5. **截图对比**：每个页面在深色、1600 宽下各截一张"改前"和"改后"，再加 2–3 张浅色和 390 宽的。放在 `{RUN_DIR}/`，报告里列出来。

## 验收标准

1. `npm run build` 通过。报告里写字体资源的体积，以及首屏加载的字体大小。
2. 断网（只连本机后端）打开页面，字体照常显示：截图，并用浏览器的 Network 面板或者 Playwright 断言没有外部请求。
3. 前端测试和 `pytest -q` 照旧通过。
4. 改前和改后的截图齐全。
5. 用户的 8000 和 5173 实例没被动过，`server/data/` 没被改过。
