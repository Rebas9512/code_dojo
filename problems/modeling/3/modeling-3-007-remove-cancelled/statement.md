## 题目

从 queue 中删除编号出现在 cancelled 的待办，保留撤销清单。

## 示例

样例最终还有 1 和 3 两条待办。

样例库已执行下面的语句。

```sql
CREATE TABLE queue (id int, task text); INSERT INTO queue VALUES (1,'box'),(2,'tag'),(3,'load');
CREATE TABLE cancelled (id int); INSERT INTO cancelled VALUES (2);
```

## 约束

沿用题目给定的英文表名和列名。
