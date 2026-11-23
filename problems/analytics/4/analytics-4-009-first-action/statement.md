## 题目

对每位有事件的读者，返回编号和最早那条事件的编号、动作。同秒按事件编号最小取一条，按读者编号升序。

把编辑器里的 ____ 补全。

## 用到的表

events(event_id, user_id, action, happened_at) 每次操作一行。view、cart、order、pay、search 分别代表浏览、加购、下单、付款和搜索。

## 示例结果

| user_id | event_id | action |
|---|---|---|
| 1 | 1 | search |
| 2 | 26 | search |
| 3 | 42 | search |
| 4 | 75 | search |
| 5 | 84 | search |

1 号先搜索，再浏览，首条操作返回 search。

样例共 48 行。上表列出其中 5 行。按示例列顺序输出，行按题意排序。
