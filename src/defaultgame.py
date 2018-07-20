"""Creates a set of default game idents based on date, number, and
first three characters of home team name.
"""

import sys
import pandas as pd

def main():
    for fn in sys.argv[1:]:
        print fn
        df = pd.read_csv(fn, encoding='utf-8', dtype='str')
        df['ident'] = df['ident'].fillna(df['game.date'].str[-4:] + \
                                         df['home.name'].str.replace(" ", "").str[:3].str.lower() + \
                                         df['game.number'].replace({"0": ""}))
        df.to_csv(fn, encoding='utf-8', index=False)
                                    


if __name__ == '__main__':
    main()
