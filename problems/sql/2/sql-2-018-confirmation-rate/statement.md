## 题目

账号有时要多次验证。请为所有注册账号输出编号和验证通过率。用结果为 `ok` 的请求数除以该账号的全部请求数，得到 0 到 1 之间的数，再四舍五入到小数点后两位。没有请求的账号填 0。

## 用到的表

`accounts(account_id)` 登记了所有账号。

`checks(check_id, account_id, outcome)` 每条请求有独立编号，结果为 ok 或 timeout。

## 样例数据

**accounts**

| account_id |
|---|
| 2 |
| 4 |
| 8 |

**checks**

| check_id | account_id | outcome |
|---|---|---|
| 1 | 4 | ok |
| 2 | 4 | timeout |
| 3 | 8 | timeout |
| 4 | 4 | timeout |

## 示例结果

| account_id | confirmation_rate |
|---|---|
| 2 | 0.00 |
| 4 | 0.33 |
| 8 | 0.00 |

样例共 3 行。

4 号账号的三次请求只有一次成功，通过率为 0.33。2 号没有请求，8 号有请求但都超时，两者的通过率都是 0。

按上表的列顺序输出。行的顺序不限。
