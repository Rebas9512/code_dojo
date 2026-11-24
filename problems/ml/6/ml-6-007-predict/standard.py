def predict_labels(probabilities, threshold):
    return (probabilities >= threshold).astype(int)
