## 题目

范围为 2025 年 2 月至少登录一次的读者，只汇总他们当月的图书流水，正负金额相加。按 channel 分组升序，只列有活跃读者的类别。净额除以全部活跃人数，未消费记零收入。输出人均金额，保留 2 位小数。

先运行初始查询，对照样例找到口径偏差，再修正查询。

## 用到的表

readers(user_id, joined_on, channel, city, device) 每人一行，含注册日期、获客渠道、城市、设备。

logins(login_id, user_id, logged_at) 每次登录一行，同一天可多次登录。

payments(payment_id, user_id, paid_at, amount) 图书交易流水，收款为正，退款为负。金额单位为元。

## 示例结果

| channel | arpu |
|---|---|
| ad | 18.75 |
| organic | 24.43 |
| referral | 13.00 |

广告渠道的分母只数当月登录过的广告渠道读者。

样例共 3 行。按示例列顺序输出，行按题意排序。
