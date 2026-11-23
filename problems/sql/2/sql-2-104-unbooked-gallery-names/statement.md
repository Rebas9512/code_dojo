## 题目

每行挂展单代表一件作品曾经挂在某个展厅，title 是可空的作品标题。输出没有挂展单的展厅名字 name。

## 样例输入

`gallery_list`

| gallery | name |
|---|---|
| 4 | Fern |
| 8 | Yew |
| 12 | Oak |

`hang_log`

| slip | gallery | title |
|---|---|---|
| 91 | 4 | NULL |
| 92 | 12 | Tide |
| 93 | 4 | Rain |

## 样例结果

| name |
|---|
| Yew |

Yew 在场馆名册上，所有挂展单却都指向其他展厅。

按上表的列顺序输出。行序不限。
