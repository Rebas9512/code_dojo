## 题目

按注册读者的设备分组，每个已有类别一行，按类别升序。依次统计做过 order、pay 的去重人数，各步骤独立计数，同一人可以进入多步。

先运行初始查询，对照样例找到口径偏差，再修正查询。

## 用到的表

readers(user_id, joined_on, channel, city, device) 每人一行，含注册日期、获客渠道、城市、设备。

events(event_id, user_id, action, happened_at) 每次操作一行。view、cart、order、pay、search 分别代表浏览、加购、下单、付款和搜索。

## 示例结果

| device | order_users | pay_users |
|---|---|---|
| android | 13 | 12 |
| ios | 14 | 14 |
| web | 14 | 11 |

android 的下单与付款人数分别是 13 和 12；对同一动作数流水会重复计人。

样例共 3 行。按示例列顺序输出，行按题意排序。
