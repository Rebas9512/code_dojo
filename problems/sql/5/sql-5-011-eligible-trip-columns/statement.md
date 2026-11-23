## 题目

只统计下单者和配送员均未封禁的订单。每个有合格订单的日期输出日期、完成数、顾客取消数、配送员取消数及总取消率（两种取消之和除以合格订单数）。空类别填零。

## 用到的表

accounts(id,blocked) 是双方共用的账号名册。trips 的 rider 为下单者、driver 为配送员，状态为 done、rider_cancel 或 driver_cancel。

## 样例数据

**accounts**

| id | blocked |
|---|---|
| 1 | False |
| 2 | True |
| 3 | False |
| 4 | False |

**trips**

| trip | day | rider | driver | status |
|---|---|---|---|---|
| 11 | 2025-04-01 | 1 | 3 | done |
| 12 | 2025-04-01 | 1 | 4 | rider_cancel |
| 13 | 2025-04-01 | 2 | 4 | driver_cancel |
| 14 | 2025-04-02 | 3 | 1 | driver_cancel |

## 示例结果

| day | done | rider_cancel | driver_cancel | cancel_rate |
|---|---|---|---|---|
| 2025-04-01 | 1 | 1 | 0 | 0.5 |
| 2025-04-02 | 0 | 0 | 1 | 1 |

样例共 2 行。

4 月 1 日的 13 号订单由封禁用户发起，分母只剩两单，其中一单取消。

按上表的列顺序输出。行的顺序不限。
