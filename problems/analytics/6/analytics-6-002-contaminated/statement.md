## 题目

只分析 cover 实验，同组多条视为同一人，同时进 A、B 的读者完全剔除。只输出被剔除的跨组读者编号，按编号升序。

## 用到的表

assignments(assignment_id, experiment, user_id, arm, assigned_at) 每次分组一行。组别为 A 或 B，可能重复上报或跨组。

## 示例结果

| user_id |
|---|
| 13 |
| 26 |

13 号和 26 号各自有两种不同的 cover 分组。

样例共 2 行。按示例列顺序输出，行按题意排序。
