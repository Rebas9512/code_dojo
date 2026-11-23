CREATE TABLE readers (
    user_id integer PRIMARY KEY,
    joined_on date NOT NULL,
    channel text NOT NULL,
    city text NOT NULL,
    device text NOT NULL
);
CREATE TABLE logins (
    login_id integer PRIMARY KEY,
    user_id integer NOT NULL REFERENCES readers,
    logged_at timestamp NOT NULL
);
CREATE TABLE events (
    event_id integer PRIMARY KEY,
    user_id integer NOT NULL REFERENCES readers,
    action text NOT NULL,
    happened_at timestamp NOT NULL
);
CREATE TABLE payments (
    payment_id integer PRIMARY KEY,
    user_id integer NOT NULL REFERENCES readers,
    paid_at timestamp NOT NULL,
    amount numeric(8,2) NOT NULL
);
CREATE TABLE memberships (
    entry_id integer PRIMARY KEY,
    user_id integer NOT NULL REFERENCES readers,
    occurred_on date NOT NULL,
    kind text NOT NULL,
    price numeric(6,2) NOT NULL
);
CREATE TABLE assignments (
    assignment_id integer PRIMARY KEY,
    experiment text NOT NULL,
    user_id integer NOT NULL REFERENCES readers,
    arm text NOT NULL,
    assigned_at timestamp NOT NULL
);

-- 结账改版的专项埋点，每次进入结账页一行。
CREATE TABLE checkout_visits (
    visit_id integer PRIMARY KEY,
    device text NOT NULL,
    viewed_at timestamp NOT NULL,
    carted_at timestamp,
    ordered_at timestamp
);
-- 续费提醒活动的到期名单，每个订阅周期一行。
CREATE TABLE renewal_offers (
    cycle_id integer PRIMARY KEY,
    plan text NOT NULL,
    due_on date NOT NULL,
    renewed_on date
);
