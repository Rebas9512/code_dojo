def main():
    readers, events, payments = load_tables(DATA_DIR)
    users = clean_readers(readers)
    sessions = sessionize(clean_events(events, users))
    orders = paid_orders(payments)
    activity = activity_features(sessions, CUTOFF)
    purchases = purchase_features(orders, CUTOFF)
    features = label_features(users, activity, purchases, orders, CUTOFF)

    features.to_csv("features.csv", index=False)
    metrics = {
        "rows": len(features),
        "columns_ok": int(list(features.columns) == FEATURE_COLUMNS),
        "churn_rate": features["churned"].mean(),
        "spend_30d": float(features["spend_30d"].sum()),
    }
    print(json.dumps(metrics))
