# A Database and Query Analyze Tool
# Copyright (c) 2010-2011 John Anderson <sontek@gmail.com>
# License: GPLv3. See COPYING


from sqlalchemy import create_engine
from sqlalchemy.exc import ResourceClosedError
import pyodbc

from lib.common import _

class MSSQLQueryPlugin(object):
    def con(self):
        """ This method is required so we can get version 8 of TDS """
        return pyodbc.connect(self.connection_string)

    def execute_query(self, connection_string, query):
        try:
            self.connection_string = connection_string
            e = create_engine('mssql+pyodbc:///', creator=self.con)
            connection = e.connect()
            results = connection.execute(query)
            data = results.fetchall()
        except ResourceClosedError as exc:
            if str(exc) == 'This result object does not return rows. It has been closed automatically.':
                return [(_('Results', ))], [(_('%d Row(s) modified' % results.rowcount), )]
            else:
                raise exc
        finally:
            e.dispose()
            connection.close()

        return results.keys(), data
