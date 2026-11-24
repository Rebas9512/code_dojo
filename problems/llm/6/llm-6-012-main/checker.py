import io
from contextlib import redirect_stdout
from unittest.mock import patch


def check_function(args, expected, fn):
    steps, count, prompt, agree = args
    cfg = SimpleNamespace(**vars(CFG))
    cfg.steps, cfg.warmup, cfg.eval_every, cfg.eval_batches = steps, 1, 2, 1
    cfg.width, cfg.layers, cfg.heads, cfg.context, cfg.batch_size = 8, 1, 2, 12, 2
    cfg.new_chars, cfg.prompt, cfg.top_k = count, prompt, 4
    cfg.seed = 23 + steps
    observed = {}
    calls = []

    def record_train(model, data, optimizer, cfg):
        assert len(data.train) == 9 * len(text) // 10
        history = train_model(model, data, optimizer, cfg)
        observed["loss"] = history[-1][1]
        return history

    def record_generate(model, prompt, steps, temperature, k, seed, use_cache):
        ids = generate(model, prompt, steps, temperature, k, seed, use_cache)
        if use_cache and not agree:
            if count == 3:
                ids.pop()
            else:
                ids[-1] = (ids[-1] + 1) % len(vocab.chars)
        calls.append((use_cache, prompt, steps, temperature, k, seed, ids))
        return ids

    text = (DATA_DIR / "pride.txt").read_text(encoding="utf-8")
    vocab = CharVocab(text)
    out = io.StringIO()
    with patch.dict(fn.__globals__, CFG=cfg, train_model=record_train, generate=record_generate):
        with redirect_stdout(out):
            fn()
    assert sorted(call[0] for call in calls) == [False, True], "需要各运行一次有缓存和无缓存生成"
    for call in calls:
        assert call[1:6] == (vocab.encode(prompt), count, cfg.temperature, cfg.top_k, cfg.seed)
    cached = next(call[-1] for call in calls if call[0])
    body, last = out.getvalue().rstrip("\n").rsplit("\n", 1)
    assert body.endswith(vocab.decode(cached)), "最后一行指标之前应有完整的续写"
    metrics = json.loads(last)
    assert math.isclose(metrics["val_loss"], observed["loss"], abs_tol=1e-5)
    return metrics["cache_match"] == int(agree) and metrics["generated_chars"] == len(cached) - len(prompt)
