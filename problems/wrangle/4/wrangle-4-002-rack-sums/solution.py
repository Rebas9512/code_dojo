def rack_totals(t):
    return t.groupby('rack', as_index=False).agg(total=('n', 'sum'))
