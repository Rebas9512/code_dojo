## 题目

按月划季：12、1、2 月为 winter，3–5 为 spring，6–8 为 summer，其余为 fall。每季取总包数最高的纸种，平手取总收入高者，收入未知时排在已知收入之后，仍平手取纸种名字母较小者。收入按各笔已知价格乘包数加总；全部价格未知时收入未知。输出 season、paper、packs、revenue。

## 样例输入

`paper_sales`

| month | paper | packs | price |
|---|---|---|---|
| 12 | Ash | 2 | 8 |
| 1 | Ash | 3 | 8 |
| 2 | Elm | 5 | 9 |
| 3 | Oak | 4 | 2 |
| 4 | Yew | 4 | 2 |
| 7 | Fir | 1 | 5 |

## 样例结果

| season | paper | packs | revenue |
|---|---|---|---|
| spring | Oak | 4 | 8 |
| summer | Fir | 1 | 5 |
| winter | Elm | 5 | 45 |

冬季 Ash 和 Elm 同为 5 包，Elm 的收入 45 更高；春季 Oak 与 Yew 比到名字。

按上表的列顺序输出。按 season 的字母升序。
