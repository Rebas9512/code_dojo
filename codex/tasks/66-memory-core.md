# 66-memory-core：助教长期记忆的存储、同步、开关接口和聊天读写

## 背景
用户 2026-11-24 拍板："可以按64c的方案做"。方案在 `docs/tutor-memory.md`（先通读全文，它就是本任务的设计；运行记录 `codex/runs/64c-tutor-memory-agent-managed-*` 里的 report.md 有核验脚本可参考）。用户要的是"就有点像现在你开发目录下的这个memory功能这样就行 整体让agent自己管理我的学习进度这样的就可以"：没有记忆页面、不需要学生下"记住"指令，助教自己记、自己改、自己删。

本任务做设计文档"分两期实施"表里的前两行：**一 · 存储及设置接口**、**一 · 聊天**。后台学习回顾、附加题参考、网页开关由后面的任务做，这次不做。

## 要做的事
1. **存储和同步**（`server/app/db.py`、`events.py`）：按文档"存储、同步与清空"一节建 `memory_notes`、登记 `KEYS`、删除写成 `deleted=1` 的普通更新；`settings` 加 `memory_enabled`，缺省按开（1）读。逐行清空。
2. **设置接口**（`server/app/main.py`）：`GET/PUT /api/memory/settings`（`{"enabled": bool}`）和 `POST /api/memory/clear`。响应格式写进 `docs/README.md` 的 API 部分，后面的网页任务照这个接。
3. **聊天读写**（新 `server/app/ai/memory.py`、`ai/tutor.py`、`main.py`、`db.py`）：按文档"每轮怎么读""聊天与回顾共用的写入格式"两节：
   - 组索引、按当前题挑正文、上限按文档；放在提示词里文档指定的位置。
   - 开启时给 `tutor.SCHEMA` 加 `memory` 字段（Claude `--json-schema` 和 Codex `strict_schema` 都要能用）；关闭时用原 schema。
   - 写入指引照文档的三段写进提示词。
   - 只让最终有效答复的记忆操作落库一次；和助教消息在同一次写事务提交；比对 `sync_versions` 跳过期间被改过的 name。
   - 学生问"你记得我什么"时能照实说（靠提示词）。
   - 记笔记不计一次提示，前端不显示任何记忆回执。
4. **文档**：`docs/README.md` 的代码结构、AI 一节、同步一节写清现在的行为（"现在是什么样"）。`docs/tutor-memory.md` 里已经实现的部分，把"拟"改成现状；没做的（后台回顾、附加题、网页开关）保持原样。

## 这次不做
- 后台学习回顾（`main.tracks()` / `submit()` 触发的那部分）、`ai/extra.py`、任何 `web/`、`desktop/`、`bootstrap/` 改动。
- 记忆页面、回执、撤销。

## 验收标准
- 新 `server/tests/test_memory.py` 和现有 `test_sync.py`、`test_tutor.py`、`test_ai_agents.py` 覆盖文档表格里列出的情况：旧库迁移、异名合并、同名平局、删除先后两种事件顺序、重放、离线新增、旧客户端拒绝整批；两套 schema、跨题偏好、无关正文不进、索引完整、关闭时用原 schema、重试只写一次。全部用 `FakeProvider`，不调用真实 AI。
- `cd server && .venv/bin/python -m pytest -q` 全过（报告写数字；会碰 git 的同步测试也要跑，不要跳过——它们只在 pytest 临时目录里操作，不碰项目仓库）。
- 起测试后端用 8016，结束关掉。
- 报告"请主控复查"一节给出用 `FakeProvider` 或 curl 走一遍"聊天写入 → 换题读到 → 清空"的步骤。
