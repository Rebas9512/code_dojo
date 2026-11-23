## 题目

列出每位用户的姓名和手机号；手机号为空时显示字符串 `none`。补全第二列。

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

| name | phone |
|---|---|
| Li Wei | 13800000001 |
| Zhang Min | none |
| Alice Brown | 15500000003 |
| Wang Fang | 13900000004 |
| Bob Smith | none |
| Chen Jie | 18600000006 |
| Liu Yang | 13700000007 |
| Li Wei | none |

（共 20 行，这里只列出前 8 行。）

## 约束

- 结果两列：姓名、手机号（或 `none`）。
- 行的顺序不要求。
- 列名不检查，但列的个数和顺序要和要求一致。
- 提交后还会在几份隐藏数据上运行（比如多了并列、空值、边界值），只对样例凑出结果是不够的。
