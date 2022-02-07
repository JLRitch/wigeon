# standard imports
import unittest
import pathlib as pl
import time

# external imports

# project imports
from wigeon import packages

class TestPackage(unittest.TestCase):

    # initialize package object for testing
    package = packages.Package("example")
    cur_dir = pl.Path().cwd()

    def test_create_dir(self):
        """
        Checks that directory was created
        """
        self.package.create(
            env_list=["dev", "qa"],
            db_engine="sqlite"
        )
        self.assertTrue(
            self.cur_dir.joinpath("packages", "example").exists()
        )

    def test_delete_dir(self):
        """
        Checks that directory was created
        """
        # sleep to ensure files are given time to create
        time.sleep(.5)
        self.package.delete()
        # sleep to ensure files are given time to delete
        time.sleep(1)
        self.assertFalse(
            self.cur_dir.joinpath("packages", "example").exists()
        )

if __name__ == '__main__':
    unittest.main()