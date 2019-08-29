import click

from . import people
from . import games
from . import coverage
from . import lint
from . import tidy


@click.group()
def cli():
    pass


@cli.command("update")
def do_update():
    people.main()
    games.main()


@cli.command("coverage")
@click.argument('year', type=int)
def do_coverage(year):
    coverage.main(year)


@cli.command("lint")
@click.argument('year', type=int)
def do_lint(year):
    lint.main(year)


@cli.command("tidy")
def do_tidy():
    tidy.main()
