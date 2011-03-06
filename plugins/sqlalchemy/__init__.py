# A Database and Query Analyze Tool
# Copyright (c) 2010-2011 John Anderson <sontek@gmail.com>
# License: GPLv3. See COPYING


from sqlalchemy import create_engine
from sqlalchemy.exc import ResourceClosedError
from lib.common import _

class SAQueryPlugin(object):
    def execute_query(self, connection_string, query):
        try:
            e = create_engine(connection_string)
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
