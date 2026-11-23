## 题目

每笔报价记录 shop、shift、price。先把每笔 price 打八折，再加 2 元包装费。用整列算术处理价格。返回每店一行的会员均价表，列为 shop、am、pm。两种班次都会出现，店内某班无报价时填 0。用整列运算完成，不能写循环或推导式。

`t` 已经是 DataFrame。

## 示例 1

`t`

| shop | shift | price |
| --- | --- | --- |
| North | am | 10 |
| North | pm | 0 |

返回

| shop | am | pm |
| --- | --- | --- |
| North | 10.0 | 2.0 |

## 示例 2

`t`

| shop | shift | price |
| --- | --- | --- |
| South | am | 3 |
| North | pm | 4 |

返回

| shop | am | pm |
| --- | --- | --- |
| North | 0 | 5.2 |
| South | 4.4 | 0 |

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。
