## 题目

t 的 shelf 是货架名，n 是现有册数。指定货架的每一行册数翻倍，其他货架保持原值，按更新后的 n 从小到大排列，同册数按 shelf 升序。

`t` 已经是 DataFrame。

## 示例 1

`t`

| shelf | n |
| --- | --- |
| Oak | 2 |
| Maple | 4 |

`shelf`

`'Oak'`

返回

| shelf | n |
| --- | --- |
| Maple | 4 |
| Oak | 4 |

## 示例 2

`t`

| shelf | n |
| --- | --- |
| Elm | 0 |

`shelf`

`'Oak'`

返回

| shelf | n |
| --- | --- |
| Elm | 0 |

按示例的列名和列顺序返回。行的排列顺序也要一致。行索引可自选。
