## 题目

模拟清理重复邮箱后的通讯录。每个邮箱保留编号最小的一条，提交 SELECT，返回留下的编号与邮箱。

## 用到的表

address_book 每条记录有唯一编号，邮箱非空，按原文相等判断重复。

## 样例数据

**address_book**

| id | email |
|---|---|
| 9 | he@desk.cn |
| 2 | he@desk.cn |
| 4 | yu@desk.cn |
| 7 | he@desk.cn |

## 示例结果

| id | email |
|---|---|
| 2 | he@desk.cn |
| 4 | yu@desk.cn |

样例共 2 行。

he@desk.cn 对应 2、7、9。清理后只留下 2；另一邮箱的 4 也留下。

按上表的列顺序输出。行的顺序不限。
