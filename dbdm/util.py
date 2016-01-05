import pandas as pd


def generate_criteria(df, values):
    """
    :param df:
    :type df: pd.DataFrame
    :param values:
    :type values:
    :return:
    :rtype:
    """
    criteria = None
    for item in values:
        if criteria is None:
            criteria = df[item[1]] == item[0]
        else:
            criteria &= df[item[1]] == item[0]

    return criteria


def create_subdataframe(df, values):
    return df[generate_criteria(df, values)]


def format_rule(a, b):
    return "{{{a}}} => {{{b}}}".format(
        a=", ".join("{1}: {0}".format(*v) for v in a),
        b=", ".join("{1}: {0}".format(*v) for v in b)
    )
