## SQL Alchemy Plugin
You need to provide protocol and query string for the conn string to work

### sqlite
sqlite:///test.db


### Postgres:
postgresql+psycopg2://user:password@host:port/dbname

### All others:
http://www.sqlalchemy.org/docs/dialects/


## MSSQL Plugin
You need to setup FreeTDS and unixodbc:
### example odbcinst.ini
    [FreeTDS]
        Description = TDS driver (Sybase/MS SQL)
        Driver = /usr/lib/odbc/libtdsodbc.so
        Setup = /usr/lib/odbc/libtdsS.so
        CPTimeout =
        CPReuse =

### example freetds.conf
    [orchid]
        host = 127.0.0.1 
        port = 1433
        tds version = 8.0

DRIVER={FreeTDS};SERVERNAME=orchid;UID=sa;PWD=pwd;DATABASE=db'
 - Driver is defined in odbcinst.ini
 - ServerName is defined freetds.conf

If you are on windows use DRIVER={SQL SERVER} instead.

MSSQL driver does not support "SELECT \*", you must provide the columns you want.
