CREATE TABLE users (
    user_id integer PRIMARY KEY,
    name text NOT NULL,
    mail text NOT NULL
);

INSERT INTO users VALUES
    (12, '陆青', 'A@leetcode.com'),
    (6, '阿澜', '9lan@leetcode.com'),
    (19, '明晓', 'Mi_2.x-y@leetcode.com'),
    (2, '冬乔', 'qiu@LeetCode.com');
