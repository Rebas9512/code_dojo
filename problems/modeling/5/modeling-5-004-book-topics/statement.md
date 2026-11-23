## 题目

按 book_id、topic_id 的顺序建 links，两列均为整数。分别引用 books.id、topics.id，并按该顺序组成主键。将 raw 的每组关联只载入一次。

## 示例

图书 7 属于两个主题，应有两行关联。重复扫描 (7,1) 只留一次。

样例库已执行下面的语句。

```sql
CREATE TABLE topics (id int PRIMARY KEY); INSERT INTO topics VALUES (1),(2);
CREATE TABLE books (id int PRIMARY KEY); INSERT INTO books VALUES (7),(9);
CREATE TABLE raw (book_id int,topic_id int); INSERT INTO raw VALUES (7,1),(7,2),(9,1),(7,1);
```

## 约束

沿用题目给定的英文表名和列名。
