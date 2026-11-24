"""从书店读者的过去 30 天记录预测下一个月是否流失。"""

import json

import numpy as np
import pandas as pd

NUMERIC_COLUMNS = [
    "signup_days", "sessions_30d", "active_days_30d", "events_30d",
    "orders_30d", "spend_30d", "avg_basket", "days_since_last_order",
]
SEED = 42
FOLDS = 4
STEPS = 120
CANDIDATES = [(0.05, 0.0), (0.05, 0.02), (0.2, 0.0), (0.2, 0.02)]
THRESHOLDS = [0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65]


def sigmoid(scores):
    """将线性分数稳定地换算为正类概率。"""
    return np.exp(-np.logaddexp(0.0, -scores))


def prepare_design(numeric, cities, train):
    """以本轮训练行的坐标系和城市词表，变换传入的所有行。"""
    center, scale = fit_scaler(numeric[train])
    vocabulary = np.unique(cities[train])
    return design_matrix((numeric - center) / scale, cities, vocabulary)


# @part ml-6-001-split-readers


# @part ml-6-002-fit-scaler


# @part ml-6-003-design-matrix


# @part ml-6-004-forward-loss


# @part ml-6-005-gradient


# @part ml-6-006-train


# @part ml-6-007-predict


# @part ml-6-008-report


# @part ml-6-009-auc


# @part ml-6-010-cross-validation


# @part ml-6-011-main
