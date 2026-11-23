## 题目

已有 depots。新建 handoffs，依次放 id 整数主键、depot_id 必填整数外键，引用 depots.id。不同交接可以指向同一个仓库。

## 示例

4 号仓库已登记，交接可以引用它；999 号不存在。

样例库已执行下面的语句。

```sql
CREATE TABLE depots (id int PRIMARY KEY);
INSERT INTO depots VALUES (4),(8);
```

## 约束

沿用题目给定的英文表名和列名。
