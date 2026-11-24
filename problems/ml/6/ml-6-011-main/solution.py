def main():
    numeric, cities, labels, train, valid, test = load_split(DATA_DIR / "features.csv", SEED)
    (rate, l2), _ = select_params(
        numeric[train], cities[train], labels[train], CANDIDATES, FOLDS, STEPS
    )
    design = prepare_design(numeric, cities, train)
    weights = train_model(design[train], labels[train], rate, l2, STEPS)

    valid_prob = sigmoid(design[valid] @ weights)
    f1_scores = [
        classification_report(labels[valid], predict_labels(valid_prob, level))["f1"]
        for level in THRESHOLDS
    ]
    threshold = THRESHOLDS[np.argmax(f1_scores)]

    test_prob = sigmoid(design[test] @ weights)
    report = classification_report(labels[test], predict_labels(test_prob, threshold))
    report["auc"] = roc_auc(labels[test], test_prob)
    report["rate"] = rate
    report["l2"] = l2
    report["threshold"] = threshold
    print("test users", len(test), "validation F1", max(f1_scores))
    print(json.dumps(report))
