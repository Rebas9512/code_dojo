## 题目

给已有 packs.qty 设默认值 6，保留原来登记的数量。再只填 code 写入一行 blue。

## 示例

red 仍是 4，blue 自动得到 6。

样例库已执行下面的语句。

```sql
CREATE TABLE packs (code text, qty integer);
INSERT INTO packs VALUES ('red',4);
```

## 约束

沿用题目给定的英文表名和列名。
