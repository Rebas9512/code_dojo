## 题目

将 inbox 全部尝试写入 members，按 id 判重。老会员保留原标签，新会员从消息取标签。

## 示例

1 保留 old，2 新增 first。

样例库已执行下面的语句。

```sql
CREATE TABLE members (id int PRIMARY KEY,tag text); INSERT INTO members VALUES (1,'old'),(3,'stay');
CREATE TABLE inbox (id int,tag text); INSERT INTO inbox VALUES (1,'changed'),(2,'first');
```

## 约束

沿用题目给定的英文表名和列名。
