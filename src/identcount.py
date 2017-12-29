import sys
import glob

import pandas as pd

def main():
    year = sys.argv[1]

    for fn in sorted(glob.glob("leagues/%s/*.csv" % year)):
        df = pd.read_csv(fn, dtype=str)
        league = df['league.name'].unique()[0]

        print "%4d/%4d %5.1f%% %s %s" % \
          (len(df[~df['ident'].isnull()]), len(df),
           100.0 * len(df[~df['ident'].isnull()]) / len(df),
           year, league)
    
if __name__ == '__main__':
    main()
