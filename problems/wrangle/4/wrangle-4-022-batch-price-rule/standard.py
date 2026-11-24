def member_prices(t):
    t['member'] = t['price'] * 0.8 + 2
    averages = t.pivot_table(
        index='shop', columns='shift', values='member', aggfunc='mean', fill_value=0
    )
    return averages.reset_index()
