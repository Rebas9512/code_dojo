## 题目

每本书有售价 price 和库存 stock。返回 title、stock_value，其中 stock_value 是按当前价格计算的该书在库金额。

`books` 已经是 DataFrame。

## 示例 1

`books`

| title | price | stock |
| --- | --- | --- |
| The Silent Harbor | 42.0 | 12 |
| Stars Over Gobi | 39.0 | 5 |
| Python in Practice | 68.0 | 20 |

返回

| title | stock_value |
| --- | --- |
| The Silent Harbor | 504.0 |
| Stars Over Gobi | 195.0 |
| Python in Practice | 1360.0 |

## 示例 2

`books`

| title | price | stock |
| --- | --- | --- |
| The Last Lantern | 39.0 | 0 |
| Little Cloud | 18.5 | 30 |
| Noodles at Midnight | 29.9 | 15 |

返回

| title | stock_value |
| --- | --- |
| The Last Lantern | 0.0 |
| Little Cloud | 555.0 |
| Noodles at Midnight | 448.5 |

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。

同一道书店查询的 SQL 练习为 [sql-0-002-stock-value](/p/sql-0-002-stock-value)。
