## 题目

范围为 2025 年 2 月至少登录一次的读者，只汇总他们当月的图书流水，正负金额相加。按 device 分组升序，只列有活跃读者的类别。净额除以至少有一笔正向收款的人数；无人付费输出 NULL。输出人均金额，保留 2 位小数。

## 用到的表

readers(user_id, joined_on, channel, city, device) 每人一行，含注册日期、获客渠道、城市、设备。

logins(login_id, user_id, logged_at) 每次登录一行，同一天可多次登录。

payments(payment_id, user_id, paid_at, amount) 图书交易流水，收款为正，退款为负。金额单位为元。

## 示例结果

| device | arppu |
|---|---|
| android | 39.86 |
| ios | 19.00 |
| web | 44.25 |

一个设备组若有活跃读者却全都没付费，该行的付费人均金额应为空。

样例共 3 行。按示例列顺序输出，行按题意排序。
