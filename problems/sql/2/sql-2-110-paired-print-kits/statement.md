## 题目

找出至少三家不同工坊都使用的工具对，输出字母较小的 first_kit、较大的 second_kit、工坊数 shops。重复领用不增加工坊数。

## 样例输入

`kit_uses`

| shop | kit |
|---|---|
| 1 | Arc |
| 1 | Pen |
| 1 | Pen |
| 2 | Arc |
| 2 | Pen |
| 3 | Arc |
| 3 | Pen |
| 3 | Wax |

## 样例结果

| first_kit | second_kit | shops |
|---|---|---|
| Arc | Pen | 3 |

Arc 与 Pen 虽然在 1 号工坊配出两行，仍只算一家。

按上表的列顺序输出。先按 shops 降序，再按两项工具名依次升序。
