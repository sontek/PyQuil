
## Setting it up with Virtualenv
Note: PyGTK/pygobject/etc isn't quite ready to be in a virtualenv,
you must use mkvirtualenv --system-site-packages to use your operating system
site packages to get those

# Experimental virtualenv docs
Install pygobject header files
Install header files for unixODBC.
Install pycairo header files

In Fedora:
yum install unixODBC-devel
yum install pygobject2-devel gobject-introspection-devel
yum install pycairo-devel

Download pygobject:
http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.0/pygobject-3.0.4.tar.xz

./configure --prefix=<your virtualenv>
make
make install



Download pycairo:
./waf configure --prefix=<your virtualenv>
./waf build
./waf install



Download pygtk:
http://ftp.gnome.org/pub/GNOME/sources/pygtk/2.24/pygtk-2.24.0.tar.bz2

./configure --prefix=<your virtualenv>
make



Then install the python libraries:
pip install -r requirements.txt

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
