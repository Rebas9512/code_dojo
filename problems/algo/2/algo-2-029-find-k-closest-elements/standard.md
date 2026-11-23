## 思路

有序列中离 x 最远的剩余值一定在两端之一。每次删掉较远的一端，直到剩下 k 项，它们已按题目要求排好序。

## 复杂度

设有 n 项，比较 n−k 次，再复制 k 项，时间 O(n)，除结果外额外空间 O(1)。

## 写法要点

- 距离相等时去掉右端，较小的左值就会留下。先筛选再一次切片，过程中无需移动数组元素。

## 进阶写法

若数组很长、k 很小，可以二分查找答案窗口的起点。把相邻两个窗口中不同的两端作比较，就能把定位时间降到 O(log(n−k+1))，最后另花 O(k) 复制结果。

```python
def closest(arr: list[int], k: int, x: int) -> list[int]:
    low, high = 0, len(arr) - k
    while low < high:
        mid = (low + high) // 2
        if x - arr[mid] > arr[mid + k] - x:
            low = mid + 1
        else:
            high = mid
    return arr[low:low + k]
```
