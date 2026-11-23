## 题目

用纯 Python 编写 Value 类，入口 make_value(x) 返回一个叶子。每个节点有浮点 data、初值为 0 的 grad、按操作数顺序排列的 parents。每条边是一对 (输入节点, 局部导数)。实现节点之间的 +、* 与无参数 .tanh()，每次返回新节点。

## 示例

a=make_value(2)、b=make_value(3) 时，(a*b).data 为 6.0，它的两条边依次是 (a,3.0)、(b,2.0)。(a+a) 有两条指向同一 a 的边。

## 约束

叶子的 parents 为空序列。相同节点用两次要有两条边；本题只建立图，无须 backward。
