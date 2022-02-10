# wigeon
DB Migrations for the continuous developer.

This is a framework and cli for building and deploying sql database migrations across your CI/CD-based development, just bring your sql skills and a database (or several)!

**STILL VERY MUCH A WORK IN PROGRESS!!**

## Features included
- Database package creation
- Auto-iterated migration naming
- Migration manifest management
- Migration build tagging
- connection manager
- connection arguments passed at runtime to support deployment across multiple
  enviroments
- migration changelog written to target database
- deploy/run sql script migrations

## Databases supported (at the moment)
- sqlite support
## Databases to support (soon)
- mssqlserver support
- postgres
- mysql

## To use:
NOTE: prefix every command with `python` if you are running directly from a clone of the repo.

Access help:
```bash
wigeon --help
```

Create `fly` package for `sqlite` with local, dev, qa, and prod environments:
```bash
wigeon createpackage fly sqlite --environments=local,dev,qa,prod
```

Create databases to connect to for each environment:
```bash
sqlite3
.open fly-local.sqlite
.open fly-dev.sqlite
.open fly-qa.sqlite
.open fly-prod.sqlite
```

(OPTIONAL) Set up environment variables and add to package manifest.json:
```bash
export LOCAL_CONNECTION_STRING=/home/usr/wigeon/fly-local.sqlite
export DEV_CONNECTION_STRING=/home/usr/wigeon/fly-dev.sqlite
export QA_CONNECTION_STRING=/home/usr/wigeon/fly-qa.sqlite
export PROD_CONNECTION_STRING=/home/usr/wigeon/fly-prod.sqlite
```

(OPTIONAL) Add environment variable names to manifest.json:
```json
  "environments": {
      "local": {
          "connectionstring": "LOCAL_CONNECTION_STRING",
          "server": null,
          "database": null,
          "username": null,
          "password:": null
      },
      "dev": {
          "connectionstring": "DEV_CONNECTION_STRING",
          "server": null,
          "database": null,
          "username": null,
          "password:": null
      },
      "qa": {
          "connectionstring": "QA_CONNECTION_STRING",
          "server": null,
          "database": null,
          "username": null,
          "password:": null
      },
      "prod": {
          "connectionstring": "PROD_CONNECTION_STRING",
          "server": null,
          "database": null,
          "username": null,
          "password:": null
      }
  }
```

Add migrations to the `fly` package with build tag of `0.0.1`:
```bash
wigeon createmigration initialize_db fly 0.0.1
wigeon createmigration add_people_table fly 0.0.1
wigeon createmigration add_cars_table fly 0.0.1
```

**SCRIPT SOME SQL IN THOSE MIGRATION FILES!!!**

List all migrations for the `fly` package:
```bash
wigeon listmigrations fly
```

Run migrations for the `fly` package (a local sqlite connection):
```bash
wigeon runmigrations fly --connstring=/path/to/exampledb.sqlite
```

OR

IF package's manifest.json is configured appropriately for a "local" environment
```bash
wigeon runmigrations fly --environment=local
```


## Requirements

### For gcc compiler on Ubuntu
```bash
sudo apt install build-essential
```
### For ODBC on Ubuntu
```bash
sudo apt-get install libssl-dev libffi-dev python3-dev
sudo apt-get install -y unixodbc-dev
```

### For mssql-server ODBC on Ubuntu
Found at:
https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15

```bash
sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

#Download appropriate package for the OS version
#Choose only ONE of the following, corresponding to your OS version

#Ubuntu 16.04
curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

#Ubuntu 18.04
curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

#Ubuntu 20.04
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

#Ubuntu 21.04
curl https://packages.microsoft.com/config/ubuntu/21.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

exit
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
sudo apt-get install -y unixodbc-dev
```