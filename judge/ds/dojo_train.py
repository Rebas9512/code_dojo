"""固定种子的小批次训练。题目提供模型、数据、损失函数和优化器工厂。"""

from contextlib import contextmanager
from copy import deepcopy
from math import isfinite
import random
from statistics import mean

import numpy as np
import torch

from dojo_compare import allclose


def tensor_storage(batch):
    """同一张量的切片可能是不同对象，但共享底层存储。"""
    if isinstance(batch, torch.Tensor):
        if batch.numel():
            yield batch.untyped_storage().data_ptr()
    elif isinstance(batch, (list, tuple, dict)):
        for element in (batch.values() if isinstance(batch, dict) else batch):
            yield from tensor_storage(element)


class TrainingData:
    def __init__(self, train, valid, loss_fn):
        self.train = train
        self._valid = deepcopy(valid)
        self._valid_storage = set(tensor_storage(self._valid))
        self._loss_fn = loss_fn
        self.in_eval = False
        self.read_valid = False
        self.evaluated = False
        self.cleared = False
        self.backward_loss = None
        self.losses = []

    @property
    def step_number(self):
        return len(self.losses) + 1

    @contextmanager
    def evaluating(self):
        """标记验证阶段，学生在其中负责切换模型模式和梯度开关。"""
        self.in_eval = True
        self.read_valid = False
        try:
            yield
        finally:
            self.in_eval = False

    @property
    def valid(self):
        if not self.in_eval:
            raise AssertionError(f"训练阶段访问了验证集（第 {self.step_number} 步），请用 data.train")
        self.read_valid = True
        return self._valid

    def check_split(self, values):
        if not self.in_eval and not self._valid_storage.isdisjoint(tensor_storage(values)):
            raise AssertionError(f"第 {self.step_number} 步使用了验证集的张量，请用训练集更新参数")

    def before_forward(self, model, args, kwargs):
        self.check_split((args, kwargs))
        if self.in_eval:
            if model.training:
                raise AssertionError("评估时模型仍在训练模式，请先调用 model.eval()")
            if torch.is_grad_enabled():
                raise AssertionError("评估时仍在记录梯度，请在 torch.no_grad() 中运行模型")
            self.evaluated |= self.read_valid
        elif not model.training:
            raise AssertionError(f"第 {self.step_number} 步仍在评估模式，请先调用 model.train()")

    def loss(self, prediction, target):
        self.check_split(target)
        loss = self._loss_fn(prediction, target)
        if not self.in_eval and loss.requires_grad:
            def on_backward(gradient):
                if not self.cleared:
                    raise AssertionError(f"第 {self.step_number} 步没有在 backward 之前清梯度，每步要先调用 zero_grad()")
                if self.backward_loss is not None:
                    raise AssertionError(f"第 {self.step_number} 步重复反向传播，梯度在累加")
                self.backward_loss = float(loss.detach())

            loss.register_hook(on_backward)
        return loss

    def clear(self):
        if self.backward_loss is not None:
            raise AssertionError(f"第 {self.step_number} 步在 backward 之后清了梯度，应先清梯度再反向传播")
        self.cleared = True


class TracedOptimizer:
    def __init__(self, optimizer, data):
        self.optimizer = optimizer
        self.data = data

    def __getattr__(self, name):
        return getattr(self.optimizer, name)

    def zero_grad(self, *args, **kwargs):
        self.data.clear()
        return self.optimizer.zero_grad(*args, **kwargs)

    def step(self):
        data = self.data
        if data.in_eval:
            raise AssertionError("评估阶段不能更新参数")
        if data.backward_loss is None:
            raise AssertionError(f"第 {data.step_number} 步更新前没有对 data.loss 的结果调用 backward()")
        if not isfinite(data.backward_loss):
            raise AssertionError(f"第 {data.step_number} 步的 loss 不是有限数")
        result = self.optimizer.step()
        data.losses.append(data.backward_loss)
        data.backward_loss = None
        data.cleared = False
        return result


def simulate_train(train, make_model, make_data, make_optimizer, loss_fn, *, steps, seed=0, require_eval=False):
    if steps < 1:
        raise ValueError("训练步数必须为正")
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    model = make_model()
    train_batch, valid_batch = make_data()
    data = TrainingData(train_batch, valid_batch, loss_fn)
    optimizer = TracedOptimizer(make_optimizer(model.parameters()), data)
    original_zero = model.zero_grad

    def zero_grad(*args, **kwargs):
        data.clear()
        return original_zero(*args, **kwargs)

    model.zero_grad = zero_grad
    try:
        with model.register_forward_pre_hook(data.before_forward, with_kwargs=True):
            train(model, data, optimizer, steps)
    finally:
        model.zero_grad = original_zero
    if len(data.losses) != steps or data.backward_loss is not None:
        raise AssertionError(f"要求完成 {steps} 次参数更新，实际完成 {len(data.losses)} 次，最后一次反向传播应配对更新")
    if require_eval and not data.evaluated:
        raise AssertionError("请在 data.evaluating() 中读取验证集，并用模型完成一次评估")
    return data.losses


def _finite(losses):
    if not losses or not all(isfinite(value) for value in losses):
        raise AssertionError("loss 序列必须非空，且每一步都是有限数")


def assert_loss_decreased(losses, *, window=10, ratio=0.5):
    _finite(losses)
    if window < 1 or len(losses) < 2 * window:
        raise AssertionError(f"比较首尾均值需要两个不重叠的窗口，每个窗口 {window} 步")
    first, last = mean(losses[:window]), mean(losses[-window:])
    if last >= ratio * first:
        raise AssertionError(f"loss 下降不足：前 {window} 步均值 {first:.5g}，后 {window} 步均值 {last:.5g}")


def assert_overfit(losses, *, atol=1e-3):
    _finite(losses)
    if abs(losses[-1]) > atol:
        raise AssertionError(f"小批次尚未拟合：最后一步 loss 为 {losses[-1]:.5g}，要求距离 0 不超过 {atol}")


def assert_trajectory(losses, reference, *, rtol=1e-5, atol=1e-8):
    _finite(losses)
    _finite(reference)
    reason = allclose(reference, losses, rtol=rtol, atol=atol)
    if reason:
        raise AssertionError(f"loss 轨迹与参考实现不同。{reason}")
