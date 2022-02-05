# standard imports
from argparse import ArgumentParser
import pathlib as pl
from typing import List

# external imports
import typer

# project imports



app = typer.Typer()

pack_path = pl.Path().cwd().joinpath("packages")

@app.command()
def createpackage(
    packagename: str,
    dbtype: str="sqlite"
):
    typer.echo(f"Creating {packagename} package")
    typer.echo(f"{packagename}'s Database type is {dbtype}")
     # check if package exists
    if pack_path.joinpath(packagename).exists:
        raise FileExistsError(f"A package with the name {packagename} already exists at {pack_path.joinpath(packagename)}.")

    # initialize package folder
    with open(pack_path.joinpath(packagename, "__init__.py"), "w") as f:
        f.write("# auto generated package initializer")



@app.command()
def createmodule(
    packagename: str, 
    modulename: str,
    environments: List[str]
):
    typer.echo(f"Creating {modulename} in {packagename} package...")
    typer.echo(f"{modulename} is to run in the following environments {environments}")


if __name__ == "__main__":
    app()