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

#################################
## CLI Commands
#################################
@app.command()
def createpackage(
    packagename: str,
    dbtype: str,
    environments: str="dev,qa,uat,prod"
):
    typer.echo(f"Creating {packagename} package")
    typer.echo(f"{packagename}'s Database type is {dbtype}")
    typer.echo(f"{packagename}'s environments include {environments.split(',')}")
     # check if package exists
    if pack_folder.joinpath(packagename).exists():
        raise FileExistsError(f"A package with the name {packagename} already exists at {pack_folder.joinpath(packagename)}.")

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
    # TODO read package numbers and increment +1 to incoming migration
    # TODO initialize SQL file


if __name__ == "__main__":
    app()