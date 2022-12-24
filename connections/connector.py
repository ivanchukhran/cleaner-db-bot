from abc import abstractmethod

import oracledb


class Connector:
    def __init__(self, user: str = None, password: str = None, host: str = None, port: int = None, dsn: str = None):
        self.__pool = oracledb.create_pool(user=user, password=password, host=host, port=port, dsn=dsn)

    def connect(self):
        return self.__pool.acquire()

    def execute(self, query: str, *args, **kwargs):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, *args, **kwargs)
                conn.commit()
                return cursor.fetchall()

    def execute_without_return(self, query: str, *args, **kwargs):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, *args, **kwargs)
                conn.commit()

    def close(self):
        self.__pool.close()
