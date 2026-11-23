from io import BytesIO
import torch

def check_function(args, expected, fn):
    torch.manual_seed(args[0])
    model = torch.nn.Linear(2, 2)
    wanted = {k:v.clone() for k,v in model.state_dict().items()}
    buf = fn(model)
    assert isinstance(buf, BytesIO) and buf.tell() == 0, "请返回已回到开头的 BytesIO"
    with torch.no_grad():
        model.weight.zero_()
    saved = torch.load(buf, weights_only=True)
    assert saved.keys() == wanted.keys() and all(torch.equal(saved[k],v) for k,v in wanted.items()), "快照应包含写入时的全部参数"
    return True
