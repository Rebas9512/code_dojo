def clean_readers(readers):
    known = readers.dropna(subset=["user_id", "joined_on"])
    users = known.loc[known["channel"] != "test"].drop_duplicates("user_id").copy()
    users["city"] = users["city"].fillna("").apply(clean_text)
    users.loc[users["city"] == "", "city"] = "unknown"
    return users[["user_id", "city", "joined_on"]].sort_values("user_id")
