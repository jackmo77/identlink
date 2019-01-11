import sys
import glob
import argparse

import pandas as pd

def main():
    """Report on coverage of idents for records by year.
    """
    parser = argparse.ArgumentParser(description="Report on ident coverage "
                                                 "by year")
    parser.add_argument('year', type=int, help="the year to report")
    args = parser.parse_args()

    for fn in sorted(glob.glob("data/ident/people/%s/*.csv" % args.year)):
        df = pd.read_csv(fn, dtype=str)
        league = df['league.name'].unique()[0]

        print("%4d/%4d %5.1f%% %s %s" % \
              (len(df[~df['ident'].isnull()]), len(df),
               100.0 * len(df[~df['ident'].isnull()]) / len(df),
               args.year, league))


if __name__ == '__main__':
    main()
