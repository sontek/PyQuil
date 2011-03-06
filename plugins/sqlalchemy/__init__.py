# A Database and Query Analyze Tool
# Copyright (c) 2010-2011 John Anderson <sontek@gmail.com>
# License: GPLv3. See COPYING


from sqlalchemy import create_engine
from sqlalchemy.exc import ResourceClosedError
from lib.common import _

class SAQueryPlugin(object):
    def execute_query(self, connection_string, query):
        e = create_engine(connection_string)
        connection = e.connect()
        results = connection.execute(query)

        if results.rowcount > 0:
            return [(_('Results', ))], [(_('%d Row(s) modified' % results.rowcount), )]

        data = results.fetchall()

        e.dispose()
        connection.close()

        return results.keys(), data
