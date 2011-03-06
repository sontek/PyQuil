from sqlalchemy import create_engine

class SAQueryPlugin(object):
    def execute_query(self, connection_string, query):
        e = create_engine(connection_string)

        connection = e.connect()
        results = connection.execute(query)
        data = results.fetchall()
        e.dispose()
        connection.close()

        return results.keys(), data
