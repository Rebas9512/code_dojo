def clean_events(events, users):
    known = events.dropna(subset=["event_id", "user_id", "action", "happened_at"])
    matched = known.loc[known["user_id"].isin(users["user_id"])].copy()
    matched["action"] = matched["action"].apply(clean_text)
    valid = matched.loc[matched["action"] != ""]
    return valid.drop_duplicates("event_id")
