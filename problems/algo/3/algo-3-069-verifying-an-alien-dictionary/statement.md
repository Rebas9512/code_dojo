## 题目

order 从最小到最大列出全部小写字母。检查 words 是否按这套字典序排列。逐位相同直到一个词结束时，短词排在前面。

## 示例

**示例 1**

```text
输入 ["za","ax"], "zyxwvutsrqponmlkjihgfedcba"
结果 true
```

新字母表先列 z 再列 a，首字符足以决定 za 在 ax 前面。

**示例 2**

```text
输入 ["ink","in"], "abcdefghijklmnopqrstuvwxyz"
结果 false
```

## 约束

1 至 100 个小写词，每词长 1 至 20；order 是 26 个字母的排列。
