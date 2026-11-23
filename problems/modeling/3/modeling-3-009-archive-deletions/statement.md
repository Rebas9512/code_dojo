## 题目

按 cancelled 清理 queue，将实际删除的完整行追加到 archive。清单上找不到的编号不能形成档案。

## 示例

样例待办 2 被移走，档案中多出 (2,tag)。

样例库已执行下面的语句。

```sql
CREATE TABLE queue (id int, task text); INSERT INTO queue VALUES (1,'box'),(2,'tag'),(3,'load');
CREATE TABLE cancelled (id int); INSERT INTO cancelled VALUES (2);
CREATE TABLE archive (id int,task text);
```

## 约束

沿用题目给定的英文表名和列名。
