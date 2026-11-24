def activity_features(sessions, cutoff):
    history = sessions.loc[sessions["happened_at"] < cutoff]
    recent = history.loc[history["happened_at"] >= cutoff - WINDOW].copy()
    recent["day"] = recent["happened_at"].dt.date
    return recent.groupby("user_id", as_index=False).agg(
        sessions_30d=("session_id", "nunique"),
        active_days_30d=("day", "nunique"),
        events_30d=("event_id", "size"),
    )
