# standard imports
from argparse import ArgumentParser
import pathlib as pl

# external imports
import typer

# project imports



app = typer.Typer()

pack_path = pl.Path().cwd().joinpath("packages")

@app.command()
def createpackage(
    packagename: str
):
    typer.echo(f"Creating {packagename} package")
     # check if package exists
    try:
        pack_path.joinpath(packagename).mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise FileExistsError(f"A package with the name {packagename} already exists at {pack_path.joinpath(packagename)}.")

    with open(pack_path.joinpath(packagename, "__init__.py"), "w") as f:
        f.write("# auto generated package initializer")



@app.command()
def createmodule(
    packagename: str, 
    modulename: str
):
    pass


if __name__ == "__main__":
    app()