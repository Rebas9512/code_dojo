## 题目

将 daily 中的积分变动合入 purse。每键一行，已有会员是余额加变动，新会员以变动作为初始余额，允许负变动。

## 示例

旧值 8 遇到 -3 应变成 5。

样例库已执行下面的语句。

```sql
CREATE TABLE purse (id int PRIMARY KEY,n int); INSERT INTO purse VALUES (4,8),(8,3);
CREATE TABLE daily (id int,n int); INSERT INTO daily VALUES (4,-3),(9,6);
```

## 约束

沿用题目给定的英文表名和列名。
