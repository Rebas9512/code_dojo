def reader_counts(users, order_counts):
    out = users.merge(order_counts, on='user_id', how='left')
    out['order_count'] = out['n'].fillna(0).astype('Int64')
    return out[['user_id', 'order_count']]
