## 题目

用一条 UPDATE 同时对调 print_faces 中所有 recto 与 verso。保留原版号 plate。提交后核对整张表。

## 样例输入

`print_faces`

| plate | face |
|---|---|
| 11 | recto |
| 12 | verso |
| 13 | recto |

## 修改后的表

| plate | face |
|---|---|
| 11 | verso |
| 12 | recto |
| 13 | verso |

11 和 12 原先方向相反，更新后仍相反。
