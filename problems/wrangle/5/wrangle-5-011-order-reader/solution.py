def order_names(orders, users):
    matched = orders.merge(users, on='user_id', how='inner')
    return matched[['order_id', 'name']]
