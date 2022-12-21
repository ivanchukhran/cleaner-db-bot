from abc import abstractmethod

from connections.connector import Connector


class CommandProcessor:
    def __init__(self, connector: Connector):
        self.__connector = connector

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def update(self, id: int):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass


class MakerCommandProcessor(CommandProcessor):
    def create(self, name: str, description: str):
        self.__connector.execute("INSERT INTO MAKER (NAME, DESCRIPTION) VALUES (:name, :description)", name=name,
                                 description=description)

    def update(self, id: int, name: str, description: str):
        self.__connector.execute("UPDATE MAKER SET NAME=:name, DESCRIPTION=:description WHERE ID=:id", name=name,
                                 description=description, id=id)

    def delete(self, id: int):
        self.__connector.execute("DELETE FROM MAKER WHERE ID=:id", id=id)


class TakerCommandProcessor(CommandProcessor):
    def create(self, name: str, description: str):
        self.__connector.execute("INSERT INTO TAKER (NAME, DESCRIPTION) VALUES (:name, :description)", name=name,
                                 description=description)

        def update(self, id: int, name: str, description: str):
            self.__connector.execute("UPDATE TAKER SET NAME=:name, DESCRIPTION=:description WHERE ID=:id", name=name,
                                     description=description, id=id)

        def delete(self, id: int):
            self.__connector.execute("DELETE FROM TAKER WHERE ID=:id", id=id)
