import glob

import pandas as pd
import tabulate


def main(year):
    """Report on club names not matching entries file.
    """
    df = pd.concat([pd.read_csv(fn, dtype=str)
                    for fn in glob.glob("data/ident/people/%s/*.csv" % year)])
    df = df[~df['entry.name'].isnull() & (df['entry.name'] != "all") &
            (df['entry.name'] != "#umpire")]
    df = df[df['source'].str.startswith("minoraverages") |
            df['source'].str.startswith("boxscores")]
    df['source'] = df['source'].str.split("/").str[-1]
    df.rename(inplace=True, columns={'league.name': 'league.name.full'})

    entries = pd.read_csv("data/ident/entries/%s.csv" % year,
                          dtype=str)

    df = pd.merge(df, entries, how='left',
                  on=['league.year', 'league.name.full', 'entry.name'])
    unmatched = df[df['entry.key'].isnull()]
    print("Records with no match on entries list:")
    print(tabulate.tabulate(unmatched[['source', 'league.name.full',
                            'person.ref', 'person.name.last', 'entry.name']],
                            showindex=False))
