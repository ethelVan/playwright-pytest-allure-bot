import psycopg2
import psycopg2.extras


class PostgresDB(object):
    def __init__(self, config):
        self.conn = psycopg2.connect(cursor_factory=psycopg2.extras.RealDictCursor, **config)
        self.cursor = self.conn.cursor()

    def __del__(self):
        """
        PgsqlDB destructor to close the cursor and connection
        :return:
        """
        self.cursor.close()
        self.conn.close()

    def queryAll(self, sql):
        """
        Execute a SQL query and return all the rows
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        return [dict(row) for row in self.cursor.fetchall()]

    def queryMany(self, sql, n):
        """
        Execute a SQL query and return n rows
        :param sql:
        :param n:
        :return:
        """
        self.cursor.execute(sql)
        return dict(self.cursor.fetchmany(n))

    def operate_sql(self, sql, params=None, DML=True):
        """
        DB operation function
        DML: True for DML operation, False for DDL operation
        :param sql:
        :param params:
        :return:
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, params)
                self.conn.commit()
        except Exception as e:
            if DML:
                self.conn.rollback()
            raise e
        return cursor.rowcount


if __name__ == '__main__':
    config = {
        'host': 'localhost',
        'port': '5432',
        'database': 'test',
        'user': 'postgres',
        'password': 'postgres'
    }
    db = PostgresDB(config)
    sql = "SELECT * FROM test_table"
    print(db.queryAll(sql))  # return all the rows
