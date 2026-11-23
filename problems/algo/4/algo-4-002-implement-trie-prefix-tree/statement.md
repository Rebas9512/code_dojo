## 题目

实现 Trie。insert(word) 收录单词，search(word) 查询完整单词，startsWith(prefix) 查询有没有以它开头的词。每组操作从一个空词柜开始。

## 示例

**示例 1**

```text
操作 ["Trie","insert","search","startsWith"]
参数 [[],["moss"],["mo"],["mo"]]
结果 [null,null,false,true]
```

插过 moss 后 mo 是前缀，只有 moss 是完整词。

**示例 2**

```text
操作 ["Trie","insert","insert","search"]
参数 [[],["tea"],["te"],["te"]]
结果 [null,null,null,true]
```

## 约束

词和前缀只含小写英文字母，长 1 至 2 000。最多调用 30 000 次。
