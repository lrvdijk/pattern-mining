"""
:mod:`dbdm.itemsets` - Generate itemsets from the dataframe
===========================================================
"""


def namedtuple_iteritems(nt):
    for f in nt._fields:
        yield (getattr(nt, f), f)


def generator(df):
    return (
        tuple(namedtuple_iteritems(v)) for v in df.itertuples(index=False)
    )
