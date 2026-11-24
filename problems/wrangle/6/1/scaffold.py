"""从书店 App 的导出表构建读者特征，预测目标为未来 30 天是否流失。"""

import json

import pandas as pd

# 导出表用空字段表示缺失；例如城市代码 NA 仍是文本。
CSV_OPTIONS = {"keep_default_na": False, "na_values": [""]}
CUTOFF = pd.Timestamp("2025-03-01", tz="UTC")
WINDOW = pd.Timedelta(days=30)
SESSION_GAP = pd.Timedelta(minutes=30)
FEATURE_COLUMNS = [
    "user_id", "city", "signup_days", "sessions_30d", "active_days_30d",
    "events_30d", "orders_30d", "spend_30d", "avg_basket",
    "days_since_last_order", "churned",
]


def clean_text(text):
    """统一导出文本的首尾空白和大小写。"""
    return text.strip().lower()


def paid_orders(payments):
    """一条正向付款算一单；排除缺失流水、重复回传和退款。"""
    complete = payments.dropna(subset=["payment_id", "user_id", "paid_at", "amount"])
    return complete.loc[complete["amount"] > 0].drop_duplicates("payment_id")


# @part wrangle-6-001-load-tables


# @part wrangle-6-002-clean-readers


# @part wrangle-6-003-clean-events


# @part wrangle-6-004-sessionize


# @part wrangle-6-005-activity


# @part wrangle-6-006-purchases


# @part wrangle-6-007-label-features


# @part wrangle-6-008-report
