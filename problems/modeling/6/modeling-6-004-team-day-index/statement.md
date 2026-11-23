## 题目

给 visits 建普通非唯一 B-tree 索引 visits_team_day_idx，依次用 team、day 作键，均用默认升序，覆盖全部记录。

## 示例

WHERE team=2 AND day >= 某天，先定位站点，再在站内依日期定位。

样例库已执行下面的语句。

```sql
CREATE TABLE visits (id integer,team integer,day date);
INSERT INTO visits VALUES (1,2,'2025-01-01');
```

## 约束

沿用题目给定的英文表名和列名。
