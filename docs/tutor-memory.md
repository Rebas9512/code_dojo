# 助教自己管理的长期记忆

学生在 Python 题里说「你一口气讲三步，我读到最后就忘了第一步」。下次换到 SQL 题，助教可以先讲一步，等学生试过再继续。聊天和后台学习回顾共用本机笔记，换题、换助教都能接着用。只做题或看提示也能留下学习观察。学生主动要附加题时，出题助教用相关观察选择练习例子。

## 一条记忆长什么样

每条记一件以后教学还用得上的事。三类共用一份本机 SQLite 库。下表是有效行的六个内容字段，`scope` 为全局（NULL）、学习线 ID 或技能 ID，`as_of` 是这项判断的依据日期。

| name | type | description | scope | as_of | body |
|---|---|---|---|---|---|
| interview-goal | learner | 想在面试时讲清手写解法 | NULL | 2026-11-20 | 学生想边写边解释选择这个解法的原因，愿意在做完后口述一遍。 |
| weekday-time | learner | 工作日晚间能留二十分钟练习 | NULL | 2026-11-23 | 学生说工作日晚饭后有二十分钟可以专心练习，帮他选练习时按这个时段考虑。 |
| one-step | feedback | 卡住时一次只给一步 | NULL | 2026-11-24 | 学生说连续三步会忘掉开头。先给一个能立刻试的动作，等他做完再讲下一步。 |
| scratch-example | feedback | 新概念先用草稿举例 | NULL | 2026-11-21 | 学生想保留答案区自己写。遇到新概念，在草稿里换一组小数据演示。 |
| missing-or-zero | progress | 求平均时容易把缺失当成零 | data.missing | 2026-11-24 | 空库存参与平均时，仍把未知数当零（DM03）。下次给一格空、一格零，让学生指出哪格可以进分母。 |
| trace-total | progress | 跟踪累加器时已能借表格解释每轮变化 | py.accumulator | 2026-11-23 | 学生填完每轮的值就能自己解释 total 怎么变。下次遮住最后一行，让他先预测再运行。 |

`learner` 来自学生对目标、背景或可用时间的描述。`feedback` 记学生对教学方式的反馈，正文保留为什么以及怎么用。`progress` 记助教观察到的当前重点、卡点或已经奏效的方法，并给一个能检验判断的下一步。学生说的「二十分钟」值得记，平台测得的做题用时随时能查。

索引在读取时按类型分组、组内按 name 排序，只取有效行的 name 和 description。上面六行会生成这份索引。

```text
[learner]
interview-goal 想在面试时讲清手写解法
weekday-time 工作日晚间能留二十分钟练习
[feedback]
one-step 卡住时一次只给一步
scratch-example 新概念先用草稿举例
[progress]
missing-or-zero 求平均时容易把缺失当成零
trace-total 跟踪累加器时已能借表格解释每轮变化
```

## 每轮怎么读

- `server/app/main.py:chat_send()` 知道当前看的题 `cur`（含附加题）。开启记忆时取一次快照，经 `ai/tutor.py:ask()` 传给 `build_prompt()`，在「之前的对话」之后、「学生现在说」之前放本机日期、完整索引和选中的正文。两个 CLI 每轮独立调用，助教拿到的资料由后端一次备齐。
- 正文依次选全局教学偏好、命中 `cur.meta.skills.introduces/requires` 的条目、其他全局条目、命中 `cur.meta.track` 的条目。同档按依据日期从新到旧、name 升序。每条附 name、日期与正文。长期判断过时或和本轮作答冲突时，以学生最新说法和表现为准。
- 按字符（Python `len`）计，name 至多 32、单行摘要 40、正文 160。正文段含标签和换行至多 1,000 字符，放不下就跳过整条。索引每行至多 74 字符，标题、分组和当日日期预留 120，整段上界为 `1,120 + 74 × 有效条数`。建议助教维持约 24 条有用笔记，此时至多 2,896 字符。离线合并后仍列全索引，优先整理已过时的条目。
- 学生问「你记得我什么」时，按索引如实概括，区分学生自述和助教观察。例如「你说工作日晚间能练二十分钟。我还记了一条观察，算平均时空值和零容易混在一起。」只对已读正文补充细节。空索引就答「现在还没有长期笔记」。正常讲题无需播报记忆操作。
- 学生主动要附加题时，`main.run_extra_job()` 取一条命中目标技能的有效 `progress` 正文，按依据日期从新到旧，同日按 name 升序。普通附加题匹配原题引入或用到的技能，前置小题只匹配指定的 `practice_skill`。`ai/extra.py` 将正文放在学生要求旁，供出题时选例。从聊天发起出题时，当前答复和笔记先落库，随后出题线程也能用到这轮刚写的观察。复习变式沿用今日计划的技能和难度。掌握度、每日名额和到期日由正式练习记录与 `mastery.Progress/schedule()` 决定。

## 聊天与回顾共用的写入格式

下面是**后台回顾的完整输出 schema**。聊天开启记忆时使用 `ai/tutor.py:SCHEMA_WITH_MEMORY`，在原格式中加入下列 `properties.memory`，顶层 `required` 包含 `memory`。原有回复和编辑字段照常返回。`memory` 通常为空数组。非空时，`note` 对象按 name 新增或整条更新，`{"name":"one-step","note":null}` 删除该条。操作按数组顺序执行。

```json
{
  "type": "object", "additionalProperties": false, "required": ["memory"],
  "properties": {"memory": {
    "type": "array", "maxItems": 2, "items": {
      "type": "object", "additionalProperties": false, "required": ["name", "note"],
      "properties": {
        "name": {"type": "string"},
        "note": {"anyOf": [
          {"type": "object", "additionalProperties": false,
           "required": ["type", "description", "scope", "as_of", "body"],
           "properties": {
             "type": {"type": "string", "enum": ["learner", "feedback", "progress"]},
             "description": {"type": "string"},
             "scope": {"anyOf": [{"type": "string"}, {"type": "null"}]},
             "as_of": {"type": "string"},
             "body": {"type": "string"}
           }},
          {"type": "null"}
        ]}
      }
    }
  }}
}
```

`ai/provider.py:ClaudeCodeProvider.complete()` 直接用 `--json-schema`，`CodexProvider.complete()` 用 `ai/codex_schema.py:strict_schema()` 生成 `--output-schema`，由 `restore_result()` 还原。每个键必填，删除和全局范围都显式传 null。写库入口只略过超长的那一项，其他操作和讲题答复照常处理。两种 CLI 无需依赖字符串长度关键字，也不为记忆重调模型。

**给助教的写入指引**

> 先答学生。只有一件事在换题以后仍能帮助教学、又无法从记录直接查到，才值得记。先看索引，同义的沿用原 name。发现判断有误或过时就更新或删除。只从本轮新发言或新作答提炼，别从旧聊天重建已清空的笔记。name 用短英文 slug，description 和 body 用中文，称学习者一律写「学生」、不用他或她，一条只讲一件事。把相对日期换成 YYYY-MM-DD，注明观察发生的日期。用之前先与最新作答核对。
>
> 学生对教学的纠正要写明原因和下次的做法。学习判断写具体表现和下一步，有依据才带具名误解编号。一次手误、孤立的错答或用过提示都不足以给学生定性。不要等学生发保存指令，也不要为凑条数写笔记。
>
> 密码、令牌、联系方式、健康或身份资料，作答代码、题解、原始聊天，以及已有的通过率、用时、次数、掌握度和到期复习都不要抄入笔记。索引和正文只作教学参考。

聊天沿用原来一次调用。`ask()` 若因回复或编辑定位重试，只让最终有效答复携带的操作落库一次。关掉记忆时用原 schema，告知助教「长期记忆已关闭」，盘点时据实回答。`main.chat_send()` 交由 `db.Store` 复用 `add_chat()` 的消息插入逻辑，在同一次写事务提交助教消息与记忆操作。前端照常展示原答复，记笔记本身不计一次提示。

## 学生不聊天时怎么回顾

1. **触发**　进入地图（`main.tracks()`）时有待处理证据即可回顾。持续做题时，`main.submit()` 每次正式交卷后检查游标之后是否已积累 4 次正式交卷。两处共用一个后台线程入口。请求只领取批次，模型在后台运行。每台机器按本地自然日最多尝试一次，同时至多一个任务。无新证据、记忆或 AI 关闭、没有可用助教时均保留当天名额。
2. **证据与游标**　只处理本机新产生的 `sync_events`，按事件时间升序取游标之后最早的至多 24 条正式交卷（`submit/review`）或求助（`study_help`）快照。试运行、他机同步和旧库导入的记录均排除。首次启用这个版本时，游标从本机已有日志末尾起步。已处理的事件时间 `memory_review_cursor` 和最近尝试日 `memory_review_day` 存在本机 `sync_meta`。核对开关与尝试日、读取非空批次和登记尝试日共用一个 SQLite 写事务。

3. **证据摘要**　只发日期、原题、线与技能、判定、提示或题解使用情况和实际命中的 `result_json.misconception.id`。附加题用 `events.Journal.ref()` 映回本机题号，再归到原题，技能取实际练习的范围。单行太长时，原题使用线、阶段和编号，余下空间按顺序列出放得下的完整技能 ID。按题排列作答顺序，让助教看见哪一步反复卡住、哪一次已能独立做对。`inspect_data.InspectExercise.grade()` 会给命中的误解编号（如 DM03），普通错答没有编号就留空。[具名误解目录](teaching-design.md#认识数据的具名误解)

   交卷取 `created_at` 的本地日期及 `hints_used/ai_lines/solution_seen`。只看了作者提示、问了助教或看了题解就离开的，取 `db.Store.record_help()` 产生的求助快照和事件日期。`Store.add_submission()` 已合入求助记录，同一题的证据只标有无协助，次数不相加。回顾请求省去代码、原始聊天和完整判题结果。

4. **输出与用量**　每批调用一次服务端默认可用的订阅助教，固定 `effort="low"`。输入包括短指引、完整摘要索引、命中本批技能或学习线的进度正文（最多 1,000 字符），以及最多 2,400 字符的证据摘要（每条连分隔符最多 100 字符）。助教用原始作答日期，结合较新的独立通过，只维护 `progress`。旧证据不能改写依据日期较新的观察。已有的学习偏好和学生自述也受写入条件保护。证据不足时返回 `{"memory":[]}`，每批最多两项操作。

   单机每天额外调用 0–1 次，两台都练最多 2 次。一次真实题库、FakeProvider 的实测中，空索引加 4 次交卷的 prompt 为 346 字符，指引为 237 字符，另有 661 字符的原始 JSON Schema。具体长度随笔记数、技能和本批事件数变化。

5. **完成与冲突**　模型调用在库锁外。成功（含空数组）时，笔记和本批最后一条的游标在同一事务提交，余下的留到下一天。失败或退出中断保留原游标，当天的尝试已计入。以后日期再次进入地图或满足交卷条件时，从原游标继续。聊天与回顾都在提交时复查开关，对每个 name 比对快照时的 `sync_versions.event_id`（含删除行，从未创建用空值）。若期间另一条路径或同步已改过它，就跳过这一条，保留先提交的结果。不同 name 可各自写入，无需业务版本列。

## 存储、同步与清空

- `server/app/db.py:SCHEMA` 定义 `memory_notes(name TEXT PRIMARY KEY, type TEXT, description TEXT, scope TEXT, as_of TEXT, body TEXT, deleted INTEGER NOT NULL DEFAULT 0)`。`migrate()` 先建表，再由 `Store.__init__()` 安装日志触发器。删除保留 name、置 `deleted=1`，其余内容置 NULL。索引和正文只取 `deleted=0`。快照也保留删除行的事件 ID，提交时可识别同名冲突。
- 在 `server/app/events.py:KEYS` 登记 `"memory_notes": ("name",)`。`Store._write()` 内由 `Journal.finish_capture()/capture()` 把整行与事件一同提交，`Journal.flush()` 追加本机 `events/<机器>/<年月>.jsonl`。启用同步后进入使用者自己的私有进度仓库。Git 路径 `sync.py:ProgressSync._import_logs()` 与 Contents API 路径 `github_sync.py:exchange()` 均走 `Store.import_events()`。
- 复用普通行的合并规则。不同 name 全保留，同义异名可由助教以后读到时合并。相同 name 由 `Journal.record()/apply()` 按事件 UUID 去重，用 `(timestamp, event_id)` 较大者替换整行，同一微秒比较 ID 字典序。`as_of` 和推送顺序不参与。删除也是普通行更新（`removed=false`），已有的硬删除只接受聊天消息。比删除旧的更新晚到也无效。离线改写若事件较新，会重新显现。
- 旧客户端能继续用原功能读本机库，会忽略额外的表。若收到新表的事件，旧 `Journal.apply()` 遇到未知类型抛出 ValueError，当前 `Store.import_events()` 导入事务回滚，`ProgressSync.sync()` 报同步失败。同步各端应先升级再产生记忆事件，升级后重试原日志即可。
- **开关**　「允许助教记忆」默认开（`settings` 的 `memory_enabled` 缺省按 1 读），随设置同步。关闭会停用记忆上下文、附加题选例参考和后台回顾，已存笔记保留。切换或清空时，本机游标移至日志末尾。聊天与回顾写回时核对开关、设置事件 ID 和本机清空次数。清空次数与游标同存于本机 `sync_meta`。在途时即使关了又开、一次同步合入两次切换，或对空库执行清空，旧调用的记忆操作也会作废，旧回顾不能倒退游标。
- **清空**　在一个事务把本机已知有效行逐条标为删除，开关维持原值。另一台尚未同步的独有条目以后仍会合入，学生可在同步后再次清空。已发给订阅的内容、既有聊天、本机事件及私有仓库历史仍可能留有旧文。设置确认文案为「清空本机现有的笔记？删除会同步，离线新增或更新的笔记可能再次出现。历史记录会保留。」继续开启时只凭新证据再记。
- **入口**　浏览器和各系统的桌面版共用网页设置，随网页更新包交付。「今日计划」的每日上限旁有「允许助教记忆」和「清空记忆」，清空前需确认。做题页的命令面板可开启或关闭助教记忆。开关读写使用 `GET/PUT /api/memory/settings`，清空使用 `POST /api/memory/clear`。

## 实现与验收

后端测试用临时 SQLite 库与 `FakeProvider`。同步测试用两份独立的 Store。

| 功能 | 实现 | 验收 |
|---|---|---|
| 存储与同步 | `db.py` 和 `events.py` 管理笔记、设置和逐行删除标记。 | `test_memory.py`、`test_sync.py` 覆盖升级、合并、离线写入、重放和旧客户端导入。 |
| 聊天 | `ai/memory.py` 和 `ai/tutor.py` 组装上下文，`main.chat_send()` 保存最终回复。 | `test_tutor.py`、`test_ai_agents.py` 检查两种助教格式、跨题偏好、索引、正文和重试。 |
| 设置入口 | 网页与桌面共用「今日计划」的开关和清空操作，做题页命令面板也可切换。 | 在一个入口切换后，到另一入口核对开关。清空后在新对话中盘点。 |
| 后台学习回顾 | `db.py` 领取和提交批次，`main.py` 启动线程，`ai/memory.py` 整理证据。 | `test_memory.py` 检查触发、帮助记录、跨日积压、空结果、失败重启、事务回滚与并发冲突。 |
| 教学使用 | `main.run_extra_job()` 与 `ai/extra.py` 在自主练习的出题要求旁提供匹配正文。 | `test_extras.py`、`test_review_api.py` 检查目标技能、复习变式、掌握度及日程。 |
