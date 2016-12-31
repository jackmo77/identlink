import pandas as pd

def collect_from_averages(path):
    """Collect playing and managing performance records from
    minoraverages repository.
    """
    print "Collecting items from minoraverages dataset."
    dflist = [ ]
    for sourcepath in glob.glob("%s/processed/*" % path):
        source = sourcepath.split("/")[-1]
        print "Collecting source %s" % source
        
        dflist.append(pd.read_csv("%s/playing_individual.csv" % sourcepath,
                                  dtype=str))
        dflist[-1]['source'] = "minoraverages/%s" % source

        try:
            dflist.append(pd.read_csv("%s/managing_individual.csv" % sourcepath,
                                      dtype=str))
            dflist[-1]['source'] = "minoraverages/%s" % source
        except IOError:
            print "  Warning: did not find managers file"
    print
    return dflist

def collect_from_boxscores(path):
    """Collect people entries from boxscores repository.
    """
    print "Collecting items from boxscores dataset."
    dflist = [ ]
    for sourcepath in glob.glob("%s/processed/*/*" % path):
        source = "/".join(sourcepath.split("/")[-2:])
        print "Collecting source %s" % source

        try:
            dflist.append(pd.read_csv("%s/people.csv" % sourcepath,
                                      dtype=str))
            dflist[-1]['source'] = "boxscores/%s" % source
        except IOError:
            print "  Warning: did not find people file"
    print
    return dflist

if __name__ == '__main__':
    import sys
    import os
    import glob

    avglist = collect_from_averages("../minoraverages")
    boxlist = collect_from_boxscores("../boxscores")
    print "Concatenating files..."
    df = pd.concat(avglist + boxlist, ignore_index=True)

    idents = [ ]
    for identfile in glob.glob("leagues/*/*.csv"):
        print "Collecting identfile %s" % identfile
        idents.append(pd.read_csv(identfile, dtype=str))
    print
    if len(idents) > 0:
        idents = pd.concat(idents, ignore_index=True)

        df['person.name.given'] = df['person.name.given'].fillna("")
        idents['person.name.given'] = idents['person.name.given'].fillna("")
        df['S_STINT'] = df['S_STINT'].fillna("")
        idents['S_STINT'] = idents['S_STINT'].fillna("")
    
        df = pd.merge(df,
                      idents[[ 'ident', 'source', 'league.year', 'league.name', 
                               'person.ref', 'person.name.last', 'person.name.given',
                               'S_STINT', 'entry.name' ]],
                      how='left',
                      on=[ 'source', 'league.year', 'league.name', 
                           'person.ref', 'person.name.last', 'person.name.given',
                           'S_STINT', 'entry.name' ])
    else:
        df['ident'] = None
    df = df[[ 'source', 'league.year', 'league.name', 'ident', 'person.ref',
              'person.name.last', 'person.name.given',
             'S_STINT', 'entry.name',
             'S_FIRST', 'S_LAST',
             'B_G', 'P_G', 'F_1B_G', 'F_2B_G', 'F_3B_G', 'F_SS_G',
             'F_OF_G', 'F_LF_G', 'F_CF_G', 'F_RF_G', 'F_C_G', 'F_P_G',
             'F_ALL_G' ]] 
    df.sort_values([ 'league.year', 'league.name',
                     'person.name.last', 'source', 'person.ref' ],
                   inplace=True)

    # We convert dates to YYYYMMDD. This way, ident files can be loaded
    # into e.g. Excel for editing, without messing up the formatting.
    # YYYYMMDD is considered a valid ISO date format as well.
    df['S_FIRST'] = df['S_FIRST'].str.replace("-", "")
    df['S_LAST'] = df['S_LAST'].str.replace("-", "")

    print "Writing ident files..."  
    for (group, data) in df.groupby([ 'league.year', 'league.name' ]):
        print group[0], group[1]
        try:
            os.makedirs("leagues/%s" % group[0])
        except os.error:
            pass
        data.to_csv("leagues/%s/%s%s.csv" % (group[0], group[0],
                                             group[1].replace(" ", "").replace("-", "")),
                    index=False)
