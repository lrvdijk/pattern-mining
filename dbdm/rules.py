import itertools

from dbdm import fp_growth, measures, itemsets


def generate_association_rules(df, min_support=10, min_conf=70):
    min_support_count = int(((len(df) * min_support) / 100) + 0.5)

    iter = fp_growth.find_frequent_itemsets(itemsets.generator(df),
                                            min_support_count,
                                            include_support=True)
    for itemset in iter:
        for rule in generate_rules(df, itemset, min_conf):
            yield rule


def non_empty_subsets(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(1, len(s))
    )


def generate_rules(df, pattern, min_conf=70):
    itemtuple, support = pattern

    if len(itemtuple) < 2:
        return

    itemset = set(itemtuple)
    for subset in non_empty_subsets(itemset):
        subset = set(subset)

        b = itemset - subset
        confidence = measures.confidence(df, subset, b, {'ab': support}) * 100

        if confidence >= min_conf:
            yield (subset, b)
