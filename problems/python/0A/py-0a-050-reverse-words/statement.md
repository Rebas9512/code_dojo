## 题目

把句子 `s` 中的单词顺序反过来，单词之间用**一个**空格连接。
`s` 的开头、结尾和单词之间可能有多个空格，结果里都不要。例如 `"  hello   world "` → `"world hello"`。

`s.split()`（不带参数）按任意空白切分并自动丢掉空串；`" ".join(words)` 用空格把单词列表连成字符串。

## 示例

**示例 1**

```
输入：s = "the sky is blue"
输出："blue is sky the"
```

**示例 2**

```
输入：s = "  hello   world "
输出："world hello"
```

## 约束

- `0 <= len(s) <= 10^4`
- 单词由非空格字符组成

---

原题参考：<https://leetcode.com/problems/reverse-words-in-a-string/>（题面为自写）
