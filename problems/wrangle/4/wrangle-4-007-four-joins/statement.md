## 题目

books 给 id、name，lots 给 id、n。按 id 合并，how 由调用方传入：inner 只留匹配，left 保留全部左行，right 保留全部右行，outer 两边都留。每一个匹配组合都要返回。

`books`、`lots` 已经是 DataFrame。

## 示例 1

`books`

| id | name |
| --- | --- |
| 1 | 甲 |
| 2 | 乙 |

`lots`

| id | n |
| --- | --- |
| 1 | 2 |
| 1 | 3 |
| 3 | 4 |

`how`

`'outer'`

返回

| id | name | n |
| --- | --- | --- |
| 1 | 甲 | 2 |
| 1 | 甲 | 3 |
| 2 | 乙 | 缺失 |
| 3 | 缺失 | 4 |

## 示例 2

`books`

| id | name |
| --- | --- |
| 2 | 乙 |

`lots`

| id | n |
| --- | --- |
| 4 | 8 |

`how`

`'right'`

返回

| id | name | n |
| --- | --- | --- |
| 4 | 缺失 | 8 |

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。
