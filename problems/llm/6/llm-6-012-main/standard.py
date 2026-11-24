def main():
    torch.set_num_threads(1)
    torch.manual_seed(CFG.seed)
    text = (DATA_DIR / "pride.txt").read_text(encoding="utf-8")
    vocab = CharVocab(text)
    data = TextWindows(vocab.encode(text))
    model = GPT(len(vocab.chars), CFG.context, CFG.width, CFG.heads, CFG.layers)
    optimizer = make_optimizer(model, CFG.peak, CFG.decay)
    history = train_model(model, data, optimizer, CFG)

    prompt = vocab.encode(CFG.prompt)
    args = (model, prompt, CFG.new_chars, CFG.temperature, CFG.top_k, CFG.seed)
    full = generate(*args, use_cache=False)
    cached = generate(*args, use_cache=True)
    print(vocab.decode(cached))
    print(json.dumps({
        "val_loss": history[-1][1],
        "cache_match": int(full == cached),
        "generated_chars": len(cached) - len(prompt),
    }))
