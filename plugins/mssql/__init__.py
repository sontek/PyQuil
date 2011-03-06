# A Database and Query Analyze Tool
# Copyright (c) 2010-2011 John Anderson <sontek@gmail.com>
# License: GPLv3. See COPYING


from sqlalchemy import create_engine
from sqlalchemy.exc import ResourceClosedError
import pyodbc

from lib.common import _

class MSSQLQueryPlugin(object):
    def __con(self):
        """ This method is required so we can get version 8 of TDS """
        return pyodbc.connect(self.connection_string)

    def __init__(self, engine=None):
        self.engine = engine

    def connect(self, connection_string):
        self.connection_string = connection_string

        if not self.engine:
            self.engine = create_engine('mssql+pyodbc:///', creator=self.__con)

        self.connection = self.engine.connect()

    def disconnect(self):
        self.connection.close()

    def execute_query(self, query):
        results = self.connection.execute(query)

        # if cursor is closed, we aren't fetching rows
        if results.closed:
            return [(_('Results', ))], [(_('%d Row(s) modified' % results.rowcount), )]

        data = results.fetchall()

        return results.keys(), data
