def classification_report(labels, predictions):
    reported = int(np.sum(predictions))
    actual = int(np.sum(labels))
    tp = int(np.sum(labels[predictions == 1]))
    fp, fn = reported - tp, actual - tp
    tn = len(labels) - tp - fp - fn
    return {
        "confusion": [[tn, fp], [fn, tp]],
        "precision": tp / reported if reported else 0.0,
        "recall": tp / actual if actual else 0.0,
        "f1": 2 * tp / (reported + actual) if reported + actual else 0.0,
    }
