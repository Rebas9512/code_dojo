把各部分接成可以交付的 churn.py。模型用训练读者拟合，验证读者决定从哪个概率开始报流失，测试读者给出最终成绩。

## 签名与任务

```python
def main():
```

无参数调用。骨架提供下列接口；各配置都取自骨架，判题时会换数据和配置。

1. 用 `load_split(DATA_DIR / "features.csv", SEED)` 得到 `numeric, cities, labels, train, valid, test`。先将三个数据数组各取训练行，交给 `select_params(..., CANDIDATES, FOLDS, STEPS)`，读回最佳 `(rate, l2)`。
2. 用 `prepare_design(numeric, cities, train)` 建立全体读者的设计矩阵，按所选参数和 `STEPS` 在全部训练行上调用 `train_model` 一次。
3. 用 `sigmoid(design[valid] @ weights)` 求验证概率。用 `predict_labels` 与 `classification_report` 比较 `THRESHOLDS` 中各阈值的验证 F1，最高者胜，相等时取排在前面的阈值。
4. 用同一个模型计算测试概率、预测标签、混淆矩阵和指标。AUC 用连续的测试概率。先打印一行英文摘要，再在末行打印 JSON 对象，键为 `confusion, precision, recall, f1, auc, rate, l2, threshold`。其中 `confusion` 排列为 `[[TN, FP], [FN, TP]]`。

## 示例

- 用随包 CSV 的前 50 行、种子 42、两折八步，候选为 `[(0.1, 0), (0.3, 0.1)]`，阈值为 `[0.4, 0.5, 0.6]`。应选第二组参数和阈值 0.4，测试矩阵为 `[[0, 1], [0, 8]]`，F1 约 0.941176，AUC 为 1。
- 从第 51 行读起取 80 位读者（均不计表头），种子 11、三折零步，参数为 `[(0.2, 0.8), (0.5, 0)]`，阈值为 `[0.5, 0.3, 0.7]`。概率全为 0.5，选第一组参数与阈值 0.5，测试矩阵为 `[[0, 8], [0, 7]]`，AUC 为 0.5。

## 约束

测试集中两种标签都出现。指标保留浮点精度，最后一行用 `json.dumps` 编码。模型训练和选参数、阈值的过程只能使用各自指定的读者。
