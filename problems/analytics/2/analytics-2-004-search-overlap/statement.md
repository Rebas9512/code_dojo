## 题目

汇总全部读者，输出一行。依次统计做过 search、view 的去重人数，各步骤独立计数，同一人可以进入多步。

## 用到的表

events(event_id, user_id, action, happened_at) 每次操作一行。view、cart、order、pay、search 分别代表浏览、加购、下单、付款和搜索。

## 示例结果

| search_users | view_users |
|---|---|
| 48 | 48 |

搜索和浏览都触达 48 人，这两群人可以重叠。

样例共 1 行。按示例列顺序输出，行序不限。
