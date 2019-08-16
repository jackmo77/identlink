from __future__ import print_function
import glob

import pandas as pd

def main(year):
    """Report on coverage of idents for records by year.
    """
    for fn in sorted(glob.glob("data/ident/people/%s/*.csv" % year)):
        df = pd.read_csv(fn, dtype=str)
        league = df['league.name'].unique()[0]

        print("%4d/%4d %5.1f%% %s %s" % \
              (len(df[~df['ident'].isnull()]), len(df),
               100.0 * len(df[~df['ident'].isnull()]) / len(df),
               year, league))
