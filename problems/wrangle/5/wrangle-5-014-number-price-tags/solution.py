import pandas as pd
shelf = pd.DataFrame({"book_id":[5,2,8], "price":[39,39,45]})
s = shelf.sort_values("book_id")
s["position"] = s["price"].rank(method="first", ascending=False, na_option="bottom")
print(s["book_id"].tolist())
print(s["position"].tolist())
