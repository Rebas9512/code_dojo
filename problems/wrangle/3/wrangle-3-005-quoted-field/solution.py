from io import StringIO

import pandas as pd
text = 'id,title\n1,"A,B"\n2,C\n'
print(pd.read_csv(StringIO(text)).shape)
