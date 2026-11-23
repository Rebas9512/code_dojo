# 27 · 润色：题干用中文，作答用英文

## 背景

用户 2026-11-22 指着"认识数据"的一道题说：

> "话说我还准备润色一下题目，比如这种题 题干可以用中文 但是答题的时候尽量保持全英文你可以派一路去把题目检查一下"

那道题是 `data-0-*`「给一条记录里的值归类」，现在要求学习者打"整数 文字 文字"。

**主控定的规则**，写进 `docs/problem-format.md`，作为题目约定：

- **用中文**：题干、讲解、提示、explain、知识卡、课的讲解。
- **用英文**：凡是学习者要**打出来**、或者程序要**输出**来比对的内容。具体包括：
  - 看数据作答（inspect）的短答案。
    - 类型名用通用英文，并且多收同义写法。比如：整数 → `integer`（也收 `int`）；小数 → `decimal`（也收 `float`、`number`）；文字 → `text`（也收 `string`、`str`）；真假 → `boolean`（也收 `bool`）；空 → `missing`（也收 `null`、`none`、`empty`、`NA`）。
    - 列名本来就是英文。
  - 单选题的选项：选项本身是值、类型名、输出或代码的，改成英文；选项是一句解释的，保留中文。
  - 预测题（predict）程序打印的文字：程序里的中文字符串改成英文，比如 `print("你好")` 改成 `print("hello")`。
  - 函数题、stdio 题的输入输出里的文字：比如返回 `"及格"` 改成 `"pass"`。题干里同步写清楚要求的英文输出。
  - SQL：学习者要写进查询的字符串字面量，以及参考解输出的文字值，比如 `CASE … THEN '高'` 改成 `'high'`。
  - 数据集里需要学习者在查询里引用的文字值也改成英文；只出现在结果里、不用打的，可以保留。
  - 课里的示例代码和小测：照同样的规则。示例里打印的文字用英文，注释和讲解用中文。
- **数字、标点、格式要求**照旧，比如保留两位小数、逗号分隔。英文大小写要在题干里写清楚，或者用不区分大小写的比较。

## 范围

主控扫描过，下面这些题的答案、输出、测试或参考解里有中文：
- data：20 道里 19 道
- python：238 道里 47 道
- algo：12 道
- wrangle：14 道
- sql：2 道

math、tensor、ml 是干净的。train 由 21 号任务在写，llm 由 22 号任务写，它们会直接按新规则来，这次不碰。

先写一个扫描脚本，脚本放 `{RUN_DIR}/`，找出全部需要改的地方，范围比主控扫的更全：
- `problem.yaml` 的 answer / options / misconceptions
- `tests.json`
- `solution.*` 和 `starter.*` 里的字符串字面量（注释不算）
- 预测题实际运行的输出
- 数据集文件
- 课文件里的 example 代码输出和 quiz 选项

**并行**：21（训练线内容）和 26（平台：打包桌面应用）在同时跑，先读 `codex/PLAN.md`。

你名下的东西：
- `problems/data|python|algo|wrangle|sql/` 下需要改的题目和课；
- `docs/problem-format.md` 里加的这条约定，用小补丁；
- `docs/teaching-design.md`：如果误解的说明里引用了中文答案，同步改；
- `server/app/ai/` 里附加题出题的提示词：只加一条规则，"题干用中文，学习者要输入或输出的内容用英文"，用小补丁。

不要动 `problems/train/`、`problems/llm/`，也不要动平台的其他文件。

## 要做的事

1. **扫描**，出一份清单写进报告：题号、哪个文件、原文 → 改成什么。
2. **逐题修改**，同步改：
   - `tests.json`
   - `solution`、`starter`
   - `wrong_examples`
   - inspect 的 `answer.accept` 和 `misconceptions`：错误答案的映射也换成英文写法，并保留常见的错误英文写法，比如把 `"7"` 也当作 integer 的误答
   - 题干里提到具体输出的地方
   - 课
3. **改完的题照样要通过全部校验**：
   - 参考解 accepted；
   - `wrong_examples` 仍然判错；
   - 改错题的 starter 仍然能在样例上看出 bug；
   - inspect 题答案自洽。
4. **扫描脚本最后再跑一遍**，确认范围内已经没有"要打出来的中文"。如果有刻意保留的，比如题目本身讲的就是中文字符的编码，`ord("中")` 这种，就在报告里逐条列出理由。
5. **规则写进约定**：
   - `docs/problem-format.md` 加一节"题目语言约定"；
   - `codex/brief.md` 的"跟着现有代码走"一条里加一句。这个文件主控允许你改这一处。

## 验收标准

1. 全部通过：
   - `cd server && .venv/bin/python ../scripts/verify_bank.py --jobs 4`，全题库，加载错误 0；
   - `python3 scripts/curriculum/verify_sql.py -q`；
   - `server/.venv/bin/python scripts/curriculum/verify_python.py -q`。
2. `check_curve.py`：0 错 0 警。
3. `server/.venv/bin/python -m pytest -q` 全过。附加题提示词改了，FakeProvider 的测试要照旧能过。
4. 起测试实例，打开截图里那道题（`data-0-*`「给一条记录里的值归类」）：
   - 用英文 `integer text text` 答对；
   - 用 `int str str` 也对；
   - 用 `7` 这类错误答案时，显示对应的误解。

   截图放 `{RUN_DIR}/`。
5. 报告里列出：每条线改了几道题、改了几个课、刻意保留中文的清单。
