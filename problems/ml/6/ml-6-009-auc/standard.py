def roc_auc(labels, scores):
    negatives = np.sort(scores[labels == 0])
    positives = scores[labels == 1]
    lower = np.searchsorted(negatives, positives, side="left")
    upper = np.searchsorted(negatives, positives, side="right")
    return np.mean((lower + upper) / 2) / len(negatives)
