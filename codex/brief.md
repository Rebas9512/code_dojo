# 标准做法：给 code-dojo 做一个开发任务

你在给 code-dojo 做一个开发任务。主控是另一个代理（Claude），负责派任务、验收和写开发笔记。你交付两样东西：项目里改好的文件，和一份报告。

## 项目是什么

code-dojo 是一个个人用的手写代码练习网站，类似 LeetCode，面向**零基础**的学习者。界面是中文。
- 判题：Python 题在 Docker 沙箱里跑（`judge/python/`），SQL 题以后在浏览器里用 PGlite 跑。
- 每道题配一节课，课按技能写：左栏是"题目 | 课 | 附加题 N"，右栏是 Monaco 编辑器，第三栏是 AI 助教。
- 题库是 `problems/<track>/` 下的文件，有技能图（`skills.yaml`），每道题最多引入 1 个新技能，学习曲线由检查脚本保证平滑。

技术栈：
- 后端：FastAPI + pydantic + SQLite，代码在 `server/app/`，测试在 `server/tests/`。
- 前端：React 19 + Vite 8 + TypeScript 7 + Monaco 0.57，代码在 `web/src/`。

动手前先读：
- `docs/README.md`：主文档，有怎么跑、代码结构、学习路线、各项设计。
- `docs/problem-format.md`：题目、技能、课的文件格式，是合同。
- 和任务相关的代码。
- 做内容时再读 `docs/curriculum.md`（题单规划、技能图规则）和 `docs/teaching-design.md`（教学设计）。
- 做界面时先读 `.impeccable.md`（设计约定）。
- **`codex/PLAN.md`**：总排期和文件归属。会有别的 codex 任务同时在跑，只改自己名下的文件和编号段。

## 硬约束

1. **不做任何 git 操作**：不 commit、不 add、不建分支、不改 `.git/`。
2. **不碰这些地方**：
   - `server/data/`：用户真实的做题记录。
   - `docs/reports/`、`docs/research_notes/`：调研报告，只读。
   - `codex/tasks/`、`codex/PLAN.md`：任务文件和排期。
   - 项目目录以外的任何地方。开发笔记的 vault 由主控写。
3. **不停也不占用户的服务**：用户自己的后端在 8000 端口、前端在 5173 端口，正在用，不要停、不要重启。测试另起实例：后端用 8001，前端用 5174。结束前关掉你自己起的进程，只关你自己起的。
4. **不调用真实 AI**：起后端测试实例时一律 `CODE_DOJO_AI_PROVIDER=off`；自动测试用 `FakeProvider`。不跑 `claude`、不跑 `codex`。AI 走用户的订阅，额度要省。
5. **依赖**：不加新依赖，除非任务里写了可以加。要加的话，Python 用 `uv add`，前端用 `npm install`，并在报告里写明。
6. **跟着现有代码走**：
   - 跟随现有风格：类型标注、pydantic 模型、函数式 React 组件、CSS 变量。
   - 界面文字和代码注释用中文。题干和讲解用中文，学习者要输入或输出的文字用英文。
   - 界面遵守 `.impeccable.md`：安静专注、字少、不用卡片堆砌、不加过渡动画、深色为主并支持浅色。
7. **改了行为就同步文档**：`docs/README.md`（目录、代码结构、相关设计节）和 `docs/problem-format.md`（格式有变就升版本号，并写清楚改了什么）。写法是"现在是什么样"，不写成变更日志。

## 怎么测

沙箱里 `uv run` 可能用不了（home 只读）。直接用项目里的虚拟环境：

```bash
cd {PROJECT_DIR}/server && .venv/bin/python -m pytest -q          # 全部后端测试（要 Docker 判题镜像，已经建好）
cd {PROJECT_DIR}/server && .venv/bin/python ../scripts/verify_bank.py --jobs 4   # 真实题库：加载 + 沙箱跑参考解
cd {PROJECT_DIR} && server/.venv/bin/python scripts/curriculum/check_curve.py     # 学习曲线平滑性检查（要 0 错）
cd {PROJECT_DIR}/web && npm run build                             # 类型检查 + 打包
```

起测试实例看接口和页面：

```bash
cd {PROJECT_DIR}/server && CODE_DOJO_DATA={RUN_DIR}/data CODE_DOJO_AI_PROVIDER=off \
  .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 &
cd {PROJECT_DIR}/web && CODE_DOJO_API=http://127.0.0.1:8001 npx vite --port 5174 --strictPort &
curl -s http://127.0.0.1:8001/api/tracks | python3 -m json.tool | head
```

改了判题镜像（`judge/python/`）才需要 `docker build -t code-dojo-judge-py:3.14 judge/python`。

页面截图可以不做，主控会在浏览器里验收。如果要截图，用 `{RUN_DIR}/` 放图，不要放进项目源码目录。

## 交付

- 改好的代码、内容和文档，直接改在项目里。
- `{RUN_DIR}/report.md`，用中文写，内容依次是：
  1. **做了什么**：按模块列出改动的文件，每个文件一句话。
  2. **自己定的事**：任务没写清楚、由你决定的地方，每条标"推断"并写理由。
  3. **测了什么**：命令 + 结果数字，比如 `pytest 40 passed`、`verify_bank 108/108`、`check_curve 0 错 0 警`、`npm run build` 通过。
  4. **没做完 / 已知问题**：标"未做"或"未测"。
  5. **请主控复查**：需要在浏览器里看的页面和操作步骤。
- 最后一条回复用几行说清楚：改了哪些模块、测试结果、报告路径。

## 做事方式

- 先通读相关代码再动手；大的重命名或迁移写成一次性脚本跑，脚本放 `{RUN_DIR}/`，不要留在项目里。
- 每完成一块就跑一次相关测试，不要攒到最后。
- 测试挂了先修，不要删测试、不要放宽断言来"通过"；确实是测试本身过时了，在报告里说明改了哪条、为什么。
- 拿不准的设计取舍，选更简单、更容易以后改的做法，写进报告"自己定的事"。
