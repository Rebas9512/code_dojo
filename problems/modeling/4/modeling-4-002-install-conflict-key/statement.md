## 题目

codes 当前没有唯一约束，已有数据互不重复。给 code 加唯一约束，再把 incoming 的新代码插入，重复请求保留一条。

## 示例

样例 A 重复到达，目标应只有 A、B 各一行。

样例库已执行下面的语句。

```sql
CREATE TABLE codes (code text NOT NULL); INSERT INTO codes VALUES ('A');
CREATE TABLE incoming (code text); INSERT INTO incoming VALUES ('A'),('B'),('B');
```

## 约束

沿用题目给定的英文表名和列名。
