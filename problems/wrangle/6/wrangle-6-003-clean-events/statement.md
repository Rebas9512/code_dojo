这一块把回传的埋点整理成会话切分的输入。`events` 的列是 event_id、user_id、action、happened_at，时间已转为 UTC。`users` 是清洗后的读者表，user_id 唯一。

```python
def clean_events(events, users):
```

只留四列都有值、user_id 出现在 users、action 去首尾空白后非空的行。action 统一为小写。重复 event_id 留第一条合格记录。返回上述四列，保持留下来的输入次序。即便同一人同一秒做两次相同操作，只要事件编号不同就各留一条。

骨架提供 `clean_text(text)`，把一个非空字符串去首尾空白、转小写。可对一列使用已学过的 `apply`。

## 示例 1

名单里有 8；事件 20、21 都是 8 在同一秒的 ` VIEW `。输出仍有两行，action 均为 view。

## 示例 2

事件 6 的首条回传是空操作，第二条是 cart；另一条事件属于名单外的 99。输出只有事件 6，action 为 cart。
