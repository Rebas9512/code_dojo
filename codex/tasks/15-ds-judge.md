# 15 · M6 平台：数据科学判题镜像，以及对拍 / 梯度检查 / 写法约束 / 模拟训练这几种判法

## 背景

用户 2026-11-22 的原话：
- "数据科学类的 数据操作，模型训练，tensor操作，手搓大语言模型之类的"
- "像这种模型训练的内容可以只做训练脚本的检查或者模拟训练 不一定需要真的把模型训练出来"

设计在 `docs/README.md` 的 2b 节，「训练类题不真训练，怎么判」那几条。先读，里面有实测数据：镜像 1.63 GB，2 层 GPT 训 100 步 0.9 秒，峰值 393 MB，同种子 loss 完全一致。

进阶 6 条线的 `track.yaml` 已经有了：
- `math` 的 runtime 是 `python`。
- `wrangle`（数据处理）、`tensor`、`ml`、`train`、`llm` 的 runtime 是 `ds`，目前都是 planned。

这次只做**平台**：判题镜像、判法、题目格式、夹具题。内容由之后的任务按线写。

**并行**：先读 `codex/PLAN.md`。平台任务 13（单用户登录、部署文档）在同时跑。

13 名下的东西，你不要碰：
- 登录相关的代码（`server/app` 里的 auth、中间件、`main.py` 的路由保护）
- `web/` 里的登录页和导航
- `deploy/`
- `docs/README.md` 第 7 节

你的改动集中在这些地方：
- `judge/`
- `server/app/judge.py`
- 题目格式和加载
- 检查脚本
- 夹具和测试

`main.py` 只在"按 runtime 选镜像"必须改的地方，用小补丁改。

`docs/README.md` 你只改 2b 节、「怎么跑」里加镜像那一行、第 8 节 M6 那一行。

另外，12（算法阶段 3）和 17（数学线）这两个内容任务也在跑。

## 要做的事

### 1. 判题镜像 `judge/ds/`

- 从 `python:3.14-slim` 起，装 numpy、pandas、CPU 版 torch（`--index-url https://download.pytorch.org/whl/cpu`），版本锁定。
- 环境变量：`OMP_NUM_THREADS=1`、`MKL_NUM_THREADS=1`。
- 复用 `judge/python/harness.py`。最好是同一份 harness 加上数据科学的比较和检查能力，两个镜像都 COPY 它，避免两份分叉。
- 镜像名 `code-dojo-judge-ds:3.14`。
- 后端按题目所在线的 `runtime` 选镜像：`python` 或 `ds`。
- ds 的资源上限单独配置：内存 1g，时限默认放宽，比如每用例 10 秒。
- 课的 playground、附加题验证也按 runtime 选镜像。

### 2. 新的比较方式和检查（`docs/problem-format.md` 升版本）

- **`compare: allclose`**：数值对拍。
  - 支持 numpy 数组、torch 张量、Python 数字和嵌套列表。
  - 先比形状和 dtype 类别（整数、浮点、布尔），再按 `rtol`、`atol` 比值。容差可以在题目里写。
  - 报错要说清楚：形状不同 `(3, 4)` 对 `(4, 3)`；dtype 不同；第一处超差的位置和两边的值。
- **`compare: frame`**：pandas DataFrame 或 Series 对比。
  - 可选忽略行序、忽略索引、列名是否要求一致。
  - 数值有容差。
  - 报错显示第一处不同。
- **写法约束** `constraints`：在 problem.yaml 里声明，判题前对用户代码做 AST 检查，违反就判"写法不符"并说明原因。
  - `no_loops: true`：禁止 for、while、推导式，用于向量化题。
  - `forbid_calls: [torch.nn.functional.scaled_dot_product_attention, torch.nn.MultiheadAttention, ...]`
  - `forbid_imports: [sklearn]`
- **梯度检查**：提供给 checker 用的工具函数。
  - `numeric_grad(f, x, eps)`
  - `check_grad(user_backward, f, inputs)`

  用于"手写反向传播"类题，比较用户算的梯度和数值梯度。
- **模拟训练**：提供 checker 用的工具，放在 harness 旁边的 `dojo_train.py` 里，镜像里可以 import。
  - 固定种子运行用户的 `train(model, data, ...)` 或训练循环函数若干步，返回 loss 序列。
  - 断言：
    - loss 下降，比如最后 10 步均值低于前 10 步的一半；
    - 能把一个小批次训到 loss 接近 0；
    - 和参考实现同种子下的 loss 轨迹逐步一致，有容差。
  - 插桩：用包装过的 optimizer 和 model 记录这些情况，违反时给出中文说明，比如"第 2 步开始梯度在累加：每步要先清梯度"：
    - 每步是否调用了 `zero_grad`，以及是在 `backward` 之前；
    - 评估时 `model.training` 是否为 False；
    - 评估时是否在 `torch.no_grad()` 里；
    - 验证集有没有被用于训练：给验证集打标记，训练时被访问就记下来。
- **形状预测**：不新增题型，用现有的 predict，程序打印每步的 `.shape`。确认 predict 在 ds 镜像里能跑出期望输出即可。

### 3. 夹具题和测试

在 `server/tests/fixtures/problems/` 里加一条测试用的 ds 线：
- `track.yaml` 写 `runtime: ds`、`status: active`，id 用 `dsfix` 一类，不要和真实线重名。
- 每种判法一道夹具题：
  - NumPy 向量化：`no_loops` 加 `allclose`
  - pandas 分组：`frame`
  - 张量操作：`allclose`，故意形状错的 `wrong_examples` 能报出形状不同
  - 手写 softmax 的反向：梯度检查
  - 训练循环改错：忘了 `zero_grad` 的 starter 被模拟训练查出来，修好后通过
  - 手写注意力：`forbid_calls` 加 `allclose`
  - 形状预测：predict

测试要真的用 ds 镜像跑。镜像不存在时跳过，和现在 Python 判题测试的做法一样。

### 4. 校验脚本和文档

- `scripts/verify_bank.py` 按 runtime 选镜像。`check_curve.py` 的 AST 识别表要认识 numpy、pandas、torch 的导入，映射到技能前缀先留空表即可，内容任务再填。
- `docs/README.md`：
  - 2b 节的"怎么判"改成现在的实现。
  - 「怎么跑」加 `docker build -t code-dojo-judge-ds:3.14 judge/ds`。
  - 第 8 节 M6 写"平台已完成，内容待写"。
- `docs/problem-format.md`：写新的 compare、constraints、ds runtime、checker 工具的用法和例子。

## 验收标准

1. `docker build -t code-dojo-judge-ds:3.14 judge/ds` 成功，报告里写镜像大小。
2. `server/.venv/bin/python -m pytest -q` 全过，包括用 ds 镜像实跑的 7 道夹具题，以及每种判法的错误路径：形状错、dtype 错、写法违规、忘了 `zero_grad`、评估没切 eval。
3. 真实题库 `verify_bank.py` 照旧全过，Python 镜像的判题时间没有变慢，报告里给前后对比。
4. 每次 ds 判题的耗时，报告里写典型值：容器启动加 import torch 一次大约多少秒。
5. 用户的 8000 和 5173 实例没被动过，`server/data/` 没被改过。
