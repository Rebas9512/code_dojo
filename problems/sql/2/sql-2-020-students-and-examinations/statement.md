## 题目

考务处要核对每位学员在每一科的签到次数。重复签到照次数计，从没签到也要列 0。依次输出学号、姓名、科目和签到次数，先按学号升序，再按英文科目名升序。

## 用到的表

`students(student_id, name)` 是学员名册，学号唯一。

`subjects(subject)` 是科目表，科目名唯一。

`attendance(student_id, subject)` 每签到一次记一行，学号、科目均非空。

## 样例数据

**students**

| student_id | name |
|---|---|
| 9 | 文 |
| 2 | 林 |

**subjects**

| subject |
|---|
| Maps |
| Ink |

**attendance**

| student_id | subject |
|---|---|
| 2 | Maps |
| 2 | Maps |
| 9 | Ink |

## 示例结果

| student_id | name | subject | attended |
|---|---|---|---|
| 2 | 林 | Ink | 0 |
| 2 | 林 | Maps | 2 |
| 9 | 文 | Ink | 1 |
| 9 | 文 | Maps | 0 |

样例共 4 行。

2 名学员和 2 门科目总共有 4 个组合。林在 Maps 签到两次，在 Ink 一次也没有。

按上表的列顺序输出。行的顺序按题目要求。
