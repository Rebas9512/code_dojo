"""在仓库中运行本文件，按固定种子从 readerapp 重建同目录的八张 CSV。"""

import csv
import random
import sqlite3
from datetime import UTC, date, datetime, timedelta, timezone
from pathlib import Path

DEST = Path(__file__).resolve().parent
SOURCE = DEST.parents[3] / "analytics" / "_db" / "readerapp"
SEED = 20261123


def load_source():
    db = sqlite3.connect(":memory:")
    for filename in ("schema.sql", "seed.sql"):
        db.executescript((SOURCE / filename).read_text(encoding="utf-8"))
    columns, tables = {}, {}
    for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
        rows = db.execute(f"SELECT * FROM {name} ORDER BY 1")
        columns[name] = [field[0] for field in rows.description]
        tables[name] = [list(row) for row in rows]
    db.close()
    return columns, tables


def extend_population(tables, rng):
    profiles = list(tables["readers"])
    for user_id in range(len(profiles) + 1, 2001):
        _, _, channel, city, device = rng.choice(profiles)
        joined = date(2024, 12, 15) + timedelta(days=rng.randrange(85))
        tables["readers"].append([user_id, joined.isoformat(), channel, city, device])
        visit_chance, buy_chance = rng.choice([(0.12, 0.12), (0.45, 0.35), (0.90, 0.77)])
        day = joined
        while day < date(2025, 4, 1):
            if rng.random() < visit_chance:
                start = datetime.combine(day, datetime.min.time()) + timedelta(minutes=rng.randrange(1440))
                tables["logins"].append([len(tables["logins"]) + 1, user_id, start.isoformat()])
                actions = ["search", "view"]
                if rng.random() < buy_chance:
                    actions.extend(["cart", "order", "pay"])
                for action in actions:
                    start += timedelta(minutes=rng.randrange(1, 12))
                    tables["events"].append([len(tables["events"]) + 1, user_id, action, start.isoformat()])
                if actions[-1] == "pay":
                    price = rng.choice([9.50, 12, 15, 18.75, 21, 24])
                    payments = tables["payments"]
                    payments.append([len(payments) + 1, user_id, start.isoformat(), price])
                    if rng.random() < 0.07:
                        refund = start + timedelta(hours=2)
                        payments.append([len(payments) + 1, user_id, refund.isoformat(), -price])
            day += timedelta(days=rng.randint(4, 9))
        assignments = tables["assignments"]
        assignments.append([len(assignments) + 1, "cover", user_id, rng.choice(["A", "B"]),
                            joined.isoformat() + "T10:00:00"])
        if rng.random() < 0.20:
            memberships = tables["memberships"]
            memberships.append([len(memberships) + 1, user_id, joined.isoformat(), "start", 12])


def dirty_exports(tables, rng):
    for row in tables["readers"]:
        if row[0] % 47 == 0:
            row[2] = "test"
        row[3] = rng.choice([row[3], row[3].upper(), f" {row[3].lower()} "])
        if row[0] % 37 == 0:
            row[3] = None
        if row[0] % 283 == 0:
            row[1] = None

    for table, index in (("logins", 2), ("events", 3), ("payments", 2), ("assignments", 4)):
        for row in tables[table]:
            stamp = datetime.fromisoformat(row[index]).replace(tzinfo=UTC)
            offset = rng.choice([None, 0, 8, -5])
            if offset is None:
                row[index] = stamp.replace(tzinfo=None).isoformat()
            else:
                row[index] = stamp.astimezone(timezone(timedelta(hours=offset))).isoformat()

    for row in tables["events"]:
        if row[0] % 71 == 0:
            row[2] = f" {row[2].upper()} "
        if row[0] % 113 == 0:
            row[3] = None
        if row[0] % 173 == 0:
            row[1] = None
    for row in tables["payments"]:
        if row[0] % 131 == 0:
            row[3] = None
    for name in ("readers", "logins", "events", "payments"):
        rows = tables[name]
        rows.extend(rng.sample(rows, len(rows) // 40))
        rng.shuffle(rows)


def main():
    rng = random.Random(SEED)
    columns, tables = load_source()
    extend_population(tables, rng)
    dirty_exports(tables, rng)
    for name, rows in tables.items():
        with (DEST / f"{name}.csv").open("w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerow(columns[name])
            writer.writerows(rows)


if __name__ == "__main__":
    main()
