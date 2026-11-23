## 题目

保留已有 labels，追加 A、B、C 三组标签，份数依次为 2、4、1。

## 示例

样例原有的 hold 标签仍然有 6 份。

样例库已执行下面的语句。

```sql
CREATE TABLE labels (code text, copies int DEFAULT 1);
INSERT INTO labels VALUES ('hold',6);
```

## 约束

沿用题目给定的英文表名和列名。
