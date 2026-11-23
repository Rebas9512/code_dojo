## 题目

以 2025-03-01 所在自然月的现有登录记录为本期；本月或上月来过的人进入账本。首个登录月为本月叫 new，两月都来叫 retained，早先来过、上月没来、本月又来叫 reactivated，只有上月来叫 lost。列出编号和英文类别，按编号升序。

把编辑器里的 ____ 补全。

## 用到的表

logins(login_id, user_id, logged_at) 每次登录一行，同一天可多次登录。

## 示例结果

| user_id | status |
|---|---|
| 1 | lost |
| 2 | lost |
| 3 | lost |
| 5 | reactivated |
| 6 | lost |

5 号一月来过、二月缺席，三月再次回来，因此应标 reactivated。

样例共 36 行。上表列出其中 5 行。按示例列顺序输出，行按题意排序。
