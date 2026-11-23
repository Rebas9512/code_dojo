-- code-dojo 练习数据库：虚构的网上书店（PostgreSQL 18）
-- 阶段 0–3 的入门题都用这个库；每道题的隐藏数据集在 seed.sql 之后再执行一个补丁脚本。
--
-- 表之间的关系：
--   authors 1 ── n books        （books.author_id 可能为空：作者不详）
--   users   1 ── n orders 1 ── n order_items n ── 1 books
--   users   1 ── n ratings n ── 1 books
--   users.referrer_id → users.user_id（推荐人，可能为空）

-- 作者
CREATE TABLE authors (
    author_id   integer PRIMARY KEY,
    name        text    NOT NULL,
    country     text,                 -- 国家代码，可能为空
    birth_year  integer               -- 可能为空
);

-- 图书
CREATE TABLE books (
    book_id       integer       PRIMARY KEY,
    title         text          NOT NULL,          -- 不同版本可能同名
    author_id     integer       REFERENCES authors (author_id),   -- 可能为空
    category      text          NOT NULL,          -- fiction / scifi / fantasy / history / programming / kids / cooking
    price         numeric(6, 2) NOT NULL,          -- 当前售价（元）
    stock         integer       NOT NULL,          -- 库存，0 表示售罄
    publisher     text,                            -- 出版社，可能为空
    published_on  date,                            -- 出版日期，可能为空
    pages         integer
);

-- 用户
CREATE TABLE users (
    user_id      integer PRIMARY KEY,
    name         text    NOT NULL,                 -- 可能重名
    email        text    NOT NULL UNIQUE,
    phone        text,                             -- 可能为空
    city         text,                             -- 可能为空
    signup_date  date    NOT NULL,
    referrer_id  integer REFERENCES users (user_id)   -- 推荐人，可能为空
);

-- 订单
CREATE TABLE orders (
    order_id     integer PRIMARY KEY,
    user_id      integer NOT NULL REFERENCES users (user_id),
    order_date   date    NOT NULL,
    status       text    NOT NULL,                 -- paid / shipped / delivered / cancelled
    coupon_code  text                              -- 优惠码，可能为空
);

-- 订单明细：一个订单里的每种书一行
CREATE TABLE order_items (
    order_id    integer       NOT NULL REFERENCES orders (order_id),
    book_id     integer       NOT NULL REFERENCES books (book_id),
    quantity    integer       NOT NULL,
    unit_price  numeric(6, 2) NOT NULL,            -- 下单时的成交单价（可能有折扣，可能和现价不同）
    PRIMARY KEY (order_id, book_id)
);

-- 评分：每个用户对每本书最多评一次；没买过也可以评
CREATE TABLE ratings (
    user_id   integer NOT NULL REFERENCES users (user_id),
    book_id   integer NOT NULL REFERENCES books (book_id),
    stars     integer NOT NULL CHECK (stars BETWEEN 1 AND 5),
    rated_on  date    NOT NULL,
    review    text,                                -- 文字评价，可能为空
    PRIMARY KEY (user_id, book_id)
);

-- 登录流水允许同一读者在同一天出现多次。
CREATE TABLE reader_logins (
    login_id   integer PRIMARY KEY,
    user_id    integer NOT NULL REFERENCES users (user_id),
    logged_on  date NOT NULL
);

-- 每一行是一次站内动作；不同动作可能恰好发生在同一时刻。
CREATE TABLE reader_events (
    event_id     integer PRIMARY KEY,
    user_id      integer NOT NULL REFERENCES users (user_id),
    action       text NOT NULL CHECK (action IN ('view', 'cart', 'buy')),
    happened_at  timestamp NOT NULL
);
