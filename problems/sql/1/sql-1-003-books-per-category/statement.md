## 题目

同事需要一份书架标签清单。每个实际出现的分类写一行，依次列出分类和该类的书目数。每个编号算一种书，库存为零也算。

把编辑器里的 `____` 换成缺少的 SQL。

## 用到的表

`books` 每行一种书。`book_id` 是编号，`category` 是分类，`price` 是单价（元），`stock` 是库存册数。

## 示例结果

| category | book_count |
|---|---|
| cooking | 4 |
| fantasy | 3 |
| fiction | 6 |
| history | 4 |
| kids | 3 |
| programming | 5 |
| scifi | 5 |

样例共 7 行。

kids 有三种书。即便其中一种有几十册库存，它在书目里也只占一行。

按上表的列顺序输出。行的顺序不限。
