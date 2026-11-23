import torch
import math

def check_function(args, expected, fn):
    scores, labels, width = args
    class Scores(torch.nn.Module):
        def forward(self, x):
            assert not self.training and not torch.is_grad_enabled(), "统计指标时用 eval 和 no_grad"
            return x
    x, y = torch.tensor(scores), torch.tensor(labels)
    batches = [(x[i:i+width],y[i:i+width]) for i in range(0,len(y),width)]
    wanted = sum(row.index(max(row)) == label for row,label in zip(scores,labels)) / len(y) if labels else 0.
    assert math.isclose(fn(Scores(), batches), wanted, abs_tol=1e-7), "按样本累计命中数和样本数，再做一次除法"
    return True
