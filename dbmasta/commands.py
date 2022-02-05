# standard imports
from argparse import ArgumentParser
import pathlib as pl

# external imports
import typer

# project imports



app = typer.Typer()

pack_path = pl.Path().cwd().joinpath("dbmasta", "packages")

@app.command()
def createpackage(
    packagename: str
):
    typer.echo(f"Creating {packagename} package")
    pack_path.joinpath(packagename).mkdir(parents=True, exist_ok=True)
    with open(pack_path.joinpath("__init__.py"), "w") as f:
        f.write("# auto generated package initializer")



@app.command()
def createmodule(
    packagename: str, 
    modulename: str
):
    pass


if __name__ == "__main__":
    app()