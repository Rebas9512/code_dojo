def training_windows(text, width):
    vocab = {c: i for i, c in enumerate(sorted(set(text)))}
    ids = [vocab[c] for c in text]
    samples = []
    for start in range(len(ids) - width):
        end = start + width
        samples.append([ids[start:end], ids[start + 1:end + 1]])
    return samples
