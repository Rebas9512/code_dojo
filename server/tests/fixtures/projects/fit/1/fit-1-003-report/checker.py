import io
import json
from contextlib import redirect_stdout


def check_function(args, expected, fn):
    output = io.StringIO()
    with redirect_stdout(output):
        fn(*args)
    lines = output.getvalue().splitlines()
    return lines[0] == "fitted" and json.loads(lines[-1])["slope"] == fit(*args) == expected
