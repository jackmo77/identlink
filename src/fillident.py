"""This utility fills out nulls in the ident column by copying down
the last non-null value above.

This is useful for speeding up manual entry of idents.  As the typical case
is there are many consecutive rows referring to the same person, one can
fill in the ident for the first row referring to the person, and then use
this tool to copy that ident down to the remaining rows.

Obviously, this should be used with some care, as it is important that the
first row for each person does have an ident entered.  Cases where there are
multiple people with the same surname do still need to be handled manually,
as those records may be intermingled in the sort.
"""

import pandas as pd

if __name__ == '__main__':
    import sys

    fn = sys.argv[1]
    df = pd.read_csv(fn, dtype=str, encoding='utf-8')
    df['ident'] = df['ident'].fillna(method='pad')
    df.to_csv(fn, index=False, encoding='utf-8')
    
