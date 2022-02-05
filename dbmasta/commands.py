# standard imports
from argparse import ArgumentParser
import pathlib as pl
from typing import List
import json

# external imports
import typer # using for quick build of cli prototype

# project imports


#################################
## Module level variables
#################################
app = typer.Typer()
pack_folder = pl.Path().cwd().joinpath("packages")

manifest_template = {}

#################################
## Module level functions
#################################
def package_exists(
    packagename: str,
    raise_error_on_exists: bool=False,
    raise_error_on_not_exist: bool=True
) -> bool:
    """
    Checks if a given package exists. Defaults to error if package is not present.
    """
    package_exists = pack_folder.joinpath(packagename).exists()
    if package_exists and raise_error_on_exists:
        raise FileExistsError(
            f"A package with the name {packagename} already exists at {pack_folder.joinpath(packagename)}."
        )
    elif (not package_exists) and (raise_error_on_not_exist):
        raise FileExistsError(
            f"A package with the name {packagename} does not exist at {pack_folder.joinpath(packagename)}."
        )
    return package_exists

def list_migrations(
    packagename: str
) -> list:
    """
    list_mgrations reads a package and returns a list of all the migrations
    """
    return [f for f in pack_folder.joinpath(packagename).iterdir() if f.suffix == ".sql"]

def find_latest_migration(
    migration_list: List[pl.Path]
) -> str:
    """
    Parses migration files and finds version number to return the latest as a string.
    
    Assumes migration filename convention of:
    ####-<migration_name>.sql
    """
    if migration_list == []:
        return "0001"
    else:
        return str(migration_list[-1].name)[0:4]

#################################
## CLI Commands
#################################
@app.command()
def createpackage(
    packagename: str,
    dbtype: str,
    environments: str="dev,qa,uat,prod"
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
    package_exists(packagename=packagename, raise_error_on_exists=True)

    # initialize package folder
    pack_folder.joinpath(packagename).mkdir()
    pack_path = pack_folder.joinpath(packagename)
    with open(pack_path.joinpath("__init__.py"), "w") as f:
        f.write("# auto generated package initializer")
    
    # initialize package manifest
    env_list = environments.split(",")
    manifest_template["environments"] = env_list
    for e in env_list:
        manifest_template[e] = {
            "connection": {},
            "migrations": []
        }
    with open(pack_path.joinpath("manifest.json"), "w") as f:
        json.dump(manifest_template, f, indent=4)


@app.command()
def createmigration(
    migrationname: str,
    packagename: str
):
    """
    createmigration initializes a .sql module for a migration
    """
    typer.echo(f"Creating {migrationname} in {packagename} package...")
    # check if package exists
    package_exists(packagename=packagename)
    # TODO read migration numbers and increment +1 to incoming migration
    typer.echo("Found following migrations:")
    current_migrations = list_migrations(packagename=packagename)
    typer.echo(current_migrations)
    latest_migr = find_latest_migration(migration_list=current_migrations)
    typer.echo(f"Latest migration is: {latest_migr}")
    # TODO initialize SQL file


if __name__ == "__main__":
    app()