## 题目

书店有一批旧邮箱，形如 `lin@example.com`。请从读者表 `users` 的 `email` 列中找出符合这条命名规则的完整地址，同时列出读者编号 `user_id`。

邮箱从头到尾依次由两部分组成：至少一个小写英文字母（a 到 z），然后是固定文字 `@example.com`。字母前后都不能夹杂数字、空格或其他符号。

## 示例

样例结果节选：

| user_id | email |
|---|---|
| 1 | liwei@example.com |
| 3 | alice@example.com |

8 号读者的邮箱是 `liwei88@example.com`，用户名里含数字，所以结果里没有 8 号。单字母用户名也合法，例如 `a@example.com`。

## 约束

- 比较时区分大小写。域名里有一个真正的点号，地址在 `com` 后就结束。
- 结果依次为 `user_id`、`email`，每个符合条件的读者一行，行序不限。
