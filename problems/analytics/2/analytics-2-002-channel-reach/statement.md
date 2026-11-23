## 题目

按注册读者的渠道分组，每个已有类别一行，按类别升序。依次统计做过 view、cart 的去重人数，各步骤独立计数，同一人可以进入多步。

## 用到的表

readers(user_id, joined_on, channel, city, device) 每人一行，含注册日期、获客渠道、城市、设备。

events(event_id, user_id, action, happened_at) 每次操作一行。view、cart、order、pay、search 分别代表浏览、加购、下单、付款和搜索。

## 示例结果

| channel | view_users | cart_users |
|---|---|---|
| ad | 16 | 16 |
| organic | 16 | 16 |
| referral | 16 | 16 |

同一位广告渠道读者重复加购，仍只在 ad 行的加购列贡献一次。

样例共 3 行。按示例列顺序输出，行按题意排序。
