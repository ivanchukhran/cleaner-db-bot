from abc import abstractmethod

from connections.connector import Connector


class QueryProcessor:
    def __init__(self, connector: Connector):
        self.__connector = connector

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id: int):
        pass


class MakerQueryProcessor(QueryProcessor):
    def get_all(self):
        return self.__connector.execute("SELECT * FROM MAKER")

    def get_by_id(self, id: int):
        return self.__connector.execute("SELECT * FROM MAKER WHERE ID=:id", id=id)


class TakerQueryProcessor(QueryProcessor):
    def get_all(self):
        return self.__connector.execute("SELECT * FROM TAKER")

    def get_by_id(self, id: int):
        return self.__connector.execute("SELECT * FROM TAKER WHERE ID=:id", id=id)
