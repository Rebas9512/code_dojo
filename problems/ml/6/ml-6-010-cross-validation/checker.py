def check_function(args, expected, fn):
    numeric, cities, labels, candidates, k, steps = args
    chosen, losses = fn(
        np.asarray(numeric, dtype=float), np.asarray(cities), np.asarray(labels),
        candidates, k, steps,
    )
    np.testing.assert_allclose(chosen, expected[0], err_msg="请按平均验证损失选参数")
    assert np.shape(losses) == (len(candidates),), "每组候选都需要一个验证损失"
    np.testing.assert_allclose(losses, expected[1], atol=1e-8)
    return True
