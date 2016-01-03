import pandas as pd
import matplotlib.pyplot as plt
import seaborn

from dbdm import itemsets, rules, measures

seaborn.set()

MIN_SUPPORT = 10
MIN_CONFIDENCE = 80


df = pd.read_csv(
    "data/adult.data",
    engine='c',
    lineterminator='\n',

    names=['age', 'workclass', 'fnlwgt', 'education', 'education_num',
           'marital_status', 'occupation', 'relationship', 'race', 'sex',
           'capital_gain', 'capital_loss', 'hours_per_week',
           'native_country', 'income'],
    header=None,
    skipinitialspace=True,
    na_values="?"
)

# Remove fnlwgt column
df = df[['age', 'workclass', 'education', 'education_num', 'marital_status',
         'occupation', 'relationship', 'race', 'sex', 'capital_gain',
         'capital_loss', 'hours_per_week', 'native_country', 'income']]

df.describe()
df.describe(include=['O'])

df['education'].value_counts(sort=False).plot(kind='bar')

iter = rules.generate_association_rules(
        df[['workclass', 'education', 'marital_status',
            'occupation', 'relationship', 'sex',
            'income']],
        MIN_SUPPORT,
        MIN_CONFIDENCE
)

print("Frequent patterns")
for a, b in iter:
    supports = measures.calculate_supports(df, a, b)
    print(a, "=>", b)
    print(measures.calculate(df, a, b, supports))
    print()

print()

plt.show()
