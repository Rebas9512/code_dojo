## 题目

为每位用户生成推荐关系名册，依次列用户编号、用户姓名、推荐人姓名。没有推荐人时，最后一列填 NULL。只查直接推荐他的人。

把编辑器里的 `____` 换成缺少的 SQL。

## 用到的表

`users(user_id, name)` 每位读者一行，编号唯一，姓名可以重复。 同表的 `referrer_id` 是直接推荐人的用户编号，可能为空。

## 示例结果

| user_id | name | referrer_name |
|---|---|---|
| 1 | Li Wei | NULL |
| 10 | Emma Davis | Alice Brown |
| 11 | Zhao Lei | NULL |
| 12 | Huang Ying | Sun Li |
| 13 | Xu Ming | NULL |
| 14 | Noah Wilson | Bob Smith |
| 15 | Gao Yan | Chen Jie |
| 16 | Ma Chao | NULL |

样例共 20 行。这里只列出其中 8 行。

10 号读者的推荐人编号是 3；3 号用户的姓名是 Alice Brown。推荐关系只沿一层。

按上表的列顺序输出。行的顺序不限。
