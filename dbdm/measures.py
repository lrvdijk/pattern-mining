import sys
import math

from dbdm import util

MEASURES = (
    'confidence',
    'lift',
    'kulczynski',
    'cosine',
    'all_confidence',
    'max_confidence',
    'imbalance_ratio'
)


def calculate_supports(df, a, b, supports=None, calculate=('a', 'b', 'ab')):
    if supports is None:
        supports = {}

    if 'a' not in supports and 'a' in calculate:
        supports['a'] = len(util.create_subdataframe(df, a))

    if 'b' not in supports and 'b' in calculate:
        supports['b'] = len(util.create_subdataframe(df, b))

    if 'ab' not in supports and 'ab' in calculate:
        supports['ab'] = len(util.create_subdataframe(df, a | b))

    return supports


def confidence(df, a=None, b=None, supports=None):
    if not (a and b) and not supports:
        raise ValueError("To calculate confidence need to have either "
                         "support values or the A => B item sets.")
    supports = calculate_supports(df, a, b, supports, calculate=('a', 'ab'))

    if supports['a'] == 0:
        return 0

    return supports['ab'] / supports['a']


def lift(df, a, b, supports=None):
    supports = calculate_supports(df, a, b, supports)

    if supports['a'] == 0 or supports['b'] == 0:
        return 0

    return supports['ab'] / (supports['a'] * supports['b'])


def kulczynski(df, a, b, supports):
    supports1 = calculate_supports(df, a, b, supports)

    supports.pop('a')
    supports.pop('b')
    supports2 = calculate_supports(df, b, a, supports)

    return 0.5 * (
        confidence(df, a, supports=supports1) +
        confidence(df, b, supports=supports2)
    )


def cosine(df, a, b, supports):
    supports = calculate_supports(df, a, b, supports)

    if supports['a'] == 0 or supports['b'] == 0:
        return 0

    return supports['ab'] / math.sqrt(supports['a'] * supports['b'])


def all_confidence(df, a, b, supports):
    supports = calculate_supports(df, a, b, supports)

    return supports['ab'] / max(supports['a'], supports['b'])


def max_confidence(df, a, b, supports):
    supports = calculate_supports(df, a, b, supports)

    return max(confidence(df, a, b, supports), confidence(df, a, b, supports))


def imbalance_ratio(df, a, b, supports):
    supports = calculate_supports(df, a, b, supports)

    return abs(supports['a'] - supports['b']) / (
        supports['a'] + supports['b'] - supports['ab']
    )


def calculate(df, a, b, supports, measures=MEASURES):
    module = sys.modules[__name__]
    return {
        measure: getattr(module, measure)(df, a, b, supports)
        for measure in measures
    }
