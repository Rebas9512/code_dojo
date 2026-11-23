def top_up(t, shelf):
    hit = t['shelf'] == shelf
    t.loc[hit, 'n'] = t.loc[hit, 'n'] * 2
    return t.sort_values(['n', 'shelf'])
