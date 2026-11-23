## 题目

以 2025-03-01 所在自然月的现有登录记录为本期；本月或上月来过的人进入账本。首个登录月为本月叫 new，两月都来叫 retained，早先来过、上月没来、本月又来叫 reactivated，只有上月来叫 lost。对账本中出现的渠道，输出渠道和净增人数（新增加回流减流失），按渠道升序。

## 用到的表

readers(user_id, joined_on, channel, city, device) 每人一行，含注册日期、获客渠道、城市、设备。

logins(login_id, user_id, logged_at) 每次登录一行，同一天可多次登录。

## 示例结果

| channel | net |
|---|---|
| ad | -7 |
| organic | -8 |
| referral | -8 |

净变化允许为负，表示该渠道流失人数超过新增与回流人数之和。

样例共 3 行。按示例列顺序输出，行按题意排序。
