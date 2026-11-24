def reader_counts(users, order_counts):
    readers = users[['user_id']].merge(order_counts, on='user_id', how='left')
    readers['order_count'] = readers['n'].fillna(0).astype('Int64')
    return readers[['user_id', 'order_count']]
