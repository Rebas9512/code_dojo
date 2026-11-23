import pandas as pd
t = pd.DataFrame({"id":[1,2], "a":[4,5], "b":[6,7], "c":[1,0]})
print(t.melt(id_vars="id").shape)
