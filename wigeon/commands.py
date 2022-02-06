# standard imports
from argparse import ArgumentParser
import pathlib as pl
from typing import List
import json

# external imports
import typer # using for quick build of cli prototype

# project imports
from wigeon.packages import Package
from wigeon.dboperations import Connection

#################################
## Module level variables
#################################
app = typer.Typer()


#################################
## Module level functions
#################################



#################################
## CLI Commands
#################################
@app.command()
def createpackage(
    packagename: str,
    dbtype: str,
    environments: str="local,dev,qa,prod"
):
    """
    createpackage initializes a package of migrations in the current
    environment. A package is linked directly to a database type and the
    deployment environments in your ci/cd pipeline.
    """
    typer.echo(f"Creating {packagename} package")
    typer.echo(f"{packagename}'s Database type is {dbtype}")
    typer.echo(f"{packagename}'s environments include {environments.split(',')}")
     # check if package exists
    package = Package(packagename=packagename)
    package.exists(
        packagename=packagename,
        raise_error_on_exists=True,
        raise_error_on_not_exist=False
    )

    # initialize package folder
    package.create(
        env_list=environments.split(","),
        db_engine=dbtype
    )


@app.command()
def createmigration(
    migrationname: str,
    packagename: str,
    build: str
):
    """
    createmigration initializes a .sql module for a migration
    """
    typer.echo(f"Creating {migrationname} in {packagename} package...")
    # check if package exists
    package = Package(packagename=packagename)
    package.exists(packagename=packagename)
    # find latest migration number
    current_migrations = package.list_migrations(packagename=packagename)
    current_migr_num = package.find_current_migration(migration_list=current_migrations)
    typer.echo(f"Current migration is: {current_migr_num}")
    # create migration
    package.add_migration(
        current_migration=current_migr_num,
        migration_name=migrationname,
        builds=[build] # TODO enable multiple build support at later date
    )
    typer.echo(f"Successfully created {current_migr_num}-{migrationname}.sql!!")

@app.command()
def listmigrations(
    packagename: str
):
    """
    listmigrations lists out all migrations for a given package name
    """
    # check if package exists
    package = Package(packagename=packagename)
    package.exists(packagename=packagename)
    typer.echo(f"Found following migrations for {packagename}:")
    current_migrations = package.list_migrations(packagename=packagename)
    for m in sorted(current_migrations):
        typer.echo(f"    {m.name}")
    current_migr = package.find_current_migration(migration_list=current_migrations)
    typer.echo(f"Current migration would be: {current_migr}")

@app.command()
def connect(
    packagename: str,
    conn_string: str=None
):
    """
    connects to a database
    """
    # check if package exists
    package = Package(packagename=packagename)
    package.exists(packagename=packagename)
    # create connection, return cursor
    # TODO remove hardboded sqlite
    conn = Connection( db_engine="sqlite")
    cur = conn.connect(
        db_path=str(pl.Path().cwd().joinpath("exampledb.sqlite"))
    )
    typer.echo("Connected to a database!!!!")


if __name__ == "__main__":
    app()