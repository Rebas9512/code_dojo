## 题目

实现 BSTIterator(root)。next() 返回升序的下一个值并前进，hasNext() 表示是否还有值，多次询问不前进。结果按调用顺序列出。

请实现 `BSTIterator`。起始代码的 `run_case` 负责转换样例和读取结果，提交时保留它。

## 示例

**示例 1**

```text
输入 [5,2,9], ["hasNext","hasNext","next","next"]
结果 [true,true,2,5]
```

两次询问都没有消耗最小的卡 2。

**示例 2**

```text
输入 [8], ["next","hasNext"]
结果 [8,false]
```

## 约束

非空搜索树，至多 20 000 次有效调用。额外空间 O(树高)，next 均摊 O(1)。
