## 题目

给从未收到评分的书做一个邀请评价的名单，输出书号和书名。现有名单混进了已打星、没写评语的书。请修好判断条件。

## 用到的表

`books(book_id, title, author_id, price, category)` 每种书一行，记录书名、作者编号、当前标价和分类；不同版本可以同名。

`ratings(user_id, book_id, stars, review)` 是评分表。每条评分都有书号和星数；文字评语允许留空。

## 示例结果

| book_id | title |
|---|---|
| 13 | Silk Road Letters |
| 14 | Moon Rabbit |
| 17 | Winter Orchard |
| 23 | Count with Panda |
| 25 | Untitled Poems |
| 29 | Bread & Butter |
| 30 | Theory of Tides |

样例共 7 行。

12 号书收到过星级评分，即使其中有空评语，也不属于这份名单。

按上表的列顺序输出。行的顺序不限。
