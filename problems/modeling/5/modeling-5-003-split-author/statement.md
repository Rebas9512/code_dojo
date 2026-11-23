## 题目

把 raw 拆为 authors(id 整数主键,name 文字) 与 notes(id 整数主键,author_id 整数外键指向 authors.id)。按所列顺序建列、载入全部原始记录。作者键决定名称。

## 示例

作者 1 有两篇笔记，作者表只有一行 Ivy，笔记表保留两个不同笔记编号。

样例库已执行下面的语句。

```sql
CREATE TABLE raw (note_id int PRIMARY KEY, author_id int, name text);
INSERT INTO raw VALUES (10,1,'Ivy'),(11,1,'Ivy'),(12,2,'Sam');
```

## 约束

沿用题目给定的英文表名和列名。
