import json
import math
from types import SimpleNamespace

import torch
from torch import nn
from torch.nn import functional as F


CFG = SimpleNamespace(
    seed=42, context=96, width=96, heads=4, layers=3,
    steps=960, batch_size=12, warmup=20, peak=0.003, floor=0.0003,
    decay=0.05, clip=1.0, eval_every=240, eval_batches=6,
    prompt="It ", new_chars=90, temperature=0.75, top_k=12,
)


# @part llm-6-001-vocab


# @part llm-6-002-windows


# @part llm-6-003-attention


# @part llm-6-004-mlp


# @part llm-6-005-block


# @part llm-6-006-gpt


# @part llm-6-007-adamw


# @part llm-6-008-schedule


# @part llm-6-009-train


# @part llm-6-010-sample


# @part llm-6-011-generate


# @part llm-6-012-main
