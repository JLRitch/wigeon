# standard imports
import pathlib as pl
import sqlite3
import sqlite3

# external imports

# project imports


class Connection(object):
    db_engines = [
        "sqlite",
        "mssql",
        "postgres"
    ]

    def __init__(self, db_engine: str):
        self.db_engine = db_engine

    def connect(
        self,
        **kwargs
    ):
        db_engines = {
            "sqlite": self.conn_sqlite,
            "mssql": self.conn_mssql,
            "postgres": self.conn_postgres
        }
        db_engines[self.db_engine](**kwargs)
        

    def conn_sqlite(
        self,
        **kwargs
    ):
        """
        Connect to a sqlite database and return cursor
        """
        conn = sqlite3.connect(kwargs["db_path"])
        return conn.cursor()

    def conn_mssql(self):
        raise NotImplementedError("conn_mssql is not yet implemented!")
    
    def conn_postgres(self):
        raise NotImplementedError("conn_postgres is not yet implemented!")