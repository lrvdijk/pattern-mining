import pandas as pd
import numpy as np

NUMERIC_DATATYPES = [
    'int16', 'int32', 'int64', 'float16', 'float32', 'float64'
]


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

        if df.dtypes[item[1]] in NUMERIC_DATATYPES:
            criteria |= df[item[1]].apply(np.isnan)

    return criteria


def create_subdataframe(df, values):
    return df[generate_criteria(df, values)]


def format_rule(a, b):
    return "{{{a}}} => {{{b}}}".format(
        a=", ".join("{1}: {0}".format(*v) for v in a),
        b=", ".join("{1}: {0}".format(*v) for v in b)
    )
