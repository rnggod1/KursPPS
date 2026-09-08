import psycopg2

class Database:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname="KursPPS",
                user="postgres",
                password="1234",
                host="localhost",
                port="5432"
            )
            self.connection.set_client_encoding('UTF8')
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            self.connection.commit()
            return result
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()

    def execute_insert(self, query, params=None):
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            result = cursor.fetchone()[0]
            self.connection.commit()
            return result
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()

    def execute_update(self, query, params=None):
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            rowcount = cursor.rowcount
            self.connection.commit()
            return rowcount
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()