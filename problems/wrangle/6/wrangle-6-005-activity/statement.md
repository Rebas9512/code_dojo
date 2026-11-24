这三项特征描述读者最近怎样使用 App。输入 `sessions` 是已经编号的事件表；`cutoff` 是 UTC 零点，骨架中的 `WINDOW` 是 30 天。

```python
def activity_features(sessions, cutoff):
```

只取从 cutoff − 30 天起（含）、到 cutoff 之前的事件。只返回窗口里有事件的用户，按 user_id 升序。四列依次是 user_id、sessions_30d（不同会话数）、active_days_30d（不同 UTC 自然日数）、events_30d（事件行数）。一个会话只要有事件落在窗内就计入，包括此前已经开始的会话。

## 示例 1

cutoff 为 3 月 1 日时，1 月 30 日 00:00 的事件计入，3 月 1 日 00:00 的事件进入下一个窗口。

## 示例 2

同一会话在 2 月 14 日 23:56、15 日 00:04 和 00:09 有三条事件，三项统计依次为 1、2、3。
