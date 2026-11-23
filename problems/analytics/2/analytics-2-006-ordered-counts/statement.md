## 题目

从每人首次 view 开始，依次找严格晚于上一步的最早 cart、order。未走到的步骤记 NULL。依次统计浏览、有效加购、有效下单的去重人数。

## 用到的表

events(event_id, user_id, action, happened_at) 每次操作一行。view、cart、order、pay、search 分别代表浏览、加购、下单、付款和搜索。

## 示例结果

| viewers | carts | orders |
|---|---|---|
| 48 | 47 | 41 |

40 号虽然留下加购记录，却没有在浏览后加购，因此 48 位浏览者只有 47 位走到第二步。

样例共 1 行。按示例列顺序输出，行序不限。
