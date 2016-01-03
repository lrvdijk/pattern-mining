def generate_criteria(df, values):
    criteria = None
    for item in values:
        if criteria is None:
            criteria = df[item[1]] == item[0]
        else:
            criteria &= df[item[1]] == item[0]

    return criteria


def create_subdataframe(df, values):
    return df[generate_criteria(df, values)]
