## 题目

供货商的文本用分号分隔两列 shelf 和 stock，字段可能用双引号包住。从中取出名为 stock 的 Series，按文件顺序保留各行。

## 示例 1

`text`

```text
shelf;stock
A;3
B;0
```

返回

| stock |
| --- |
| 3 |
| 0 |

## 示例 2

`text`

```text
shelf;stock
"North;East";5
```

返回

| stock |
| --- |
| 5 |

返回 Series，保留题目要求的名称。行的排列顺序也要一致。保留示例所示的索引规则。
