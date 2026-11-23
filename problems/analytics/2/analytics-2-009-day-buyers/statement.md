## 题目

每人以首次 view 为起点，取严格晚于它的首个 order。24 小时内含右端点。统计成功人数。

把编辑器里的 ____ 补全。

## 用到的表

events(event_id, user_id, action, happened_at) 每次操作一行。view、cart、order、pay、search 分别代表浏览、加购、下单、付款和搜索。

## 示例结果

| buyers |
|---|
| 36 |

1 号在首次浏览的同一小时下单，只为成功人数贡献一人。

样例共 1 行。按示例列顺序输出，行序不限。
