# standard imports
from email.policy import default
import platform
from argparse import ArgumentParser
import pathlib as pl
from pydoc import cli
from typing import List
import getpass

# external imports
import click

# project imports
import wigeon
from wigeon.packages import Package
from wigeon.levels import get_level


###############
### Module-level variables
###############
user = getpass.getuser()

###############
### Call back functions
###############
def print_version(
    ctx: click.Context,
    param: click.Parameter,
    value: bool
) -> None:
    if not value or ctx.resilient_parsing:
        return
    click.echo(
        f"Running wigeon version {wigeon.__version__} with {platform.python_implementation()} {platform.python_version()} on {platform.system()}"
    )
    ctx.exit()

def nerd(
    ctx: click.Context,
    param: click.Parameter,
    value: bool
) -> None:
    """
    For the funnies.
    """
    if not value or ctx.resilient_parsing:
        return
    click.echo("wigeon recalls... ", nl=False)
    click.echo(click.style(get_level(),  bg='blue', fg='white'))
    ctx.exit()


###############
### cli base
###############
@click.group("wigeon")
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Display the wigeon version and exit.",
)
@click.option(
    "--nerd",
    is_flag=True,
    callback=nerd,
    expose_value=False,
    is_eager=True,
    help="wigeon nerds"
)
def app():
    # present only for sub-commands
    pass


###############
### create commands
###############
@app.group("create")
def create():
     # present only for sub-commands
    pass

@create.command("package")
@click.option(
    "-n",
    "--name",
    type=str,
    help="The name of the package you want to create"
)
@click.option(
    "-d",
    "--dbtype",
    type=str,
    help="The db type this package will connect to (either sqlite or mssql currently)"
)
@click.option(
    "-e",
    "--environments",
    type=str,
    default="local,dev,qa,prod",
    help="A comma delmimted string of the enviornments in your db deployment "
)
def create_package(
    name: str,
    dbtype: str,
    environments: str
):
    """
    createpackage initializes a package of migrations in the current
    environment. A package is linked directly to a database type and the
    deployment environments in your ci/cd pipeline.

    dbtype either sqlite, mssql, or postgres
    """
    click.echo(f"Creating {name} package")
    click.echo(f"{name}'s Database type is {dbtype}")
    click.echo(f"{name}'s environments include {environments.split(',')}")
    # check if package exists
    package = Package(packagename=name)
    package.exists(
        raise_error_on_exists=True,
        raise_error_on_not_exist=False
    )

    # initialize package folder
    package.create(
        env_list=environments.split(","),
        db_engine=dbtype
    )

    click.echo(click.style(f"Successfully created package: {name}!", fg="green"))

@create.command("migration")
@click.option(
    "-n",
    "--name",
    type=str,
    help="The name of the migration you want to create"
)
@click.option(
    "-p",
    "--package",
    type=str,
    help="The name of the package you want to add a migration to"
)
@click.option(
    "-b",
    "--build",
    type=str,
    default=None,
    help="The build version you want to apply to the migration (use #.#.# format)"
)
def create_migration(
    name: str,
    package: str,
    build: str    
):
    """
    createmigration initializes a .sql module for a migration
    """
    click.echo(f"Creating {name} in {package} package...")
    # check if package exists
    package = Package(packagename=package)
    package.exists()
    # find latest migration number
    current_migrations = package.list_local_migrations()
    current_migr_num = package.find_current_migration(migration_list=current_migrations)
    click.echo(f"Current migration is: {current_migr_num}")
    # create migration
    package.add_migration(
        current_migration=current_migr_num,
        migration_name=name,
        builds=[build] # TODO enable multiple build support at later date
    )
    click.echo(click.style(f"Successfully created {current_migr_num}-{name}.sql!!", fg="green"))


###############
### package commands
###############
@app.command("package")
@click.option(
    "-n",
    "--name",
    type=str,
    help="The name of the package you want to use"
)
@click.option(
    "-s",
    "--server",
    type=str,
    default=None,
    help="The server address for your db (host:port)"
)
@click.option(
    "-b",
    "--buildtag",
    type=str,
    default=None,
    help="The build version you want to run up to (format #.#.#)"
)
@click.option(
    "-d",
    "--database",
    type=str,
    default=None,
    help="The name of the database"
)
@click.option(
    "-u",
    "--username",
    type=str,
    default=None,
    help="The db server username"
)
@click.option(
    "-p",
    "--password",
    type=str,
    default=None,
    help="The db server password"
)
@click.option(
    "-dr",
    "--driver",
    type=str,
    default=None,
    help="The driver to be used to connect (ODBC)"
)
@click.option(
    "-c",
    "--conn_string",
    type=str,
    default=None,
    help="The full connection string"
)
@click.option(
    "-e",
    "--environment",
    type=str,
    default=None,
    help="The name of the environment you are targeting (forces read of env vars)"
)
@click.option(
    "-ct",
    "--connect_test",
    is_flag=True,
    type=bool,
    default=False,
    expose_value=True,
    is_eager=True,
    help="Force use of env variable as named in manifest environments",
)
@click.option(
    "-l",
    "--list_migrations",
    is_flag=True,
    type=bool,
    default=False,
    expose_value=True,
    is_eager=True,
    help="Display the migrations for a package and exit",
)
@click.option(
    "-m",
    "--migrate",
    is_flag=True,
    type=bool,
    default=False,
    expose_value=True,
    is_eager=True,
    help="Run migrations to target db",
)
@click.option(
    "-a",
    "--run_all",
    is_flag=True,
    type=bool,
    default=False,
    expose_value=True,
    is_eager=True,
    help="Run all migrations to target db",
)
def package(
    name:str,
    list_migrations: bool,
    server: str,
    database: str,
    username: str,
    password: str,
    driver: str,
    conn_string: str,
    environment: str,
    connect_test: bool,
    migrate: bool,
    run_all: bool,
    buildtag: str
):
    # check if package exists and read data
    package = Package(packagename=name)
    package.exists()
    package.read_manifest()

    # list migration flag option
    if list_migrations:
        click.echo(f"Found following migrations for {name}:")
        current_migrations = package.list_local_migrations()
        for m in sorted(current_migrations):
            click.echo(f"    {m.name}")
        current_migr = package.find_current_migration(migration_list=current_migrations)
        click.echo(click.style(f"Current migration would be: {current_migr}", fg="yellow"))
        return

    # create connection, return cursor
    cnxn = package.connect(
        server=server,
        database=database,
        username=username,
        password=password,
        driver=driver,
        connectionstring=conn_string,
        environment=environment
    )
    click.echo(click.style(f"Successfully connected to {package.manifest['db_engine']} database!!!!", fg="green"))

    # connect_test flag option
    if connect_test:
        cnxn.close()
        return
    
    # migrate flag option
    if migrate:
        # initialize changelog table if not exists and add columns
        # change_id, migration_date, applied_by(username), and migration_name(.sql filename)
        package.init_changelog()

        # find migrations already in target database
        db_migrations = package.list_db_migrations()

        # find migrations in manifest
        # filter to migrations only with certain build tag
        mani_migrations = package.list_manifest_migrations(buildtag=buildtag)
        click.echo(f"Migrations in manifest: {mani_migrations}")


        # find migrations alead in the database
        # duplicate_migrations = [m.name for m in mani_migrations if m.name in db_migrations]
        duplicate_migrations = package.compare_migrations(
            manifest_migrations=mani_migrations,
            db_migrations=db_migrations
        )
        click.echo(f"Migrations already in db: {duplicate_migrations}")
        # remove duplicate migrations from manifest, unless all option is given
        if not run_all:
            mani_migrations = [m for m in mani_migrations if m.name not in db_migrations]

        click.echo(f"Migrations to run: {mani_migrations}")
        if len(mani_migrations) > 0:
            for mig in mani_migrations:
                if mig.name in db_migrations:
                    duplicate_migrations.append(mig.name)
                    continue
                click.echo(f"Running migration {mig}... ")
                mig.run(
                    package_path=package.pack_path,
                    cursor=package.cursor,
                    user=user,
                    db_engine=package.manifest["db_engine"]
                )
            click.echo(click.style(f"Successfully migrated {len(mani_migrations)} migrations", fg="green"))
            package.connection.commit()
            package.connection.close()
        else:
            click.echo("No migrations to migrate, wigeon is flying home...")
        print()


if __name__ == "__main__":
    app()