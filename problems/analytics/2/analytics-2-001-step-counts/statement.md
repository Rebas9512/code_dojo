## 题目

汇总全部读者，输出一行。依次统计做过 view、cart、order 的去重人数，各步骤独立计数，同一人可以进入多步。

把编辑器里的 ____ 补全。

## 用到的表

events(event_id, user_id, action, happened_at) 每次操作一行。view、cart、order、pay、search 分别代表浏览、加购、下单、付款和搜索。

## 示例结果

| view_users | cart_users | order_users |
|---|---|---|
| 48 | 48 | 41 |

表中 48 位读者都触达过加购。检查先后顺序后，有效加购人数可能更少。

样例共 1 行。按示例列顺序输出，行序不限。
