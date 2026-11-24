def sessionize(events):
    ordered = events.sort_values(["user_id", "happened_at", "event_id"]).copy()
    gaps = ordered.groupby("user_id")["happened_at"].diff()
    starts = gaps.fillna(SESSION_GAP) >= SESSION_GAP
    ordered["session_id"] = starts.groupby(ordered["user_id"]).cumsum()
    return ordered
