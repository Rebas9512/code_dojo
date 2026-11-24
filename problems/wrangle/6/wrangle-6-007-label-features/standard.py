def label_features(users, activity, purchases, orders, cutoff):
    cohort = users.loc[users["joined_on"] < cutoff].copy()
    cohort["signup_days"] = (cutoff - cohort["joined_on"]).dt.days
    features = cohort.merge(activity, on="user_id", how="left").merge(
        purchases, on="user_id", how="left"
    )
    features["days_since_last_order"] = features["days_since_last_order"].fillna(WINDOW.days + 1)
    features = features.fillna(0)

    future = orders.loc[orders["paid_at"] >= cutoff]
    buyers = future.loc[future["paid_at"] < cutoff + WINDOW, "user_id"]
    features["churned"] = features["user_id"].isin(buyers).eq(False).astype(int)
    return features[FEATURE_COLUMNS].sort_values("user_id")
