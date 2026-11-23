## 题目

返回一行一列，计算 readings.v 为空的行数除以全部行数，以 0 到 1 的小数表示。空表按 0 计算。

## 示例

样例一行空、三行非空，答案是 0.25。

```sql
CREATE TABLE readings (v int); INSERT INTO readings VALUES (0),(2),(6),(NULL);
```

## 约束

列依题面顺序，结果行可按任意顺序。
