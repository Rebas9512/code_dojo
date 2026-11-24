def top_up(t, shelf):
    selected = t['shelf'] == shelf
    t.loc[selected, 'n'] *= 2
    return t.sort_values(['n', 'shelf'])
