## 题目

实现 TinySet()。add(x) 记下整数，重复加入只保留一份；contains(x) 返回是否记过。add 没有返回值。

样例里的操作、参数、结果按列一一对应。第一项建立对象，同一个用例的后续操作都作用在它上面。null 表示该步没有返回值。

## 示例

**示例 1**

```text
操作 ["TinySet","add","contains"]
参数 [[],[3],[3]]
结果 [null,null,true]
```

add(3) 写入对象，紧接着的 contains(3) 就能读到它。

**示例 2**

```text
操作 ["TinySet","contains"]
参数 [[],[-7]]
结果 [null,false]
```

## 约束

每个操作序列最多 1000 次调用，可使用列表。
