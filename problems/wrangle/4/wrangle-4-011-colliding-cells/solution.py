import pandas as pd
t = pd.DataFrame({"r":["A","A","B"], "s":["am","am","pm"], "n":[3,5,2]})
p = t.pivot_table(index="r", columns="s", values="n", aggfunc="sum", fill_value=0)
print(p.loc["A","am"])
print(p.loc["A","pm"])
