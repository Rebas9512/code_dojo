## 题目

feed 中同一 id 的 rev 不重复。每键只取本批最大 rev 的整行，再覆盖或插入 catalog。本题保证本批胜者比该键的旧版本更新。

## 示例

1 应保留 rev=3 的 gold，不能让随后出现的 rev=1 覆盖它。

样例库已执行下面的语句。

```sql
CREATE TABLE catalog (id int PRIMARY KEY,rev int,tag text); INSERT INTO catalog VALUES (3,4,'keep');
CREATE TABLE feed (id int,rev int,tag text); INSERT INTO feed VALUES (1,3,'gold'),(1,1,'base'),(2,1,'plus');
```

## 约束

沿用题目给定的英文表名和列名。
