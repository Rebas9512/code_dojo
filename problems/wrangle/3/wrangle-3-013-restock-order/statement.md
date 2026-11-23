## 题目

text 是带表头 id,stock 的 CSV 文本。读成表并保留有库存的行，先按 stock 升序，同库存按 id 升序。返回 id、stock 两列。

## 示例 1

`text`

```text
id,stock
3,4
1,0
2,4
```

返回

| id | stock |
| --- | --- |
| 2 | 4 |
| 3 | 4 |

## 示例 2

`text`

```text
id,stock
1,0
```

返回

| id | stock |
| --- | --- |

（空表）

按示例的列名和列顺序返回。行的排列顺序也要一致。行索引可自选。
