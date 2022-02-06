# standard imports
import pathlib as pl
import json
from typing import List

# external imports

# project imports


class Package(object):
    pack_folder = pl.Path().cwd().joinpath("packages")

    def __init__(
        self,
        packagename:str
    ):
        self.pack_path = Package.pack_folder.joinpath(packagename)

    def exists(
        self,
        packagename: str,
        raise_error_on_exists: bool=False,
        raise_error_on_not_exist: bool=True
    ) -> bool:
        """
        Checks if a given package exists. Defaults to error if package is not present.
        """
        package_exists = Package.pack_folder.joinpath(packagename).exists()
        if package_exists and raise_error_on_exists:
            raise FileExistsError(
                f"A package with the name {packagename} already exists at {Package.pack_folder.joinpath(packagename)}."
            )
        elif (not package_exists) and (raise_error_on_not_exist):
            raise FileExistsError(
                f"A package with the name {packagename} does not exist at {Package.pack_folder.joinpath(packagename)}."
            )
        return package_exists
    
    def create(
        self,
        env_list: list,
        db_engine: str
    ):
        """
        Package.create initializes a package in the root/packages/ directory and
        supplies an __init__.py and manifest.json
        """
        # initialize package folder
        self.pack_path.mkdir(parents=True)
        with open(self.pack_path.joinpath("__init__.py"), "w") as f:
            f.write("# auto generated package initializer")
        
        # initialize package manifest
        manifest_template = {}
        manifest_template["db_engine"] = db_engine
        manifest_template["environments"] = {}
        for e in env_list:
            manifest_template["environments"][e] = {"connection": "TODO"}
        manifest_template["migrations"] = []

        with open(self.pack_path.joinpath("manifest.json"), "w") as f:
            json.dump(manifest_template, f, indent=4)
    
    def list_migrations(
        self,
        packagename: str
    ) -> list:
        """
        list_mgrations reads a package and returns a list of all the migrations
        """
        return [f for f in Package.pack_folder.joinpath(packagename).iterdir() if f.suffix == ".sql"]

    def find_current_migration(
        self,
        migration_list: List[pl.Path]
    ) -> str:
        """
        Parses migration files and finds version number to return the latest as a string.
        
        Assumes migration filename convention of:
        ####-<migration_name>.sql
        """
        # BUG latest migration algorithm is erroring sometimes
        if migration_list == []:
            latest_migration_int = 0
        else:
            # sort migration list to ensure largest number is the latest
            migration_list = sorted(migration_list)
            latest_migration_int = int(
                str(
                    migration_list[-1].name
                )[0:4]
            )
        
        # increment migration guid
        current_migration = latest_migration_int + 1
        # check if migration greater than limit of 4 characters
        if current_migration > 9999:
            raise ValueError(
                f"Current migration number ({current_migration}) cannot exceed 9999, max characters allowed in migration guid is 4"
            )
        # return 4 character migration guid string left padded with zeros
        return str(current_migration).zfill(4)

    def read_manifest(self):
        with open(self.pack_path.joinpath("manifest.json"), "r") as f:
            self.manifest = json.load(f)

    def write_manifest(self):
        with open(self.pack_path.joinpath("manifest.json"), "w") as f:
            json.dump(self.manifest, f, indent=4)
    
    def add_migration(
        self,
        current_migration: str,
        migration_name: str,
        builds: List[str]
    ):
        with open(self.pack_path.joinpath(f"{current_migration}-{migration_name}.sql"), "w") as f:
            f.write("-- TODO build migration code")
        self.read_manifest()
        self.manifest["migrations"].append(
            {
                "name": f"{current_migration}-{migration_name}.sql",
                "builds": [b for b in builds]
            }
        )
        self.write_manifest()

class manifest(object):

    def __init__(self):
        pass