## 题目

返回 ratings 中 score 小于 1 或大于 5 的 id 和 score。空值由另一条规则处理，此处排除。

## 示例

0 和 6 越界，1 和 5 都合法。

```sql
CREATE TABLE ratings (id int,score int); INSERT INTO ratings VALUES (1,0),(2,1),(3,5),(4,6),(5,NULL);
```

## 约束

列依题面顺序，结果行可按任意顺序。
