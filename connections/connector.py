from abc import abstractmethod

import oracledb

class Connector:
    def __init__(self, user: str, password: str, host: str, port: int):
        self.__pool = oracledb.create_pool(user=user, password=password, host=host, port=port)

    def connect(self):
        return self.__pool.acquire()

    def execute(self, query: str, *args, **kwargs):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, *args, **kwargs)
                return cursor.fetchall()

    def close(self):
        self.__pool.close()
