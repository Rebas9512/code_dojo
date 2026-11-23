## 题目

每人以首次 view 为起点，取严格晚于它的首个 order。24 小时内含右端点。按设备列出有浏览者的设备、浏览人数、成功人数和转化率，按设备升序，比例保留 4 位小数。

## 用到的表

readers(user_id, joined_on, channel, city, device) 每人一行，含注册日期、获客渠道、城市、设备。

events(event_id, user_id, action, happened_at) 每次操作一行。view、cart、order、pay、search 分别代表浏览、加购、下单、付款和搜索。

## 示例结果

| device | viewers | buyers | rate |
|---|---|---|---|
| android | 16 | 12 | 0.7500 |
| ios | 16 | 12 | 0.7500 |
| web | 16 | 12 | 0.7500 |

android 组 16 人浏览，其中 12 人按时下单，得到 0.7500。

样例共 3 行。按示例列顺序输出，行按题意排序。
