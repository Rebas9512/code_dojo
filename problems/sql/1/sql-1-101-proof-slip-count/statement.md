## 题目

校样单一行一张，note 是可空的批注。返回校样单总张数 slip_count。

## 样例输入

`proof_slips`

| slip | imprint | note |
|---|---|---|
| 1 | Ash | ink |
| 2 | Ash | NULL |
| 3 | Elm | ink |
| 4 | Ash | ink |

## 样例结果

| slip_count |
|---|
| 4 |

第 2 张的批注为空，它也要占一张。

按上表的列顺序输出。行序不限。
