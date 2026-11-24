def label_features(users, activity, purchases, orders, cutoff):
    """合并截止前的特征，用后续 30 天订单为每位读者打标签。"""
