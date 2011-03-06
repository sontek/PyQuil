from sqlalchemy import create_engine
import pyodbc

class MSSQLQueryPlugin(object):
    def con(self):
        """ This method is required so we can get version 8 of TDS """
        return pyodbc.connect(self.connection_string)

    def execute_query(self, connection_string, query):
        self.connection_string = connection_string
        e = create_engine('mssql+pyodbc:///', creator=self.con)
        connection = e.connect()
        results = connection.execute(query)
        data = results.fetchall()
        e.dispose()
        connection.close()

        return results.keys(), data