import pandas as pd
books = pd.DataFrame({"category":["kids","scifi","kids"], "book_id":[6,2,14]})
g = books.groupby("category").agg(book_count=("book_id","size")).reset_index()
print(g["category"].tolist())
print(g["book_count"].tolist())
