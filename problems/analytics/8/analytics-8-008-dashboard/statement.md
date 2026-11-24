## 题目

七个视图已经把人、会话、批次和实验组数清楚了。现在给运营交一行 3 月 15 日的快照，让他们同时看到到访人数、下单率和本月增长。

写最后一条 `SELECT`（可用 `WITH`），按下面顺序返回一行。判这部分时，输入视图已经建好。

| 输出列 | 从哪里取数 |
|---|---|
| `as_of` | 业务日期 2025-03-15 |
| `dau`、`wau` | `active_reach(grain, period_start, active_users)` 中的当日和当周登录人数 |
| `sessions_wtd` | `app_sessions(user_id, session_no, started_at, ended_at, event_count)` 中本周开启的会话数 |
| `order_rate` | `order_funnel(viewers, carters, buyers, order_rate)` 中全期的浏览到下单率 |
| `cohort_week`、`w1_rate` | `cohort_retention(cohort_week, registered, returned, w1_rate)` 中最新成熟批次的周一和次周留存率 |
| `net_active` | `monthly_growth(month_start, new_users, retained, reactivated, lost)` 中三月的新增 + 回流 − 流失 |
| `cover_a`、`cover_b` | `cover_readout(arm, enrolled, buyers, buy_rate)` 中 A、B 两组各自的七日付费率 |

## 示例

**运行样例**　小样本中，本周有 3 位读者登录，开启 2 个会话；三月新增 2 人、回流 1 人、流失 1 人。输出如下。

```text
2025-03-15 | 1 | 3 | 2 | 0.3333 | 2025-02-24 | 1.0000 | 2 | 0.5000 | 0.0000
```

**完整项目库**　在完整库运行同一条查询，三月的净变化变为 −24，最新成熟批次为 02-10。输出如下。

```text
2025-03-15 | 1 | 4 | 7 | 0.8542 | 2025-02-10 | 1.0000 | -24 | 0.8235 | 0.5882
```

## 约束

- 本周从本地 03-10 零点开始，数据已截至 03-15 当天结束。跨周会话按开始时刻归属。
- 缺少当日或当周登录时人数填 0，无会话填 0。没有浏览者、成熟批次或合格实验组时，对应比例（以及缺失的批次日期）填 `NULL`。保留来源视图中四位小数的比例。
