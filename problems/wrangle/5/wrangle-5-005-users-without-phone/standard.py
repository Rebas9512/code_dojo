def missing_phones(users):
    return users.loc[users['phone'].isna(), ['user_id', 'name']]
