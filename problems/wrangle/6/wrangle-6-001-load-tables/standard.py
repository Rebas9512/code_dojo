def load_tables(data_dir):
    import pandas as pd

    readers = pd.read_csv(
        data_dir / "readers.csv",
        dtype={"user_id": "Int64", "channel": "string", "city": "string", "device": "string"},
        **CSV_OPTIONS,
    )
    events = pd.read_csv(
        data_dir / "events.csv",
        dtype={"event_id": "Int64", "user_id": "Int64", "action": "string"},
        **CSV_OPTIONS,
    )
    payments = pd.read_csv(
        data_dir / "payments.csv",
        dtype={"payment_id": "Int64", "user_id": "Int64", "amount": "float64"},
        **CSV_OPTIONS,
    )
    readers["joined_on"] = pd.to_datetime(readers["joined_on"], utc=True)
    events["happened_at"] = pd.to_datetime(events["happened_at"], format="mixed", utc=True)
    payments["paid_at"] = pd.to_datetime(payments["paid_at"], format="mixed", utc=True)
    return readers, events, payments
