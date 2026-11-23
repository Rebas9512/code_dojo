## 题目

实现 Twitter。postTweet(userId,tweetId) 发布唯一编号的动态；follow 和 unfollow 按两个用户编号建立或取消单向关注；getNewsFeed(userId) 返回自己和当前所关注用户的最近十条编号，从新到旧。

操作与参数逐项对应。第一步创建实例，之后共用这个实例，null 表示该步没有返回值。

## 示例

**示例 1**

```text
操作 ["Twitter","postTweet","follow","postTweet","getNewsFeed"]
参数 [[],[2,8],[1,2],[1,4],[1]]
结果 [null,null,null,null,[4,8]]
```

读者 1 能看到自己的 4 和已关注用户的 8，4 发布得更晚。

**示例 2**

```text
操作 ["Twitter","postTweet","follow","unfollow","getNewsFeed"]
参数 [[],[2,9],[1,2],[1,2],[1]]
结果 [null,null,null,null,[]]
```

## 约束

用户编号为 1 至 500，最多 30 000 次操作；不会关注自己。
