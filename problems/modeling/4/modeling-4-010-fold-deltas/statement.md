## 题目

entries 的每行都是独立变动，同一会员可能有多笔。先按会员汇总，再累计到 purse。新会员从零开始。

## 示例

会员 1 的两笔是 +3 和 -1，旧余额 8 应变为 10。

样例库已执行下面的语句。

```sql
CREATE TABLE purse (id int PRIMARY KEY,n int); INSERT INTO purse VALUES (1,8);
CREATE TABLE entries (id int,n int); INSERT INTO entries VALUES (1,3),(1,-1),(2,6);
```

## 约束

沿用题目给定的英文表名和列名。
