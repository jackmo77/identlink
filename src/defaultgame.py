"""Creates a set of default game idents based on date, number, and
first three characters of home team name.
"""

import sys
import pandas as pd

def main():
    replacechars = [" ", ".", "&", "-"]
    for fn in sys.argv[1:]:
        print fn
        df = pd.read_csv(fn, encoding='utf-8', dtype='str')
        team0 = df[['away.name', 'home.name']].min(axis=1).str.lower()
        team1 = df[['away.name', 'home.name']].max(axis=1).str.lower()
        for char in replacechars:
            team0 = team0.str.replace(char, "")
            team1 = team1.str.replace(char, "")
        
        ident = (df['game.date'].str[-4:] + "-" +
                 team0 + "-" + team1 + "-" + df['game.number'])
        df['ident'] = df['ident'].fillna(ident)
        df.to_csv(fn, encoding='utf-8', index=False)
                                    


if __name__ == '__main__':
    main()
