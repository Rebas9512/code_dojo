## 题目

在已有 crates 末尾新增 capacity 整数列，必填且默认 12。保留所有原记录，以后只登记箱号也应成功。

## 示例

样例两个箱子都应读到容量 12。

样例库已执行下面的语句。

```sql
CREATE TABLE crates (code text);
INSERT INTO crates VALUES ('A'),('B');
```

## 约束

沿用题目给定的英文表名和列名。
