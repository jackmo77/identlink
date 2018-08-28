import glob

import pandas as pd



def main():
    seasons = pd.concat([pd.read_csv(fn, dtype=str)
                         for fn in glob.glob("seasons/*.csv")],
                        ignore_index=True)
    seasons.rename(inplace=True, columns={'league.name.full': 'league.name'})
    df = pd.concat([pd.read_csv(fn, dtype=str)
                    for fn in glob.glob("leagues/19[01]?/*.csv")],
                   ignore_index=True)
    df = df[df['source'].str.startswith("researchers")].copy()
    df = df[~df['ident'].isnull()].copy()
    df = pd.merge(df, seasons, how='left', on=['league.year', 'league.name'])
    df['mentions'] = df.groupby(['source', 'person.ref'])['league.key'].transform(lambda x: x.nunique())
    df = df[df['mentions']>=2].copy()
    df['ident'] = df['league.key']+":"+df['ident']
    df['person.ref'] = df['source']+":"+df['person.ref']
    df.sort_values(['person.name.last', 'person.name.given', 'person.ref',
                    'league.key'],
                   inplace=True)
    print df[['person.ref', 'ident', 'person.name.last', 'person.name.given']].drop_duplicates().to_string()


if __name__ == '__main__':
    main()
