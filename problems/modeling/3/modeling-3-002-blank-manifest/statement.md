## 题目

将两张新单据 pack、ship 加入 docs，份数全部采用该库当前的默认值。不要改原有记录。

## 示例

样例默认 2 份。另一个站点可有不同默认份数。

样例库已执行下面的语句。

```sql
CREATE TABLE docs (title text,copies int DEFAULT 2);
INSERT INTO docs VALUES ('old',7);
```

## 约束

沿用题目给定的英文表名和列名。
