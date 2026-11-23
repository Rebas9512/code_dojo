## 题目

报名表约定了邮箱的写法。`@` 前第一位必须是英文字母。从第二位起，可以用英文字母、数字、下划线 `_`、点号 `.` 和连字符 `-`。后半段必须完整写作小写的 `@leetcode.com`。列出邮箱完全符合规则的用户。

`users` 每人一行。`user_id` 是唯一编号，`name` 是姓名，`mail` 保存报名时填写的整段文字。

## 示例

**users**

| user_id | name | mail |
|---|---|---|
| 12 | 陆青 | A@leetcode.com |
| 6 | 阿澜 | 9lan@leetcode.com |
| 19 | 明晓 | Mi_2.x-y@leetcode.com |
| 2 | 冬乔 | qiu@LeetCode.com |

**查询结果**

| user_id | name | mail |
|---|---|---|
| 12 | 陆青 | A@leetcode.com |
| 19 | 明晓 | Mi_2.x-y@leetcode.com |

12 号的用户名只有一个字母也合格。6 号用数字开头，2 号的域名含大写字母。

## 约束

- 英文字母包括 A–Z 和 a–z。域名中的点号是字面上的一个点。
- 地址前后不能有多余字符。依次输出 `user_id`、`name`、`mail`，行序不限。
