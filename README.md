# Features to build!
- define and run sql script packages
- json manifests managed via environment variables
- auto generate guid for modules
- migration changelog written to target database
- connection manager
- connection via environment variables


## To use:
Access help
```shell
python3 dbmasta -help
```

Create package
```shell
python3 dbmasta createpackage devdb sqlite --environments=dev,qa,uat,prod
```

Add module to package
```shell
python3 dbmasta createpackage devdb <module_name>
```