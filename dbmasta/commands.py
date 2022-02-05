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
    typer.echo(f"Creating {migrationname} in {packagename} package...")
    # check if package exists
    package_exists(packagename=packagename)
    # TODO read package numbers and increment +1 to incoming migration
    # TODO initialize SQL file


if __name__ == "__main__":
    app()