# 8×8 手写数字

E. Alpaydin 和 C. Kaynak（1998）发布了 *Optical Recognition of Handwritten Digits*。UCI 原始数据把 32×32 的二值图按 4×4 分块计数，一张图得到 8×8 个介于 0 和 16 之间的整数。[UCI 数据页](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits) · [DOI](https://doi.org/10.24432/C50P49)

数据使用 Creative Commons Attribution 4.0 International 许可。[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## 从原始文件得到 digits.csv

从 [UCI 压缩包](https://archive.ics.uci.edu/static/public/80/optical+recognition+of+handwritten+digits.zip) 取出 `optdigits.tes`。保留全部 1,797 行的顺序、65 个整数与逗号分隔，统一使用 LF 换行，在首行添加列名。前 64 列依次为 `p0` 至 `p63`，从左到右、从上到下读像素。最后一列 `label` 为 0 到 9 的数字类别。

原发布将这份文件用作测试集。本项目把它作为独立练习数据，用固定种子重新切分，默认 1,438 张用于更新参数、359 张用于验证。项目报告的是这 359 张上的准确率。
