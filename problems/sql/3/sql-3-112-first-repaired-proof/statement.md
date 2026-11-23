## 题目

每块印版从首次 bad 开始，到严格晚于该日的首次 ok 为止。输出有完整过程的 plate 和相隔的天数 days。

## 样例输入

`plate_tests`

| plate | day | verdict |
|---|---|---|
| Arc | 2025-02-25 | ok |
| Arc | 2025-02-28 | bad |
| Arc | 2025-03-01 | bad |
| Arc | 2025-03-02 | ok |
| Bay | 2025-03-03 | bad |

## 样例结果

| plate | days |
|---|---|
| Arc | 2 |

Arc 在 2 月 28 日首次报损，3 月 2 日首次恢复，跨月相隔 2 天。

按上表的列顺序输出。按 days、plate 依次升序。
