## 题目

返回最贵的三本书的 book_id、title、price，少于三本就全部返回。价格降序，相同价格以较小书号优先。

`books` 已经是 DataFrame。

## 示例 1

`books`

| book_id | title | price |
| --- | --- | --- |
| 2 | Stars Over Gobi | 39.0 |
| 5 | The Last Lantern | 39.0 |
| 8 | Quantum Garden | 45.0 |
| 22 | Orbit of Ashes | 39.0 |

返回

| book_id | title | price |
| --- | --- | --- |
| 8 | Quantum Garden | 45.0 |
| 2 | Stars Over Gobi | 39.0 |
| 5 | The Last Lantern | 39.0 |

## 示例 2

`books`

| book_id | title | price |
| --- | --- | --- |
| 1 | The Silent Harbor | 42.0 |
| 2 | Stars Over Gobi | 39.0 |

返回

| book_id | title | price |
| --- | --- | --- |
| 1 | The Silent Harbor | 42.0 |
| 2 | Stars Over Gobi | 39.0 |

按示例的列名和列顺序返回。行的排列顺序也要一致。行索引可自选。

同一道书店查询的 SQL 练习为 [sql-0-015-top3-expensive](/p/sql-0-015-top3-expensive)。
