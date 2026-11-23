## 题目

只分析 cover 实验，同组多条视为同一人，同时进 A、B 的读者完全剔除。按组别升序输出有合格读者的组别及去重人数。

## 用到的表

assignments(assignment_id, experiment, user_id, arm, assigned_at) 每次分组一行。组别为 A 或 B，可能重复上报或跨组。

## 示例结果

| arm | readers_n |
|---|---|
| A | 17 |
| B | 17 |

剔除两个跨组编号后，共余 34 人，两组各 17。

样例共 2 行。按示例列顺序输出，行按题意排序。
