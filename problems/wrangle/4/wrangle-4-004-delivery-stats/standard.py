def delivery_stats(t):
    t['n'] = t['n'].astype('Int64')
    return t.groupby('rack', as_index=False).agg(batches=('n', 'size'), total=('n', 'sum'))
