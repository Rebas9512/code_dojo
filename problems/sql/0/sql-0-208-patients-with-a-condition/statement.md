## 题目

资料员要找出有 `DIAB1` 系列记录的人。只要其中一个编号以 `DIAB1` 开头，这个人就入选。依次输出他的 `patient_id`、`patient_name` 和原样的 `conditions`。

`patients` 每人一行。`patient_id` 是唯一编号，`patient_name` 是姓名，`conditions` 是一串用空格隔开的编号。没有记录时这一列是空字符串。

## 示例

**patients**

| patient_id | patient_name | conditions |
|---|---|---|
| 4 | 阿宁 | DIAB100 R03 |
| 9 | 阿蓝 | G12 DIAB18 |
| 7 | 子墨 | XDIAB12 |
| 3 | 许青 | `''` |

**查询结果**

| patient_id | patient_name | conditions |
|---|---|---|
| 4 | 阿宁 | DIAB100 R03 |
| 9 | 阿蓝 | G12 DIAB18 |

阿蓝的第二个编号以目标文字开头。子墨的编号以 X 开头，没有入选。表中的 `''` 表示空字符串。

## 约束

- 编号之间有一个普通空格，两端没有空格。按大小写匹配。
- 同一人即使有两个匹配编号也只输出一行，行序不限。
