这张名单决定哪些账号可以进入项目。输入 `readers` 是已定类型的登记表，列为 user_id、joined_on、channel、city、device。

```python
def clean_readers(readers):
```

去掉缺 user_id 或 joined_on 的行，以及 channel 等于 `test` 的测试账号。channel 有值，取自 ad、referral、organic、test。同一 user_id 保留第一条合格登记，以输入次序为准。城市去首尾空白、转小写，缺失或只含空白记为 `unknown`。返回 user_id、city、joined_on 三列，按 user_id 升序；保留原 UTC 注册日。截止日前后的人都先登记。

骨架提供 `clean_text(text)`，把一个非空字符串去首尾空白、转小写。可对一列使用已学过的 `apply`。

## 示例 1

编号 7 的城市是 ` YORK `，编号 2 的城市为空。若两人均合格，先返回 2（unknown），再返回 7（york）。

## 示例 2

编号 4 的首条登记缺注册日，第二条填了日期和 Rome。留下第二条，城市写作 rome。只有测试登记的账号没有输出行。
