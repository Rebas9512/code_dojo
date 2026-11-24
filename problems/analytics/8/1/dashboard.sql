-- 书店 App 增长看板，业务时区 UTC+08，观察至 2025-03-15 当天结束。
-- 在装有 readerapp 结构与种子的空库中执行，末条查询返回看板快照。

-- 合并登录和操作，统一业务时间
-- @part analytics-8-001-clean-activity

-- 把相邻操作切成会话
-- @part analytics-8-002-sessions

-- 统计日活和自然周活
-- @part analytics-8-003-active-reach

-- 计算浏览到下单的转化
-- @part analytics-8-004-ordered-funnel

-- 按注册周计算次周留存
-- @part analytics-8-005-cohort-retention

-- 核对三个月的增长账
-- @part analytics-8-006-monthly-growth

-- 读出封面实验的付费率
-- @part analytics-8-007-cover-experiment

-- 交付增长看板快照
-- @part analytics-8-008-dashboard
