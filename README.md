# dbmasta (to be renamed, pipeybase?) 
This is a framework for building and deploying sql database migrations across your CI/CD-based applications!

## Features included
- Database package creation
- Auto-serialized Migration creation
- Migration manifest management
- Migration tagging
## Features to build
- json manifests managed via environment variables
- migration changelog written to target database
- connection manager
- connection via environment variables
- deploy/run sql script migrations
- sqlite support
- mssqlserver support

## To use:
Access help
```shell
python3 dbmasta --help
```

Create package
```shell
python3 -m dbmasta createpackage devdb sqlite --environments=local,dev,qa,prod
```

Add migrations to a package
```shell
python3 -m dbmasta createmigration initialize_db devdb
python3 -m dbmasta createmigration add_people_table devdb
python3 -m dbmasta createmigration add_cars_table devdb --tags=mercedes,bugati
```

List all migrations
```shell
python3 -m dbmasta listmigrations devdb
```