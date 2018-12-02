import glob
import argparse

import pandas as pd
import tabulate


def main():
    """Report on club names not matching entries file.
    """
    parser = argparse.ArgumentParser(description="Report on club names "
                                                 "not matching entries file")
    parser.add_argument('year', type=int, help="the year to report")
    args = parser.parse_args()

    df = pd.concat([pd.read_csv(fn, dtype=str)
                    for fn in glob.glob("data/ident/people/%s/*.csv" % args.year)])
    df = df[~df['entry.name'].isnull() & (df['entry.name']!="all") &
            (df['entry.name']!="#umpire")]
    df = df[df['source'].str.startswith("minoraverages")]
    df['source'] = df['source'].str.split("/").str[-1]
    df.rename(inplace=True, columns={'league.name': 'league.name.full'})
    
    entries = pd.read_csv("data/ident/entries/%s.csv" % args.year,
                          dtype=str)

    df = pd.merge(df, entries, how='left',
                  on=['league.year', 'league.name.full', 'entry.name'])
    unmatched = df[df['entry.key'].isnull()]
    print "Records with no match on entries list:"
    print tabulate.tabulate(unmatched[['source', 'league.name.full',
                            'person.ref', 'person.name.last', 'entry.name']],
                            showindex=False)
    

if __name__ == '__main__':
    main()
    
