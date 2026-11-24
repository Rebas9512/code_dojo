import io
import json
import math
import sys
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import numpy as np
import torch


def check_function(args, expected, fn):
    epochs, seed, batch_size, patience, kind = args
    with TemporaryDirectory(dir=".") as work:
        directory = Path(work).resolve()
        rows = np.loadtxt(DATA_DIR / "digits.csv", delimiter=",", skiprows=1, max_rows=41, dtype=int)
        if kind == "zeros":
            rows.fill(0)
        header = ",".join([f"p{i}" for i in range(64)] + ["label"])
        np.savetxt(directory / "digits.csv", rows, fmt="%d", delimiter=",", header=header, comments="")
        path = directory / "saved.pt"
        argv = ["train.py", "--epochs", str(epochs), "--checkpoint", str(path)]
        # 第一例只覆盖轮数与输出位置，检验其余默认设置。
        if epochs != 1:
            argv.extend(["--seed", str(seed), "--batch-size", str(batch_size), "--patience", str(patience)])
        measured = []

        def measure(model, loader):
            accuracy = evaluate(model, loader)
            measured.append({name: value.clone() for name, value in model.state_dict().items()})
            return accuracy

        output = io.StringIO()
        setting = {"DATA_DIR": directory, "evaluate": measure}
        with patch.object(sys, "argv", argv), patch.dict(fn.__globals__, setting), redirect_stdout(output):
            fn()
        lines = [json.loads(line) for line in output.getvalue().splitlines()]
        assert path.is_file(), "请将最佳检查点写到 --checkpoint 指定的位置"
        saved = torch.load(path, weights_only=True)

        config = Config(seed=seed, batch_size=batch_size, epochs=epochs, patience=patience)
        config.set_seed()
        dataset = DigitsDataset(directory / "digits.csv")
        train, valid = make_loaders(dataset, round(0.2 * len(dataset)), batch_size, seed)
        model = build_model(config.hidden_size)
        optimizer, scheduler = make_optimizer(model, config)
        best = -1.0
        best_epoch = 0
        for epoch in range(1, epochs + 1):
            lr = optimizer.param_groups[0]["lr"]
            loss = train_one_epoch(model, train, optimizer, torch.nn.CrossEntropyLoss(), config.max_norm)
            accuracy = evaluate(model, valid)
            assert epoch < len(lines), "每个实际训练轮应输出一行日志，最后还要有一行汇总"
            record = lines[epoch - 1]
            assert record["epoch"] == epoch and math.isclose(record["lr"], lr), "日志需要本轮轮号及更新前的学习率"
            assert math.isclose(record["loss"], loss, rel_tol=1e-5, abs_tol=1e-7), "损失偏离同种子参考训练，请检查配置和数据划分"
            assert math.isclose(record["val_accuracy"], accuracy), "每轮日志需要该轮在验证集上的准确率"
            scheduler.step()
            if accuracy > best:
                best, best_epoch = accuracy, epoch
                best_weights = {k: v.clone() for k, v in model.state_dict().items()}
                best_lr = optimizer.param_groups[0]["lr"]
            if epoch - best_epoch == patience:
                break
        assert len(lines) == epoch + 1, "到达轮数上限或早停轮后只再输出一行最终指标"
        assert lines[-1]["best_epoch"] == saved["epoch"] == best_epoch, "总结和检查点的轮号应为首次最佳轮"
        assert math.isclose(lines[-1]["val_accuracy"], best), "最终指标需要恢复最佳权重后重新验证"
        assert len(measured) == epoch + 1, "每轮验证一次，恢复权重后还要再验证一次"
        for name, value in best_weights.items():
            assert torch.allclose(measured[-1][name], value, atol=1e-6), "最后一次验证应使用已恢复的最佳权重"
            assert torch.allclose(saved["model"][name], value, atol=1e-6), "检查点的参数应属于最佳轮"
        assert math.isclose(saved["optimizer"]["param_groups"][0]["lr"], best_lr), "请在轮末调度后保存，保留下一轮的步长"
    return True
