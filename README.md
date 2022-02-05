# dbmasta (to be renamed, pipeybase?) 
This is a framework for building and deploying sql database migrations across your CI/CD-based applications!
# Features to build
- define and run sql script packages
- json manifests managed via environment variables
- json manifests 
- auto generate guid for modules
- migration changelog written to target database
- connection manager
- connection via environment variables

## To use:
Access help
```shell
python3 dbmasta --help
```

Create package
```shell
python3 -m dbmasta createpackage devdb sqlite --environments=local,dev,qa,prod
```

Add migration to package
```shell
python3 -m dbmasta createmigration initialize_db devdb
python3 -m dbmasta createmigration add_people_table devdb
python3 -m dbmasta createmigration add_cars_table devdb
python3 -m dbmasta createmigration add_boats_table devdb
```

List all packages
```shell
python3 -m dbmasta listmigrations devdb
```