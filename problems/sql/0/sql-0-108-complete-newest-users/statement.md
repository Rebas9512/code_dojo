## 题目

列出所有用户的姓名和注册日期，**最新**注册的排在最前面；同一天注册的，`user_id` 小的在前。补全 ORDER BY 后面的部分。

用到的表（书店练习数据库）：

**users**（用户）

| 列 | 类型 | 说明 |
|---|---|---|
| user_id | integer | 主键 |
| name | text | 姓名；可能重名 |
| email | text | 邮箱 |
| phone | text | 手机号，可能为空 |
| city | text | 城市，可能为空 |
| signup_date | date | 注册日期 |
| referrer_id | integer | 推荐人的 user_id，可能为空 |

## 示例

在书店样例数据上，正确结果是：

| name | signup_date |
|---|---|
| Kevin Zhou | 2025-06-30 |
| Lin Xi | 2025-06-15 |
| He Jun | 2025-06-06 |
| Olivia Chen | 2025-05-20 |
| Ma Chao | 2025-05-01 |
| Gao Yan | 2025-04-18 |
| Noah Wilson | 2025-04-02 |
| Xu Ming | 2025-03-30 |

（共 20 行，这里只列出前 8 行。）

## 约束

- 结果两列：`name`、`signup_date`。
- 结果要按题目要求的顺序排列。
- 列名不检查，但列的个数和顺序要和要求一致。
- 提交后还会在几份隐藏数据上运行（比如多了并列、空值、边界值），只对样例凑出结果是不够的。
