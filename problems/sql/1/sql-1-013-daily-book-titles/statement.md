## 题目

发货台要一份按日归档的书名清单。输出销售日期，以及当天所有不同书名按字母升序、用英文逗号紧挨着拼成的文字；同名不同版合为一个名字。

把编辑器里的 `____` 换成缺少的 SQL。

## 用到的表

书店随题提供 `sold_titles(sold_on, title)`。每行是一笔未取消订单中的一种书，已经带上订单日期和英文书名。

## 示例结果

| sold_on | titles |
|---|---|
| 2024-12-02 | Data at Dawn,Python in Practice |
| 2024-12-15 | Little Cloud,Moon Rabbit |
| 2024-12-31 | SQL for Curious Minds |
| 2025-01-01 | Rainy Season,The Map Maker,The Silent Harbor |
| 2025-01-09 | Quantum Garden,Stars Over Gobi |
| 2025-01-20 | Algorithms, Gently,Bread & Butter,Noodles at Midnight,Spice Atlas |
| 2025-02-01 | The Last Lantern |
| 2025-02-14 | The Glass Fox |

样例共 28 行。这里只列出其中 8 行。

2024 年 12 月 2 日卖了两种不同书名。拼接后 Data at Dawn 在 Python in Practice 前面。

按上表的列顺序输出。行的顺序不限。
