def sample_token(logits, temperature, k, generator):
    """按温度与 top-k 抽一个字符编号。"""
