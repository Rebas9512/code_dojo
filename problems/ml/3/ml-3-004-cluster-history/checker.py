from dojo_compare import allclose


def check_function(args, expected, cluster):
    points, original, rounds = args
    centers = [list(map(float, row)) for row in original]
    history = cluster(points, original, rounds)
    assert len(history) == rounds, "每一轮都应留下记录"
    for turn, (actual_centers, actual_labels) in enumerate(history, 1):
        labels = [min(range(len(centers)), key=lambda i: sum((a-b)**2 for a,b in zip(point, centers[i])))
                  for point in points]
        for i in range(len(centers)):
            members = [p for p, label in zip(points, labels) if label == i]
            if members:
                centers[i] = [sum(col) / len(members) for col in zip(*members)]
        for name, want, got in [("标签", labels, actual_labels), ("中心", centers, actual_centers)]:
            reason = allclose(want, got)
            assert reason is None, f"第 {turn} 轮的{name}不符。{reason}"
    return True
