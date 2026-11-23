## 思路

MySQL 原稿想给每个箱子做一串标签。PostgreSQL 用 `STRING_AGG`，在函数内保留去重、斜杠分隔和按标签排序三项要求。

## 写法要点

- 分隔符是第二个参数，决定拼接次序的 `ORDER BY label` 紧跟其后。漏掉 `DISTINCT` 会让同箱的重名标签出现两次。
