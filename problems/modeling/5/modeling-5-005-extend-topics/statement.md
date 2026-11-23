## 题目

links 已经按 (book_id,topic_id) 唯一。raw 是本轮扫描，把缺少的关联追加到 links，保留原有关联。

## 示例

图书 7 已有主题 1，补充主题 2 后应同时保有它们。

样例库已执行下面的语句。

```sql
CREATE TABLE topics (id int PRIMARY KEY); INSERT INTO topics VALUES (1),(2);
CREATE TABLE books (id int PRIMARY KEY); INSERT INTO books VALUES (7),(9);
CREATE TABLE raw (book_id int,topic_id int); INSERT INTO raw VALUES (7,1),(7,2),(9,1),(7,1);
CREATE TABLE links (book_id int,topic_id int,PRIMARY KEY(book_id,topic_id)); INSERT INTO links VALUES (7,1);
```

## 约束

沿用题目给定的英文表名和列名。
