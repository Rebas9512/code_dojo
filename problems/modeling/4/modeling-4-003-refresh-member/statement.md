## 题目

将 inbox 合并到 members。id 已存在就以本批 tag 覆盖旧值，不存在就新增。每批每个 id 只有一行。

## 示例

1 改成 changed，2 为 first，3 仍是 stay。

样例库已执行下面的语句。

```sql
CREATE TABLE members (id int PRIMARY KEY,tag text); INSERT INTO members VALUES (1,'old'),(3,'stay');
CREATE TABLE inbox (id int,tag text); INSERT INTO inbox VALUES (1,'changed'),(2,'first');
```

## 约束

沿用题目给定的英文表名和列名。
