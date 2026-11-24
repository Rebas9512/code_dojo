def purchase_features(orders, cutoff):
    import pandas as pd

    history = orders.loc[orders["paid_at"] < cutoff]
    last = history.groupby("user_id", as_index=False).agg(last_order=("paid_at", "max"))
    last_midnight = pd.to_datetime(last["last_order"].dt.date, utc=True)
    last["days_since_last_order"] = (cutoff - last_midnight).dt.days

    recent = history.loc[history["paid_at"] >= cutoff - WINDOW]
    totals = recent.groupby("user_id", as_index=False).agg(
        orders_30d=("payment_id", "size"),
        spend_30d=("amount", "sum"),
        avg_basket=("amount", "mean"),
    )
    return (
        last[["user_id", "days_since_last_order"]].merge(totals, on="user_id", how="left").fillna(0)
    )
