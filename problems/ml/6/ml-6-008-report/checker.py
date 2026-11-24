def check_function(args, expected, fn):
    actual = fn(np.asarray(args[0]), np.asarray(args[1]))
    actual = json.loads(json.dumps(actual))
    np.testing.assert_array_equal(actual["confusion"], expected["confusion"])
    for key in ("precision", "recall", "f1"):
        assert np.isscalar(actual[key]), f"{key} 应为一个数"
        np.testing.assert_allclose(actual[key], expected[key], atol=1e-8)
    return True
