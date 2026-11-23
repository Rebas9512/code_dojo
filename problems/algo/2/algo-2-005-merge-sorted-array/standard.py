def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    i, j = m - 1, n - 1
    for dest in range(m + n - 1, -1, -1):
        if j < 0:
            break
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[dest] = nums1[i]
            i -= 1
        else:
            nums1[dest] = nums2[j]
            j -= 1


def run_case(nums1: list[int], m: int, nums2: list[int], n: int) -> list:
    merge(nums1, m, nums2, n)
    return nums1
