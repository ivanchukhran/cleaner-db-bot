from abc import abstractmethod

from connections.connector import Connector


class QueryProcessor:
    def __init__(self, connector: Connector):
        self.__connector = connector

    @property
    def connector(self):
        return self.__connector

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_all_view(self):
        pass

    @abstractmethod
    def get_by_id(self, id: int):
        pass

    @abstractmethod
    def get_view_by_id(self, id: int):
        pass


class MakerQueryProcessor(QueryProcessor):
    def get_all(self):
        return self.connector.execute("SELECT * FROM MAKERS")

    def get_by_id(self, id: int):
        return self.connector.execute("SELECT * FROM MAKERS WHERE ID=:id", id=id)


class TakerQueryProcessor(QueryProcessor):
    def get_all(self):
        return self.connector.execute("SELECT * FROM TAKERS")

    def get_by_id(self, id: int):
        return self.connector.execute("SELECT * FROM TAKERS WHERE ID=:id", id=id)


class VictimQueryProcessor(QueryProcessor):
    def get_all(self):
        return self.connector.execute("SELECT * FROM VICTIMS")

    def get_by_id(self, id: int):
        return self.connector.execute("SELECT * FROM VICTIMS WHERE ID=:id", id=id)

    def get_view_by_id(self, id: int):
        return self.connector.execute("SELECT * FROM VICTIM_VIEW WHERE ID=:id", id=id)

    def get_all_view(self):
        return self.connector.execute("SELECT * FROM VICTIM_VIEW")


class OrderQueryProcessor(QueryProcessor):
    def get_all(self):
        return self.connector.execute("SELECT * FROM ORDERS")

    def get_by_id(self, id: int):
        return self.connector.execute("SELECT * FROM ORDERS WHERE ID=:id", id=id)

    def get_by_maker(self, maker_id: str):
        return self.connector.execute('SELECT * FROM MAKER_ORDER_LIST mol WHERE mol."maker"=:maker', maker_id=maker_id)

    def get_by_taker(self, taker_id: str):
        return self.connector.execute('SELECT * FROM ORDERS_VIEW '
                                      'WHERE "taker"=:taker_id AND '
                                      '"status"=(SELECT NAME FROM STATUSES WHERE ID = 4)',
                                      taker_id=taker_id)

    def get_for_taker(self, user_id: str):
        return self.connector.execute('SELECT * FROM ORDERS_VIEW WHERE ("weapon"='
                                      '(SELECT WEAPON_NAME '
                                      'FROM TAKER_WEAPON_VIEW WHERE TAKER_NAME=:user_id) OR "weapon" = \'ALL\') '
                                      'AND "status"=(SELECT NAME FROM STATUSES WHERE ID=3) AND "taker" IS NULL',
                                      user_id=user_id)

    def get_view_by_maker_id(self, maker_id: int):
        return self.connector.execute("SELECT * FROM ORDER_VIEW WHERE MAKER_ID=:maker_id", maker_id=maker_id)

    def get_view_by_taker_id(self, taker_id: int):
        return self.connector.execute("SELECT * FROM ORDER_VIEW WHERE TAKER_ID=:taker_id", taker_id=taker_id)

    def get_view_by_id(self, id: int):
        return self.connector.execute("SELECT * FROM ORDER_VIEW WHERE ID=:id", id=id)

    def get_all_view(self):
        return self.connector.execute("SELECT * FROM ORDER_VIEW")
