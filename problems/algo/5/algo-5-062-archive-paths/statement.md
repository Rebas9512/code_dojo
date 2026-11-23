## 题目

实现 Archive。mkdir(path) 沿绝对路径创建缺少的所有目录，已存在时保留原内容。ls(path) 按字典序返回直属子项的名字。根目录写作 /。 如果 path 是文件，ls 返回只含文件名的列表。addContentToFile(path,content) 新建文件或在末尾追加文字；父目录保证存在。readContentFromFile(path) 返回完整内容。写操作返回 None。

起始代码保留上一级的实现。区分目录和文件，并让列举操作也支持文件路径。

## 示例

**示例 1**

```text
操作 ["Archive","mkdir","addContentToFile","addContentToFile","readContentFromFile","ls"]
参数 [[],["/r"],["/r/k","hi"],["/r/k","ya"],["/r/k"],["/r/k"]]
结果 [null,null,null,null,"hiya",["k"]]
```

两次写入同一个文件，读回的是依次拼接的文本。

**示例 2**

```text
操作 ["Archive","mkdir","mkdir","ls","ls"]
参数 [[],["/zo/m"],["/ax"],["/"],["/zo"]]
结果 [null,null,null,["ax","zo"],["m"]]
```

## 约束

路径由非空小写英文名字以 / 隔开，除根外无末尾 /。至多 20 000 次调用。查询的路径一定存在。 文件和目录不会重名。
