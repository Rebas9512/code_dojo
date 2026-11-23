## 题目

对每个在 cutoff 出现的站点，从 batches 删除 day 严格早于该站 cutoff.day 的行。边界当天和没有期限的站点全部保留。

## 示例

east 的 1 月 1 日过期，1 月 2 日仍有效。

样例库已执行下面的语句。

```sql
CREATE TABLE batches (site text,day date); INSERT INTO batches VALUES ('east','2025-01-01'),('east','2025-01-02'),('west','2025-01-01');
CREATE TABLE cutoff (site text PRIMARY KEY,day date); INSERT INTO cutoff VALUES ('east','2025-01-02');
```

## 约束

沿用题目给定的英文表名和列名。
