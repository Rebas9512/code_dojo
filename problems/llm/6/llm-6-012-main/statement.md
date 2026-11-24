现在把前十一部分拼成可运行的 gpt.py。入口用公版英文语料训练，打印一段续写，再向项目页报告验证和缓存核对结果。

## 接口

`main()` 使用骨架的 CFG 和 DATA_DIR。设置 CPU 单线程和 torch.manual_seed(CFG.seed)，以 UTF-8 读 pride.txt，建立 CharVocab、TextWindows、GPT、AdamW，然后调用 train_model。按 CFG.prompt、new_chars、temperature、top_k、seed 各运行一次无缓存和缓存生成，打印缓存路径解码的整段文字（含提示）。

## 示例

默认提示为 "It "，续写 90 个字符，所以打印的整段文字有 93 个字符，包含可能出现的换行。最后一个非空行是 JSON 对象，例如 `{"val_loss": 1.72, "cache_match": 1, "generated_chars": 90}`；示意数值以实跑为准。

## 约束

模型参数取自 CFG.context、width、heads、layers，优化器用 CFG.peak 和 CFG.decay。val_loss 取最后一次验证均值；cache_match 为实际比较两串完整编号所得的 0 或 1；generated_chars 只数新生成的字符。独立判题会替换为小配置；项目整跑使用骨架默认值。
