## 题目

实现 WordDictionary。addWord(word) 收录完整词。search(word) 判断词柜里有无匹配整个查询的词，其中每个点恰好代替一个字母。

## 示例

**示例 1**

```text
操作 ["WordDictionary","addWord","search","search"]
参数 [[],["lamp"],["l..p"],["lam"]]
结果 [null,null,true,false]
```

l..p 正好填入两个字母就得到 lamp。lam 少了一位。

**示例 2**

```text
操作 ["WordDictionary","addWord","search"]
参数 [[],["be"],["b.."]]
结果 [null,null,false]
```

## 约束

单词长 1 至 25，只含小写英文字母。查询额外允许最多两个点，最多 10 000 次操作。
