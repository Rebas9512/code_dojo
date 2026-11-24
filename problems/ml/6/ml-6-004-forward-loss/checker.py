def check_function(args, expected, fn):
    design, labels, weights, l2 = args
    probabilities, loss = fn(np.asarray(design), np.asarray(labels), np.asarray(weights), l2)
    assert np.shape(probabilities) == (len(labels),), "每位读者应有一个概率"
    assert np.ndim(loss) == 0, "整批记录应得到一个平均损失"
    np.testing.assert_allclose(probabilities, expected[0], atol=1e-8)
    np.testing.assert_allclose(loss, expected[1], atol=1e-8)
    return True
