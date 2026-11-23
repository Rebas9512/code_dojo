## 题目

每行有 shop、note、jan、feb。仅将一月和二月的数量展开，保留店名，不输出备注。同店可能有多份账目，按店与月合计，结果列为 shop、month、qty。

`t` 已经是 DataFrame。

## 示例 1

`t`

| shop | note | jan | feb |
| --- | --- | --- | --- |
| A | 已核 | 2 | 3 |
| B | 已核 | 0 | 4 |

返回

| shop | month | qty |
| --- | --- | --- |
| A | jan | 2 |
| A | feb | 3 |
| B | jan | 0 |
| B | feb | 4 |

## 示例 2

`t`

| shop | note | jan | feb |
| --- | --- | --- | --- |
| C | 已核 | 1 | 1 |

返回

| shop | month | qty |
| --- | --- | --- |
| C | jan | 1 |
| C | feb | 1 |

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。
