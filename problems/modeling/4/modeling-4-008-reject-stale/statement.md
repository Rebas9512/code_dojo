## 题目

先取 feed 每键最大 rev 的整行（同键版本不重复）。新键插入，已有键仅在批次胜者版本严格更高时覆盖，相同版本也保留原值。

## 示例

目标中 3 已经是 rev=4，本批 rev=2 即使写着 late 也不能覆盖它。

样例库已执行下面的语句。

```sql
CREATE TABLE catalog (id int PRIMARY KEY,rev int,tag text); INSERT INTO catalog VALUES (3,4,'keep');
CREATE TABLE feed (id int,rev int,tag text); INSERT INTO feed VALUES (1,3,'gold'),(1,1,'base'),(2,1,'plus'); INSERT INTO feed VALUES (3,2,'late');
```

## 约束

沿用题目给定的英文表名和列名。
