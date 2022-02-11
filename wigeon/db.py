# standard imports
import pathlib as pl
import os
import sqlite3
import datetime
from typing import TypedDict, Union, List

# external imports
# import pyodbc

# project imports
from wigeon.packages import Package


class Environment(TypedDict):
    connection_string: str
    server: str
    database: str
    username: str
    password: str

class Connector(object):

    db_engines = [
        "sqlite",
        "mssql",
        "postgres"
    ]

    def __init__(
        self,
        package: Package,
        environment: str=None
    ):
        self.db_engine = package.manifest["db_engine"]
        self.package = package
        self.environment = environment
        self.cnxn = None


    def connect(
        self,
        **kwargs
    ):
        db_engines = {
            "sqlite": self.conn_sqlite,
            "mssql": self.conn_mssql,
            "postgres": self.conn_postgres
        }
       
       # read environment name from Connector and collect envvariable names
       # extract environment variables to kwargs if variables exist
        if self.environment:
            print(f"Connecting to {self.environment} environment...")
            kwargs = self.package.manifest["environments"][self.environment]
            # dictionary comprehension ftwftwftw
            kwargs = {k:os.environ[v] for k,v in kwargs.items() if v}

         # run connection method based on db_engine for package
        db_engines[self.db_engine](**kwargs)
        return self.cnxn
        

    def conn_sqlite(
        self,
        **kwargs
    ) -> sqlite3.Connection:
        """
        Connect to a sqlite database and return conn
        """
        if kwargs["connectionstring"]:
            self.cnxn = sqlite3.connect(kwargs["connectionstring"])
            return self.cnxn

    def conn_mssql(self, **kwargs):
        raise NotImplementedError("conn_mssql is not yet implemented!")
    
    def conn_postgres(self, **kwargs):
        raise NotImplementedError("conn_postgres is not yet implemented!")

class Migration(object):

    def __init__(
        self,
        name: str,
        builds: List[str]
    ):
        self.name = name
        self.builds = builds
    
    def __str__(self):
        return f"name: {self.name}, builds: {self.builds}"
    
    def __repr__(self):
        return f"name: {self.name}, builds: {self.builds}"

    def run(
        self,
        package: Package,
        cursor: Union[sqlite3.Cursor, str], # TODO replace str with pyodbc.cursor once implemented
        user: str
    ):
        with open(package.pack_path.joinpath(self.name), "r") as f:
            query = f.read()
        cursor.execute(query)
        cursor.execute(
            "INSERT INTO changelog (migration_date, migration_name, applied_by) VALUES(:migration_date, :migration_name, :applied_by)",
            {
                "migration_date": datetime.datetime.now().strftime("%Y%m%d-%H%M"),
                "migration_name":self.name,
                "applied_by": user
            }
        )