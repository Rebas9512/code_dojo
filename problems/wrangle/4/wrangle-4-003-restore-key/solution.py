def rack_peaks(t):
    return t.groupby('rack').agg(peak=('n', 'max')).reset_index()
