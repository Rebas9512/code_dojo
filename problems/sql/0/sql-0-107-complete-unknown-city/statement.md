## 题目

查出城市没有填写（`city` 为 NULL）的用户的 `user_id` 和姓名。补全 `city` 后面的部分。

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

| user_id | name |
|---|---|
| 4 | Wang Fang |
| 10 | Emma Davis |
| 11 | Zhao Lei |
| 18 | He Jun |

（共 4 行。）

## 约束

- 结果两列：`user_id`、`name`。
- 行的顺序不要求。
- 列名不检查，但列的个数和顺序要和要求一致。
- 提交后还会在几份隐藏数据上运行（比如多了并列、空值、边界值），只对样例凑出结果是不够的。
