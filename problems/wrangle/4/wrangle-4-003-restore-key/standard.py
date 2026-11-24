def rack_peaks(t):
    return t.groupby('rack', as_index=False).agg(peak=('n', 'max'))
