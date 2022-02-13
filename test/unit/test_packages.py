# standard imports
import unittest
import pathlib as pl
import time
import json
import shutil

# external imports

# project imports
from wigeon import packages

class TestPackage(unittest.TestCase):
    cur_dir = pl.Path().cwd()

    def test_create_dir(self):
        """
        Checks that directory was created
        """
        # inputs
        package = packages.Package("example")

        # cleanup folders before test
        shutil.rmtree(package.pack_path, ignore_errors=True)

        package.create(
            env_list=["dev", "qa"],
            db_engine="sqlite"
        )

        self.assertTrue(
            self.cur_dir.joinpath("packages", "example").exists()
        )
        self.assertTrue(
            self.cur_dir.joinpath("packages", "example", "manifest.json").exists()
        )

        expect_init_mani = {
            "db_engine": "sqlite",
            "environments": {
                "dev": {
                    "connectionstring": None,
                    "server": None,
                    "database": None,
                    "username": None,
                    "password": None
                },
                "qa": {
                    "connectionstring": None,
                    "server": None,
                    "database": None,
                    "username": None,
                    "password": None
                }
            },
            "migrations": []
        }

        with open(self.cur_dir.joinpath("packages", "example", "manifest.json"), "r") as f:
            out_man_js = json.load(f)
        
        self.assertEqual(out_man_js, expect_init_mani)

        # cleanup folders after test
        shutil.rmtree(package.pack_path, ignore_errors=True)
    
    def test_exists(self):
        """
        tests package existence methods
        """
        # inputs
        package_exist = packages.Package("exist")
        package_no_exist = packages.Package("noexist")

         # cleanup folders before test
        shutil.rmtree(package_exist.pack_folder, ignore_errors=True)
        shutil.rmtree(package_no_exist.pack_folder, ignore_errors=True)
        package_exist.pack_path.mkdir(parents=True)

        # assertions
        self.assertRaises(
            FileExistsError,
            package_exist.exists,
            raise_error_on_exists=True,
            raise_error_on_not_exist=False
        )

        self.assertRaises(
            FileExistsError,
            package_no_exist.exists,
            raise_error_on_exists=False,
            raise_error_on_not_exist=True
        )

        self.assertTrue(package_exist.exists(
            raise_error_on_exists=False,
            raise_error_on_not_exist=False
            )
        )
        self.assertFalse(package_no_exist.exists(
            raise_error_on_exists=False,
            raise_error_on_not_exist=False
            )
        )

        # cleanup folders after test
        shutil.rmtree(package_exist.pack_folder, ignore_errors=True)
        shutil.rmtree(package_no_exist.pack_folder, ignore_errors=True)
        

    def test_find_current_migration(self):
        """
        test returns 1 for None or sting value of migration name prefix + 1
        """
        # inputs
        package = packages.Package("example")

        self.assertEqual(
            package.find_current_migration(migration_list=[]),
            "0001"
        )
        self.assertEqual(
            package.find_current_migration(migration_list=[pl.Path("0001-migration.sql")]),
            "0002"
        )
        self.assertRaises(
            ValueError,
            package.find_current_migration,
            migration_list=[pl.Path("9999-migration.sql")]
        )

    def test_list_migrations(self):
        """
        test migration file reads
        """
        self.maxDiff = None
        no_migrations = packages.Package("no_migrations")
        with_migrations = packages.Package("with_migrations")

        # cleanup folders before test
        shutil.rmtree(no_migrations.pack_folder, ignore_errors=True)
        shutil.rmtree(with_migrations.pack_folder, ignore_errors=True)

        # create migrations
        with_migrations.pack_path.mkdir(parents=True, exist_ok=True)
        no_migrations.pack_path.mkdir(parents=True, exist_ok=True)
        mig_path = with_migrations.pack_path.joinpath("0001-migration1.sql")
        with open(mig_path, 'w') as f:
            f.write('emptyfile')
        
        # assertions
        self.assertEqual(
            no_migrations.list_migrations(),
            []
        )
        self.assertEqual(
            with_migrations.list_migrations(),
            [mig_path]
        )

        # cleanup folders after test
        shutil.rmtree(no_migrations.pack_folder, ignore_errors=True)
        shutil.rmtree(with_migrations.pack_folder, ignore_errors=True)


    def test_delete_dir(self):
        """
        Checks that directory was created
        """
        # inputs
        package = packages.Package("example")
        # cleanup folders after test
        shutil.rmtree(package.pack_path, ignore_errors=True)
        package.pack_path.mkdir(parents=True, exist_ok=True)
        # sleep to ensure files are given time to create
        time.sleep(1)
        package.delete()
        # sleep to ensure files are given time to delete
        time.sleep(1)
        self.assertFalse(
            self.cur_dir.joinpath("packages", "example").exists()
        )


if __name__ == '__main__':
    unittest.main()