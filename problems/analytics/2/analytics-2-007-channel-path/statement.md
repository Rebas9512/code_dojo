## 题目

从每人首次 view 开始，依次找严格晚于上一步的最早 cart、order。未走到的步骤记 NULL。对有浏览者的渠道输出渠道、浏览人数、有效加购人数，按渠道升序。

先运行初始查询，对照样例找到口径偏差，再修正查询。

## 用到的表

readers(user_id, joined_on, channel, city, device) 每人一行，含注册日期、获客渠道、城市、设备。

events(event_id, user_id, action, happened_at) 每次操作一行。view、cart、order、pay、search 分别代表浏览、加购、下单、付款和搜索。

## 示例结果

| channel | viewers | carts |
|---|---|---|
| ad | 16 | 15 |
| organic | 16 | 16 |
| referral | 16 | 16 |

广告渠道有 16 位浏览者，40 号的逆序动作使有效加购只有 15 人。

样例共 3 行。按示例列顺序输出，行按题意排序。
