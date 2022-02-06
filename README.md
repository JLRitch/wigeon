# wigeon (to be renamed, pipeybase, dbdonedid?) 
This is a framework for building and deploying sql database migrations across your CI/CD-based applications!

## Features included
- Database package creation
- Auto-serialized Migration creation
- Migration manifest management
- Migration build tagging
## Features to build
- json manifests managed via environment variables
- migration changelog written to target database
- connection manager
- connection via environment variables
- deploy/run sql script migrations
- sqlite support
- mssqlserver support

## To use (FROM GIT REPO):
Access help:
```shell
python3 wigeon --help
```

Create `fly` package for `sqlite` with local, dev, qa, and prod environments:
```shell
python3 -m wigeon createpackage fly sqlite --environments=local,dev,qa,prod
```

Add migrations to the `fly` package with build tag of `0.0.1`:
```shell
python3 -m wigeon createmigration initialize_db fly 0.0.1
python3 -m wigeon createmigration add_people_table fly 0.0.1
python3 -m wigeon createmigration add_cars_table fly 0.0.1
```

List all migrations for the `fly` package:
```shell
python3 -m wigeon listmigrations fly
```

## To use (FROM PIP INSTALL):
Access help:
```shell
wigeon --help
```

Create `fly` package for `sqlite` with local, dev, qa, and prod environments:
```shell
wigeon createpackage fly sqlite --environments=local,dev,qa,prod
```

Add migrations to the `fly` package with build tag of `0.0.1` :
```shell
wigeon createmigration initialize_db fly 0.0.1
wigeon createmigration add_people_table fly 0.0.1
wigeon createmigration add_cars_table fly 0.0.1
```

List all migrations for the `fly` package:
```shell
wigeon listmigrations fly
```