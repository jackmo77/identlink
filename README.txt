Identity linking files for historical baseball data
Maintained by T L Turocy (ted.turocy@gmail.com)
              Chadwick Baseball Bureau (http://www.chadwick-bureau.com)
              
This repository contains files which support records matching and linking across
other source datasets.

At present, the only records included in these files are those from the
minoraverages repository (http://www.github.com/chadwickbureau/minoraverages).
This uses a blocking scheme at the level of an individual league-season.
Each league-season corresponds to one CSV file under leagues/.  Columns in the
file include:
* source: source of the record
* league.year: league-season year
* league.name: league-season name
* ident: identity tag (see explanation below)
* person.ref: person identifier from source
* person.name.last: last name of person
* person.name.given: given name of person
* entry.name: name of the team ("entry") in the league person is associated with

The ident column is used to establish the linking of records.  Records tagged with
the same ident value are deemed to refer to the same person (and therefore should
be grouped for subsequent processing).

Ident tags are arbitrary strings, but we recommend certain conventions:
* use only lowercase letters [a-z], dashes, periods, and plus signs.
* if a person's last name is unique within the league season, use it (removing any
  spaces, apostrophes, or dashes)
* if there are two or more people with the same last name, disambiguate by one or
  more of the following:
** add a dash plus an abbreviation of the team associated with
** add a period plus a first initial or name
** add a plus sign plus a position abbreviation.

For example:
* If there is just one person named Smith, use 'smith'.
* If there is a John Smith and a William Smith, use 'smith.j' and 'smith.w'
* If there is a Smith on Springfield and a Smith on Greenville, use 'smith-spr'
  and 'smith-gre'
* If there are two Smiths on Springfield, neither of whom has a known first name,
  but one is a pitcher and one a shortstop, use 'smith+p-spr' and 'smith+ss-spr'
  
These are only examples.  Ident names are completely arbitrary; disambiguation can be
done in whatever way seems to be the most sensible in the particular circumstance.

The blocking scheme treats ident names in different league-seasons as being different
labels.  So, the ident tag 'smith' in the (hypothetical) 1946 Universal League is
not necessarily the same as the ident tag 'smith' in the 1947 Universal League, or
the 1946 Federal Association, or any other league-season.  The task of linking
people across their activities in different league-seasons is accomplished by different,
complementary blocking schemes.

Over time, new records associated with a league-season will be added to the system.
Ident names for record groups should not be changed arbitrarily.  If there is an ident
tag 'smith' in place, and a new record should be added to that group, then continue to
use 'smith'.  However, if a new person named Smith should be identified (or it is
realised that the records previously collected under one Smith should be separated into
two ident groups), then the ident names can be changed.  Ideally, in such a case,
'smith' would *not* be used, and two new ident names would be used to distinguish the
two groups.

CONTRIBUTING:

Any entries in these files which have null values in the ident column are unlinked
records.  Anyone can contribute to the identification of records by filling in the
ident column with proposed ident tags, following the conventions outlined above.
The CSV files can most easily be loaded into a spreadsheet (Excel, OpenOffice, etc.)
and edited there.  The files include additional useful information, like games by
position, which can be used to unpick hairy situations.  For example, Guides often
did not bother to list initials for two players with the same surname on the same
club, if they played different positions and therefore could be distinguished by
e.g. number of games played, or if one was a position and another a position player.

There is a utility file, src/tidycsv.py, which can be used to create a canonical
CSV representation of a file after it has been edited in Excel or another tool.
 