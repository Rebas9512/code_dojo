def count_label(t, label):
    counts = t['status'].value_counts()
    return int(counts.get(label, 0))
