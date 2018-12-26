"""Update person ident lists from source records.
"""
import os
import glob
import argparse

import pandas as pd

def collect_from_averages(path):
    """Collect playing and managing performance records from
    minoraverages repository.
    """
    print "Collecting items from minoraverages dataset."
    dflist = []
    for sourcepath in glob.glob("%s/processed/*" % path):
        source = sourcepath.split("/")[-1]
        print "Collecting source %s" % source
        dflist.append(pd.read_csv("%s/playing_individual.csv" % sourcepath,
                                  dtype=str, encoding='utf-8'))
        dflist[-1]['source'] = "minoraverages/%s" % source
        try:
            dflist.append(pd.read_csv("%s/managing_individual.csv" % sourcepath,
                                      dtype=str, encoding='utf-8'))
            dflist[-1]['source'] = "minoraverages/%s" % source
        except IOError:
            print "  Warning: did not find managers file"
    print
    return dflist

def collect_from_boxscores(path):
    """Collect people entries from boxscores repository.
    """
    print "Collecting items from boxscores dataset."
    dflist = []
    for sourcepath in glob.glob("%s/data/boxscores/processed/*/*" % path):
        source = "/".join(sourcepath.split("/")[-2:])
        print "Collecting source %s" % source

        try:
            dflist.append(pd.read_csv("%s/players.csv" % sourcepath,
                                      dtype=str, encoding='utf-8'))
            dflist[-1]['source'] = "boxscores/%s" % source
        except IOError:
            print "  Warning: did not find people file"
    print
    return dflist


def collect_umpires_from_boxscores(path):
    """Collect umpire entries from boxscores repository.
    """
    print "Collecting umpires from boxscores dataset."
    dflist = []
    for sourcepath in glob.glob("%s/data/boxscores/processed/*/*" % path):
        source = "/".join(sourcepath.split("/")[-2:])
        print "Collecting source %s" % source
        try:
            dflist.append(pd.read_csv("%s/umpires.csv" % sourcepath,
                                      dtype=str, encoding='utf-8'))
            dflist[-1]['source'] = "boxscores/%s" % source
            dflist[-1]['entry.name'] = "#umpire"
        except IOError:
            print "  Warning: did not find umpires file"
    print
    return dflist



def collect_from_retrosheet(path):
    """Collect playing entries from retrosplits repository.
    """
    print "Collecting items from retrosheet dataset."
    dflist = []
    lookup = pd.read_csv("support/retroteams.csv", dtype=str, encoding='utf-8')
    for year in range(1906, 1920):
        source = "retrosheet/%s" % year
        print "Collecting source %s" % source
        df = pd.read_csv("%s/retrosplits/daybyday/playing-%d.csv" % (path, year),
                         dtype=str, encoding='utf-8')
        df = df[['person.key', 'team.key', 'game.date']]
        df = df.groupby(['person.key', 'team.key']).aggregate(['min', 'max'])
        df.columns = ['S_FIRST', 'S_LAST']
        df.reset_index(inplace=True)
        df['league.year'] = df['S_FIRST'].str.split('-').str[0]
        df = pd.merge(df, lookup, how='left', on=['league.year', 'team.key'])
        df.rename(inplace=True, columns={'person.key':  'person.ref'})
        df['source'] = source

        rosters = pd.concat([pd.read_csv(fn, dtype=str, encoding='utf-8',
                                         header=None,
                                         names=['person.ref',
                                                'person.name.last',
                                                'person.name.given',
                                                'bats', 'throws',
                                                'team.key', 'pos'])
                             for fn in glob.glob("%s/retrosheet/rosters/*%s.ROS" %
                                                 (path, year))],
                            sort=False, ignore_index=True)
        df = pd.merge(df, rosters[['person.ref', 'team.key',
                                   'person.name.last', 'person.name.given']],
                      how='left', on=['person.ref', 'team.key'])
        dflist.append(df[['source', 'league.year', 'league.name',
                          'person.ref',
                          'person.name.last', 'person.name.given',
                          'entry.name', 'S_FIRST', 'S_LAST']].copy())
    return dflist

def collect_from_researchers(path):
    """Collect engagement records from researchers repository.
    """
    print "Collecting items from researchers dataset."
    df = pd.read_csv("%s/processed/clubs.csv" % path, encoding='utf-8',
                     dtype=str)
    df.rename(inplace=True,
              columns={'last':       'person.name.last',
                       'first':      'person.name.given',
                       'date':       'league.year',
                       'league':     'league.name',
                       'person':     'person.ref',
                       'club':       'entry.name'})
    df['source'] = 'researchers' + '/' + df['person.ref'].str.split("/").str[0]
    df['person.ref'] = df['person.ref'].str.split("/").str[1]
    df = df[~df['person.name.last'].isnull()].copy()
    return [df]

def main():
    """Update person ident lists from source records.
    """
    parser = argparse.ArgumentParser(description="Update person ident lists "
                                                 "from source records")
    parser.parse_args()

    retrolist = collect_from_retrosheet("..")
    avglist = collect_from_averages("../minoraverages")
    boxlist = collect_from_boxscores("../boxscores")
    umplist = collect_umpires_from_boxscores("../boxscores")
    reslist = collect_from_researchers("../researchers")
    print "Concatenating files..."
    df = pd.concat(retrolist + avglist + boxlist + umplist + reslist,
                   sort=False, ignore_index=True)

    # Fill in an indicator for records which indicate a position played
    # but not games at that position
    for pos in ["P", "C", "1B", "2B", "3B", "SS", "OF", "LF", "CF", "RF"]:
        if "F_%s_G" % pos in df and "F_%s_POS" % pos in df:
            df["F_%s_G" % pos] = df["F_%s_G" % pos] \
                                 .fillna(df["F_%s_POS" % pos] \
                                 .apply(lambda x:
                                        "yes" if not pd.isnull(x) and int(x) > 0
                                        else None))

    idents = []
    for identfile in glob.glob("data/ident/people/*/*.csv"):
        print "Collecting identfile %s" % identfile
        idents.append(pd.read_csv(identfile, dtype=str, encoding='utf-8'))
    print
    if idents:
        idents = pd.concat(idents, sort=False, ignore_index=True)

        df['person.name.given'] = df['person.name.given'].fillna("")
        idents['person.name.given'] = idents['person.name.given'].fillna("")
        df['S_STINT'] = df['S_STINT'].fillna("")
        idents['S_STINT'] = idents['S_STINT'].fillna("")
        df = pd.merge(df,
                      idents[['ident', 'source', 'league.year', 'league.name',
                              'person.ref', 'person.name.last', 'person.name.given',
                              'S_STINT', 'entry.name']],
                      how='left',
                      on=['source', 'league.year', 'league.name',
                          'person.ref', 'person.name.last', 'person.name.given',
                          'S_STINT', 'entry.name'])
    else:
        df['ident'] = None
    df = df[['source', 'league.year', 'league.name', 'ident', 'person.ref',
             'person.name.last', 'person.name.given',
             'S_STINT', 'entry.name',
             'S_FIRST', 'S_LAST',
             'B_G', 'P_G', 'F_1B_G', 'F_2B_G', 'F_3B_G', 'F_SS_G',
             'F_OF_G', 'F_LF_G', 'F_CF_G', 'F_RF_G', 'F_C_G', 'F_P_G',
             'F_ALL_G']]
    df.sort_values(['league.year', 'league.name',
                    'person.name.last', 'source', 'person.ref'],
                   inplace=True)

    # We convert dates to YYYYMMDD. This way, ident files can be loaded
    # into e.g. Excel for editing, without messing up the formatting.
    # YYYYMMDD is considered a valid ISO date format as well.
    df['S_FIRST'] = df['S_FIRST'].str.replace("-", "")
    df['S_LAST'] = df['S_LAST'].str.replace("-", "")

    print "Writing ident files..."
    for (group, data) in df.groupby(['league.year', 'league.name']):
        # We only generate ident files for leagues where we have
        # either an averages compilation or boxscore data
        sample = data[data['source'].str.startswith('retrosheet/') |
                      data['source'].str.startswith('minoraverages/') |
                      data['source'].str.startswith('boxscores/')]
        if sample.empty:
            continue
        print group[0], group[1]
        try:
            os.makedirs("data/ident/people/%s" % group[0])
        except os.error:
            pass
        data = data.drop_duplicates()
        data.to_csv("data/ident/people/%s/%s%s.csv" %
                    (group[0], group[0],
                     group[1].replace(" ", "").replace("-", "")),
                    index=False,
                    encoding='utf-8')


if __name__ == '__main__':
    main()
